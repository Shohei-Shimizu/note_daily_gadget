# Claude handoff: 2026-07-10 Prime Day extra article

Codex research prep is complete for the Prime Day extra article draft.

## Status

| Date | Title | Research | Items | URL audit | Publication status |
|---|---|---:|---:|---|---|
| 2026-07-10 | 【Amazonプライムデー】値下げ幅が大きいお得ガジェット 20 選 | `06_research/2026-07/2026-07-10_prime_day_research_data.json` | 20 | PASS | Draft only; live confirmation required before publish |

## Critical confidentiality note

- Deal Hub information, including sale target status, sale price, discount amount, and discount rate, is Amazon Associates confidential information until each product is actually live on Amazon.co.jp.
- Do not publish or imply that any selected item is confirmed as a Prime Day deal until the 2026-07-10 pre-publication live check is complete.
- In the draft, avoid exact prices, discount rates, "セール対象確定", "何%OFF", "最安級", and similar claims.
- Use wording such as "候補", "公開直前に価格を確認", "セール開始後に差し替え予定" only in internal draft notes, not in the final public article.

## Notes for writing

- All 20 `selected_items[*].asin` values are present and match the ASIN in each Amazon URL.
- All Amazon URLs use the `daily-gadget-22` affiliate tag.
- The current data was assembled from existing PA-API-acquired research JSON because direct PA-API access failed from this environment on 2026-07-04 with a DNS resolution error. Do not treat the current price fields as live sale data.
- `selected_items[*].price` is intentionally `N/A`; price and discount copy must be filled only after the live confirmation pass.
- The list is category-mixed by design: Amazon devices, charging gear, smart home, desk peripherals, tablet/storage, audio, video creation, robot cleaning, and creator desk equipment.
- Amazon device entries are limited to Echo Show 15 and Kindle Scribe. Do not add Fire TV or other Amazon devices unless Codex refreshes the data later.
- SwitchBot appears twice: Hub 2 and the Alexa-compatible circulator. Keep their use cases separate.
- Logitech appears twice: MX Master 3S and MX Keys S. Avoid repeating the same "作業効率" phrasing in both sections.
- Samsung T9 and Crucial X10 Pro are both 2TB portable SSDs. Differentiate them by positioning, not by unverified speed comparisons beyond the provided feature text.
- DJI Osmo Action 5 Pro and Insta360 Flow 2 Pro are different shooting tools. Do not describe the Insta360 item as an action camera.
- Roborock Q7B+ is a robot vacuum candidate. Confirm model name and live availability before making any sale-price statement.

## Required before final publication

- Run a 2026-07-10 live check for all 20 Amazon pages.
- Confirm each item is actually on sale on Amazon.co.jp at publication time.
- Replace `N/A` with the verified public sale price only if available on the live product page.
- Add discount rate or discount amount only after it is visible publicly on Amazon.co.jp.
- Remove or replace any item that is out of stock, no longer discounted, or has a changed ASIN.

## 2026-07-07 live-check update (PA-API retry)

- PA-API connectivity: FAILED. Attempted `GetItems` against `https://webservices.amazon.co.jp/paapi5/getitems` in two ASIN batches of 10. Both failed before authentication/offer lookup with DNS resolution error: `URLError gaierror(8, 'nodename nor servname provided, or not known')` for `webservices.amazon.co.jp`.
- Pricing update: none. No `price`, `sale_price`, `discount_rate`, or `list_price` values were changed because no current Amazon.co.jp offer data was returned.
- URL/ASIN audit: PASS for all 20. Every selected URL uses `tag=daily-gadget-22` and `linkCode=osi`, and every `/dp/<ASIN>` matches `selected_items[*].asin`.
- JSON update: added `sale_context.live_check`, refreshed `sale_context.price_discount_status`, refreshed `url_audit.checked_at`, and recorded `search_execution.latest_pa_api_attempt`.

| ASIN | Sale status | JSON/handoff update |
|---|---|---|
| B0C7Y1N38H | Unverified due to PA-API DNS failure; no sale status confirmed | Pricing untouched; status documented |
| B0CZ9SX1GW | Unverified due to PA-API DNS failure; no sale status confirmed | Pricing untouched; status documented |
| B0BZ87C549 | Unverified due to PA-API DNS failure; no sale status confirmed | Pricing untouched; status documented |
| B0D53XL7GL | Unverified due to PA-API DNS failure; no sale status confirmed | Pricing untouched; status documented |
| B0BM8VS13P | Unverified due to PA-API DNS failure; no sale status confirmed | Pricing untouched; status documented |
| B0C9TKSP8V | Unverified due to PA-API DNS failure; no sale status confirmed | Pricing untouched; status documented |
| B0B6GL3N8D | Unverified due to PA-API DNS failure; no sale status confirmed | Pricing untouched; status documented |
| B0C9PYN7RN | Unverified due to PA-API DNS failure; no sale status confirmed | Pricing untouched; status documented |
| B0DK59YKRS | Unverified due to PA-API DNS failure; no sale status confirmed | Pricing untouched; status documented |
| B0FR8KBS5K | Unverified due to PA-API DNS failure; no sale status confirmed | Pricing untouched; status documented |
| B0C65F55K5 | Unverified due to PA-API DNS failure; no sale status confirmed | Pricing untouched; status documented |
| B0DXFC2WC9 | Unverified due to PA-API DNS failure; no sale status confirmed | Pricing untouched; status documented |
| B0CHFS9K14 | Unverified due to PA-API DNS failure; no sale status confirmed | Pricing untouched; status documented |
| B0CCYKY4T4 | Unverified due to PA-API DNS failure; no sale status confirmed | Pricing untouched; status documented |
| B0DW3RWMNM | Unverified due to PA-API DNS failure; no sale status confirmed | Pricing untouched; status documented |
| B0F1MZJTB7 | Unverified due to PA-API DNS failure; no sale status confirmed | Pricing untouched; status documented |
| B0DS2DF5S5 | Unverified due to PA-API DNS failure; no sale status confirmed | Pricing untouched; status documented |
| B0G64QDV8J | Unverified due to PA-API DNS failure; no sale status confirmed | Pricing untouched; status documented |
| B0F6NRWF9V | Unverified due to PA-API DNS failure; no sale status confirmed | Pricing untouched; status documented |
| B0DZCCPH3V | Unverified due to PA-API DNS failure; no sale status confirmed | Pricing untouched; status documented |
