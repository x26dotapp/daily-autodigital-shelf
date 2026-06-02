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
- Verified 2026-06-02: CalmSprout Worker commit `6b5e7bf` (`Add Daily Shelf support intent redirects`) deployed as version `f571cf59-c42e-4781-ad71-7fc8e2861646`; live `/daily-shelf/products/2026-06-02-one-page-sop/support` returns HTTP 200 and its primary CTA points to `/daily-shelf/products/2026-06-02-one-page-sop/support/go`. Live `/daily-shelf/products/2026-06-02-one-page-sop/support/go` returns HTTP 302 to the Square support page with `utm_source=calmsprout`, `utm_medium=daily_shelf`, `utm_campaign=product_support`, and `utm_content=2026-06-02-one-page-sop`. Browser QA found no console messages and no desktop/mobile horizontal overflow. CalmSprout record commit `a255b23` records the deploy locally; Daily Shelf CalmSprout IndexNow dry run returned `candidate_count: 72` and `submit_count: 0`. Store checkout remains disconnected and daily revenue is not proven.
- Added 2026-06-02: Daily Shelf commit `6179a74` (`Expose branded support intent metadata`) adds generated CalmSprout branded product/support/support-intent URL fields to catalog/import rows, current branded support URLs to `status.json`, and support-intent lines to `llms.txt`/`llms-full.txt`. Pages run `26813575995` succeeded. Live GitHub Pages and CalmSprout status/catalog JSON expose `/support/go`; `verify-system.ps1` passed with `bundle_bytes: 330836`, `store_import_zip_bytes: 163692`, `support_connected: true`, and `store_connected: false`; IndexNow accepted 9 GitHub Pages URLs and 65 CalmSprout URLs with HTTP 200, and follow-up dry runs returned `submit_count: 0`.
- Verified 2026-06-02: CalmSprout Worker commit `2821d51` (`Expose support intent in LLM discovery`) deployed as version `37cbc214-76e9-4568-b3ed-8656c70db132`; live `/llms.txt` and `/llms-full.txt` include `/support/go` and `branded_support_intent_url`, and cache-busted `/daily-shelf/llms.txt` plus `/daily-shelf/llms-full.txt` verified the same deployed content. CalmSprout record commit `392479e` records the deploy locally. Product checkout remains disconnected and daily revenue is not proven.
- Verified 2026-06-02: CalmSprout Worker commit `187a1b6` (`Add product offer FAQ schema`) deployed as version `4108d3fb-3cb6-444f-88db-9914c995a967`; live `/daily-shelf/products/2026-06-02-one-page-sop` exposes JSON-LD `CreativeWork`/`Product`, a free-public-download `Offer`, product-specific `DonateAction` to `/support/go`, `FAQPage`, and a visible FAQ section. Desktop/mobile QA found no console messages and no horizontal overflow. CalmSprout record commit `874504d` records the deploy locally. Forced CalmSprout IndexNow submission accepted 72 URLs with HTTP 200, and the follow-up dry run returned `submit_count: 0`. Product checkout remains disconnected and daily revenue is not proven.
- Added 2026-06-02: Daily Shelf commit `90a4853` (`Add static product offer FAQ schema`) refreshes deterministic historical pack pages, so all 21 static pack pages expose JSON-LD `CreativeWork`/`Product`, free-public-download `Offer`, product-specific `DonateAction` to CalmSprout `/support/go`, `FAQPage`, and visible FAQ copy. It rebuilt all 21 product ZIPs plus starter/import ZIPs. Pages run `26814777758` succeeded; live HTTPS browser QA on the current pack page found the schema, support-intent href, visible FAQ, no console warnings/errors, and no horizontal overflow. `verify-system.ps1` passed with `bundle_bytes: 351257`, `pack_download_bytes: 137039`, `store_import_zip_bytes: 173842`, `support_connected: true`, and `store_connected: false`.
- Added 2026-06-02: Daily Shelf commit `bd1b187` (`Track CalmSprout proxied pack routes`) adds `/daily-shelf/packs/{slug}/` and `/daily-shelf/downloads/{slug}.zip` to the CalmSprout IndexNow candidate set. Pages run `26814868699` succeeded. IndexNow accepted 24 GitHub Pages static schema URLs, 9 CalmSprout data/bundle URLs, and 42 newly tracked CalmSprout proxied pack/ZIP URLs with HTTP 200; follow-up dry runs returned `submit_count: 0` for both hosts. Product checkout remains disconnected and daily revenue is not proven.
- Added 2026-06-02: Daily Shelf commit `6cbeba1` (`Add support cards to pack downloads`) adds `SUPPORT.txt` to every generated pack ZIP and to the starter archive. Each pack card records the pack page, ZIP URL, product support page, product-specific CalmSprout `/support/go`, voluntary-support text, and `Product checkout is not connected`. Pages run `26815277958` succeeded; live ZIP checks verified the current product ZIP and starter archive both contain `SUPPORT.txt`, `/support/go`, and the checkout boundary. `verify-system.ps1` passed with `bundle_bytes: 360116`, `pack_download_bytes: 148948`, `store_import_zip_bytes: 182206`, `support_connected: true`, and `store_connected: false`.
- Added 2026-06-02: Daily Shelf commit `ab350a5` (`Track zip artifacts in IndexNow`) adds starter archive ZIP, store upload kit ZIP, current ZIP, and all catalog product ZIPs to the GitHub Pages IndexNow submitter. Pages run `26815383934` succeeded. IndexNow accepted 23 direct GitHub Pages ZIP artifact URLs and 30 CalmSprout download/data URLs with HTTP 200 after the support-card change. Product checkout remains disconnected and daily revenue is not proven.
- Added 2026-06-02: Daily Shelf commit `de0b29a` (`Add support-aware download pages`) generates 21 public `docs/downloads/<pack>.html` landing pages with JSON-LD `DownloadAction`, product-specific `DonateAction`, direct ZIP buttons, voluntary support text, and the product-checkout boundary. Catalog/import rows now expose `download_page_url`; `status.json` exposes `today_download_page` and `pack_download_page_count`; sitemap and IndexNow include the generated pages. GitHub Pages run `26816113707` succeeded; `verify-system.ps1` passed with `files_checked: 40`, `bundle_bytes: 361321`, current `download_bytes: 6875`, `store_import_zip_bytes: 182765`, `support_connected: true`, and `store_connected: false`.
- Verified 2026-06-02: CalmSprout commits `53b3183` (`Route shelf downloads through landing pages`) and `1d44688` (`Proxy Daily Shelf stylesheet`) deploy the branded product CTAs to `/daily-shelf/downloads/<pack>.html`, include proxied download pages in the dynamic product sitemap, keep ZIP `encoding` metadata, and proxy `/daily-shelf/styles.css` so proxied shelf pages render correctly. Latest Cloudflare Worker version is `4be3afcc-a783-43d4-a442-32777a74acfd`. Live browser QA passed on GitHub Pages `/downloads/2026-06-02-one-page-sop.html`, CalmSprout `/daily-shelf/products/2026-06-02-one-page-sop`, and CalmSprout `/daily-shelf/downloads/2026-06-02-one-page-sop.html` with no console warnings/errors and no horizontal overflow.
- Verified 2026-06-02: IndexNow accepted 88 changed GitHub Pages URLs with HTTP 200 for the support-aware download pages, then accepted 100 and 31 changed CalmSprout URLs with HTTP 200 for the branded product/download/support route set. Follow-up dry runs returned `candidate_count: 99`, `submit_count: 0` for GitHub Pages and `candidate_count: 135`, `submit_count: 0` for CalmSprout. Product checkout remains disconnected and daily revenue is not proven.
- Added 2026-06-02: Daily Shelf commit `0a5d3da` (`Add public product feed`) adds `product-feed.json`, `product-feed.xml`, and `product-feed.csv` with 21 public product/download/support records, product-specific CalmSprout `/support/go` fields, and the explicit `Product checkout is not connected` boundary. The feed files are linked from the homepage, sitemap, status, LLM discovery files, and store upload kit. GitHub Pages run `26816697269` succeeded; `verify-system.ps1` passed with `files_checked: 43`, `bundle_bytes: 375773`, `store_import_zip_bytes: 197650`, `support_connected: true`, and `store_connected: false`.
- Verified 2026-06-02: CalmSprout commit `8d70dc3` (`Proxy Daily Shelf product feeds`) deployed as Worker version `da74cb60-539e-4717-8be2-696257d252b3`. Live GitHub Pages and CalmSprout product-feed JSON/XML/CSV URLs returned HTTP 200 with 21 items, `One-Page SOP Builder`, product-specific `/support/go`, and the checkout boundary. IndexNow accepted 11 GitHub Pages URLs and 15 CalmSprout URLs with HTTP 200; follow-up dry runs returned `candidate_count: 102`, `submit_count: 0` for GitHub Pages and `candidate_count: 138`, `submit_count: 0` for CalmSprout. Product checkout remains disconnected and daily revenue is not proven.
- Added 2026-06-02: Daily Shelf commit `468f34f` (`Add support funnel feed`) adds `support-funnel.json`, `support-funnel.xml`, and `support-funnel.csv` with 21 public download-to-support records, `DownloadAction`, `DonateAction`, product-specific `branded_support_intent_url`, `utm_campaign=product_support`, suggested support tiers, and the explicit `Product checkout is not connected` boundary. The feed files are linked from the homepage, sitemap, status, LLM discovery files, and store upload kit. GitHub Pages run `26817314700` succeeded; `verify-system.ps1` passed with `files_checked: 46`, `bundle_bytes: 389716`, `store_import_zip_bytes: 211788`, `support_connected: true`, and `store_connected: false`.
- Verified 2026-06-02: CalmSprout commit `c8c0833` (`Proxy Daily Shelf support funnel feed`) deployed as Worker version `28df22d3-2e56-4107-9545-cca23922a759`. Live GitHub Pages and CalmSprout support-funnel JSON/XML/CSV URLs returned HTTP 200 with 21 items, `One-Page SOP Builder`, support-intent fields, UTM fields, suggested support tiers, and the checkout boundary. Browser QA on local homepage found the support-funnel link, no console warnings/errors, and no horizontal overflow. IndexNow accepted 11 GitHub Pages URLs and 15 CalmSprout URLs with HTTP 200; follow-up dry runs returned `candidate_count: 105`, `submit_count: 0` for GitHub Pages and `candidate_count: 141`, `submit_count: 0` for CalmSprout. Product checkout remains disconnected and daily revenue is not proven.
- Added 2026-06-02: CalmSprout commit `95534a5` (`Track Daily Shelf support metrics`) binds Cloudflare KV namespace `DAILY_SHELF_METRICS` and exposes `https://www.calmsprout.com/daily-shelf/support-metrics.json` as aggregate support-intent telemetry. It counts hits to `/daily-shelf/products/<pack-slug>/support/go` and stores no IP, user-agent, cookie, email, or payment data. Worker version `f5e2ec27-2098-4fc3-a2c6-f59fc1ab38dd` is live.
- Verified 2026-06-02: Daily Shelf commit `8d097a9` (`Track CalmSprout support metrics route`) adds `/daily-shelf/support-metrics.json` to the CalmSprout IndexNow submitter and verifier; Pages run `26817774688` succeeded. Live metrics returned `storage_connected: true`; sitemap and `llms.txt` include the metrics route; one synthetic verification redirect changed `total_support_intent_clicks` from `0` to `1` for `2026-06-02-one-page-sop`. IndexNow accepted the metrics route with HTTP 200 and follow-up dry runs returned `candidate_count: 142`, `submit_count: 0`. This is click measurement only, not payment or daily revenue proof.
- Added 2026-06-02: Daily Shelf commit `0b72b3a` (`Backfill full 29 pack inventory`) backfilled the remaining deterministic templates so the public shelf now has 29 pack pages, 29 product ZIPs, 29 support-aware download pages, 29 product-feed items, 29 support-funnel items, 29 store-import rows, and a 517,838-byte starter archive while preserving `One-Page SOP Builder` as the June 2 current pack. GitHub Pages run `26819825807` succeeded. Live GitHub Pages verified `status.json`, the new `Weekly Reset Board` pack/download page, and `product-feed.json`; live CalmSprout verified the new product/support pages, product sitemap, digital-product-prep collection count, and offers feed. `verify-system.ps1` passed with `pack_count: 29`, `files_checked: 46`, `bundle_bytes: 517838`, `store_import_zip_bytes: 286183`, `support_connected: true`, and `store_connected: false`. IndexNow accepted 58 GitHub Pages URLs and 133 CalmSprout URLs with HTTP 200; follow-up dry runs returned `submit_count: 0` for both hosts. This is inventory/discovery expansion, not payment or daily revenue proof.
- Added 2026-06-02: Daily Shelf commit `e4df7be` (`Add collection bundle downloads`) generated 5 focused collection bundle ZIPs under `docs/bundles/`, added `collection_bundle_path` and `collection_bundle_url` to `offers.json`, added bundle URLs to `sitemap.xml` and `status.json`, and teaches both IndexNow submitters to publish the new ZIP routes. GitHub Pages run `26820505998` succeeded. `status.json` reports `collection_bundle_ready: true`, `collection_bundle_count: 5`, and `collection_bundle_bytes: 1064282`; the starter archive is now 518,112 bytes. CalmSprout commit `39eba70` (`Proxy Daily Shelf collection bundles`) deployed as Worker version `4e8c2013-14e1-4c02-a574-affa4c1e8837`, proxies `/daily-shelf/bundles/<topic-slug>-collection.zip`, adds those URLs to the sitemap, and exposes a first-party `Download collection bundle` CTA. Live QA verified GitHub Pages and CalmSprout `digital-product-prep-collection.zip` returned matching 417,334-byte ZIP files with `SUPPORT.txt`, voluntary support text, and the `Product checkout is not connected` boundary; live offer pages and feeds expose the new bundle metadata. `verify-system.ps1` passed with `pack_count: 29`, `bundle_bytes: 518112`, `store_import_zip_bytes: 286183`, `support_connected: true`, and `store_connected: false`. IndexNow accepted 13 GitHub Pages URLs and 32 CalmSprout URLs with HTTP 200; follow-up dry runs returned `submit_count: 0` for both hosts. No new synthetic support click was triggered; live metrics remain `total_support_intent_clicks: 4`. This is conversion/discovery infrastructure, not payment or daily revenue proof.
- Verified 2026-06-02: CalmSprout commit `c9da4c5` (`Render Daily Shelf collection hub`) replaces the `/daily-shelf/offers` redirect with a first-party collection hub containing topic collection cards, collection bundle CTAs, measured collection support links, `CollectionPage`/`ItemList` JSON-LD, and the product-checkout boundary. Cloudflare Worker version `619efb27-1bb6-44b4-a460-90b82f3d5579` is live. Live HTTP QA verified `/daily-shelf/offers` returns HTTP 200 HTML without redirect, includes `CalmSprout collection hub`, `/daily-shelf/bundles/digital-product-prep-collection.zip`, `/daily-shelf/offers/small-business-ops/support/go`, and `Product checkout is not connected`. Browser QA verified page identity, nonblank rendered content, no framework overlay, no console warnings/errors, and opening the `digital-product-prep` offer from the hub lands on the first-party collection offer with bundle/support links intact. `verify-system.ps1` passed with `pack_count: 29`, `bundle_bytes: 518112`, `store_import_zip_bytes: 286183`, `support_connected: true`, and `store_connected: false`. IndexNow accepted 205 forced CalmSprout URLs with HTTP 200; follow-up dry runs returned `submit_count: 0` for both hosts. No support redirect was triggered; live metrics remain `total_support_intent_clicks: 4`. This is conversion/discovery infrastructure, not payment or daily revenue proof.
- Verified 2026-06-02: CalmSprout commit `f7e38dd` (`Render Daily Shelf support funnel`) replaces the `/daily-shelf/support` redirect with a first-party support funnel page while keeping `/daily-shelf/support/go` as the measured external Square redirect. Cloudflare Worker version `ac785aa2-c6d1-4d54-9e27-6180e7476c6d` is live. Live HTTP QA verified `/daily-shelf/support` returns HTTP 200 HTML without redirect, includes `CalmSprout shelf support`, suggested `$3`/`$9`/`$21` tiers, the newest pack `One-Page SOP Builder`, `/daily-shelf/support/go`, product/collection browse links, `DonateAction` JSON-LD, and the `Product checkout is not connected` / not-revenue-proof boundary. Browser QA verified page identity, nonblank rendered content, no framework overlay, no console warnings/errors, and safe internal navigation from the support page to `/daily-shelf/offers`. `verify-system.ps1` passed with `pack_count: 29`, `bundle_bytes: 518112`, `store_import_zip_bytes: 286183`, `support_connected: true`, and `store_connected: false`. IndexNow accepted 205 forced CalmSprout URLs with HTTP 200; follow-up dry runs returned `submit_count: 0` for both hosts. No support redirect was triggered; live metrics remain `total_support_intent_clicks: 4`. This is conversion/discovery infrastructure, not payment or daily revenue proof.
- Added 2026-06-02: Daily Shelf commit `36869dc` (`Add Daily Shelf use case pages`) generates `docs/use-cases/` with 5 buyer-intent collection pages and `use-cases/use-cases.json`. The generator adds use-case URLs to `status.json`, `sitemap.xml`, `llms-full.txt`, starter bundle contents, collection bundle contents, and both IndexNow submitters. GitHub Pages run `26822426886` succeeded. CalmSprout commit `f1916d5` (`Proxy Daily Shelf use case pages`) deployed as Worker version `a8ff54c7-723c-4a11-9ff6-aea6fca90e33`, proxies `/daily-shelf/use-cases/`, `/daily-shelf/use-cases/<slug>.html`, `/daily-shelf/use-cases/use-cases.json`, and includes use-case URLs in `https://www.calmsprout.com/sitemap.xml`. Live HTTP QA verified GitHub Pages and CalmSprout use-case JSON/page routes return HTTP 200; browser QA verified styled, nonblank GitHub and branded use-case index/detail pages with no console warnings/errors. `verify-system.ps1` passed with `files_checked: 49`, `use_case_page_count: 5`, `bundle_bytes: 543481`, `support_connected: true`, and `store_connected: false`. IndexNow accepted 21 GitHub Pages URLs and 43 CalmSprout URLs with HTTP 200; follow-up dry runs returned `submit_count: 0` for both hosts. No support redirect was triggered; live metrics remain `total_support_intent_clicks: 4`. This is discovery/conversion infrastructure, not payment or daily revenue proof.

