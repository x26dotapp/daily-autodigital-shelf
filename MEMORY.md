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
- Public support destination is connected through `config/config.public.json`: `https://gift.calmsprout.com` (Square-hosted CalmSprout gift-card/support page). This is not product checkout; `store_connected` remains false and pack downloads remain public until a store checkout exists. `config/config.local.json` stays reserved for private local overrides and is not present/committed.
- Verified 2026-06-02: GitHub Pages is built at `https://x26dotapp.github.io/daily-autodigital-shelf/`.
- Verified 2026-06-02: Scheduled task `HUMANi Daily Autodigital Shelf` runs daily at 06:10 local time, last manual Task Scheduler run returned `0`, and next run was `2026-06-02 06:10`.
- Verified 2026-06-02: Scheduled task `HUMANi Daily Autodigital Shelf Watchdog` runs daily at 07:15 local time, last Task Scheduler run returned `0`, and writes local health status to `state/watchdog-status.json`.
- Verified 2026-06-02: Today's pack is `One-Page SOP Builder` under `docs/packs/2026-06-02-one-page-sop/`, including landing page, worksheet, checklist, cover SVG, manifest, and `seller-copy.md`.
- Verified 2026-06-02: `verify-system.ps1` passed against local output, the live URL, the daily task, and the watchdog task.
- Added 2026-06-02: Generated shelf also writes `archive.html`, `catalog.json`, and `catalog.csv` so future store/import workflows can reuse packs without scraping the site.
- Added 2026-06-02: Expanded the generator to 29 pack templates and seeded a 21-pack starter archive from `2026-05-13` through `2026-06-02`.
- Added 2026-06-02: Generated shelf also writes `starter-bundle.html` and `docs/bundles/starter-archive.zip` as a single store-uploadable ZIP; live ZIP verified and current local bundle size is 304,869 bytes.
- Added 2026-06-02: Generated shelf writes 21 individual product ZIPs under `docs/downloads/`; every seeded pack page now links its own `Download pack ZIP` action and catalog rows include `download_url`.
- Added 2026-06-02: Generated shelf writes `store-import.html`, `imports/store-listings.csv`, `imports/store-listings.json`, and `imports/store-upload-kit.zip`; current import kit has 21 listing rows, topic metadata fields, policy pages, and the ZIP is 161,610 bytes.
- Added 2026-06-02: Generated public pages include Open Graph image tags, Twitter summary-card tags, and richer JSON-LD for pack pages, archive, starter bundle, and import kit.
- Added 2026-06-02: IndexNow discovery automation is enabled. Public key file `docs/b0d7a0387b4f41cc886dc47328c20bcb.txt` is generated; latest social-metadata submission sent 25 changed URLs and received HTTP 200 after Pages served the key.
- Added 2026-06-02: Generated shelf writes topic surfaces under `docs/topics/`: topic index, 5 topic pages, and `topics/topics.json`. Product pages link related topics; catalog/import rows include `topic_urls`; sitemap and IndexNow include topic URLs. Commit `d631af4` pushed and Pages deployed successfully.
- Verified 2026-06-02: Live topic browser check passed for `https://x26dotapp.github.io/daily-autodigital-shelf/topics/` and `topics/small-business-ops.html`; IndexNow accepted 37 changed URLs with HTTP 200 and a follow-up dry run showed 0 queued URLs.
- Added 2026-06-02: GitHub Actions fallback publisher `.github/workflows/daily-shelf.yml` is active. It runs after the local PC task/watchdog, computes the date in `America/New_York`, generates/verifies, commits only on changed output, pushes to `main`, and submits IndexNow.
- Verified 2026-06-02: Manual fallback run `26803177994` succeeded on commit `4c3b5a2` and logged `No generated changes to publish`; this proves the fallback can execute without creating repeat same-day churn.
- Added 2026-06-02: Generator now normalizes text bytes inside ZIPs, fixes ZIP creator metadata, forces LF CSV output, and uses `.gitattributes` for generated text files so Windows and GitHub runners stay stable.
- Verified 2026-06-02: Direct IndexNow submission after fallback/determinism updates accepted 5 changed URLs with HTTP 200; follow-up dry run showed 0 queued URLs.
- Added 2026-06-02: Generated shelf writes store-readiness policy pages: `terms.html`, `privacy.html`, `license.html`, and `refund-policy.html`. Homepage/archive/import/bundle surfaces link policies; starter bundle and store upload kit include the policy files.
- Verified 2026-06-02: Store policy commit `190d77c` deployed successfully. Live browser check passed for `terms.html` and `store-import.html`; `verify-system.ps1` now checks 4 policy pages and 28 files; IndexNow accepted 9 policy/discovery URLs and follow-up dry run showed 0 queued URLs.
- Added 2026-06-02: Generated shelf now writes RSS and Atom feeds at `feed.xml`
  and `atom.xml`, links them from the homepage, includes them in the starter
  bundle, adds them to the sitemap and status file, and submits them through
  IndexNow. Commit `cd2dd12` pushed to `main`.
