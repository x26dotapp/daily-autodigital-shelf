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
OFFERS = DOCS / "offers"
USE_CASES = DOCS / "use-cases"
TEMPLATES = DOCS / "templates"
GUIDES = DOCS / "guides"
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


def branded_url(config: dict[str, Any], path: str) -> str:
    base = str(config["site"].get("branded_base_url") or "").rstrip("/")
    if not base:
        return ""
    return f"{base}/{path.lstrip('/')}"


def branded_product_urls(config: dict[str, Any], item: dict[str, Any]) -> dict[str, str]:
    path_parts = Path(str(item.get("path", ""))).parts
    slug = str(item.get("pack_slug") or (path_parts[-1] if path_parts else "")).strip("/")
    if not slug:
        return {
            "branded_product_url": "",
            "branded_support_url": "",
            "branded_support_intent_url": "",
        }
    product_path = f"products/{slug}"
    support_path = f"{product_path}/support"
    return {
        "branded_product_url": branded_url(config, product_path),
        "branded_support_url": branded_url(config, support_path),
        "branded_support_intent_url": branded_url(config, f"{support_path}/go"),
    }


def branded_collection_support_url(config: dict[str, Any], slug: str) -> str:
    clean_slug = slug.strip().lower()
    if not clean_slug or not all(char in "abcdefghijklmnopqrstuvwxyz0123456789-" for char in clean_slug):
        return ""
    return branded_url(config, f"offers/{clean_slug}/support/go")


def branded_template_support_urls(config: dict[str, Any], slug: str) -> dict[str, str]:
    clean_slug = slug.strip().lower()
    if not clean_slug or not all(char in "abcdefghijklmnopqrstuvwxyz0123456789-" for char in clean_slug):
        return {
            "template_support_page_url": "",
            "template_support_intent_url": "",
        }
    support_path = f"templates/{clean_slug}/support"
    return {
        "template_support_page_url": branded_url(config, support_path),
        "template_support_intent_url": branded_url(config, f"{support_path}/go"),
    }


def pack_faq_items(pack: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "question": f"Is {pack['title']} a paid checkout?",
            "answer": "No. The pack download is public while product checkout remains disconnected.",
        },
        {
            "question": "How can someone support this pack?",
            "answer": "Use the support action for this pack. The branded support-intent redirect goes to the external Square support page with pack attribution.",
        },
        {
            "question": "What is included in the download?",
            "answer": "The ZIP includes a printable worksheet, checklist, cover image, seller copy, manifest, and related pack files.",
        },
    ]


def pack_support_card_text(item: dict[str, Any], config: dict[str, Any]) -> str:
    monetization = config["monetization"]
    support_url = str(monetization.get("support_url") or "").strip()
    branded_urls = branded_product_urls(config, item)
    support_intent_url = branded_urls.get("branded_support_intent_url") or support_url or pack_url(config, "support.html")
    support_page_url = branded_urls.get("branded_support_url") or pack_url(config, "support.html")
    return "\n".join(
        [
            f"{item['title']} - Support Card",
            "",
            f"Pack page: {pack_url(config, str(item['path']))}",
            f"Download page: {pack_url(config, pack_download_page_path(item))}",
            f"Pack ZIP: {pack_url(config, pack_download_path(item))}",
            f"Product support page: {support_page_url}",
            f"Support this pack: {support_intent_url}",
            "",
            "Support is voluntary. Product checkout is not connected. The pack download remains public.",
            "This file does not contain payment credentials, private account data, or guaranteed-income claims.",
            f"External support destination: {support_url}" if support_url else "External support destination: not connected",
        ]
    )


def starter_support_card_text(manifests: list[dict[str, Any]], config: dict[str, Any]) -> str:
    monetization = config["monetization"]
    support_url = str(monetization.get("support_url") or "").strip()
    latest = manifests[0] if manifests else None
    latest_support_url = ""
    if latest:
        latest_support_url = branded_product_urls(config, latest).get("branded_support_intent_url", "")
    return "\n".join(
        [
            "Daily Autodigital Shelf Starter Archive - Support Card",
            "",
            f"Starter bundle page: {pack_url(config, 'starter-bundle.html')}",
            f"Pay what you can page: {pack_url(config, 'pay-what-you-can.html')}",
            f"Support page: {pack_url(config, 'support.html')}",
            f"Latest pack support: {latest_support_url or support_url or pack_url(config, 'support.html')}",
            "",
            "Support is voluntary. Product checkout is not connected. The bundle remains public.",
            "This file does not contain payment credentials, private account data, or guaranteed-income claims.",
            f"External support destination: {support_url}" if support_url else "External support destination: not connected",
        ]
    )


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
    branded_urls = branded_product_urls(config, pack)
    support_intent_url = branded_urls.get("branded_support_intent_url") or support_url
    destination_url = store_url or support_intent_url
    destination_type = "store" if store_url else ("support" if support_url else "none")
    buy_label = "Store link not connected"
    buy_href = "../../#setup"
    if monetization.get("enabled") and store_url:
        buy_label = "Buy or download from store"
        buy_href = store_url
    elif support_intent_url:
        buy_label = "Support this pack"
        buy_href = support_intent_url

    pack_path = f"packs/{pack['pack_slug']}/"
    canonical_url = pack_url(config, pack_path)
    cover_url = pack_url(config, f"{pack_path}cover.svg")
    download_url = pack_url(config, f"downloads/{pack['pack_slug']}.zip")
    offer_data: dict[str, Any] = {
        "@type": "Offer",
        "url": canonical_url if not store_url else store_url,
        "availability": "https://schema.org/InStock",
    }
    if store_url:
        offer_data["description"] = "External store checkout for this digital pack."
    else:
        offer_data.update(
            {
                "price": "0.00",
                "priceCurrency": "USD",
                "description": "Public digital-pack download. Voluntary support is handled separately through Square.",
            }
        )
    product_data: dict[str, Any] = {
        "@type": ["CreativeWork", "Product"],
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
        "offers": offer_data,
        "url": canonical_url,
    }
    if destination_url:
        product_data["potentialAction"] = {
            "@type": "BuyAction" if destination_type == "store" else "DonateAction",
            "target": destination_url,
            "name": "Open product checkout" if destination_type == "store" else "Support this pack",
        }
    faq_items = pack_faq_items(pack)
    faq_data = {
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item["answer"],
                },
            }
            for item in faq_items
        ],
    }
    structured_data = {
        "@context": "https://schema.org",
        "@graph": [product_data, faq_data],
    }
    worksheet_items = "\n".join(f"<li>{esc(item)}</li>" for item in pack["worksheets"])
    checklist_items = "\n".join(f"<li>{esc(item)}</li>" for item in pack["checklist"])
    faq_sections = "\n".join(
        f"""        <section class="faq-item">
          <h3>{esc(item["question"])}</h3>
          <p>{esc(item["answer"])}</p>
        </section>"""
        for item in faq_items
    )
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
        <a class="button" href="../../downloads/{esc(pack["pack_slug"])}.html">Download pack</a>
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
      <h2>Product FAQ</h2>
      <div class="faq-list">
{faq_sections}
      </div>
      <p class="fineprint">{esc(monetization.get("affiliate_disclosure", ""))}</p>
    </article>
  </main>
