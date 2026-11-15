# Weekly recheck notes: 15 Nov 2026

Hand-checked official pricing pages and Shopify App Store listings for all 25 support and search apps Stillprice tracks. Date of check: Sunday 15 Nov 2026 (Africa/Johannesburg). Fetched over HTTPS with curl, then Playwright where the page is a JavaScript shell.

These notes go with the 15 Nov updates in /workspace/microbiz/shopai-ledger (data/apps.json, data/search_apps.json, changelog and /price-moves). A copy also lives at data/recheck-notes-2026-11-15.md in that repo.

Store inputs are unchanged: support small 200 conv / 1 seat, medium 1,000 / 2, large 4,000 / 5, AI rate 0.5. Search sizes as in data/search_apps.json.

## Price changes

### Richpanel
URL: https://www.richpanel.com/pricing
Date: 15 Nov 2026

Quote, monthly billing (Pay Annually off): "All subscriptions are on yearly contracts. PRO $89 per agent/month. PRO MAX $119 per agent/month. ENTERPRISE Custom per agent/month. For teams with more than 50 agents."
Quote, annual billing (Pay Annually on): "PRO $69 per agent/month $1,068 $828/yr. PRO MAX $99 per agent/month $1,428 $1,188/yr."
Quote, add-on card: "ADD-ON Customer Service AI $0.20 per AI-handled conversation. AI agents resolve your repetitive tickets end to end, in your brand voice. You pay only for the conversations they handle."
The official page's calculator script still has FLOOR=200, ANNUAL_PER_CONV=0.20, MONTHLY_MULT=1.2. The $200/mo minimum is not stated on the add-on card itself.

We now estimate on Pro, the cheapest published helpdesk seat, at $89/mo, with $0.20 per conversation and a $200 AI minimum. We previously listed a single seat at $119 monthly / $99 annual (now Pro Max) and $0.60 per credit. The old $0.60 token meter, and a public Returns & Exchanges price of $99/mo, were not on the page we read.

New estimates vs old: small $289 (was $319), medium $378 (was $478), large $1,245 (was $1,555). Logged on /price-moves.

Do not rewrite verdicts automatically. Pages and drafts that still describe the old Richpanel figures or ranking:
- Live /gorgias-alternatives short answer ("Re:amaze, HubSpot and Intercom Fin land between $420 and $573… below Gorgias at $1,015") omits cheaper Richpanel at $378.
- Unpublished 19 Nov Black Friday essay at /workspace/stillprice-essays/2026-11-19-black-friday-bill/draft-final.md (Richpanel $478/$718, 2 x $119 seats, 2,000 x $0.24).
- The under-$50 correction draft in this folder's sibling, under-50-correction/, uses the new figures.

A one-off glitch while toggling every checkbox once showed AI as "$99 per conversation". A clean recapture of only the Pay Annually switch still showed $0.20. We use $0.20, not $99.

### HubSpot Service Hub
URL: https://www.hubspot.com/pricing/?term=monthly (the old /pricing/service URL now redirects to the unified HubSpot pricing page)
Also: https://www.hubspot.com/products/artificial-intelligence/ai-customer-service-agent
Also: https://blog.hubspot.com/service/hubspot-service-hub-pricing
Date: 15 Nov 2026

Quote, monthly pricing page: "Starter For growing teams $10/mo/seat. Professional For mature teams $100/mo/seat. Enterprise For sophisticated teams $175/mo/seat."
Quote, Customer Agent page: "Messaging $0.50 per resolution. Professional and Enterprise editions of HubSpot are required to access customer agent."
The Service Hub pricing guide still describes Professional at $100/mo/seat, 3,000 HubSpot Credits, and a $1,500 Professional onboarding fee, and still lists Enterprise as starting at $150 per seat/month.

We updated Starter monthly from $15 to $10. Professional $100 and Customer Agent $0.50 are confirmed, so sample-store estimates are unchanged. We have not changed the Enterprise list price, because the unified page ($175) and the Service Hub guide ($150) disagree. Flagged in the changelog and in the deploy report. Logged the Starter change on /price-moves.

## Unchanged support apps (checked 15 Nov 2026)

Each matched the prices already on the ledger. Checked date updated to 15 Nov 2026.

- Aide, https://www.aide.com/pricing (and the Shopify listing): Free 150 resolutions; Starter $39 / 1,000 / $0.15 up to $110; Pro $149 / 4,000 / $0.10 up to $350; Scale $499 / 15,000 / $0.07 up to $1,000.
- Gorgias, https://www.gorgias.com/pricing: Starter $40, Basic $90, Pro $550, Advanced $1,430 monthly with AI Agent; $1.50 overage past the included allowance; included block $1.00 monthly / $0.90 annual, as already corrected on 9 Nov.
- Tidio, tidio.com/pricing (annual default) and https://apps.shopify.com/tidio (monthly): Customer Service $29 / Growth $59, Lyro $39, Plus $300 on the Shopify listing. Official site still leads with annual $24.17 / $49.17 / $32.50.
- Zipchat, official pricing: $80 / $300 / $600, Scale Plus $960 annual, Unlimited from $2,100.
- Helpcenter, https://apps.shopify.com/helpcenter: $40 / $70 / $120, $0.15 / $0.12 overage. The $5.99 Basic plan is still gone (that move was logged 26 Oct).
- Chatty: $19.99 / $68.99 / $199.
- Shopify Inbox: still free.
- Re:amaze, https://www.reamaze.com/pricing: $59 Starter, $29/seat, $0.85 per resolution.
- Freshdesk: $19 monthly / $15 annual, $49 per 100 sessions.
- Siena: $750 + $0.90.
- Intercom: $39 monthly seat, $0.99 Fin (annual $29 / $85 / $132 also on the official page).
- Zendesk: Suite Team $69, $1.50 committed / $2.00 PAYG. The Shopify listing still shows Suite Growth $89, which we already note.

## Unchanged search apps (checked 15 Nov 2026)

- Searchanise: $19 / $39 / $89 / $139 / $209 / $349.
- Boost: Launch $29, Convert $239 on the pricing page vs $299 on the help centre (medium/large still not public for the exact sub-tier), Accelerate $399 vs $699 on the help centre.
- Fast Simon: Shopify listing https://apps.shopify.com/instant-search $39.99 / $114.99 / $299.99. Official fastsimon.com/pricing was a thin JavaScript shell with no prices in static HTML.
- Doofinder: Shopify listing $61 / $186 / $436; the general site still shows $49 / $149 / $349.
- Algolia: page JS still has RATE grow 0.50, growPlus 1.75, records 0.40, with 10K searches / 100K records included.
- Wiser: $9 / $19 / $49 / $99 / $199 by orders. Large is still above the published 2,000-order cap.
- LimeSpot, https://limespot.com/shopify: slider values still match the stored Turbo and Max tables (small Turbo $19.99 at 250 orders; medium Turbo $149.99 at 1,000; large Max $525 at up to $400k revenue; Turbo would be $649.99 at 4,000 orders). "50% off for life" is still advertised; we use list prices.
- Rebuy Search & Collections, https://www.rebuyengine.com/pricing: $35 / $69 / $264 at 500 / 1,000 / 4,000 orders, $136 at 2,000. Pre-existing flag, not rewritten: the Rebuy vs LimeSpot verdict still says Rebuy order tiers are not public, which has been stale since 8 Nov.
- Klevu / Athos and Nosto: still quote only.
- Shopify Search & Discovery: still free.