- 2026-06-02 evergreen template pages: Daily Shelf commit `7b91c1f` (`Add
  evergreen template pages`) generates `docs/templates/` with 29 stable
  non-dated template landing pages and `templates/templates.json`. The generator
  wires template URLs into `status.json`, `sitemap.xml`, starter and collection
  bundles, `llms.txt`/`llms-full.txt`, and both IndexNow submitters. GitHub
  Pages run `26823553947` succeeded. CalmSprout commit `d8e1350` (`Proxy Daily
  Shelf template pages`) deployed as Worker version
  `cfb8cff2-62ee-4843-ab4d-a0ce7d1c3bf1`, proxies `/daily-shelf/templates/`,
  `/daily-shelf/templates/<slug>.html`, `/daily-shelf/templates.json`, and
  `/daily-shelf/templates/templates.json`, and includes template URLs in
  `https://www.calmsprout.com/sitemap.xml`. Live HTTP QA verified GitHub Pages
  and CalmSprout template JSON/page routes return HTTP 200; browser QA verified
  styled, nonblank GitHub and branded template index/detail pages with no
  console warnings/errors. `verify-system.ps1` passed with `files_checked: 52`,
  `template_page_count: 29`, `bundle_bytes: 625876`, `support_connected: true`,
  and `store_connected: false`. IndexNow accepted 45 GitHub Pages URLs and 67
  CalmSprout URLs with HTTP 200; follow-up dry runs returned `submit_count: 0`
  for both hosts. No support redirect was triggered; live metrics remain
  `total_support_intent_clicks: 4`. This is discovery/conversion
  infrastructure, not payment or daily revenue proof.

