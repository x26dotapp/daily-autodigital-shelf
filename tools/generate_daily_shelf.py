from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
STATE = ROOT / "state"
CONFIG_EXAMPLE = ROOT / "config" / "config.example.json"
CONFIG_LOCAL = ROOT / "config" / "config.local.json"
LEDGER = STATE / "ledger.jsonl"


PACKS: list[dict[str, Any]] = [
    {
        "slug": "calm-launch",
        "title": "Calm Launch One-Page Kit",
        "summary": "A printable page for turning one messy idea into one offer, one audience, and one next action.",
        "buyer": "Creators, solo operators, and small service shops with an idea that keeps staying unfinished.",
        "worksheets": [
            "Name the buyer in one sentence.",
            "Write the smallest useful outcome this offer gives them.",
            "Choose the one intake path that should exist first.",
            "List the proof you already have, without exaggeration.",
        ],
        "checklist": [
            "One offer named",
            "One buyer named",
            "One action path chosen",
            "No fake proof added",
            "Publish-ready paragraph drafted",
        ],
    },
    {
        "slug": "receipt-runner",
        "title": "Receipt Runner Ledger Pack",
        "summary": "A simple ledger and daily receipt habit for tiny projects that need proof of movement.",
        "buyer": "People who lose progress in scattered notes and need a visible record of what changed.",
        "worksheets": [
            "What changed today?",
            "What proof exists?",
            "What is still blocked?",
            "What is the next visible action?",
        ],
        "checklist": [
            "Date recorded",
            "Change written plainly",
            "Proof path saved",
            "Next action is under 20 minutes",
            "No vague progress claims",
        ],
    },
    {
        "slug": "low-energy-week",
        "title": "Low-Energy Week Planner",
        "summary": "A gentle planning sheet for weeks where consistency matters more than intensity.",
        "buyer": "Disabled and neurodivergent workers who need low-friction planning without motivational noise.",
        "worksheets": [
            "Pick the one task that protects the week.",
            "Pick two tasks that can wait without guilt.",
            "Choose a fallback version that still counts.",
            "Write the shutdown rule for today.",
        ],
        "checklist": [
            "One anchor task chosen",
            "Fallback version written",
            "Breaks protected",
            "Shutdown rule visible",
            "No overpacked task list",
        ],
    },
    {
        "slug": "home-inventory",
        "title": "Tiny Home Inventory Pack",
        "summary": "A room-by-room mini inventory for renters, homeowners, resellers, and insurance prep.",
        "buyer": "People who need a simple physical inventory without a full spreadsheet system.",
        "worksheets": [
            "List the five most valuable visible items.",
            "Write where photos are stored.",
            "Mark anything missing a serial number.",
            "Choose one drawer, shelf, or box to finish.",
        ],
        "checklist": [
            "Room named",
            "Photos taken",
            "Serial numbers captured where available",
            "One storage zone finished",
            "Next room chosen",
        ],
    },
    {
        "slug": "micro-budget",
        "title": "Micro Budget Reset",
        "summary": "A one-page reset for seeing near-term bills, small leaks, and the next cash decision.",
        "buyer": "Solo households and freelancers who need a short money picture without a complex finance app.",
        "worksheets": [
            "Write the next three due dates.",
            "List the spending leak that can be paused this week.",
            "Write the smallest income follow-up to do next.",
            "Name the bill or purchase that must not surprise you.",
        ],
        "checklist": [
            "Three due dates visible",
            "One pause candidate picked",
            "One income follow-up named",
            "No investment or trading advice added",
            "Next cash decision written",
        ],
    },
    {
        "slug": "digital-declutter",
        "title": "Digital Declutter Sprint",
        "summary": "A focused cleanup sheet for one folder, inbox, download pile, or project archive.",
        "buyer": "People whose digital mess blocks useful work but who cannot handle a full cleanup marathon.",
        "worksheets": [
            "Pick one folder or inbox view.",
            "Define what counts as keep, archive, delete, or later.",
            "Set a 15-minute stop line.",
            "Write what changed before moving on.",
        ],
        "checklist": [
            "One location chosen",
            "Four decision labels written",
            "Timer limit set",
            "Trash/review pile handled",
            "Receipt note written",
        ],
    },
    {
        "slug": "offer-followup",
        "title": "Honest Follow-Up Draft Kit",
        "summary": "A non-spam template sheet for following up with one real person or lead.",
        "buyer": "Service providers who need a clear follow-up without manipulation, fake urgency, or bulk blasting.",
        "worksheets": [
            "Name the person and the last real context.",
            "Write the useful reason for the message.",
            "Offer one simple next step.",
            "Remove pressure language before sending.",
        ],
        "checklist": [
            "Real prior context confirmed",
            "No fake urgency",
            "One useful reason included",
            "One next step offered",
            "No bulk send configured",
        ],
    },
]


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def json_for_script(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False).replace("</", "<\\/")


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower())
    return cleaned.strip("-") or "pack"