</body>
</html>
"""
    out_path.write_text(content, encoding="utf-8")


def refresh_existing_pack_pages(config: dict[str, Any]) -> dict[str, Any]:
    refreshed = 0
    skipped = 0
    for manifest in read_manifests():
        try:
            day = dt.date.fromisoformat(str(manifest["date"]))
        except (KeyError, ValueError):
            skipped += 1
            continue
        pack = pack_for_day(day, config)
        if (
            manifest.get("title") != pack["title"]
            or manifest.get("summary") != pack["summary"]
            or Path(str(manifest.get("path", ""))).parts[-1] != pack["pack_slug"]
        ):
            skipped += 1
            continue
        render_pack_page(pack, config, DOCS / str(manifest["path"]).strip("/") / "index.html")
        refreshed += 1
    return {"refreshed": refreshed, "skipped": skipped}


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
        "pay-what-you-can.html",
        "sponsor.html",
        "commercial-use.html",
        "sponsor-kit.json",
        "store-import.html",
        "license.html",
        "privacy.html",
        "refund-policy.html",
        "terms.html",
        "llms.txt",
        "llms-full.txt",
        "offers/index.html",
        "offers/offers.json",
        "topics/index.html",
        "topics/topics.json",
        "use-cases/index.html",
        "use-cases/use-cases.json",
        "templates/index.html",
        "templates/templates.json",
        "guides/index.html",
        "guides/guides.json",
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
    for path in sorted(OFFERS.glob("*.html")):
        rel_paths.append(path.relative_to(DOCS).as_posix())
    for path in sorted(USE_CASES.glob("*.html")):
        rel_paths.append(path.relative_to(DOCS).as_posix())
    for path in sorted(TEMPLATES.glob("*.html")):
        rel_paths.append(path.relative_to(DOCS).as_posix())
    for path in sorted(GUIDES.glob("*.html")):
        rel_paths.append(path.relative_to(DOCS).as_posix())

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


def pack_download_page_path(item: dict[str, Any]) -> str:
    return f"downloads/{pack_slug_from_manifest(item)}.html"


def template_slug_for_item(item: dict[str, Any]) -> str:
    slug = pack_slug_from_manifest(item)
    return re.sub(r"^\d{4}-\d{2}-\d{2}-", "", slug)


def template_page_path(item: dict[str, Any]) -> str:
    return f"templates/{template_slug_for_item(item)}.html"


def guide_page_path(item: dict[str, Any]) -> str:
    return f"guides/{template_slug_for_item(item)}.html"


def template_records(config: dict[str, Any]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in read_manifests():
        slug = template_slug_for_item(item)
        if not slug or slug in seen:
            continue
        seen.add(slug)
        path = f"templates/{slug}.html"
        branded_urls = branded_product_urls(config, item)
        template_support_urls = branded_template_support_urls(config, slug)
        topics = topic_records_for_item(item, config)
        records.append(
            {
                "slug": slug,
                "id": item["id"],
                "date": item["date"],
                "date_label": item["date_label"],
                "title": item["title"],
                "summary": item["summary"],
                "buyer": item.get("buyer", ""),
                "path": path,
                "url": pack_url(config, path),
                "branded_url": branded_url(config, path),
                "pack_path": item["path"],
                "pack_url": pack_url(config, item["path"]),
                "download_page_path": pack_download_page_path(item),
                "download_page_url": pack_url(config, pack_download_page_path(item)),
                "download_path": pack_download_path(item),
                "download_url": pack_url(config, pack_download_path(item)),
                "seller_copy_path": item.get("seller_copy", ""),
                "seller_copy_url": pack_url(config, item.get("seller_copy", "")),
                "cover_path": item.get("cover", ""),
                "cover_url": pack_url(config, item.get("cover", "")),
                "support_page_url": template_support_urls["template_support_page_url"] or branded_urls.get("branded_support_url") or pack_url(config, "support.html"),
                "support_intent_url": template_support_urls["template_support_intent_url"] or branded_urls.get("branded_support_intent_url") or str(config["monetization"].get("support_url") or ""),
                "dated_product_support_page_url": branded_urls.get("branded_support_url", ""),
                "dated_product_support_intent_url": branded_urls.get("branded_support_intent_url", ""),
                "starter_bundle_path": "bundles/starter-archive.zip",
                "starter_bundle_url": pack_url(config, "bundles/starter-archive.zip"),
                "topic_slugs": [topic["slug"] for topic in topics],
                "topic_urls": [topic["url"] for topic in topics],
            }
        )
    return records


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


USE_CASE_DEFINITIONS: dict[str, dict[str, Any]] = {
    "small-business-ops": {
        "topic_slug": "small-business-ops",
        "label": "Small business SOP and client ops worksheets",
        "short_label": "Client and SOP ops",
        "description": "A buyer-intent page for tiny service shops that need client intake, SOP, follow-up, listing, and admin worksheets without a full operations buildout.",
        "intent": "small business SOP templates, client admin worksheets, and simple operating routines",
        "outcomes": [
            "Name the next client or service workflow that needs a written path.",
            "Pick a public worksheet pack that can be downloaded immediately.",
            "Use the collection bundle when a single ZIP is easier than one-by-one downloads.",
        ],
    },
    "home-admin": {
        "topic_slug": "home-admin",
        "label": "Home admin reset printables",
        "short_label": "Home admin reset",
        "description": "A buyer-intent page for households and freelancers who need paperwork, renewals, subscription, inventory, and appointment sheets that stay simple.",
        "intent": "home admin printables, renewal trackers, budget reset sheets, and household paperwork templates",
        "outcomes": [
            "Choose one household admin area that needs a visible page.",
            "Download the related pack instead of building a full spreadsheet system.",
            "Use the collection bundle as a small home-admin starter folder.",
        ],
    },
    "low-energy-systems": {
        "topic_slug": "low-energy-systems",
        "label": "Low-energy planning systems",
        "short_label": "Low-energy planning",
        "description": "A buyer-intent page for disabled, neurodivergent, or overloaded workers who need gentle planning packs with fallback versions and shutdown notes.",
        "intent": "low energy planner, neurodivergent task planning sheets, and gentle printable systems",
        "outcomes": [
            "Pick one anchor task instead of an overbuilt plan.",
            "Use a worksheet with a fallback version that still counts.",
            "Keep the bundle available for uneven-energy weeks.",
        ],
    },
    "digital-product-prep": {
        "topic_slug": "digital-product-prep",
        "label": "Digital product launch prep worksheets",
        "short_label": "Product launch prep",
        "description": "A buyer-intent page for creators and small operators preparing listing copy, launch assets, import metadata, and product pages.",
        "intent": "digital product launch checklist, listing copy templates, and store import prep worksheets",
        "outcomes": [
            "Choose the product-prep worksheet that matches the next launch bottleneck.",
            "Inspect seller-copy files before putting anything into a store.",
            "Download the collection bundle for product listing preparation.",
        ],
    },
    "cleanup-and-reset": {
        "topic_slug": "cleanup-and-reset",
        "label": "Cleanup and reset sprint worksheets",
        "short_label": "Cleanup reset",
        "description": "A buyer-intent page for people who need short reset worksheets for files, folders, receipts, stalled projects, and digital clutter.",
        "intent": "digital declutter worksheets, reset sprint printables, and project cleanup checklists",
        "outcomes": [
            "Choose one cleanup surface that can be finished without a marathon.",
            "Use a public worksheet to make the next visible decision.",
            "Keep the collection bundle ready for repeated reset sessions.",
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


def render_pack_downloads(config: dict[str, Any]) -> dict[str, Any]:
    manifests = read_manifests()
    DOWNLOADS.mkdir(parents=True, exist_ok=True)
    outputs = []

    for item in manifests:
        slug = pack_slug_from_manifest(item)
        zip_rel_path = pack_download_path(item)
        download_page_rel_path = pack_download_page_path(item)
        if item.get("download") != zip_rel_path:
            item["download"] = zip_rel_path
            manifest_path = DOCS / item["path"] / "manifest.json"
            manifest_path.write_text(json.dumps(item, indent=2), encoding="utf-8")
        download_page_url = pack_url(config, download_page_rel_path)
        zip_url = pack_url(config, zip_rel_path)
        pack_page_url = pack_url(config, str(item["path"]))
        branded_urls = branded_product_urls(config, item)
        support_intent_url = branded_urls.get("branded_support_intent_url") or str(config["monetization"].get("support_url") or "")
        support_page_url = branded_urls.get("branded_support_url") or pack_url(config, "support.html")
        cover_url = pack_url(config, str(item["cover"]))
        structured_data = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": f"{item['title']} download page",
            "description": f"Download the public {item['title']} pack ZIP and optionally support the shelf.",
            "url": download_page_url,
            "about": {
                "@type": "CreativeWork",
                "name": item["title"],
                "url": pack_page_url,
            },
            "potentialAction": [
                {
                    "@type": "DownloadAction",
                    "target": zip_url,
                    "name": "Download pack ZIP",
                },
                {
                    "@type": "DonateAction",
                    "target": support_intent_url,
                    "name": "Support this pack",
                },
            ],
        }
        download_page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(item["title"])} Download | {esc(config["site"]["name"])}</title>
  <meta name="description" content="Download the public {esc(item["title"])} pack ZIP and optionally support the shelf.">
  <link rel="canonical" href="{esc(download_page_url)}">
{social_meta(f"{item['title']} Download", item["summary"], download_page_url, cover_url, f"{item['title']} cover")}
  <script type="application/ld+json">{json_for_script(structured_data)}</script>
  <link rel="stylesheet" href="../styles.css">
</head>
<body>
  <div class="site-shell">
    <header class="topbar">
      <a class="brand" href="../">
        <span class="brand-mark">D</span>
        <span class="brand-name">{esc(config["site"]["name"])}</span>
      </a>
      <nav class="topnav" aria-label="Download navigation">
        <a href="../{esc(item["path"])}">Pack page</a>
        <a href="../support.html">Support</a>
        <a href="../pay-what-you-can.html">Pay what you can</a>
      </nav>
    </header>
    <main>
      <section class="hero">
        <div class="hero-copy">
          <p class="label">Public download</p>
          <h1>{esc(item["title"])}</h1>
          <p>{esc(item["summary"])}</p>
          <div class="actions">
            <a class="button primary" href="./{esc(slug)}.zip">Download ZIP</a>
            <a class="button" href="{esc(support_intent_url)}">Support this pack</a>
            <a class="button" href="../{esc(item["path"])}">Open pack page</a>
          </div>
          <p class="fineprint">Support is voluntary. Product checkout is not connected. The pack download remains public.</p>
        </div>
        <aside class="shelf-panel">
          <div class="panel-head">
            <div>
              <p class="label">Support route</p>
              <h2>Pack attribution</h2>
            </div>
            <span class="status">support</span>
          </div>
          <article class="artifact">
            <div>
              <h3>Where support goes</h3>
              <p>The support action routes through the product-specific CalmSprout support page before reaching the external Square support destination.</p>
              <p><a href="{esc(support_page_url)}">Open support page</a></p>
            </div>
          </article>
        </aside>
      </section>
    </main>
    <footer class="site-footer">
      <p>{esc(config["monetization"].get("affiliate_disclosure", ""))}</p>
      <p>{policy_links(config, "../")}</p>
    </footer>
  </div>
</body>
</html>
"""
        (DOCS / download_page_rel_path).write_text(download_page, encoding="utf-8")
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
                "See SUPPORT.txt for the voluntary support URL for this pack.",
            ]
        )
        with zipfile.ZipFile(zip_path, "w") as bundle:
            write_zip_entry(bundle, f"{zip_root}/README.txt", readme.encode("utf-8"))
            write_zip_entry(bundle, f"{zip_root}/SUPPORT.txt", pack_support_card_text(item, config).encode("utf-8"))
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
                "download_page": download_page_rel_path,
                "bytes": zip_path.stat().st_size,
            }
        )

    return {
        "count": len(outputs),
        "page_count": len(outputs),
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
    monetization = config["monetization"]
    store_url = str(monetization.get("store_url") or "")
    support_url = str(monetization.get("support_url") or "")
    destination_url = store_url or support_url
    destination_type = "store" if store_url else ("support" if support_url else "none")
    support_page_url = pack_url(config, "support.html")
    pay_what_you_can_url = pack_url(config, "pay-what-you-can.html")
    for item in read_manifests():
        branded_urls = branded_product_urls(config, item)
        rows.append(
            {
                "sku": item["id"].replace("daily-autodigital-shelf:", "das-"),
                "title": item["title"],
                "subtitle": item["summary"],
                "buyer": item.get("buyer", ""),
                "price_hint": config["generation"].get("default_price_hint", "$3 to $9 digital pack"),
                "currency": "USD",
                "download_url": pack_url(config, pack_download_path(item)),
                "download_page_url": pack_url(config, pack_download_page_path(item)),
                "preview_url": pack_url(config, item["path"]),
                "worksheet_url": pack_url(config, item["worksheet"]),
                "checklist_url": pack_url(config, item["checklist"]),
                "cover_url": pack_url(config, item["cover"]),
                "seller_copy_url": pack_url(config, item.get("seller_copy", "")),
                "support_page_url": support_page_url,
                "pay_what_you_can_url": pay_what_you_can_url,
                **branded_urls,
                "monetization_destination_type": destination_type,
                "monetization_destination_url": destination_url,
                "store_connected": bool(store_url),
                "support_connected": bool(support_url),
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
        "download_page_url",
        "preview_url",
        "worksheet_url",
        "checklist_url",
        "cover_url",
        "seller_copy_url",
        "support_page_url",
        "pay_what_you_can_url",
        "branded_product_url",
        "branded_support_url",
        "branded_support_intent_url",
        "monetization_destination_type",
        "monetization_destination_url",
        "store_connected",
        "support_connected",
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
        for rel_path in [
            csv_rel_path,
            json_rel_path,
            "catalog.csv",
            "catalog.json",
            "product-feed.json",
            "product-feed.xml",
            "product-feed.csv",
            "support-funnel.json",
            "support-funnel.xml",
            "support-funnel.csv",
            "sponsor.html",
            "commercial-use.html",
            "sponsor-kit.json",
            "guides/index.html",
            "guides/guides.json",
            *policy_paths,
        ]:
            source = DOCS / rel_path
            if source.exists():
                write_zip_entry(bundle, f"{zip_root}/{rel_path}", read_zip_source_bytes(source))
        for item in read_manifests():
            for rel_path in [item.get("seller_copy", ""), pack_download_path(item), item["cover"], template_page_path(item), guide_page_path(item)]:
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
            <a class="button" href="{esc(row["download_page_url"])}">Download page</a>
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
        <a href="./use-cases/">Use cases</a>
        <a href="./templates/">Templates</a>
        <a href="./guides/">Guides</a>
        <a href="./offers/">Offers</a>
        <a href="./commercial-use.html">Commercial use</a>
        <a href="./sponsor.html">Sponsor</a>
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
              <a class="button" href="./commercial-use.html">Commercial use</a>
              <a class="button" href="./sponsor.html">Sponsor kit</a>
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


def collection_bundle_rel_path(slug: str) -> str:
    return f"bundles/{slug}-collection.zip"


def collection_bundle_file_paths(slug: str, items: list[dict[str, Any]]) -> list[Path]:
    rel_paths = [
        "support.html",
        "pay-what-you-can.html",
        "topics/topics.json",
        f"topics/{slug}.html",
        "use-cases/use-cases.json",
        f"use-cases/{slug}.html",
        "templates/index.html",
        "templates/templates.json",
        "guides/index.html",
        "guides/guides.json",
        "catalog.json",
        "catalog.csv",
    ]
    for item in items:
        pack_path = str(item["path"]).rstrip("/")
        rel_paths.extend(
            [
                f"{pack_path}/index.html",
                f"{pack_path}/printable.html",
                f"{pack_path}/checklist.html",
                f"{pack_path}/cover.svg",
                f"{pack_path}/manifest.json",
                f"{pack_path}/seller-copy.md",
                pack_download_path(item),
                pack_download_page_path(item),
                template_page_path(item),
                guide_page_path(item),
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


def collection_support_card_text(
    slug: str,
    topic: dict[str, Any],
    items: list[dict[str, Any]],
    config: dict[str, Any],
) -> str:
    support_url = str(config["monetization"].get("support_url") or "").strip()
    support_intent_url = branded_collection_support_url(config, slug) or support_url or pack_url(config, "support.html")
    return "\n".join(
        [
            f"{topic['label']} Collection Bundle - Support Card",
            "",
            f"Collection offer page: {pack_url(config, f'offers/{slug}.html')}",
            f"Topic page: {pack_url(config, f'topics/{slug}.html')}",
            f"Collection bundle ZIP: {pack_url(config, collection_bundle_rel_path(slug))}",
            f"Support this collection: {support_intent_url}",
            f"Included pack count: {len(items)}",
            "",
            "Support is voluntary. Product checkout is not connected. The collection bundle remains public.",
            "This file does not contain payment credentials, private account data, or guaranteed-income claims.",
            f"External support destination: {support_url}" if support_url else "External support destination: not connected",
        ]
    )


def write_collection_bundle(
    config: dict[str, Any],
    slug: str,
    topic: dict[str, Any],
    items: list[dict[str, Any]],
) -> dict[str, Any]:
    BUNDLES.mkdir(parents=True, exist_ok=True)
    bundle_rel_path = collection_bundle_rel_path(slug)
    bundle_path = DOCS / bundle_rel_path
    zip_root = f"daily-autodigital-shelf-{slug}-collection"
    latest_date = items[0]["date"] if items else ""
    oldest_date = items[-1]["date"] if items else ""
    support_intent_url = branded_collection_support_url(config, slug)
    bundle_manifest = {
        "id": f"daily-autodigital-shelf:collection:{slug}",
        "title": f"{topic['label']} Collection Bundle",
        "description": topic["description"],
        "slug": slug,
        "pack_count": len(items),
        "oldest_date": oldest_date,
        "latest_date": latest_date,
        "zip_path": bundle_rel_path,
        "url": pack_url(config, bundle_rel_path),
        "offer_page": f"offers/{slug}.html",
        "topic_page": f"topics/{slug}.html",
        "support_intent_url": support_intent_url,
        "items": [
            {
                "id": item["id"],
                "date": item["date"],
                "title": item["title"],
                "path": item["path"],
                "download": pack_download_path(item),
                "download_page": pack_download_page_path(item),
            }
            for item in items
        ],
    }
    readme = "\n".join(
        [
            f"{topic['label']} Collection Bundle",
            "",
            topic["description"],
            "",
            f"Pack count: {len(items)}",
            f"Date range: {oldest_date} to {latest_date}",
            f"Offer page: {pack_url(config, f'offers/{slug}.html')}",
            f"Topic page: {pack_url(config, f'topics/{slug}.html')}",
            "",
            "This bundle contains public generated worksheets, checklists, cover SVGs, manifests, seller-copy files, individual ZIPs, and download landing pages for one topic collection.",
            "It is designed as a focused digital-download bundle that can be supported voluntarily while checkout is disconnected.",
            "",
            "Guardrails: no guaranteed-income claims, no payment credentials, no medical/legal/investment advice, and no hidden live-fund behavior.",
        ]
    )

    with zipfile.ZipFile(bundle_path, "w") as bundle:
        write_zip_entry(bundle, f"{zip_root}/README.txt", readme.encode("utf-8"))
        write_zip_entry(
            bundle,
            f"{zip_root}/SUPPORT.txt",
            collection_support_card_text(slug, topic, items, config).encode("utf-8"),
        )
        write_zip_entry(
            bundle,
            f"{zip_root}/COLLECTION-BUNDLE-MANIFEST.json",
            json.dumps(bundle_manifest, indent=2).encode("utf-8"),
        )
        for source in collection_bundle_file_paths(slug, items):
            rel = source.relative_to(DOCS).as_posix()
            write_zip_entry(bundle, f"{zip_root}/{rel}", read_zip_source_bytes(source))

    return {
        "path": bundle_rel_path,
        "url": pack_url(config, bundle_rel_path),
        "bytes": bundle_path.stat().st_size,
        "pack_count": len(items),
    }


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
        <a href="../offers/">Offers</a>
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
            <a class="button" href="../{esc(pack_download_page_path(item))}">Download page</a>
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
        <a href="../offers/{esc(slug)}.html">Offer</a>
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


def render_use_case_pages(config: dict[str, Any]) -> dict[str, Any]:
    USE_CASES.mkdir(parents=True, exist_ok=True)
    manifests = read_manifests()
    topics = topic_index(manifests, config)
    monetization = config["monetization"]
    store_url = str(monetization.get("store_url") or "").strip()
    support_url = str(monetization.get("support_url") or "").strip()
    general_support_url = branded_url(config, "support") or pack_url(config, "support.html")
    destination_note = (
        "Product checkout is connected through the configured external store."
        if store_url
        else (
            "Product checkout is not connected. Downloads remain public and support is voluntary through the connected support path."
            if support_url
            else "No external store, support, or affiliate destination is connected yet."
        )
    )

    records: list[dict[str, Any]] = []
    for slug, definition in USE_CASE_DEFINITIONS.items():
        topic_slug = str(definition["topic_slug"])
        items = topics.get(topic_slug, [])
        if not items:
            continue
        page_path = f"use-cases/{slug}.html"
        collection_bundle_path = collection_bundle_rel_path(topic_slug)
        collection_bundle_url = pack_url(config, collection_bundle_path)
        collection_support_url = branded_collection_support_url(config, topic_slug) or general_support_url
        record = {
            "slug": slug,
            "topic_slug": topic_slug,
            "label": definition["label"],
            "short_label": definition["short_label"],
            "description": definition["description"],
            "intent": definition["intent"],
            "path": page_path,
            "url": pack_url(config, page_path),
            "branded_url": branded_url(config, page_path),
            "topic_url": pack_url(config, f"topics/{topic_slug}.html"),
            "offer_url": pack_url(config, f"offers/{topic_slug}.html"),
            "collection_bundle_path": collection_bundle_path,
            "collection_bundle_url": collection_bundle_url,
            "support_page_url": general_support_url,
            "support_intent_url": collection_support_url,
            "count": len(items),
            "outcomes": list(definition["outcomes"]),
            "items": [
                {
                    "id": item["id"],
                    "title": item["title"],
                    "summary": item["summary"],
                    "url": pack_url(config, item["path"]),
                    "download_page_url": pack_url(config, pack_download_page_path(item)),
                    "download_url": pack_url(config, pack_download_path(item)),
                }
                for item in items
            ],
        }
        records.append(record)

    use_cases_export = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Daily Autodigital Shelf Use Cases",
        "description": "Buyer-intent use-case pages for public printable digital pack collections.",
        "url": pack_url(config, "use-cases/"),
        "numberOfItems": len(records),
        "checkoutBoundary": destination_note,
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index + 1,
                "name": record["label"],
                "url": record["url"],
            }
            for index, record in enumerate(records)
        ],
        "items": records,
    }
    (USE_CASES / "use-cases.json").write_text(json.dumps(use_cases_export, indent=2), encoding="utf-8")

    first_cover = pack_url(config, manifests[0]["cover"]) if manifests else pack_url(config, "")
    index_url = pack_url(config, "use-cases/")
    index_cards = "\n".join(
        f"""<article class="pack-card">
          <span class="pack-date">{record["count"]} packs</span>
          <h3>{esc(record["short_label"])}</h3>
          <p>{esc(record["description"])}</p>
          <div class="artifact-links">
            <a class="button primary" href="./{esc(record["slug"])}.html">Open use case</a>
            <a class="button" href="../offers/{esc(record["topic_slug"])}.html">Offer</a>
          </div>
        </article>"""
        for record in records
    )
    if not index_cards:
        index_cards = "<p>No use cases generated yet.</p>"

    index_data = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Daily Autodigital Shelf Use Cases",
        "description": "Buyer-intent use-case pages for generated printable digital packs.",
        "url": index_url,
        "hasPart": [
            {
                "@type": "CollectionPage",
                "name": record["label"],
                "url": record["url"],
            }
            for record in records
        ],
    }
    index_html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Use Cases | {esc(config["site"]["name"])}</title>
  <meta name="description" content="Buyer-intent use-case pages for Daily Autodigital Shelf printable digital packs.">
  <link rel="canonical" href="{esc(index_url)}">
{social_meta("Daily Autodigital Shelf Use Cases", "Buyer-intent use-case pages for generated printable digital packs.", index_url, first_cover, "Daily Autodigital Shelf use cases")}
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
      <nav class="topnav" aria-label="Use case navigation">
        <a href="../">Home</a>
        <a href="../archive.html">Archive</a>
        <a href="../topics/">Topics</a>
        <a href="../offers/">Offers</a>
        <a href="../support.html">Support</a>
      </nav>
    </header>
    <main>
      <section>
        <div class="section-head">
          <div>
            <p class="label">Use cases</p>
            <h2>Buyer-intent pages for public pack collections</h2>
          </div>
          <p>These pages translate the generated archive into practical search and support surfaces. Downloads stay public; support is voluntary unless a real store checkout is connected.</p>
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
    (USE_CASES / "index.html").write_text(index_html, encoding="utf-8")

    for record in records:
        items = topics[record["topic_slug"]]
        image_url = pack_url(config, items[0]["cover"])
        outcome_cards = "\n".join(
            f"""<div class="signal">{esc(outcome)}</div>"""
            for outcome in record["outcomes"]
        )
        rows = "\n".join(
            f"""<article class="ledger-row">
          <strong>{esc(item["date_label"])}</strong>
          <p><a href="../{esc(item["path"])}">{esc(item["title"])}</a><br>{esc(item["summary"])}</p>
          <div class="row-actions">
            <a class="button" href="../{esc(pack_download_page_path(item))}">Download page</a>
            <a class="button" href="../{esc(item.get("seller_copy", item["path"]))}">Listing copy</a>
          </div>
        </article>"""
            for item in items
        )
        page_data = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "CollectionPage",
                    "name": record["label"],
                    "description": record["description"],
                    "url": record["url"],
                    "keywords": record["intent"],
                    "isPartOf": {
                        "@type": "WebSite",
                        "name": config["site"]["name"],
                        "url": pack_url(config, ""),
                    },
                    "hasPart": [
                        {
                            "@type": "CreativeWork",
                            "name": item["title"],
                            "description": item["summary"],
                            "url": pack_url(config, item["path"]),
                            "encoding": {
                                "@type": "MediaObject",
                                "contentUrl": pack_url(config, pack_download_path(item)),
                                "encodingFormat": "application/zip",
                            },
                        }
                        for item in items[:50]
                    ],
                    "potentialAction": [
                        {
                            "@type": "DownloadAction",
                            "target": record["collection_bundle_url"],
                            "name": "Download collection bundle",
                        },
                        {
                            "@type": "DonateAction",
                            "target": record["support_intent_url"],
                            "name": "Support this use case",
                        },
                    ],
                },
                {
                    "@type": "ItemList",
                    "name": f"{record['short_label']} included packs",
                    "numberOfItems": len(items),
                    "itemListElement": [
                        {
                            "@type": "ListItem",
                            "position": index + 1,
                            "name": item["title"],
                            "url": pack_url(config, item["path"]),
                        }
                        for index, item in enumerate(items[:50])
                    ],
                },
            ],
        }
        html_content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(record["short_label"])} | {esc(config["site"]["name"])}</title>
  <meta name="description" content="{esc(record["description"])}">
  <link rel="canonical" href="{esc(record["url"])}">
{social_meta(record["label"], record["description"], record["url"], image_url, f"{record['short_label']} use case")}
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
      <nav class="topnav" aria-label="Use case page navigation">
        <a href="../">Home</a>
        <a href="./">Use cases</a>
        <a href="../topics/{esc(record["topic_slug"])}.html">Topic</a>
        <a href="../offers/{esc(record["topic_slug"])}.html">Offer</a>
        <a href="../support.html">Support</a>
      </nav>
    </header>
    <main>
      <section class="hero">
        <div class="hero-copy">
          <p class="label">Use case</p>
          <h1>{esc(record["label"])}</h1>
          <p>{esc(record["description"])}</p>
          <div class="actions">
            <a class="button primary" href="../{esc(record["collection_bundle_path"])}">Download collection bundle</a>
            <a class="button" href="../offers/{esc(record["topic_slug"])}.html">Open collection offer</a>
            <a class="button" href="{esc(record["support_page_url"])}">Open support page</a>
            <a class="button" href="{esc(record["support_intent_url"])}">Support this use case</a>
          </div>
          <p class="fineprint">{esc(destination_note)} This page is a discovery and support surface, not proof of revenue.</p>
        </div>
        <aside class="shelf-panel">
          <div class="panel-head">
            <div>
              <p class="label">Intent match</p>
              <h2>{esc(record["short_label"])}</h2>
            </div>
            <span class="status">{record["count"]} packs</span>
          </div>
          <article class="artifact">
            <div>
              <h3>Search intent</h3>
              <p>{esc(record["intent"])}</p>
            </div>
          </article>
        </aside>
      </section>
      <section>
        <div class="section-head">
          <div>
            <p class="label">Practical path</p>
            <h2>What a visitor can do immediately</h2>
          </div>
          <p>Each step stays small: inspect the pack, download the public file, then optionally support the shelf through CalmSprout.</p>
        </div>
        <div class="system-note">
          {outcome_cards}
        </div>
      </section>
      <section>
        <div class="section-head">
          <div>
            <p class="label">Included packs</p>
            <h2>Public downloads for this use case</h2>
          </div>
          <p>These files are generated by the scheduled Daily Shelf run and remain available without manual fulfillment.</p>
        </div>
        <div class="ledger">
          {rows}
        </div>
      </section>
    </main>
    <footer class="site-footer">
      <p>{esc(monetization.get("affiliate_disclosure", ""))}</p>
      <p>{policy_links(config, "../")}</p>
    </footer>
  </div>