- 2026-06-02 template support attribution: Daily Shelf commit `24ec523` (`Add
  template support attribution`) adds stable template-level support page and
  intent URLs to `templates/templates.json`, template landing pages,
  `status.json`, generated starter/collection bundles, verifier coverage, and
  the CalmSprout IndexNow submitter. GitHub Pages run `26824392886` succeeded.
  CalmSprout commit `436a80c` (`Measure Daily Shelf template support routes`)
  deployed as Worker version `d7c26f5f-4b97-4181-ac94-340b315fab26`, renders
  `/daily-shelf/templates/<template-slug>/support`, measures
  `/daily-shelf/templates/<template-slug>/support/go` with
  `utm_campaign=template_support` and `utm_content=template-<slug>`, and adds
  template support pages to `https://www.calmsprout.com/sitemap.xml`. Live HTTP
  QA verified GitHub Pages and CalmSprout `one-page-sop` template routes return
  HTTP 200 and expose `/daily-shelf/templates/one-page-sop/support/go`; live
  `/daily-shelf/templates/one-page-sop/support` returns HTTP 200 with the
  Square CTA and `Product checkout is not connected` boundary. Browser QA found
  no console warnings/errors and no horizontal overflow on the support page or
  proxied template detail page. `verify-system.ps1` passed with
  `files_checked: 52`, `template_page_count: 29`, `bundle_bytes: 626093`,
  `support_connected: true`, and `store_connected: false`. IndexNow accepted 37
  GitHub Pages URLs and 121 CalmSprout URLs with HTTP 200; follow-up dry runs
  returned `submit_count: 0` for both hosts. No support redirect was triggered;
  live metrics remain `total_support_intent_clicks: 4`. This is conversion
  attribution infrastructure, not payment or daily revenue proof.