def load_config() -> dict[str, Any]:
    config = json.loads(CONFIG_EXAMPLE.read_text(encoding="utf-8"))
    if CONFIG_LOCAL.exists():
        override = json.loads(CONFIG_LOCAL.read_text(encoding="utf-8"))
        deep_update(config, override)
    return config


def deep_update(base: dict[str, Any], override: dict[str, Any]) -> None:
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            deep_update(base[key], value)
        else:
            base[key] = value


def date_from_args(value: str | None) -> dt.date:
    if value:
        return dt.date.fromisoformat(value)
    return dt.datetime.now().astimezone().date()


def pack_for_day(day: dt.date, config: dict[str, Any]) -> dict[str, Any]:
    seed = config["generation"].get("daily_seed", "daily-autodigital-shelf")
    ordinal = day.toordinal() + sum(ord(char) for char in seed)
    base = dict(PACKS[ordinal % len(PACKS)])
    base["date"] = day.isoformat()
    base["date_label"] = day.strftime("%B %d, %Y")
    base["pack_slug"] = f"{day.isoformat()}-{base['slug']}"
    base["price_hint"] = config["generation"].get("default_price_hint", "$3 to $9 digital pack")
    return base


def pack_url(config: dict[str, Any], path: str) -> str:
    base = config["site"].get("base_url", "").rstrip("/")
    if not base:
        return path
    return f"{base}/{path.lstrip('/')}"


def render_cover_svg(pack: dict[str, Any], out_path: Path) -> None:
    title = esc(pack["title"])
    date_label = esc(pack["date_label"])
    summary = esc(pack["summary"])
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1600" viewBox="0 0 1200 1600" role="img" aria-label="{title}">
  <rect width="1200" height="1600" fill="#f7f8f5"/>
  <path d="M90 110H1110V1490H90Z" fill="#ffffff" stroke="#aeb8b0" stroke-width="3"/>
  <path d="M152 188H1048V398H152Z" fill="#d7f2ee"/>
  <text x="152" y="520" fill="#141716" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="86" font-weight="900">
    <tspan x="152" dy="0">{title}</tspan>
  </text>
  <text x="152" y="640" fill="#0f766e" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="34" font-weight="800">{date_label}</text>
  <foreignObject x="152" y="720" width="880" height="260">
    <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: Inter, Segoe UI, Arial, sans-serif; color: #626b66; font-size: 42px; line-height: 1.42;">{summary}</div>
  </foreignObject>
  <path d="M152 1110H1048" stroke="#d9ded8" stroke-width="3"/>
  <text x="152" y="1215" fill="#d88a1d" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="42" font-weight="900">Daily Autodigital Shelf</text>
  <text x="152" y="1285" fill="#626b66" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="30">Generated automatically. Payment links are explicit and optional.</text>