</body>
</html>
"""
        (USE_CASES / f"{record['slug']}.html").write_text(html_content, encoding="utf-8")

    return {
        "ready": bool(records),
        "count": len(records),
        "index_path": "use-cases/index.html",
        "json_path": "use-cases/use-cases.json",
        "paths": [record["path"] for record in records],
        "branded_urls": [record["branded_url"] for record in records if record.get("branded_url")],
    }


def render_template_pages(config: dict[str, Any]) -> dict[str, Any]:
    TEMPLATES.mkdir(parents=True, exist_ok=True)
    manifests = read_manifests()
    records = template_records(config)
    monetization = config["monetization"]
    store_url = str(monetization.get("store_url") or "").strip()
    support_url = str(monetization.get("support_url") or "").strip()
    general_support_url = branded_url(config, "support") or pack_url(config, "support.html")
    destination_note = (
        "Product checkout is connected through the configured external store."
        if store_url
        else (
            "Product checkout is not connected. Downloads remain public and support is voluntary through the connected support path."
            if support_url
            else "No external store, support, or affiliate destination is connected yet."
        )
    )

    template_export = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Daily Autodigital Shelf Templates",
        "description": "Evergreen template pages for the latest public Daily Autodigital Shelf digital pack in each template family.",
        "url": pack_url(config, "templates/"),
        "numberOfItems": len(records),
        "checkoutBoundary": destination_note,
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index + 1,
                "name": record["title"],
                "url": record["url"],
            }
            for index, record in enumerate(records)
        ],
        "items": records,
    }
    (TEMPLATES / "templates.json").write_text(json.dumps(template_export, indent=2), encoding="utf-8")

    first_cover = pack_url(config, manifests[0]["cover"]) if manifests else pack_url(config, "")
    index_url = pack_url(config, "templates/")
    index_cards = "\n".join(
        f"""<article class="pack-card">
          <span class="pack-date">{esc(record["date_label"])}</span>
          <h3>{esc(record["title"])} template</h3>
          <p>{esc(record["summary"])}</p>
          <div class="artifact-links">
            <a class="button primary" href="./{esc(record["slug"])}.html">Open template</a>
            <a class="button" href="../{esc(record["download_page_path"])}">Download page</a>
          </div>
        </article>"""
        for record in records
    )
    if not index_cards:
        index_cards = "<p>No templates generated yet.</p>"

    index_data = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Daily Autodigital Shelf Templates",
        "description": "Evergreen template landing pages for generated printable digital packs.",
        "url": index_url,
        "hasPart": [
            {
                "@type": "WebPage",
                "name": f"{record['title']} template",
                "url": record["url"],
            }
            for record in records
        ],
    }
    index_html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Templates | {esc(config["site"]["name"])}</title>
  <meta name="description" content="Evergreen template landing pages for Daily Autodigital Shelf printable digital packs.">
  <link rel="canonical" href="{esc(index_url)}">
{social_meta("Daily Autodigital Shelf Templates", "Evergreen template pages for generated printable digital packs.", index_url, first_cover, "Daily Autodigital Shelf templates")}
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
      <nav class="topnav" aria-label="Template navigation">
        <a href="../">Home</a>
        <a href="../archive.html">Archive</a>
        <a href="../topics/">Topics</a>
        <a href="../use-cases/">Use cases</a>
        <a href="../offers/">Offers</a>
        <a href="../support.html">Support</a>
      </nav>
    </header>
    <main>
      <section>
        <div class="section-head">
          <div>
            <p class="label">Templates</p>
            <h2>Evergreen landing pages for public digital packs</h2>
          </div>
          <p>Each template page keeps a stable URL while pointing to the newest dated pack, download page, ZIP, listing copy, and voluntary support route.</p>
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
    (TEMPLATES / "index.html").write_text(index_html, encoding="utf-8")

    for record in records:
        topic_links = " ".join(
            f"""<a class="topic-link" href="../topics/{esc(slug)}.html">{esc(TOPIC_DEFINITIONS[slug]["label"])}</a>"""
            for slug in record["topic_slugs"]
            if slug in TOPIC_DEFINITIONS
        )
        offer_links = " ".join(
            f"""<a class="button" href="../offers/{esc(slug)}.html">Open {esc(TOPIC_DEFINITIONS[slug]["label"])} offer</a>"""
            for slug in record["topic_slugs"]
            if slug in TOPIC_DEFINITIONS
        )
        offer_data: dict[str, Any] = {
            "@type": "Offer",
            "url": store_url or record["url"],
            "availability": "https://schema.org/InStock",
        }
        if store_url:
            offer_data["description"] = "External store checkout for this digital pack."
        else:
            offer_data.update(
                {
                    "price": "0.00",
                    "priceCurrency": "USD",
                    "description": "Public digital-pack download. Voluntary support is handled separately through Square.",
                }
            )
        page_data = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": ["CreativeWork", "Product"],
                    "name": f"{record['title']} template",
                    "description": record["summary"],
                    "url": record["url"],
                    "image": record["cover_url"],
                    "dateModified": record["date"],
                    "audience": {
                        "@type": "Audience",
                        "audienceType": record["buyer"],
                    },
                    "encoding": {
                        "@type": "MediaObject",
                        "contentUrl": record["download_url"],
                        "encodingFormat": "application/zip",
                        "name": f"{record['title']} ZIP",
                    },
                    "offers": {
                        **offer_data,
                    },
                    "potentialAction": [
                        {
                            "@type": "DownloadAction",
                            "target": record["download_url"],
                            "name": "Download ZIP",
                        },
                        {
                            "@type": "DonateAction",
                            "target": record["support_intent_url"] or general_support_url,
                            "name": "Support this template",
                        },
                    ],
                    "isPartOf": {
                        "@type": "WebSite",
                        "name": config["site"]["name"],
                        "url": pack_url(config, ""),
                    },
                },
                {
                    "@type": "WebPage",
                    "name": f"{record['title']} template landing page",
                    "description": f"Download, inspect, and optionally support the latest {record['title']} template pack.",
                    "url": record["url"],
                },
            ],
        }
        html_content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(record["title"])} Template | {esc(config["site"]["name"])}</title>
  <meta name="description" content="{esc(record["summary"])} Download the public template ZIP, inspect listing copy, or support the shelf.">
  <link rel="canonical" href="{esc(record["url"])}">
{social_meta(f"{record['title']} Template", record["summary"], record["url"], record["cover_url"], f"{record['title']} template")}
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
      <nav class="topnav" aria-label="Template page navigation">
        <a href="../">Home</a>
        <a href="./">Templates</a>
        <a href="../archive.html">Archive</a>
        <a href="../use-cases/">Use cases</a>
        <a href="../support.html">Support</a>
      </nav>
    </header>
    <main>
      <section class="hero">
        <div class="hero-copy">
          <p class="label">Template</p>
          <h1>{esc(record["title"])} template</h1>
          <p>{esc(record["summary"])}</p>
          <div class="actions">
            <a class="button primary" href="../{esc(record["download_page_path"])}">Download page</a>
            <a class="button" href="../{esc(record["download_path"])}">Download ZIP</a>
            <a class="button" href="../{esc(record["pack_path"])}">Open latest pack</a>
            <a class="button" href="../{esc(record["seller_copy_path"])}">Listing copy</a>
            <a class="button" href="{esc(record["support_intent_url"] or general_support_url)}">Support this template</a>
          </div>
          <p class="fineprint">{esc(destination_note)} This page is a stable discovery surface, not proof of revenue.</p>
        </div>
        <aside class="shelf-panel">
          <div class="panel-head">
            <div>
              <p class="label">Latest version</p>
              <h2>{esc(record["date_label"])}</h2>
            </div>
            <span class="status">Template</span>
          </div>
          <article class="artifact">
            <div>
              <h3>Who this helps</h3>
              <p>{esc(record["buyer"])}</p>
              <p class="topic-links">{topic_links}</p>
            </div>
          </article>
        </aside>
      </section>
      <section>
        <div class="section-head">
          <div>
            <p class="label">Unattended delivery</p>
            <h2>What this page connects</h2>
          </div>
          <p>The stable template URL points to the latest dated pack page, public download page, ZIP file, listing copy, topic pages, collection offers, and starter bundle.</p>
        </div>
        <div class="setup-list">
          <article class="setup-item done">
            <span class="setup-dot">1</span>
            <div>
              <strong>Inspect the pack</strong>
              <p><a href="../{esc(record["pack_path"])}">Open the latest generated pack page</a>.</p>
            </div>
          </article>
          <article class="setup-item done">
            <span class="setup-dot">2</span>
            <div>
              <strong>Download the file</strong>
              <p><a href="../{esc(record["download_page_path"])}">Download page</a> or <a href="../{esc(record["download_path"])}">Download ZIP</a>.</p>
            </div>
          </article>
          <article class="setup-item done">
            <span class="setup-dot">3</span>
            <div>
              <strong>Use or list it</strong>
              <p><a href="../{esc(record["seller_copy_path"])}">Listing copy</a> and the <a href="../store-import.html">store import kit</a> are ready for a future checkout platform.</p>
            </div>
          </article>
          <article class="setup-item">
            <span class="setup-dot">4</span>
            <div>
              <strong>Revenue boundary</strong>
              <p>Product checkout is not connected. Support is voluntary and routed through CalmSprout when selected.</p>
            </div>
          </article>
        </div>
      </section>
      <section>
        <div class="section-head">
          <div>
            <p class="label">Related offer paths</p>
            <h2>Bundles and collections</h2>
          </div>
          <p>These links make the template easier to discover and support without requiring manual fulfillment.</p>
        </div>
        <div class="actions">
          <a class="button primary" href="../{esc(record["starter_bundle_path"])}">Download starter bundle</a>
          <a class="button" href="../templates/templates.json">Templates JSON</a>
          <a class="button" href="{esc(record["support_page_url"])}">Open support page</a>
          {offer_links}
        </div>
      </section>
    </main>
    <footer class="site-footer">
      <p>{esc(monetization.get("affiliate_disclosure", ""))}</p>
      <p>{policy_links(config, "../")}</p>
    </footer>
  </div>
</body>
</html>
"""
        (TEMPLATES / f"{record['slug']}.html").write_text(html_content, encoding="utf-8")

    return {
        "ready": bool(records),
        "count": len(records),
        "index_path": "templates/index.html",
        "json_path": "templates/templates.json",
        "paths": [record["path"] for record in records],
        "branded_urls": [record["branded_url"] for record in records if record.get("branded_url")],
        "support_page_urls": [record["support_page_url"] for record in records if record.get("support_page_url")],
        "support_intent_urls": [record["support_intent_url"] for record in records if record.get("support_intent_url")],
    }


