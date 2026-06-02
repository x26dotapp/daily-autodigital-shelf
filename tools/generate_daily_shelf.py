from __future__ import annotations

import argparse
import csv
import datetime as dt
import html
import json
import re
import zipfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BUNDLES = DOCS / "bundles"
DOWNLOADS = DOCS / "downloads"
IMPORTS = DOCS / "imports"
TOPICS = DOCS / "topics"
STATE = ROOT / "state"
CONFIG_EXAMPLE = ROOT / "config" / "config.example.json"
CONFIG_PUBLIC = ROOT / "config" / "config.public.json"
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
    {
        "slug": "subscription-audit",
        "title": "Subscription Audit Sheet",
        "summary": "A quick worksheet for finding recurring charges, renewal dates, and pause candidates.",
        "buyer": "Households and freelancers who need a clearer view of subscriptions without a finance app.",
        "worksheets": [
            "List every recurring charge you can find.",
            "Mark the ones you used in the last 30 days.",
            "Write the renewal date or billing day for each.",
            "Choose one pause, cancel, or keep decision.",
        ],
        "checklist": [
            "Recurring charges listed",
            "Usage marked",
            "Renewal dates captured",
            "One decision made",
            "No investment advice added",
        ],
    },
    {
        "slug": "simple-content-calendar",
        "title": "Simple Content Calendar",
        "summary": "A low-pressure one-week content planner for small brands, creators, and solo operators.",
        "buyer": "People who need a content plan that does not become a second full-time job.",
        "worksheets": [
            "Pick one message worth repeating this week.",
            "Write three post ideas from that message.",
            "Choose the easiest publishing day.",
            "Name one asset you can reuse instead of creating from scratch.",
        ],
        "checklist": [
            "One weekly message chosen",
            "Three post ideas written",
            "Publishing day picked",
            "Reusable asset named",
            "No fake audience metrics added",
        ],
    },
    {
        "slug": "invoice-followup",
        "title": "Invoice Follow-Up Mini Kit",
        "summary": "A calm worksheet for tracking unpaid invoices and writing one clear follow-up.",
        "buyer": "Freelancers and service providers who need a polite payment follow-up without pressure tricks.",
        "worksheets": [
            "Write the invoice number, date, and amount.",
            "Record the last real contact about it.",
            "Write one factual follow-up sentence.",
            "Choose the next check-in date.",
        ],
        "checklist": [
            "Invoice details captured",
            "Last contact recorded",
            "Follow-up is factual",
            "No threats or fake urgency",
            "Next check-in date chosen",
        ],
    },
    {
        "slug": "download-folder-reset",
        "title": "Downloads Folder Reset",
        "summary": "A 20-minute digital cleanup worksheet for turning a downloads pile into decisions.",
        "buyer": "People whose downloads folder has become a source of friction and lost files.",
        "worksheets": [
            "Sort the first 20 files into keep, archive, delete, or review.",
            "Create one named destination folder.",
            "Write what should never be saved here again.",
            "Schedule the next short reset.",
        ],
        "checklist": [
            "First 20 files handled",
            "Destination folder made",
            "Delete pile cleared",
            "Review pile named",
            "Next reset scheduled",
        ],
    },
    {
        "slug": "appointment-prep",
        "title": "Appointment Prep Card",
        "summary": "A one-page prep card for collecting questions, documents, and follow-up notes before an appointment.",
        "buyer": "People who forget key questions or documents when appointments get stressful.",
        "worksheets": [
            "Write the appointment time, place, and contact.",
            "List the top three questions.",
            "Name the documents or photos to bring.",
            "Write the follow-up action before leaving.",
        ],
        "checklist": [
            "Time and place written",
            "Questions listed",
            "Documents gathered",
            "Follow-up action captured",
            "No medical/legal advice added",
        ],
    },
    {
        "slug": "client-intake-lite",
        "title": "Client Intake Lite",
        "summary": "A small intake sheet for turning a vague request into scope, timeline, budget, and next action.",
        "buyer": "Service providers who need a repeatable first-call intake without a heavy CRM.",
        "worksheets": [
            "Write the requested outcome in the client's words.",
            "Name what is in scope and out of scope.",
            "Capture the deadline and budget signal.",
            "Choose the next action and owner.",
        ],
        "checklist": [
            "Outcome captured",
            "Scope boundaries written",
            "Deadline noted",
            "Budget signal noted",
            "Next owner chosen",
        ],
    },
    {
        "slug": "listing-photo-checklist",
        "title": "Listing Photo Checklist",
        "summary": "A practical shot list for creating clearer marketplace, rental, or product listing photos.",
        "buyer": "People preparing simple listings who need better photos without hiring a photographer.",
        "worksheets": [
            "List the item, room, or product being photographed.",
            "Take one wide shot, one detail shot, and one scale shot.",
            "Write what defect or limitation must be shown honestly.",
            "Choose the best cover image.",
        ],
        "checklist": [
            "Wide shot taken",
            "Detail shot taken",
            "Scale shot taken",
            "Limitations shown honestly",
            "Cover image chosen",
        ],
    },
    {
        "slug": "one-page-sop",
        "title": "One-Page SOP Builder",
        "summary": "A worksheet for documenting one repeatable task so someone else can follow it.",
        "buyer": "Small teams and solo operators who need process notes without a full operations manual.",
        "worksheets": [
            "Name the task and when it starts.",
            "List the tools and files needed.",
            "Write the steps in order.",
            "Describe the done state and common mistake.",
        ],
        "checklist": [
            "Task named",
            "Inputs listed",
            "Steps ordered",
            "Done state defined",
            "Common mistake noted",
        ],
    },
    {
        "slug": "weekly-reset",
        "title": "Weekly Reset Board",
        "summary": "A printable reset board for tasks, bills, errands, and loose ends that need one weekly review.",
        "buyer": "Busy households and solo workers who need one visible weekly reset page.",
        "worksheets": [
            "Write the three things that must not surprise you this week.",
            "List bills, errands, messages, and cleanup tasks.",
            "Choose one task to delegate, defer, or delete.",
            "Write the week-end shutdown rule.",
        ],
        "checklist": [
            "Surprises named",
            "Loose ends listed",
            "One task reduced",
            "Shutdown rule written",
            "No overpacked week",
        ],
    },
    {
        "slug": "micro-offer-pricing",
        "title": "Micro Offer Pricing Sheet",
        "summary": "A simple worksheet for pricing a small digital or service offer without pretending the market is guaranteed.",
        "buyer": "Creators and service providers turning a small repeatable outcome into an offer.",
        "worksheets": [
            "Write the exact outcome the buyer receives.",
            "List three comparable offers or substitutes.",
            "Choose a starter price and a revision rule.",
            "Write what is included and not included.",
        ],
        "checklist": [
            "Outcome written",
            "Substitutes listed",
            "Starter price chosen",
            "Revision rule written",
            "No guaranteed-income claim",
        ],
    },
    {
        "slug": "tiny-launch-checklist",
        "title": "Tiny Launch Checklist",
        "summary": "A compact launch checklist for publishing a small page, pack, or offer without waiting for perfect.",
        "buyer": "People with useful work stuck in draft mode who need a small publish path.",
        "worksheets": [
            "Name the thing being launched.",
            "Write the one sentence description.",
            "Check the link, price/status, and contact path.",
            "Write what to improve after launch.",
        ],
        "checklist": [
            "Title set",
            "Description written",
            "Primary link tested",
            "Status honest",
            "Next improvement noted",
        ],
    },
    {
        "slug": "decision-parking-lot",
        "title": "Decision Parking Lot",
        "summary": "A worksheet for parking unresolved decisions so they stop interrupting the current task.",
        "buyer": "People who get pulled away by unresolved choices and need a simple holding place.",
        "worksheets": [
            "Write the decision that keeps interrupting you.",
            "Name what information is missing.",
            "Set a review date.",
            "Write the current task you are returning to.",
        ],
        "checklist": [
            "Decision captured",
            "Missing info named",
            "Review date set",
            "Current task named",
            "Decision not solved prematurely",
        ],
    },
    {
        "slug": "email-triage",
        "title": "Email Triage Sprint",
        "summary": "A 15-minute inbox worksheet for finding the few messages that actually need action.",
        "buyer": "People who avoid inboxes because every message feels equally urgent.",
        "worksheets": [
            "Search for invoices, appointments, deadlines, and direct requests.",
            "Pick five messages that need action.",
            "Choose reply, schedule, archive, or defer for each.",
            "Write the one reply you can send first.",
        ],
        "checklist": [
            "Important searches run",
            "Five messages selected",
            "Action label chosen",
            "First reply drafted",
            "Bulk send avoided",
        ],
    },
    {
        "slug": "project-rescue-map",
        "title": "Project Rescue Map",
        "summary": "A one-page map for rescuing a messy project by separating assets, blockers, risks, and next moves.",
        "buyer": "Builders and operators who need to recover a project without starting over.",
        "worksheets": [
            "List what already exists and where it lives.",
            "Name the blocker that stops useful progress.",
            "Write the smallest rescue step.",
            "Choose what not to touch today.",
        ],
        "checklist": [
            "Existing assets listed",
            "Blocker named",
            "Rescue step chosen",
            "Non-targets protected",
            "Progress receipt written",
        ],
    },
    {
        "slug": "daily-proof-log",
        "title": "Daily Proof Log",
        "summary": "A receipt-style log for recording visible proof of work without overexplaining the whole day.",
        "buyer": "Solo workers who need evidence of progress for themselves, clients, or future handoff.",
        "worksheets": [
            "Write the visible thing that changed.",
            "Record the path, URL, screenshot, or file.",
            "Write what still needs review.",
            "Choose tomorrow's first proof target.",
        ],
        "checklist": [
            "Change named",
            "Proof path recorded",
            "Review need written",
            "Tomorrow target chosen",
            "No vague progress claim",
        ],
    },
    {
        "slug": "simple-order-form",
        "title": "Simple Order Form Draft",
        "summary": "A draft sheet for designing a small order or request form before building it online.",
        "buyer": "Small sellers and service providers who need a clear order form before platform setup.",
        "worksheets": [
            "Write what the buyer is requesting.",
            "List the required fields only.",
            "Name optional details that can wait.",
            "Write the confirmation message.",
        ],
        "checklist": [
            "Offer/request named",
            "Required fields listed",
            "Optional fields separated",
            "Confirmation message written",
            "No payment info collected here",
        ],
    },
    {
        "slug": "two-hour-workblock",
        "title": "Two-Hour Workblock Planner",
        "summary": "A compact planning sheet for choosing one outcome, one timer, and one shutdown note.",
        "buyer": "People who need a bounded work session that does not expand into the whole day.",
        "worksheets": [
            "Write the single outcome for this block.",
            "List the files or tools needed before starting.",
            "Set the stop time.",
            "Write the shutdown note when done.",
        ],
        "checklist": [
            "One outcome chosen",
            "Inputs ready",
            "Stop time set",
            "Shutdown note written",
            "No second project added",
        ],
    },
    {
        "slug": "store-import-prep",
        "title": "Store Import Prep Sheet",
        "summary": "A worksheet for gathering product title, description, price hint, tags, and delivery files before using a store platform.",
        "buyer": "Digital sellers preparing listings for Payhip, Gumroad, Etsy-style shops, or similar platforms.",
        "worksheets": [
            "Write the product title and short description.",
            "List the downloadable files.",
            "Choose tags and a starter price.",
            "Write the refund/support note for the listing.",
        ],
        "checklist": [
            "Title and description ready",
            "Files listed",
            "Tags chosen",
            "Price hint chosen",
            "Support note written",
        ],
    },
    {
        "slug": "focus-menu",
        "title": "Focus Menu Builder",
        "summary": "A menu of low, medium, and high energy task options for days when planning from scratch is too expensive.",
        "buyer": "People who need usable work choices that adapt to uneven energy.",
        "worksheets": [
            "List three low-energy tasks that still count.",
            "List three medium-energy tasks.",
            "List one high-energy task for better days.",
            "Choose today's menu item.",
        ],
        "checklist": [
            "Low-energy options written",
            "Medium options written",
            "High option written",
            "Today's item chosen",
            "Fallback still counts",
        ],
    },
    {
        "slug": "link-in-bio-audit",
        "title": "Link-in-Bio Audit",
        "summary": "A simple audit sheet for checking whether a public profile points visitors to one useful action.",
        "buyer": "Creators and small sellers whose public links do not clearly route visitors.",
        "worksheets": [
            "Write the current top link and what it asks visitors to do.",
            "Remove or park links that distract from the main action.",
            "Write a clearer button label.",
            "Choose the next public proof link.",
        ],
        "checklist": [
            "Top action identified",
            "Distracting links parked",
            "Button label improved",
            "Proof link chosen",
            "No fake metrics added",
        ],
    },
    {
        "slug": "renewal-reminder",
        "title": "Renewal Reminder Sheet",
        "summary": "A small tracker for domain, software, insurance, lease, and service renewal dates.",
        "buyer": "People who need renewal dates visible before they become urgent surprises.",
        "worksheets": [
            "List the renewal name and date.",
            "Write the cost if known.",
            "Choose keep, compare, cancel, or review.",
            "Set a reminder date before renewal.",
        ],
        "checklist": [
            "Renewal named",
            "Date recorded",
            "Cost noted if known",
            "Decision label chosen",
            "Reminder date set",
        ],
    },
    {
        "slug": "landing-page-copy",
        "title": "Landing Page Copy Blocks",
        "summary": "A fill-in worksheet for headline, promise, proof, offer, and next action copy.",
        "buyer": "Small operators who need usable page copy before a designer or builder gets involved.",
        "worksheets": [
            "Write the buyer and problem in plain words.",
            "Write the useful outcome without hype.",
            "List real proof or leave it blank.",
            "Write the next action button text.",
        ],
        "checklist": [
            "Buyer named",
            "Outcome written",
            "Proof honest",
            "Button text chosen",
            "No fake testimonial added",
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
    if CONFIG_PUBLIC.exists():
        public_override = json.loads(CONFIG_PUBLIC.read_text(encoding="utf-8"))
        deep_update(config, public_override)
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


def social_meta(title: str, description: str, url: str, image_url: str, image_alt: str, og_type: str = "website") -> str:
    return "\n".join(
        [
            f'  <meta property="og:title" content="{esc(title)}">',
            f'  <meta property="og:description" content="{esc(description)}">',
            f'  <meta property="og:type" content="{esc(og_type)}">',
            f'  <meta property="og:url" content="{esc(url)}">',
            f'  <meta property="og:image" content="{esc(image_url)}">',
            f'  <meta property="og:image:alt" content="{esc(image_alt)}">',
            '  <meta name="twitter:card" content="summary_large_image">',
            f'  <meta name="twitter:title" content="{esc(title)}">',
            f'  <meta name="twitter:description" content="{esc(description)}">',
            f'  <meta name="twitter:image" content="{esc(image_url)}">',
        ]
    )


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
    cover_url = pack_url(config, f"{pack_path}cover.svg")
    download_url = pack_url(config, f"downloads/{pack['pack_slug']}.zip")
    structured_data = {
        "@context": "https://schema.org",
        "@type": "CreativeWork",
        "name": pack["title"],
        "description": pack["summary"],
        "datePublished": pack["date"],
        "image": cover_url,
        "keywords": "printable worksheet, digital download, planner, checklist",
        "audience": {
            "@type": "Audience",
            "audienceType": pack["buyer"],
        },
        "encoding": {
            "@type": "MediaObject",
            "contentUrl": download_url,
            "encodingFormat": "application/zip",
            "name": f"{pack['title']} download ZIP",
        },
        "isPartOf": {
            "@type": "WebSite",
            "name": config["site"]["name"],
            "url": pack_url(config, ""),
        },
        "url": canonical_url,
    }
    worksheet_items = "\n".join(f"<li>{esc(item)}</li>" for item in pack["worksheets"])
    checklist_items = "\n".join(f"<li>{esc(item)}</li>" for item in pack["checklist"])
    topic_links = " ".join(
        f"""<a class="topic-link" href="../../topics/{esc(slug)}.html">{esc(TOPIC_DEFINITIONS[slug]["label"])}</a>"""
        for slug in topic_slugs_for_item(pack)
    )
    content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(pack["title"])} | {esc(config["site"]["name"])}</title>
  <meta name="description" content="{esc(pack["summary"])}">
  <link rel="canonical" href="{esc(canonical_url)}">
{social_meta(pack["title"], pack["summary"], canonical_url, cover_url, f"{pack['title']} cover", "article")}
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
        <a href="../../support.html">Support</a>
      </div>
    </nav>
    <article class="pack-body">
      <p class="pack-date">{esc(pack["date_label"])}</p>
      <h1>{esc(pack["title"])}</h1>
      <p>{esc(pack["summary"])}</p>
      <div class="actions">
        <a class="button primary" href="./printable.html">Open worksheet</a>
        <a class="button" href="./checklist.html">Open checklist</a>
        <a class="button" href="../../downloads/{esc(pack["pack_slug"])}.zip">Download pack ZIP</a>
        <a class="button" href="{esc(buy_href)}">{esc(buy_label)}</a>
      </div>
      <h2>Who This Helps</h2>
      <p>{esc(pack["buyer"])}</p>
      <h2>Related Topics</h2>
      <p class="topic-links">{topic_links}</p>
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


def bundle_file_paths(manifests: list[dict[str, Any]]) -> list[Path]:
    rel_paths = [
        "archive.html",
        "support.html",
        "store-import.html",
        "license.html",
        "privacy.html",
        "refund-policy.html",
        "terms.html",
        "llms.txt",
        "llms-full.txt",
        "topics/index.html",
        "topics/topics.json",
        "catalog.csv",
        "catalog.json",
        "imports/store-listings.csv",
        "imports/store-listings.json",
        "imports/store-upload-kit.zip",
        "feed.json",
        "feed.xml",
        "atom.xml",
    ]
    for item in manifests:
        pack_path = str(item["path"]).rstrip("/")
        rel_paths.extend(
            [
                f"{pack_path}/index.html",
                f"{pack_path}/printable.html",
                f"{pack_path}/checklist.html",
                f"{pack_path}/cover.svg",
                f"{pack_path}/manifest.json",
                f"{pack_path}/seller-copy.md",
            ]
        )

    files: list[Path] = []
    seen: set[str] = set()
    for rel_path in rel_paths:
        path = DOCS / rel_path
        key = path.resolve().as_posix()
        if path.exists() and key not in seen:
            files.append(path)
            seen.add(key)
    return files


def write_zip_entry(bundle: zipfile.ZipFile, arcname: str, data: bytes) -> None:
    info = zipfile.ZipInfo(arcname)
    info.create_system = 3
    info.date_time = (2026, 1, 1, 0, 0, 0)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    bundle.writestr(info, data)


ZIP_TEXT_SUFFIXES = {
    ".css",
    ".csv",
    ".html",
    ".json",
    ".md",
    ".svg",
    ".txt",
    ".xml",
}


def read_zip_source_bytes(source: Path) -> bytes:
    data = source.read_bytes()
    if source.suffix.lower() in ZIP_TEXT_SUFFIXES:
        return data.replace(b"\r\n", b"\n")
    return data


def pack_slug_from_manifest(item: dict[str, Any]) -> str:
    return str(item["path"]).strip("/").split("/")[-1]


def pack_download_path(item: dict[str, Any]) -> str:
    return str(item.get("download") or f"downloads/{pack_slug_from_manifest(item)}.zip")


TOPIC_DEFINITIONS: dict[str, dict[str, Any]] = {
    "small-business-ops": {
        "label": "Small Business Ops",
        "description": "Digital worksheets for client intake, invoices, SOPs, listings, follow-up, and simple operating routines.",
        "keywords": [
            "client",
            "invoice",
            "sop",
            "store",
            "listing",
            "offer",
            "follow-up",
            "landing",
            "content",
            "business",
            "service",
        ],
    },
    "home-admin": {
        "label": "Home Admin",
        "description": "Printable tools for household paperwork, appointments, renewals, subscriptions, budgets, receipts, and inventories.",
        "keywords": [
            "home",
            "appointment",
            "renewal",
            "subscription",
            "budget",
            "receipt",
            "inventory",
            "folder",
            "downloads",
            "bill",
        ],
    },
    "low-energy-systems": {
        "label": "Low-Energy Systems",
        "description": "Gentle planning packs for uneven energy, neurodivergent workflows, shutdown notes, and low-friction task choices.",
        "keywords": [
            "low-energy",
            "energy",
            "focus",
            "calm",
            "gentle",
            "shutdown",
            "neurodivergent",
            "bounded",
            "planner",
        ],
    },
    "digital-product-prep": {
        "label": "Digital Product Prep",
        "description": "Sheets for preparing small digital products, listing copy, import details, content calendars, and public launch assets.",
        "keywords": [
            "digital",
            "product",
            "store",
            "import",
            "marketplace",
            "listing",
            "landing",
            "content",
            "link-in-bio",
            "launch",
        ],
    },
    "cleanup-and-reset": {
        "label": "Cleanup And Reset",
        "description": "Short reset worksheets for files, folders, digital clutter, weekly planning, receipts, and stalled projects.",
        "keywords": [
            "reset",
            "declutter",
            "downloads",
            "folder",
            "cleanup",
            "receipt",
            "weekly",
            "rescue",
            "triage",
        ],
    },
}


def item_search_text(item: dict[str, Any]) -> str:
    parts = [
        str(item.get("title", "")),
        str(item.get("summary", "")),
        str(item.get("description", "")),
        str(item.get("buyer", "")),
        str(item.get("slug", "")),
        str(item.get("path", "")),
        str(item.get("id", "")),
    ]
    return " ".join(parts).lower()


def topic_slugs_for_item(item: dict[str, Any]) -> list[str]:
    text = item_search_text(item)
    matches = [
        slug
        for slug, topic in TOPIC_DEFINITIONS.items()
        if any(keyword in text for keyword in topic["keywords"])
    ]
    if not matches:
        matches.append("cleanup-and-reset")
    return matches


def topic_records_for_item(item: dict[str, Any], config: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "slug": slug,
            "label": TOPIC_DEFINITIONS[slug]["label"],
            "url": pack_url(config, f"topics/{slug}.html"),
        }
        for slug in topic_slugs_for_item(item)
    ]