</svg>
"""
    out_path.write_text(svg, encoding="utf-8")


def render_pack_page(pack: dict[str, Any], config: dict[str, Any], out_path: Path) -> None:
    monetization = config["monetization"]
    store_url = monetization.get("store_url") or ""
    support_url = monetization.get("support_url") or ""
    buy_label = "Store link not connected"
    buy_href = "../../#setup"
    if monetization.get("enabled") and store_url:
        buy_label = "Buy or download from store"
        buy_href = store_url
    elif support_url:
        buy_label = "Support this shelf"
        buy_href = support_url

    pack_path = f"packs/{pack['pack_slug']}/"
    canonical_url = pack_url(config, pack_path)
    structured_data = {
        "@context": "https://schema.org",
        "@type": "CreativeWork",
        "name": pack["title"],
        "description": pack["summary"],
        "datePublished": pack["date"],
        "isPartOf": {
            "@type": "WebSite",
            "name": config["site"]["name"],
            "url": pack_url(config, ""),
        },
        "url": canonical_url,
    }
    worksheet_items = "\n".join(f"<li>{esc(item)}</li>" for item in pack["worksheets"])
    checklist_items = "\n".join(f"<li>{esc(item)}</li>" for item in pack["checklist"])
    content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(pack["title"])} | {esc(config["site"]["name"])}</title>
  <meta name="description" content="{esc(pack["summary"])}">
  <link rel="canonical" href="{esc(canonical_url)}">
  <meta property="og:title" content="{esc(pack["title"])}">
  <meta property="og:description" content="{esc(pack["summary"])}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{esc(canonical_url)}">
  <script type="application/ld+json">{json_for_script(structured_data)}</script>
  <link rel="stylesheet" href="../../styles.css">
</head>
<body>
  <main class="pack-page">
    <nav class="topbar" aria-label="Pack navigation">
      <a class="brand" href="../../">
        <span class="brand-mark">D</span>
        <span class="brand-name">{esc(config["site"]["name"])}</span>
      </a>
      <div class="topnav">
        <a href="./printable.html">Worksheet</a>
        <a href="./checklist.html">Checklist</a>
        <a href="./cover.svg">Cover SVG</a>
      </div>
    </nav>
    <article class="pack-body">
      <p class="pack-date">{esc(pack["date_label"])}</p>
      <h1>{esc(pack["title"])}</h1>
      <p>{esc(pack["summary"])}</p>
      <div class="actions">
        <a class="button primary" href="./printable.html">Open worksheet</a>
        <a class="button" href="./checklist.html">Open checklist</a>
        <a class="button" href="{esc(buy_href)}">{esc(buy_label)}</a>
      </div>
      <h2>Who This Helps</h2>
      <p>{esc(pack["buyer"])}</p>
      <h2>Worksheet Prompts</h2>
      <ol>{worksheet_items}</ol>
      <h2>Pack Checklist</h2>
      <ol>{checklist_items}</ol>
      <p class="fineprint">{esc(monetization.get("affiliate_disclosure", ""))}</p>
    </article>
  </main>
</body>
</html>
"""
    out_path.write_text(content, encoding="utf-8")


def render_printable(pack: dict[str, Any], out_path: Path) -> None:
    boxes = "\n".join(
        f"""<section class="print-box"><strong>{esc(item)}</strong><br><span>Notes:</span></section>"""
        for item in pack["worksheets"]
    )
    content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(pack["title"])} Worksheet</title>
  <link rel="stylesheet" href="../../styles.css">
</head>
<body>
  <main class="print-sheet">
    <p class="pack-date">{esc(pack["date_label"])}</p>
    <h1>{esc(pack["title"])} Worksheet</h1>
    <p>{esc(pack["summary"])}</p>
    <div class="print-grid">
      {boxes}
    </div>
  </main>
</body>
</html>
"""
    out_path.write_text(content, encoding="utf-8")


def render_checklist(pack: dict[str, Any], out_path: Path) -> None:
    items = "\n".join(
        f"""<section class="print-box"><strong>[ ] {esc(item)}</strong><br><span>Proof or note:</span></section>"""
        for item in pack["checklist"]
    )
    content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(pack["title"])} Checklist</title>
  <link rel="stylesheet" href="../../styles.css">
</head>
<body>
  <main class="print-sheet">
    <p class="pack-date">{esc(pack["date_label"])}</p>
    <h1>{esc(pack["title"])} Checklist</h1>
    <div class="print-grid">
      {items}
    </div>
  </main>
</body>
</html>
"""
    out_path.write_text(content, encoding="utf-8")


