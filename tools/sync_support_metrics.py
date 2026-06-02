from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state"
CONFIG_EXAMPLE = ROOT / "config" / "config.example.json"
CONFIG_PUBLIC = ROOT / "config" / "config.public.json"
CONFIG_LOCAL = ROOT / "config" / "config.local.json"
SNAPSHOT_PATH = STATE / "support-metrics-snapshot.json"
DEFAULT_SOURCE_URL = "https://www.calmsprout.com/daily-shelf/support-metrics.json"
USER_AGENT = "daily-autodigital-shelf-support-metrics-sync/1.0"


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


def configured_source_url(config: dict[str, Any]) -> str:
    monetization = config.get("monetization", {})
    source_url = str(monetization.get("support_metrics_url") or "").strip()
    if source_url:
        return source_url
    branded_base = str(config.get("site", {}).get("branded_base_url") or "").strip().rstrip("/")
    if branded_base:
        return f"{branded_base}/support-metrics.json"
    return DEFAULT_SOURCE_URL


def safe_int(value: Any) -> int:
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return 0


def clean_map(value: Any, max_keys: int = 120) -> dict[str, int]:
    if not isinstance(value, dict):
        return {}
    cleaned: dict[str, int] = {}
    for key, raw_count in list(value.items())[:max_keys]:
        slug = str(key or "").strip().lower()
        if not slug or len(slug) > 140:
            continue
        cleaned[slug] = safe_int(raw_count)
    return cleaned


def clean_nested_map(value: Any, max_outer: int = 120, max_inner: int = 60) -> dict[str, dict[str, int]]:
    if not isinstance(value, dict):
        return {}
    cleaned: dict[str, dict[str, int]] = {}
    for key, raw_days in list(value.items())[:max_outer]:
        slug = str(key or "").strip().lower()
        if not slug or len(slug) > 140 or not isinstance(raw_days, dict):
            continue
        cleaned_days: dict[str, int] = {}
        for day, raw_count in list(raw_days.items())[-max_inner:]:
            day_text = str(day or "").strip()
            if len(day_text) == 10:
                cleaned_days[day_text] = safe_int(raw_count)
        cleaned[slug] = cleaned_days
    return cleaned


def clean_recent(value: Any, max_items: int = 25) -> list[dict[str, str]]:
    if not isinstance(value, list):
        return []
    recent: list[dict[str, str]] = []
    for item in value[:max_items]:
        if not isinstance(item, dict):
            continue
        recent.append(
            {
                "at": str(item.get("at") or ""),
                "slug": str(item.get("slug") or "")[:140],
                "route": str(item.get("route") or "")[:240],
                "destination_type": str(item.get("destination_type") or "")[:80],
                "utm_campaign": str(item.get("utm_campaign") or "")[:80],
                "utm_content": str(item.get("utm_content") or "")[:140],
            }
        )
    return recent


def blank_snapshot(source_url: str, error: str = "") -> dict[str, Any]:
    return {
        "version": 1,
        "kind": "daily-shelf-support-metrics-snapshot",
        "source_url": source_url,
        "fetched_at": dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat(),
        "sync_ok": False,
        "sync_error": error,
        "storage_connected": False,
        "privacy": "Aggregate support-intent counts only. No IP address, user-agent, cookie, email, or payment data is stored.",
        "revenue_boundary": "This measures clicks to the external Square support page. It does not prove payments or daily revenue.",
        "total_support_intent_clicks": 0,
        "by_day": {},
        "by_slug": {},
        "by_slug_day": {},
        "recent": [],
        "updated_at": None,
    }


def fetch_metrics(source_url: str, timeout: int) -> dict[str, Any]:
    request = urllib.request.Request(source_url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read().decode("utf-8", errors="replace")
        payload = json.loads(body)
    if not isinstance(payload, dict):
        raise RuntimeError("metrics response was not a JSON object")
    return payload


def sanitize_metrics(payload: dict[str, Any], source_url: str) -> dict[str, Any]:
    return {
        "version": 1,
        "kind": "daily-shelf-support-metrics-snapshot",
        "source_url": source_url,
        "fetched_at": dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat(),
        "sync_ok": True,
        "sync_error": "",
        "source_kind": str(payload.get("kind") or ""),
        "storage_connected": bool(payload.get("storage_connected")),
        "privacy": str(payload.get("privacy") or "Aggregate support-intent counts only."),
        "revenue_boundary": str(
            payload.get("revenue_boundary")
            or "This measures clicks to the external support page. It does not prove payments or daily revenue."
        ),
        "total_support_intent_clicks": safe_int(payload.get("total_support_intent_clicks")),
        "by_day": clean_map(payload.get("by_day"), max_keys=80),
        "by_slug": clean_map(payload.get("by_slug"), max_keys=160),
        "by_slug_day": clean_nested_map(payload.get("by_slug_day"), max_outer=160, max_inner=80),
        "recent": clean_recent(payload.get("recent")),
        "updated_at": payload.get("updated_at"),
    }


def write_snapshot(snapshot: dict[str, Any]) -> None:
    STATE.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_PATH.write_text(json.dumps(snapshot, indent=2, sort_keys=True), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync public CalmSprout support-intent metrics into local state.")
    parser.add_argument("--source-url", help="Override support metrics JSON URL.")
    parser.add_argument("--timeout", type=int, default=20, help="HTTP timeout in seconds.")
    parser.add_argument("--allow-stale", action="store_true", default=True, help="Keep the last snapshot if sync fails.")
    args = parser.parse_args()

    config = load_config()
    source_url = str(args.source_url or configured_source_url(config)).strip()
    try:
        payload = fetch_metrics(source_url, args.timeout)
        snapshot = sanitize_metrics(payload, source_url)
        write_snapshot(snapshot)
        print(json.dumps({"status": "ok", "source_url": source_url, "total_support_intent_clicks": snapshot["total_support_intent_clicks"]}, indent=2))
        return 0
    except Exception as exc:
        if SNAPSHOT_PATH.exists() and args.allow_stale:
            stale = read_json(SNAPSHOT_PATH)
            stale["last_sync_error"] = str(exc)
            stale["last_sync_error_at"] = dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()
            write_snapshot(stale)
            print(json.dumps({"status": "stale", "source_url": source_url, "error": str(exc)}, indent=2))
            return 0
        snapshot = blank_snapshot(source_url, str(exc))
        write_snapshot(snapshot)
        print(json.dumps({"status": "blank", "source_url": source_url, "error": str(exc)}, indent=2), file=sys.stderr)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
