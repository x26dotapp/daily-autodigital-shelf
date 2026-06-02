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

    pack_cta_needle = "Store link not connected"
    action_needle = "Store link not connected"
    if status.get("store_connected"):
        pack_cta_needle = "Buy or download from store"
        action_needle = "BuyAction"
    elif status.get("support_connected"):
        pack_cta_needle = "Support this shelf"
        action_needle = "DonateAction"

    require_contains(
        DOCS / "index.html",
        [
            "Daily Autodigital Shelf",
            "Open today's pack",
            "View setup status",
            "application/ld+json",
            "og:image",
            "twitter:card",
            "feed.json",
            "feed.xml",
            "atom.xml",
            "llms.txt",
            "sitemap.xml",
            "seller-copy.md",
            "Writes store-ready listing copy",
            "archive.html",
            "topics/",
            "offers/",
            "starter-bundle.html",
            "starter-archive.zip",
            "support.html",
            "pay-what-you-can.html",
            "store-import.html",
            "terms.html",
            "Download ZIP",
            "catalog.csv",
            "catalog.json",
        ],
    )
    require_contains(
        pack_dir / "index.html",
        [
            manifest["title"],
            pack_cta_needle,
            "Download pack ZIP",
            "og:image",
            "twitter:card",
            "contentUrl",
            "encodingFormat",
            action_needle,
            "Related Topics",
            "topic-link",
        ],
    )
    require_file(pack_dir / "printable.html", 800)
    require_file(pack_dir / "checklist.html", 800)
    require_file(pack_dir / "cover.svg", 800)
    require_contains(pack_dir / "seller-copy.md", ["Store-Ready Listing Copy", "Price Hint", "Safety Note"])
    download_path = DOCS / manifest.get("download", f"downloads/{Path(pack_path).parts[-1]}.zip")
    require_file(download_path, 2500)
    with zipfile.ZipFile(download_path) as pack_zip:
        names = pack_zip.namelist()
        if any(name.startswith("/") or ".." in Path(name).parts for name in names):
            fail("Pack ZIP contains unsafe archive paths")
        for suffix in ["README.txt", "printable.html", "checklist.html", "cover.svg", "seller-copy.md", "manifest.json"]:
            if not any(name.endswith(suffix) for name in names):
                fail(f"Pack ZIP missing {suffix}")
    require_file(DOCS / "feed.json", 100)
    require_contains(DOCS / "feed.xml", ["<rss version=\"2.0\">", "<channel>", manifest["title"], "application/rss+xml"])
    require_contains(DOCS / "atom.xml", ["<feed xmlns=\"http://www.w3.org/2005/Atom\">", "<entry>", manifest["title"], "application/atom+xml"])
    require_file(DOCS / "catalog.json", 100)
    require_contains(DOCS / "catalog.csv", ["seller_copy_url", "download_url", "starter_bundle_url", "support_page_url", "pay_what_you_can_url", "monetization_destination_url", "topic_urls", manifest["title"]])
    require_contains(DOCS / "archive.html", ["Pack archive", manifest["title"], "Starter bundle", "Topics", "Offers", "Support", "Policies", "Import kit", "Catalog CSV", "Download ZIP", "ItemList", "og:image", "twitter:card"])
    require_contains(DOCS / "starter-bundle.html", ["Starter bundle", "Download ZIP", "starter-archive.zip", "Pack ZIP", "Topics", "Offers", "Support", "Policies", "ItemList", "og:image", "twitter:card"])
    require_contains(DOCS / "support.html", ["Support this shelf", "Download starter bundle", "This is not product checkout", "WebPage", "og:image", "twitter:card"])
    require_contains(DOCS / "pay-what-you-can.html", ["Pay what you can", "Download starter ZIP", "Suggested support", "Simple levels", "This is not product checkout", "WebPage", "og:image", "twitter:card"])
    require_contains(DOCS / "store-import.html", ["Store import kit", "Download import kit", "Marketplace queue", "topic_urls", "Policy pages", "license, terms, privacy, and refund", manifest["title"], "Offers", "Support", "ItemList", "og:image", "twitter:card"])
    require_contains(DOCS / "imports" / "store-listings.csv", ["download_url", "preview_url", "price_hint", "support_page_url", "pay_what_you_can_url", "monetization_destination_url", "topic_urls", manifest["title"]])
    require_contains(DOCS / "llms.txt", ["Daily Autodigital Shelf", "Support page", "Monetization destination", "Product checkout is not connected"])
    require_contains(DOCS / "llms-full.txt", ["Daily Autodigital Shelf Full Context", "Generated Packs", manifest["title"], "Machine-Readable Files", "status.json"])
    import_json = read_json(DOCS / "imports" / "store-listings.json")
    if len(import_json.get("items", [])) < min_pack_count:
        fail(f"store-listings.json item count is {len(import_json.get('items', []))}, expected at least {min_pack_count}")
    topics_index = str(status.get("topics_index", "topics/index.html")).strip("/")
    topics_json_path = str(status.get("topics_json", "topics/topics.json")).strip("/")
    require_contains(DOCS / topics_index, ["Topics", "CollectionPage", "og:image", "twitter:card"])
    topics_json = read_json(DOCS / topics_json_path)
    topic_rows = topics_json.get("topics", [])
    if len(topic_rows) < 3:
        fail(f"topics.json topic count is {len(topic_rows)}, expected at least 3")
    today_topic = next(
        (
            topic
            for topic in topic_rows
            if any(item.get("id") == manifest["id"] for item in topic.get("items", []))
        ),
        None,
    )
    if not today_topic:
        fail(f"topics.json does not assign current manifest id: {manifest['id']}")
    topic_page = DOCS / "topics" / f"{today_topic['slug']}.html"
    require_contains(topic_page, [today_topic["label"], manifest["title"], "Product ZIP", "Listing copy", "CollectionPage"])
    offers_index = str(status.get("offers_index", "offers/index.html")).strip("/")
    offers_json_path = str(status.get("offers_json", "offers/offers.json")).strip("/")
    require_contains(DOCS / offers_index, ["Offers", "CollectionPage", "Open offer", "Support", "Starter bundle"])
    offers_json = read_json(DOCS / offers_json_path)
    offer_rows = offers_json.get("offers", [])
    if len(offer_rows) < 3:
        fail(f"offers.json offer count is {len(offer_rows)}, expected at least 3")
    today_offer = next(
        (
            offer
            for offer in offer_rows
            if any(item.get("id") == manifest["id"] for item in offer.get("items", []))
        ),
        None,
    )
    if not today_offer:
        fail(f"offers.json does not assign current manifest id: {manifest['id']}")
    offer_cta_needle = "Open product checkout" if status.get("store_connected") else "Support this collection"
    offer_page = DOCS / str(today_offer.get("path", f"offers/{today_offer['slug']}.html")).strip("/")
    require_contains(
        offer_page,
        [
            today_offer["label"],
            manifest["title"],
            "Collection offer",
            "Download starter bundle",
            offer_cta_needle,
            "Product checkout is not connected",
            "CollectionPage",
            "og:image",
            "twitter:card",
        ],
    )
    policy_paths = [str(path).strip("/") for path in status.get("policy_pages", [])]
    expected_policy_paths = ["license.html", "privacy.html", "refund-policy.html", "terms.html"]
    for policy_path in expected_policy_paths:
        if policy_path not in policy_paths:
            fail(f"status.json policy_pages missing {policy_path}")
        require_contains(DOCS / policy_path, ["Policy", "Store readiness", "WebPage", "og:image", "twitter:card", "checkout", "payout"])
    import_zip_path = DOCS / "imports" / "store-upload-kit.zip"
    require_file(import_zip_path, max(15000, min_pack_count * 1200))
    with zipfile.ZipFile(import_zip_path) as import_zip:
        names = import_zip.namelist()
        if any(name.startswith("/") or ".." in Path(name).parts for name in names):
            fail("Store import kit ZIP contains unsafe archive paths")
        for suffix in ["README.txt", "store-listings.csv", "store-listings.json", "terms.html", "privacy.html", "license.html", "refund-policy.html", "seller-copy.md", ".zip"]:
            if not any(name.endswith(suffix) for name in names):
                fail(f"Store import kit ZIP missing {suffix}")
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
            "daily-autodigital-shelf-starter/terms.html",
            "daily-autodigital-shelf-starter/license.html",
            "daily-autodigital-shelf-starter/privacy.html",
            "daily-autodigital-shelf-starter/refund-policy.html",
            "daily-autodigital-shelf-starter/support.html",
            "daily-autodigital-shelf-starter/pay-what-you-can.html",
            "daily-autodigital-shelf-starter/offers/index.html",
            "daily-autodigital-shelf-starter/offers/offers.json",
            f"daily-autodigital-shelf-starter/{str(today_offer.get('path')).strip('/')}",
            "daily-autodigital-shelf-starter/llms.txt",
            "daily-autodigital-shelf-starter/llms-full.txt",
            f"daily-autodigital-shelf-starter/{manifest['worksheet']}",
            f"daily-autodigital-shelf-starter/{manifest['checklist']}",
            f"daily-autodigital-shelf-starter/{manifest['seller_copy']}",
        ]
        for name in required_names:
            if name not in names:
                fail(f"Starter bundle missing {name}")
    require_file(DOCS / "sitemap.xml", 100)
    require_contains(DOCS / "sitemap.xml", ["starter-bundle.html", "support.html", "pay-what-you-can.html", "offers/", "offers/offers.json", "topics/", "topics/topics.json", "terms.html", "privacy.html", "license.html", "refund-policy.html", "feed.xml", "atom.xml", "llms.txt", "llms-full.txt"])
    require_contains(DOCS / "robots.txt", ["User-agent: *", "Sitemap:"])
    require_file(DOCS / ".nojekyll", 0)
    require_file(ROOT / "tools" / "submit_calmsprout_indexnow.py", 4000)
    require_contains(
        ROOT / "run-daily.ps1",
        ["tools\\submit_calmsprout_indexnow.py", "CalmSprout IndexNow submission complete"],
    )
    require_contains(
        ROOT / ".github" / "workflows" / "daily-shelf.yml",
        ["Submit changed CalmSprout URLs to IndexNow", "tools/submit_calmsprout_indexnow.py"],
    )
    require_contains(
        ROOT / ".gitignore",
        ["state/calmsprout-indexnow-state.json"],
    )

    catalog = read_json(DOCS / "catalog.json")
    catalog_item = next((item for item in catalog.get("items", []) if item.get("id") == manifest["id"]), None)
    if not catalog_item:
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
    if status.get("store_connected") or status.get("support_connected"):
        if status.get("monetization_destination_type") not in {"store", "support"}:
            fail("Connected monetization is missing a store/support destination type")
        destination_url = str(status.get("monetization_destination_url") or "")
        if not destination_url.startswith(("https://", "http://")):
            fail("Connected monetization destination is missing a public URL")
        require_contains(DOCS / "index.html", [destination_url])
        require_contains(DOCS / "support.html", [destination_url])
        require_contains(DOCS / "pay-what-you-can.html", [destination_url])
        require_contains(offer_page, [destination_url])
        require_contains(DOCS / "llms.txt", [destination_url])
        require_contains(DOCS / "llms-full.txt", [destination_url])
        require_contains(pack_dir / "index.html", [destination_url])
        if catalog_item.get("monetization_destination_url") != destination_url:
            fail("catalog.json current item missing monetization destination URL")
        if catalog_item.get("support_page_url") != "https://x26dotapp.github.io/daily-autodigital-shelf/support.html":
            fail("catalog.json current item missing support_page_url")
        if catalog_item.get("pay_what_you_can_url") != "https://x26dotapp.github.io/daily-autodigital-shelf/pay-what-you-can.html":
            fail("catalog.json current item missing pay_what_you_can_url")
        import_row = next((item for item in import_json.get("items", []) if item.get("sku", "").endswith(manifest["id"].split(":")[-1])), None)
        if not import_row:
            fail("store-listings.json missing current item")
        if import_row.get("monetization_destination_url") != destination_url:
            fail("store-listings.json current item missing monetization destination URL")
        if import_row.get("support_page_url") != "https://x26dotapp.github.io/daily-autodigital-shelf/support.html":
            fail("store-listings.json current item missing support_page_url")
        if import_row.get("pay_what_you_can_url") != "https://x26dotapp.github.io/daily-autodigital-shelf/pay-what-you-can.html":
            fail("store-listings.json current item missing pay_what_you_can_url")
    if not status.get("bundle_ready"):
        fail("status.json reports bundle_ready=false")
    if int(status.get("bundle_pack_count") or 0) < min_pack_count:
        fail(f"status.json bundle_pack_count is {status.get('bundle_pack_count')}, expected at least {min_pack_count}")
    if int(status.get("pack_download_count") or 0) < min_pack_count:
        fail(f"status.json pack_download_count is {status.get('pack_download_count')}, expected at least {min_pack_count}")
    if status.get("today_download") != manifest.get("download"):
        fail(f"status.json today_download is {status.get('today_download')}, expected {manifest.get('download')}")
    if status.get("feed_json") != "feed.json" or status.get("feed_xml") != "feed.xml" or status.get("atom_xml") != "atom.xml":
        fail("status.json missing feed_json/feed_xml/atom_xml paths")
    if int(status.get("feed_item_count") or 0) < min_pack_count:
        fail(f"status.json feed_item_count is {status.get('feed_item_count')}, expected at least {min_pack_count}")
    if not status.get("store_import_ready"):
        fail("status.json reports store_import_ready=false")
    if int(status.get("store_import_count") or 0) < min_pack_count:
        fail(f"status.json store_import_count is {status.get('store_import_count')}, expected at least {min_pack_count}")
    if not status.get("topic_pages_ready"):
        fail("status.json reports topic_pages_ready=false")
    if int(status.get("topic_page_count") or 0) < 3:
        fail(f"status.json topic_page_count is {status.get('topic_page_count')}, expected at least 3")
    if int(status.get("topic_item_count") or 0) < min_pack_count:
        fail(f"status.json topic_item_count is {status.get('topic_item_count')}, expected at least {min_pack_count}")
    if not status.get("policy_pages_ready"):
        fail("status.json reports policy_pages_ready=false")
    if int(status.get("policy_page_count") or 0) < 4:
        fail(f"status.json policy_page_count is {status.get('policy_page_count')}, expected at least 4")
    if not status.get("support_page_ready") or status.get("support_page") != "support.html":
        fail("status.json missing support_page_ready/support.html")
    if status.get("support_page_url") != "https://x26dotapp.github.io/daily-autodigital-shelf/support.html":
        fail("status.json missing support_page_url")
    if not status.get("pay_what_you_can_ready") or status.get("pay_what_you_can_page") != "pay-what-you-can.html":
        fail("status.json missing pay_what_you_can_ready/pay-what-you-can.html")
    if status.get("pay_what_you_can_url") != "https://x26dotapp.github.io/daily-autodigital-shelf/pay-what-you-can.html":
        fail("status.json missing pay_what_you_can_url")
    if int(status.get("support_tier_count") or 0) < 3:
        fail(f"status.json support_tier_count is {status.get('support_tier_count')}, expected at least 3")
    if not status.get("offer_pages_ready"):
        fail("status.json reports offer_pages_ready=false")
    if int(status.get("offer_page_count") or 0) < 3:
        fail(f"status.json offer_page_count is {status.get('offer_page_count')}, expected at least 3")
    if status.get("offers_index") != "offers/index.html" or status.get("offers_json") != "offers/offers.json":
        fail("status.json missing offers index/json paths")
    if not status.get("ai_discovery_ready"):
        fail("status.json reports ai_discovery_ready=false")
    if status.get("llms_txt") != "llms.txt" or status.get("llms_full_txt") != "llms-full.txt":
        fail("status.json missing llms discovery paths")
    if not status.get("indexnow_enabled"):
        fail("status.json reports indexnow_enabled=false")
    indexnow_key_file = str(status.get("indexnow_key_file", ""))
    if not indexnow_key_file.endswith(".txt"):
        fail("status.json missing indexnow_key_file")
    require_file(DOCS / indexnow_key_file, 8)
    indexnow_key = (DOCS / indexnow_key_file).read_text(encoding="utf-8").strip()
    if indexnow_key_file != f"{indexnow_key}.txt":
        fail("IndexNow key file name does not match file body")
    if not status.get("indexnow_key_location"):
        fail("status.json missing indexnow_key_location")

    return {
        "today": day,
        "title": manifest["title"],
        "path": pack_path,
        "pack_count": pack_count,
        "bundle_bytes": bundle_path.stat().st_size,
        "download_bytes": download_path.stat().st_size,
        "store_import_zip_bytes": import_zip_path.stat().st_size,
        "topic_page_count": int(status.get("topic_page_count") or 0),
        "policy_page_count": int(status.get("policy_page_count") or 0),
        "files_checked": 40,
        "indexnow_enabled": True,
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