def render_seller_copy(pack: dict[str, Any], config: dict[str, Any], out_path: Path) -> None:
    tags = [
        "printable planner",
        "digital download",
        slugify(pack["title"]).replace("-", " "),
        "low maintenance",
        "worksheet",
    ]
    worksheet_rows = "\n".join(f"- {item}" for item in pack["worksheets"])
    checklist_rows = "\n".join(f"- {item}" for item in pack["checklist"])
    content = f"""# Store-Ready Listing Copy

## Listing Title

{pack["title"]} - Printable Worksheet and Checklist Pack

## Short Description

{pack["summary"]}

## Long Description

This printable digital pack is built for {pack["buyer"].lower()} It includes a focused worksheet, a completion checklist, and a simple cover asset. Use it as a standalone low-cost digital download, a bonus for a larger bundle, or a lead magnet connected to a real store or support page.

## Includes

- Pack landing page
- Printable worksheet page
- Printable checklist page
- Cover SVG
- Manifest JSON

## Worksheet Prompts

{worksheet_rows}

## Checklist

{checklist_rows}

## Price Hint

{config["generation"].get("default_price_hint", "$3 to $9 digital pack")}

## Tags

{", ".join(tags)}

## Safety Note

This listing copy is generated as a starting point. It does not include a payment link, medical/legal/investment advice, fake testimonials, or guaranteed-income claims.
"""
    out_path.write_text(content, encoding="utf-8")


def read_manifests() -> list[dict[str, Any]]:
    manifests = []
    for path in sorted((DOCS / "packs").glob("*/manifest.json"), reverse=True):
        try:
            manifests.append(json.loads(path.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            continue
    return manifests


def render_index(today_pack: dict[str, Any], config: dict[str, Any]) -> None:
    recent_count = int(config["generation"].get("recent_pack_count", 7))
    manifests = read_manifests()[:recent_count]
    monetization = config["monetization"]
    store_connected = bool(monetization.get("enabled") and monetization.get("store_url"))
    support_connected = bool(monetization.get("support_url"))
    setup_status = "Connected" if store_connected or support_connected else "Not connected"
    setup_class = "done" if store_connected or support_connected else ""
    home_url = pack_url(config, "")
    today_path = f"packs/{today_pack['pack_slug']}/"
    today_url = pack_url(config, today_path)
    structured_data = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": config["site"]["name"],
        "description": config["site"]["tagline"],
        "url": home_url,
        "hasPart": [
            {
                "@type": "CreativeWork",
                "name": today_pack["title"],
                "description": today_pack["summary"],
                "url": today_url,
                "datePublished": today_pack["date"],
            }
        ],
    }

    cards = "\n".join(
        f"""<article class="pack-card">
          <span class="pack-date">{esc(item["date_label"])}</span>
          <h3>{esc(item["title"])}</h3>
          <p>{esc(item["summary"])}</p>
          <a class="button" href="{esc(item["path"])}">Open pack</a>
        </article>"""
        for item in manifests
    )
    if not cards:
        cards = "<p>No packs generated yet.</p>"

    ledger_rows = "\n".join(
        f"""<article class="ledger-row">
          <strong>{esc(item["date_label"])}</strong>
          <p>{esc(item["title"])} generated with worksheet, checklist, cover SVG, manifest, feed entry, and static page.</p>
          <a class="button" href="{esc(item["path"])}">View receipt</a>
        </article>"""
        for item in manifests[:5]
    )

    support_or_store = monetization.get("store_url") or monetization.get("support_url") or "#setup"
    content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(config["site"]["name"])}</title>
  <meta name="description" content="{esc(config["site"]["tagline"])}">
  <link rel="canonical" href="{esc(home_url)}">
  <link rel="alternate" type="application/feed+json" title="{esc(config["site"]["name"])} feed" href="./feed.json">
  <link rel="sitemap" type="application/xml" href="./sitemap.xml">
  <meta property="og:title" content="{esc(config["site"]["name"])}">
  <meta property="og:description" content="{esc(config["site"]["tagline"])}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{esc(home_url)}">
  <script type="application/ld+json">{json_for_script(structured_data)}</script>
  <link rel="stylesheet" href="./styles.css">