def render_pack_downloads() -> dict[str, Any]:
    manifests = read_manifests()
    DOWNLOADS.mkdir(parents=True, exist_ok=True)
    outputs = []

    for item in manifests:
        slug = pack_slug_from_manifest(item)
        zip_rel_path = pack_download_path(item)
        if item.get("download") != zip_rel_path:
            item["download"] = zip_rel_path
            manifest_path = DOCS / item["path"] / "manifest.json"
            manifest_path.write_text(json.dumps(item, indent=2), encoding="utf-8")
        zip_path = DOCS / zip_rel_path
        zip_root = f"daily-autodigital-shelf-{slug}"
        readme = "\n".join(
            [
                item["title"],
                "",
                f"Date: {item['date']}",
                f"Summary: {item['summary']}",
                f"Buyer: {item.get('buyer', '')}",
                "",
                "Included files: pack page, printable worksheet, checklist, cover SVG, manifest JSON, and seller-copy markdown.",
                "This ZIP is generated for digital-product upload workflows. It contains no payment credentials or guaranteed-income claims.",
            ]
        )
        with zipfile.ZipFile(zip_path, "w") as bundle:
            write_zip_entry(bundle, f"{zip_root}/README.txt", readme.encode("utf-8"))
            for rel_path in [
                item["path"] + "index.html",
                item["worksheet"],
                item["checklist"],
                item["cover"],
                item["path"] + "manifest.json",
                item.get("seller_copy", ""),
            ]:
                if not rel_path:
                    continue
                source = DOCS / rel_path
                if source.exists():
                    write_zip_entry(bundle, f"{zip_root}/{source.relative_to(DOCS).as_posix()}", read_zip_source_bytes(source))

        outputs.append(
            {
                "id": item["id"],
                "title": item["title"],
                "path": zip_rel_path,
                "bytes": zip_path.stat().st_size,
            }
        )

    return {
        "count": len(outputs),
        "bytes": sum(item["bytes"] for item in outputs),
        "downloads": outputs,
    }