- Verified 2026-06-02: GitHub Pages deployment `26803871909` succeeded for
  `cd2dd12`. Live `feed.xml` returned HTTP 200 with 10,552 bytes; live
  `atom.xml` returned HTTP 200 with 8,706 bytes; both contain
  `One-Page SOP Builder`. `verify-system.ps1` now checks 30 files.
- Verified 2026-06-02: IndexNow accepted six changed feed/discovery URLs with
  HTTP 200: homepage, starter bundle, `feed.json`, `feed.xml`, `atom.xml`, and
  `sitemap.xml`; follow-up dry run showed 0 queued URLs.
- Verified 2026-06-02: GitHub fallback publisher run `26803952952` succeeded
  on `cd2dd12` and logged `No generated changes to publish`.
- Current 2026-06-02 pack after library expansion: `One-Page SOP Builder` under `docs/packs/2026-06-02-one-page-sop/`.
- Verified 2026-06-02: Commit `2159455` (`Connect support destination`) pushed to `main`; GitHub Pages run `26804778546` deployed it. Live homepage and backfilled pack pages show `Support this shelf`, link to `https://gift.calmsprout.com`, and no longer show disconnected store copy.
- Verified 2026-06-02: Live `status.json` reports `monetization_enabled: true`, `monetization_destination_type: support`, `monetization_destination_url: https://gift.calmsprout.com`, `support_connected: true`, and `store_connected: false`. `https://gift.calmsprout.com` resolves to the Square-hosted gift/support page at `https://app.squareup.com/gift/MLZ021BP45QKH/order`.
- Verified 2026-06-02: IndexNow accepted 26 support-connected URLs with HTTP 200; follow-up dry run showed `submit_count: 0`. GitHub fallback publisher run `26804835124` succeeded on `2159455`, verified `support_connected: true`, and logged `No generated changes to publish`.
- Added 2026-06-02: Generated shelf now writes `support.html`, `llms.txt`, and `llms-full.txt`. Homepage/archive/bundle/import/pack pages link the support surface; the starter bundle includes the support and AI discovery files; sitemap and IndexNow include them. Commit `f90b8d9` pushed to `main`.
- Verified 2026-06-02: GitHub Pages deployment `26805338049` succeeded for `f90b8d9`. Live `support.html`, `llms.txt`, `llms-full.txt`, `sitemap.xml`, and `status.json` returned HTTP 200 and include the support URL/boundary. `verify-system.ps1` now checks 33 files with bundle `304,869` bytes, store import ZIP `161,610` bytes, and pack download aggregate `126,854` bytes.
- Verified 2026-06-02: IndexNow accepted 29 support/discovery URLs with HTTP 200 and a follow-up dry run showed `submit_count: 0`. GitHub fallback publisher run `26805392972` succeeded on `f90b8d9`, verified `files_checked: 33` and `support_connected: true`, and logged `No generated changes to publish`.
- Added 2026-06-02: Generated shelf now writes support-backed collection offer pages under `docs/offers/`: offer index, `offers/offers.json`, and 5 topic collection pages. The pages group related public packs, expose CollectionPage JSON-LD, link the starter bundle, and route the primary CTA to `https://gift.calmsprout.com` while stating product checkout is not connected. Commit `5d6eec6` pushed to `main`.
- Verified 2026-06-02: GitHub Pages deployment `26805912605` succeeded for `5d6eec6`. Live `offers/`, `offers/small-business-ops.html`, `offers/offers.json`, `sitemap.xml`, and `status.json` returned HTTP 200; status reports `offer_pages_ready: true`, `offer_page_count: 5`, `bundle_bytes: 323728`, `store_import_zip_bytes: 161610`, `support_connected: true`, and `store_connected: false`.
- Verified 2026-06-02: Browser QA passed locally for `offers/small-business-ops.html`: correct page title, nonblank content, no framework overlay, no console warnings/errors, support/download links visible, product-checkout guardrail visible, and `Browse topic` navigated to the matching topic page.
- Verified 2026-06-02: IndexNow accepted 21 changed offer/support/discovery URLs with HTTP 200 and a follow-up dry run showed `submit_count: 0`. GitHub fallback publisher run `26805969926` succeeded on `5d6eec6`, verified `files_checked: 36`, `bundle_bytes: 323728`, `support_connected: true`, `store_connected: false`, and logged `No generated changes to publish`.
- Added 2026-06-02: Generated shelf now writes `pay-what-you-can.html` as a support-first bundle funnel, includes it in the starter archive, sitemap, status, and LLM discovery files, and keeps the page explicit that product checkout is not connected while `store_connected` is false.
- Verified 2026-06-02: `verify-system.ps1` passed with `files_checked: 37`, `bundle_bytes: 326576`, `store_import_zip_bytes: 161610`, `support_connected: true`, and `store_connected: false`; GitHub Pages deployments for the pay funnel and handoff commits completed successfully.
- Verified 2026-06-02: CalmSprout Worker commit `49b00c2` deployed LLM discovery routes as version `7d733d3e-4db2-4268-a618-9f1c33fbb90c`; live `/llms.txt`, `/llms-full.txt`, and `/daily-shelf/llms.txt` returned HTTP 200 text files with the branded pay route, Square support path, and checkout boundary.
- Verified 2026-06-02: CalmSprout Worker commit `9401218` deployed bridge aliases as version `c3a3f5b4-551b-4074-95e9-a0264ff88f1c`; live `/daily-shelf/today` and `/daily-shelf/bundle` returned HTTP 200 first-party pages, `/daily-shelf/status` resolved to public `status.json` with `store_connected: false`, browser QA found no console issues, and IndexNow accepted 13 CalmSprout bridge/discovery URLs with HTTP 200.
- Added 2026-06-02: Commit `e50f94e` (`Add support monetization metadata`) adds `support_page_url`, `pay_what_you_can_url`, `monetization_destination_type`, `monetization_destination_url`, `store_connected`, and `support_connected` to catalog/import JSON and CSV, adds public support/pay URLs to `status.json`, and adds support-mode `DonateAction` JSON-LD to generated pack pages. Pages run `26808927786` succeeded; live metadata checks passed; IndexNow accepted 8 changed shelf URLs with HTTP 200; `store_connected` remains false.
- Verified 2026-06-02: CalmSprout Worker commit `0c509a0` deployed branded data aliases as version `737bd883-dc0a-4610-ac60-4e29ec4b29d1`; live `/daily-shelf/status`, `/status.json`, `/catalog.json`, `/catalog.csv`, `/store-listings.json`, `/store-listings.csv`, `/feed.json`, `/feed.xml`, `/atom.xml`, and `/starter.zip` returned HTTP 200; metadata routes include support/pay fields, starter ZIP returned 328,177 bytes, and IndexNow accepted 22 CalmSprout bridge/data URLs with HTTP 200.
- Added 2026-06-02: Daily Shelf commit `4bad33c` (`Add CalmSprout IndexNow automation`) adds `tools/submit_calmsprout_indexnow.py`, wires it into `run-daily.ps1` and `.github/workflows/daily-shelf.yml`, ignores `state/calmsprout-indexnow-state.json`, and expands verifier coverage to `files_checked: 40`.
- Verified 2026-06-02: `tools/submit_calmsprout_indexnow.py --all --wait-for-key-seconds 90` verified `https://www.calmsprout.com/a4f604db6d2046939ff6c7e3d29d341e.txt` with HTTP 200, submitted 25 CalmSprout bridge/data URLs with HTTP 200, and follow-up dry runs returned `submit_count: 0`. GitHub Pages deployment `26809864174` succeeded for `4bad33c`; `verify-system.ps1` passed with `files_checked: 40`, `support_connected: true`, and `store_connected: false`.
- Verified 2026-06-02: CalmSprout Worker commit `6786fe0` (`Add dynamic Daily Shelf current pack routes`) deployed as version `91486cba-f17b-4525-8ff8-6f99baab0399`; live `/daily-shelf` and `/daily-shelf/today` render the current pack from `status.json`, live `/daily-shelf/today.zip` and `/daily-shelf/current.zip` proxy the current 5,869-byte pack ZIP, `llms.txt` and `sitemap.xml` list `today.zip`, and browser QA found no console messages on `/daily-shelf/today`.
- Added 2026-06-02: Daily Shelf commit `d3221af` (`Track CalmSprout current pack routes`) adds `/daily-shelf`, `/daily-shelf/today`, `/daily-shelf/today.zip`, and `/daily-shelf/current.zip` to the default CalmSprout IndexNow candidate set. Forced `tools/submit_calmsprout_indexnow.py --all --force --wait-for-key-seconds 90` accepted 27 URLs with HTTP 200 and follow-up dry runs returned `submit_count: 0`; Pages run `26810528589` succeeded.
- Verified 2026-06-02: CalmSprout Worker commit `557e6c5` (`Add Daily Shelf product catalog page`) deployed as version `51bd5adb-e134-4e90-8be4-e628d5727368`; live `/daily-shelf/products` and `/daily-shelf/browse` return first-party catalog pages with 21 product cards, support state, and checkout-boundary text. Live `/daily-shelf/downloads/2026-06-02-one-page-sop.zip` returns a 5,869-byte ZIP with `PK` signature; browser QA found no console messages on desktop products and mobile browse views.
- Added 2026-06-02: Daily Shelf commit `c68c63a` (`Track CalmSprout product catalog routes`) adds `/daily-shelf/products` and `/daily-shelf/browse` to the default CalmSprout IndexNow candidate set and verifier expectations. GitHub Pages run `26811230682` succeeded; `tools/submit_calmsprout_indexnow.py --all --wait-for-key-seconds 90` accepted those two URLs with HTTP 200 and follow-up dry runs returned `submit_count: 0`.
- Verified 2026-06-02: CalmSprout Worker commit `9194d08` (`Add Daily Shelf product detail routes`) deployed as version `2dc1f4d3-a6bf-4af4-aec7-9fef87539100`; live `/daily-shelf/products/2026-06-02-one-page-sop` returns a first-party product detail page with related packs, support state, checkout-boundary text, and first-party ZIP CTA. Live `/daily-shelf/packs/2026-06-02-one-page-sop/` proxies the public pack page; browser QA found no console messages or mobile horizontal overflow.
- Added 2026-06-02: Daily Shelf commit `cc21a51` (`Track CalmSprout product detail routes`) adds 21 catalog-derived `/daily-shelf/products/<pack-slug>` URLs to the default CalmSprout IndexNow candidate set and verifier expectations. GitHub Pages run `26811768255` succeeded; `tools/submit_calmsprout_indexnow.py --all --wait-for-key-seconds 90` accepted all 21 detail URLs with HTTP 200 and follow-up dry runs returned `submit_count: 0`.
- Verified 2026-06-02: CalmSprout Worker commit `d8af561` (`Add Daily Shelf dynamic product sitemap`) deployed as version `738a15ee-3f18-44b1-b92d-cf75d865f0f6`; live `/sitemap.xml` includes 44 URLs including the current product detail page and `/daily-shelf/product-sitemap.xml`, and live `/daily-shelf/product-sitemap.xml` lists 21 product detail URLs. Browser QA loaded the product sitemap with no console messages.
- Added 2026-06-02: Daily Shelf commit `8b42dce` (`Track CalmSprout product sitemap routes`) adds `/sitemap.xml` and `/daily-shelf/product-sitemap.xml` to the default CalmSprout IndexNow candidate set and verifier expectations. GitHub Pages run `26812212317` succeeded; `tools/submit_calmsprout_indexnow.py --all --wait-for-key-seconds 90` accepted both sitemap URLs with HTTP 200 and follow-up dry runs returned `submit_count: 0`.
- Verified 2026-06-02: CalmSprout Worker commit `3001f49` (`Add Daily Shelf product support funnels`) deployed as version `8777e666-af2d-40db-bcbc-317dccf50560`; live `/daily-shelf/products/2026-06-02-one-page-sop/support` returns a product-specific support funnel with Square support CTA, suggested support tiers, and checkout-boundary text. The live product detail page links to this support route, and the product sitemap now includes product support URLs. Browser QA found no console messages or mobile horizontal overflow.
- Added 2026-06-02: Daily Shelf commit `41949c7` (`Track CalmSprout product support routes`) adds 21 catalog-derived `/daily-shelf/products/<pack-slug>/support` URLs to the default CalmSprout IndexNow candidate set and verifier expectations. GitHub Pages run `26812672540` succeeded; `tools/submit_calmsprout_indexnow.py --all --wait-for-key-seconds 90` accepted all 21 support URLs with HTTP 200 and follow-up dry runs returned `submit_count: 0`.

## Operator Rule

- Keep this file honest. Record stable truths, not wishful plans.
- Update current task and handoff files when the lane materially changes.
- If a payout/store/ad/affiliate platform is connected, record the exact public URL and the non-secret setup state here.
