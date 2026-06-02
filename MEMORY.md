# Daily Autodigital Shelf Memory

## Project Identity

- Project ID: `daily-autodigital-shelf`
- Primary operator: `DAI-AUT-01`
- Supervising operator: `NYX-01`
- Template: `site`
- Stage: `launch`
- Status: `active`

## Stable Surfaces

- `https://x26dotapp.github.io/daily-autodigital-shelf/`

## Stable Runtime Roots

- `C:\GitHub\x26dotapp\daily-autodigital-shelf\state`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\docs`

## Current Reality

- This is a daily static digital-pack shelf. It generates original printable/content packs under `docs/packs/`, updates `docs/index.html`, and writes status/ledger artifacts.
- The public site root is `docs/` for GitHub Pages.
- The generator is deterministic and uses only local Python standard library code. It does not call paid APIs.
- The lane intentionally does not trade, send outreach, scrape copyrighted content, create payment accounts, touch bank/wallet data, or claim guaranteed revenue.
- Monetization is not connected by default. `config/config.local.json` can add a real store/support/affiliate destination later without committing secrets.
- Verified 2026-06-02: GitHub Pages is built at `https://x26dotapp.github.io/daily-autodigital-shelf/`.
- Verified 2026-06-02: Scheduled task `HUMANi Daily Autodigital Shelf` runs daily at 06:10 local time, last manual Task Scheduler run returned `0`, and next run was `2026-06-02 06:10`.
- Verified 2026-06-02: Scheduled task `HUMANi Daily Autodigital Shelf Watchdog` runs daily at 07:15 local time, last Task Scheduler run returned `0`, and writes local health status to `state/watchdog-status.json`.
- Verified 2026-06-02: Today's pack is `One-Page SOP Builder` under `docs/packs/2026-06-02-one-page-sop/`, including landing page, worksheet, checklist, cover SVG, manifest, and `seller-copy.md`.
- Verified 2026-06-02: `verify-system.ps1` passed against local output, the live URL, the daily task, and the watchdog task.
- Added 2026-06-02: Generated shelf also writes `archive.html`, `catalog.json`, and `catalog.csv` so future store/import workflows can reuse packs without scraping the site.
- Added 2026-06-02: Expanded the generator to 29 pack templates and seeded a 21-pack starter archive from `2026-05-13` through `2026-06-02`.
- Added 2026-06-02: Generated shelf also writes `starter-bundle.html` and `docs/bundles/starter-archive.zip` as a single store-uploadable ZIP; live ZIP verified and current local bundle size is 272,703 bytes.
- Added 2026-06-02: Generated shelf writes 21 individual product ZIPs under `docs/downloads/`; every seeded pack page now links its own `Download pack ZIP` action and catalog rows include `download_url`.
- Added 2026-06-02: Generated shelf writes `store-import.html`, `imports/store-listings.csv`, `imports/store-listings.json`, and `imports/store-upload-kit.zip`; current import kit has 21 listing rows and the ZIP is 152,453 bytes.
- Added 2026-06-02: Generated public pages include Open Graph image tags, Twitter summary-card tags, and richer JSON-LD for pack pages, archive, starter bundle, and import kit.
- Added 2026-06-02: IndexNow discovery automation is enabled. Public key file `docs/b0d7a0387b4f41cc886dc47328c20bcb.txt` is generated; latest social-metadata submission sent 25 changed URLs and received HTTP 200 after Pages served the key.
- Current 2026-06-02 pack after library expansion: `One-Page SOP Builder` under `docs/packs/2026-06-02-one-page-sop/`.

## Operator Rule

- Keep this file honest. Record stable truths, not wishful plans.
- Update current task and handoff files when the lane materially changes.
- If a payout/store/ad/affiliate platform is connected, record the exact public URL and the non-secret setup state here.