def listing_keywords(item: dict[str, Any]) -> str:
    title_words = slugify(str(item["title"])).replace("-", ",")
    base = [
        "digital download",
        "printable worksheet",
        "planner",
        "checklist",
        "low maintenance",
    ]
    return ",".join(dict.fromkeys([*base, *[word for word in title_words.split(",") if word]]))


def marketplace_rows(config: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for item in read_manifests():
        rows.append(
            {
                "sku": item["id"].replace("daily-autodigital-shelf:", "das-"),
                "title": item["title"],
                "subtitle": item["summary"],
                "buyer": item.get("buyer", ""),
                "price_hint": config["generation"].get("default_price_hint", "$3 to $9 digital pack"),
                "currency": "USD",
                "download_url": pack_url(config, pack_download_path(item)),
                "preview_url": pack_url(config, item["path"]),
                "worksheet_url": pack_url(config, item["worksheet"]),
                "checklist_url": pack_url(config, item["checklist"]),
                "cover_url": pack_url(config, item["cover"]),
                "seller_copy_url": pack_url(config, item.get("seller_copy", "")),
                "topic_labels": "|".join(record["label"] for record in topic_records_for_item(item, config)),
                "topic_urls": "|".join(record["url"] for record in topic_records_for_item(item, config)),
                "tags": listing_keywords(item),
                "fulfillment": "digital download",
                "status": "ready for external store import; checkout not connected",
            }
        )
    return rows


POLICY_DEFINITIONS: dict[str, dict[str, Any]] = {
    "license": {
        "path": "license.html",
        "title": "Digital Product License",
        "label": "License",
        "description": "Plain license terms for Daily Autodigital Shelf generated printable packs.",
        "sections": [
            (
                "Personal And Internal Use",
                "A buyer may use downloaded packs for personal planning, household organization, or internal business operations.",
            ),
            (
                "No Resale Of The Files",
                "A buyer may not resell, redistribute, upload, or claim ownership of the original generated files, ZIP archives, templates, or listing copy.",
            ),
            (
                "Printable Workflow Use",
                "A buyer may print copies for their own household, team, client call, or internal workflow as long as the files themselves are not resold or republished.",
            ),
            (
                "No Professional Advice",
                "The packs are general organizational tools. They are not medical, legal, financial, tax, investment, or mental-health advice.",
            ),
        ],
    },
    "terms": {
        "path": "terms.html",
        "title": "Terms Of Use",
        "label": "Terms",
        "description": "Operating terms for the Daily Autodigital Shelf public site and generated files.",
        "sections": [
            (
                "Static Site",
                "This site publishes generated digital pack previews, listing metadata, and downloadable ZIP files. It does not operate checkout or collect payment directly.",
            ),
            (
                "External Platforms",
                "When a legitimate store, support, ad, affiliate, or marketplace destination is connected, that external platform will control its own checkout, tax, refund, and account rules.",
            ),
            (
                "No Income Claims",
                "The site does not claim guaranteed revenue, automated profit, buyer demand, or marketplace approval.",
            ),
            (
                "Acceptable Use",
                "Do not use these materials for spam, fraud, deceptive income claims, or regulated professional advice.",
            ),
        ],
    },
    "privacy": {
        "path": "privacy.html",
        "title": "Privacy Notice",
        "label": "Privacy",
        "description": "Privacy notice for the static Daily Autodigital Shelf site.",
        "sections": [
            (
                "No Native Accounts",
                "This static site does not create user accounts, run a checkout form, or ask visitors for payment credentials.",
            ),
            (
                "No Local Visitor Database",
                "The generator does not write a visitor database, mailing list, customer table, or lead file.",
            ),
            (
                "Hosting And External Services",
                "GitHub Pages and any future external store, support, ad, affiliate, or analytics provider may process requests under their own policies.",
            ),
            (
                "Future Changes",
                "If checkout, contact forms, analytics, or support links are connected later, this notice should be updated before collecting personal data.",
            ),
        ],
    },
    "refund": {
        "path": "refund-policy.html",
        "title": "Digital Download Refund Note",
        "label": "Refund",
        "description": "Refund and delivery note for future Daily Autodigital Shelf digital downloads.",
        "sections": [
            (
                "Checkout Not Connected",
                "No direct checkout is currently active on this site, so this site does not process refunds directly.",
            ),
            (
                "Future Store Rules",
                "If these files are sold through an external marketplace or support platform, that platform's refund, dispute, tax, and payout rules will apply.",
            ),
            (
                "Digital Delivery",
                "Generated packs are digital downloads. Buyers should review the public preview and listing text before purchase when a store is connected.",
            ),
            (
                "Broken Files",
                "If a future paid download is broken or incomplete, the intended remedy is access to a working copy through the external platform where the purchase happened.",
            ),
        ],
    },
}


def policy_records(config: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "slug": slug,
            "label": policy["label"],
            "title": policy["title"],
            "path": policy["path"],
            "url": pack_url(config, policy["path"]),
        }
        for slug, policy in POLICY_DEFINITIONS.items()
    ]


def policy_links(config: dict[str, Any], prefix: str = "./") -> str:
    return " ".join(
        f"""<a href="{esc(prefix + record["path"])}">{esc(record["label"])}</a>"""
        for record in policy_records(config)
    )


