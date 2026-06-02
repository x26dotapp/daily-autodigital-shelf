from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
STATE = ROOT / "state"
CONFIG_EXAMPLE = ROOT / "config" / "config.example.json"
CONFIG_PUBLIC = ROOT / "config" / "config.public.json"
CONFIG_LOCAL = ROOT / "config" / "config.local.json"
INDEXNOW_STATE = STATE / "indexnow-state.json"


def fail(message: str) -> None:
    raise RuntimeError(message)


def read_json(path: Path, fallback: dict[str, Any] | None = None) -> dict[str, Any]:
    if not path.exists():
        if fallback is not None:
            return fallback
        fail(f"Missing JSON file: {path}")
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


def site_base(config: dict[str, Any]) -> str:
    base = str(config["site"].get("base_url", "")).strip().rstrip("/")
    if not base:
        fail("site.base_url is required for IndexNow submission")
    return base


def site_url(config: dict[str, Any], path: str) -> str:
    return f"{site_base(config)}/{path.lstrip('/')}"


def file_signature(path: Path) -> str:
    if not path.exists():
        return "missing"
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def add_candidate(candidates: list[dict[str, str]], config: dict[str, Any], rel_path: str) -> None:
    rel_path = rel_path.lstrip("./")
    candidates.append(
        {
            "url": site_url(config, rel_path),
            "path": str(DOCS / rel_path),
            "signature": file_signature(DOCS / rel_path),
        }
    )


def collect_candidates(config: dict[str, Any], include_all_packs: bool) -> list[dict[str, str]]:
    status = read_json(DOCS / "status.json")
    catalog = read_json(DOCS / "catalog.json", {"items": []})
    topics = read_json(DOCS / "topics" / "topics.json", {"topics": []})
    offers = read_json(DOCS / "offers" / "offers.json", {"offers": []})
    candidates: list[dict[str, str]] = []

    for rel_path in [
        "index.html",
        "archive.html",
        "support.html",
        "pay-what-you-can.html",
        "offers/index.html",
        "offers/offers.json",
        "starter-bundle.html",
        "bundles/starter-archive.zip",
        "store-import.html",
        "imports/store-upload-kit.zip",
        "license.html",
        "privacy.html",
        "refund-policy.html",
        "terms.html",
        "topics/index.html",
        "topics/topics.json",
        "catalog.json",
        "catalog.csv",
        "product-feed.json",
        "product-feed.xml",
        "product-feed.csv",
        "support-funnel.json",
        "support-funnel.xml",
        "support-funnel.csv",
        "imports/store-listings.json",
        "imports/store-listings.csv",
        "feed.json",
        "feed.xml",
        "atom.xml",
        "llms.txt",
        "llms-full.txt",
        "sitemap.xml",
    ]:
        add_candidate(candidates, config, rel_path)

    today_path = str(status.get("today_path", "")).strip("/")
    if today_path:
        add_candidate(candidates, config, f"{today_path}/index.html")
    today_download = str(status.get("today_download", "")).strip("/")
    if today_download:
        add_candidate(candidates, config, today_download)
    today_download_page = str(status.get("today_download_page", "")).strip("/")
    if today_download_page:
        add_candidate(candidates, config, today_download_page)

    if include_all_packs:
        for item in catalog.get("items", []):
            path = str(item.get("url", "")).replace(site_base(config) + "/", "")
            if path:
                add_candidate(candidates, config, path.rstrip("/") + "/index.html")
            download_url = str(item.get("download_url", "")).replace(site_base(config) + "/", "")
            if download_url:
                add_candidate(candidates, config, download_url)
            download_page_url = str(item.get("download_page_url", "")).replace(site_base(config) + "/", "")
            if download_page_url:
                add_candidate(candidates, config, download_page_url)

    for topic in topics.get("topics", []):
        slug = str(topic.get("slug", "")).strip()
        if slug:
            add_candidate(candidates, config, f"topics/{slug}.html")

    for offer in offers.get("offers", []):
        path = str(offer.get("path", "")).strip("/")
        if path:
            add_candidate(candidates, config, path)

    deduped: list[dict[str, str]] = []
    seen: set[str] = set()
    for candidate in candidates:
        url = candidate["url"]
        if url.endswith("/index.html"):
            url = url[: -len("index.html")]
            candidate = {**candidate, "url": url}
        if url not in seen:
            deduped.append(candidate)
            seen.add(url)
    return deduped


def load_state() -> dict[str, Any]:
    return read_json(INDEXNOW_STATE, {"submitted": {}})


