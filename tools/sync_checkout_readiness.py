from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state"
CONFIG_EXAMPLE = ROOT / "config" / "config.example.json"
CONFIG_PUBLIC = ROOT / "config" / "config.public.json"
CONFIG_LOCAL = ROOT / "config" / "config.local.json"
SNAPSHOT_PATH = STATE / "checkout-readiness-snapshot.json"
USER_AGENT = "daily-autodigital-shelf-checkout-readiness-sync/1.0"
BODY_LIMIT = 128_000


def read_json(path: Path, fallback: dict[str, Any] | None = None) -> dict[str, Any]:
    if not path.exists():
        return fallback or {}
    return json.loads(path.read_text(encoding="utf-8"))


def deep_update(base: dict[str, Any], override: dict[str, Any]) -> None:
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            deep_update(base[key], value)
        else:
            base[key] = value


def load_config() -> dict[str, Any]:
    config = read_json(CONFIG_EXAMPLE)
    if CONFIG_PUBLIC.exists():
        deep_update(config, read_json(CONFIG_PUBLIC))
    if CONFIG_LOCAL.exists():
        deep_update(config, read_json(CONFIG_LOCAL))
    return config


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "candidate"


def safe_public_url(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    parsed = urllib.parse.urlparse(text)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return ""
    return text


def is_counter_route(url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.lower()
    return (
        path.endswith("/support/go")
        or "/support/go/" in path
        or path.endswith(".zip")
        or "/downloads/" in path
        or path.endswith("/today.zip")
        or path.endswith("/current.zip")
    )


def candidate_records(config: dict[str, Any]) -> list[dict[str, Any]]:
    monetization = config.get("monetization", {})
    records: list[dict[str, Any]] = []
    for raw in monetization.get("checkout_candidates") or []:
        if not isinstance(raw, dict):
            continue
        label = str(raw.get("label") or raw.get("name") or "Checkout candidate").strip()
        url = safe_public_url(raw.get("url"))
        records.append(
            {
                "id": slugify(label),
                "label": label,
                "kind": str(raw.get("kind") or "external_destination").strip().lower(),
                "status": str(raw.get("status") or "requires_verification").strip().lower(),
                "url": url,
                "daily_shelf_checkout": bool(raw.get("daily_shelf_checkout") and url),
                "publicly_linkable": bool(raw.get("publicly_linkable") and url),
            }
        )
    return records


def page_title(html: str) -> str:
    match = re.search(r"<title[^>]*>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return ""
    return re.sub(r"\s+", " ", match.group(1)).strip()[:160]


def compact_text(html: str, limit: int = 360) -> str:
    text = re.sub(r"<script\b[^>]*>.*?</script>", " ", html, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<style\b[^>]*>.*?</style>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]


def fetch_candidate(candidate: dict[str, Any], timeout: int) -> dict[str, Any]:
    url = str(candidate.get("url") or "")
    base = {
        "id": candidate.get("id", ""),
        "label": candidate.get("label", ""),
        "kind": candidate.get("kind", ""),
        "configured_status": candidate.get("status", ""),
        "configured_daily_shelf_checkout": bool(candidate.get("daily_shelf_checkout")),
        "url": url,
        "checked": False,
        "counter_route_skipped": False,
        "reachable": False,
        "status_code": 0,
        "final_url": "",
        "content_type": "",
        "title": "",
        "signals": {},
        "error": "",
    }
    if not url:
        return {**base, "error": "no public URL configured"}
    if is_counter_route(url):
        return {**base, "counter_route_skipped": True, "error": "counter route skipped"}

    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status_code = int(getattr(response, "status", 0) or response.getcode() or 0)
            final_url = str(response.geturl() or url)
            content_type = str(response.headers.get("content-type") or "")[:160]
            body = response.read(BODY_LIMIT).decode("utf-8", errors="replace")
    except Exception as exc:
        return {**base, "error": str(exc)[:240]}

    lowered = body.lower()
    text_sample = compact_text(body)
    title = page_title(body)
    return {
        **base,
        "checked": True,
        "reachable": 200 <= status_code < 400,
        "status_code": status_code,
        "final_url": final_url[:320],
        "content_type": content_type,
        "title": title,
        "signals": {
            "contains_daily_shelf": "daily shelf" in lowered or "daily autodigital shelf" in lowered,
            "contains_calmsprout": "calmsprout" in lowered or "calm sprout" in lowered,
            "contains_square": "square" in lowered or "app.squareup.com" in final_url.lower(),
            "contains_paypal": "paypal" in lowered,
            "contains_checkout_terms": any(term in lowered for term in ["checkout", "add to cart", "buy now", "purchase"]),
            "contains_sold_out": "sold out" in lowered,
            "contains_cbd_terms": "cbd" in lowered or "south carolina" in lowered,
            "text_sample": text_sample,
        },
        "error": "",
    }


def blank_snapshot(config: dict[str, Any], error: str = "") -> dict[str, Any]:
    candidates = candidate_records(config)
    return {
        "version": 1,
        "kind": "daily-shelf-checkout-readiness-snapshot",
        "fetched_at": dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat(),
        "sync_ok": False,
        "sync_error": error,
        "checked_url_count": 0,
        "reachable_url_count": 0,
        "counter_route_skip_count": 0,
        "configured_candidate_count": len(candidates),
        "verified_product_checkout_count": 0,
        "public_support_reachable": False,
        "daily_shelf_checkout_reachable": False,
        "checks": [],
        "boundary": "This public monitor checks configured destinations without triggering support-intent redirects or download counters. It does not prove payments or daily revenue.",
    }


def build_snapshot(config: dict[str, Any], timeout: int) -> dict[str, Any]:
    candidates = candidate_records(config)
    checks = [fetch_candidate(candidate, timeout) for candidate in candidates]
    checked_url_count = sum(1 for item in checks if item.get("checked"))
    reachable_url_count = sum(1 for item in checks if item.get("reachable"))
    counter_route_skip_count = sum(1 for item in checks if item.get("counter_route_skipped"))
    verified_product_checkout_count = sum(
        1
        for item in checks
        if item.get("reachable")
        and item.get("configured_daily_shelf_checkout")
        and bool((item.get("signals") or {}).get("contains_daily_shelf"))
        and bool((item.get("signals") or {}).get("contains_checkout_terms"))
    )
    public_support_reachable = any(
        item.get("reachable") and str(item.get("kind") or "") == "support"
        for item in checks
    )
    return {
        "version": 1,
        "kind": "daily-shelf-checkout-readiness-snapshot",
        "fetched_at": dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat(),
        "sync_ok": True,
        "sync_error": "",
        "checked_url_count": checked_url_count,
        "reachable_url_count": reachable_url_count,
        "counter_route_skip_count": counter_route_skip_count,
        "configured_candidate_count": len(candidates),
        "verified_product_checkout_count": verified_product_checkout_count,
        "public_support_reachable": public_support_reachable,
        "daily_shelf_checkout_reachable": verified_product_checkout_count > 0,
        "checks": checks,
        "boundary": "This public monitor checks configured destinations without triggering support-intent redirects or download counters. It does not prove payments or daily revenue.",
    }


def write_snapshot(snapshot: dict[str, Any]) -> None:
    STATE.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_PATH.write_text(json.dumps(snapshot, indent=2, sort_keys=True), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync public checkout-readiness destination checks into local state.")
    parser.add_argument("--timeout", type=int, default=20, help="HTTP timeout in seconds.")
    parser.add_argument("--allow-stale", action="store_true", default=True, help="Keep the last snapshot if sync fails.")
    args = parser.parse_args()

    config = load_config()
    try:
        snapshot = build_snapshot(config, args.timeout)
        write_snapshot(snapshot)
        print(
            json.dumps(
                {
                    "status": "ok",
                    "checked_url_count": snapshot["checked_url_count"],
                    "reachable_url_count": snapshot["reachable_url_count"],
                    "verified_product_checkout_count": snapshot["verified_product_checkout_count"],
                },
                indent=2,
            )
        )
        return 0
    except Exception as exc:
        if SNAPSHOT_PATH.exists() and args.allow_stale:
            stale = read_json(SNAPSHOT_PATH)
            stale["last_sync_error"] = str(exc)
            stale["last_sync_error_at"] = dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()
            write_snapshot(stale)
            print(json.dumps({"status": "stale", "error": str(exc)}, indent=2))
            return 0
        snapshot = blank_snapshot(config, str(exc))
        write_snapshot(snapshot)
        print(json.dumps({"status": "blank", "error": str(exc)}, indent=2), file=sys.stderr)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
