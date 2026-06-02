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
    today_guide_path = f"guides/{template_slug}.html"
    expected_template_count = len(
        {
            evergreen_slug(path.parent.name)
            for path in (DOCS / "packs").glob("*/manifest.json")
        }
    )
    printable_rel = f"packs/{pack_slug}/printable.html"
    checklist_rel = f"packs/{pack_slug}/checklist.html"
    printable_url = f"https://x26dotapp.github.io/daily-autodigital-shelf/{printable_rel}"
    checklist_url = f"https://x26dotapp.github.io/daily-autodigital-shelf/{checklist_rel}"
    download_page_rel = f"downloads/{pack_slug}.html"
    download_page_url = f"https://x26dotapp.github.io/daily-autodigital-shelf/{download_page_rel}"
    branded_product_url = f"https://www.calmsprout.com/daily-shelf/products/{pack_slug}"
    branded_support_url = f"{branded_product_url}/support"
    branded_support_intent_url = f"{branded_support_url}/go"
    branded_printable_url = f"https://www.calmsprout.com/daily-shelf/{printable_rel}"
    branded_checklist_url = f"https://www.calmsprout.com/daily-shelf/{checklist_rel}"
    general_support_intent_url = "https://www.calmsprout.com/daily-shelf/support/go"
    template_support_url = f"https://www.calmsprout.com/daily-shelf/templates/{template_slug}/support"
    template_support_intent_url = f"{template_support_url}/go"
    preferred_collection_bundle_page = "bundles/small-business-ops-collection.html"
    preferred_collection_bundle_page_url = f"https://x26dotapp.github.io/daily-autodigital-shelf/{preferred_collection_bundle_page}"
    preferred_collection_bundle_branded_page_url = f"https://www.calmsprout.com/daily-shelf/{preferred_collection_bundle_page}"
    support_card_path = "assets/support-card.svg"
    support_card_url = f"https://x26dotapp.github.io/daily-autodigital-shelf/{support_card_path}"
    support_signal_page = "support-signal.html"
    support_signal_json = "support-signal.json"
    checkout_readiness_page = "checkout-readiness.html"
    checkout_readiness_json = "checkout-readiness.json"
    revenue_proof_page = "revenue-proof.html"
    revenue_proof_json = "revenue-proof.json"
    daily_offer_page = "daily-offer.html"
    daily_offer_json = "daily-offer.json"
    support_signal_page_url = f"https://x26dotapp.github.io/daily-autodigital-shelf/{support_signal_page}"
    support_signal_json_url = f"https://x26dotapp.github.io/daily-autodigital-shelf/{support_signal_json}"
    support_signal_branded_page_url = "https://www.calmsprout.com/daily-shelf/support-signal.html"
    support_signal_branded_json_url = "https://www.calmsprout.com/daily-shelf/support-signal.json"
    checkout_readiness_page_url = f"https://x26dotapp.github.io/daily-autodigital-shelf/{checkout_readiness_page}"
    checkout_readiness_json_url = f"https://x26dotapp.github.io/daily-autodigital-shelf/{checkout_readiness_json}"
    checkout_readiness_branded_page_url = "https://www.calmsprout.com/daily-shelf/checkout-readiness.html"
    checkout_readiness_branded_json_url = "https://www.calmsprout.com/daily-shelf/checkout-readiness.json"
    revenue_proof_page_url = f"https://x26dotapp.github.io/daily-autodigital-shelf/{revenue_proof_page}"
    revenue_proof_json_url = f"https://x26dotapp.github.io/daily-autodigital-shelf/{revenue_proof_json}"
    revenue_proof_branded_page_url = "https://www.calmsprout.com/daily-shelf/revenue-proof.html"
    revenue_proof_branded_json_url = "https://www.calmsprout.com/daily-shelf/revenue-proof.json"
    daily_offer_page_url = f"https://x26dotapp.github.io/daily-autodigital-shelf/{daily_offer_page}"
    daily_offer_json_url = f"https://x26dotapp.github.io/daily-autodigital-shelf/{daily_offer_json}"
    daily_offer_branded_page_url = "https://www.calmsprout.com/daily-shelf/daily-offer.html"
    daily_offer_branded_json_url = "https://www.calmsprout.com/daily-shelf/daily-offer.json"
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
    artifact_support_needles = ["Support this pack", "Delivery does not require manual fulfillment"]
    if status.get("store_connected"):
        artifact_support_needles.extend(["Open product checkout", str(status.get("monetization_destination_url") or "")])
    elif status.get("support_connected"):
        artifact_support_needles.extend([branded_support_intent_url, "Product checkout is not connected", "Downloads remain public"])
    else:
        artifact_support_needles.extend(["Open support page", "No external store, support, or affiliate destination is connected yet"])

    require_file(DOCS / support_card_path, 1000)
    require_contains(
        DOCS / support_card_path,
        [
            "Daily Autodigital Shelf",
            "Support card",
            "Public downloads stay free",
            "No product checkout claim",
            "No payment credentials",
            "www.calmsprout.com/daily-shelf/support/go",
        ],
    )

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
            "guides/",
            "commercial-use.html",
            "sponsor.html",
            "pricing.html",
            "offers/",
            preferred_collection_bundle_page,
            "starter-bundle.html",
            "starter-archive.zip",
            "support.html",
            "pay-what-you-can.html",
            support_signal_page,
            support_signal_json,
            checkout_readiness_page,
            checkout_readiness_json,
            revenue_proof_page,
            revenue_proof_json,
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
    require_contains(pack_dir / "printable.html", artifact_support_needles)
    require_contains(pack_dir / "checklist.html", artifact_support_needles)
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
        for suffix in ["printable.html", "checklist.html"]:
            artifact_name = next((name for name in names if name.endswith(suffix)), "")
            artifact_text = pack_zip.read(artifact_name).decode("utf-8") if artifact_name else ""
            for needle in artifact_support_needles:
                if needle and needle not in artifact_text:
                    fail(f"Pack ZIP {suffix} missing {needle}")
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
    support_signal = read_json(DOCS / support_signal_json)
    if support_signal.get("kind") != "daily-shelf-support-signal":
        fail("support-signal.json has wrong kind")
    if not support_signal.get("promoted"):
        fail("support-signal.json missing promoted target")
    if int(support_signal.get("total_support_intent_clicks") or 0) < 0:
        fail("support-signal.json has invalid total support-intent clicks")
    if int(support_signal.get("total_download_interest") or 0) < 0:
        fail("support-signal.json has invalid total download interest")
    require_contains(
        DOCS / support_signal_json,
        [
            "daily-shelf-support-signal",
            "revenue_boundary",
            "download_revenue_boundary",
            "download_source_url",
            "total_download_interest",
            "top_products",
            "top_collections",
            "top_download_products",
            "promoted",
            "promotion_url",
            "signal_score",
            "download_interest",
            "support_intent_url",
        ],
    )
    require_contains(
        DOCS / support_signal_page,
        [
            "Support Signal",
            "Promote what shows support or download intent",
            "Top pack routes",
            "Top bundle routes",
            "Intent is not income",
            "download interest",
            "does not prove payments or daily revenue",
            support_signal_json,
            "Dataset",
            "og:image",
            "twitter:card",
        ],
    )
    require_contains(DOCS / "archive.html", ["Pack archive", manifest["title"], "Starter bundle", "Topics", "Use cases", "Offers", "Support", "Policies", "Import kit", "Catalog CSV", "Download page", "ItemList", "og:image", "twitter:card"])
    require_contains(DOCS / "archive.html", ["Templates", "template pages"])
    require_contains(DOCS / "starter-bundle.html", ["Starter bundle", "Download ZIP", "starter-archive.zip", support_card_path, "Download page", "Topics", "Use cases", "Templates", "Guides", "Commercial use", "Sponsor", "Offers", "Support", "Policies", "ItemList", "og:image", "twitter:card"])
    require_contains(DOCS / "support.html", ["Support this shelf", "Download starter bundle", preferred_collection_bundle_page, support_card_path, daily_offer_page, support_signal_page, checkout_readiness_page, "Current support-interest target", "Commercial use", "Sponsor", general_support_intent_url, "This is not product checkout", "WebPage", "og:image", "twitter:card"])
    require_contains(DOCS / "pay-what-you-can.html", ["Pay what you can", "Download starter ZIP", preferred_collection_bundle_page, support_card_path, "Suggested support", "Simple levels", "Commercial use", "Sponsor", general_support_intent_url, "This is not product checkout", "WebPage", "og:image", "twitter:card"])
    require_contains(DOCS / "pricing.html", ["Pricing", "Clear support levels", "Value ladder", support_card_path, "https://www.calmsprout.com/daily-shelf/pricing/support/go", "Product checkout is not connected", "OfferCatalog", "FAQPage", "DonateAction", "og:image", "twitter:card"])
    require_contains(DOCS / "commercial-use.html", ["Commercial use", "Use the templates internally", "Read license", "Browse templates", "Browse guides", "https://www.calmsprout.com/daily-shelf/commercial-use/support/go", "Product checkout is not connected", "FAQPage", "DonateAction", "og:image", "twitter:card"])
    require_contains(DOCS / "sponsor.html", ["Sponsor", "Support ladder", "Sponsor kit JSON", "sponsor-kit.json", "https://www.calmsprout.com/daily-shelf/sponsor/support/go", "Product checkout is not connected", "FAQPage", "DonateAction", "og:image", "twitter:card"])
    sponsor_kit = read_json(DOCS / "sponsor-kit.json")
    if int(sponsor_kit.get("numberOfItems") or 0) < 3:
        fail("sponsor-kit.json support tier count is too low")
    if sponsor_kit.get("support_intent_url") != "https://www.calmsprout.com/daily-shelf/sponsor/support/go":
        fail("sponsor-kit.json missing branded sponsor support-intent URL")
    if sponsor_kit.get("commercial_support_intent_url") != "https://www.calmsprout.com/daily-shelf/commercial-use/support/go":
        fail("sponsor-kit.json missing branded commercial support-intent URL")
    if sponsor_kit.get("pricing_support_intent_url") != "https://www.calmsprout.com/daily-shelf/pricing/support/go":
        fail("sponsor-kit.json missing branded pricing support-intent URL")
    require_contains(DOCS / "sponsor-kit.json", ["Daily Autodigital Shelf Sponsor Kit", "Commercial-use supporter", "Product checkout is not connected", "pricing_support_intent_url", "sponsor_support_intent_url", "commercial_support_intent_url"])
    require_contains(DOCS / "store-import.html", ["Store import kit", "Download import kit", "Marketplace queue", "topic_urls", "Policy pages", "license, terms, privacy, and refund", manifest["title"], "Commercial use", "Sponsor kit", "Offers", "Support", "Support signal", "ItemList", "og:image", "twitter:card"])
    require_contains(DOCS / "imports" / "store-listings.csv", ["download_url", "download_page_url", "preview_url", "price_hint", "support_page_url", "pay_what_you_can_url", "branded_product_url", "branded_support_url", "branded_support_intent_url", "monetization_destination_url", "topic_urls", manifest["title"]])
    require_contains(DOCS / "llms.txt", ["Daily Autodigital Shelf", "Support page", "Sponsor page", "Commercial use page", "Sponsor Kit JSON", "Support card SVG", support_card_url, daily_offer_page_url, daily_offer_json_url, support_signal_page_url, support_signal_json_url, checkout_readiness_page_url, checkout_readiness_json_url, revenue_proof_page_url, revenue_proof_json_url, preferred_collection_bundle_page_url, "Monetization destination", "Branded support intent redirect", "Download page", "Product Feed JSON", "Support Funnel JSON", "Daily Offer JSON", "Support Signal JSON", "Checkout Readiness JSON", "Revenue Proof JSON", "Templates", "Guides", "Product checkout is not connected"])
    require_contains(DOCS / "llms-full.txt", ["Daily Autodigital Shelf Full Context", "Generated Packs", manifest["title"], "Download page", "Product Feed JSON", "Support Funnel JSON", "Daily Offer JSON", "Support Signal JSON", "Checkout Readiness JSON", "Revenue Proof JSON", "Sponsor Kit JSON", "Support card SVG", support_card_url, daily_offer_page_url, daily_offer_json_url, support_signal_page_url, checkout_readiness_json_url, revenue_proof_json_url, "Use Cases JSON", "Templates JSON", "Guides JSON", preferred_collection_bundle_page_url, "Machine-Readable Files", "status.json"])
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
    guides_index = str(status.get("guides_index", "guides/index.html")).strip("/")
    guides_json_path = str(status.get("guides_json", "guides/guides.json")).strip("/")
    require_contains(DOCS / guides_index, ["Guides", "How-to pages", "Open guide", "CollectionPage", "og:image", "twitter:card"])
    guides_json = read_json(DOCS / guides_json_path)
    guide_rows = guides_json.get("items", [])
    if len(guide_rows) < expected_template_count:
        fail(f"guides.json guide count is {len(guide_rows)}, expected at least {expected_template_count}")
    today_guide = next(
        (
            guide
            for guide in guide_rows
            if guide.get("id") == manifest["id"]
        ),
        None,
    )
    if not today_guide:
        fail(f"guides.json does not assign current manifest id: {manifest['id']}")
    today_guide_path = str(today_guide.get("path", today_guide_path)).strip("/")
    if today_guide_path not in status.get("guide_pages", []):
        fail("status.json missing current guide page path")
    guide_branded_url = f"https://www.calmsprout.com/daily-shelf/guides/{template_slug}.html"
    if guide_branded_url not in status.get("guide_branded_urls", []):
        fail("status.json missing current branded guide URL")
    require_contains(
        DOCS / today_guide_path,
        [
            manifest["title"],
            "How-to guide",
            "Five steps, no manual delivery",
            "Download page",
            "Template page",
            "Support page",
            template_support_url,
            "Product checkout is not connected",
            "HowTo",
            "FAQPage",
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
    today_collection_bundle_page_path = str(today_offer.get("collection_bundle_page_path") or "").strip("/")
    today_collection_bundle_page_url = f"https://x26dotapp.github.io/daily-autodigital-shelf/{today_collection_bundle_page_path}"
    if not today_collection_bundle_path:
        fail("offers.json current offer missing collection_bundle_path")
    if today_offer.get("collection_bundle_url") != today_collection_bundle_url:
        fail("offers.json current offer collection_bundle_url does not match the public bundle path")
    if not today_collection_bundle_page_path:
        fail("offers.json current offer missing collection_bundle_page_path")
    if today_offer.get("collection_bundle_page_url") != today_collection_bundle_page_url:
        fail("offers.json current offer collection_bundle_page_url does not match the public bundle page path")
    if today_collection_bundle_path not in status.get("collection_bundle_paths", []):
        fail("status.json missing current offer collection bundle path")
    if today_collection_bundle_page_path not in status.get("collection_bundle_page_paths", []):
        fail("status.json missing current offer collection bundle page path")
    require_file(DOCS / today_collection_bundle_path, 3000)
    require_contains(
        DOCS / today_collection_bundle_page_path,
        [
            today_offer["label"],
            manifest["title"],
            "Collection bundle",
            "Download collection ZIP",
            "Support this collection",
            today_offer_support_intent,
            today_collection_bundle_path,
            support_card_path,
            "Product checkout is not connected",
            "Product",
            "FAQPage",
            "DownloadAction",
            "DonateAction",
            "og:image",
            "twitter:card",
        ],
    )
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
            "Open bundle page",
            "Download starter bundle",
            offer_cta_needle,
            today_offer_support_intent,
            today_collection_bundle_path,
            today_collection_bundle_page_path,
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
        for suffix in ["README.txt", "store-listings.csv", "store-listings.json", "terms.html", "privacy.html", "license.html", "refund-policy.html", "pricing.html", "commercial-use.html", "sponsor.html", "sponsor-kit.json", support_signal_page, support_signal_json, "seller-copy.md", ".zip"]:
            if not any(name.endswith(suffix) for name in names):
                fail(f"Store import kit ZIP missing {suffix}")
        for suffix in ["product-feed.json", "product-feed.xml", "product-feed.csv"]:
            if not any(name.endswith(suffix) for name in names):
                fail(f"Store import kit ZIP missing {suffix}")
        for suffix in ["support-funnel.json", "support-funnel.xml", "support-funnel.csv"]:
            if not any(name.endswith(suffix) for name in names):
                fail(f"Store import kit ZIP missing {suffix}")
        for suffix in ["guides/index.html", "guides/guides.json", today_guide_path]:
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
            "daily-autodigital-shelf-starter/assets/support-card.svg",
            "daily-autodigital-shelf-starter/terms.html",
            "daily-autodigital-shelf-starter/license.html",
            "daily-autodigital-shelf-starter/privacy.html",
            "daily-autodigital-shelf-starter/refund-policy.html",
            "daily-autodigital-shelf-starter/support.html",
            f"daily-autodigital-shelf-starter/{support_signal_page}",
            f"daily-autodigital-shelf-starter/{support_signal_json}",
            "daily-autodigital-shelf-starter/pay-what-you-can.html",
            "daily-autodigital-shelf-starter/pricing.html",
            "daily-autodigital-shelf-starter/commercial-use.html",
            "daily-autodigital-shelf-starter/sponsor.html",
            "daily-autodigital-shelf-starter/sponsor-kit.json",
            "daily-autodigital-shelf-starter/offers/index.html",
            "daily-autodigital-shelf-starter/offers/offers.json",
            "daily-autodigital-shelf-starter/use-cases/index.html",
            "daily-autodigital-shelf-starter/use-cases/use-cases.json",
            "daily-autodigital-shelf-starter/templates/index.html",
            "daily-autodigital-shelf-starter/templates/templates.json",
            "daily-autodigital-shelf-starter/guides/index.html",
            "daily-autodigital-shelf-starter/guides/guides.json",
            f"daily-autodigital-shelf-starter/{today_use_case_path}",
            f"daily-autodigital-shelf-starter/{today_template_path}",
            f"daily-autodigital-shelf-starter/{today_guide_path}",
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
        starter_card_text = bundle.read("daily-autodigital-shelf-starter/assets/support-card.svg").decode("utf-8")
        for needle in ["Support card", "No product checkout claim", "No payment credentials"]:
            if needle not in starter_card_text:
                fail(f"Starter bundle support-card.svg missing {needle}")
    with zipfile.ZipFile(DOCS / today_collection_bundle_path) as collection_zip:
        names = collection_zip.namelist()
        if any(name.startswith("/") or ".." in Path(name).parts for name in names):
            fail("Collection bundle ZIP contains unsafe archive paths")
        collection_card_name = next((name for name in names if name.endswith("assets/support-card.svg")), "")
        if not collection_card_name:
            fail("Collection bundle ZIP missing assets/support-card.svg")
        for suffix in ["README.txt", "SUPPORT.txt", "COLLECTION-BUNDLE-MANIFEST.json", "manifest.json", "seller-copy.md", ".zip"]:
            if not any(name.endswith(suffix) for name in names):
                fail(f"Collection bundle ZIP missing {suffix}")
        if not any(name.endswith(today_use_case_path) for name in names):
            fail(f"Collection bundle ZIP missing {today_use_case_path}")
        if not any(name.endswith(today_template_path) for name in names):
            fail(f"Collection bundle ZIP missing {today_template_path}")
        if not any(name.endswith(today_guide_path) for name in names):
            fail(f"Collection bundle ZIP missing {today_guide_path}")
        support_name = next((name for name in names if name.endswith("SUPPORT.txt")), "")
        support_text = collection_zip.read(support_name).decode("utf-8") if support_name else ""
        for needle in [today_offer_support_intent, "Support is voluntary", "Product checkout is not connected"]:
            if needle not in support_text:
                fail(f"Collection bundle SUPPORT.txt missing {needle}")
        collection_card_text = collection_zip.read(collection_card_name).decode("utf-8")
        for needle in ["Support card", "No product checkout claim", "No payment credentials"]:
            if needle not in collection_card_text:
                fail(f"Collection bundle support-card.svg missing {needle}")
    require_file(DOCS / "sitemap.xml", 100)
    require_contains(DOCS / "sitemap.xml", ["starter-bundle.html", "support.html", "pay-what-you-can.html", daily_offer_page, daily_offer_json, support_signal_page, support_signal_json, checkout_readiness_page, checkout_readiness_json, revenue_proof_page, revenue_proof_json, "pricing.html", support_card_path, "commercial-use.html", "sponsor.html", "sponsor-kit.json", "offers/", "offers/offers.json", today_collection_bundle_path, today_collection_bundle_page_path, "topics/", "topics/topics.json", "use-cases/", "use-cases/use-cases.json", today_use_case_path, "templates/", "templates/templates.json", today_template_path, "guides/", "guides/guides.json", today_guide_path, "terms.html", "privacy.html", "license.html", "refund-policy.html", "feed.xml", "atom.xml", "product-feed.json", "product-feed.xml", "product-feed.csv", "support-funnel.json", "support-funnel.xml", "support-funnel.csv", "llms.txt", "llms-full.txt"])
    require_contains(DOCS / "sitemap.xml", [download_page_url, printable_url, checklist_url])
    require_contains(DOCS / "robots.txt", ["User-agent: *", "Sitemap:"])
    require_file(DOCS / ".nojekyll", 0)
    require_file(ROOT / "tools" / "sync_download_metrics.py", 3000)
    require_contains(ROOT / "tools" / "sync_download_metrics.py", ["download-metrics.json", "total_download_interest", "daily-shelf-download-metrics-snapshot"])
    require_contains(ROOT / "tools" / "sync_checkout_readiness.py", ["checkout-readiness-snapshot.json", "counter_route_skipped", "daily-shelf-checkout-readiness-snapshot"])
    require_contains(ROOT / "tools" / "sync_revenue_proofs.py", ["revenue-proof-snapshot.json", "actual_daily_revenue_proven", "daily-shelf-revenue-proof-snapshot"])
    require_file(ROOT / "tools" / "submit_indexnow.py", 4000)
    require_contains(
        ROOT / "tools" / "submit_indexnow.py",
        ["bundles/starter-archive.zip", support_card_path, daily_offer_page, daily_offer_json, support_signal_page, support_signal_json, checkout_readiness_page, checkout_readiness_json, revenue_proof_page, revenue_proof_json, "collection_bundle_path", "collection_bundle_page_path", "imports/store-upload-kit.zip", "commercial-use.html", "sponsor.html", "sponsor-kit.json", "use-cases/index.html", "use-cases/use-cases.json", "templates/index.html", "templates/templates.json", "guides/index.html", "guides/guides.json", "product-feed.json", "product-feed.xml", "product-feed.csv", "support-funnel.json", "support-funnel.xml", "support-funnel.csv", "today_download", "today_download_page", "printable.html", "checklist.html", "download_url", "download_page_url"],
    )
    require_file(ROOT / "tools" / "submit_calmsprout_indexnow.py", 4000)
    require_contains(
        ROOT / "tools" / "submit_calmsprout_indexnow.py",
        ["/daily-shelf/today.zip", "/daily-shelf/current.zip", "/daily-shelf/packs/{slug}/", "/daily-shelf/packs/{slug}/printable.html", "/daily-shelf/packs/{slug}/checklist.html", "/daily-shelf/downloads/{slug}.zip", "/daily-shelf/downloads/{slug}.html", "/daily-shelf/bundles/{bundle_name}", "/daily-shelf/bundles/{bundle_page_name}", "/daily-shelf/products", "/daily-shelf/products/", "/daily-shelf/offers.json", "/daily-shelf/offers/{slug}", "/daily-shelf/offers/{slug}/support/go", "/daily-shelf/use-cases", "/daily-shelf/use-cases/{slug}.html", "/daily-shelf/use-cases/use-cases.json", "/daily-shelf/templates", "/daily-shelf/templates/{slug}.html", "/daily-shelf/templates/{slug}/support", "/daily-shelf/templates/{slug}/support/go", "/daily-shelf/templates/templates.json", "/daily-shelf/guides", "/daily-shelf/guides/{slug}.html", "/daily-shelf/guides/guides.json", "/daily-shelf/assets/support-card.svg", "/daily-shelf/daily-offer", "/daily-shelf/daily-offer.html", "/daily-shelf/daily-offer.json", "/daily-shelf/support-signal.html", "/daily-shelf/support-signal.json", "/daily-shelf/support-signal", "/daily-shelf/checkout-readiness", "/daily-shelf/checkout-readiness.html", "/daily-shelf/checkout-readiness.json", "/daily-shelf/revenue-proof", "/daily-shelf/revenue-proof.html", "/daily-shelf/revenue-proof.json", "/daily-shelf/pricing", "/daily-shelf/pricing.html", "/daily-shelf/pricing/support/go", "/daily-shelf/commercial-use", "/daily-shelf/commercial-use.html", "/daily-shelf/commercial-use/support/go", "/daily-shelf/sponsor", "/daily-shelf/sponsor.html", "/daily-shelf/sponsor/support/go", "/daily-shelf/starter-bundle.html", "/daily-shelf/support.html", "/daily-shelf/license.html", "/daily-shelf/privacy.html", "/daily-shelf/terms.html", "/daily-shelf/sponsor-kit.json", "/daily-shelf/product-feed.json", "/daily-shelf/product-feed.xml", "/daily-shelf/product-feed.csv", "/daily-shelf/support-funnel.json", "/daily-shelf/support-funnel.xml", "/daily-shelf/support-funnel.csv", "/daily-shelf/support-metrics.json", "/daily-shelf/download-metrics.json", "/daily-shelf/support/go", "/daily-shelf/products/{slug}/support", "/daily-shelf/product-sitemap.xml"],
    )
    require_contains(
        ROOT / "run-daily.ps1",
        ["tools\\sync_support_metrics.py", "tools\\sync_download_metrics.py", "tools\\sync_checkout_readiness.py", "tools\\sync_revenue_proofs.py", "Support metrics sync complete", "Download metrics sync complete", "Checkout readiness sync complete", "Revenue proof sync complete", "tools\\submit_calmsprout_indexnow.py", "CalmSprout IndexNow submission complete"],
    )
    require_contains(
        ROOT / ".github" / "workflows" / "daily-shelf.yml",
        ["Sync public support metrics", "tools/sync_support_metrics.py", "Sync public download metrics", "tools/sync_download_metrics.py", "Sync public checkout readiness", "tools/sync_checkout_readiness.py", "Sync revenue proof evidence", "tools/sync_revenue_proofs.py", "Submit changed CalmSprout URLs to IndexNow", "tools/submit_calmsprout_indexnow.py"],
    )
    require_contains(
        ROOT / ".gitignore",
        ["state/calmsprout-indexnow-state.json", "state/revenue-proofs/inbox/*"],
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
        if status.get("today_printable") != printable_rel or status.get("today_checklist") != checklist_rel:
            fail("status.json missing today artifact paths")
        if status.get("today_printable_url") != printable_url or status.get("today_checklist_url") != checklist_url:
            fail("status.json missing today artifact URLs")
        if status.get("today_branded_printable_url") != branded_printable_url or status.get("today_branded_checklist_url") != branded_checklist_url:
            fail("status.json missing branded artifact URLs")
        if not status.get("artifact_support_links_ready"):
            fail("status.json artifact_support_links_ready is false")
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
    if not status.get("guide_pages_ready"):
        fail("status.json reports guide_pages_ready=false")
    if int(status.get("guide_page_count") or 0) < expected_template_count:
        fail(f"status.json guide_page_count is {status.get('guide_page_count')}, expected at least {expected_template_count}")
    if status.get("guides_index") != "guides/index.html" or status.get("guides_json") != "guides/guides.json":
        fail("status.json missing guides index/json paths")
    if not status.get("policy_pages_ready"):
        fail("status.json reports policy_pages_ready=false")
    if int(status.get("policy_page_count") or 0) < 4:
        fail(f"status.json policy_page_count is {status.get('policy_page_count')}, expected at least 4")
    if not status.get("support_page_ready") or status.get("support_page") != "support.html":
        fail("status.json missing support_page_ready/support.html")
    if status.get("support_page_url") != "https://x26dotapp.github.io/daily-autodigital-shelf/support.html":
        fail("status.json missing support_page_url")
    if not status.get("support_card_ready") or status.get("support_card_path") != support_card_path:
        fail("status.json missing support_card_ready/assets/support-card.svg")
    if status.get("support_card_url") != support_card_url:
        fail("status.json missing support_card_url")
    if status.get("support_card_action_url") != general_support_intent_url:
        fail("status.json missing support_card_action_url")
    if int(status.get("support_card_bytes") or 0) < 1000:
        fail("status.json support_card_bytes is too low")
    if not status.get("support_signal_ready"):
        fail("status.json reports support_signal_ready=false")
    if status.get("support_signal_page") != support_signal_page or status.get("support_signal_json") != support_signal_json:
        fail("status.json missing support signal paths")
    if status.get("support_signal_page_url") != support_signal_page_url or status.get("support_signal_json_url") != support_signal_json_url:
        fail("status.json missing support signal URLs")
    if status.get("support_signal_branded_page_url") != support_signal_branded_page_url or status.get("support_signal_branded_json_url") != support_signal_branded_json_url:
        fail("status.json missing branded support signal URLs")
    if not status.get("support_signal_source_url"):
        fail("status.json missing support_signal_source_url")
    if status.get("support_signal_download_source_url") != "https://www.calmsprout.com/daily-shelf/download-metrics.json":
        fail("status.json missing support_signal_download_source_url")
    if int(status.get("support_signal_total_download_interest") or 0) < 0:
        fail("status.json invalid support_signal_total_download_interest")
    if int(status.get("support_signal_promoted_score") or 0) < 0:
        fail("status.json invalid support_signal_promoted_score")
    promoted_signal_url = str(status.get("support_signal_promoted_url") or "")
    promoted_branded_url = str(status.get("support_signal_promoted_branded_url") or "")
    promoted_public_url = str(status.get("support_signal_promoted_public_url") or "")
    if not promoted_signal_url.startswith("https://www.calmsprout.com/daily-shelf/"):
        fail("status.json support_signal_promoted_url should prefer the branded CalmSprout route")
    if promoted_branded_url and promoted_signal_url != promoted_branded_url:
        fail("status.json support_signal_promoted_url does not match branded URL")
    if promoted_public_url == promoted_signal_url:
        fail("status.json support_signal_promoted_url fell back to the public URL")
    if status.get("support_signal_promoted_slug") == "small-business-ops" and promoted_signal_url != preferred_collection_bundle_branded_page_url:
        fail("status.json support_signal_promoted_url missing preferred branded bundle page")
    support_signal_html = (DOCS / support_signal_page).read_text(encoding="utf-8")
    if str(status.get("support_signal_promoted_title") or "") not in support_signal_html:
        fail("support-signal.html missing promoted title from status.json")
    if promoted_signal_url not in support_signal_html:
        fail("support-signal.html missing branded promoted URL")
    daily_offer = read_json(DOCS / daily_offer_json)
    if daily_offer.get("kind") != "daily-shelf-daily-offer":
        fail("daily-offer.json has wrong kind")
    if daily_offer.get("page_path") != daily_offer_page or daily_offer.get("json_path") != daily_offer_json:
        fail("daily-offer.json missing page/json paths")
    if daily_offer.get("page_url") != daily_offer_page_url or daily_offer.get("json_url") != daily_offer_json_url:
        fail("daily-offer.json missing public page/json URLs")
    if daily_offer.get("branded_page_url") != daily_offer_branded_page_url or daily_offer.get("branded_json_url") != daily_offer_branded_json_url:
        fail("daily-offer.json missing branded page/json URLs")
    if bool(daily_offer.get("store_connected")) != bool(status.get("store_connected")):
        fail("daily-offer.json store_connected does not match status.json")
    if bool(daily_offer.get("support_connected")) != bool(status.get("support_connected")):
        fail("daily-offer.json support_connected does not match status.json")
    if bool(daily_offer.get("product_checkout_ready")) != bool(status.get("product_checkout_ready")):
        fail("daily-offer.json product_checkout_ready does not match status.json")
    if not status.get("store_connected") and daily_offer.get("action_type") == "BuyAction":
        fail("daily-offer.json uses BuyAction while store_connected is false")
    if not status.get("store_connected") and daily_offer.get("product_checkout_ready"):
        fail("daily-offer.json claims product checkout is ready while store_connected is false")
    expected_daily_offer_action = "BuyAction" if status.get("store_connected") else "DonateAction"
    if daily_offer.get("action_type") != expected_daily_offer_action:
        fail(f"daily-offer.json action_type is {daily_offer.get('action_type')}, expected {expected_daily_offer_action}")
    if daily_offer.get("promotion_url") != promoted_signal_url:
        fail("daily-offer.json promotion_url does not match promoted support signal URL")
    if not status.get("daily_offer_ready"):
        fail("status.json reports daily_offer_ready=false")
    if status.get("daily_offer_page") != daily_offer_page or status.get("daily_offer_json") != daily_offer_json:
        fail("status.json missing daily offer paths")
    if status.get("daily_offer_page_url") != daily_offer_page_url or status.get("daily_offer_json_url") != daily_offer_json_url:
        fail("status.json missing daily offer URLs")
    if status.get("daily_offer_branded_page_url") != daily_offer_branded_page_url or status.get("daily_offer_branded_json_url") != daily_offer_branded_json_url:
        fail("status.json missing branded daily offer URLs")
    if status.get("daily_offer_action_type") != daily_offer.get("action_type"):
        fail("status.json daily offer action type mismatch")
    require_contains(
        DOCS / daily_offer_json,
        [
            "daily-shelf-daily-offer",
            "support_tiers",
            "checkout_boundary",
            "revenue_boundary",
            "promotion_url",
            "support_intent_url",
            expected_daily_offer_action,
        ],
    )
    require_contains(
        DOCS / daily_offer_page,
        [
            "Daily support offer",
            "Support the strongest current shelf path",
            "Simple voluntary levels",
            "Product checkout is not connected",
            "Revenue is not proven",
            "daily-offer.json",
            expected_daily_offer_action,
            "does not gate downloads",
            "og:image",
            "twitter:card",
        ],
    )
    checkout_readiness = read_json(DOCS / checkout_readiness_json)
    checkout_snapshot = read_json(STATE / "checkout-readiness-snapshot.json")
    if checkout_snapshot.get("kind") != "daily-shelf-checkout-readiness-snapshot":
        fail("checkout-readiness snapshot has wrong kind")
    if int(checkout_snapshot.get("configured_candidate_count") or 0) < 3:
        fail("checkout-readiness snapshot missing configured candidates")
    if int(checkout_snapshot.get("checked_url_count") or 0) < 2:
        fail("checkout-readiness snapshot did not check public candidate URLs")
    if int(checkout_snapshot.get("reachable_url_count") or 0) < 1:
        fail("checkout-readiness snapshot has no reachable public candidate URL")
    if int(checkout_snapshot.get("verified_product_checkout_count") or 0) != 0:
        fail("checkout-readiness snapshot unexpectedly verified product checkout")
    if checkout_snapshot.get("daily_shelf_checkout_reachable"):
        fail("checkout-readiness snapshot claims Daily Shelf checkout is reachable")
    if checkout_readiness.get("kind") != "daily-shelf-checkout-readiness":
        fail("checkout-readiness.json has wrong kind")
    if checkout_readiness.get("page_path") != checkout_readiness_page or checkout_readiness.get("json_path") != checkout_readiness_json:
        fail("checkout-readiness.json missing page/json paths")
    if checkout_readiness.get("page_url") != checkout_readiness_page_url or checkout_readiness.get("json_url") != checkout_readiness_json_url:
        fail("checkout-readiness.json missing public page/json URLs")
    if checkout_readiness.get("branded_page_url") != checkout_readiness_branded_page_url or checkout_readiness.get("branded_json_url") != checkout_readiness_branded_json_url:
        fail("checkout-readiness.json missing branded page/json URLs")
    if bool(checkout_readiness.get("store_connected")) != bool(status.get("store_connected")):
        fail("checkout-readiness.json store_connected does not match status.json")
    if bool(checkout_readiness.get("support_connected")) != bool(status.get("support_connected")):
        fail("checkout-readiness.json support_connected does not match status.json")
    if not status.get("store_connected") and checkout_readiness.get("product_checkout_ready"):
        fail("checkout-readiness.json claims product checkout is ready while store_connected is false")
    if not isinstance(checkout_readiness.get("candidates"), list) or len(checkout_readiness.get("candidates", [])) < 3:
        fail("checkout-readiness.json missing configured checkout candidates")
    candidate_labels = {str(item.get("label") or "") for item in checkout_readiness.get("candidates", []) if isinstance(item, dict)}
    for label in ["CalmSprout Square support", "CalmSprout Square shop", "Archived PayPal hosted-button code"]:
        if label not in candidate_labels:
            fail(f"checkout-readiness.json missing candidate: {label}")
    paypal_candidate = next(
        (item for item in checkout_readiness.get("candidates", []) if item.get("label") == "Archived PayPal hosted-button code"),
        {},
    )
    if paypal_candidate.get("publicly_linkable") or paypal_candidate.get("url"):
        fail("Archived PayPal candidate should not publish a live pay URL")
    if int(checkout_readiness.get("verified_checkout_candidate_count") or 0) != int(status.get("checkout_verified_candidate_count") or 0):
        fail("checkout readiness verified candidate count mismatch")
    if int(checkout_readiness.get("monitor_checked_url_count") or 0) != int(status.get("checkout_monitor_checked_url_count") or 0):
        fail("checkout readiness monitor checked count mismatch")
    if int(checkout_readiness.get("monitor_reachable_url_count") or 0) != int(status.get("checkout_monitor_reachable_url_count") or 0):
        fail("checkout readiness monitor reachable count mismatch")
    if int(checkout_readiness.get("monitor_verified_product_checkout_count") or 0) != 0:
        fail("checkout readiness monitor unexpectedly verified product checkout")
    if checkout_readiness.get("monitor_daily_shelf_checkout_reachable"):
        fail("checkout readiness monitor claims Daily Shelf checkout is reachable")
    if not status.get("checkout_readiness_ready"):
        fail("status.json reports checkout_readiness_ready=false")
    if status.get("checkout_readiness_page") != checkout_readiness_page or status.get("checkout_readiness_json") != checkout_readiness_json:
        fail("status.json missing checkout readiness paths")
    if status.get("checkout_readiness_page_url") != checkout_readiness_page_url or status.get("checkout_readiness_json_url") != checkout_readiness_json_url:
        fail("status.json missing checkout readiness URLs")
    if status.get("checkout_readiness_branded_page_url") != checkout_readiness_branded_page_url or status.get("checkout_readiness_branded_json_url") != checkout_readiness_branded_json_url:
        fail("status.json missing branded checkout readiness URLs")
    if int(status.get("checkout_candidate_count") or 0) < 3:
        fail("status.json checkout_candidate_count is too low")
    require_contains(
        DOCS / checkout_readiness_page,
        [
            "Checkout Readiness",
            "Product checkout not connected",
            "Candidate payment surfaces",
            "CalmSprout Square support",
            "CalmSprout Square shop",
            "Archived PayPal hosted-button code",
            "Public monitor sync",
            "Monitor-verified product checkout URLs",
            "Store checkout remains disconnected",
            checkout_readiness_json,
            "not linked as checkout",
        ],
    )
    revenue_snapshot = read_json(STATE / "revenue-proof-snapshot.json")
    revenue_proof = read_json(DOCS / revenue_proof_json)
    if revenue_snapshot.get("kind") != "daily-shelf-revenue-proof-snapshot":
        fail("revenue-proof snapshot has wrong kind")
    if revenue_snapshot.get("today") != day:
        fail(f"revenue-proof snapshot today is {revenue_snapshot.get('today')}, expected {day}")
    if revenue_proof.get("kind") != "daily-shelf-revenue-proof":
        fail("revenue-proof.json has wrong kind")
    if revenue_proof.get("page_path") != revenue_proof_page or revenue_proof.get("json_path") != revenue_proof_json:
        fail("revenue-proof.json missing page/json paths")
    if revenue_proof.get("page_url") != revenue_proof_page_url or revenue_proof.get("json_url") != revenue_proof_json_url:
        fail("revenue-proof.json missing public page/json URLs")
    if revenue_proof.get("branded_page_url") != revenue_proof_branded_page_url or revenue_proof.get("branded_json_url") != revenue_proof_branded_json_url:
        fail("revenue-proof.json missing branded page/json URLs")
    if int(revenue_proof.get("accepted_receipt_count") or 0) != int(status.get("revenue_proof_accepted_receipt_count") or 0):
        fail("revenue proof accepted receipt count mismatch")
    if int(revenue_proof.get("today_revenue_cents") or 0) != int(status.get("revenue_proof_today_revenue_cents") or 0):
        fail("revenue proof today cents mismatch")
    if bool(revenue_proof.get("actual_daily_revenue_proven")) != bool(status.get("actual_daily_revenue_proven")):
        fail("revenue proof daily proof state mismatch")
    if int(revenue_proof.get("today_revenue_cents") or 0) <= 0 and revenue_proof.get("actual_daily_revenue_proven"):
        fail("revenue-proof.json claims daily revenue without positive today cents")
    if int(revenue_proof.get("accepted_receipt_count") or 0) <= 0 and revenue_proof.get("any_revenue_proven"):
        fail("revenue-proof.json claims revenue without accepted receipts")
    if not status.get("revenue_proof_ready"):
        fail("status.json reports revenue_proof_ready=false")
    if status.get("revenue_proof_page") != revenue_proof_page or status.get("revenue_proof_json") != revenue_proof_json:
        fail("status.json missing revenue proof paths")
    if status.get("revenue_proof_page_url") != revenue_proof_page_url or status.get("revenue_proof_json_url") != revenue_proof_json_url:
        fail("status.json missing revenue proof URLs")
    if status.get("revenue_proof_branded_page_url") != revenue_proof_branded_page_url or status.get("revenue_proof_branded_json_url") != revenue_proof_branded_json_url:
        fail("status.json missing branded revenue proof URLs")
    require_contains(
        DOCS / revenue_proof_page,
        [
            "Revenue Proof",
            "Sanitized receipt ledger",
            "Revenue boundary",
            "Raw exports stay local",
            "Checkout still has its own gate",
            "does not create checkout",
            revenue_proof_json,
        ],
    )
    if not status.get("pay_what_you_can_ready") or status.get("pay_what_you_can_page") != "pay-what-you-can.html":
        fail("status.json missing pay_what_you_can_ready/pay-what-you-can.html")
    if status.get("pay_what_you_can_url") != "https://x26dotapp.github.io/daily-autodigital-shelf/pay-what-you-can.html":
        fail("status.json missing pay_what_you_can_url")
    if int(status.get("support_tier_count") or 0) < 3:
        fail(f"status.json support_tier_count is {status.get('support_tier_count')}, expected at least 3")
    if not status.get("sponsor_surface_ready"):
        fail("status.json reports sponsor_surface_ready=false")
    if status.get("pricing_page") != "pricing.html":
        fail("status.json missing pricing.html")
    if status.get("pricing_page_url") != "https://x26dotapp.github.io/daily-autodigital-shelf/pricing.html":
        fail("status.json missing pricing_page_url")
    if status.get("pricing_branded_url") != "https://www.calmsprout.com/daily-shelf/pricing":
        fail("status.json missing pricing_branded_url")
    if status.get("pricing_support_intent_url") != "https://www.calmsprout.com/daily-shelf/pricing/support/go":
        fail("status.json missing pricing_support_intent_url")
    if status.get("sponsor_page") != "sponsor.html" or status.get("commercial_use_page") != "commercial-use.html":
        fail("status.json missing sponsor/commercial page paths")
    if status.get("sponsor_kit_json") != "sponsor-kit.json":
        fail("status.json missing sponsor-kit JSON path")
    if status.get("sponsor_branded_url") != "https://www.calmsprout.com/daily-shelf/sponsor":
        fail("status.json missing sponsor_branded_url")
    if status.get("commercial_use_branded_url") != "https://www.calmsprout.com/daily-shelf/commercial-use":
        fail("status.json missing commercial_use_branded_url")
    if status.get("sponsor_kit_branded_url") != "https://www.calmsprout.com/daily-shelf/sponsor-kit.json":
        fail("status.json missing sponsor_kit_branded_url")
    if status.get("sponsor_support_intent_url") != "https://www.calmsprout.com/daily-shelf/sponsor/support/go":
        fail("status.json missing sponsor_support_intent_url")
    if status.get("commercial_support_intent_url") != "https://www.calmsprout.com/daily-shelf/commercial-use/support/go":
        fail("status.json missing commercial_support_intent_url")
    if status.get("general_support_intent_url") != "https://www.calmsprout.com/daily-shelf/support/go":
        fail("status.json missing general_support_intent_url")
    if int(status.get("sponsor_tier_count") or 0) < 5:
        fail(f"status.json sponsor_tier_count is {status.get('sponsor_tier_count')}, expected at least 5")
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
    if int(status.get("collection_bundle_page_count") or 0) < 3:
        fail(f"status.json collection_bundle_page_count is {status.get('collection_bundle_page_count')}, expected at least 3")
    if status.get("preferred_collection_bundle_slug") != "small-business-ops":
        fail("status.json missing preferred_collection_bundle_slug")
    if status.get("preferred_collection_bundle_page") != preferred_collection_bundle_page:
        fail("status.json missing preferred_collection_bundle_page")
    if status.get("preferred_collection_bundle_page_url") != preferred_collection_bundle_page_url:
        fail("status.json missing preferred_collection_bundle_page_url")
    if status.get("preferred_collection_bundle_branded_page_url") != "https://www.calmsprout.com/daily-shelf/bundles/small-business-ops-collection.html":
        fail("status.json missing preferred_collection_bundle_branded_page_url")
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
        "guide_page_count": int(status.get("guide_page_count") or 0),
        "policy_page_count": int(status.get("policy_page_count") or 0),
        "sponsor_tier_count": int(status.get("sponsor_tier_count") or 0),
        "collection_bundle_page_count": int(status.get("collection_bundle_page_count") or 0),
        "files_checked": 76,
        "indexnow_enabled": True,
        "monetization_enabled": bool(status.get("monetization_enabled")),
        "store_connected": bool(status.get("store_connected")),
        "support_connected": bool(status.get("support_connected")),
        "support_signal_ready": bool(status.get("support_signal_ready")),
        "support_signal_total_intent_clicks": int(status.get("support_signal_total_intent_clicks") or 0),
        "support_signal_total_download_interest": int(status.get("support_signal_total_download_interest") or 0),
        "daily_offer_ready": bool(status.get("daily_offer_ready")),
        "daily_offer_action_type": str(status.get("daily_offer_action_type") or ""),
        "checkout_readiness_ready": bool(status.get("checkout_readiness_ready")),
        "checkout_candidate_count": int(status.get("checkout_candidate_count") or 0),
        "checkout_verified_candidate_count": int(status.get("checkout_verified_candidate_count") or 0),
        "checkout_monitor_sync_ok": bool(status.get("checkout_monitor_sync_ok")),
        "checkout_monitor_checked_url_count": int(status.get("checkout_monitor_checked_url_count") or 0),
        "checkout_monitor_reachable_url_count": int(status.get("checkout_monitor_reachable_url_count") or 0),
        "checkout_monitor_verified_product_checkout_count": int(status.get("checkout_monitor_verified_product_checkout_count") or 0),
        "revenue_proof_ready": bool(status.get("revenue_proof_ready")),
        "revenue_proof_accepted_receipt_count": int(status.get("revenue_proof_accepted_receipt_count") or 0),
        "revenue_proof_today_revenue_cents": int(status.get("revenue_proof_today_revenue_cents") or 0),
        "actual_daily_revenue_proven": bool(status.get("actual_daily_revenue_proven")),
        "product_checkout_ready": bool(status.get("product_checkout_ready")),
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
