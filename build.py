import json, html, pathlib
from calc import MODELS, m
R = pathlib.Path(__file__).parent
D = json.load(open(R / "data/apps.json")); S = D["site"]; A = D["apps"]; e = html.escape
SIZES = S["sizes"]; RATE = S["ai_rate"]; BY = {a["slug"]: a for a in A}
for a in A:
    a["est"] = [MODELS[a["model"]](a["params"], s["conv"], s["seats"], int(s["conv"] * RATE)) for s in SIZES]
def money(o): return "Not public" if o["total"] is None else m(o["total"])
def link(a): return a.get("affiliate_url") or a["pricing_url"]

CSS = """*{box-sizing:border-box}body{margin:0;font:16px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#17202a;background:#f7f8fa}
a{color:#0b5fd1}header,main,footer{max-width:1120px;margin:0 auto;padding:14px 16px}header{display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center;justify-content:space-between}
.logo{font-weight:800;font-size:21px;text-decoration:none;color:#17202a;letter-spacing:-.01em}.logo span{color:#5b3fd6}nav{display:flex;flex-wrap:wrap;gap:4px 16px}nav a{text-decoration:none;font-size:15px}
h1{font-size:clamp(27px,4.6vw,42px);line-height:1.15;margin:.35em 0 .25em;letter-spacing:-.02em}h2{margin-top:1.6em;line-height:1.25}.lead{font-size:18px;color:#3d4a57;margin:0 0 16px;max-width:780px}
.tw{overflow-x:auto;background:#fff;border-radius:12px;box-shadow:0 1px 3px #0002;margin:12px 0 24px}table{border-collapse:collapse;width:100%;font-size:14.5px}
th,td{padding:10px 12px;text-align:left;border-bottom:1px solid #e7eaee;vertical-align:top}thead th{background:#1d1640;color:#fff;font-weight:600;white-space:nowrap}tbody th{background:#f1eefc;width:190px}
td.n .muted{white-space:normal;display:block;font-size:12.5px;min-width:110px}.cmp td:first-child{min-width:190px}.cmp td:last-child{white-space:nowrap}.plans td:last-child{min-width:230px}.cmp td:nth-child(2){min-width:210px}td.n{white-space:nowrap;font-variant-numeric:tabular-nums;font-weight:600}.box{background:#fff;border-radius:12px;padding:18px 20px;box-shadow:0 1px 3px #0002;margin:20px 0}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}.card{background:#fff;border-radius:12px;padding:14px 16px;box-shadow:0 1px 3px #0002}
.tag{display:inline-block;font-size:12px;font-weight:700;padding:2px 8px;border-radius:99px;background:#e6f6ee;color:#0a7a4c;margin:2px 4px 2px 0}.tag.warn{background:#fff3dc;color:#8a5a00}.tag.free{background:#e8f0ff;color:#1f4fbf}
.math{font-size:14px;color:#33404d;margin:6px 0 0;padding-left:18px}.muted{color:#5d6b78;font-size:14px}.btn{display:inline-block;background:#5b3fd6;color:#fff;font-weight:700;text-decoration:none;padding:11px 18px;border-radius:8px;margin:6px 6px 6px 0}
.btn.alt{background:#fff;color:#5b3fd6;border:2px solid #5b3fd6}.callout{background:#fff8e8;border:1px solid #e6b54a;border-radius:12px;padding:12px 16px;margin:16px 0;font-size:15px}
.news{background:linear-gradient(135deg,#1d1640,#3a2a8f);color:#fff;border-radius:14px;padding:20px 22px;margin:28px 0}.news h2{margin:0 0 6px}.news p{margin:4px 0;color:#ddd8ff}
.sizes{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 4px}.sizes span{background:#fff;border:1px solid #dcd6f7;border-radius:8px;padding:6px 10px;font-size:14px}
footer{color:#5d6b78;font-size:14px;border-top:1px solid #dde2e8;margin-top:36px}footer a{margin-right:12px}
@media(max-width:640px){th,td{padding:8px}tbody th{width:auto}.lead{font-size:16.5px}}"""