def render_policy_pages(config: dict[str, Any]) -> dict[str, Any]:
    manifests = read_manifests()
    image_url = pack_url(config, manifests[0]["cover"]) if manifests else pack_url(config, "")
    records = policy_records(config)
    all_links = policy_links(config)
    for slug, policy in POLICY_DEFINITIONS.items():
        page_url = pack_url(config, policy["path"])
        sections = "\n".join(
            f"""<article class="setup-item">
            <span class="setup-dot">{index}</span>
            <div>
              <strong>{esc(title)}</strong>
              <p>{esc(body)}</p>
            </div>
          </article>"""
            for index, (title, body) in enumerate(policy["sections"], start=1)
        )
        structured_data = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": policy["title"],
            "description": policy["description"],
            "url": page_url,
            "isPartOf": {
                "@type": "WebSite",
                "name": config["site"]["name"],
                "url": pack_url(config, ""),
            },
        }
        html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(policy["title"])} | {esc(config["site"]["name"])}</title>
  <meta name="description" content="{esc(policy["description"])}">
  <link rel="canonical" href="{esc(page_url)}">
{social_meta(policy["title"], policy["description"], page_url, image_url, f"{policy['title']} page")}
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
      <nav class="topnav" aria-label="Policy navigation">
        <a href="./">Home</a>
        <a href="./archive.html">Archive</a>
        <a href="./store-import.html">Import kit</a>
      </nav>
    </header>
    <main>
      <section>
        <div class="section-head">
          <div>
            <p class="label">Policy</p>
            <h2>{esc(policy["title"])}</h2>
          </div>
          <p>{esc(policy["description"])}</p>
        </div>
        <div class="setup-list">
          {sections}
        </div>
      </section>
      <section>
        <div class="section-head">
          <div>
            <p class="label">Store readiness</p>
            <h2>Policy set</h2>
          </div>
          <p>These pages support future store setup. They do not activate checkout, collect payment, or create a payout account.</p>
        </div>
        <p class="policy-links">{all_links}</p>
      </section>
    </main>
  </div>
</body>
</html>
"""
        (DOCS / policy["path"]).write_text(html, encoding="utf-8")

    return {
        "count": len(records),
        "paths": [record["path"] for record in records],
        "urls": [record["url"] for record in records],
    }


def render_store_import_kit(config: dict[str, Any]) -> dict[str, Any]:
    IMPORTS.mkdir(parents=True, exist_ok=True)
    rows = marketplace_rows(config)
    csv_rel_path = "imports/store-listings.csv"
    json_rel_path = "imports/store-listings.json"
    zip_rel_path = "imports/store-upload-kit.zip"
    page_rel_path = "store-import.html"
    fieldnames = [
        "sku",
        "title",
        "subtitle",
        "buyer",
        "price_hint",
        "currency",
        "download_url",
        "preview_url",
        "worksheet_url",
        "checklist_url",
        "cover_url",
        "seller_copy_url",
        "topic_labels",
        "topic_urls",
        "tags",
        "fulfillment",
        "status",
    ]
    with (DOCS / csv_rel_path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (DOCS / json_rel_path).write_text(json.dumps({"items": rows}, indent=2), encoding="utf-8")

    zip_root = "daily-autodigital-shelf-store-upload-kit"
    readme = "\n".join(
        [
            "Daily Autodigital Shelf Store Upload Kit",
            "",
            f"Listing count: {len(rows)}",
            "",
            "This kit contains generic marketplace listing metadata, seller-copy files, and generated product ZIPs.",
            "It also includes policy pages for license, terms, privacy, and refund/delivery notes.",
            "It is intended for a legitimate external store, support platform, or marketplace after payout setup exists.",
            "",
            "No checkout, payout account, tax profile, or payment processor is configured inside this archive.",
        ]
    )
    with zipfile.ZipFile(DOCS / zip_rel_path, "w") as bundle:
        write_zip_entry(bundle, f"{zip_root}/README.txt", readme.encode("utf-8"))
        policy_paths = [record["path"] for record in policy_records(config)]
        for rel_path in [csv_rel_path, json_rel_path, "catalog.csv", "catalog.json", *policy_paths]:
            source = DOCS / rel_path
            if source.exists():
                write_zip_entry(bundle, f"{zip_root}/{rel_path}", read_zip_source_bytes(source))
        for item in read_manifests():
            for rel_path in [item.get("seller_copy", ""), pack_download_path(item), item["cover"]]:
                if not rel_path:
                    continue
                source = DOCS / rel_path
                if source.exists():
                    write_zip_entry(bundle, f"{zip_root}/{source.relative_to(DOCS).as_posix()}", read_zip_source_bytes(source))

    cards = "\n".join(
        f"""<article class="ledger-row">
          <strong>{esc(row["sku"])}</strong>
          <p><a href="{esc(row["preview_url"])}">{esc(row["title"])}</a><br>{esc(row["subtitle"])}</p>
          <div class="row-actions">
            <a class="button" href="{esc(row["download_url"])}">Product ZIP</a>
            <a class="button" href="{esc(row["seller_copy_url"])}">Listing copy</a>
          </div>
        </article>"""
        for row in rows
    )
    if not cards:
        cards = "<p>No listings generated yet.</p>"

    zip_bytes = (DOCS / zip_rel_path).stat().st_size
    zip_kb = max(1, round(zip_bytes / 1024))
    page_url = pack_url(config, page_rel_path)
    image_url = rows[0]["cover_url"] if rows else pack_url(config, "")
    structured_data = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Daily Autodigital Shelf Store Import Kit",
        "description": "Generated marketplace listing metadata for digital download products.",
        "url": page_url,
        "numberOfItems": len(rows),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index + 1,
                "name": row["title"],
                "url": row["preview_url"],
            }
            for index, row in enumerate(rows[:50])
        ],
    }
    content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Store Import Kit | {esc(config["site"]["name"])}</title>
  <meta name="description" content="Generic marketplace import kit for Daily Autodigital Shelf generated digital products.">
  <link rel="canonical" href="{esc(page_url)}">
{social_meta("Store Import Kit", "Generated marketplace listing metadata for Daily Autodigital Shelf digital products.", page_url, image_url, "Daily Autodigital Shelf store import kit")}
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
      <nav class="topnav" aria-label="Import kit navigation">
        <a href="./">Home</a>
        <a href="./archive.html">Archive</a>
        <a href="./topics/">Topics</a>
        <a href="./support.html">Support</a>
        <a href="./terms.html">Policies</a>
        <a href="./starter-bundle.html">Starter bundle</a>
      </nav>
    </header>
    <main>
      <section>
        <div class="section-head">
          <div>
            <p class="label">Store import kit</p>
            <h2>Listings ready for a real marketplace</h2>
          </div>
          <p>This page packages titles, descriptions, tags, suggested pricing, listing copy, preview links, product ZIP URLs, and store policy pages. It does not connect checkout or claim revenue.</p>
        </div>
        <div class="bundle-panel">
          <div>
            <p class="label">Import files</p>
            <h3>{len(rows)} product listings prepared</h3>
            <p>Use the CSV, JSON, or ZIP when a legitimate payout-enabled store exists. Each row points at a direct product ZIP, public preview page, topic_labels, and topic_urls, and the ZIP includes license, terms, privacy, and refund notes.</p>
            <div class="actions">
              <a class="button primary" href="./{esc(zip_rel_path)}">Download import kit</a>
              <a class="button" href="./{esc(csv_rel_path)}">Listing CSV</a>
              <a class="button" href="./{esc(json_rel_path)}">Listing JSON</a>
              <a class="button" href="./terms.html">Policy pages</a>
            </div>
          </div>
          <div class="bundle-stat">
            <span>{len(rows)}</span>
            <strong>listings</strong>
            <small>{zip_kb} KB ZIP</small>
          </div>
        </div>
      </section>
      <section>
        <div class="section-head">
          <div>
            <p class="label">Prepared listings</p>
            <h2>Marketplace queue</h2>
          </div>
          <p>These are generated listing records. They are not active paid listings until an external store account and payout path are connected.</p>
        </div>
        <div class="ledger">
          {cards}
        </div>
      </section>
    </main>
  </div>
</body>
</html>
"""
    (DOCS / page_rel_path).write_text(content, encoding="utf-8")
    return {
        "count": len(rows),
        "csv_path": csv_rel_path,
        "json_path": json_rel_path,
        "zip_path": zip_rel_path,
        "page_path": page_rel_path,
        "zip_bytes": zip_bytes,
    }


def topic_index(manifests: list[dict[str, Any]], config: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    topics: dict[str, list[dict[str, Any]]] = {slug: [] for slug in TOPIC_DEFINITIONS}
    for item in manifests:
        for slug in topic_slugs_for_item(item):
            topics.setdefault(slug, []).append(item)
    return {slug: items for slug, items in topics.items() if items}


def render_topic_pages(config: dict[str, Any]) -> dict[str, Any]:
    TOPICS.mkdir(parents=True, exist_ok=True)
    manifests = read_manifests()
    topics = topic_index(manifests, config)
    topic_export = {
        "topics": [
            {
                "slug": slug,
                "label": TOPIC_DEFINITIONS[slug]["label"],
                "description": TOPIC_DEFINITIONS[slug]["description"],
                "url": pack_url(config, f"topics/{slug}.html"),
                "count": len(items),
                "items": [
                    {
                        "id": item["id"],
                        "title": item["title"],
                        "summary": item["summary"],
                        "url": pack_url(config, item["path"]),
                        "download_url": pack_url(config, pack_download_path(item)),
                    }
                    for item in items
                ],
            }
            for slug, items in topics.items()
        ]
    }
    (TOPICS / "topics.json").write_text(json.dumps(topic_export, indent=2), encoding="utf-8")

    index_cards = "\n".join(
        f"""<article class="pack-card">
          <span class="pack-date">{len(items)} packs</span>
          <h3>{esc(TOPIC_DEFINITIONS[slug]["label"])}</h3>
          <p>{esc(TOPIC_DEFINITIONS[slug]["description"])}</p>
          <a class="button" href="./{esc(slug)}.html">Open topic</a>
        </article>"""
        for slug, items in topics.items()
    )
    if not index_cards:
        index_cards = "<p>No topics generated yet.</p>"

    first_cover = pack_url(config, manifests[0]["cover"]) if manifests else pack_url(config, "")
    index_url = pack_url(config, "topics/")
    index_data = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Daily Autodigital Shelf Topics",
        "description": "Topic groups for generated printable digital packs.",
        "url": index_url,
        "hasPart": [
            {
                "@type": "CollectionPage",
                "name": TOPIC_DEFINITIONS[slug]["label"],
                "url": pack_url(config, f"topics/{slug}.html"),
            }
            for slug in topics
        ],
    }
    index_html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Topics | {esc(config["site"]["name"])}</title>
  <meta name="description" content="Topic groups for Daily Autodigital Shelf generated digital packs.">
  <link rel="canonical" href="{esc(index_url)}">
{social_meta("Daily Autodigital Shelf Topics", "Topic groups for generated printable digital packs.", index_url, first_cover, "Daily Autodigital Shelf topics")}
  <script type="application/ld+json">{json_for_script(index_data)}</script>
  <link rel="stylesheet" href="../styles.css">
