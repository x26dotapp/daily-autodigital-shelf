# Daily Autodigital Shelf Handoff

## Project State

Daily Autodigital Shelf is a public static site plus a local daily generator. The generator creates one dated digital pack per run, writes printable worksheet/checklist/cover assets, updates the homepage, writes `docs/status.json`, appends `state/ledger.jsonl`, then the wrapper can commit and push the changed site.

This is revenue infrastructure, not guaranteed revenue. It does not touch live funds, run trading, send lead messages, create accounts, or claim that money is being earned before a real buyer/platform/payout path exists.

Verified 2026-06-02:

- Public site: `https://x26dotapp.github.io/daily-autodigital-shelf/`
- Repo: `https://github.com/x26dotapp/daily-autodigital-shelf`
- Task: `HUMANi Daily Autodigital Shelf`, daily at 06:10 local time, last manual run result `0`
- Pack: `Micro Budget Reset`
- Catalog surfaces: `archive.html`, `catalog.json`, `catalog.csv`, `feed.json`, `sitemap.xml`, `robots.txt`
- Live verifier: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\verify-system.ps1`
- Monetization: not connected; public site says `Status: Not connected`

## Where To Start

1. Open `MEMORY.md`
2. Open `CURRENT-TASK.md`
3. Verify the live surfaces and runtime state
4. Continue from the real current edge, not from stale assumptions

## Important Guardrails

- Do not leave fake wins, fake testimonials, or dishonest proof states behind after verification.
- Keep intake, admin, outreach, and delivery/runtime paths easy to rediscover after chat drift.
- Do not connect live payout, ad, store, support, or affiliate links without recording the public destination and setup state.
- Do not add bulk outreach or scraping to this lane. If discovery is needed, create a separate reviewed lane.
- Keep generated packs original, public-domain-safe, and free of medical, legal, investment, or guaranteed-income advice.

## Runtime Paths

- `C:\GitHub\x26dotapp\daily-autodigital-shelf\state`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\docs`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\tools\generate_daily_shelf.py`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\tools\verify_daily_shelf.py`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\run-daily.ps1`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\verify-system.ps1`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\install-scheduled-task.ps1`