NAV = [("index.html", "Compare"), ("gorgias-alternatives.html", "Gorgias alternatives"), ("changelog.html", "Change log"), ("methodology.html", "How we calculate"), ("advertise.html", "Advertise")]
def ld(o): return '<script type="application/ld+json">' + json.dumps(o) + "</script>"
PAGES = []
def page(fn, title, desc, body, head=""):
    PAGES.append(fn)
    url = S["base_url"] + "/" + ("" if fn == "index.html" else fn)
    nav = "".join(f'<a href="{h}">{t}</a>' for h, t in NAV)
    (R / fn).write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="ShopAI Ledger"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta name="twitter:card" content="summary">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%235b3fd6'/%3E%3Ctext x='16' y='22' font-size='17' text-anchor='middle' fill='white' font-family='Arial' font-weight='bold'%3E$%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="style.css">{head}</head><body>
<header><a class="logo" href="index.html">ShopAI <span>Ledger</span></a><nav>{nav}</nav></header>
<main>{body}</main>
<footer><p>ShopAI Ledger is independent and not affiliated with Shopify or any app listed. Prices are in USD, checked by hand on the date shown, and can change at any time. Always confirm on the vendor's site.</p>
<p><a href="methodology.html">How we calculate</a><a href="disclosure.html">Affiliate disclosure</a><a href="changelog.html">Change log</a><a href="advertise.html">Advertise / get listed</a><a href="mailto:{S['contact']}?subject=ShopAI%20Ledger%20correction">Report a wrong price</a></p></footer></body></html>""")

# Newsletter placeholder: swap the inner #newsletter-embed contents for the Beehiiv embed when ready.
NEWS = """<section class="news" id="newsletter"><h2>Weekly price-change email (coming soon)</h2>
<p>One short email a week: which Shopify AI apps changed their prices or plans, and what that means for your bill.</p>
<div id="newsletter-embed"><!-- NEWSLETTER_EMBED: replace this comment and the paragraph below with the Beehiiv form embed --><p><b>Launching soon.</b> Check the <a href="changelog.html" style="color:#fff">change log</a> in the meantime.</p></div></section>"""

sizes_html = '<div class="sizes">' + "".join(f"<span><b>{s['label']}</b>: {s['conv']:,} support conversations/mo, {s['seats']} agent seat{'s' if s['seats']>1 else ''}</span>" for s in SIZES) + f"<span>AI resolves {int(RATE*100)}% of conversations</span></div>"
def flag(a): return f'<span class="tag free">Free option overlaps</span>' if a.get("free_alt") and a["model"] != "free" else ('<span class="tag free">Free</span>' if a["model"] == "free" else "")
def conf(a): return '<span class="tag">Prices confirmed</span>' if not a["unconfirmed"] else '<span class="tag warn">Partly confirmed</span>'

def table(apps):
    rows = "".join(f"<tr><td><a href='{x['slug']}-pricing.html'><b>{e(x['name'])}</b></a><br><span class=muted>{e(x['type'])}</span><br>{flag(x)}</td><td>{e(x['ai_short'])}</td>"
                   + "".join(f"<td class=n>{money(o)}<br><span class=muted style='font-weight:400'>{e(o['plan'])}</span></td>" for o in x["est"]) + f"<td class=muted>{x['checked']}</td></tr>" for x in apps)
    return ("<div class=tw><table class=cmp><thead><tr><th>App</th><th>How AI is billed</th>" + "".join(f"<th>{s['label']}<br><span style='font-weight:400'>{s['conv']:,} conv/mo</span></th>" for s in SIZES)
            + f"<th>Checked</th></tr></thead><tbody>{rows}</tbody></table></div>")

def sortkey(a):
    t = a["est"][1]["total"]; return (t is None, t if t is not None else 0)
ordered = sorted(A, key=sortkey)

COMPS = [("gorgias", "tidio"), ("gorgias", "intercom-fin"), ("zendesk", "gorgias"), ("intercom-fin", "zendesk"), ("tidio", "shopify-inbox"), ("gorgias", "richpanel")]
def cslug(x, y): return f"{x}-vs-{y}-pricing.html"
def short(a): return a["name"].split(" (")[0]

# ---- home
comp_links = "".join(f"<li><a href='{cslug(x,y)}'>{e(short(BY[x]))} vs {e(short(BY[y]))} pricing</a></li>" for x, y in COMPS)
page("index.html", "ShopAI Ledger: What AI Customer Support Apps Really Cost Shopify Stores (2026)",
 f"Real monthly cost of {len(A)} AI support apps for Shopify (Gorgias, Tidio Lyro, Intercom Fin, Zendesk, HubSpot and more) at three store sizes, with the math shown and dated sources.",
 f"<h1>What Shopify AI support apps really cost</h1><p class=lead>Most AI helpdesks now bill per resolution, per conversation or per reply, so the sticker price rarely matches the invoice. We read every official pricing page by hand and show the estimated monthly bill at three store sizes, with the math.</p>"
 f"{sizes_html}<p class=muted>Prices checked {S['updated']}. Monthly-billing prices unless noted. Sorted by medium-store cost. Click an app to see the full plan list and math.</p>{table(ordered)}"
 f"<div class=callout><b>The free option first.</b> <a href='shopify-inbox-pricing.html'>Shopify Inbox</a> is free and now includes an AI agent trained on your catalog and policies. If you only need storefront chat, start there. Paid apps make sense when you need email/social ticketing, order actions, or higher automation.</div>"
 f"<h2>Pricing comparisons</h2><ul>{comp_links}<li><a href='gorgias-alternatives.html'>Gorgias alternatives by real cost</a></li></ul>"
 f"<h2>Why the bill surprises people</h2><div class=grid><div class=card><b>Per-resolution billing</b><p class=muted>Gorgias, Zendesk, Intercom Fin, HubSpot, Re:amaze and Siena charge for each conversation the AI closes. Better automation means a bigger AI line on the bill.</p></div><div class=card><b>Per-conversation or per-reply billing</b><p class=muted>Tidio Lyro, Chatty, Richpanel, Freshdesk and Zipchat count conversations (or messages) the AI touches, resolved or not.</p></div><div class=card><b>Seats still matter</b><p class=muted>Intercom, Zendesk, HubSpot, Re:amaze, Freshdesk and Richpanel also charge per human agent seat, and HubSpot Professional adds a one-time onboarding fee.</p></div></div>{NEWS}",
 head=ld({"@context": "https://schema.org", "@type": "WebSite", "name": "ShopAI Ledger", "url": S["base_url"] + "/"}))

# ---- app pages
def plans_table(a):
    rows = "".join(f"<tr><td><b>{e(p['name'])}</b></td><td class=n>{m(p['monthly']) if p['monthly'] is not None else '—'}</td><td class=n>{m(p['annual']) if p['annual'] is not None else '—'}</td><td>{e(p['includes'])}</td></tr>" for p in a["plans"])
    return f"<div class=tw><table class=plans><thead><tr><th>Plan</th><th>Monthly billing</th><th>Annual (per mo)</th><th>What's included</th></tr></thead><tbody>{rows}</tbody></table></div>"
def est_block(a):
    out = ""
    for s, o in zip(SIZES, a["est"]):
        out += f"<div class=card><b>{s['label']}</b> <span class=muted>({s['conv']:,} conversations, {s['seats']} seat{'s' if s['seats']>1 else ''}, {int(s['conv']*RATE):,} AI-resolved)</span><div style='font-size:24px;font-weight:800;margin:4px 0'>{money(o)}<span class=muted style='font-size:14px;font-weight:400'>{'/mo' if o['total'] is not None else ''}</span></div><span class=muted>{e(o['plan'])}</span><ul class=math>" + "".join(f"<li>{e(l)}</li>" for l in o["math"]) + "</ul></div>"
    return f"<div class=grid>{out}</div>"
for a in A:
    nm = short(a); rel = [c for c in COMPS if a["slug"] in c]
    rel_html = " · ".join(f"<a href='{cslug(x,y)}'>{e(short(BY[x]))} vs {e(short(BY[y]))}</a>" for x, y in rel)
    others = " · ".join(f"<a href='{o['slug']}-pricing.html'>{e(short(o))}</a>" for o in A if o is not a)
    unc = ("<div class=callout><b>Not confirmed / not public:</b><ul>" + "".join(f"<li>{e(u)}</li>" for u in a["unconfirmed"]) + "</ul>Check the vendor's site for these.</div>") if a["unconfirmed"] else ""
    srcs = "".join(f"<li><a href='{e(u)}' rel='nofollow noopener' target='_blank'>{e(l)}</a> (checked {a['checked']})</li>" for l, u in a["sources"])
    fa = f"<div class=box><b>Free Shopify alternative:</b> {e(a['free_alt'])} {'<a href=\"shopify-inbox-pricing.html\">See Shopify Inbox</a>.' if a['model']!='free' else ''}</div>" if a.get("free_alt") else ""
    faq = [(f"How much does {nm} cost per month?", f"On our assumptions, about {money(a['est'][0])} for a small store ({SIZES[0]['conv']} conversations), {money(a['est'][1])} for a medium store and {money(a['est'][2])} for a large store. Prices checked {a['checked']}."),
           (f"How does {nm} charge for AI?", a["ai_billing"])]
    page(f"{a['slug']}-pricing.html", f"{nm} Pricing 2026: Plans & Real Monthly Cost for Shopify Stores | ShopAI Ledger",
     f"{nm} pricing explained: plans, how AI usage is billed, and the estimated monthly cost for small, medium and large Shopify stores, with the math. Checked {a['checked']}.",
     f"<h1>{e(nm)} pricing: what it really costs a Shopify store</h1><p class=lead>{e(a['summary'])}</p><p>{conf(a)}{flag(a)}<span class=muted>Price checked on {a['checked']} from the official source.</span></p>"
     f"<h2>Plans</h2>{plans_table(a)}<h2>How AI usage is billed</h2><p>{e(a['ai_billing'])}</p>"
     f"<h2>Estimated monthly cost by store size</h2>{est_block(a)}<p class=muted>Assumptions: AI resolves {int(RATE*100)}% of conversations; monthly billing unless noted; taxes, add-ons, SMS/voice and phone fees excluded. <a href='methodology.html'>How we calculate</a>.</p>"
     f"{unc}{fa}" + (f"<p class=muted>Note: {e(a['notes'])}</p>" if a["notes"] else "")
     + f"<p><a class=btn href='{e(link(a))}' rel='nofollow noopener' target='_blank'>See {e(nm)}'s official pricing</a>" + (f"<a class='btn alt' href='{e(a['shopify_url'])}' rel='nofollow noopener' target='_blank'>Shopify App Store listing</a>" if a.get("shopify_url") and a["shopify_url"] != link(a) else "") + "</p>"
     f"<h2>Sources</h2><ul class=muted>{srcs}</ul>" + (f"<p>Compare: {rel_html}</p>" if rel else "") + f"<p class=muted>Other apps: {others}</p>{NEWS}",
     head=ld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": t}} for q, t in faq]}))

# ---- comparison pages
for x, y in COMPS:
    a, b = BY[x], BY[y]; na, nb = short(a), short(b)
    lines = []
    for s, oa, ob in zip(SIZES, a["est"], b["est"]):
        if oa["total"] is None or ob["total"] is None: lines.append(f"<li><b>{s['label']}:</b> can't compare, because one price isn't public at this volume.</li>")
        elif oa["total"] == ob["total"]: lines.append(f"<li><b>{s['label']}:</b> same estimated cost ({money(oa)}).</li>")
        else:
            lo, hi, ol, oh = (na, nb, oa, ob) if oa["total"] < ob["total"] else (nb, na, ob, oa)
            lines.append(f"<li><b>{s['label']}:</b> {e(lo)} is lower on our assumptions ({money(ol)} vs {money(oh)}, a {m(oh['total']-ol['total'])}/mo difference).</li>")
    rows = "".join(f"<tr><th>{lab}</th><td>{fa_}</td><td>{fb}</td></tr>" for lab, fa_, fb in [
        ("Type", e(a["type"]), e(b["type"])), ("How AI is billed", e(a["ai_billing"]), e(b["ai_billing"])),
        *[(f"{s['label']} ({s['conv']:,} conv)", f"<b>{money(oa)}</b><br><span class=muted>{e(oa['plan'])}</span>", f"<b>{money(ob)}</b><br><span class=muted>{e(ob['plan'])}</span>") for s, oa, ob in zip(SIZES, a["est"], b["est"])],
        ("Free Shopify alternative", e(a.get("free_alt") or "—"), e(b.get("free_alt") or "—")), ("Checked", a["checked"], b["checked"]),
        ("Details", f"<a href='{x}-pricing.html'>{e(na)} pricing & math</a>", f"<a href='{y}-pricing.html'>{e(nb)} pricing & math</a>")])
    page(cslug(x, y), f"{na} vs {nb} Pricing (2026): Real Monthly Cost Compared | ShopAI Ledger",
     f"{na} vs {nb}: how each bills for AI, and the estimated monthly cost for small, medium and large Shopify stores side by side. Prices checked {S['updated']}.",
     f"<h1>{e(na)} vs {e(nb)} pricing</h1><p class=lead>Two different ways of billing AI support. Here's what each would cost the same Shopify store, using official prices checked {S['updated']}.</p>{sizes_html}"
     f"<div class=tw><table><thead><tr><th></th><th>{e(na)}</th><th>{e(nb)}</th></tr></thead><tbody>{rows}</tbody></table></div><h2>Bottom line on cost</h2><ul>{''.join(lines)}</ul>"
     "<p class=muted>Cost is only one factor. Features, channels, integrations and AI quality differ, and your real volume and resolution rate will move these numbers. See the full math on each app's page.</p>" + NEWS)

# ---- Gorgias alternatives
alts = [o for o in ordered if o["slug"] != "gorgias"]
page("gorgias-alternatives.html", "Gorgias Alternatives 2026: Real Monthly Cost of 12 AI Support Apps for Shopify | ShopAI Ledger",
 "Gorgias alternatives for Shopify compared on real monthly cost at three store sizes: Tidio, Intercom Fin, Zendesk, HubSpot, Richpanel, Re:amaze, Freshdesk, Zipchat, Chatty and Shopify Inbox.",
 f"<h1>Gorgias alternatives, compared on real cost</h1><p class=lead>For reference, Gorgias comes out at about <b>{money(BY['gorgias']['est'][0])}</b> (small), <b>{money(BY['gorgias']['est'][1])}</b> (medium) and <b>{money(BY['gorgias']['est'][2])}</b> (large) a month on our assumptions (<a href='gorgias-pricing.html'>see the math</a>). Here's how the alternatives price out for the same store.</p>"
 f"{sizes_html}{table(alts)}<p class=muted>Some of these are full helpdesks, and others (Zipchat, Chatty, Shopify Inbox) are chat/AI layers only. Compare like with like. <a href='methodology.html'>How we calculate</a>.</p>{NEWS}")

# ---- change log
CL = D.get("changelog") or []
page("changelog.html", "Shopify AI App Price Change Log | ShopAI Ledger", "A dated log of pricing and plan changes for AI customer-support apps on Shopify, updated weekly.",
 "<h1>Price change log</h1><p class=lead>Every pricing or plan change we spot, dated. We re-check every app's official pricing page weekly.</p>"
 + "".join(f"<div class=box><b>{e(c['date'])}</b>: {e(c['title'])}<ul>" + "".join(f"<li>{e(i)}</li>" for i in c["items"]) + "</ul></div>" for c in CL) + NEWS)

# ---- methodology
page("methodology.html", "How We Calculate Shopify AI App Costs | ShopAI Ledger", "The store sizes, assumptions and formulas ShopAI Ledger uses to estimate the real monthly cost of AI support apps.",
 f"""<h1>How we calculate</h1><div class=box><h2 style="margin-top:0">Sources</h2><ul><li>Every price comes from the vendor's official pricing page or its official Shopify App Store listing, read by hand. No scraping, no third-party price lists.</li>