</head>
<body>
  <div class="site-shell">
    <header class="topbar">
      <a class="brand" href="../">
        <span class="brand-mark">D</span>
        <span class="brand-name">{esc(config["site"]["name"])}</span>
      </a>
      <nav class="topnav" aria-label="Topics navigation">
        <a href="../">Home</a>
        <a href="../archive.html">Archive</a>
        <a href="../store-import.html">Import kit</a>
      </nav>
    </header>
    <main>
      <section>
        <div class="section-head">
          <div>
            <p class="label">Topics</p>
            <h2>Browse generated packs by use case</h2>
          </div>
          <p>These topic pages group generated packs into searchable collections without claiming checkout or revenue.</p>
        </div>
        <div class="pack-grid">
          {index_cards}
        </div>
      </section>
    </main>
  </div>
</body>
</html>
"""
    (TOPICS / "index.html").write_text(index_html, encoding="utf-8")

    for slug, items in topics.items():
        topic = TOPIC_DEFINITIONS[slug]
        page_url = pack_url(config, f"topics/{slug}.html")
        image_url = pack_url(config, items[0]["cover"])
        rows = "\n".join(
            f"""<article class="ledger-row">
          <strong>{esc(item["date_label"])}</strong>
          <p><a href="../{esc(item["path"])}">{esc(item["title"])}</a><br>{esc(item["summary"])}</p>
          <div class="row-actions">
            <a class="button" href="../{esc(pack_download_path(item))}">Product ZIP</a>
            <a class="button" href="../{esc(item.get("seller_copy", item["path"]))}">Listing copy</a>
          </div>
        </article>"""
            for item in items
        )
        page_data = {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": topic["label"],
            "description": topic["description"],
            "url": page_url,
            "hasPart": [
                {
                    "@type": "CreativeWork",
                    "name": item["title"],
                    "description": item["summary"],
                    "url": pack_url(config, item["path"]),
                    "image": pack_url(config, item["cover"]),
                }
                for item in items[:50]
            ],
        }
        html_content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(topic["label"])} | {esc(config["site"]["name"])}</title>
  <meta name="description" content="{esc(topic["description"])}">
  <link rel="canonical" href="{esc(page_url)}">
{social_meta(topic["label"], topic["description"], page_url, image_url, f"{topic['label']} topic")}
  <script type="application/ld+json">{json_for_script(page_data)}</script>
  <link rel="stylesheet" href="../styles.css">
</head>
<body>
  <div class="site-shell">
    <header class="topbar">
      <a class="brand" href="../">
        <span class="brand-mark">D</span>
        <span class="brand-name">{esc(config["site"]["name"])}</span>
      </a>
      <nav class="topnav" aria-label="Topic navigation">
        <a href="../">Home</a>
        <a href="./">Topics</a>
        <a href="../archive.html">Archive</a>
      </nav>
    </header>
    <main>
      <section>
        <div class="section-head">
          <div>
            <p class="label">Topic</p>
            <h2>{esc(topic["label"])}</h2>
          </div>
          <p>{esc(topic["description"])}</p>
        </div>
        <div class="ledger">
          {rows}
        </div>
      </section>
    </main>
  </div>
</body>
</html>
"""
        (TOPICS / f"{slug}.html").write_text(html_content, encoding="utf-8")

    return {
        "count": len(topics),
        "items": sum(len(items) for items in topics.values()),
        "index_path": "topics/index.html",
        "json_path": "topics/topics.json",
    }


def render_bundle(config: dict[str, Any]) -> dict[str, Any]:
    manifests = read_manifests()
    BUNDLES.mkdir(parents=True, exist_ok=True)

    bundle_rel_path = "bundles/starter-archive.zip"
    bundle_path = DOCS / bundle_rel_path
    page_rel_path = "starter-bundle.html"
    latest_date = manifests[0]["date"] if manifests else ""
    oldest_date = manifests[-1]["date"] if manifests else ""
    zip_root = "daily-autodigital-shelf-starter"
    bundle_manifest = {
        "id": "daily-autodigital-shelf:starter-archive",
        "title": "Daily Autodigital Shelf Starter Archive",
        "pack_count": len(manifests),
        "oldest_date": oldest_date,
        "latest_date": latest_date,
        "zip_path": bundle_rel_path,
        "page_path": page_rel_path,
        "items": [
            {
                "id": item["id"],
                "date": item["date"],
                "title": item["title"],
                "path": item["path"],
                "worksheet": item["worksheet"],
                "checklist": item["checklist"],
                "cover": item["cover"],
                "seller_copy": item.get("seller_copy", ""),
                "download": pack_download_path(item),
            }
            for item in manifests
        ],
    }
    readme = "\n".join(
        [
            "Daily Autodigital Shelf Starter Archive",
            "",
            f"Pack count: {len(manifests)}",
            f"Date range: {oldest_date} to {latest_date}",
            "",
            "This bundle contains generated printable worksheets, checklists, cover SVGs, manifests, and seller-copy files.",
            "It is designed to be uploaded to a store or support platform as one digital-download product.",
            "",
            "Guardrails: no guaranteed-income claims, no payment credentials, no medical/legal/investment advice, and no hidden live-fund behavior.",
            "",
            "Suggested listing position: starter printable archive for low-maintenance planning and operations worksheets.",
        ]
    )

    with zipfile.ZipFile(bundle_path, "w") as bundle:
        write_zip_entry(bundle, f"{zip_root}/README.txt", readme.encode("utf-8"))
        write_zip_entry(
            bundle,
            f"{zip_root}/STARTER-BUNDLE-MANIFEST.json",
            json.dumps(bundle_manifest, indent=2).encode("utf-8"),
        )
        for source in bundle_file_paths(manifests):
            rel = source.relative_to(DOCS).as_posix()
            write_zip_entry(bundle, f"{zip_root}/{rel}", read_zip_source_bytes(source))

    bundle_bytes = bundle_path.stat().st_size
    bundle_kb = max(1, round(bundle_bytes / 1024))
    rows = "\n".join(
        f"""<article class="ledger-row">
          <strong>{esc(item["date_label"])}</strong>
          <p><a href="./{esc(item["path"])}">{esc(item["title"])}</a><br>{esc(item["summary"])}</p>
          <div class="row-actions">
            <a class="button" href="./{esc(item.get("seller_copy", item["path"]))}">Listing copy</a>
            <a class="button" href="./{esc(pack_download_path(item))}">Pack ZIP</a>
          </div>
        </article>"""
        for item in manifests
    )
    if not rows:
        rows = "<p>No packs generated yet.</p>"

    page_url = pack_url(config, page_rel_path)
    image_url = pack_url(config, manifests[0]["cover"]) if manifests else pack_url(config, "")
    structured_data = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Daily Autodigital Shelf Starter Archive",
        "description": "Generated starter archive of printable worksheet digital packs.",
        "url": page_url,
        "numberOfItems": len(manifests),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index + 1,
                "name": item["title"],
                "url": pack_url(config, item["path"]),
            }
            for index, item in enumerate(manifests[:50])
        ],
    }
    content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Starter Bundle | {esc(config["site"]["name"])}</title>
  <meta name="description" content="Downloadable starter archive for Daily Autodigital Shelf generated packs.">
  <link rel="canonical" href="{esc(page_url)}">
{social_meta("Daily Autodigital Shelf Starter Archive", "Downloadable starter archive of generated printable digital packs.", page_url, image_url, "Daily Autodigital Shelf starter archive")}
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
      <nav class="topnav" aria-label="Bundle navigation">
        <a href="./">Home</a>
        <a href="./archive.html">Archive</a>
        <a href="./topics/">Topics</a>
        <a href="./support.html">Support</a>
        <a href="./terms.html">Policies</a>
        <a href="./catalog.csv">Catalog CSV</a>
      </nav>
    </header>
    <main>
      <section>
        <div class="section-head">
          <div>
            <p class="label">Starter bundle</p>
            <h2>One ZIP for the generated shelf</h2>
          </div>
          <p>The ZIP is generated by the same daily automation as the public pages, so it can be used as a single upload for a store, support platform, or manual product import.</p>
        </div>
        <div class="bundle-panel">
          <div>
            <p class="label">Bundle contents</p>
            <h3>Daily Autodigital Shelf Starter Archive</h3>
            <p>{len(manifests)} generated packs from {esc(oldest_date)} through {esc(latest_date)}, including printable worksheets, checklists, cover SVGs, manifests, catalog files, and seller-copy files.</p>
            <div class="actions">
              <a class="button primary" href="./{esc(bundle_rel_path)}">Download ZIP</a>
              <a class="button" href="./catalog.csv">Open catalog CSV</a>
            </div>
          </div>
          <div class="bundle-stat">
            <span>{len(manifests)}</span>
            <strong>packs</strong>
            <small>{bundle_kb} KB ZIP</small>
          </div>
        </div>
      </section>
      <section>
        <div class="section-head">
          <div>
            <p class="label">Included packs</p>
            <h2>Bundle inventory</h2>
          </div>
          <p>These entries mirror the public archive and are included in the downloadable ZIP.</p>
        </div>
        <div class="ledger">
          {rows}
        </div>
      </section>
    </main>
  </div>