def save_state(state: dict[str, Any]) -> None:
    STATE.mkdir(parents=True, exist_ok=True)
    INDEXNOW_STATE.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")


def changed_candidates(candidates: list[dict[str, str]], state: dict[str, Any], force: bool) -> list[dict[str, str]]:
    if force:
        return candidates
    submitted = state.get("submitted", {})
    changed = []
    for candidate in candidates:
        previous = submitted.get(candidate["url"], {})
        if previous.get("signature") != candidate["signature"]:
            changed.append(candidate)
    return changed


def wait_for_key(key_location: str, key: str, seconds: int) -> dict[str, Any]:
    deadline = time.monotonic() + max(0, seconds)
    last_error = ""
    while True:
        try:
            with urllib.request.urlopen(key_location, timeout=15) as response:
                body = response.read().decode("utf-8", errors="replace").strip()
                if response.status == 200 and body == key:
                    return {"status_code": response.status, "key_location": key_location}
                last_error = f"status={response.status} body={body[:80]!r}"
        except OSError as exc:
            last_error = str(exc)

        if time.monotonic() >= deadline:
            fail(f"IndexNow key file not verified at {key_location}: {last_error}")
        time.sleep(5)


def submit_indexnow(endpoint: str, host: str, key: str, key_location: str, urls: list[str]) -> dict[str, Any]:
    payload = {
        "host": host,
        "key": key,
        "keyLocation": key_location,
        "urlList": urls,
    }
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8", errors="replace")
            status_code = response.status
    except urllib.error.HTTPError as exc:
        status_code = exc.code
        body = exc.read().decode("utf-8", errors="replace")

    if status_code not in {200, 202}:
        fail(f"IndexNow returned HTTP {status_code}: {body[:400]}")
    return {"status_code": status_code, "body": body[:400]}


def main() -> int:
    parser = argparse.ArgumentParser(description="Submit changed Daily Autodigital Shelf URLs to IndexNow.")
    parser.add_argument("--all", action="store_true", help="Include every pack page, not only the current daily pack.")
    parser.add_argument("--force", action="store_true", help="Submit selected URLs even if local signatures did not change.")
    parser.add_argument("--dry-run", action="store_true", help="Print intended submission without calling IndexNow.")
    parser.add_argument("--max-urls", type=int, default=100, help="Maximum URLs to submit in one request.")
    parser.add_argument("--wait-for-key-seconds", type=int, default=0, help="Wait for the public IndexNow key file.")
    args = parser.parse_args()

    config = load_config()
    discovery = config.get("discovery", {})
    if not discovery.get("indexnow_enabled"):
        print(json.dumps({"status": "skipped", "reason": "indexnow disabled"}, indent=2))
        return 0

    key = str(discovery.get("indexnow_key", "")).strip()
    endpoint = str(discovery.get("indexnow_endpoint", "https://api.indexnow.org/indexnow")).strip()
    if not key:
        fail("discovery.indexnow_key is required")
    key_location = site_url(config, f"{key}.txt")
    host = urllib.parse.urlparse(site_base(config)).netloc
    if not host:
        fail("site.base_url must include a host")

    candidates = collect_candidates(config, args.all)
    state = load_state()
    selected = changed_candidates(candidates, state, args.force)[: args.max_urls]
    urls = [candidate["url"] for candidate in selected]

    result: dict[str, Any] = {
        "status": "ok",
        "dry_run": args.dry_run,
        "endpoint": endpoint,
        "host": host,
        "key_location": key_location,
        "candidate_count": len(candidates),
        "submit_count": len(urls),
        "urls": urls,
    }
    if not urls:
        print(json.dumps(result, indent=2))
        return 0

    if args.dry_run:
        print(json.dumps(result, indent=2))
        return 0

    key_check = wait_for_key(key_location, key, args.wait_for_key_seconds)
    submission = submit_indexnow(endpoint, host, key, key_location, urls)
    submitted_at = dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()
    state.setdefault("submitted", {})
    for candidate in selected:
        state["submitted"][candidate["url"]] = {
            "signature": candidate["signature"],
            "submitted_at": submitted_at,
        }
    state["last_submission"] = {
        "submitted_at": submitted_at,
        "endpoint": endpoint,
        "host": host,
        "count": len(urls),
        "status_code": submission["status_code"],
    }
    save_state(state)

    result["key_check"] = key_check
    result["submission"] = submission
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, indent=2), file=sys.stderr)
        raise SystemExit(1)
