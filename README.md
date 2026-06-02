# Daily Autodigital Shelf

This is a small, legal, low-maintenance revenue lane.

It does not promise guaranteed income, trade funds, send outreach, scrape
copyrighted work, or create payment accounts. It does one practical thing every
day: generate a new public digital pack and update a static site that can be
connected to a store, affiliate link, support link, or ad setup later.

## What Runs

- `tools/generate_daily_shelf.py` creates today's pack under `docs/packs/`.
- `tools/verify_daily_shelf.py` checks that the generated site and pack are complete.
- `tools/submit_indexnow.py` submits changed public URLs to IndexNow after a successful push.
- `run-daily.ps1` runs the generator, commits site changes, and pushes them.
- `install-scheduled-task.ps1` installs a daily Windows Scheduled Task.
- `verify-system.ps1` checks local output, the live site, and the scheduled task.
- `docs/` is the GitHub Pages site root.

Each generated pack includes:

- pack landing page
- printable worksheet
- printable checklist
- cover SVG
- manifest JSON
- `seller-copy.md` for store listing copy
- direct per-pack download ZIP under `docs/downloads/`
- inclusion in the generated starter bundle ZIP

The site also publishes:

- `archive.html` for all generated packs
- `downloads/*.zip` for one-file individual product upload
- `starter-bundle.html` and `bundles/starter-archive.zip` for one-file product upload
- `catalog.json` for programmatic product import
- `catalog.csv` for spreadsheet/store import workflows
- `feed.json`, `sitemap.xml`, and `robots.txt` for discoverability
- an IndexNow key file so changed URLs can be submitted to participating search engines

IndexNow submission state is kept locally in `state/indexnow-state.json` and is
ignored by Git. The key file itself is public by design because the protocol
uses a public text file to prove site control.

## Current Guardrail

No payout or monetization account is configured by default. Edit
`config/config.local.json` only when a real store/support/affiliate destination
exists.

Copy the example first:

```powershell
Copy-Item .\config\config.example.json .\config\config.local.json
```

Then set real URLs in `config.local.json`. Do not put secrets in this repo.

## Manual Run

```powershell
cd C:\GitHub\x26dotapp\daily-autodigital-shelf
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run-daily.ps1
```

## Starter Archive Backfill

Use this when the shelf needs more inventory immediately while preserving the
daily dated format:

```powershell
cd C:\GitHub\x26dotapp\daily-autodigital-shelf
python .\tools\generate_daily_shelf.py --date 2026-06-02 --backfill-days 21
```

The command generates the archive in chronological order so the final homepage
still points at the target date.

The same generator also builds `docs/bundles/starter-archive.zip`, a single
downloadable archive containing the generated pack pages, worksheets,
checklists, covers, manifests, catalog files, and seller-copy files.

## Verify

```powershell
cd C:\GitHub\x26dotapp\daily-autodigital-shelf
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\verify-system.ps1
```

## Install Daily Task

```powershell
cd C:\GitHub\x26dotapp\daily-autodigital-shelf
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\install-scheduled-task.ps1
```

The task name is `HUMANi Daily Autodigital Shelf`.

## Honest Money Note

This can produce and publish sellable material automatically. Actual money still
requires an external platform, buyer, advertiser, affiliate program, or support
link. That legal/payment layer is kept explicit so the automation cannot fake
revenue or touch funds silently.