</body>
</html>
"""
    (DOCS / page_rel_path).write_text(content, encoding="utf-8")

    return {
        **bundle_manifest,
        "zip_url": pack_url(config, bundle_rel_path),
        "page_url": pack_url(config, page_rel_path),
        "bytes": bundle_bytes,
    }


def render_index(today_pack: dict[str, Any], config: dict[str, Any], bundle: dict[str, Any]) -> None:
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
    today_cover_url = pack_url(config, f"{today_path}cover.svg")
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
                "image": today_cover_url,
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
    if store_connected:
        recent_monetization_note = "Each pack is plain, reusable, and ready for the connected external store path."
        bundle_monetization_note = "The starter archive is packaged for the connected external checkout path."
        destination_label = "Store destination"
        destination_detail = f"Current store destination: {support_or_store}."
        destination_cta_label = "Open store"
    elif support_connected:
        recent_monetization_note = "Each pack is plain, reusable, and public while the connected support path can receive voluntary support."
        bundle_monetization_note = "The starter archive is packaged and ready; product checkout is still separate from the connected support path."
        destination_label = "Support destination"
        destination_detail = f"Current support destination: {support_or_store}. This is not product checkout."
        destination_cta_label = "Support this shelf"
    else:
        recent_monetization_note = "Each pack is plain, reusable, and honest enough to be sold, given away, bundled, or used as a lead magnet once the external monetization account exists."
        bundle_monetization_note = "The daily generator also creates one ZIP containing the starter archive. This is the simplest file to upload when a real checkout, support, or affiliate path is connected."
        destination_label = "Store, support, or affiliate link"
        destination_detail = f"Current destination: {support_or_store}. Edit local config when a real payout path exists."
        destination_cta_label = ""
    destination_cta = (
        f"""<a class="button" href="{esc(support_or_store)}">{esc(destination_cta_label)}</a>"""
        if destination_cta_label
        else ""
    )
    policy_nav_links = policy_links(config)
    bundle_zip_path = str(bundle.get("zip_path", "bundles/starter-archive.zip"))
    bundle_page_path = str(bundle.get("page_path", "starter-bundle.html"))
    bundle_pack_count = int(bundle.get("pack_count", 0))
    bundle_bytes = int(bundle.get("bytes", 0))
    bundle_kb = max(1, round(bundle_bytes / 1024)) if bundle_bytes else 0
    content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(config["site"]["name"])}</title>
  <meta name="description" content="{esc(config["site"]["tagline"])}">
  <link rel="canonical" href="{esc(home_url)}">
  <link rel="alternate" type="application/feed+json" title="{esc(config["site"]["name"])} feed" href="./feed.json">
  <link rel="alternate" type="application/rss+xml" title="{esc(config["site"]["name"])} RSS" href="./feed.xml">
  <link rel="alternate" type="application/atom+xml" title="{esc(config["site"]["name"])} Atom" href="./atom.xml">
  <link rel="alternate" type="text/plain" title="{esc(config["site"]["name"])} AI summary" href="./llms.txt">
  <link rel="sitemap" type="application/xml" href="./sitemap.xml">
{social_meta(config["site"]["name"], config["site"]["tagline"], home_url, today_cover_url, f"{today_pack['title']} cover")}
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
        <a href="./archive.html">Archive</a>
        <a href="./topics/">Topics</a>
        <a href="./{esc(bundle_page_path)}">Starter bundle</a>
        <a href="./support.html">Support</a>
        <a href="./store-import.html">Import kit</a>
        <a href="./terms.html">Policies</a>
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
            <a class="button" href="./{esc(bundle_page_path)}">Open starter bundle</a>
            <a class="button" href="./store-import.html">Open import kit</a>
            <a class="button" href="#setup">View setup status</a>
          </div>
          <div class="system-note">
            <div class="signal">Generates one dated pack per run.</div>
            <div class="signal">Publishes static files only.</div>
            <div class="signal">Writes store-ready listing copy.</div>
            <div class="signal">Bundles the shelf as one ZIP.</div>
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
                <a class="button" href="./{esc(today_path)}seller-copy.md">Seller copy</a>
                <a class="button" href="./downloads/{esc(today_pack["pack_slug"])}.zip">Download ZIP</a>
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
          <p>{esc(recent_monetization_note)} <a href="./archive.html">Open archive</a> · <a href="./topics/">Topics</a> · <a href="./{esc(bundle_page_path)}">Starter bundle</a> · <a href="./support.html">Support</a> · <a href="./store-import.html">Import kit</a> · <a href="./terms.html">Policies</a> · <a href="./catalog.csv">Catalog CSV</a> · <a href="./catalog.json">Catalog JSON</a></p>
        </div>
        <div class="pack-grid">
          {cards}
        </div>
      </section>

      <section id="bundle">
        <div class="section-head">
          <div>
            <p class="label">Sellable bundle</p>
            <h2>Single download product</h2>
          </div>
          <p>{esc(bundle_monetization_note)}</p>
        </div>
        <div class="bundle-panel">
          <div>
            <p class="label">Starter archive</p>
            <h3>{bundle_pack_count} generated packs bundled</h3>
            <p>Worksheets, checklists, cover SVGs, manifests, listing copy, and catalog files are packaged together for a store-ready digital download.</p>
            <div class="actions">
              <a class="button primary" href="./{esc(bundle_zip_path)}">Download ZIP</a>
              <a class="button" href="./{esc(bundle_page_path)}">Bundle page</a>
              <a class="button" href="./support.html">Support page</a>
              {destination_cta}
            </div>
          </div>
          <div class="bundle-stat">
            <span>{bundle_pack_count}</span>
            <strong>packs</strong>
            <small>{bundle_kb} KB ZIP</small>
          </div>
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
              <strong>{esc(destination_label)}</strong>
              <p>{esc(destination_detail)}</p>
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
      <p>{policy_nav_links}</p>
    </footer>
  </div>
</body>
</html>
"""
    (DOCS / "index.html").write_text(content, encoding="utf-8")


def feed_timestamp(date_value: str) -> str:
    return f"{dt.date.fromisoformat(date_value).isoformat()}T00:00:00Z"


def rss_timestamp(date_value: str) -> str:
    day = dt.date.fromisoformat(date_value)
    stamp = dt.datetime(day.year, day.month, day.day, tzinfo=dt.UTC)
    return stamp.strftime("%a, %d %b %Y %H:%M:%S +0000")


def render_feed(config: dict[str, Any]) -> dict[str, Any]:
    manifests = read_manifests()[:50]
    site_name = config["site"]["name"]
    site_url = pack_url(config, "")
    feed_json_url = pack_url(config, "feed.json")
    feed_xml_url = pack_url(config, "feed.xml")
    atom_url = pack_url(config, "atom.xml")
    updated = feed_timestamp(manifests[0]["date"]) if manifests else "2026-01-01T00:00:00Z"
    feed = {
        "title": site_name,
        "home_page_url": site_url,
        "feed_url": feed_json_url,
        "rss_url": feed_xml_url,
        "atom_url": atom_url,
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

    rss_items = "\n".join(
        f"""    <item>
      <title>{esc(item["title"])}</title>
      <link>{esc(pack_url(config, item["path"]))}</link>
      <guid isPermaLink="true">{esc(pack_url(config, item["path"]))}</guid>
      <description>{esc(item["summary"])}</description>
      <pubDate>{rss_timestamp(item["date"])}</pubDate>
    </item>"""
        for item in manifests
    )
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>{esc(site_name)}</title>
    <link>{esc(site_url)}</link>
    <description>{esc(config["site"]["tagline"])}</description>
    <lastBuildDate>{rss_timestamp(manifests[0]["date"]) if manifests else "Thu, 01 Jan 2026 00:00:00 +0000"}</lastBuildDate>
    <atom:link xmlns:atom="http://www.w3.org/2005/Atom" href="{esc(feed_xml_url)}" rel="self" type="application/rss+xml"/>
{rss_items}
  </channel>
</rss>
"""
    (DOCS / "feed.xml").write_text(rss, encoding="utf-8")

    atom_entries = "\n".join(
        f"""  <entry>
    <title>{esc(item["title"])}</title>
    <id>{esc(item["id"])}</id>
    <link href="{esc(pack_url(config, item["path"]))}"/>
    <updated>{feed_timestamp(item["date"])}</updated>
    <summary>{esc(item["summary"])}</summary>
  </entry>"""
        for item in manifests
    )
    atom = f"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>{esc(site_name)}</title>
  <id>{esc(site_url)}</id>
  <link href="{esc(site_url)}"/>
  <link href="{esc(atom_url)}" rel="self" type="application/atom+xml"/>
  <updated>{updated}</updated>
  <subtitle>{esc(config["site"]["tagline"])}</subtitle>
{atom_entries}
</feed>
"""
    (DOCS / "atom.xml").write_text(atom, encoding="utf-8")

    return {
        "json_path": "feed.json",
        "rss_path": "feed.xml",
        "atom_path": "atom.xml",
        "item_count": len(manifests),
    }


def render_catalog(config: dict[str, Any]) -> None:
    manifests = read_manifests()
    catalog_items = []
    for item in manifests:
        catalog_items.append(
            {
                "id": item["id"],
                "date": item["date"],
                "title": item["title"],
                "description": item["summary"],
                "buyer": item.get("buyer", ""),
                "price_hint": config["generation"].get("default_price_hint", "$3 to $9 digital pack"),
                "url": pack_url(config, item["path"]),
                "worksheet_url": pack_url(config, item["worksheet"]),
                "checklist_url": pack_url(config, item["checklist"]),
                "cover_url": pack_url(config, item["cover"]),
                "seller_copy_url": pack_url(config, item.get("seller_copy", "")),
                "download_url": pack_url(config, pack_download_path(item)),
                "starter_bundle_url": pack_url(config, "bundles/starter-archive.zip"),
                "topic_urls": "|".join(record["url"] for record in topic_records_for_item(item, config)),
                "tags": listing_keywords(item),
                "monetization_enabled": bool(config["monetization"].get("enabled")),
            }
        )

    (DOCS / "catalog.json").write_text(
        json.dumps({"items": catalog_items}, indent=2),
        encoding="utf-8",
    )

    csv_path = DOCS / "catalog.csv"
    fieldnames = [
        "id",
        "date",
        "title",
        "description",
        "buyer",
        "price_hint",
        "url",
        "worksheet_url",
        "checklist_url",
        "cover_url",
        "seller_copy_url",
        "download_url",
        "starter_bundle_url",
        "topic_urls",
        "tags",
        "monetization_enabled",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(catalog_items)


def render_archive(config: dict[str, Any]) -> None:
    manifests = read_manifests()
    rows = "\n".join(
        f"""<article class="ledger-row">
          <strong>{esc(item["date_label"])}</strong>
          <p><a href="./{esc(item["path"])}">{esc(item["title"])}</a><br>{esc(item["summary"])}</p>
          <div class="row-actions">
            <a class="button" href="./{esc(item.get("seller_copy", item["path"]))}">Seller copy</a>
            <a class="button" href="./{esc(pack_download_path(item))}">Download ZIP</a>
          </div>
        </article>"""
        for item in manifests
    )
    if not rows:
        rows = "<p>No packs generated yet.</p>"

    page_url = pack_url(config, "archive.html")
    image_url = pack_url(config, manifests[0]["cover"]) if manifests else pack_url(config, "")
    structured_data = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Daily Autodigital Shelf Pack Archive",
        "description": "Archive of generated printable digital packs.",
        "url": page_url,
        "numberOfItems": len(manifests),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index + 1,
                "name": item["title"],
                "url": pack_url(config, item["path"]),
            }
            for index, item in enumerate(manifests[:80])
        ],
    }
    content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Pack Archive | {esc(config["site"]["name"])}</title>
  <meta name="description" content="Archive of generated Daily Autodigital Shelf packs.">
  <link rel="canonical" href="{esc(page_url)}">
{social_meta("Daily Autodigital Shelf Pack Archive", "Archive of generated printable digital packs.", page_url, image_url, "Daily Autodigital Shelf pack archive")}
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
      <nav class="topnav" aria-label="Archive navigation">
        <a href="./">Home</a>
        <a href="./topics/">Topics</a>
        <a href="./starter-bundle.html">Starter bundle</a>
        <a href="./support.html">Support</a>
        <a href="./store-import.html">Import kit</a>
        <a href="./terms.html">Policies</a>
        <a href="./catalog.json">Catalog JSON</a>
        <a href="./catalog.csv">Catalog CSV</a>
      </nav>
    </header>
    <main>
      <section>
        <div class="section-head">
          <div>
            <p class="label">Pack archive</p>
            <h2>Generated digital packs</h2>
          </div>
          <p>Each row has a public pack page, direct product ZIP, and store-ready listing copy. Topic pages group packs by use case, the <a href="./starter-bundle.html">starter bundle</a> packages the archive as one ZIP, the <a href="./store-import.html">import kit</a> packages marketplace listing metadata, and <a href="./terms.html">policy pages</a> prepare the shelf for future store review. Payment links remain off until a real store or support destination is connected.</p>
        </div>
        <div class="ledger">
          {rows}
        </div>
      </section>
    </main>
  </div>
