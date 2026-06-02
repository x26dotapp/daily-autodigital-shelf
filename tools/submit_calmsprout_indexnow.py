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
INDEXNOW_STATE = STATE / "calmsprout-indexnow-state.json"

BASE_URL = "https://www.calmsprout.com"
HOST = urllib.parse.urlparse(BASE_URL).netloc
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"
INDEXNOW_KEY = "a4f604db6d2046939ff6c7e3d29d341e"
KEY_LOCATION = f"{BASE_URL}/{INDEXNOW_KEY}.txt"
USER_AGENT = "daily-autodigital-shelf-calmsprout-indexnow/1.0"


DYNAMIC_ROUTE_SOURCES: list[tuple[str, str]] = [
    ("/daily-shelf", "status.json"),
    ("/daily-shelf/today", "status.json"),
    ("/daily-shelf/today.zip", "status.json"),
    ("/daily-shelf/current.zip", "status.json"),
    ("/daily-shelf/products", "catalog.json"),
    ("/daily-shelf/browse", "catalog.json"),
    ("/daily-shelf/product-sitemap.xml", "catalog.json"),
    ("/daily-shelf/support-metrics.json", "status.json"),
    ("/sitemap.xml", "catalog.json"),
    ("/daily-shelf/status", "status.json"),
    ("/daily-shelf/status.json", "status.json"),
    ("/daily-shelf/catalog", "catalog.json"),
    ("/daily-shelf/catalog.json", "catalog.json"),
    ("/daily-shelf/catalog.csv", "catalog.csv"),
    ("/daily-shelf/offers.json", "offers/offers.json"),
    ("/daily-shelf/offers/offers.json", "offers/offers.json"),
    ("/daily-shelf/use-cases.json", "use-cases/use-cases.json"),
    ("/daily-shelf/use-cases/use-cases.json", "use-cases/use-cases.json"),
    ("/daily-shelf/templates.json", "templates/templates.json"),
    ("/daily-shelf/templates/templates.json", "templates/templates.json"),
    ("/daily-shelf/guides.json", "guides/guides.json"),
    ("/daily-shelf/guides/guides.json", "guides/guides.json"),
    ("/daily-shelf/sponsor-kit.json", "sponsor-kit.json"),
    ("/daily-shelf/product-feed.json", "product-feed.json"),
    ("/daily-shelf/product-feed.xml", "product-feed.xml"),
    ("/daily-shelf/product-feed.csv", "product-feed.csv"),
    ("/daily-shelf/support-funnel.json", "support-funnel.json"),
    ("/daily-shelf/support-funnel.xml", "support-funnel.xml"),
    ("/daily-shelf/support-funnel.csv", "support-funnel.csv"),
    ("/daily-shelf/store-listings.json", "imports/store-listings.json"),
    ("/daily-shelf/store-listings.csv", "imports/store-listings.csv"),
    ("/daily-shelf/imports/store-listings.json", "imports/store-listings.json"),
    ("/daily-shelf/imports/store-listings.csv", "imports/store-listings.csv"),
    ("/daily-shelf/feed.json", "feed.json"),
    ("/daily-shelf/feed.xml", "feed.xml"),
    ("/daily-shelf/atom.xml", "atom.xml"),
    ("/daily-shelf/starter.zip", "bundles/starter-archive.zip"),
    ("/daily-shelf/bundles/starter-archive.zip", "bundles/starter-archive.zip"),
    ("/daily-shelf/assets/support-card.svg", "assets/support-card.svg"),
]

STATIC_ROUTE_SOURCES: list[tuple[str, str]] = [
    ("/daily-shelf/offers", "offers/index.html"),
    ("/daily-shelf/use-cases/", "use-cases/index.html"),
    ("/daily-shelf/templates/", "templates/index.html"),
    ("/daily-shelf/guides/", "guides/index.html"),
    ("/daily-shelf/pricing", "pricing.html"),
    ("/daily-shelf/pricing.html", "pricing.html"),
    ("/daily-shelf/pricing/support/go", "pricing.html"),
    ("/daily-shelf/commercial-use", "commercial-use.html"),
    ("/daily-shelf/commercial-use.html", "commercial-use.html"),
    ("/daily-shelf/commercial-use/support/go", "commercial-use.html"),
    ("/daily-shelf/sponsor", "sponsor.html"),
    ("/daily-shelf/sponsor.html", "sponsor.html"),
    ("/daily-shelf/sponsor/support/go", "sponsor.html"),
    ("/daily-shelf/starter-bundle.html", "starter-bundle.html"),
    ("/daily-shelf/support.html", "support.html"),
    ("/daily-shelf/license.html", "license.html"),
    ("/daily-shelf/privacy.html", "privacy.html"),
    ("/daily-shelf/terms.html", "terms.html"),
    ("/daily-shelf/pay", "pay-what-you-can.html"),
    ("/daily-shelf/pay-what-you-can", "pay-what-you-can.html"),
    ("/daily-shelf/bundle", "bundles/starter-archive.zip"),
    ("/daily-shelf/support", "support.html"),
    ("/daily-shelf/support/go", "support.html"),
    ("/llms.txt", "llms.txt"),
    ("/llms-full.txt", "llms-full.txt"),
    ("/daily-shelf/llms.txt", "llms.txt"),
    ("/daily-shelf/sitemap.xml", "sitemap.xml"),
    ("/sitemap.xml", "sitemap.xml"),
]


