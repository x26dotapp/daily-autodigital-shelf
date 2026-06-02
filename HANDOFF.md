# Daily Autodigital Shelf Handoff

## Project State

Daily Autodigital Shelf is a public static site plus a local daily generator. The generator creates one dated digital pack per run, writes printable worksheet/checklist/cover assets, updates the homepage, writes `docs/status.json`, appends `state/ledger.jsonl`, then the wrapper can commit and push the changed site.

This is revenue infrastructure, not guaranteed revenue. It does not touch live funds, run trading, send lead messages, create accounts, or claim that money is being earned before a real buyer/platform/payout path exists.

Verified 2026-06-02:

- Public site: `https://x26dotapp.github.io/daily-autodigital-shelf/`
- Branded entry: `https://www.calmsprout.com/daily-shelf`
- Branded pay funnel: `https://www.calmsprout.com/daily-shelf/pay`
- Branded aliases: `https://www.calmsprout.com/daily-shelf/today`, `https://www.calmsprout.com/daily-shelf/products`, `https://www.calmsprout.com/daily-shelf/browse`, `https://www.calmsprout.com/daily-shelf/bundle`, `https://www.calmsprout.com/daily-shelf/status`, `https://www.calmsprout.com/daily-shelf/catalog.json`, and `https://www.calmsprout.com/daily-shelf/starter.zip`
- Repo: `https://github.com/x26dotapp/daily-autodigital-shelf`
- Task: `HUMANi Daily Autodigital Shelf`, daily at 06:10 local time, last manual run result `0`
- Watchdog task: `HUMANi Daily Autodigital Shelf Watchdog`, daily at 07:15 local time, last Task Scheduler run result `0`
- Pack: `One-Page SOP Builder`
- Starter archive: 21 packs dated `2026-05-13` through `2026-06-02`
- Individual downloads: 21 product ZIPs under `downloads/`; all seeded pack pages now include `Download pack ZIP`
- Bundle surface: `starter-bundle.html` and `bundles/starter-archive.zip` live; current local ZIP size is 328,177 bytes and includes policy pages, support page, pay-what-you-can page, offer pages, `llms.txt`, `llms-full.txt`, and RSS/Atom feed files
- Import surface: `store-import.html`, `imports/store-listings.csv`, `imports/store-listings.json`, and `imports/store-upload-kit.zip` live; import ZIP is 162,402 bytes and rows include topic fields, support/pay URLs, monetization destination fields, and policy pages
- Support/discovery surfaces: `support.html`, `pay-what-you-can.html`, `llms.txt`, and `llms-full.txt` live; the support and pay-what-you-can pages link to `https://gift.calmsprout.com` while stating that product checkout is not connected
- Offer surfaces: `offers/index.html`, `offers/offers.json`, and 5 topic collection offer pages live; offer pages link the starter bundle, expose CollectionPage JSON-LD, route support CTAs to `https://gift.calmsprout.com`, and state that product checkout is not connected
- CalmSprout bridge: `C:\scripts\CalmSprout` commits `f063a55` (`Add Daily Shelf bridge`), `d8fa6d9` (`Add Daily Shelf landing page`), `8a689e1` (`Add CalmSprout IndexNow key`), `8d4d298` (`Add Daily Shelf pay bridge`), `49b00c2` (`Add Daily Shelf LLM discovery`), `9401218` (`Add Daily Shelf bridge aliases`), `0c509a0` (`Add Daily Shelf data aliases`), `6786fe0` (`Add dynamic Daily Shelf current pack routes`), and `557e6c5` (`Add Daily Shelf product catalog page`) deployed directly to Cloudflare. Latest Worker version is `51bd5adb-e134-4e90-8be4-e628d5727368`. Live `https://www.calmsprout.com/daily-shelf` and `/daily-shelf/today` now render the current pack from live shelf status; `/daily-shelf/products` and `/daily-shelf/browse` render the live catalog as first-party product cards; `/daily-shelf/today.zip`, `/daily-shelf/current.zip`, and `/daily-shelf/downloads/<pack>.zip` proxy public pack ZIPs; `/daily-shelf/pay` and `/daily-shelf/bundle` are first-party support funnel pages; `/daily-shelf/offers` redirects to the offer index; `/daily-shelf/support` redirects to the public Square support page; `/daily-shelf/status`, `/daily-shelf/catalog.json`, `/daily-shelf/catalog.csv`, `/daily-shelf/store-listings.json`, `/daily-shelf/store-listings.csv`, `/daily-shelf/feed.json`, `/daily-shelf/feed.xml`, `/daily-shelf/atom.xml`, and `/daily-shelf/starter.zip` proxy public shelf data/assets under the CalmSprout domain; `robots.txt`, `sitemap.xml`, `llms.txt`, `llms-full.txt`, and public IndexNow key file `a4f604db6d2046939ff6c7e3d29d341e.txt` are live; the `www.calmsprout.com` homepage includes Daily Shelf banner links for offers, products, today, bundle, pay, and support.
- Topic surfaces: `topics/index.html`, 5 topic pages, and `topics/topics.json` live; seeded pack pages link related topics and topic URLs are in catalog/import outputs
- Policy surfaces: `terms.html`, `privacy.html`, `license.html`, and `refund-policy.html` live; they are store-readiness pages and do not activate checkout or payout
- Metadata: generated pages include Open Graph image tags, Twitter summary-card tags, richer JSON-LD for products and listing surfaces, and support-mode product `DonateAction` structured data when `store_connected` is false
- Catalog/discovery surfaces: `archive.html`, `catalog.json`, `catalog.csv`, `feed.json`, `feed.xml`, `atom.xml`, `llms.txt`, `llms-full.txt`, `sitemap.xml`, `robots.txt`; catalog/import JSON and CSV expose `support_page_url`, `pay_what_you_can_url`, `monetization_destination_type`, `monetization_destination_url`, `store_connected`, and `support_connected`
- Feed proof: live `feed.xml` returned HTTP 200 with 10,552 bytes; live `atom.xml` returned HTTP 200 with 8,706 bytes; both contain `One-Page SOP Builder`
- Discovery: IndexNow key files are live for both the GitHub Pages shelf and CalmSprout branded bridge. Latest direct `tools/submit_indexnow.py --all --wait-for-key-seconds 90` submitted 8 support-metadata URLs and received HTTP 200. Latest direct `tools/submit_calmsprout_indexnow.py --all --force --wait-for-key-seconds 90` submitted 27 CalmSprout current-pack/bridge/data URLs and received HTTP 200.
- GitHub fallback publisher: `.github/workflows/daily-shelf.yml` is active. It runs daily after the local PC task/watchdog, can be run manually, generates/verifies, commits only on changed output, pushes to `main`, submits Daily Shelf IndexNow when it commits, and now submits changed CalmSprout current-pack/data/feed/archive routes to IndexNow.
- Fallback proof: manual run `26805969926` completed successfully on commit `5d6eec6` and logged `No generated changes to publish`
- Determinism: generator normalizes text bytes inside ZIPs, fixes ZIP creator metadata, forces LF CSV output, and tracks `.gitattributes` so Windows and GitHub runners do not churn same-day artifacts
- Latest functional infrastructure commit: `c68c63a` (`Track CalmSprout product catalog routes`) pushed to `main`; GitHub Pages deployment `26811230682` succeeded
- Live verifier: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\verify-system.ps1`
- Monetization: public support destination connected; public site says `Status: Connected`, shows `Support this shelf`, and links to `https://gift.calmsprout.com`, which resolves to the Square-hosted CalmSprout gift/support page. Product checkout is not connected, `store_connected` is false, and daily revenue is not proven.
- Direct deploy note: CalmSprout has local Git but no remote, so bridge changes were committed locally before direct Wrangler deploy. Keep future CalmSprout changes committed locally and record deployed Worker version IDs.
- Latest verifier baseline: `files_checked: 40`, `bundle_bytes: 328177`, `pack_download_bytes: 126887`, `store_import_zip_bytes: 162402`, `support_connected: true`, `store_connected: false`
- Pay-what-you-can proof: local browser QA loaded `pay-what-you-can.html`, found the generated support tiers and starter ZIP link, reported no console errors, and verified the hero support CTA navigated to `https://app.squareup.com/gift/MLZ021BP45QKH/order`.
- CalmSprout discovery proof: public key `https://www.calmsprout.com/a4f604db6d2046939ff6c7e3d29d341e.txt` returned HTTP 200; IndexNow accepted 6 CalmSprout URLs with HTTP 202: homepage, `/daily-shelf`, `/daily-shelf/offers`, `/daily-shelf/support`, `robots.txt`, and `sitemap.xml`.
- CalmSprout pay proof: live `https://www.calmsprout.com/daily-shelf/pay` returned HTTP 200 with the support tiers, starter ZIP link, and Square support CTA; browser QA found no console errors; IndexNow accepted 7 CalmSprout URLs including `/daily-shelf/pay` and `/daily-shelf/pay-what-you-can` with HTTP 200.
- CalmSprout LLM discovery proof: live `https://www.calmsprout.com/llms.txt`, `/llms-full.txt`, and `/daily-shelf/llms.txt` returned HTTP 200 text files with the branded pay route, Square support path, and checkout boundary; IndexNow accepted 10 CalmSprout URLs with HTTP 200.
- CalmSprout alias proof: live `https://www.calmsprout.com/daily-shelf/today` and `/daily-shelf/bundle` returned HTTP 200 first-party pages with support links and product-checkout boundary text; `/daily-shelf/status` resolved to public `status.json` with `store_connected: false`; live browser QA found no console issues; IndexNow accepted 13 CalmSprout bridge/discovery URLs with HTTP 200.
- Support metadata proof: live `catalog.json`, `imports/store-listings.json`, and `status.json` returned HTTP 200 with `support_page_url`, `pay_what_you_can_url`, `monetization_destination_url`, and `store_connected`; live current pack page returned HTTP 200 with `DonateAction`; IndexNow accepted 8 changed shelf URLs with HTTP 200.
- CalmSprout data alias proof: live `https://www.calmsprout.com/daily-shelf/status`, `/status.json`, `/catalog.json`, `/catalog.csv`, `/store-listings.json`, `/store-listings.csv`, `/feed.json`, `/feed.xml`, `/atom.xml`, and `/starter.zip` returned HTTP 200; metadata routes expose support/pay monetization fields and starter ZIP returned 328,177 bytes; CalmSprout `llms.txt` and `sitemap.xml` include the branded data aliases; IndexNow accepted 22 CalmSprout bridge/data URLs with HTTP 200.
- CalmSprout IndexNow automation proof: Daily Shelf commit `4bad33c` adds `tools/submit_calmsprout_indexnow.py`, wires it into `run-daily.ps1` and `.github/workflows/daily-shelf.yml`, ignores `state/calmsprout-indexnow-state.json`, and expands verifier coverage. Direct `tools/submit_calmsprout_indexnow.py --all --wait-for-key-seconds 90` verified the public CalmSprout key with HTTP 200, submitted 25 branded URLs with HTTP 200, and follow-up dry runs returned `submit_count: 0`. `verify-system.ps1` passed after Pages run `26809864174` with `files_checked: 40`, `support_connected: true`, and `store_connected: false`.
- CalmSprout current-pack route proof: CalmSprout commit `6786fe0` deployed as Worker version `91486cba-f17b-4525-8ff8-6f99baab0399`; live `/daily-shelf` and `/daily-shelf/today` returned HTTP 200 with `One-Page SOP Builder`, `Download today's ZIP`, support-connected text, and product-checkout boundary text. Live `/daily-shelf/today.zip` and `/daily-shelf/current.zip` returned HTTP 200 ZIP responses with 5,869 bytes and `PK` signature. Browser QA on live `/daily-shelf/today` found no console messages. Daily Shelf commit `d3221af` adds those routes to the CalmSprout IndexNow submitter; forced submission accepted 27 URLs with HTTP 200 and follow-up dry runs returned `submit_count: 0`.
- CalmSprout product catalog proof: CalmSprout commit `557e6c5` deployed as Worker version `51bd5adb-e134-4e90-8be4-e628d5727368`; live `/daily-shelf/products` and `/daily-shelf/browse` returned HTTP 200 with 21 product cards, `One-Page SOP Builder`, support-connected text, and product-checkout boundary text. Live `/daily-shelf/downloads/2026-06-02-one-page-sop.zip` returned HTTP 200 with 5,869 bytes and `PK` signature. Browser QA on live `/daily-shelf/products` and mobile `/daily-shelf/browse` found no console messages and no horizontal overflow. Daily Shelf commit `c68c63a` adds these routes to the CalmSprout IndexNow submitter; GitHub Pages deployment `26811230682` succeeded; IndexNow accepted `/daily-shelf/products` and `/daily-shelf/browse` with HTTP 200 and follow-up dry runs returned `submit_count: 0`.

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
- `C:\GitHub\x26dotapp\daily-autodigital-shelf\docs\pay-what-you-can.html`
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