- 2026-06-02 CalmSprout first-party template hub: CalmSprout commit `c43a8a1`
  (`Render Daily Shelf template hub`) replaces the proxied
  `/daily-shelf/templates/` index with a first-party CalmSprout template hub
  while preserving `/daily-shelf/templates/<template-slug>.html`,
  `/daily-shelf/templates/<template-slug>/support`, and measured
  `/daily-shelf/templates/<template-slug>/support/go` routes. Cloudflare Worker
  version `f5d86dd0-e75f-4b48-9af1-dd5c84d264b3` is live. Live HTTP QA
  verified `/daily-shelf/templates/` returns HTTP 200 with
  `CalmSprout template hub`, the `one-page-sop` support/detail/download links,
  `CollectionPage`/`ItemList` JSON-LD, and the `Product checkout is not
  connected` / revenue-unverified boundary; `/daily-shelf/templates` redirects
  to the trailing slash and the proxied template detail page remains HTTP 200.
  Browser QA on a narrow viewport verified 29 rendered template cards, no
  console warnings/errors, no horizontal overflow, and expected
  support/detail/download links. Forced CalmSprout IndexNow submission accepted
  303 URLs with HTTP 200 and follow-up dry run returned `submit_count: 0`. No
  support redirect was triggered; live metrics remain
  `total_support_intent_clicks: 4`. This is discovery/conversion
  infrastructure, not payment or daily revenue proof.

