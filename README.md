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
- `watchdog.ps1` verifies the daily task, live site, and generated artifacts, then reruns the safe daily wrapper only when verification fails.
- `install-watchdog-task.ps1` installs the daily watchdog Scheduled Task.
- `.github/workflows/daily-shelf.yml` is a GitHub Actions fallback publisher in case the PC misses a daily run.
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
- `topics/index.html`, topic pages, and `topics/topics.json` for use-case browsing
- `terms.html`, `privacy.html`, `license.html`, and `refund-policy.html` for store-readiness policy review
- `downloads/*.zip` for one-file individual product upload
- `starter-bundle.html` and `bundles/starter-archive.zip` for one-file product upload
- `support.html` as a dedicated support/conversion page for the connected public support path
- `offers/index.html`, `offers/offers.json`, and topic-based offer pages that
  group related packs into support-backed collection surfaces
- `store-import.html`, `imports/store-listings.csv`, `imports/store-listings.json`, and
  `imports/store-upload-kit.zip` for generic marketplace import workflows, including policy pages
- `catalog.json` for programmatic product import
- `catalog.csv` for spreadsheet/store import workflows
- `feed.json`, `feed.xml`, `atom.xml`, `llms.txt`, `llms-full.txt`,
  `sitemap.xml`, and `robots.txt` for search/AI discoverability
- an IndexNow key file so changed URLs can be submitted to participating search engines

IndexNow submission state is kept locally in `state/indexnow-state.json` and is
ignored by Git. The key file itself is public by design because the protocol
uses a public text file to prove site control.

## Branded Entry Bridge

The CalmSprout Worker at `C:\scripts\CalmSprout` also exposes a branded bridge
for this shelf:

- `https://www.calmsprout.com/daily-shelf`
- `https://www.calmsprout.com/daily-shelf/offers`
- `https://www.calmsprout.com/daily-shelf/support`
- `https://www.calmsprout.com/sitemap.xml`
- `https://www.calmsprout.com/a4f604db6d2046939ff6c7e3d29d341e.txt`

This improves discovery and support conversion through an existing public
domain. It does not make CalmSprout product checkout and does not prove revenue.

## Current Guardrail

A public support destination is configured in `config/config.public.json`:
`https://gift.calmsprout.com`. This is a Square-hosted CalmSprout gift-card /
support path, not product checkout. The generated `support.html` page links to
that destination while keeping the boundary explicit. Generated offer pages use
the same support path and state that product checkout is not connected. The
generated packs remain public downloads until a real store checkout is connected.

Use `config/config.local.json` only for private local overrides. Do not put
secrets in this repo.

Copy the example first:

```powershell
Copy-Item .\config\config.example.json .\config\config.local.json
```

Then set real private override URLs in `config.local.json` when needed.

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

## Install Watchdog Task

```powershell
cd C:\GitHub\x26dotapp\daily-autodigital-shelf
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\install-watchdog-task.ps1
```

The watchdog task name is `HUMANi Daily Autodigital Shelf Watchdog`. It runs at
7:15am local time, after the daily generator. It logs to `logs/watchdog.log` and
writes local status to `state/watchdog-status.json`.

## GitHub Fallback Publisher

The workflow `.github/workflows/daily-shelf.yml` runs daily from GitHub Actions
after the local PC task and watchdog. It computes the shelf date in
`America/New_York`, runs the generator and verifier, commits only when files
changed, pushes to `main`, and submits changed URLs to IndexNow.

This is a reliability fallback, not a separate monetization layer.

## Honest Money Note

This can produce and publish sellable material automatically. Actual money still
requires an external platform, buyer, advertiser, affiliate program, or support
link. That legal/payment layer is kept explicit so the automation cannot fake
revenue or touch funds silently.