def render_guide_pages(config: dict[str, Any]) -> dict[str, Any]:
    GUIDES.mkdir(parents=True, exist_ok=True)
    records = template_records(config)
    monetization = config["monetization"]
    store_url = str(monetization.get("store_url") or "").strip()
    support_url = str(monetization.get("support_url") or "").strip()
    general_support_url = branded_url(config, "support") or pack_url(config, "support.html")
    destination_note = (
        "Product checkout is connected through the configured external store."
        if store_url
        else (
            "Product checkout is not connected. Downloads remain public and support is voluntary through the connected support path."
            if support_url
            else "No external store, support, or affiliate destination is connected yet."
        )
    )

    guide_records = []
    for record in records:
        path = f"guides/{record['slug']}.html"
        guide_records.append(
            {
                "slug": record["slug"],
                "id": record["id"],
                "date": record["date"],
                "date_label": record["date_label"],
                "title": f"How to use the {record['title']} template",
                "summary": f"A practical guide for using the public {record['title']} template without manual delivery or checkout friction.",
                "buyer": record.get("buyer", ""),
                "path": path,
                "url": pack_url(config, path),
                "branded_url": branded_url(config, path),
                "template_path": record["path"],
                "template_url": record["url"],
                "template_branded_url": record.get("branded_url", ""),
                "pack_path": record["pack_path"],
                "pack_url": record["pack_url"],
                "download_page_path": record["download_page_path"],
                "download_page_url": record["download_page_url"],
                "download_url": record["download_url"],
                "support_page_url": record["support_page_url"],
                "support_intent_url": record["support_intent_url"],
                "cover_url": record["cover_url"],
                "topic_slugs": record["topic_slugs"],
                "topic_urls": record["topic_urls"],
            }
        )

    guide_export = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Daily Autodigital Shelf Guides",
        "description": "Search-friendly how-to guides for public Daily Autodigital Shelf templates and downloads.",
        "url": pack_url(config, "guides/"),
        "numberOfItems": len(guide_records),
        "checkoutBoundary": destination_note,
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index + 1,
                "name": record["title"],
                "url": record["url"],
            }
            for index, record in enumerate(guide_records)
        ],
        "items": guide_records,
    }
    (GUIDES / "guides.json").write_text(json.dumps(guide_export, indent=2), encoding="utf-8")

    first_cover = guide_records[0]["cover_url"] if guide_records else pack_url(config, "")
    index_url = pack_url(config, "guides/")
    index_cards = "\n".join(
        f"""<article class="pack-card">
          <span class="pack-date">{esc(record["date_label"])}</span>
          <h3>{esc(record["title"])}</h3>
          <p>{esc(record["summary"])}</p>
          <div class="artifact-links">
            <a class="button primary" href="./{esc(record["slug"])}.html">Open guide</a>
            <a class="button" href="../{esc(record["template_path"])}">Template page</a>
            <a class="button" href="../{esc(record["download_page_path"])}">Download page</a>
          </div>
        </article>"""
        for record in guide_records
    )
    if not index_cards:
        index_cards = "<p>No guides generated yet.</p>"

    index_data = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Daily Autodigital Shelf Guides",
        "description": "Practical how-to guides for public generated templates and support-backed downloads.",
        "url": index_url,
        "hasPart": [
            {
                "@type": "WebPage",
                "name": record["title"],
                "url": record["url"],
            }
            for record in guide_records
        ],
    }
    index_html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Guides | {esc(config["site"]["name"])}</title>
  <meta name="description" content="How-to guides for Daily Autodigital Shelf printable templates, public downloads, and support-backed delivery.">
  <link rel="canonical" href="{esc(index_url)}">
{social_meta("Daily Autodigital Shelf Guides", "How-to guides for public generated templates and support-backed downloads.", index_url, first_cover, "Daily Autodigital Shelf guides")}
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
      <nav class="topnav" aria-label="Guide navigation">
        <a href="../">Home</a>
        <a href="../archive.html">Archive</a>
        <a href="../templates/">Templates</a>
        <a href="../use-cases/">Use cases</a>
        <a href="../offers/">Offers</a>
        <a href="../support.html">Support</a>
      </nav>
    </header>
    <main>
      <section>
        <div class="section-head">
          <div>
            <p class="label">Guides</p>
            <h2>How-to pages for public templates</h2>
          </div>
          <p>These pages turn each generated template into a practical search surface. Downloads stay public; support is voluntary unless a real product checkout is connected.</p>
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
    (GUIDES / "index.html").write_text(index_html, encoding="utf-8")

    for record in guide_records:
        topic_links = " ".join(
            f"""<a class="topic-link" href="../topics/{esc(slug)}.html">{esc(TOPIC_DEFINITIONS[slug]["label"])}</a>"""
            for slug in record["topic_slugs"]
            if slug in TOPIC_DEFINITIONS
        )
        steps = [
            {
                "name": "Open the template page",
                "text": f"Start with the stable {record['title'].removeprefix('How to use the ')} page so you can inspect the current public version before downloading.",
                "url": record["template_url"],
            },
            {
                "name": "Download the public file",
                "text": "Use the download page or ZIP link. Delivery is public, so no manual fulfillment is required.",
                "url": record["download_page_url"],
            },
            {
                "name": "Fill the worksheet in one pass",
                "text": "Complete the worksheet with plain facts and avoid adding fake testimonials, fake urgency, or unsupported claims.",
                "url": record["pack_url"],
            },
            {
                "name": "Use the checklist to finish",
                "text": "Check the included list before sharing, listing, or saving the finished work.",
                "url": record["pack_url"],
            },
            {
                "name": "Support the shelf if useful",
                "text": "If the template helps, use the support page. Product checkout remains disconnected unless status.json says otherwise.",
                "url": record["support_page_url"],
            },
        ]
        step_cards = "\n".join(
            f"""<article class="setup-item done">
            <span class="setup-dot">{index}</span>
            <div>
              <strong>{esc(step["name"])}</strong>
              <p>{esc(step["text"])} <a href="{esc(step["url"])}">Open link</a>.</p>
            </div>
          </article>"""
            for index, step in enumerate(steps, start=1)
        )
        faq_items = [
            {
                "question": f"Is this {record['title'].removeprefix('How to use the ')} guide a paid checkout?",
                "answer": "No. The guide and template download are public while product checkout remains disconnected.",
            },
            {
                "question": "How does this guide move the shelf closer to unattended revenue?",
                "answer": "It creates a search-friendly entry point that routes visitors to public downloads and voluntary CalmSprout support without manual fulfillment.",
            },
            {
                "question": "Does this page prove revenue?",
                "answer": "No. It improves discovery and conversion paths, but actual revenue is only proven by a real payment or connected checkout report.",
            },
        ]
        faq_sections = "\n".join(
            f"""<article class="artifact">
            <div>
              <h3>{esc(item["question"])}</h3>
              <p>{esc(item["answer"])}</p>
            </div>
          </article>"""
            for item in faq_items
        )
        page_data = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "HowTo",
                    "name": record["title"],
                    "description": record["summary"],
                    "image": record["cover_url"],
                    "url": record["url"],
                    "supply": [
                        {
                            "@type": "HowToSupply",
                            "name": "Public template ZIP",
                        }
                    ],
                    "tool": [
                        {
                            "@type": "HowToTool",
                            "name": "Daily Autodigital Shelf printable template",
                        }
                    ],
                    "step": [
                        {
                            "@type": "HowToStep",
                            "position": index,
                            "name": step["name"],
                            "text": step["text"],
                            "url": step["url"],
                        }
                        for index, step in enumerate(steps, start=1)
                    ],
                    "potentialAction": [
                        {
                            "@type": "DownloadAction",
                            "target": record["download_page_url"],
                            "name": "Download public template",
                        },
                        {
                            "@type": "DonateAction",
                            "target": record["support_intent_url"] or general_support_url,
                            "name": "Support this guide",
                        },
                    ],
                },
                {
                    "@type": "FAQPage",
                    "mainEntity": [
                        {
                            "@type": "Question",
                            "name": item["question"],
                            "acceptedAnswer": {
                                "@type": "Answer",
                                "text": item["answer"],
                            },
                        }
                        for item in faq_items
                    ],
                },
            ],
        }
        html_content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(record["title"])} | {esc(config["site"]["name"])}</title>
  <meta name="description" content="{esc(record["summary"])}">
  <link rel="canonical" href="{esc(record["url"])}">
{social_meta(record["title"], record["summary"], record["url"], record["cover_url"], record["title"], "article")}
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
      <nav class="topnav" aria-label="Guide page navigation">
        <a href="../">Home</a>
        <a href="./">Guides</a>
        <a href="../templates/">Templates</a>
        <a href="../offers/">Offers</a>
        <a href="../support.html">Support</a>
      </nav>
    </header>
    <main>
      <section class="hero">
        <div class="hero-copy">
          <p class="label">How-to guide</p>
          <h1>{esc(record["title"])}</h1>
          <p>{esc(record["summary"])}</p>
          <div class="actions">
            <a class="button primary" href="../{esc(record["download_page_path"])}">Download page</a>
            <a class="button" href="../{esc(record["template_path"])}">Template page</a>
            <a class="button" href="../{esc(record["pack_path"])}">Latest pack</a>
            <a class="button" href="{esc(record["support_page_url"])}">Support page</a>
          </div>
          <p class="fineprint">{esc(destination_note)} This guide is a discovery and support surface, not proof of revenue.</p>
        </div>
        <aside class="shelf-panel">
          <div class="panel-head">
            <div>
              <p class="label">Best fit</p>
              <h2>{esc(record["date_label"])}</h2>
            </div>
            <span class="status">Guide</span>
          </div>
          <article class="artifact">
            <div>
              <h3>Who this helps</h3>
              <p>{esc(record["buyer"])}</p>
              <p class="topic-links">{topic_links}</p>
            </div>
          </article>
        </aside>
      </section>
      <section>
        <div class="section-head">
          <div>
            <p class="label">Use path</p>
            <h2>Five steps, no manual delivery</h2>
          </div>
          <p>The page points to public files and measured support routes, so the system can keep serving visitors even when nobody is at the PC.</p>
        </div>
        <div class="setup-list">
          {step_cards}
        </div>
      </section>
      <section>
        <div class="section-head">
          <div>
            <p class="label">Boundary</p>
            <h2>What this page does and does not prove</h2>
          </div>
          <p>Guides are traffic and conversion infrastructure. They do not claim income, collect payment credentials, or move funds.</p>
        </div>
        <div class="pack-grid">
          {faq_sections}
        </div>
      </section>
    </main>
    <footer class="site-footer">
      <p>{esc(monetization.get("affiliate_disclosure", ""))}</p>
      <p>{policy_links(config, "../")}</p>
    </footer>
  </div>