- 2026-06-02 Daily Shelf guide pages: Daily Shelf commit `0ce22b6` (`Add Daily
  Shelf guide pages`) generates `docs/guides/` with 29 stable how-to guide
  pages plus `guides/guides.json`, and wires guide URLs into `status.json`,
  `sitemap.xml`, starter/collection bundles, store import kit, LLM discovery,
  verifier coverage, and both IndexNow submitters. GitHub Pages run
  `26826182871` succeeded. CalmSprout commit `8cc6ca3` (`Proxy Daily Shelf
  guide pages`) deployed as Worker version
  `5ef35b32-4cca-469a-9056-f53ce2a348d4`, proxies `/daily-shelf/guides/`,
  `/daily-shelf/guides/<template-slug>.html`, `/daily-shelf/guides.json`, and
  `/daily-shelf/guides/guides.json`, and includes guide URLs in
  `https://www.calmsprout.com/sitemap.xml`. Live HTTP QA verified GitHub Pages
  and CalmSprout guide routes return HTTP 200; CalmSprout guide JSON returns
  `@type: ItemList` with 29 items; the `one-page-sop` guide contains
  `HowTo`/`FAQPage` JSON-LD, download/template/support links, and the
  `Product checkout is not connected` boundary. Browser QA found no console
  errors and no horizontal overflow. `verify-system.ps1` passed with
  `files_checked: 55`, `guide_page_count: 29`, `bundle_bytes: 863286`,
  `store_import_zip_bytes: 445994`, `support_connected: true`, and
  `store_connected: false`. IndexNow accepted 46 GitHub Pages URLs and 335
  CalmSprout URLs with HTTP 200; follow-up dry runs returned `submit_count: 0`
  for both hosts. No support redirect was triggered; live metrics remain
  `total_support_intent_clicks: 4`. This is search/discovery infrastructure,
  not payment or daily revenue proof.

