from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import urllib.request
import zipfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
STATE = ROOT / "state"


def fail(message: str) -> None:
    raise AssertionError(message)


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"Missing JSON file: {path}")
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON in {path}: {exc}")


def require_file(path: Path, min_bytes: int = 1) -> None:
    if not path.exists():
        fail(f"Missing file: {path}")
    if path.stat().st_size < min_bytes:
        fail(f"File is too small: {path}")


def require_contains(path: Path, needles: list[str]) -> None:
    require_file(path)
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            fail(f"{path} does not contain expected text: {needle}")


def today_iso(value: str | None) -> str:
    if value:
        return dt.date.fromisoformat(value).isoformat()
    return dt.datetime.now().astimezone().date().isoformat()


def verify_local(day: str, min_pack_count: int = 1) -> dict[str, Any]:
    status = read_json(DOCS / "status.json")
    if status.get("today") != day:
        fail(f"status.json today is {status.get('today')}, expected {day}")

    pack_path = status.get("today_path")
    if not pack_path:
        fail("status.json missing today_path")

    pack_count = len([path for path in (DOCS / "packs").glob("*/manifest.json")])
    if pack_count < min_pack_count:
        fail(f"Pack count is {pack_count}, expected at least {min_pack_count}")

    pack_dir = DOCS / pack_path
    manifest = read_json(pack_dir / "manifest.json")
    for key in ["path", "worksheet", "checklist", "cover", "seller_copy"]:
        if not manifest.get(key):
            fail(f"manifest missing {key}")

    require_contains(
        DOCS / "index.html",
        [
            "Daily Autodigital Shelf",
            "Open today's pack",
            "View setup status",
            "application/ld+json",
            "feed.json",
            "sitemap.xml",
            "seller-copy.md",
            "Writes store-ready listing copy",
            "archive.html",
            "starter-bundle.html",
            "starter-archive.zip",
            "catalog.csv",
            "catalog.json",
        ],
    )
    require_contains(pack_dir / "index.html", [manifest["title"], "Store link not connected"])
    require_file(pack_dir / "printable.html", 800)
    require_file(pack_dir / "checklist.html", 800)
    require_file(pack_dir / "cover.svg", 800)
    require_contains(pack_dir / "seller-copy.md", ["Store-Ready Listing Copy", "Price Hint", "Safety Note"])
    require_file(DOCS / "feed.json", 100)
    require_file(DOCS / "catalog.json", 100)
    require_contains(DOCS / "catalog.csv", ["seller_copy_url", "starter_bundle_url", manifest["title"]])
    require_contains(DOCS / "archive.html", ["Pack archive", manifest["title"], "Starter bundle", "Catalog CSV"])
    require_contains(DOCS / "starter-bundle.html", ["Starter bundle", "Download ZIP", "starter-archive.zip"])
    bundle_path = DOCS / "bundles" / "starter-archive.zip"
    require_file(bundle_path, max(12000, min_pack_count * 900))
    with zipfile.ZipFile(bundle_path) as bundle:
        names = bundle.namelist()
        if any(name.startswith("/") or ".." in Path(name).parts for name in names):
            fail("Starter bundle contains unsafe archive paths")
        manifest_names = [name for name in names if name.endswith("/manifest.json")]
        if len(manifest_names) < min_pack_count:
            fail(f"Starter bundle manifest count is {len(manifest_names)}, expected at least {min_pack_count}")
        required_names = [
            "daily-autodigital-shelf-starter/README.txt",
            "daily-autodigital-shelf-starter/STARTER-BUNDLE-MANIFEST.json",
            f"daily-autodigital-shelf-starter/{manifest['worksheet']}",
            f"daily-autodigital-shelf-starter/{manifest['checklist']}",
            f"daily-autodigital-shelf-starter/{manifest['seller_copy']}",
        ]
        for name in required_names:
            if name not in names:
                fail(f"Starter bundle missing {name}")
    require_file(DOCS / "sitemap.xml", 100)
    require_contains(DOCS / "sitemap.xml", ["starter-bundle.html"])
    require_contains(DOCS / "robots.txt", ["User-agent: *", "Sitemap:"])
    require_file(DOCS / ".nojekyll", 0)

    catalog = read_json(DOCS / "catalog.json")
    if not any(item.get("id") == manifest["id"] for item in catalog.get("items", [])):
        fail(f"catalog.json does not contain manifest id: {manifest['id']}")

    ledger_path = STATE / "ledger.jsonl"
    require_file(ledger_path, 20)
    ledger_rows = [
        json.loads(line)
        for line in ledger_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not any(row.get("date") == day and row.get("pack_slug") in pack_path for row in ledger_rows):
        fail(f"No ledger row for {day} and {pack_path}")

    if status.get("monetization_enabled") and not (status.get("store_connected") or status.get("support_connected")):
        fail("Monetization is enabled but no store/support destination is connected")
    if not status.get("bundle_ready"):
        fail("status.json reports bundle_ready=false")
    if int(status.get("bundle_pack_count") or 0) < min_pack_count:
        fail(f"status.json bundle_pack_count is {status.get('bundle_pack_count')}, expected at least {min_pack_count}")

    return {
        "today": day,
        "title": manifest["title"],
        "path": pack_path,
        "pack_count": pack_count,
        "bundle_bytes": bundle_path.stat().st_size,
        "files_checked": 15,
        "monetization_enabled": bool(status.get("monetization_enabled")),
        "store_connected": bool(status.get("store_connected")),
        "support_connected": bool(status.get("support_connected")),
    }


def verify_live(url: str) -> dict[str, Any]:
    with urllib.request.urlopen(url, timeout=30) as response:
        status_code = response.status
        body = response.read().decode("utf-8", errors="replace")
    if status_code != 200:
        fail(f"Live URL returned {status_code}: {url}")
    for needle in ["Daily Autodigital Shelf", "Open today's pack", "Starter bundle", "Monetization setup"]:
        if needle not in body:
            fail(f"Live URL missing expected text: {needle}")
    return {"url": url, "status_code": status_code, "bytes": len(body)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Daily Autodigital Shelf output.")
    parser.add_argument("--date", help="Expected ISO date. Defaults to local today.")
    parser.add_argument("--live-url", help="Optional live homepage URL to verify.")
    parser.add_argument("--min-pack-count", type=int, default=1, help="Minimum generated pack manifests expected.")
    args = parser.parse_args()

    result: dict[str, Any] = {"local": verify_local(today_iso(args.date), args.min_pack_count)}
    if args.live_url:
        result["live"] = verify_live(args.live_url)

    print(json.dumps({"status": "ok", **result}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, indent=2), file=sys.stderr)
        raise SystemExit(1)