</body>
</html>
"""
        (GUIDES / f"{record['slug']}.html").write_text(html_content, encoding="utf-8")

    return {
        "ready": bool(guide_records),
        "count": len(guide_records),
        "index_path": "guides/index.html",
        "json_path": "guides/guides.json",
        "paths": [record["path"] for record in guide_records],
        "branded_urls": [record["branded_url"] for record in guide_records if record.get("branded_url")],
    }


def render_offer_pages(config: dict[str, Any], support: dict[str, Any]) -> dict[str, Any]:
    OFFERS.mkdir(parents=True, exist_ok=True)
    manifests = read_manifests()
    topics = topic_index(manifests, config)
    monetization = config["monetization"]
    store_url = str(monetization.get("store_url") or "").strip()
    support_url = str(monetization.get("support_url") or "").strip()
    destination_url = store_url or support_url
    destination_type = "store" if store_url else ("support" if support_url else "none")
    cta_label = "Open product checkout" if store_url else "Support this collection"
    destination_note = (
        "This collection has a connected product checkout."
        if store_url
        else (
            "This collection uses a voluntary Square-hosted support path. Product checkout is not connected."
            if support_url
            else "No external store, support, or affiliate destination is connected yet."
        )
    )

    offer_records = []
    for slug, items in topics.items():
        topic = TOPIC_DEFINITIONS[slug]
        page_path = f"offers/{slug}.html"
        collection_bundle = write_collection_bundle(config, slug, topic, items)
        collection_support_url = branded_collection_support_url(config, slug)
        action_url = store_url or collection_support_url or support_url
        offer_records.append(
            {
                "slug": slug,
                "label": topic["label"],
                "description": topic["description"],
                "path": page_path,
                "url": pack_url(config, page_path),
                "count": len(items),
                "support_url": action_url,
                "branded_support_intent_url": collection_support_url,
                "external_support_destination": support_url,
                "destination_type": destination_type,
                "collection_bundle_url": collection_bundle["url"],
                "collection_bundle_path": collection_bundle["path"],
                "collection_bundle_bytes": collection_bundle["bytes"],
                "starter_bundle_url": pack_url(config, "bundles/starter-archive.zip"),
                "topic_url": pack_url(config, f"topics/{slug}.html"),
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
        )

    (OFFERS / "offers.json").write_text(json.dumps({"offers": offer_records}, indent=2), encoding="utf-8")

    first_cover = pack_url(config, manifests[0]["cover"]) if manifests else pack_url(config, "")
    index_url = pack_url(config, "offers/")
    index_cards = "\n".join(
        f"""<article class="pack-card">
          <span class="pack-date">{record["count"]} packs</span>
          <h3>{esc(record["label"])}</h3>
          <p>{esc(record["description"])}</p>
          <a class="button primary" href="./{esc(record["slug"])}.html">Open offer</a>
        </article>"""
        for record in offer_records
    )
    if not index_cards:
        index_cards = "<p>No offers generated yet.</p>"

    index_data = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Daily Autodigital Shelf Offers",
        "description": "Support-backed collection pages for generated printable pack bundles.",
        "url": index_url,
        "hasPart": [
            {
                "@type": "CollectionPage",
                "name": record["label"],
                "url": record["url"],
            }
            for record in offer_records
        ],
    }
    index_html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Offers | {esc(config["site"]["name"])}</title>
  <meta name="description" content="Support-backed collection offers for generated Daily Autodigital Shelf digital packs.">
  <link rel="canonical" href="{esc(index_url)}">
{social_meta("Daily Autodigital Shelf Offers", "Support-backed collection offers for generated printable packs.", index_url, first_cover, "Daily Autodigital Shelf offers")}
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
      <nav class="topnav" aria-label="Offers navigation">
        <a href="../">Home</a>
        <a href="../support.html">Support</a>
        <a href="../pay-what-you-can.html">Pay what you can</a>
        <a href="../starter-bundle.html">Starter bundle</a>
        <a href="../archive.html">Archive</a>
        <a href="../terms.html">Policies</a>
      </nav>
    </header>
    <main>
      <section>
        <div class="section-head">
          <div>
            <p class="label">Offers</p>
            <h2>Collection pages for useful pack groups</h2>
          </div>
          <p>These pages turn the generated archive into clearer support-backed offers. Downloads remain public; support is voluntary unless a real store checkout is connected.</p>
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
    (OFFERS / "index.html").write_text(index_html, encoding="utf-8")

    for record in offer_records:
        items = topics[record["slug"]]
        page_url = record["url"]
        image_url = pack_url(config, items[0]["cover"])
        action_url = str(record.get("support_url") or destination_url)
        support_cta = (
            f"""<a class="button primary" href="{esc(action_url)}">{esc(cta_label)}</a>"""
            if action_url
            else """<a class="button primary" href="../support.html">Support destination not connected</a>"""
        )
        collection_bundle_path = str(record.get("collection_bundle_path") or "").strip("/")
        collection_bundle_url = str(record.get("collection_bundle_url") or pack_url(config, collection_bundle_path))
        collection_bundle_cta = (
            f"""<a class="button" href="../{esc(collection_bundle_path)}">Download collection bundle</a>"""
            if collection_bundle_path
            else ""
        )
        rows = "\n".join(
            f"""<article class="ledger-row">
          <strong>{esc(item["date_label"])}</strong>
          <p><a href="../{esc(item["path"])}">{esc(item["title"])}</a><br>{esc(item["summary"])}</p>
          <div class="row-actions">
            <a class="button" href="../{esc(pack_download_page_path(item))}">Download page</a>
            <a class="button" href="../{esc(item.get("seller_copy", item["path"]))}">Listing copy</a>
          </div>
        </article>"""
            for item in items
        )
        page_data: dict[str, Any] = {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": f"{record['label']} Printable Pack Collection",
            "description": record["description"],
            "url": page_url,
            "isPartOf": {
                "@type": "WebSite",
                "name": config["site"]["name"],
                "url": pack_url(config, ""),
            },
            "hasPart": [
                {
                    "@type": "CreativeWork",
                    "name": item["title"],
                    "description": item["summary"],
                    "url": pack_url(config, item["path"]),
                    "encoding": {
                        "@type": "MediaObject",
                        "contentUrl": pack_url(config, pack_download_path(item)),
                        "encodingFormat": "application/zip",
                    },
                }
                for item in items[:50]
            ],
            "encoding": {
                "@type": "MediaObject",
                "contentUrl": collection_bundle_url,
                "encodingFormat": "application/zip",
                "name": f"{record['label']} collection bundle ZIP",
            },
        }
        if destination_url:
            page_data["potentialAction"] = {
                "@type": "BuyAction" if store_url else "DonateAction",
                "target": action_url,
                "name": cta_label,
            }

        html_content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(record["label"])} Offer | {esc(config["site"]["name"])}</title>
  <meta name="description" content="{esc(record["description"])}">
  <link rel="canonical" href="{esc(page_url)}">
{social_meta(f"{record['label']} Printable Pack Collection", record["description"], page_url, image_url, f"{record['label']} offer")}
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
      <nav class="topnav" aria-label="Offer navigation">
        <a href="../">Home</a>
        <a href="./">Offers</a>
        <a href="../support.html">Support</a>
        <a href="../pay-what-you-can.html">Pay what you can</a>
        <a href="../topics/{esc(record["slug"])}.html">Topic</a>
        <a href="../starter-bundle.html">Starter bundle</a>
      </nav>
    </header>
    <main>
      <section class="hero">
        <div class="hero-copy">
          <p class="label">Collection offer</p>
          <h1>{esc(record["label"])} printable pack collection</h1>
          <p>{esc(record["description"])}</p>
          <div class="actions">
            {support_cta}
            {collection_bundle_cta}
            <a class="button" href="../bundles/starter-archive.zip">Download starter bundle</a>
            <a class="button" href="../topics/{esc(record["slug"])}.html">Browse topic</a>
          </div>
          <p class="fineprint">{esc(destination_note)} The pack downloads on this page remain public until store checkout is connected.</p>
        </div>
        <aside class="shelf-panel">
          <div class="panel-head">
            <div>
              <p class="label">Included collection</p>
              <h2>{record["count"]} packs</h2>
            </div>
            <span class="status">{esc(destination_type)}</span>
          </div>
          <article class="artifact">
            <div>
              <h3>What this offers</h3>
              <p>A focused landing page for one pack group, with public downloads, listing copy, and one clear support action.</p>
            </div>
          </article>
        </aside>
      </section>
      <section>
        <div class="section-head">
          <div>
            <p class="label">Included packs</p>
            <h2>Download or inspect each file</h2>
          </div>
          <p>Every row has a public ZIP and listing-copy file. This keeps delivery independent from support while checkout is not connected.</p>
        </div>
        <div class="ledger">
          {rows}
        </div>
      </section>
    </main>
    <footer class="site-footer">
      <p>{esc(monetization.get("affiliate_disclosure", ""))}</p>
      <p>{policy_links(config, "../")}</p>
    </footer>
  </div>
</body>
</html>
"""
        (OFFERS / f"{record['slug']}.html").write_text(html_content, encoding="utf-8")

    return {
        "ready": bool(offer_records),
        "count": len(offer_records),
        "index_path": "offers/index.html",
        "json_path": "offers/offers.json",
        "paths": [record["path"] for record in offer_records],
        "collection_bundle_paths": [
            record["collection_bundle_path"]
            for record in offer_records
            if record.get("collection_bundle_path")
        ],
        "collection_bundle_urls": [
            record["collection_bundle_url"]
            for record in offer_records
            if record.get("collection_bundle_url")
        ],
        "collection_bundle_count": len([record for record in offer_records if record.get("collection_bundle_path")]),
        "collection_bundle_bytes": sum(int(record.get("collection_bundle_bytes") or 0) for record in offer_records),
        "support_intent_urls": [
            record["branded_support_intent_url"]
            for record in offer_records
            if record.get("branded_support_intent_url")
        ],
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
            "See SUPPORT.txt for voluntary support URLs. Product checkout is not connected yet.",
            "",
            "Suggested listing position: starter printable archive for low-maintenance planning and operations worksheets.",
        ]
    )

    with zipfile.ZipFile(bundle_path, "w") as bundle:
        write_zip_entry(bundle, f"{zip_root}/README.txt", readme.encode("utf-8"))
        write_zip_entry(bundle, f"{zip_root}/SUPPORT.txt", starter_support_card_text(manifests, config).encode("utf-8"))
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
            <a class="button" href="./{esc(pack_download_page_path(item))}">Download page</a>
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
        <a href="./use-cases/">Use cases</a>
        <a href="./templates/">Templates</a>
        <a href="./guides/">Guides</a>
        <a href="./offers/">Offers</a>
        <a href="./commercial-use.html">Commercial use</a>
        <a href="./sponsor.html">Sponsor</a>
        <a href="./support.html">Support</a>
        <a href="./pay-what-you-can.html">Pay what you can</a>
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
              <a class="button" href="./pay-what-you-can.html">Support the bundle</a>
              <a class="button" href="./use-cases/">Browse use cases</a>
              <a class="button" href="./templates/">Browse templates</a>
              <a class="button" href="./guides/">Browse guides</a>
              <a class="button" href="./commercial-use.html">Commercial use</a>
              <a class="button" href="./sponsor.html">Sponsor</a>
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
  <link rel="alternate" type="application/json" title="{esc(config["site"]["name"])} support funnel feed" href="./support-funnel.json">
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
        <a href="./use-cases/">Use cases</a>
        <a href="./templates/">Templates</a>
        <a href="./guides/">Guides</a>
        <a href="./{esc(bundle_page_path)}">Starter bundle</a>
        <a href="./offers/">Offers</a>
        <a href="./commercial-use.html">Commercial use</a>
        <a href="./sponsor.html">Sponsor</a>
        <a href="./support.html">Support</a>
        <a href="./pay-what-you-can.html">Pay what you can</a>
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
            <a class="button" href="./pay-what-you-can.html">Pay what you can</a>
            <a class="button" href="./use-cases/">Browse use cases</a>
            <a class="button" href="./templates/">Browse templates</a>
            <a class="button" href="./guides/">Browse guides</a>
            <a class="button" href="./{esc(bundle_page_path)}">Open starter bundle</a>
            <a class="button" href="./commercial-use.html">Commercial use</a>
            <a class="button" href="./sponsor.html">Sponsor</a>
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
                <a class="button" href="./downloads/{esc(today_pack["pack_slug"])}.html">Download pack</a>
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
          <p>{esc(recent_monetization_note)} <a href="./archive.html">Open archive</a> - <a href="./topics/">Topics</a> - <a href="./use-cases/">Use cases</a> - <a href="./templates/">Templates</a> - <a href="./guides/">Guides</a> - <a href="./offers/">Offers</a> - <a href="./{esc(bundle_page_path)}">Starter bundle</a> - <a href="./support.html">Support</a> - <a href="./store-import.html">Import kit</a> - <a href="./terms.html">Policies</a> - <a href="./catalog.csv">Catalog CSV</a> - <a href="./catalog.json">Catalog JSON</a> - <a href="./product-feed.json">Product feed</a> - <a href="./support-funnel.json">Support funnel feed</a></p>
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
              <a class="button" href="./pay-what-you-can.html">Pay what you can</a>
              <a class="button" href="./offers/">Offer pages</a>
              <a class="button" href="./use-cases/">Use cases</a>
              <a class="button" href="./templates/">Templates</a>
              <a class="button" href="./guides/">Guides</a>
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
    monetization = config["monetization"]
    store_url = str(monetization.get("store_url") or "")
    support_url = str(monetization.get("support_url") or "")
    destination_url = store_url or support_url
    destination_type = "store" if store_url else ("support" if support_url else "none")
    support_page_url = pack_url(config, "support.html")
    pay_what_you_can_url = pack_url(config, "pay-what-you-can.html")
    for item in manifests:
        branded_urls = branded_product_urls(config, item)
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
                "download_page_url": pack_url(config, pack_download_page_path(item)),
                "starter_bundle_url": pack_url(config, "bundles/starter-archive.zip"),
                "support_page_url": support_page_url,
                "pay_what_you_can_url": pay_what_you_can_url,
                **branded_urls,
                "monetization_destination_type": destination_type,
                "monetization_destination_url": destination_url,
                "store_connected": bool(store_url),
                "support_connected": bool(support_url),
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
        "download_page_url",
        "starter_bundle_url",
        "support_page_url",
        "pay_what_you_can_url",
        "branded_product_url",
        "branded_support_url",
        "branded_support_intent_url",
        "monetization_destination_type",
        "monetization_destination_url",
        "store_connected",
        "support_connected",
        "topic_urls",
        "tags",
        "monetization_enabled",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(catalog_items)