- 2026-06-02 sponsor support pages: Daily Shelf commit `8516a4b` (`Add Daily
  Shelf sponsor support pages`) generates `sponsor.html`, `commercial-use.html`,
  and `sponsor-kit.json`, and wires them into `status.json`, `sitemap.xml`,
  starter/collection bundles, store import kit, LLM discovery, verifier
  coverage, and both IndexNow submitters. GitHub Pages run `26827270859`
  succeeded. CalmSprout commit `e17752e` (`Proxy Daily Shelf sponsor pages`)
  deployed as Worker version `4da9f662-7e37-4416-890f-7f7c230966d2`, proxies
  `/daily-shelf/sponsor`, `/daily-shelf/commercial-use`, and
  `/daily-shelf/sponsor-kit.json`, and includes those URLs in
  `https://www.calmsprout.com/sitemap.xml`. Live HTTP QA verified GitHub Pages
  and CalmSprout sponsor/commercial routes return HTTP 200 with the measured
  `/daily-shelf/support/go` support path, `FAQPage`/`DonateAction` schema, and
  the `Product checkout is not connected` boundary. CalmSprout sponsor-kit JSON
  returns `@type: ItemList`, 5 support tiers, `support_connected: true`,
  `store_connected: false`, and `support_intent_url:
  https://www.calmsprout.com/daily-shelf/support/go`. Browser QA found no
  console errors and no horizontal overflow on the branded sponsor page.
  `verify-system.ps1` passed with `files_checked: 58`,
  `sponsor_tier_count: 5`, `bundle_bytes: 876212`,
  `store_import_zip_bytes: 452552`, `support_connected: true`, and
  `store_connected: false`. IndexNow accepted 20 GitHub Pages URLs and 338
  CalmSprout URLs with HTTP 200; follow-up dry runs returned `submit_count: 0`
  for both hosts. No support redirect was triggered; live metrics remain
  `total_support_intent_clicks: 4`. This is buyer-intent support
  infrastructure, not payment or daily revenue proof.

- 2026-06-02 sponsor/commercial support attribution: Daily Shelf commits
  `b7f0ea8` (`Attribute sponsor support routes`) and `0e935da` (`Cover
  CalmSprout static page aliases`) route sponsor CTAs through
  `https://www.calmsprout.com/daily-shelf/sponsor/support/go`, route
  commercial/internal-use CTAs through
  `https://www.calmsprout.com/daily-shelf/commercial-use/support/go`, expose
  sponsor/commercial/general support intent URLs in `sponsor-kit.json` and
  `status.json`, and add the new intent/static alias routes to the CalmSprout
  IndexNow submitter and verifier. GitHub Pages runs `26827996984` and
  `26828288446` succeeded. CalmSprout commits `e472359` (`Measure sponsor
  support redirects`) and `a660a6f` (`Add Daily Shelf static aliases`) deployed
  as Worker versions `b2f3b3b8-db00-4755-a107-f60932134ca7` and
  `a7f5a23a-6dc4-41bf-a667-a46b94a93863`; the Worker now measures sponsor and
  commercial support separately and proxies `/daily-shelf/commercial-use.html`,
  `/daily-shelf/sponsor.html`, `/daily-shelf/starter-bundle.html`,
  `/daily-shelf/support.html`, `/daily-shelf/license.html`,
  `/daily-shelf/privacy.html`, and `/daily-shelf/terms.html`. Live QA verified
  sponsor/commercial pages, sponsor kit, sitemap, all seven aliases, and browser
  rendering with no console errors or horizontal overflow. IndexNow accepted 5
  GitHub Pages URLs and 347 CalmSprout URLs; follow-up dry runs returned
  `submit_count: 0`. No support redirect was triggered; live metrics remain
  `total_support_intent_clicks: 4`. This is attribution/conversion
  infrastructure, not payment or daily revenue proof.

- 2026-06-02 pricing support surface: Daily Shelf commit `6255269` (`Add Daily
  Shelf pricing support page`) generates `pricing.html`, adds pricing fields to
  `status.json` and `sponsor-kit.json`, wires pricing into `sitemap.xml`,
  starter/store-import bundles, LLM discovery, verifier coverage, and the
  IndexNow submitters. Follow-up commits `9d71846` (`Index Daily Shelf pricing
  page`) and `3c8c2a7` (`Index CalmSprout Daily Shelf sitemap alias`) keep the
  GitHub pricing URL and branded `/daily-shelf/sitemap.xml` alias in unattended
  indexing coverage. GitHub Pages runs `26829045827`, `26829362677`, and
  `26829419355` succeeded. CalmSprout commit `f1cef1a` (`Proxy Daily Shelf
  pricing page`) deployed as Worker version
  `fbf34331-4e2b-477e-ac9e-172c12a710dd`, proxies `/daily-shelf/pricing` and
  `/daily-shelf/pricing.html`, measures `/daily-shelf/pricing/support/go`, and
  serves `/daily-shelf/sitemap.xml`. Live QA verified GitHub Pages
  `pricing.html`, CalmSprout pricing aliases, root sitemap, Daily Shelf sitemap
  alias, `llms.txt`, and `llms-full.txt` return HTTP 200 with pricing/support
  URLs, `OfferCatalog`, `FAQPage`, `DonateAction`, and the
  `Product checkout is not connected` boundary. Browser QA at 1280x720 and
  390x844 found no console errors and no horizontal overflow. `verify-system.ps1`
  passed with `files_checked: 58`, `bundle_bytes: 882541`,
  `store_import_zip_bytes: 455745`, `support_connected: true`, and
  `store_connected: false`. IndexNow accepted 12 GitHub Pages URLs, then the
  new pricing URL, then 350 CalmSprout URLs, then the branded sitemap alias;
  follow-up dry runs returned `submit_count: 0` for both hosts. No support
  redirect was triggered; live metrics remain `total_support_intent_clicks: 4`.
  This is buyer-intent support infrastructure, not payment or daily revenue
  proof.