</body>
</html>
"""
    (DOCS / "archive.html").write_text(content, encoding="utf-8")


def render_support_page(config: dict[str, Any]) -> dict[str, Any]:
    manifests = read_manifests()
    monetization = config["monetization"]
    store_url = str(monetization.get("store_url") or "").strip()
    support_url = str(monetization.get("support_url") or "").strip()
    destination_url = store_url or support_url
    destination_type = "store" if store_url else ("support" if support_url else "none")
    connected = bool(destination_url)
    page_rel_path = "support.html"
    page_url = pack_url(config, page_rel_path)
    home_url = pack_url(config, "")
    image_url = pack_url(config, manifests[0]["cover"]) if manifests else home_url
    latest_pack = manifests[0] if manifests else None
    latest_pack_url = pack_url(config, latest_pack["path"]) if latest_pack else home_url
    external_cta_label = "Open product checkout" if store_url else "Open Square support page"
    external_cta = (
        f"""<a class="button primary" href="{esc(destination_url)}">{esc(external_cta_label)}</a>"""
        if connected
        else """<a class="button primary" href="./#setup">Destination not connected</a>"""
    )
    destination_note = (
        f"Current public destination: {destination_url}. This is product checkout."
        if store_url
        else (
            f"Current public destination: {destination_url}. This is a Square-hosted CalmSprout gift-card/support path, not product checkout."
            if support_url
            else "No public support, store, or affiliate destination is connected yet."
        )
    )
    action_type = "BuyAction" if store_url else "DonateAction"
    structured_data: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "Support Daily Autodigital Shelf",
        "description": "Support page for a public automated digital-pack shelf.",
        "url": page_url,
        "isPartOf": {
            "@type": "WebSite",
            "name": config["site"]["name"],
            "url": home_url,
        },
    }
    if connected:
        structured_data["potentialAction"] = {
            "@type": action_type,
            "target": destination_url,
            "name": external_cta_label,
        }

    pack_rows = "\n".join(
        f"""<article class="ledger-row">
          <strong>{esc(item["date_label"])}</strong>
          <p><a href="./{esc(item["path"])}">{esc(item["title"])}</a><br>{esc(item["summary"])}</p>
          <div class="row-actions">
            <a class="button" href="./{esc(pack_download_path(item))}">Download ZIP</a>
            <a class="button" href="./{esc(item.get("seller_copy", item["path"]))}">Listing copy</a>
          </div>
        </article>"""
        for item in manifests[:7]
    )
    if not pack_rows:
        pack_rows = "<p>No packs generated yet.</p>"

    content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Support | {esc(config["site"]["name"])}</title>
  <meta name="description" content="Support the Daily Autodigital Shelf and download public generated digital packs.">
  <link rel="canonical" href="{esc(page_url)}">
{social_meta("Support Daily Autodigital Shelf", "Support the automated public digital-pack shelf.", page_url, image_url, "Daily Autodigital Shelf support page")}
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
      <nav class="topnav" aria-label="Support navigation">
        <a href="./">Home</a>
        <a href="./archive.html">Archive</a>
        <a href="./topics/">Topics</a>
        <a href="./starter-bundle.html">Starter bundle</a>
        <a href="./store-import.html">Import kit</a>
        <a href="./terms.html">Policies</a>
      </nav>
    </header>
    <main>
      <section class="hero support-hero">
        <div class="hero-copy">
          <p class="label">Support this shelf</p>
          <h1>Keep the daily pack shelf running.</h1>
          <p>The shelf publishes plain digital packs automatically. Downloads stay public while the support path can receive voluntary support through the connected external page.</p>
          <div class="actions">
            {external_cta}
            <a class="button" href="./starter-bundle.html">Open starter bundle</a>
            <a class="button" href="./bundles/starter-archive.zip">Download starter bundle</a>
            <a class="button" href="{esc(latest_pack_url)}">Open latest pack</a>
          </div>
          <p class="fineprint">{esc(destination_note)}</p>
        </div>
        <aside class="shelf-panel">
          <div class="panel-head">
            <div>
              <p class="label">Revenue boundary</p>
              <h2>{esc("Connected" if connected else "Not connected")}</h2>
            </div>
            <span class="status">{esc(destination_type)}</span>
          </div>
          <article class="artifact">
            <div>
              <h3>What support does</h3>
              <p>Support helps keep the automated pack shelf online. It does not create a private order queue, gated download, guaranteed delivery promise, or hidden live-money automation.</p>
              <p class="fineprint">This is not product checkout unless store_connected is true in status.json.</p>
            </div>
          </article>
        </aside>
      </section>
      <section>
        <div class="section-head">
          <div>
            <p class="label">Public downloads</p>
            <h2>Latest packs</h2>
          </div>
          <p>These files are available without a checkout gate. The support link is voluntary and handled by the external provider.</p>
        </div>
        <div class="ledger">
          {pack_rows}
        </div>
      </section>
    </main>
    <footer class="site-footer">
      <p>{esc(monetization.get("affiliate_disclosure", ""))}</p>
      <p>{policy_links(config)}</p>
    </footer>
  </div>
</body>
</html>
"""
    (DOCS / page_rel_path).write_text(content, encoding="utf-8")
    return {
        "page_path": page_rel_path,
        "page_url": page_url,
        "destination_type": destination_type,
        "destination_url": destination_url,
        "connected": connected,
    }


