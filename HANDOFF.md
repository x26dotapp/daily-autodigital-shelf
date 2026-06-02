# Daily Autodigital Shelf Handoff

## Project State

Daily Autodigital Shelf is a public static site plus a local daily generator. The generator creates one dated digital pack per run, writes printable worksheet/checklist/cover assets, updates the homepage, writes `docs/status.json`, appends `state/ledger.jsonl`, then the wrapper can commit and push the changed site.

This is revenue infrastructure, not guaranteed revenue. It does not touch live funds, run trading, send lead messages, create accounts, or claim that money is being earned before a real buyer/platform/payout path exists.

Verified 2026-06-02:

- Public site: `https://x26dotapp.github.io/daily-autodigital-shelf/`
- Branded entry: `https://www.calmsprout.com/daily-shelf`
- Repo: `https://github.com/x26dotapp/daily-autodigital-shelf`
- Task: `HUMANi Daily Autodigital Shelf`, daily at 06:10 local time, last manual run result `0`
- Watchdog task: `HUMANi Daily Autodigital Shelf Watchdog`, daily at 07:15 local time, last Task Scheduler run result `0`
- Pack: `One-Page SOP Builder`
- Starter archive: 21 packs dated `2026-05-13` through `2026-06-02`
- Individual downloads: 21 product ZIPs under `downloads/`; all seeded pack pages now include `Download pack ZIP`
- Bundle surface: `starter-bundle.html` and `bundles/starter-archive.zip` live; current local ZIP size is 323,728 bytes and includes policy pages, support page, offer pages, `llms.txt`, `llms-full.txt`, and RSS/Atom feed files
- Import surface: `store-import.html`, `imports/store-listings.csv`, `imports/store-listings.json`, and `imports/store-upload-kit.zip` live; import ZIP is 161,610 bytes and rows include topic fields plus policy pages
- Support/discovery surfaces: `support.html`, `llms.txt`, and `llms-full.txt` live; the support page links to `https://gift.calmsprout.com` while stating that product checkout is not connected
- Offer surfaces: `offers/index.html`, `offers/offers.json`, and 5 topic collection offer pages live; offer pages link the starter bundle, expose CollectionPage JSON-LD, route support CTAs to `https://gift.calmsprout.com`, and state that product checkout is not connected
- CalmSprout bridge: `C:\scripts\CalmSprout` commits `f063a55` (`Add Daily Shelf bridge`), `d8fa6d9` (`Add Daily Shelf landing page`), and `8a689e1` (`Add CalmSprout IndexNow key`) deployed directly to Cloudflare. Latest Worker version is `61361a87-0bab-4cdc-b477-d332b254cf23`. Live `https://www.calmsprout.com/daily-shelf` is an indexable landing page; `/daily-shelf/offers` redirects to the offer index; `/daily-shelf/support` redirects to the public Square support page; `robots.txt`, `sitemap.xml`, and public IndexNow key file `a4f604db6d2046939ff6c7e3d29d341e.txt` are live; the `www.calmsprout.com` homepage includes a Daily Shelf banner.
- Topic surfaces: `topics/index.html`, 5 topic pages, and `topics/topics.json` live; seeded pack pages link related topics and topic URLs are in catalog/import outputs
- Policy surfaces: `terms.html`, `privacy.html`, `license.html`, and `refund-policy.html` live; they are store-readiness pages and do not activate checkout or payout
- Metadata: generated pages include Open Graph image tags, Twitter summary-card tags, and richer JSON-LD for products and listing surfaces
- Catalog/discovery surfaces: `archive.html`, `catalog.json`, `catalog.csv`, `feed.json`, `feed.xml`, `atom.xml`, `llms.txt`, `llms-full.txt`, `sitemap.xml`, `robots.txt`
- Feed proof: live `feed.xml` returned HTTP 200 with 10,552 bytes; live `atom.xml` returned HTTP 200 with 8,706 bytes; both contain `One-Page SOP Builder`
- Discovery: IndexNow key file live; latest direct `tools/submit_indexnow.py --all` submitted 21 offer/support/discovery URLs and received HTTP 200; follow-up dry run queued 0 URLs
- GitHub fallback publisher: `.github/workflows/daily-shelf.yml` is active. It runs daily after the local PC task/watchdog, can be run manually, generates/verifies, commits only on changed output, pushes to `main`, and submits IndexNow when it commits.
- Fallback proof: manual run `26805969926` completed successfully on commit `5d6eec6` and logged `No generated changes to publish`
- Determinism: generator normalizes text bytes inside ZIPs, fixes ZIP creator metadata, forces LF CSV output, and tracks `.gitattributes` so Windows and GitHub runners do not churn same-day artifacts
- Latest functional infrastructure commit: `5d6eec6` (`Add support-backed offer pages`) pushed to `main`; GitHub Pages deployment `26805912605` succeeded
- Live verifier: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\verify-system.ps1`
- Monetization: public support destination connected; public site says `Status: Connected`, shows `Support this shelf`, and links to `https://gift.calmsprout.com`, which resolves to the Square-hosted CalmSprout gift/support page. Product checkout is not connected, `store_connected` is false, and daily revenue is not proven.
- Direct deploy note: CalmSprout has local Git but no remote, so bridge changes were committed locally before direct Wrangler deploy. Keep future CalmSprout changes committed locally and record deployed Worker version IDs.
- Latest verifier baseline: `files_checked: 36`, `bundle_bytes: 323728`, `pack_download_bytes: 126854`, `store_import_zip_bytes: 161610`, `support_connected: true`, `store_connected: false`
- CalmSprout discovery proof: public key `https://www.calmsprout.com/a4f604db6d2046939ff6c7e3d29d341e.txt` returned HTTP 200; IndexNow accepted 6 CalmSprout URLs with HTTP 202: homepage, `/daily-shelf`, `/daily-shelf/offers`, `/daily-shelf/support`, `robots.txt`, and `sitemap.xml`.

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
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\docs\imports`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\docs\topics`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\docs\terms.html`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\docs\privacy.html`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\docs\license.html`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\docs\refund-policy.html`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\docs\feed.json`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\docs\feed.xml`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\docs\atom.xml`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\docs\support.html`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\docs\offers`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\docs\llms.txt`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\docs\llms-full.txt`
- `C:\scripts\CalmSprout\src\worker.js`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\config\config.public.json`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\tools\generate_daily_shelf.py`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\tools\verify_daily_shelf.py`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\tools\submit_indexnow.py`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\run-daily.ps1`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\.github\workflows\daily-shelf.yml`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\.gitattributes`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\watchdog.ps1`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\verify-system.ps1`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\install-scheduled-task.ps1`
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\install-watchdog-task.ps1`