def render_product_feed(config: dict[str, Any]) -> dict[str, Any]:
    manifests = read_manifests()
    monetization = config["monetization"]
    store_connected = bool(str(monetization.get("store_url") or ""))
    support_connected = bool(str(monetization.get("support_url") or ""))
    checkout_boundary = (
        "Product checkout is connected through the configured external store."
        if store_connected
        else "Product checkout is not connected. Downloads remain public and support is voluntary."
    )
    generated_from = manifests[0]["date"] if manifests else "2026-01-01"
    rows: list[dict[str, Any]] = []
    for item in manifests:
        branded_urls = branded_product_urls(config, item)
        rows.append(
            {
                "id": item["id"],
                "date": item["date"],
                "title": item["title"],
                "description": item["summary"],
                "buyer": item.get("buyer", ""),
                "url": pack_url(config, item["path"]),
                "download_page_url": pack_url(config, pack_download_page_path(item)),
                "download_url": pack_url(config, pack_download_path(item)),
                "cover_url": pack_url(config, item["cover"]),
                "seller_copy_url": pack_url(config, item.get("seller_copy", "")),
                "support_page_url": pack_url(config, "support.html"),
                "pay_what_you_can_url": pack_url(config, "pay-what-you-can.html"),
                **branded_urls,
                "price_hint": config["generation"].get("default_price_hint", "$3 to $9 digital pack"),
                "currency": "USD",
                "store_connected": store_connected,
                "support_connected": support_connected,
                "is_accessible_for_free": True,
                "fulfillment": "public digital download",
                "checkout_boundary": checkout_boundary,
                "tags": listing_keywords(item),
            }
        )

    json_rel_path = "product-feed.json"
    xml_rel_path = "product-feed.xml"
    csv_rel_path = "product-feed.csv"
    feed_url = pack_url(config, json_rel_path)
    feed = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": f"{config['site']['name']} Product Feed",
        "url": feed_url,
        "dateModified": generated_from,
        "numberOfItems": len(rows),
        "checkoutBoundary": checkout_boundary,
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index + 1,
                "item": {
                    "@type": ["CreativeWork", "Product"],
                    "identifier": row["id"],
                    "name": row["title"],
                    "description": row["description"],
                    "url": row["url"],
                    "image": row["cover_url"],
                    "isAccessibleForFree": True,
                    "offers": {
                        "@type": "Offer",
                        "url": row["download_page_url"],
                        "price": "0.00",
                        "priceCurrency": row["currency"],
                        "availability": "https://schema.org/InStock",
                        "description": checkout_boundary,
                    },
                    "potentialAction": {
                        "@type": "DonateAction",
                        "target": row["branded_support_intent_url"],
                        "name": "Support this pack",
                    },
                    "downloadUrl": row["download_url"],
                    "sameAs": [
                        row["download_page_url"],
                        row["branded_product_url"],
                        row["branded_support_url"],
                    ],
                },
            }
            for index, row in enumerate(rows)
        ],
        "items": rows,
    }
    (DOCS / json_rel_path).write_text(json.dumps(feed, indent=2), encoding="utf-8")

    xml_rows = "\n".join(
        f"""  <product>
    <id>{esc(row["id"])}</id>
    <date>{esc(row["date"])}</date>
    <title>{esc(row["title"])}</title>
    <description>{esc(row["description"])}</description>
    <buyer>{esc(row["buyer"])}</buyer>
    <url>{esc(row["url"])}</url>
    <downloadPageUrl>{esc(row["download_page_url"])}</downloadPageUrl>
    <downloadUrl>{esc(row["download_url"])}</downloadUrl>
    <coverUrl>{esc(row["cover_url"])}</coverUrl>
    <sellerCopyUrl>{esc(row["seller_copy_url"])}</sellerCopyUrl>
    <supportPageUrl>{esc(row["support_page_url"])}</supportPageUrl>
    <brandedProductUrl>{esc(row["branded_product_url"])}</brandedProductUrl>
    <brandedSupportUrl>{esc(row["branded_support_url"])}</brandedSupportUrl>
    <brandedSupportIntentUrl>{esc(row["branded_support_intent_url"])}</brandedSupportIntentUrl>
    <priceHint>{esc(row["price_hint"])}</priceHint>
    <currency>{esc(row["currency"])}</currency>
    <storeConnected>{str(row["store_connected"]).lower()}</storeConnected>
    <supportConnected>{str(row["support_connected"]).lower()}</supportConnected>
    <isAccessibleForFree>true</isAccessibleForFree>
    <fulfillment>{esc(row["fulfillment"])}</fulfillment>
    <checkoutBoundary>{esc(row["checkout_boundary"])}</checkoutBoundary>
    <tags>{esc(row["tags"])}</tags>
  </product>"""
        for row in rows
    )
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<productFeed>
  <name>{esc(config["site"]["name"])} Product Feed</name>
  <url>{esc(feed_url)}</url>
  <dateModified>{esc(generated_from)}</dateModified>
  <numberOfItems>{len(rows)}</numberOfItems>
  <checkoutBoundary>{esc(checkout_boundary)}</checkoutBoundary>
{xml_rows}
</productFeed>
"""
    (DOCS / xml_rel_path).write_text(xml, encoding="utf-8")

    fieldnames = [
        "id",
        "date",
        "title",
        "description",
        "buyer",
        "url",
        "download_page_url",
        "download_url",
        "cover_url",
        "seller_copy_url",
        "support_page_url",
        "pay_what_you_can_url",
        "branded_product_url",
        "branded_support_url",
        "branded_support_intent_url",
        "price_hint",
        "currency",
        "store_connected",
        "support_connected",
        "is_accessible_for_free",
        "fulfillment",
        "checkout_boundary",
        "tags",
    ]
    with (DOCS / csv_rel_path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    return {
        "ready": True,
        "json_path": json_rel_path,
        "xml_path": xml_rel_path,
        "csv_path": csv_rel_path,
        "count": len(rows),
    }


def render_support_funnel_feed(config: dict[str, Any]) -> dict[str, Any]:
    manifests = read_manifests()
    monetization = config["monetization"]
    store_connected = bool(str(monetization.get("store_url") or ""))
    support_url = str(monetization.get("support_url") or "").strip()
    support_connected = bool(support_url)
    checkout_boundary = (
        "Product checkout is connected through the configured external store."
        if store_connected
        else "Product checkout is not connected. Downloads remain public and support is voluntary."
    )
    tier_summary = " | ".join(
        f"{tier['amount']} {tier['label']}: {tier['description']}"
        for tier in support_tiers(config)
    )
    generated_from = manifests[0]["date"] if manifests else "2026-01-01"
    rows: list[dict[str, Any]] = []
    for item in manifests:
        branded_urls = branded_product_urls(config, item)
        slug = pack_slug_from_manifest(item)
        rows.append(
            {
                "id": item["id"],
                "date": item["date"],
                "title": item["title"],
                "description": item["summary"],
                "buyer": item.get("buyer", ""),
                "product_url": pack_url(config, item["path"]),
                "download_page_url": pack_url(config, pack_download_page_path(item)),
                "download_url": pack_url(config, pack_download_path(item)),
                "branded_product_url": branded_urls["branded_product_url"],
                "branded_support_url": branded_urls["branded_support_url"],
                "branded_support_intent_url": branded_urls["branded_support_intent_url"],
                "public_support_page_url": pack_url(config, "support.html"),
                "pay_what_you_can_url": pack_url(config, "pay-what-you-can.html"),
                "external_support_destination": support_url,
                "utm_source": "calmsprout",
                "utm_medium": "daily_shelf",
                "utm_campaign": "product_support",
                "utm_content": slug,
                "suggested_support_tiers": tier_summary,
                "support_connected": support_connected,
                "store_connected": store_connected,
                "fulfillment": "public digital download with voluntary external support",
                "checkout_boundary": checkout_boundary,
            }
        )

    json_rel_path = "support-funnel.json"
    xml_rel_path = "support-funnel.xml"
    csv_rel_path = "support-funnel.csv"
    feed_url = pack_url(config, json_rel_path)
    feed = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": f"{config['site']['name']} Support Funnel Feed",
        "url": feed_url,
        "dateModified": generated_from,
        "numberOfItems": len(rows),
        "supportConnected": support_connected,
        "checkoutBoundary": checkout_boundary,
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index + 1,
                "item": {
                    "@type": ["CreativeWork", "Product"],
                    "identifier": row["id"],
                    "name": row["title"],
                    "description": row["description"],
                    "url": row["branded_product_url"],
                    "isAccessibleForFree": True,
                    "potentialAction": [
                        {
                            "@type": "DownloadAction",
                            "target": row["download_page_url"],
                            "name": "Download public pack",
                        },
                        {
                            "@type": "DonateAction",
                            "target": row["branded_support_intent_url"],
                            "name": "Support this pack",
                            "description": checkout_boundary,
                        },
                    ],
                    "sameAs": [
                        row["product_url"],
                        row["download_page_url"],
                        row["branded_support_url"],
                    ],
                },
            }
            for index, row in enumerate(rows)
        ],
        "items": rows,
    }
    (DOCS / json_rel_path).write_text(json.dumps(feed, indent=2), encoding="utf-8")

    xml_rows = "\n".join(
        f"""  <supportFunnel>
    <id>{esc(row["id"])}</id>
    <date>{esc(row["date"])}</date>
    <title>{esc(row["title"])}</title>
    <description>{esc(row["description"])}</description>
    <buyer>{esc(row["buyer"])}</buyer>
    <productUrl>{esc(row["product_url"])}</productUrl>
    <downloadPageUrl>{esc(row["download_page_url"])}</downloadPageUrl>
    <downloadUrl>{esc(row["download_url"])}</downloadUrl>
    <brandedProductUrl>{esc(row["branded_product_url"])}</brandedProductUrl>
    <brandedSupportUrl>{esc(row["branded_support_url"])}</brandedSupportUrl>
    <brandedSupportIntentUrl>{esc(row["branded_support_intent_url"])}</brandedSupportIntentUrl>
    <publicSupportPageUrl>{esc(row["public_support_page_url"])}</publicSupportPageUrl>
    <payWhatYouCanUrl>{esc(row["pay_what_you_can_url"])}</payWhatYouCanUrl>
    <externalSupportDestination>{esc(row["external_support_destination"])}</externalSupportDestination>
    <utmSource>{esc(row["utm_source"])}</utmSource>
    <utmMedium>{esc(row["utm_medium"])}</utmMedium>
    <utmCampaign>{esc(row["utm_campaign"])}</utmCampaign>
    <utmContent>{esc(row["utm_content"])}</utmContent>
    <suggestedSupportTiers>{esc(row["suggested_support_tiers"])}</suggestedSupportTiers>
    <supportConnected>{str(row["support_connected"]).lower()}</supportConnected>
    <storeConnected>{str(row["store_connected"]).lower()}</storeConnected>
    <fulfillment>{esc(row["fulfillment"])}</fulfillment>
    <checkoutBoundary>{esc(row["checkout_boundary"])}</checkoutBoundary>
  </supportFunnel>"""
        for row in rows
    )
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<supportFunnelFeed>
  <name>{esc(config["site"]["name"])} Support Funnel Feed</name>
  <url>{esc(feed_url)}</url>
  <dateModified>{esc(generated_from)}</dateModified>
  <numberOfItems>{len(rows)}</numberOfItems>
  <supportConnected>{str(support_connected).lower()}</supportConnected>
  <checkoutBoundary>{esc(checkout_boundary)}</checkoutBoundary>
{xml_rows}
</supportFunnelFeed>
"""
    (DOCS / xml_rel_path).write_text(xml, encoding="utf-8")

    fieldnames = [
        "id",
        "date",
        "title",
        "description",
        "buyer",
        "product_url",
        "download_page_url",
        "download_url",
        "branded_product_url",
        "branded_support_url",
        "branded_support_intent_url",
        "public_support_page_url",
        "pay_what_you_can_url",
        "external_support_destination",
        "utm_source",
        "utm_medium",
        "utm_campaign",
        "utm_content",
        "suggested_support_tiers",
        "support_connected",
        "store_connected",
        "fulfillment",
        "checkout_boundary",
    ]
    with (DOCS / csv_rel_path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    return {
        "ready": True,
        "json_path": json_rel_path,
        "xml_path": xml_rel_path,
        "csv_path": csv_rel_path,
        "count": len(rows),
    }


def render_archive(config: dict[str, Any]) -> None:
    manifests = read_manifests()
    rows = "\n".join(
        f"""<article class="ledger-row">
          <strong>{esc(item["date_label"])}</strong>
          <p><a href="./{esc(item["path"])}">{esc(item["title"])}</a><br>{esc(item["summary"])}</p>
          <div class="row-actions">
            <a class="button" href="./{esc(item.get("seller_copy", item["path"]))}">Seller copy</a>
            <a class="button" href="./{esc(pack_download_page_path(item))}">Download page</a>
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
        <a href="./use-cases/">Use cases</a>
        <a href="./templates/">Templates</a>
        <a href="./starter-bundle.html">Starter bundle</a>
        <a href="./offers/">Offers</a>
        <a href="./commercial-use.html">Commercial use</a>
        <a href="./sponsor.html">Sponsor</a>
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
          <p>Each row has a public pack page, direct product ZIP, and store-ready listing copy. Topic pages group packs by use case, <a href="./use-cases/">buyer-intent use-case pages</a> make the archive easier to discover, <a href="./templates/">template pages</a> provide stable non-dated product URLs, <a href="./guides/">guide pages</a> add how-to search surfaces, <a href="./offers/">offer pages</a> make the collections easier to support, the <a href="./commercial-use.html">commercial-use page</a> and <a href="./sponsor.html">sponsor page</a> add an unattended support ladder, the <a href="./starter-bundle.html">starter bundle</a> packages the archive as one ZIP, the <a href="./store-import.html">import kit</a> packages marketplace listing metadata, and <a href="./terms.html">policy pages</a> prepare the shelf for future store review. Payment links remain off until a real store or support destination is connected.</p>
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
            <a class="button" href="./{esc(pack_download_page_path(item))}">Download page</a>
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
        <a href="./offers/">Offers</a>
        <a href="./starter-bundle.html">Starter bundle</a>
        <a href="./pay-what-you-can.html">Pay what you can</a>
        <a href="./commercial-use.html">Commercial use</a>
        <a href="./sponsor.html">Sponsor</a>
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
            <a class="button" href="./pay-what-you-can.html">Pay what you can</a>
            <a class="button" href="./commercial-use.html">Commercial use</a>
            <a class="button" href="./sponsor.html">Sponsor</a>
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


def support_tiers(config: dict[str, Any]) -> list[dict[str, str]]:
    raw_tiers = config["monetization"].get("support_tiers") or []
    tiers: list[dict[str, str]] = []
    for raw in raw_tiers:
        if not isinstance(raw, dict):
            continue
        label = str(raw.get("label") or "").strip()
        amount = str(raw.get("amount") or "").strip()
        description = str(raw.get("description") or "").strip()
        if not label or not amount:
            continue
        tiers.append(
            {
                "label": label,
                "amount": amount,
                "description": description or "Voluntary support for the generated shelf.",
            }
        )
    if tiers:
        return tiers
    return [
        {
            "label": "Small thank-you",
            "amount": "$3",
            "description": "A light support nudge for one useful worksheet.",
        },
        {
            "label": "Bundle supporter",
            "amount": "$9",
            "description": "A fair support level for the starter archive.",
        },
        {
            "label": "Keep it running",
            "amount": "$21",
            "description": "Helps keep daily publishing, hosting, and maintenance alive.",
        },
    ]


def render_pay_what_you_can_page(config: dict[str, Any], support: dict[str, Any]) -> dict[str, Any]:
    manifests = read_manifests()
    monetization = config["monetization"]
    destination_url = str(support.get("destination_url") or "").strip()
    destination_type = str(support.get("destination_type") or "none")
    connected = bool(destination_url)
    page_rel_path = "pay-what-you-can.html"
    page_url = pack_url(config, page_rel_path)
    home_url = pack_url(config, "")
    bundle_path = "bundles/starter-archive.zip"
    bundle_url = pack_url(config, bundle_path)
    image_url = pack_url(config, manifests[0]["cover"]) if manifests else home_url
    cta_label = "Open Square support page" if destination_type == "support" else "Open product checkout"
    primary_cta = (
        f"""<a class="button primary" href="{esc(destination_url)}">{esc(cta_label)}</a>"""
        if connected
        else """<a class="button primary" href="./#setup">Destination not connected</a>"""
    )
    tiers = support_tiers(config)
    tier_cards = "\n".join(
        f"""<article class="tier-card">
          <span class="tier-amount">{esc(tier["amount"])}</span>
          <h3>{esc(tier["label"])}</h3>
          <p>{esc(tier["description"])}</p>
          {primary_cta if index == 1 else f'<a class="button" href="{esc(destination_url or "./#setup")}">Choose this level</a>'}
        </article>"""
        for index, tier in enumerate(tiers)
    )
    pack_rows = "\n".join(
        f"""<article class="ledger-row">
          <strong>{esc(item["date_label"])}</strong>
          <p><a href="./{esc(item["path"])}">{esc(item["title"])}</a><br>{esc(item["summary"])}</p>
          <div class="row-actions">
            <a class="button" href="./{esc(pack_download_page_path(item))}">Download page</a>
            <a class="button" href="./{esc(item.get("seller_copy", item["path"]))}">Listing copy</a>
          </div>
        </article>"""
        for item in manifests[:5]
    )
    if not pack_rows:
        pack_rows = "<p>No packs generated yet.</p>"
    destination_note = (
        f"Support is handled by the external destination at {destination_url}."
        if connected
        else "No external support or store destination is connected yet."
    )
    structured_data: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "Pay What You Can Bundle",
        "description": "A voluntary support page for the Daily Autodigital Shelf starter archive.",
        "url": page_url,
        "isPartOf": {
            "@type": "WebSite",
            "name": config["site"]["name"],
            "url": home_url,
        },
        "about": {
            "@type": "CreativeWork",
            "name": "Daily Autodigital Shelf Starter Archive",
            "encoding": {
                "@type": "MediaObject",
                "contentUrl": bundle_url,
                "encodingFormat": "application/zip",
            },
        },
    }
    if connected:
        structured_data["potentialAction"] = {
            "@type": "DonateAction" if destination_type == "support" else "BuyAction",
            "target": destination_url,
            "name": cta_label,
        }

    content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Pay What You Can Bundle | {esc(config["site"]["name"])}</title>
  <meta name="description" content="Download the generated starter archive and support the Daily Autodigital Shelf through the connected external support path.">
  <link rel="canonical" href="{esc(page_url)}">
{social_meta("Pay What You Can Bundle", "Download the starter archive and optionally support the automated public shelf.", page_url, image_url, "Daily Autodigital Shelf pay what you can page")}
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
      <nav class="topnav" aria-label="Pay what you can navigation">
        <a href="./">Home</a>
        <a href="./starter-bundle.html">Starter bundle</a>
        <a href="./offers/">Offers</a>
        <a href="./support.html">Support</a>
        <a href="./terms.html">Policies</a>
      </nav>
    </header>
    <main>
      <section class="hero support-hero">
        <div class="hero-copy">
          <p class="label">Pay what you can</p>
          <h1>Download the starter archive. Support it if it helps.</h1>
          <p>The full starter ZIP stays public so delivery does not depend on manual handling. The connected support path can receive voluntary support automatically through the external provider.</p>
          <div class="actions">
            {primary_cta}
            <a class="button" href="./{esc(bundle_path)}">Download starter ZIP</a>
            <a class="button" href="./starter-bundle.html">Inspect bundle</a>
            <a class="button" href="./commercial-use.html">Commercial use</a>
            <a class="button" href="./sponsor.html">Sponsor</a>
          </div>
          <p class="fineprint">{esc(destination_note)} This is not product checkout unless store_connected is true in status.json.</p>
        </div>
        <aside class="shelf-panel">
          <div class="panel-head">
            <div>
              <p class="label">Generated value</p>
              <h2>{len(manifests)} packs</h2>
            </div>
            <span class="status">{esc(destination_type)}</span>
          </div>
          <article class="artifact">
            <div>
              <h3>What visitors get</h3>
              <p>A ZIP containing worksheets, checklists, cover SVGs, listing copy, catalog files, and policy pages. Support is voluntary while downloads remain public.</p>
            </div>
          </article>
        </aside>
      </section>
      <section>
        <div class="section-head">
          <div>
            <p class="label">Suggested support</p>
            <h2>Simple levels</h2>
          </div>
          <p>Each button routes to the same connected external support destination. Amount choice is handled there, not by this static site.</p>
        </div>
        <div class="tier-grid">
          {tier_cards}
        </div>
      </section>
      <section>
        <div class="section-head">
          <div>
            <p class="label">Preview files</p>
            <h2>Recent packs inside the bundle</h2>
          </div>
          <p>Visitors can inspect the work before supporting it. This keeps the funnel clear, low-pressure, and fully unattended.</p>
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
        "connected": connected,
        "tier_count": len(tiers),
    }


def render_sponsor_pages(config: dict[str, Any]) -> dict[str, Any]:
    manifests = read_manifests()
    monetization = config["monetization"]
    support_url = str(monetization.get("support_url") or "").strip()
    general_support_intent_url = branded_url(config, "support/go") or support_url
    sponsor_support_intent_url = branded_url(config, "sponsor/support/go") or general_support_intent_url
    commercial_support_intent_url = branded_url(config, "commercial-use/support/go") or general_support_intent_url
    sponsor_page_path = "sponsor.html"
    commercial_page_path = "commercial-use.html"
    kit_path = "sponsor-kit.json"
    sponsor_url = pack_url(config, sponsor_page_path)
    commercial_url = pack_url(config, commercial_page_path)
    image_url = pack_url(config, manifests[0]["cover"]) if manifests else pack_url(config, "")
    tiers = list(monetization.get("support_tiers", []))
    sponsor_tiers = [
        *tiers,
        {
            "label": "Commercial-use supporter",
            "amount": "$49",
            "description": "A practical support level for a small team using the worksheets internally.",
        },
        {
            "label": "Shelf sponsor",
            "amount": "$99",
            "description": "A stronger contribution for keeping the unattended public shelf online.",
        },
    ]
    checkout_boundary = (
        "Product checkout is not connected. Downloads remain public and support is voluntary through the connected support path."
        if support_url
        else "No external store, support, or affiliate destination is connected yet."
    )
    def support_cta(intent_url: str, label: str = "Open support page") -> str:
        if intent_url:
            return f"""<a class="button primary" href="{esc(intent_url)}">{esc(label)}</a>"""
        return """<a class="button primary" href="./support.html">Open support page</a>"""

    def tier_cards_for(intent_url: str) -> str:
        return "\n".join(
            f"""<article class="tier-card">
          <span class="tier-amount">{esc(tier.get("amount", ""))}</span>
          <h3>{esc(tier.get("label", "Support level"))}</h3>
          <p>{esc(tier.get("description", ""))}</p>
          {support_cta(intent_url)}
        </article>"""
            for tier in sponsor_tiers
        )
    recent_rows = "\n".join(
        f"""<article class="ledger-row">
          <strong>{esc(item["date_label"])}</strong>
          <p><a href="./{esc(item["path"])}">{esc(item["title"])}</a><br>{esc(item["summary"])}</p>
          <div class="row-actions">
            <a class="button" href="./{esc(template_page_path(item))}">Template</a>
            <a class="button" href="./{esc(guide_page_path(item))}">Guide</a>
            <a class="button" href="./{esc(pack_download_page_path(item))}">Download page</a>
          </div>
        </article>"""
        for item in manifests[:6]
    )
    if not recent_rows:
        recent_rows = "<p>No packs generated yet.</p>"

    sponsor_graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "name": "Sponsor Daily Autodigital Shelf",
                "description": "Sponsor and voluntary support page for an unattended public worksheet shelf.",
                "url": sponsor_url,
                "isPartOf": {
                    "@type": "WebSite",
                    "name": config["site"]["name"],
                    "url": pack_url(config, ""),
                },
                "potentialAction": {
                    "@type": "DonateAction",
                    "target": sponsor_support_intent_url,
                    "name": "Support the shelf",
                },
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": "Does sponsoring create a private order or manual fulfillment promise?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "No. The downloads remain public and unattended. Support helps keep the automated shelf online.",
                        },
                    },
                    {
                        "@type": "Question",
                        "name": "Is product checkout connected?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": checkout_boundary,
                        },
                    },
                ],
            },
        ],
    }
    commercial_graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "name": "Commercial Use Support",
                "description": "Commercial and internal-use support page for Daily Autodigital Shelf templates.",
                "url": commercial_url,
                "isPartOf": {
                    "@type": "WebSite",
                    "name": config["site"]["name"],
                    "url": pack_url(config, ""),
                },
                "potentialAction": {
                    "@type": "DonateAction",
                    "target": commercial_support_intent_url,
                    "name": "Support commercial use",
                },
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": "Can a team use these templates internally?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Yes. The plain license allows personal and internal business use. The files themselves should not be resold, redistributed, or claimed as original work.",
                        },
                    },
                    {
                        "@type": "Question",
                        "name": "Is support required for commercial use?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Support is voluntary while product checkout is disconnected. The commercial-use page exists to give teams a clear unattended support path.",
                        },
                    },
                ],
            },
        ],
    }
    sponsor_kit = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Daily Autodigital Shelf Sponsor Kit",
        "description": "Machine-readable sponsor and commercial-use support metadata for Daily Autodigital Shelf.",
        "url": sponsor_url,
        "branded_url": branded_url(config, "sponsor"),
        "commercial_use_url": commercial_url,
        "branded_commercial_use_url": branded_url(config, "commercial-use"),
        "support_intent_url": sponsor_support_intent_url,
        "sponsor_support_intent_url": sponsor_support_intent_url,
        "commercial_support_intent_url": commercial_support_intent_url,
        "general_support_intent_url": general_support_intent_url,
        "checkout_boundary": checkout_boundary,
        "support_connected": bool(support_url),
        "store_connected": bool(monetization.get("store_url")),
        "numberOfItems": len(sponsor_tiers),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index + 1,
                "name": tier.get("label", "Support level"),
                "description": tier.get("description", ""),
                "url": sponsor_support_intent_url,
            }
            for index, tier in enumerate(sponsor_tiers)
        ],
        "items": sponsor_tiers,
    }
    (DOCS / kit_path).write_text(json.dumps(sponsor_kit, indent=2), encoding="utf-8")

    sponsor_html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Sponsor Daily Autodigital Shelf | {esc(config["site"]["name"])}</title>
  <meta name="description" content="Sponsor the unattended Daily Autodigital Shelf public worksheet library through the connected support path.">
  <link rel="canonical" href="{esc(sponsor_url)}">
{social_meta("Sponsor Daily Autodigital Shelf", "Sponsor the unattended public worksheet shelf through the connected support path.", sponsor_url, image_url, "Daily Autodigital Shelf sponsor page")}
  <script type="application/ld+json">{json_for_script(sponsor_graph)}</script>
  <link rel="stylesheet" href="./styles.css">
</head>
<body>
  <div class="site-shell">
    <header class="topbar">
      <a class="brand" href="./">
        <span class="brand-mark">D</span>
        <span class="brand-name">{esc(config["site"]["name"])}</span>
      </a>
      <nav class="topnav" aria-label="Sponsor navigation">
        <a href="./">Home</a>
        <a href="./commercial-use.html">Commercial use</a>
        <a href="./starter-bundle.html">Starter bundle</a>
        <a href="./templates/">Templates</a>
        <a href="./guides/">Guides</a>
        <a href="./support.html">Support</a>
        <a href="./terms.html">Policies</a>
      </nav>
    </header>
    <main>
      <section class="hero support-hero">
        <div class="hero-copy">
          <p class="label">Sponsor</p>
          <h1>Sponsor the unattended public worksheet shelf.</h1>
          <p>Daily Autodigital Shelf publishes reusable worksheets, templates, guide pages, feeds, and bundles without manual delivery. Sponsorship is voluntary support through the connected external path.</p>
          <div class="actions">
            {support_cta(sponsor_support_intent_url)}
            <a class="button" href="./commercial-use.html">Commercial use terms</a>
            <a class="button" href="./sponsor-kit.json">Sponsor kit JSON</a>
            <a class="button" href="./bundles/starter-archive.zip">Download starter ZIP</a>
          </div>
          <p class="fineprint">{esc(checkout_boundary)} Sponsorship does not promise private fulfillment, paid placement, or revenue proof.</p>
        </div>
        <aside class="shelf-panel">
          <div class="panel-head">
            <div>
              <p class="label">Unattended output</p>
              <h2>{len(manifests)} packs</h2>
            </div>
            <span class="status">support</span>
          </div>
          <article class="artifact">
            <div>
              <h3>What support keeps running</h3>
              <p>Daily generation, public downloads, guide pages, template pages, collection bundles, metadata feeds, and search submission.</p>
            </div>
          </article>
        </aside>
      </section>
      <section>
        <div class="section-head">
          <div>
            <p class="label">Suggested support</p>
            <h2>Support ladder</h2>
          </div>
          <p>All buttons route to the connected support path. Amount selection happens externally, not on this static page.</p>
        </div>
        <div class="tier-grid">
          {tier_cards_for(sponsor_support_intent_url)}
        </div>
      </section>
      <section>
        <div class="section-head">
          <div>
            <p class="label">Proof of work</p>
            <h2>Recent generated assets</h2>
          </div>
          <p>These public files show what the support path keeps available without manual delivery.</p>
        </div>
        <div class="ledger">
          {recent_rows}
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
    (DOCS / sponsor_page_path).write_text(sponsor_html, encoding="utf-8")

    commercial_html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Commercial Use Support | {esc(config["site"]["name"])}</title>
  <meta name="description" content="Commercial and internal-use support page for Daily Autodigital Shelf public templates and guides.">
  <link rel="canonical" href="{esc(commercial_url)}">
{social_meta("Commercial Use Support", "Use Daily Autodigital Shelf templates internally and support the unattended public shelf.", commercial_url, image_url, "Daily Autodigital Shelf commercial use page")}
  <script type="application/ld+json">{json_for_script(commercial_graph)}</script>
  <link rel="stylesheet" href="./styles.css">
</head>
<body>
  <div class="site-shell">
    <header class="topbar">
      <a class="brand" href="./">
        <span class="brand-mark">D</span>
        <span class="brand-name">{esc(config["site"]["name"])}</span>
      </a>
      <nav class="topnav" aria-label="Commercial use navigation">
        <a href="./">Home</a>
        <a href="./sponsor.html">Sponsor</a>
        <a href="./license.html">License</a>
        <a href="./templates/">Templates</a>
        <a href="./guides/">Guides</a>
        <a href="./support.html">Support</a>
        <a href="./terms.html">Policies</a>
      </nav>
    </header>
    <main>
      <section class="hero support-hero">
        <div class="hero-copy">
          <p class="label">Commercial use</p>
          <h1>Use the templates internally. Support the shelf if they help.</h1>
          <p>The public license allows personal and internal business use. The files should not be resold, redistributed, uploaded as-is, or claimed as original work.</p>
          <div class="actions">
            {support_cta(commercial_support_intent_url)}
            <a class="button" href="./license.html">Read license</a>
            <a class="button" href="./templates/">Browse templates</a>
            <a class="button" href="./guides/">Browse guides</a>
          </div>
          <p class="fineprint">{esc(checkout_boundary)} Support is voluntary and handled by the external provider.</p>
        </div>
        <aside class="shelf-panel">
          <div class="panel-head">
            <div>
              <p class="label">Use boundary</p>
              <h2>Internal use</h2>
            </div>
            <span class="status">license</span>
          </div>
          <article class="artifact">
            <div>
              <h3>Allowed shape</h3>
              <p>Print or use the worksheets for household, team, client-call, and internal workflow operations. Do not resell or republish the generated files.</p>
            </div>
          </article>
        </aside>
      </section>
      <section>
        <div class="section-head">
          <div>
            <p class="label">Commercial support path</p>
            <h2>Suggested team support</h2>
          </div>
          <p>These suggested levels keep support unattended and low-friction while making the buyer-intent path explicit.</p>
        </div>
        <div class="tier-grid">
          {tier_cards_for(commercial_support_intent_url)}
        </div>
      </section>
      <section>
        <div class="section-head">
          <div>
            <p class="label">Useful starting points</p>
            <h2>Templates with guides</h2>
          </div>
          <p>Each item has a stable template page, guide page, and public download page.</p>
        </div>
        <div class="ledger">
          {recent_rows}
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
    (DOCS / commercial_page_path).write_text(commercial_html, encoding="utf-8")

    return {
        "ready": True,
        "sponsor_page": sponsor_page_path,
        "sponsor_page_url": sponsor_url,
        "sponsor_branded_url": branded_url(config, "sponsor"),
        "commercial_use_page": commercial_page_path,
        "commercial_use_page_url": commercial_url,
        "commercial_use_branded_url": branded_url(config, "commercial-use"),
        "kit_path": kit_path,
        "kit_url": pack_url(config, kit_path),
        "kit_branded_url": branded_url(config, "sponsor-kit.json"),
        "support_intent_url": sponsor_support_intent_url,
        "sponsor_support_intent_url": sponsor_support_intent_url,
        "commercial_support_intent_url": commercial_support_intent_url,
        "general_support_intent_url": general_support_intent_url,
        "tier_count": len(sponsor_tiers),
    }


def render_ai_discovery_files(config: dict[str, Any], support: dict[str, Any], pay_page: dict[str, Any], sponsor_pages: dict[str, Any]) -> dict[str, Any]:
    manifests = read_manifests()
    site_name = config["site"]["name"]
    base_url = pack_url(config, "")
    support_path = str(support.get("page_path", "support.html"))
    support_url = pack_url(config, support_path)
    pay_path = str(pay_page.get("page_path", "pay-what-you-can.html"))
    pay_url = pack_url(config, pay_path)
    sponsor_path = str(sponsor_pages.get("sponsor_page", "sponsor.html"))
    sponsor_url = pack_url(config, sponsor_path)
    commercial_use_path = str(sponsor_pages.get("commercial_use_page", "commercial-use.html"))
    commercial_use_url = pack_url(config, commercial_use_path)
    sponsor_kit_path = str(sponsor_pages.get("kit_path", "sponsor-kit.json"))
    sponsor_kit_url = pack_url(config, sponsor_kit_path)
    destination_type = str(support.get("destination_type", "none"))
    destination_url = str(support.get("destination_url", ""))
    latest = manifests[0] if manifests else None
    latest_branded_urls = branded_product_urls(config, latest) if latest else {}
    latest_line = (
        f"- Latest pack: [{latest['title']}]({pack_url(config, latest['path'])}) - {latest['summary']} Download page: {pack_url(config, pack_download_page_path(latest))}"
        if latest
        else "- Latest pack: none generated yet"
    )
    latest_branded_lines = []
    if latest_branded_urls.get("branded_product_url"):
        latest_branded_lines.extend(
            [
                f"- Branded latest product: {latest_branded_urls['branded_product_url']}",
                f"- Branded product support page: {latest_branded_urls['branded_support_url']}",
                f"- Branded support intent redirect: {latest_branded_urls['branded_support_intent_url']}",
            ]
        )
    pack_lines = "\n".join(
        f"- [{item['title']}]({pack_url(config, item['path'])}) - {item['summary']} Download page: {pack_url(config, pack_download_page_path(item))} ZIP: {pack_url(config, pack_download_path(item))}"
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
            f"- Pay what you can bundle: {pay_url}",
            f"- Sponsor page: {sponsor_url}",
            f"- Commercial use page: {commercial_use_url}",
            f"- Sponsor Kit JSON: {sponsor_kit_url}",
            f"- Offers: {pack_url(config, 'offers/')}",
            f"- Use cases: {pack_url(config, 'use-cases/')}",
            f"- Templates: {pack_url(config, 'templates/')}",
            f"- Guides: {pack_url(config, 'guides/')}",
            f"- Archive: {pack_url(config, 'archive.html')}",
            f"- Starter bundle: {pack_url(config, 'starter-bundle.html')}",
            f"- Store import kit: {pack_url(config, 'store-import.html')}",
            f"- Catalog JSON: {pack_url(config, 'catalog.json')}",
            f"- Product Feed JSON: {pack_url(config, 'product-feed.json')}",
            f"- Product Feed XML: {pack_url(config, 'product-feed.xml')}",
            f"- Product Feed CSV: {pack_url(config, 'product-feed.csv')}",
            f"- Support Funnel JSON: {pack_url(config, 'support-funnel.json')}",
            f"- Support Funnel XML: {pack_url(config, 'support-funnel.xml')}",
            f"- Support Funnel CSV: {pack_url(config, 'support-funnel.csv')}",
            f"- RSS: {pack_url(config, 'feed.xml')}",
            f"- Atom: {pack_url(config, 'atom.xml')}",
            "",
            "## Current State",
            "",
            latest_line,
            *latest_branded_lines,
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
            "- Pay what you can bundle page: " + pay_url,
            "- Sponsor page: " + sponsor_url,
            "- Commercial use page: " + commercial_use_url,
            "- Sponsor Kit JSON: " + sponsor_kit_url,
            *latest_branded_lines,
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
            f"- Product Feed JSON: {pack_url(config, 'product-feed.json')}",
            f"- Product Feed XML: {pack_url(config, 'product-feed.xml')}",
            f"- Product Feed CSV: {pack_url(config, 'product-feed.csv')}",
            f"- Support Funnel JSON: {pack_url(config, 'support-funnel.json')}",
            f"- Support Funnel XML: {pack_url(config, 'support-funnel.xml')}",
            f"- Support Funnel CSV: {pack_url(config, 'support-funnel.csv')}",
            f"- Sponsor Kit JSON: {sponsor_kit_url}",
            f"- Topics JSON: {pack_url(config, 'topics/topics.json')}",
            f"- Offers JSON: {pack_url(config, 'offers/offers.json')}",
            f"- Use Cases JSON: {pack_url(config, 'use-cases/use-cases.json')}",
            f"- Templates JSON: {pack_url(config, 'templates/templates.json')}",
            f"- Guides JSON: {pack_url(config, 'guides/guides.json')}",
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
    topics = topic_index(read_manifests(), config)
    urls = [
        pack_url(config, ""),
        pack_url(config, "archive.html"),
        pack_url(config, "support.html"),
        pack_url(config, "pay-what-you-can.html"),
        pack_url(config, "sponsor.html"),
        pack_url(config, "commercial-use.html"),
        pack_url(config, "sponsor-kit.json"),
        pack_url(config, "offers/"),
        pack_url(config, "offers/offers.json"),
        pack_url(config, "topics/"),
        pack_url(config, "use-cases/"),
        pack_url(config, "use-cases/use-cases.json"),
        pack_url(config, "templates/"),
        pack_url(config, "templates/templates.json"),
        pack_url(config, "guides/"),
        pack_url(config, "guides/guides.json"),
        pack_url(config, "starter-bundle.html"),
        pack_url(config, "store-import.html"),
        pack_url(config, "license.html"),
        pack_url(config, "privacy.html"),
        pack_url(config, "refund-policy.html"),
        pack_url(config, "terms.html"),
        pack_url(config, "catalog.json"),
        pack_url(config, "product-feed.json"),
        pack_url(config, "product-feed.xml"),
        pack_url(config, "product-feed.csv"),
        pack_url(config, "support-funnel.json"),
        pack_url(config, "support-funnel.xml"),
        pack_url(config, "support-funnel.csv"),
        pack_url(config, "topics/topics.json"),
        pack_url(config, "imports/store-listings.csv"),
        pack_url(config, "imports/store-listings.json"),
        pack_url(config, "feed.json"),
        pack_url(config, "feed.xml"),
        pack_url(config, "atom.xml"),
        pack_url(config, "llms.txt"),
        pack_url(config, "llms-full.txt"),
    ]
    urls.extend(pack_url(config, f"offers/{slug}.html") for slug in topics)
    urls.extend(pack_url(config, collection_bundle_rel_path(slug)) for slug in topics)
    urls.extend(pack_url(config, f"topics/{slug}.html") for slug in topics)
    urls.extend(pack_url(config, f"use-cases/{slug}.html") for slug in USE_CASE_DEFINITIONS if slug in topics)
    urls.extend(record["url"] for record in template_records(config))
    urls.extend(pack_url(config, f"guides/{record['slug']}.html") for record in template_records(config))
    urls.extend(pack_url(config, item["path"]) for item in read_manifests()[:80])
    urls.extend(pack_url(config, pack_download_page_path(item)) for item in read_manifests()[:80])
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
    product_feed: dict[str, Any],
    support_funnel: dict[str, Any],
    import_kit: dict[str, Any],
    topics: dict[str, Any],
    use_cases: dict[str, Any],
    templates: dict[str, Any],
    guides: dict[str, Any],
    policies: dict[str, Any],
    support: dict[str, Any],
    pay_page: dict[str, Any],
    sponsor_pages: dict[str, Any],
    offers: dict[str, Any],
    ai_discovery: dict[str, Any],
    discovery: dict[str, Any],
) -> None:
    status_path = DOCS / "status.json"
    monetization = config["monetization"]
    store_url = str(monetization.get("store_url") or "")
    support_url = str(monetization.get("support_url") or "")
    destination_url = store_url or support_url
    destination_type = "store" if store_url else ("support" if support_url else "none")
    today_branded_urls = branded_product_urls(config, pack)
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
        "today_download_page": f"downloads/{pack['pack_slug']}.html",
        "today_branded_product_url": today_branded_urls["branded_product_url"],
        "today_branded_support_url": today_branded_urls["branded_support_url"],
        "today_branded_support_intent_url": today_branded_urls["branded_support_intent_url"],
        "feed_json": feeds.get("json_path", "feed.json"),
        "feed_xml": feeds.get("rss_path", "feed.xml"),
        "atom_xml": feeds.get("atom_path", "atom.xml"),
        "feed_item_count": int(feeds.get("item_count", 0)),
        "product_feed_ready": bool(product_feed.get("ready")),
        "product_feed_json": product_feed.get("json_path", "product-feed.json"),
        "product_feed_xml": product_feed.get("xml_path", "product-feed.xml"),
        "product_feed_csv": product_feed.get("csv_path", "product-feed.csv"),
        "product_feed_count": int(product_feed.get("count", 0)),
        "support_funnel_ready": bool(support_funnel.get("ready")),
        "support_funnel_json": support_funnel.get("json_path", "support-funnel.json"),
        "support_funnel_xml": support_funnel.get("xml_path", "support-funnel.xml"),
        "support_funnel_csv": support_funnel.get("csv_path", "support-funnel.csv"),
        "support_funnel_count": int(support_funnel.get("count", 0)),
        "bundle_ready": bool(bundle.get("pack_count")),
        "bundle_path": bundle.get("zip_path", "bundles/starter-archive.zip"),
        "bundle_page": bundle.get("page_path", "starter-bundle.html"),
        "bundle_pack_count": int(bundle.get("pack_count", 0)),
        "bundle_bytes": int(bundle.get("bytes", 0)),
        "pack_download_count": int(downloads.get("count", 0)),
        "pack_download_page_count": int(downloads.get("page_count", 0)),
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
        "use_case_pages_ready": bool(use_cases.get("ready")),
        "use_case_page_count": int(use_cases.get("count", 0)),
        "use_cases_index": use_cases.get("index_path", "use-cases/index.html"),
        "use_cases_json": use_cases.get("json_path", "use-cases/use-cases.json"),
        "use_case_pages": use_cases.get("paths", []),
        "use_case_branded_urls": use_cases.get("branded_urls", []),
        "template_pages_ready": bool(templates.get("ready")),
        "template_page_count": int(templates.get("count", 0)),
        "templates_index": templates.get("index_path", "templates/index.html"),
        "templates_json": templates.get("json_path", "templates/templates.json"),
        "template_pages": templates.get("paths", []),
        "template_branded_urls": templates.get("branded_urls", []),
        "template_support_page_urls": templates.get("support_page_urls", []),
        "template_support_intent_urls": templates.get("support_intent_urls", []),
        "template_support_intent_count": len(templates.get("support_intent_urls", [])),
        "guide_pages_ready": bool(guides.get("ready")),
        "guide_page_count": int(guides.get("count", 0)),
        "guides_index": guides.get("index_path", "guides/index.html"),
        "guides_json": guides.get("json_path", "guides/guides.json"),
        "guide_pages": guides.get("paths", []),
        "guide_branded_urls": guides.get("branded_urls", []),
        "policy_pages_ready": bool(policies.get("count")),
        "policy_page_count": int(policies.get("count", 0)),
        "policy_pages": policies.get("paths", []),
        "support_page_ready": bool(support.get("page_path")),
        "support_page": support.get("page_path", "support.html"),
        "support_page_url": pack_url(config, support.get("page_path", "support.html")),
        "pay_what_you_can_ready": bool(pay_page.get("page_path")),
        "pay_what_you_can_page": pay_page.get("page_path", "pay-what-you-can.html"),
        "pay_what_you_can_url": pack_url(config, pay_page.get("page_path", "pay-what-you-can.html")),
        "support_tier_count": int(pay_page.get("tier_count", 0)),
        "sponsor_surface_ready": bool(sponsor_pages.get("ready")),
        "sponsor_page": sponsor_pages.get("sponsor_page", "sponsor.html"),
        "sponsor_page_url": sponsor_pages.get("sponsor_page_url", pack_url(config, "sponsor.html")),
        "sponsor_branded_url": sponsor_pages.get("sponsor_branded_url", branded_url(config, "sponsor")),
        "commercial_use_page": sponsor_pages.get("commercial_use_page", "commercial-use.html"),
        "commercial_use_page_url": sponsor_pages.get("commercial_use_page_url", pack_url(config, "commercial-use.html")),
        "commercial_use_branded_url": sponsor_pages.get("commercial_use_branded_url", branded_url(config, "commercial-use")),
        "sponsor_kit_json": sponsor_pages.get("kit_path", "sponsor-kit.json"),
        "sponsor_kit_url": sponsor_pages.get("kit_url", pack_url(config, "sponsor-kit.json")),
        "sponsor_kit_branded_url": sponsor_pages.get("kit_branded_url", branded_url(config, "sponsor-kit.json")),
        "sponsor_support_intent_url": sponsor_pages.get("sponsor_support_intent_url", sponsor_pages.get("support_intent_url", branded_url(config, "support/go") or support_url)),
        "commercial_support_intent_url": sponsor_pages.get("commercial_support_intent_url", branded_url(config, "commercial-use/support/go") or support_url),
        "general_support_intent_url": sponsor_pages.get("general_support_intent_url", branded_url(config, "support/go") or support_url),
        "sponsor_tier_count": int(sponsor_pages.get("tier_count", 0)),
        "offer_pages_ready": bool(offers.get("ready")),
        "offer_page_count": int(offers.get("count", 0)),
        "offers_index": offers.get("index_path", "offers/index.html"),
        "offers_json": offers.get("json_path", "offers/offers.json"),
        "offer_pages": offers.get("paths", []),
        "collection_bundle_ready": bool(offers.get("collection_bundle_count")),
        "collection_bundle_count": int(offers.get("collection_bundle_count", 0)),
        "collection_bundle_paths": offers.get("collection_bundle_paths", []),
        "collection_bundle_urls": offers.get("collection_bundle_urls", []),
        "collection_bundle_bytes": int(offers.get("collection_bundle_bytes", 0)),
        "collection_support_intent_urls": offers.get("support_intent_urls", []),
        "collection_support_intent_count": len(offers.get("support_intent_urls", [])),
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

    refresh_existing_pack_pages(config)
    downloads = render_pack_downloads(config)
    feeds = render_feed(config)
    render_catalog(config)
    product_feed = render_product_feed(config)
    support_funnel = render_support_funnel_feed(config)
    render_archive(config)
    topics = render_topic_pages(config)
    use_cases = render_use_case_pages(config)
    templates = render_template_pages(config)
    guides = render_guide_pages(config)
    policies = render_policy_pages(config)
    support = render_support_page(config)
    pay_page = render_pay_what_you_can_page(config, support)
    sponsor_pages = render_sponsor_pages(config)
    offers = render_offer_pages(config, support)
    ai_discovery = render_ai_discovery_files(config, support, pay_page, sponsor_pages)
    import_kit = render_store_import_kit(config)
    bundle = render_bundle(config)
    render_index(pack, config, bundle)
    render_sitemap(config)
    render_robots(config)
    discovery = render_indexnow_key(config)
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    write_status(
        pack,
        config,
        bundle,
        downloads,
        feeds,
        product_feed,
        support_funnel,
        import_kit,
        topics,
        use_cases,
        templates,
        guides,
        policies,
        support,
        pay_page,
        sponsor_pages,
        offers,
        ai_discovery,
        discovery,
    )
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