def render_ai_discovery_files(config: dict[str, Any], support: dict[str, Any]) -> dict[str, Any]:
    manifests = read_manifests()
    site_name = config["site"]["name"]
    base_url = pack_url(config, "")
    support_path = str(support.get("page_path", "support.html"))
    support_url = pack_url(config, support_path)
    destination_type = str(support.get("destination_type", "none"))
    destination_url = str(support.get("destination_url", ""))
    latest = manifests[0] if manifests else None
    latest_line = (
        f"- Latest pack: [{latest['title']}]({pack_url(config, latest['path'])}) - {latest['summary']}"
        if latest
        else "- Latest pack: none generated yet"
    )
    pack_lines = "\n".join(
        f"- [{item['title']}]({pack_url(config, item['path'])}) - {item['summary']} Download: {pack_url(config, pack_download_path(item))}"
        for item in manifests
    )
    if not pack_lines:
        pack_lines = "- No generated packs yet."

    monetization_line = (
        f"- Monetization destination: {destination_type} at {destination_url}"
        if destination_url
        else "- Monetization destination: none connected"
    )
    llms_txt = "\n".join(
        [
            f"# {site_name}",
            "",
            "> Automated public shelf of printable digital packs, worksheets, checklists, seller-copy files, and bundle/import artifacts.",
            "",
            "## Primary URLs",
            "",
            f"- Home: {base_url}",
            f"- Support page: {support_url}",
            f"- Archive: {pack_url(config, 'archive.html')}",
            f"- Starter bundle: {pack_url(config, 'starter-bundle.html')}",
            f"- Store import kit: {pack_url(config, 'store-import.html')}",
            f"- Catalog JSON: {pack_url(config, 'catalog.json')}",
            f"- RSS: {pack_url(config, 'feed.xml')}",
            f"- Atom: {pack_url(config, 'atom.xml')}",
            "",
            "## Current State",
            "",
            latest_line,
            monetization_line,
            "- Product checkout is not connected unless `store_connected` is true in status.json.",
            "- Support is voluntary and downloads remain public unless a real store checkout is connected.",
            "",
            "## Guardrails",
            "",
            "- No guaranteed-income claims.",
            "- No live trading.",
            "- No outbound spam.",
            "- No hidden payment credentials.",
            "- No medical, legal, investment, or tax advice.",
            "",
        ]
    )
    llms_full = "\n".join(
        [
            f"# {site_name} Full Context",
            "",
            "## Description",
            "",
            config["site"]["tagline"],
            "",
            "The shelf is generated by deterministic local Python automation and published as static files. It creates reusable printable worksheet packs, catalog metadata, policy pages, feeds, and ZIP archives.",
            "",
            "## Monetization Boundary",
            "",
            monetization_line,
            "- Current public support page: " + support_url,
            "- Product checkout is not connected unless `store_connected` is true in status.json.",
            "- Revenue is not guaranteed or claimed by the site.",
            "",
            "## Generated Packs",
            "",
            pack_lines,
            "",
            "## Machine-Readable Files",
            "",
            f"- Status: {pack_url(config, 'status.json')}",
            f"- Catalog JSON: {pack_url(config, 'catalog.json')}",
            f"- Catalog CSV: {pack_url(config, 'catalog.csv')}",
            f"- Topics JSON: {pack_url(config, 'topics/topics.json')}",
            f"- Store listings JSON: {pack_url(config, 'imports/store-listings.json')}",
            f"- Store listings CSV: {pack_url(config, 'imports/store-listings.csv')}",
            f"- JSON Feed: {pack_url(config, 'feed.json')}",
            f"- RSS: {pack_url(config, 'feed.xml')}",
            f"- Atom: {pack_url(config, 'atom.xml')}",
            f"- Sitemap: {pack_url(config, 'sitemap.xml')}",
            "",
        ]
    )
    (DOCS / "llms.txt").write_text(llms_txt, encoding="utf-8")
    (DOCS / "llms-full.txt").write_text(llms_full, encoding="utf-8")
    return {
        "ready": True,
        "llms_txt": "llms.txt",
        "llms_full_txt": "llms-full.txt",
    }


def render_sitemap(config: dict[str, Any]) -> None:
    urls = [
        pack_url(config, ""),
        pack_url(config, "archive.html"),
        pack_url(config, "support.html"),
        pack_url(config, "topics/"),
        pack_url(config, "starter-bundle.html"),
        pack_url(config, "store-import.html"),
        pack_url(config, "license.html"),
        pack_url(config, "privacy.html"),
        pack_url(config, "refund-policy.html"),
        pack_url(config, "terms.html"),
        pack_url(config, "catalog.json"),
        pack_url(config, "topics/topics.json"),
        pack_url(config, "imports/store-listings.csv"),
        pack_url(config, "imports/store-listings.json"),
        pack_url(config, "feed.json"),
        pack_url(config, "feed.xml"),
        pack_url(config, "atom.xml"),
        pack_url(config, "llms.txt"),
        pack_url(config, "llms-full.txt"),
    ]
    urls.extend(pack_url(config, f"topics/{slug}.html") for slug in topic_index(read_manifests(), config))
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


def render_indexnow_key(config: dict[str, Any]) -> dict[str, Any]:
    discovery = config.get("discovery", {})
    enabled = bool(discovery.get("indexnow_enabled"))
    key = str(discovery.get("indexnow_key", "")).strip()
    if not enabled:
        return {"enabled": False}
    if not re.fullmatch(r"[A-Za-z0-9-]{8,128}", key):
        raise ValueError("discovery.indexnow_key must be 8-128 letters, numbers, or dashes")

    key_file = f"{key}.txt"
    (DOCS / key_file).write_text(key, encoding="utf-8")
    return {
        "enabled": True,
        "key_file": key_file,
        "key_location": pack_url(config, key_file),
        "endpoint": discovery.get("indexnow_endpoint", "https://api.indexnow.org/indexnow"),
    }


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


def write_status(
    pack: dict[str, Any],
    config: dict[str, Any],
    bundle: dict[str, Any],
    downloads: dict[str, Any],
    feeds: dict[str, Any],
    import_kit: dict[str, Any],
    topics: dict[str, Any],
    policies: dict[str, Any],
    support: dict[str, Any],
    ai_discovery: dict[str, Any],
    discovery: dict[str, Any],
) -> None:
    status_path = DOCS / "status.json"
    monetization = config["monetization"]
    store_url = str(monetization.get("store_url") or "")
    support_url = str(monetization.get("support_url") or "")
    destination_url = store_url or support_url
    destination_type = "store" if store_url else ("support" if support_url else "none")
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
        "today_download": f"downloads/{pack['pack_slug']}.zip",
        "feed_json": feeds.get("json_path", "feed.json"),
        "feed_xml": feeds.get("rss_path", "feed.xml"),
        "atom_xml": feeds.get("atom_path", "atom.xml"),
        "feed_item_count": int(feeds.get("item_count", 0)),
        "bundle_ready": bool(bundle.get("pack_count")),
        "bundle_path": bundle.get("zip_path", "bundles/starter-archive.zip"),
        "bundle_page": bundle.get("page_path", "starter-bundle.html"),
        "bundle_pack_count": int(bundle.get("pack_count", 0)),
        "bundle_bytes": int(bundle.get("bytes", 0)),
        "pack_download_count": int(downloads.get("count", 0)),
        "pack_download_bytes": int(downloads.get("bytes", 0)),
        "store_import_ready": bool(import_kit.get("count")),
        "store_import_count": int(import_kit.get("count", 0)),
        "store_import_page": import_kit.get("page_path", "store-import.html"),
        "store_import_csv": import_kit.get("csv_path", "imports/store-listings.csv"),
        "store_import_json": import_kit.get("json_path", "imports/store-listings.json"),
        "store_import_zip": import_kit.get("zip_path", "imports/store-upload-kit.zip"),
        "store_import_zip_bytes": int(import_kit.get("zip_bytes", 0)),
        "topic_pages_ready": bool(topics.get("count")),
        "topic_page_count": int(topics.get("count", 0)),
        "topic_item_count": int(topics.get("items", 0)),
        "topics_index": topics.get("index_path", "topics/index.html"),
        "topics_json": topics.get("json_path", "topics/topics.json"),
        "policy_pages_ready": bool(policies.get("count")),
        "policy_page_count": int(policies.get("count", 0)),
        "policy_pages": policies.get("paths", []),
        "support_page_ready": bool(support.get("page_path")),
        "support_page": support.get("page_path", "support.html"),
        "ai_discovery_ready": bool(ai_discovery.get("ready")),
        "llms_txt": ai_discovery.get("llms_txt", "llms.txt"),
        "llms_full_txt": ai_discovery.get("llms_full_txt", "llms-full.txt"),
        "indexnow_enabled": bool(discovery.get("enabled")),
        "indexnow_key_file": discovery.get("key_file", ""),
        "indexnow_key_location": discovery.get("key_location", ""),
        "indexnow_endpoint": discovery.get("endpoint", ""),
        "monetization_enabled": bool(monetization.get("enabled")),
        "monetization_destination_type": destination_type,
        "monetization_destination_url": destination_url,
        "store_connected": bool(store_url),
        "support_connected": bool(support_url),
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
        "download": f"downloads/{pack['pack_slug']}.zip",
    }

    render_cover_svg(pack, pack_dir / "cover.svg")
    render_pack_page(pack, config, pack_dir / "index.html")
    render_printable(pack, pack_dir / "printable.html")
    render_checklist(pack, pack_dir / "checklist.html")
    render_seller_copy(pack, config, pack_dir / "seller-copy.md")
    (pack_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    downloads = render_pack_downloads()
    feeds = render_feed(config)
    render_catalog(config)
    render_archive(config)
    topics = render_topic_pages(config)
    policies = render_policy_pages(config)
    support = render_support_page(config)
    ai_discovery = render_ai_discovery_files(config, support)
    import_kit = render_store_import_kit(config)
    bundle = render_bundle(config)
    render_index(pack, config, bundle)
    render_sitemap(config)
    render_robots(config)
    discovery = render_indexnow_key(config)
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    write_status(pack, config, bundle, downloads, feeds, import_kit, topics, policies, support, ai_discovery, discovery)
    append_ledger(pack)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the Daily Autodigital Shelf static site.")
    parser.add_argument("--date", help="Optional ISO date override, for example 2026-06-02.")
    parser.add_argument(
        "--backfill-days",
        type=int,
        default=0,
        help="Generate a dated starter archive ending on --date/local today. Example: --backfill-days 21.",
    )
    args = parser.parse_args()

    target_day = date_from_args(args.date)
    if args.backfill_days and args.backfill_days > 0:
        start_day = target_day - dt.timedelta(days=args.backfill_days - 1)
        manifests = []
        for offset in range(args.backfill_days):
            manifests.append(generate(start_day + dt.timedelta(days=offset)))
        print(
            json.dumps(
                {
                    "status": "ok",
                    "mode": "backfill",
                    "days": args.backfill_days,
                    "start": start_day.isoformat(),
                    "end": target_day.isoformat(),
                    "packs": manifests,
                },
                indent=2,
            )
        )
        return 0

    manifest = generate(target_day)
    print(json.dumps({"status": "ok", "pack": manifest}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