- 2026-06-02 general support funnel attribution: Daily Shelf commit `7d86844`
  (`Route support funnels through measured support intent`) routes generated
  `support.html` and `pay-what-you-can.html` CTAs and `DonateAction` JSON-LD
  through measured `https://www.calmsprout.com/daily-shelf/support/go` while
  keeping `https://gift.calmsprout.com` visible as the external Square support
  destination. The generated starter archive and 5 collection bundles were
  refreshed because they embed the updated support/pay pages. GitHub Pages run
  `26830081016` succeeded. Live QA verified GitHub Pages `support.html` and
  `pay-what-you-can.html`, CalmSprout `/daily-shelf/support.html`, and
  `/daily-shelf/pay-what-you-can` return HTTP 200 with measured support intent
  and the product-checkout boundary; browser QA found no console errors and no
  horizontal overflow on support desktop and pay mobile. `verify-system.ps1`
  passed with `files_checked: 58`, `bundle_bytes: 882620`,
  `support_connected: true`, and `store_connected: false`. IndexNow accepted 9
  GitHub Pages URLs and 37 CalmSprout URLs; follow-up dry runs returned
  `submit_count: 0` for both hosts. No support redirect was triggered; live
  metrics remain `total_support_intent_clicks: 4`. This is
  attribution/conversion infrastructure, not payment or daily revenue proof.

- 2026-06-02 CalmSprout bridge support ladder: CalmSprout commit `fdcbd94`
  (`Surface pricing paths on Daily Shelf bridge`) updates `/daily-shelf`,
  `/daily-shelf/pay`, `/daily-shelf/bundle`, and `/daily-shelf/support` so the
  first-party bridge surfaces expose `/daily-shelf/pricing`,
  `/daily-shelf/commercial-use`, `/daily-shelf/sponsor`, and measured
  `/daily-shelf/support/go` paths. Cloudflare Worker version
  `42c2c27f-487a-49d2-af85-3170476dfd12` is live. Live HTTP and browser QA
  verified the landing, pay, bundle, and support pages return HTTP 200, expose
  pricing/commercial/sponsor/support links, keep the product-checkout boundary
  visible, have no console errors, and have no horizontal overflow at 1280x720
  and 390x844. IndexNow accepted 351 forced CalmSprout URLs; follow-up dry run
  returned `submit_count: 0`. No support redirect was triggered; live metrics
  remain `total_support_intent_clicks: 4` with `support_connected: true` and
  `store_connected: false`. This is conversion-path infrastructure, not payment
  or daily revenue proof.

- 2026-06-02 unattended publishing schedule QA: Windows Scheduled Tasks
  `HUMANi Daily Autodigital Shelf` and
  `HUMANi Daily Autodigital Shelf Watchdog` are registered, `Ready`, and point
  at `C:\GitHub\x26dotapp\daily-autodigital-shelf\run-daily.ps1` and
  `watchdog.ps1`. Both ran successfully on 2026-06-02 with `LastTaskResult: 0`;
  next runs are 2026-06-03 6:10am and 7:15am America/New_York. Current
  `verify-system.ps1` passed with `pack_count: 29`, `files_checked: 58`,
  `support_connected: true`, `store_connected: false`, and confirmed the GitHub
  fallback workflow plus CalmSprout IndexNow automation. The watchdog status
  file reports `status: ok`, `failures: 0`, and `repair_attempts: 0`.

- 2026-06-02 collection bundle landing pages: Daily Shelf commit `ee1a729`
  (`Add collection bundle landing pages`) generated 5 focused collection bundle
  product pages under `docs/bundles/*-collection.html`, added
  `collection_bundle_page_path`, `collection_bundle_page_url`, and
  `collection_bundle_branded_page_url` to `offers.json`, added page paths/counts
  to `status.json`, added the URLs to `sitemap.xml`, and wired both IndexNow
  submitters plus verifier coverage. GitHub Pages run `26831541576` succeeded.
  CalmSprout commit `ea1db61` (`Index Daily Shelf bundle pages`) adds the
  bundle page URLs to the branded dynamic sitemap; Cloudflare Worker version
  `39c6e94a-2ce2-475b-86c2-28d8fd2e236f` is live. `verify-system.ps1` passed
  with `pack_count: 29`, `collection_bundle_page_count: 5`, `files_checked: 63`,
  `support_connected: true`, and `store_connected: false`. Live QA verified
  GitHub Pages and CalmSprout `small-business-ops-collection.html` return HTTP
  200 with collection ZIP CTA, measured collection support CTA,
  `Product`/`FAQPage`/`DownloadAction`/`DonateAction` JSON-LD, and the
  `Product checkout is not connected` boundary. Browser QA at 1280x720 and
  390x844 found no console errors and no horizontal overflow. IndexNow accepted
  19 GitHub Pages URLs and 39 CalmSprout URLs; follow-up dry runs returned
  `submit_count: 0`. No support redirect was triggered; live metrics remain
  `total_support_intent_clicks: 4`. This is higher-value conversion
  infrastructure, not payment or daily revenue proof.

