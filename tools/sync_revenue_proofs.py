from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state"
PROOF_ROOT = STATE / "revenue-proofs"
INBOX = PROOF_ROOT / "inbox"
SNAPSHOT = STATE / "revenue-proof-snapshot.json"

ACCEPTED_STATUSES = {
    "paid",
    "complete",
    "completed",
    "succeeded",
    "settled",
    "captured",
    "approved",
}
SUPPORTED_SUFFIXES = {".csv", ".json"}

DATE_KEYS = ("date", "paid_at", "created_at", "timestamp", "payment_date", "transaction_date")
AMOUNT_KEYS = ("amount", "gross", "net", "total", "payment_amount", "amount_money", "paid_amount")
CURRENCY_KEYS = ("currency", "currency_code", "amount_currency")
STATUS_KEYS = ("status", "payment_status", "state")
PLATFORM_KEYS = ("platform", "provider", "processor", "source", "source_platform")
ID_KEYS = ("transaction_id", "payment_id", "order_id", "receipt_id", "id")
PRODUCT_KEYS = ("product", "item", "description", "memo", "title", "sku")


def now_utc() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()


def today_iso(value: str | None) -> str:
    if value:
        return dt.date.fromisoformat(value).isoformat()
    return dt.datetime.now().astimezone().date().isoformat()


def cents_to_usd(cents: int) -> str:
    return f"{Decimal(cents) / Decimal(100):.2f}"


def normalize_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")


def normalize_row(row: dict[str, Any]) -> dict[str, Any]:
    return {normalize_key(str(key)): value for key, value in row.items()}


def first_value(row: dict[str, Any], keys: tuple[str, ...]) -> str:
    for key in keys:
        value = row.get(key)
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return ""


def parse_amount_cents(value: str) -> int:
    text = str(value or "").strip()
    if not text:
        return 0
    text = text.replace(",", "")
    text = re.sub(r"[^0-9.\-]", "", text)
    if not text or text in {"-", "."}:
        return 0
    try:
        amount = Decimal(text)
    except InvalidOperation:
        return 0
    if amount <= 0:
        return 0
    return int((amount * Decimal(100)).quantize(Decimal("1")))


def parse_date(value: str) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    if "T" in text:
        try:
            return dt.datetime.fromisoformat(text.replace("Z", "+00:00")).date().isoformat()
        except ValueError:
            pass
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d", "%d-%m-%Y"):
        try:
            return dt.datetime.strptime(text[:10], fmt).date().isoformat()
        except ValueError:
            continue
    return ""


def hash_receipt_id(value: str) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def load_json_rows(path: Path) -> list[dict[str, Any]]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    if isinstance(raw, list):
        return [item for item in raw if isinstance(item, dict)]
    if isinstance(raw, dict):
        for key in ("payments", "transactions", "orders", "items", "records", "data"):
            value = raw.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        return [raw]
    return []


def load_csv_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append({str(key): value for key, value in row.items() if key is not None})
    return rows


def iter_source_rows() -> tuple[list[Path], list[dict[str, Any]]]:
    INBOX.mkdir(parents=True, exist_ok=True)
    source_files = [
        path
        for path in sorted(INBOX.glob("*"))
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
    ]
    rows: list[dict[str, Any]] = []
    for path in source_files:
        try:
            raw_rows = load_csv_rows(path) if path.suffix.lower() == ".csv" else load_json_rows(path)
        except OSError:
            raw_rows = []
        for row in raw_rows:
            normalized = normalize_row(row)
            normalized["_source_file"] = path.name
            rows.append(normalized)
    return source_files, rows