<li>Each app shows the date we checked it and links the source. If a number isn't published, we say <b>"Not public / check site"</b> instead of guessing.</li><li>We re-check weekly and log changes on the <a href="changelog.html">change log</a>.</li></ul></div>
<div class=box><h2 style="margin-top:0">Store sizes</h2>{sizes_html}<p>We size stores by <b>support conversations per month</b>, not orders, because conversations are what these apps bill. Seats are the number of human agents paying for a seat.</p></div>
<div class=box><h2 style="margin-top:0">Assumptions</h2><ul><li><b>AI resolves {int(RATE*100)}% of conversations.</b> Vendors advertise 50–75%+; your rate may be higher or lower, and the cost scales with it.</li>
<li><b>Per-resolution apps</b> (Gorgias, Zendesk, Intercom Fin, HubSpot, Re:amaze, Siena) are charged for the resolved {int(RATE*100)}%.</li><li><b>Per-conversation, per-session or per-reply apps</b> (Tidio Lyro, Chatty, Richpanel, Freshdesk, Zipchat) are charged for every conversation the AI touches, which we assume is all of them.</li>
<li>Included allowances (e.g. 5 resolutions per agent, 3,000 HubSpot credits) are subtracted first.</li><li>We use <b>monthly-billing</b> prices where published; where only annual prices are public we say so. We pick the cheapest published plan that fits the size.</li>
<li>Excluded: taxes, SMS/voice/WhatsApp fees, optional add-ons (Copilot etc.), one-time fees (shown separately) and negotiated discounts.</li></ul></div>
<p>Spotted an error? <a href="mailto:{S['contact']}?subject=ShopAI%20Ledger%20correction">Email a correction</a>. App makers are welcome to send corrections too, and we'll verify them against your public pricing page.</p>""")

