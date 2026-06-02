# Daily Autodigital Shelf Worker Status

## Status

- Operator: `DAI-AUT-01`
- Project: `daily-autodigital-shelf`
- State: idle
- Last updated: `2026-06-02T07:55:00-04:00`
- Active broker action: none

## Latest Verified Work

- Public site: `https://x26dotapp.github.io/daily-autodigital-shelf/`
- Current pack: `One-Page SOP Builder`
- Latest handoff update: support-aware download pages and CalmSprout proxied download-page routing recorded
- Latest functional commit: `de0b29a` (`Add support-aware download pages`)
- Latest adjacent bridge commit: CalmSprout `f063a55` (`Add Daily Shelf bridge`)
- Latest CalmSprout commits: `d8fa6d9` (`Add Daily Shelf landing page`), `8a689e1` (`Add CalmSprout IndexNow key`), `8d4d298` (`Add Daily Shelf pay bridge`), `49b00c2` (`Add Daily Shelf LLM discovery`), `9401218` (`Add Daily Shelf bridge aliases`), `0c509a0` (`Add Daily Shelf data aliases`), `6786fe0` (`Add dynamic Daily Shelf current pack routes`), `557e6c5` (`Add Daily Shelf product catalog page`), `9194d08` (`Add Daily Shelf product detail routes`), `d8af561` (`Add Daily Shelf dynamic product sitemap`), `3001f49` (`Add Daily Shelf product support funnels`), `6b5e7bf` (`Add Daily Shelf support intent redirects`), `2821d51` (`Expose support intent in LLM discovery`), `392479e` (`Record support intent LLM deploy`), `187a1b6` (`Add product offer FAQ schema`), `874504d` (`Record product offer FAQ schema deploy`), `53b3183` (`Route shelf downloads through landing pages`), and `1d44688` (`Proxy Daily Shelf stylesheet`)
- CalmSprout deploy: Cloudflare Worker version `4be3afcc-a783-43d4-a442-32777a74acfd`
- Pages deployment: `26816113707` for support-aware download pages; prior ZIP artifact deployment `26815383934` succeeded for `ab350a5`
- Fallback proof: run `26805969926` verified `files_checked: 36`, `support_connected: true`, `store_connected: false`, and logged `No generated changes to publish`
- Verification: `verify-system.ps1` passed with `files_checked: 40`, `bundle_bytes: 361321`, current `download_bytes: 6875`, `store_import_zip_bytes: 182765`, `monetization_enabled: true`, `support_connected: true`, `store_connected: false`
- Discovery: IndexNow accepted 88 GitHub Pages URLs, then 100 and 31 CalmSprout URLs with HTTP 200 after adding support-aware download pages; follow-up dry runs returned `submit_count: 0` for both hosts
- Support/discovery surfaces: `support.html`, `pay-what-you-can.html`, `llms.txt`, and `llms-full.txt` are generated
- Support metadata: catalog/import JSON and CSV expose `support_page_url`, `pay_what_you_can_url`, `monetization_destination_type`, `monetization_destination_url`, `store_connected`, and `support_connected`; current pack JSON-LD exposes `DonateAction` while only support mode is connected
- Branded support metadata: catalog/import JSON and CSV expose `branded_product_url`, `branded_support_url`, and `branded_support_intent_url`; `status.json` exposes `today_branded_product_url`, `today_branded_support_url`, and `today_branded_support_intent_url`
- Pay-what-you-can QA: local browser loaded the page with no console errors and verified the support CTA reaches `https://app.squareup.com/gift/MLZ021BP45QKH/order`
- Offer surfaces: `offers/index.html`, `offers/offers.json`, and 5 topic collection offer pages are live
- Branded bridge: `https://www.calmsprout.com/daily-shelf` and `/daily-shelf/today` dynamically render the current pack from shelf status; `/daily-shelf/today.zip` and `/daily-shelf/current.zip` proxy the current pack ZIP; `/daily-shelf/pay` and `/daily-shelf/bundle` are first-party support funnel pages; `/daily-shelf/offers` and `/daily-shelf/support` redirect to the offer index and Square support page; `/daily-shelf/status`, `/daily-shelf/status.json`, `/daily-shelf/catalog.json`, `/daily-shelf/catalog.csv`, `/daily-shelf/store-listings.json`, `/daily-shelf/store-listings.csv`, `/daily-shelf/feed.json`, `/daily-shelf/feed.xml`, `/daily-shelf/atom.xml`, and `/daily-shelf/starter.zip` proxy public shelf data/assets under the CalmSprout domain; `www.calmsprout.com` homepage contains the Daily Shelf banner; CalmSprout `robots.txt`, `sitemap.xml`, `llms.txt`, `llms-full.txt`, and IndexNow key file are live
- CalmSprout discovery: IndexNow accepted 22 bridge/data URLs with HTTP 200
- CalmSprout IndexNow automation: `tools/submit_calmsprout_indexnow.py` is wired into `run-daily.ps1` and the GitHub fallback publisher so changed branded data/feed/archive routes are submitted after successful shelf publishes
- CalmSprout alias QA: live browser loaded `/daily-shelf/today` and `/daily-shelf/bundle` with no console issues; live `/daily-shelf/status` resolved to `status.json` with `store_connected: false`
- CalmSprout data QA: live branded status/catalog/import/feed routes returned HTTP 200; metadata routes include support/pay fields; `/daily-shelf/starter.zip` returned 328,177 bytes
- CalmSprout current-pack QA: live `/daily-shelf/today` returned HTTP 200 with `One-Page SOP Builder`, the current ZIP CTA, support state, and product-checkout boundary; live browser QA found no console messages; `/daily-shelf/today.zip` and `/daily-shelf/current.zip` returned 5,869-byte ZIP responses
- CalmSprout product catalog QA: live `/daily-shelf/products` and `/daily-shelf/browse` returned HTTP 200 with 21 product cards, `One-Page SOP Builder`, support state, and product-checkout boundary; live browser QA found no console messages and no mobile horizontal overflow; `/daily-shelf/downloads/2026-06-02-one-page-sop.zip` returned a 5,869-byte ZIP response
- CalmSprout product detail QA: live `/daily-shelf/products/2026-06-02-one-page-sop` returned HTTP 200 with related packs, support state, product-checkout boundary, and first-party ZIP CTA; live `/daily-shelf/packs/2026-06-02-one-page-sop/` proxied the public pack page; live browser QA found no console messages and no mobile horizontal overflow
- CalmSprout product sitemap QA: live `/sitemap.xml` returned HTTP 200 with 44 URLs including product detail URLs and `/daily-shelf/product-sitemap.xml`; live `/daily-shelf/product-sitemap.xml` returned HTTP 200 with 21 product detail URLs; browser QA found no console messages
- CalmSprout product support QA: live `/daily-shelf/products/2026-06-02-one-page-sop/support` returned HTTP 200 with Square support CTA, suggested support tiers, and primary CTA `/daily-shelf/products/2026-06-02-one-page-sop/support/go`; live `/support/go` returned HTTP 302 to the Square support page with CalmSprout UTM attribution; browser QA found no console messages and no desktop/mobile horizontal overflow
- CalmSprout LLM QA: live `/llms.txt` and `/llms-full.txt` returned HTTP 200 with `/support/go` and `branded_support_intent_url`; cache-busted `/daily-shelf/llms.txt` and `/daily-shelf/llms-full.txt` verified the same deployed Worker content
- CalmSprout product offer/FAQ schema QA: live `/daily-shelf/products/2026-06-02-one-page-sop` returned HTTP 200 with JSON-LD `CreativeWork`/`Product`, a free-public-download `Offer`, product-specific `DonateAction` to `/support/go`, `FAQPage`, and a visible FAQ section; desktop/mobile QA found no console messages and no horizontal overflow
- Static pack offer/FAQ schema QA: live GitHub Pages `/packs/2026-06-02-one-page-sop/` returned HTTPS browser proof with JSON-LD `CreativeWork`, `Product`, `FAQPage`, free `Offer` price `0.00` `USD`, product support-intent href, visible FAQ, no console warnings/errors, and no horizontal overflow
- ZIP support-card QA: live GitHub Pages current product ZIP and starter archive both contain `SUPPORT.txt` with `/support/go` and `Product checkout is not connected`
- Support-aware download-page QA: live GitHub Pages `/downloads/2026-06-02-one-page-sop.html` and CalmSprout `/daily-shelf/downloads/2026-06-02-one-page-sop.html` return rendered landing pages with `DownloadAction`, `DonateAction`, a direct ZIP button, `/support/go`, and the product-checkout boundary; browser QA found no console warnings/errors and no horizontal overflow. Live CalmSprout `/daily-shelf/products/2026-06-02-one-page-sop` now routes its primary CTA to the download page and still exposes ZIP encoding metadata.
- Support destination: `https://gift.calmsprout.com` resolves to the Square-hosted CalmSprout gift/support page

## Boundaries

- This lane is revenue infrastructure, not verified revenue.
- No live trading, store checkout, affiliate endpoint, or proven daily revenue
  is connected yet.
- A public support endpoint is connected and recorded, but do not mark
  autonomous income complete until actual revenue or a real product checkout
  path is proven.