</head>
<body>
  <div class="site-shell">
    <header class="topbar">
      <a class="brand" href="./">
        <span class="brand-mark">D</span>
        <span class="brand-name">{esc(config["site"]["name"])}</span>
      </a>
      <nav class="topnav" aria-label="Primary">
        <a href="#today">Today's pack</a>
        <a href="#ledger">Automation ledger</a>
        <a href="#setup">Monetization setup</a>
      </nav>
    </header>

    <main>
      <section class="hero">
        <div class="hero-copy">
          <h1>{esc(config["site"]["tagline"])}</h1>
          <p>This lane creates public, printable digital packs on a schedule. It keeps the money layer explicit, so there are no fake earnings claims and no hidden live-fund behavior.</p>
          <div class="actions">
            <a class="button primary" href="./{esc(today_path)}">Open today's pack</a>
            <a class="button" href="#setup">View setup status</a>
          </div>
          <div class="system-note">
            <div class="signal">Generates one dated pack per run.</div>
            <div class="signal">Publishes static files only.</div>
            <div class="signal">Payment links stay off until connected.</div>
          </div>
        </div>

        <aside class="shelf-panel" id="today">
          <div class="panel-head">
            <div>
              <p class="label">Today's pack</p>
              <h2>{esc(today_pack["title"])}</h2>
            </div>
            <span class="status">Generated</span>
          </div>
          <article class="artifact">
            <div>
              <h3>{esc(today_pack["date_label"])}</h3>
              <p>{esc(today_pack["summary"])}</p>
              <p class="fineprint">Suggested market position: {esc(today_pack["price_hint"])}. Actual checkout requires a connected store or support link.</p>
              <div class="artifact-links">
                <a class="button primary" href="./{esc(today_path)}">Open today's pack</a>
                <a class="button" href="./{esc(today_path)}printable.html">Worksheet</a>
                <a class="button" href="./{esc(today_path)}cover.svg">Cover</a>
              </div>
            </div>
            <div class="mini-cover">{esc(today_pack["title"])}</div>
          </article>
        </aside>
      </section>

      <section>
        <div class="section-head">
          <div>
            <p class="label">Recent shelf</p>
            <h2>Latest generated packs</h2>
          </div>
          <p>Each pack is plain, reusable, and honest enough to be sold, given away, bundled, or used as a lead magnet once the external monetization account exists.</p>
        </div>
        <div class="pack-grid">
          {cards}
        </div>
      </section>

      <section id="ledger">
        <div class="section-head">
          <div>
            <p class="label">Automation ledger</p>
            <h2>Receipts, not promises</h2>
          </div>
          <p>The generator writes dated artifacts and status JSON. It records what was produced instead of claiming revenue.</p>
        </div>
        <div class="ledger">
          {ledger_rows}
        </div>
      </section>

      <section id="setup">
        <div class="section-head">
          <div>
            <p class="label">Monetization setup</p>
            <h2>Status: {esc(setup_status)}</h2>
          </div>
          <p>Money cannot appear without a real buyer, ad network, affiliate approval, store, support link, or payout account. This list keeps that boundary visible.</p>
        </div>
        <div class="setup-list">
          <article class="setup-item done">
            <span class="setup-dot">1</span>
            <div>
              <strong>Daily generator installed</strong>
              <p>Creates a new public pack and updates the static site.</p>
            </div>
          </article>
          <article class="setup-item done">
            <span class="setup-dot">2</span>
            <div>
              <strong>Public site files ready</strong>
              <p>Static output lives in the GitHub Pages `docs/` root.</p>
            </div>
          </article>
          <article class="setup-item {setup_class}">
            <span class="setup-dot">3</span>
            <div>
              <strong>Store, support, or affiliate link</strong>
              <p>Current destination: {esc(support_or_store)}. Edit local config when a real payout path exists.</p>
            </div>
          </article>
          <article class="setup-item">
            <span class="setup-dot">4</span>
            <div>
              <strong>Payment/legal layer</strong>
              <p>External platforms may require identity, tax, payout, approval, and threshold steps. This automation does not bypass those.</p>
            </div>
          </article>
        </div>
      </section>
    </main>

    <footer class="site-footer">
      <p>{esc(monetization.get("affiliate_disclosure", ""))}</p>
    </footer>
  </div>