def fail(message: str) -> None:
    raise RuntimeError(message)


def read_json(path: Path, fallback: dict[str, Any] | None = None) -> dict[str, Any]:
    if not path.exists():
        if fallback is not None:
            return fallback
        fail(f"Missing JSON file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def route_url(path: str) -> str:
    return f"{BASE_URL}/{path.lstrip('/')}"


def clean_pack_slug(value: str) -> str:
    slug = str(value or "").strip().lower()
    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789-")
    first_allowed = set("abcdefghijklmnopqrstuvwxyz0123456789")
    if len(slug) < 4 or slug[0] not in first_allowed or not all(char in allowed for char in slug):
        return ""
    return slug


def pack_slug_from_item(item: dict[str, Any]) -> str:
    candidates: list[str] = []
    item_id = str(item.get("id") or "")
    if ":" in item_id:
        candidates.append(item_id.rsplit(":", 1)[-1])
    for key in ("url", "download_url", "download_page_url"):
        try:
            parsed = urllib.parse.urlparse(str(item.get(key) or ""))
        except ValueError:
            continue
        parts = [urllib.parse.unquote(part) for part in parsed.path.split("/") if part]
        if "packs" in parts:
            index = parts.index("packs")
            if index + 1 < len(parts):
                candidates.append(parts[index + 1])
        if "downloads" in parts:
            index = parts.index("downloads")
            if index + 1 < len(parts):
                candidates.append(parts[index + 1].removesuffix(".zip"))
    for candidate in candidates:
        slug = clean_pack_slug(candidate)
        if slug:
            return slug
    return ""


def catalog_product_routes() -> list[tuple[str, str]]:
    catalog = read_json(DOCS / "catalog.json")
    routes: list[tuple[str, str]] = []
    for item in catalog.get("items", []):
        if isinstance(item, dict):
            slug = pack_slug_from_item(item)
            if slug:
                routes.append((f"/daily-shelf/packs/{slug}/", f"packs/{slug}/index.html"))
                routes.append((f"/daily-shelf/downloads/{slug}.zip", f"downloads/{slug}.zip"))
                routes.append((f"/daily-shelf/downloads/{slug}.html", f"downloads/{slug}.html"))
                routes.append((f"/daily-shelf/products/{slug}", "catalog.json"))
                routes.append((f"/daily-shelf/products/{slug}/support", "catalog.json"))
    return routes


def offer_routes() -> list[tuple[str, str]]:
    offers = read_json(DOCS / "offers" / "offers.json", fallback={"offers": []})
    routes: list[tuple[str, str]] = []
    for offer in offers.get("offers", []):
        if isinstance(offer, dict):
            slug = clean_pack_slug(str(offer.get("slug") or ""))
            if slug:
                routes.append((f"/daily-shelf/offers/{slug}", "offers/offers.json"))
                routes.append((f"/daily-shelf/offers/{slug}.html", "offers/offers.json"))
                routes.append((f"/daily-shelf/offers/{slug}/support/go", "offers/offers.json"))
            bundle_path = str(offer.get("collection_bundle_path") or "").strip("/")
            bundle_name = Path(bundle_path).name
            if bundle_path.startswith("bundles/") and bundle_name.endswith(".zip"):
                routes.append((f"/daily-shelf/bundles/{bundle_name}", bundle_path))
            bundle_page_path = str(offer.get("collection_bundle_page_path") or "").strip("/")
            bundle_page_name = Path(bundle_page_path).name
            if bundle_page_path.startswith("bundles/") and bundle_page_name.endswith(".html"):
                routes.append((f"/daily-shelf/bundles/{bundle_page_name}", bundle_page_path))
    return routes


def use_case_routes() -> list[tuple[str, str]]:
    use_cases = read_json(DOCS / "use-cases" / "use-cases.json", fallback={"items": []})
    routes: list[tuple[str, str]] = []
    for use_case in use_cases.get("items", []):
        if isinstance(use_case, dict):
            slug = clean_pack_slug(str(use_case.get("slug") or ""))
            path = str(use_case.get("path") or "").strip("/")
            if slug and path.startswith("use-cases/") and path.endswith(".html"):
                routes.append((f"/daily-shelf/use-cases/{slug}.html", path))
    return routes


def template_routes() -> list[tuple[str, str]]:
    templates = read_json(DOCS / "templates" / "templates.json", fallback={"items": []})
    routes: list[tuple[str, str]] = []
    for template in templates.get("items", []):
        if isinstance(template, dict):
            slug = clean_pack_slug(str(template.get("slug") or ""))
            path = str(template.get("path") or "").strip("/")
            if slug and path.startswith("templates/") and path.endswith(".html"):
                routes.append((f"/daily-shelf/templates/{slug}.html", path))
                routes.append((f"/daily-shelf/templates/{slug}/support", "templates/templates.json"))
                routes.append((f"/daily-shelf/templates/{slug}/support/go", "templates/templates.json"))
    return routes


def guide_routes() -> list[tuple[str, str]]:
    guides = read_json(DOCS / "guides" / "guides.json", fallback={"items": []})
    routes: list[tuple[str, str]] = []
    for guide in guides.get("items", []):
        if isinstance(guide, dict):
            slug = clean_pack_slug(str(guide.get("slug") or ""))
            path = str(guide.get("path") or "").strip("/")
            if slug and path.startswith("guides/") and path.endswith(".html"):
                routes.append((f"/daily-shelf/guides/{slug}.html", path))
    return routes


def file_signature(path: Path) -> str:
    if not path.exists():
        return "missing"
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def add_candidate(candidates: list[dict[str, str]], route_path: str, source_rel_path: str) -> None:
    source_path = DOCS / source_rel_path
    candidates.append(
        {
            "url": route_url(route_path),
            "path": str(source_path),
            "signature": file_signature(source_path),
        }
    )


def collect_candidates(include_static: bool) -> list[dict[str, str]]:
    # Validate core output before we compute signatures. This keeps a broken
    # generation run from updating the branded submit state.
    status = read_json(DOCS / "status.json")
    if not status.get("indexnow_enabled"):
        fail("Daily Shelf IndexNow output is not enabled")

    candidates: list[dict[str, str]] = []
    for route_path, source_rel_path in DYNAMIC_ROUTE_SOURCES:
        add_candidate(candidates, route_path, source_rel_path)
    for route_path, source_rel_path in catalog_product_routes():
        add_candidate(candidates, route_path, source_rel_path)
    for route_path, source_rel_path in offer_routes():
        add_candidate(candidates, route_path, source_rel_path)
    for route_path, source_rel_path in use_case_routes():
        add_candidate(candidates, route_path, source_rel_path)
    for route_path, source_rel_path in template_routes():
        add_candidate(candidates, route_path, source_rel_path)
    for route_path, source_rel_path in guide_routes():
        add_candidate(candidates, route_path, source_rel_path)
    if include_static:
        for route_path, source_rel_path in STATIC_ROUTE_SOURCES:
            add_candidate(candidates, route_path, source_rel_path)

    deduped: list[dict[str, str]] = []
    seen: set[str] = set()
    for candidate in candidates:
        if candidate["url"] not in seen:
            deduped.append(candidate)
            seen.add(candidate["url"])
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


def wait_for_key(seconds: int) -> dict[str, Any]:
    deadline = time.monotonic() + max(0, seconds)
    last_error = ""
    while True:
        try:
            request = urllib.request.Request(KEY_LOCATION, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=15) as response:
                body = response.read().decode("utf-8", errors="replace").strip()
                if response.status == 200 and body == INDEXNOW_KEY:
                    return {"status_code": response.status, "key_location": KEY_LOCATION}
                last_error = f"status={response.status} body={body[:80]!r}"
        except OSError as exc:
            last_error = str(exc)

        if time.monotonic() >= deadline:
            fail(f"IndexNow key file not verified at {KEY_LOCATION}: {last_error}")
        time.sleep(5)


def submit_indexnow(urls: list[str]) -> dict[str, Any]:
    payload = {
        "host": HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }
    request = urllib.request.Request(
        INDEXNOW_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": USER_AGENT},
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
    parser = argparse.ArgumentParser(description="Submit changed CalmSprout Daily Shelf URLs to IndexNow.")
    parser.add_argument("--all", action="store_true", help="Include static bridge/discovery routes in addition to proxied data routes.")
    parser.add_argument("--force", action="store_true", help="Submit selected URLs even if local signatures did not change.")
    parser.add_argument("--dry-run", action="store_true", help="Print intended submission without calling IndexNow.")
    parser.add_argument("--max-urls", type=int, default=100, help="Maximum URLs to submit in one request.")
    parser.add_argument("--wait-for-key-seconds", type=int, default=0, help="Wait for the public CalmSprout IndexNow key file.")
    args = parser.parse_args()

    candidates = collect_candidates(args.all)
    state = load_state()
    selected = changed_candidates(candidates, state, args.force)[: args.max_urls]
    urls = [candidate["url"] for candidate in selected]

    result: dict[str, Any] = {
        "status": "ok",
        "dry_run": args.dry_run,
        "endpoint": INDEXNOW_ENDPOINT,
        "host": HOST,
        "key_location": KEY_LOCATION,
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

    key_check = wait_for_key(args.wait_for_key_seconds)
    submission = submit_indexnow(urls)
    submitted_at = dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()
    state.setdefault("submitted", {})
    for candidate in selected:
        state["submitted"][candidate["url"]] = {
            "signature": candidate["signature"],
            "submitted_at": submitted_at,
        }
    state["last_submission"] = {
        "submitted_at": submitted_at,
        "endpoint": INDEXNOW_ENDPOINT,
        "host": HOST,
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
