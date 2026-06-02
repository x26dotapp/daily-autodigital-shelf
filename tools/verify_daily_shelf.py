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


def evergreen_slug(value: str) -> str:
    slug = str(value).strip("/").split("/")[-1]
    if len(slug) > 11 and slug[4] == "-" and slug[7] == "-" and slug[10] == "-":
        return slug[11:]
    return slug


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
    pack_slug = Path(str(pack_path).strip("/")).parts[-1]
    template_slug = evergreen_slug(pack_slug)
    today_template_path = f"templates/{template_slug}.html"
    expected_template_count = len(
        {
            evergreen_slug(path.parent.name)
            for path in (DOCS / "packs").glob("*/manifest.json")
        }
    )
    download_page_rel = f"downloads/{pack_slug}.html"
    download_page_url = f"https://x26dotapp.github.io/daily-autodigital-shelf/{download_page_rel}"
    branded_product_url = f"https://www.calmsprout.com/daily-shelf/products/{pack_slug}"
    branded_support_url = f"{branded_product_url}/support"
    branded_support_intent_url = f"{branded_support_url}/go"
    template_support_url = f"https://www.calmsprout.com/daily-shelf/templates/{template_slug}/support"
    template_support_intent_url = f"{template_support_url}/go"
    for key in ["path", "worksheet", "checklist", "cover", "seller_copy"]:
        if not manifest.get(key):
            fail(f"manifest missing {key}")

    pack_cta_needle = "Store link not connected"
    action_needle = "Store link not connected"
    if status.get("store_connected"):
        pack_cta_needle = "Buy or download from store"
        action_needle = "BuyAction"
    elif status.get("support_connected"):
        pack_cta_needle = "Support this pack"
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
            "use-cases/",
            "templates/",
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
            "product-feed.json",
            "support-funnel.json",
            download_page_rel,
        ],
    )
    require_contains(
        pack_dir / "index.html",
        [
            manifest["title"],
            pack_cta_needle,
            "Download pack",
            download_page_rel,
            "og:image",
            "twitter:card",
            "contentUrl",
            "encodingFormat",
            "Product",
            "Offer",
            "priceCurrency",
            "FAQPage",
            "Product FAQ",
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
    require_contains(
        DOCS / download_page_rel,
        [
            manifest["title"],
            "Download ZIP",
            f"./{pack_slug}.zip",
            "Support this pack",
            "DownloadAction",
            "DonateAction",
            branded_support_intent_url,
            "Product checkout is not connected",
            "og:image",
            "twitter:card",
        ],
    )
    with zipfile.ZipFile(download_path) as pack_zip:
        names = pack_zip.namelist()
        if any(name.startswith("/") or ".." in Path(name).parts for name in names):
            fail("Pack ZIP contains unsafe archive paths")
        for suffix in ["README.txt", "SUPPORT.txt", "printable.html", "checklist.html", "cover.svg", "seller-copy.md", "manifest.json"]:
            if not any(name.endswith(suffix) for name in names):
                fail(f"Pack ZIP missing {suffix}")
        support_name = next((name for name in names if name.endswith("SUPPORT.txt")), "")
        support_text = pack_zip.read(support_name).decode("utf-8") if support_name else ""
        for needle in [branded_support_intent_url, "Support is voluntary", "Product checkout is not connected"]:
            if needle not in support_text:
                fail(f"Pack ZIP SUPPORT.txt missing {needle}")
    require_file(DOCS / "feed.json", 100)
    require_contains(DOCS / "feed.xml", ["<rss version=\"2.0\">", "<channel>", manifest["title"], "application/rss+xml"])
    require_contains(DOCS / "atom.xml", ["<feed xmlns=\"http://www.w3.org/2005/Atom\">", "<entry>", manifest["title"], "application/atom+xml"])
    require_file(DOCS / "catalog.json", 100)
    require_contains(DOCS / "catalog.csv", ["seller_copy_url", "download_url", "download_page_url", "starter_bundle_url", "support_page_url", "pay_what_you_can_url", "branded_product_url", "branded_support_url", "branded_support_intent_url", "monetization_destination_url", "topic_urls", manifest["title"]])
    product_feed = read_json(DOCS / "product-feed.json")
    if int(product_feed.get("numberOfItems") or 0) < min_pack_count:
        fail(f"product-feed.json item count is {product_feed.get('numberOfItems')}, expected at least {min_pack_count}")
    require_contains(DOCS / "product-feed.json", [manifest["title"], "download_page_url", "branded_support_intent_url", "Product checkout is not connected", "DonateAction", "Offer"])
    require_contains(DOCS / "product-feed.xml", ["<productFeed>", "<product>", manifest["title"], "<downloadPageUrl>", "<brandedSupportIntentUrl>", "Product checkout is not connected"])
    require_contains(DOCS / "product-feed.csv", ["download_page_url", "branded_support_intent_url", "checkout_boundary", manifest["title"]])
    support_funnel = read_json(DOCS / "support-funnel.json")
    if int(support_funnel.get("numberOfItems") or 0) < min_pack_count:
        fail(f"support-funnel.json item count is {support_funnel.get('numberOfItems')}, expected at least {min_pack_count}")
    require_contains(DOCS / "support-funnel.json", [manifest["title"], "DownloadAction", "DonateAction", "branded_support_intent_url", "utm_campaign", "product_support", "suggested_support_tiers", "Product checkout is not connected"])
    require_contains(DOCS / "support-funnel.xml", ["<supportFunnelFeed>", "<supportFunnel>", manifest["title"], "<brandedSupportIntentUrl>", "<utmCampaign>product_support</utmCampaign>", "Product checkout is not connected"])
    require_contains(DOCS / "support-funnel.csv", ["branded_support_intent_url", "utm_campaign", "suggested_support_tiers", "checkout_boundary", manifest["title"]])
    require_contains(DOCS / "archive.html", ["Pack archive", manifest["title"], "Starter bundle", "Topics", "Use cases", "Offers", "Support", "Policies", "Import kit", "Catalog CSV", "Download page", "ItemList", "og:image", "twitter:card"])
    require_contains(DOCS / "archive.html", ["Templates", "template pages"])
    require_contains(DOCS / "starter-bundle.html", ["Starter bundle", "Download ZIP", "starter-archive.zip", "Download page", "Topics", "Use cases", "Templates", "Offers", "Support", "Policies", "ItemList", "og:image", "twitter:card"])
    require_contains(DOCS / "support.html", ["Support this shelf", "Download starter bundle", "This is not product checkout", "WebPage", "og:image", "twitter:card"])
    require_contains(DOCS / "pay-what-you-can.html", ["Pay what you can", "Download starter ZIP", "Suggested support", "Simple levels", "This is not product checkout", "WebPage", "og:image", "twitter:card"])
    require_contains(DOCS / "store-import.html", ["Store import kit", "Download import kit", "Marketplace queue", "topic_urls", "Policy pages", "license, terms, privacy, and refund", manifest["title"], "Offers", "Support", "ItemList", "og:image", "twitter:card"])
    require_contains(DOCS / "imports" / "store-listings.csv", ["download_url", "download_page_url", "preview_url", "price_hint", "support_page_url", "pay_what_you_can_url", "branded_product_url", "branded_support_url", "branded_support_intent_url", "monetization_destination_url", "topic_urls", manifest["title"]])
    require_contains(DOCS / "llms.txt", ["Daily Autodigital Shelf", "Support page", "Monetization destination", "Branded support intent redirect", "Download page", "Product Feed JSON", "Support Funnel JSON", "Templates", "Product checkout is not connected"])
    require_contains(DOCS / "llms-full.txt", ["Daily Autodigital Shelf Full Context", "Generated Packs", manifest["title"], "Download page", "Product Feed JSON", "Support Funnel JSON", "Use Cases JSON", "Templates JSON", "Machine-Readable Files", "status.json"])
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
    require_contains(topic_page, [today_topic["label"], manifest["title"], "Download page", "Listing copy", "CollectionPage"])
    use_cases_index = str(status.get("use_cases_index", "use-cases/index.html")).strip("/")
    use_cases_json_path = str(status.get("use_cases_json", "use-cases/use-cases.json")).strip("/")
    require_contains(DOCS / use_cases_index, ["Use cases", "Buyer-intent pages", "Open use case", "CollectionPage", "og:image", "twitter:card"])
    use_cases_json = read_json(DOCS / use_cases_json_path)
    use_case_rows = use_cases_json.get("items", [])
    if len(use_case_rows) < 3:
        fail(f"use-cases.json use case count is {len(use_case_rows)}, expected at least 3")
    today_use_case = next(
        (
            use_case
            for use_case in use_case_rows
            if any(item.get("id") == manifest["id"] for item in use_case.get("items", []))
        ),
        None,
    )
    if not today_use_case:
        fail(f"use-cases.json does not assign current manifest id: {manifest['id']}")
    today_use_case_path = str(today_use_case.get("path", f"use-cases/{today_use_case['slug']}.html")).strip("/")
    today_use_case_support_intent = f"https://www.calmsprout.com/daily-shelf/offers/{today_use_case['topic_slug']}/support/go"
    today_use_case_bundle_path = str(today_use_case.get("collection_bundle_path") or "").strip("/")
    if today_use_case.get("support_intent_url") != today_use_case_support_intent:
        fail("use-cases.json current use case missing collection support-intent URL")
    if today_use_case_bundle_path not in status.get("collection_bundle_paths", []):
        fail("use-cases.json current use case collection bundle path is not in status collection bundles")
    if today_use_case_path not in status.get("use_case_pages", []):
        fail("status.json missing current use case page path")
    require_contains(
        DOCS / today_use_case_path,
        [
            today_use_case["short_label"],
            manifest["title"],
            "Use case",
            "Download collection bundle",
            "Support this use case",
            today_use_case_support_intent,
            today_use_case_bundle_path,
            "Product checkout is not connected",
            "CollectionPage",
            "DonateAction",
            "og:image",
            "twitter:card",
        ],
    )
    templates_index = str(status.get("templates_index", "templates/index.html")).strip("/")
    templates_json_path = str(status.get("templates_json", "templates/templates.json")).strip("/")
    require_contains(DOCS / templates_index, ["Templates", "Evergreen landing pages", "Open template", "CollectionPage", "og:image", "twitter:card"])
    templates_json = read_json(DOCS / templates_json_path)
    template_rows = templates_json.get("items", [])
    if len(template_rows) < expected_template_count:
        fail(f"templates.json template count is {len(template_rows)}, expected at least {expected_template_count}")
    today_template = next(
        (
            template
            for template in template_rows
            if template.get("id") == manifest["id"]
        ),
        None,
    )
    if not today_template:
        fail(f"templates.json does not assign current manifest id: {manifest['id']}")
    today_template_path = str(today_template.get("path", today_template_path)).strip("/")
    if today_template.get("support_page_url") != template_support_url:
        fail("templates.json current template missing template support page URL")
    if today_template.get("support_intent_url") != template_support_intent_url:
        fail("templates.json current template missing template support-intent URL")
    if today_template_path not in status.get("template_pages", []):
        fail("status.json missing current template page path")
    if template_support_url not in status.get("template_support_page_urls", []):
        fail("status.json missing current template support page URL")
    if template_support_intent_url not in status.get("template_support_intent_urls", []):
        fail("status.json missing current template support-intent URL")
    if int(status.get("template_support_intent_count", 0)) < expected_template_count:
        fail("status.json template_support_intent_count is too low")
    require_contains(
        DOCS / today_template_path,
        [
            manifest["title"],
            "Template",
            "Download page",
            "Download ZIP",
            "Support this template",
            template_support_url,
            template_support_intent_url,
            "Product checkout is not connected",
            "CreativeWork",
            "Product",
            "DonateAction",
            "DownloadAction",
            "og:image",
            "twitter:card",
        ],
    )
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
    today_offer_support_intent = f"https://www.calmsprout.com/daily-shelf/offers/{today_offer['slug']}/support/go"
    today_collection_bundle_path = str(today_offer.get("collection_bundle_path") or "").strip("/")
    today_collection_bundle_url = f"https://x26dotapp.github.io/daily-autodigital-shelf/{today_collection_bundle_path}"
    if not today_collection_bundle_path:
        fail("offers.json current offer missing collection_bundle_path")
    if today_offer.get("collection_bundle_url") != today_collection_bundle_url:
        fail("offers.json current offer collection_bundle_url does not match the public bundle path")
    if today_collection_bundle_path not in status.get("collection_bundle_paths", []):
        fail("status.json missing current offer collection bundle path")
    require_file(DOCS / today_collection_bundle_path, 3000)
    if not status.get("store_connected"):
        if today_offer.get("support_url") != today_offer_support_intent:
            fail("offers.json current offer support_url is not the measured CalmSprout support-intent route")
        if today_offer.get("branded_support_intent_url") != today_offer_support_intent:
            fail("offers.json current offer missing branded_support_intent_url")
        if not str(today_offer.get("external_support_destination") or "").startswith(("https://", "http://")):
            fail("offers.json current offer missing external_support_destination")
        if today_offer_support_intent not in status.get("collection_support_intent_urls", []):
            fail("status.json missing current offer collection support-intent URL")
        if int(status.get("collection_support_intent_count", 0)) < 3:
            fail("status.json collection_support_intent_count is too low")
    offer_page = DOCS / str(today_offer.get("path", f"offers/{today_offer['slug']}.html")).strip("/")
    require_contains(
        offer_page,
        [
            today_offer["label"],
            manifest["title"],
            "Collection offer",
            "Download collection bundle",
            "Download starter bundle",
            offer_cta_needle,
            today_offer_support_intent,
            today_collection_bundle_path,
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
        for suffix in ["product-feed.json", "product-feed.xml", "product-feed.csv"]:
            if not any(name.endswith(suffix) for name in names):
                fail(f"Store import kit ZIP missing {suffix}")
        for suffix in ["support-funnel.json", "support-funnel.xml", "support-funnel.csv"]:
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
            "daily-autodigital-shelf-starter/SUPPORT.txt",
            "daily-autodigital-shelf-starter/STARTER-BUNDLE-MANIFEST.json",
            "daily-autodigital-shelf-starter/terms.html",
            "daily-autodigital-shelf-starter/license.html",
            "daily-autodigital-shelf-starter/privacy.html",
            "daily-autodigital-shelf-starter/refund-policy.html",
            "daily-autodigital-shelf-starter/support.html",
            "daily-autodigital-shelf-starter/pay-what-you-can.html",
            "daily-autodigital-shelf-starter/offers/index.html",
            "daily-autodigital-shelf-starter/offers/offers.json",
            "daily-autodigital-shelf-starter/use-cases/index.html",
            "daily-autodigital-shelf-starter/use-cases/use-cases.json",
            "daily-autodigital-shelf-starter/templates/index.html",
            "daily-autodigital-shelf-starter/templates/templates.json",
            f"daily-autodigital-shelf-starter/{today_use_case_path}",
            f"daily-autodigital-shelf-starter/{today_template_path}",
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
        starter_support_text = bundle.read("daily-autodigital-shelf-starter/SUPPORT.txt").decode("utf-8")
        for needle in ["Pay what you can page", "Support is voluntary", "Product checkout is not connected"]:
            if needle not in starter_support_text:
                fail(f"Starter bundle SUPPORT.txt missing {needle}")
    with zipfile.ZipFile(DOCS / today_collection_bundle_path) as collection_zip:
        names = collection_zip.namelist()
        if any(name.startswith("/") or ".." in Path(name).parts for name in names):
            fail("Collection bundle ZIP contains unsafe archive paths")
        for suffix in ["README.txt", "SUPPORT.txt", "COLLECTION-BUNDLE-MANIFEST.json", "manifest.json", "seller-copy.md", ".zip"]:
            if not any(name.endswith(suffix) for name in names):
                fail(f"Collection bundle ZIP missing {suffix}")
        if not any(name.endswith(today_use_case_path) for name in names):
            fail(f"Collection bundle ZIP missing {today_use_case_path}")
        if not any(name.endswith(today_template_path) for name in names):
            fail(f"Collection bundle ZIP missing {today_template_path}")
        support_name = next((name for name in names if name.endswith("SUPPORT.txt")), "")
        support_text = collection_zip.read(support_name).decode("utf-8") if support_name else ""
        for needle in [today_offer_support_intent, "Support is voluntary", "Product checkout is not connected"]:
            if needle not in support_text:
                fail(f"Collection bundle SUPPORT.txt missing {needle}")
    require_file(DOCS / "sitemap.xml", 100)
    require_contains(DOCS / "sitemap.xml", ["starter-bundle.html", "support.html", "pay-what-you-can.html", "offers/", "offers/offers.json", today_collection_bundle_path, "topics/", "topics/topics.json", "use-cases/", "use-cases/use-cases.json", today_use_case_path, "templates/", "templates/templates.json", today_template_path, "terms.html", "privacy.html", "license.html", "refund-policy.html", "feed.xml", "atom.xml", "product-feed.json", "product-feed.xml", "product-feed.csv", "support-funnel.json", "support-funnel.xml", "support-funnel.csv", "llms.txt", "llms-full.txt"])
    require_contains(DOCS / "sitemap.xml", [download_page_url])
    require_contains(DOCS / "robots.txt", ["User-agent: *", "Sitemap:"])
    require_file(DOCS / ".nojekyll", 0)
    require_file(ROOT / "tools" / "submit_indexnow.py", 4000)
    require_contains(
        ROOT / "tools" / "submit_indexnow.py",
        ["bundles/starter-archive.zip", "collection_bundle_path", "imports/store-upload-kit.zip", "use-cases/index.html", "use-cases/use-cases.json", "templates/index.html", "templates/templates.json", "product-feed.json", "product-feed.xml", "product-feed.csv", "support-funnel.json", "support-funnel.xml", "support-funnel.csv", "today_download", "today_download_page", "download_url", "download_page_url"],
    )
    require_file(ROOT / "tools" / "submit_calmsprout_indexnow.py", 4000)
    require_contains(
        ROOT / "tools" / "submit_calmsprout_indexnow.py",
        ["/daily-shelf/today.zip", "/daily-shelf/current.zip", "/daily-shelf/packs/{slug}/", "/daily-shelf/downloads/{slug}.zip", "/daily-shelf/downloads/{slug}.html", "/daily-shelf/bundles/{bundle_name}", "/daily-shelf/products", "/daily-shelf/products/", "/daily-shelf/offers.json", "/daily-shelf/offers/{slug}", "/daily-shelf/offers/{slug}/support/go", "/daily-shelf/use-cases", "/daily-shelf/use-cases/{slug}.html", "/daily-shelf/use-cases/use-cases.json", "/daily-shelf/templates", "/daily-shelf/templates/{slug}.html", "/daily-shelf/templates/{slug}/support", "/daily-shelf/templates/{slug}/support/go", "/daily-shelf/templates/templates.json", "/daily-shelf/product-feed.json", "/daily-shelf/product-feed.xml", "/daily-shelf/product-feed.csv", "/daily-shelf/support-funnel.json", "/daily-shelf/support-funnel.xml", "/daily-shelf/support-funnel.csv", "/daily-shelf/support-metrics.json", "/daily-shelf/support/go", "/daily-shelf/products/{slug}/support", "/daily-shelf/product-sitemap.xml"],
    )
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
        if status.get("store_connected"):
            require_contains(offer_page, [destination_url])
        require_contains(DOCS / "llms.txt", [destination_url])
        require_contains(DOCS / "llms-full.txt", [destination_url])
        pack_destination_needle = (branded_support_intent_url or destination_url) if status.get("support_connected") else destination_url
        require_contains(pack_dir / "index.html", [pack_destination_needle])
        if catalog_item.get("monetization_destination_url") != destination_url:
            fail("catalog.json current item missing monetization destination URL")
        if catalog_item.get("support_page_url") != "https://x26dotapp.github.io/daily-autodigital-shelf/support.html":
            fail("catalog.json current item missing support_page_url")
        if catalog_item.get("pay_what_you_can_url") != "https://x26dotapp.github.io/daily-autodigital-shelf/pay-what-you-can.html":
            fail("catalog.json current item missing pay_what_you_can_url")
        if catalog_item.get("branded_product_url") != branded_product_url:
            fail("catalog.json current item missing branded_product_url")
        if catalog_item.get("branded_support_url") != branded_support_url:
            fail("catalog.json current item missing branded_support_url")
        if catalog_item.get("branded_support_intent_url") != branded_support_intent_url:
            fail("catalog.json current item missing branded_support_intent_url")
        if catalog_item.get("download_page_url") != download_page_url:
            fail("catalog.json current item missing download_page_url")
        import_row = next((item for item in import_json.get("items", []) if item.get("sku", "").endswith(manifest["id"].split(":")[-1])), None)
        if not import_row:
            fail("store-listings.json missing current item")
        if import_row.get("monetization_destination_url") != destination_url:
            fail("store-listings.json current item missing monetization destination URL")
        if import_row.get("support_page_url") != "https://x26dotapp.github.io/daily-autodigital-shelf/support.html":
            fail("store-listings.json current item missing support_page_url")
        if import_row.get("pay_what_you_can_url") != "https://x26dotapp.github.io/daily-autodigital-shelf/pay-what-you-can.html":
            fail("store-listings.json current item missing pay_what_you_can_url")
        if import_row.get("branded_product_url") != branded_product_url:
            fail("store-listings.json current item missing branded_product_url")
        if import_row.get("branded_support_url") != branded_support_url:
            fail("store-listings.json current item missing branded_support_url")
        if import_row.get("branded_support_intent_url") != branded_support_intent_url:
            fail("store-listings.json current item missing branded_support_intent_url")
        if import_row.get("download_page_url") != download_page_url:
            fail("store-listings.json current item missing download_page_url")
        if status.get("today_branded_product_url") != branded_product_url:
            fail("status.json missing today_branded_product_url")
        if status.get("today_branded_support_url") != branded_support_url:
            fail("status.json missing today_branded_support_url")
        if status.get("today_branded_support_intent_url") != branded_support_intent_url:
            fail("status.json missing today_branded_support_intent_url")
        require_contains(DOCS / "llms.txt", [branded_support_intent_url])
        require_contains(DOCS / "llms-full.txt", [branded_support_intent_url])
    if not status.get("bundle_ready"):
        fail("status.json reports bundle_ready=false")
    if int(status.get("bundle_pack_count") or 0) < min_pack_count:
        fail(f"status.json bundle_pack_count is {status.get('bundle_pack_count')}, expected at least {min_pack_count}")
    if int(status.get("pack_download_count") or 0) < min_pack_count:
        fail(f"status.json pack_download_count is {status.get('pack_download_count')}, expected at least {min_pack_count}")
    if status.get("today_download") != manifest.get("download"):
        fail(f"status.json today_download is {status.get('today_download')}, expected {manifest.get('download')}")
    if status.get("today_download_page") != download_page_rel:
        fail(f"status.json today_download_page is {status.get('today_download_page')}, expected {download_page_rel}")
    if int(status.get("pack_download_page_count") or 0) < min_pack_count:
        fail(f"status.json pack_download_page_count is {status.get('pack_download_page_count')}, expected at least {min_pack_count}")
    if status.get("feed_json") != "feed.json" or status.get("feed_xml") != "feed.xml" or status.get("atom_xml") != "atom.xml":
        fail("status.json missing feed_json/feed_xml/atom_xml paths")
    if int(status.get("feed_item_count") or 0) < min_pack_count:
        fail(f"status.json feed_item_count is {status.get('feed_item_count')}, expected at least {min_pack_count}")
    if not status.get("product_feed_ready"):
        fail("status.json reports product_feed_ready=false")
    if status.get("product_feed_json") != "product-feed.json" or status.get("product_feed_xml") != "product-feed.xml" or status.get("product_feed_csv") != "product-feed.csv":
        fail("status.json missing product feed paths")
    if int(status.get("product_feed_count") or 0) < min_pack_count:
        fail(f"status.json product_feed_count is {status.get('product_feed_count')}, expected at least {min_pack_count}")
    if not status.get("support_funnel_ready"):
        fail("status.json reports support_funnel_ready=false")
    if status.get("support_funnel_json") != "support-funnel.json" or status.get("support_funnel_xml") != "support-funnel.xml" or status.get("support_funnel_csv") != "support-funnel.csv":
        fail("status.json missing support funnel feed paths")
    if int(status.get("support_funnel_count") or 0) < min_pack_count:
        fail(f"status.json support_funnel_count is {status.get('support_funnel_count')}, expected at least {min_pack_count}")
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
    if not status.get("use_case_pages_ready"):
        fail("status.json reports use_case_pages_ready=false")
    if int(status.get("use_case_page_count") or 0) < 3:
        fail(f"status.json use_case_page_count is {status.get('use_case_page_count')}, expected at least 3")
    if status.get("use_cases_index") != "use-cases/index.html" or status.get("use_cases_json") != "use-cases/use-cases.json":
        fail("status.json missing use cases index/json paths")
    if not status.get("template_pages_ready"):
        fail("status.json reports template_pages_ready=false")
    if int(status.get("template_page_count") or 0) < expected_template_count:
        fail(f"status.json template_page_count is {status.get('template_page_count')}, expected at least {expected_template_count}")
    if status.get("templates_index") != "templates/index.html" or status.get("templates_json") != "templates/templates.json":
        fail("status.json missing templates index/json paths")
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
    if not status.get("collection_bundle_ready"):
        fail("status.json reports collection_bundle_ready=false")
    if int(status.get("collection_bundle_count") or 0) < 3:
        fail(f"status.json collection_bundle_count is {status.get('collection_bundle_count')}, expected at least 3")
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
        "use_case_page_count": int(status.get("use_case_page_count") or 0),
        "template_page_count": int(status.get("template_page_count") or 0),
        "policy_page_count": int(status.get("policy_page_count") or 0),
        "files_checked": 52,
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
    parser.add_argument("--min-pack-count", type=int, default=29, help="Minimum generated pack manifests expected.")
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