- 2026-06-02 CalmSprout homepage bundle promotion: CalmSprout commit `0f38441`
  (`Promote Daily Shelf bundle page`) adds a direct
  `/daily-shelf/bundles/small-business-ops-collection.html` link to the
  homepage Daily Shelf banner, dynamic `/daily-shelf` landing,
  `/daily-shelf/pay`, `/daily-shelf/support`, root sitemap, `llms.txt`, and
  `llms-full.txt`. Cloudflare Worker version
  `d0f5beb5-a772-4e18-8228-a7f0d839ae75` is live. `node --check
  src/worker.js`, `npm test`, `npm run build`, and `npx wrangler deploy
  --dry-run` passed before deploy. Live HTTP QA verified homepage,
  `/daily-shelf`, `/daily-shelf/pay`, `/daily-shelf/support`, root sitemap,
  LLM discovery files, and the small-business bundle page return HTTP 200 and
  expose the route where expected. Browser QA at 1280x720 and 390x844 found the
  new link visible on the entry pages with no console errors and no horizontal
  overflow. IndexNow accepted 356 forced CalmSprout URLs; follow-up dry run
  returned `submit_count: 0`. No support redirect was triggered; live metrics
  remain `total_support_intent_clicks: 4`, `support_connected: true`, and
  `store_connected: false`. This is conversion-path infrastructure, not payment
  or daily revenue proof.

- 2026-06-02 public preferred bundle promotion: Daily Shelf commit `bc14553`
  (`Promote preferred collection bundle`) adds the deterministic preferred
  route `bundles/small-business-ops-collection.html` to the generated public
  homepage, `support.html`, `pay-what-you-can.html`, `llms.txt`,
  `llms-full.txt`, and `status.json` fields
  `preferred_collection_bundle_*`. GitHub Pages run `26832639314` succeeded.
  `python -m py_compile` passed for the generator/verifier/submitters, and
  `verify-system.ps1` passed with `pack_count: 29`, `files_checked: 63`,
  `collection_bundle_page_count: 5`, `bundle_bytes: 882979`,
  `support_connected: true`, and `store_connected: false`. Live HTTP QA
  verified GitHub Pages homepage/support/pay/LLM/status routes and CalmSprout
  proxied support/pay aliases return HTTP 200 and expose
  `small-business-ops-collection.html`. Browser QA at 1280x720 and 390x844
  found the preferred bundle links visible on the public homepage/support/pay
  pages with no console errors and no horizontal overflow. IndexNow accepted
  212 GitHub Pages URLs and 356 CalmSprout URLs; follow-up dry runs returned
  `submit_count: 0` for both hosts. No support redirect was triggered; live
  metrics remain `total_support_intent_clicks: 4`, `support_connected: true`,
  and `store_connected: false`. This is conversion-path infrastructure, not
  payment or daily revenue proof.

- 2026-06-02 generated support-card asset: Daily Shelf commits `da88826`,
  `7eabae3`, and `10011b1` add a deterministic
  `docs/assets/support-card.svg`, embed it on generated support,
  pay-what-you-can, pricing, starter bundle, and collection bundle pages,
  include it in the starter archive and all collection bundle ZIPs, expose
  `support_card_*` fields in `status.json`, and add verifier plus IndexNow
  coverage. CalmSprout commit `493c162` proxies
  `/daily-shelf/assets/support-card.svg`; commit `3bb171d` records Worker
  version `bdd64ce9-cf85-4a4c-8857-60147f5e6d25`. GitHub Pages run
  `26833933357` succeeded for `10011b1`. `verify-system.ps1` passed with
  `pack_count: 29`, `files_checked: 63`, `bundle_bytes: 884701`,
  `store_import_zip_bytes: 455945`, `support_connected: true`, and
  `store_connected: false`. Live HTTP QA verified GitHub Pages and CalmSprout
  SVG/page routes return HTTP 200 with inline constrained support-card markup;
  support metrics stayed `total_support_intent_clicks: 4`. Browser QA at
  1280x720 and 390x844 on fresh CalmSprout support/starter routes found the
  card image loaded, link target `/daily-shelf/support/go`, no console
  warnings/errors, no framework overlay, and no horizontal overflow. IndexNow
  accepted 213 GitHub Pages URLs and 357 CalmSprout URLs; follow-up dry runs
  returned `submit_count: 0` for both hosts. A prior normal-path browser click
  showed stale cached pre-inline starter markup, so current proof uses fresh
  published markup and inline sizing prevents recurrence after cache refresh.
  This is conversion-path support infrastructure, not payment or daily revenue
  proof.

## Operator Rule

- Keep this file honest. Record stable truths, not wishful plans.
- Update current task and handoff files when the lane materially changes.
- If a payout/store/ad/affiliate platform is connected, record the exact public URL and the non-secret setup state here.