def classify_receipt(row: dict[str, Any]) -> dict[str, Any]:
    payment_date = parse_date(first_value(row, DATE_KEYS))
    status = first_value(row, STATUS_KEYS).lower()
    amount_cents = parse_amount_cents(first_value(row, AMOUNT_KEYS))
    currency = (first_value(row, CURRENCY_KEYS) or "USD").upper()
    platform = first_value(row, PLATFORM_KEYS) or "local-export"
    receipt_hash = hash_receipt_id(first_value(row, ID_KEYS))
    product = first_value(row, PRODUCT_KEYS)
    accepted = bool(payment_date and status in ACCEPTED_STATUSES and amount_cents > 0 and currency == "USD")
    reject_reasons: list[str] = []
    if not payment_date:
        reject_reasons.append("missing payment date")
    if status not in ACCEPTED_STATUSES:
        reject_reasons.append("status not paid/settled")
    if amount_cents <= 0:
        reject_reasons.append("missing positive amount")
    if currency != "USD":
        reject_reasons.append("non-USD currency not counted")
    return {
        "accepted": accepted,
        "date": payment_date,
        "amount_cents": amount_cents if accepted else 0,
        "amount_usd": cents_to_usd(amount_cents) if accepted else "0.00",
        "currency": currency,
        "status": status or "unknown",
        "platform": platform,
        "product": product,
        "receipt_hash": receipt_hash,
        "source_file": str(row.get("_source_file") or ""),
        "reject_reasons": reject_reasons,
    }


def build_snapshot(day: str) -> dict[str, Any]:
    source_files, raw_rows = iter_source_rows()
    visible_source_files = [
        path
        for path in INBOX.glob("*")
        if path.is_file() and path.name != ".gitkeep"
    ]
    receipts = [classify_receipt(row) for row in raw_rows]
    accepted = [item for item in receipts if item["accepted"]]
    rejected = [item for item in receipts if not item["accepted"]]
    today_receipts = [item for item in accepted if item["date"] == day]
    today_cents = sum(int(item["amount_cents"]) for item in today_receipts)
    total_cents = sum(int(item["amount_cents"]) for item in accepted)
    by_day: dict[str, int] = {}
    for item in accepted:
        by_day[item["date"]] = by_day.get(item["date"], 0) + int(item["amount_cents"])
    public_receipts = [
        {
            "date": item["date"],
            "amount_usd": item["amount_usd"],
            "currency": item["currency"],
            "status": item["status"],
            "platform": item["platform"],
            "product": item["product"],
            "receipt_hash": item["receipt_hash"],
        }
        for item in accepted[-25:]
    ]
    return {
        "kind": "daily-shelf-revenue-proof-snapshot",
        "version": 1,
        "fetched_at": now_utc(),
        "today": day,
        "source_dir": "state/revenue-proofs/inbox",
        "source_dir_exists": INBOX.exists(),
        "source_file_count": len(visible_source_files),
        "supported_file_count": len(source_files),
        "candidate_receipt_count": len(receipts),
        "accepted_receipt_count": len(accepted),
        "rejected_receipt_count": len(rejected),
        "today_receipt_count": len(today_receipts),
        "today_revenue_cents": today_cents,
        "today_revenue_usd": cents_to_usd(today_cents),
        "total_revenue_cents": total_cents,
        "total_revenue_usd": cents_to_usd(total_cents),
        "actual_daily_revenue_proven": today_cents > 0,
        "any_revenue_proven": total_cents > 0,
        "payment_provider_api_verified": False,
        "accepted_statuses": sorted(ACCEPTED_STATUSES),
        "by_day_usd": {date: cents_to_usd(cents) for date, cents in sorted(by_day.items())},
        "recent_receipts": public_receipts,
        "rejected_sample_count": min(len(rejected), 10),
        "rejected_samples": [
            {
                "source_file": item["source_file"],
                "status": item["status"],
                "currency": item["currency"],
                "reject_reasons": item["reject_reasons"],
            }
            for item in rejected[:10]
        ],
        "privacy": "Publishes totals and hashed receipt identifiers only. Raw payment exports stay ignored by git in state/revenue-proofs/inbox.",
        "boundary": "This monitor only reports sanitized local payment-export evidence. It does not create checkout, collect payment credentials, or guarantee future daily revenue.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync sanitized Daily Shelf revenue proof evidence.")
    parser.add_argument("--date", help="Expected shelf date. Defaults to local today.")
    args = parser.parse_args()

    STATE.mkdir(parents=True, exist_ok=True)
    INBOX.mkdir(parents=True, exist_ok=True)
    snapshot = build_snapshot(today_iso(args.date))
    SNAPSHOT.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    print(json.dumps(snapshot, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