</body>
</html>
"""
    (DOCS / "index.html").write_text(content, encoding="utf-8")


def render_feed(config: dict[str, Any]) -> None:
    manifests = read_manifests()[:20]
    feed = {
        "title": config["site"]["name"],
        "home_page_url": config["site"].get("base_url", ""),
        "feed_url": pack_url(config, "feed.json"),
        "items": [
            {
                "id": item["id"],
                "url": pack_url(config, item["path"]),
                "title": item["title"],
                "summary": item["summary"],
                "date_published": item["date"],
            }
            for item in manifests
        ],
    }
    (DOCS / "feed.json").write_text(json.dumps(feed, indent=2), encoding="utf-8")


def render_sitemap(config: dict[str, Any]) -> None:
    urls = [pack_url(config, "")]
    urls.extend(pack_url(config, item["path"]) for item in read_manifests()[:80])
    rows = "\n".join(f"  <url><loc>{esc(url)}</loc></url>" for url in urls if url)
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{rows}
</urlset>
"""
    (DOCS / "sitemap.xml").write_text(sitemap, encoding="utf-8")


def render_robots(config: dict[str, Any]) -> None:
    base = pack_url(config, "").rstrip("/")
    sitemap_url = pack_url(config, "sitemap.xml")
    lines = [
        "User-agent: *",
        "Allow: /",
    ]
    if sitemap_url:
        lines.append(f"Sitemap: {sitemap_url}")
    if base:
        lines.append(f"# Site: {base}/")
    (DOCS / "robots.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_ledger(pack: dict[str, Any]) -> None:
    STATE.mkdir(parents=True, exist_ok=True)
    if LEDGER.exists():
        for line in LEDGER.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("date") == pack["date"] and row.get("pack_slug") == pack["pack_slug"]:
                return

    row = {
        "generated_at": dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat(),
        "date": pack["date"],
        "pack_slug": pack["pack_slug"],
        "title": pack["title"],
        "status": "generated",
    }
    with LEDGER.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, sort_keys=True) + "\n")


def write_status(pack: dict[str, Any], config: dict[str, Any]) -> None:
    status_path = DOCS / "status.json"
    generated_at = dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()
    if status_path.exists():
        try:
            existing = json.loads(status_path.read_text(encoding="utf-8"))
            if existing.get("today") == pack["date"] and existing.get("today_pack") == pack["title"]:
                generated_at = existing.get("generated_at") or generated_at
        except json.JSONDecodeError:
            pass

    status = {
        "generated_at": generated_at,
        "today": pack["date"],
        "today_pack": pack["title"],
        "today_path": f"packs/{pack['pack_slug']}/",
        "monetization_enabled": bool(config["monetization"].get("enabled")),
        "store_connected": bool(config["monetization"].get("store_url")),
        "support_connected": bool(config["monetization"].get("support_url")),
        "guardrails": [
            "No live trading",
            "No paid account creation",
            "No outbound spam",
            "No fake revenue claims",
            "No secret values written",
        ],
    }
    status_path.write_text(json.dumps(status, indent=2), encoding="utf-8")


def generate(day: dt.date) -> dict[str, Any]:
    config = load_config()
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "packs").mkdir(parents=True, exist_ok=True)
    pack = pack_for_day(day, config)
    pack_dir = DOCS / "packs" / pack["pack_slug"]
    pack_dir.mkdir(parents=True, exist_ok=True)

    path = f"packs/{pack['pack_slug']}/"
    manifest = {
        "id": f"daily-autodigital-shelf:{pack['pack_slug']}",
        "date": pack["date"],
        "date_label": pack["date_label"],
        "title": pack["title"],
        "summary": pack["summary"],
        "buyer": pack["buyer"],
        "path": path,
        "worksheet": f"{path}printable.html",
        "checklist": f"{path}checklist.html",
        "cover": f"{path}cover.svg",
        "seller_copy": f"{path}seller-copy.md",
    }

    render_cover_svg(pack, pack_dir / "cover.svg")
    render_pack_page(pack, config, pack_dir / "index.html")
    render_printable(pack, pack_dir / "printable.html")
    render_checklist(pack, pack_dir / "checklist.html")
    render_seller_copy(pack, config, pack_dir / "seller-copy.md")
    (pack_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    render_index(pack, config)
    render_feed(config)
    render_sitemap(config)
    render_robots(config)
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    write_status(pack, config)
    append_ledger(pack)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the Daily Autodigital Shelf static site.")
    parser.add_argument("--date", help="Optional ISO date override, for example 2026-06-02.")
    args = parser.parse_args()

    manifest = generate(date_from_args(args.date))
    print(json.dumps({"status": "ok", "pack": manifest}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