# ---- disclosure
page("disclosure.html", "Affiliate Disclosure | ShopAI Ledger", "How ShopAI Ledger makes money and how that is kept separate from prices and rankings.",
 """<h1>Affiliate disclosure</h1><div class=box><p><b>Right now, ShopAI Ledger has no affiliate links.</b> Every "official pricing" link goes straight to the vendor.</p>
<p>In future we may join affiliate programs run by some app makers. If we do, those links will be labelled, and this page will list which apps pay us. Affiliate status never changes the prices we show, the math, or the sort order (always by estimated cost).</p>
<p>We may also offer clearly-labelled sponsored placements. Sponsored content is always marked "Sponsored" and never changes an app's price data. See <a href="advertise.html">Advertise</a>.</p></div>""")

# ---- advertise
page("advertise.html", "Advertise or Get Your App Listed | ShopAI Ledger", "App makers: get your Shopify AI app listed, correct your pricing, or sponsor the weekly price-change email.",
 f"""<h1>Advertise / get your app listed</h1><p class=lead>ShopAI Ledger is read by Shopify merchants comparing what AI apps really cost.</p>
<div class=grid><div class=card><b>Free listing</b><p class=muted>Have a Shopify AI support app with public pricing? Send us the link, and we list apps for free if the pricing is public.</p></div>
<div class=card><b>Pricing corrections</b><p class=muted>Changed your plans? Tell us and we'll re-check against your public pricing page within a week.</p></div>
<div class=card><b>Sponsorship</b><p class=muted>Featured placements and sponsor slots in the weekly price-change email (launching soon). Always labelled as sponsored. Placements never change price data.</p></div></div>
<p><a class=btn href="mailto:{S['contact']}?subject=ShopAI%20Ledger%20listing%20%2F%20sponsorship">Contact us</a></p>""")

(R / "style.css").write_text(CSS)
(R / "404.html").write_text('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Not found | ShopAI Ledger</title><link rel="stylesheet" href="/shopai-ledger/style.css"><main><h1>Page not found</h1><p><a href="/shopai-ledger/">Go to the ShopAI Ledger comparison</a></p></main>')
(R / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{S['base_url']}/{'' if p=='index.html' else p}</loc><lastmod>{S['updated']}</lastmod></url>\n" for p in PAGES) + "</urlset>\n")
(R / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {S['base_url']}/sitemap.xml\n")
(R / ".nojekyll").write_text("")
print("built", len(PAGES), "pages")
