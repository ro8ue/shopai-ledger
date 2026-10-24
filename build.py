import json, html, pathlib
from calc import MODELS, m
R = pathlib.Path(__file__).parent
D = json.load(open(R / "data/apps.json")); S = D["site"]; A = D["apps"]; e = html.escape
SIZES = S["sizes"]; RATE = S["ai_rate"]; BY = {a["slug"]: a for a in A}
for a in A:
    a["est"] = [MODELS[a["model"]](a["params"], s["conv"], s["seats"], int(s["conv"] * RATE)) for s in SIZES]
# Search & recommendations category (data/search_apps.json, calc_search.py)
from calc_search import MODELS as SMODELS
SD = json.load(open(R / "data/search_apps.json")); SC = SD["category"]; SA = SD["apps"]; SSIZES = SC["sizes"]; SBY = {a["slug"]: a for a in SA}
for a in SA:
    a["est"] = [SMODELS[a["model"]](a["params"], s, i) for i, s in enumerate(SSIZES)]
SLAND = SC["slug"] + ".html"
def money(o): return "Not public" if o["total"] is None else m(o["total"])
def link(a): return a["pricing_url"]
def colmax(apps, k): return max([x["est"][k]["total"] for x in apps if x["est"][k]["total"]] or [1])
def cell(o, mx, txt):
    if o["total"] is None: return f"<span class='tag np'>{txt}</span>"
    return f"{txt}<span class=bar style='--w:{max(0, min(100, round(o['total'] / mx * 100)))}%'></span>"

CSS = (R / "design.css").read_text()  # edit design.css, not style.css (style.css is generated)
import re
HERO_END = "<!--/hero-->"

NAV = [("index.html#support", "Support apps"), (SLAND, "Search & recommendations"), ("gorgias-alternatives.html", "Gorgias alternatives"), ("changelog.html", "Change log"), ("methodology.html", "How we calculate"), ("advertise.html", "Advertise")]
def ld(o): return '<script type="application/ld+json">' + json.dumps(o) + "</script>"
PAGES = []
LOGO = """<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="0.5" y="0.5" width="23" height="23" rx="4" fill="none" stroke="currentColor" stroke-opacity=".35"/><rect x="5" y="6" width="14" height="2" rx="1" fill="currentColor"/><rect x="5" y="11" width="9" height="2" rx="1" fill="currentColor"/><rect x="5" y="16" width="11.5" height="2" rx="1" fill="currentColor" fill-opacity=".55"/></svg>"""
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600&family=Instrument+Serif:ital@0;1&display=swap">'
def page(fn, title, desc, body, head=""):
    PAGES.append(fn)
    url = S["base_url"] + "/" + ("" if fn == "index.html" else fn)
    nav = "".join(f'<a href="{h}"' + (' aria-current="page"' if h == fn else "") + f'>{t}</a>' for h, t in NAV)
    news = NEWS in body; body = body.replace(NEWS, "")
    hero, sep, rest = body.partition(HERO_END)
    if not sep: hero, rest = "", body
    if fn != "index.html":
        hero = re.sub(r"<h1>(.*?): (.*?)</h1>", r"<h1>\1: <em>\2</em></h1>", hero, count=1)
        hero = f'<section class="hero"><div class="wrap">{hero}</div></section>' if hero else ""
    (R / fn).write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="google-site-verification" content="JHZv0niTmEJr6Eywzr3X6kB2OFSl9WHrn6igGEJn2Qw" />
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="ShopAI Ledger"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta name="twitter:card" content="summary">
<meta name="theme-color" content="#0c0c0c"><link rel="icon" href="favicon.svg" type="image/svg+xml">
{FONTS}<link rel="stylesheet" href="style.css">{head}</head><body>
<header class="top"><div class="wrap"><a class="logo" href="index.html" aria-label="ShopAI Ledger home">{LOGO}<span>ShopAI <em>Ledger</em></span></a><nav class="main" aria-label="Main">{nav}</nav><a class="btn light sm" href="{'#newsletter' if news else 'index.html#newsletter'}">Weekly email</a></div></header>
{hero}<main class="wrap">{rest}</main>{NEWS if news else ""}
<footer class="site"><div class="wrap"><div><a class="logo" href="index.html">{LOGO}<span>ShopAI <em>Ledger</em></span></a><p>ShopAI Ledger is independent and not affiliated with Shopify or any app listed. Prices are in USD, checked by hand on the date shown, and can change at any time. Always confirm on the vendor's site.</p></div>
<div class="links"><a href="methodology.html">How we calculate</a><a href="disclosure.html">Affiliate disclosure</a><a href="changelog.html">Change log</a><a href="advertise.html">Advertise / get listed</a><a href="mailto:{S['contact']}?subject=ShopAI%20Ledger%20correction">Report a wrong price</a></div>
<div class="base"><span>Prices checked {S['updated']}</span><a href="#">Back to top ↑</a></div></div></footer></body></html>""")

# Newsletter: Substack signup (shopailedger.substack.com) inside the cream .news .embed card.
NEWS = """<section class="news" id="newsletter"><div class="wrap"><div><p class="eyebrow">( The Ledger )</p><h2>The Ledger, every Monday</h2>
<p>The Ledger, every Monday: what AI apps really cost Shopify stores, plus a Thursday deep-dive.</p><div class="perks"><span>Free</span><span>Mondays + Thursdays</span><span>Unsubscribe anytime</span></div></div>
<div class="embed" id="newsletter-embed"><iframe src="https://shopailedger.substack.com/embed" width="480" height="320" title="Subscribe to The Ledger on Substack" loading="lazy" style="border:1px solid #EEE;background:white" frameborder="0" scrolling="no"></iframe><p style="font-size:.85em;margin:14px 0 0">Free. Or read past issues at <a href="https://shopailedger.substack.com">shopailedger.substack.com</a>.</p></div></div></section>"""

sizes_html = '<div class="sizes">' + "".join(f"<span><b>{s['label']}</b>: {s['conv']:,} support conversations/mo, {s['seats']} agent seat{'s' if s['seats']>1 else ''}</span>" for s in SIZES) + f"<span>AI resolves {int(RATE*100)}% of conversations</span></div>"
def flag(a): return f'<span class="tag free">Free option overlaps</span>' if a.get("free_alt") and a["model"] != "free" else ('<span class="tag free">Free</span>' if a["model"] == "free" else "")
def conf(a): return '<span class="tag">Prices confirmed</span>' if not a["unconfirmed"] else '<span class="tag warn">Partly confirmed</span>'

def table(apps):
    rows = "".join(f"<tr><td><a href='{x['slug']}-pricing.html'><b>{e(x['name'])}</b></a><br><span class=muted>{e(x['type'])}</span><br>{flag(x)}</td><td>{e(x['ai_short'])}</td>"
                   + "".join(f"<td class=n data-l='{SIZES[k]['label'].split()[0]}'>{cell(o, colmax(apps, k), money(o))}<span class=muted style='font-weight:400'>{e(o['plan'])}</span></td>" for k, o in enumerate(x["est"])) + f"<td class='muted ck'>{x['checked']}</td></tr>" for x in apps)
    return ("<p class=scroll-hint>Swipe sideways to see every store size →</p><div class=tw><table class=cmp><thead><tr><th>App</th><th>How AI is billed</th>" + "".join(f"<th>{s['label']}<br><span style='font-weight:400'>{s['conv']:,} conv/mo</span></th>" for s in SIZES)
            + f"<th>Checked</th></tr></thead><tbody>{rows}</tbody></table></div>")

def sortkey(a):
    t = a["est"][1]["total"]; return (t is None, t if t is not None else 0)
ordered = sorted(A, key=sortkey)

COMPS = [("gorgias", "tidio"), ("gorgias", "intercom-fin"), ("zendesk", "gorgias"), ("intercom-fin", "zendesk"), ("tidio", "shopify-inbox"), ("gorgias", "richpanel"), ("gorgias", "reamaze"), ("gorgias", "freshdesk"), ("richpanel", "reamaze")]
def vs_btns(*apps):  # official pricing links stay clean; affiliate is a separate labelled rel=sponsored button
    return "<p>" + "".join(f"<a class=btn href='{e(a['pricing_url'])}' rel='nofollow noopener' target='_blank'>{e(a['_n'])} official pricing</a>" + (f"<a class='btn alt' href='{e(a['affiliate_url'])}' rel='sponsored noopener' target='_blank'>Try {e(a['_n'])} (affiliate link)</a>" if a.get("affiliate_url") else "") for a in apps) + "</p>"
def cslug(x, y): return f"{x}-vs-{y}-pricing.html"
def short(a): return a["name"].split(" (")[0]

# ---- search category helpers
def sfmt(k, v): return m(v) if k == "revenue" else f"{v:,}"
ssizes_html = '<div class="sizes">' + "".join(f"<span><b>{s['label']}</b>: {s['products']:,} products, {s['orders']:,} orders/mo, {m(s['revenue'])} revenue/mo, {s['sessions']:,} sessions/mo, {s['requests']:,} search requests/mo</span>" for s in SSIZES) + "</div>"
def sflag(a): return '<span class="tag free">Free</span>' if a["model"] == "free" else '<span class="tag free">Free option overlaps</span>'
def sconf(a): return '<span class="tag">Prices confirmed</span>' if not a["unconfirmed"] else ('<span class="tag warn">Quote only</span>' if all(o["total"] is None for o in a["est"]) else '<span class="tag warn">Partly confirmed</span>')
def smoney(o): return "Not public / check site" if o["total"] is None else m(o["total"])
def ssort(a):
    t = a["est"][1]["total"]; return (t is None, t if t is not None else 0, a["est"][0]["total"] is None)
sordered = sorted(SA, key=ssort)
def stable(apps):
    rows = "".join(f"<tr><td><a href='{x['slug']}-pricing.html'><b>{e(x['name'])}</b></a><br><span class=muted>{e(x['type'])}</span><br>{sflag(x)}</td><td>{e(x['ai_short'])}<br><span class=muted>Billed on: {e(x['unit'])}</span></td>"
                   + "".join(f"<td class=n data-l='{SSIZES[k]['label'].split()[0]}'>{cell(o, colmax(apps, k), smoney(o))}<span class=muted style='font-weight:400'>{e(o['plan'])}</span></td>" for k, o in enumerate(x["est"])) + f"<td class='muted ck'>{x['checked']}</td></tr>" for x in apps)
    return ("<p class=scroll-hint>Swipe sideways to see every store size →</p><div class=tw><table class=cmp><thead><tr><th>App</th><th>How it's billed</th>" + "".join(f"<th>{s['label']}<br><span style='font-weight:400'>{s['products']:,} products · {s['orders']:,} orders</span></th>" for s in SSIZES)
            + f"<th>Checked</th></tr></thead><tbody>{rows}</tbody></table></div>")
SCOMPS = [("searchanise", "boost-ai-search"), ("rebuy", "limespot"), ("doofinder", "algolia"), ("doofinder", "searchanise")]
SALTS = ["klevu", "boost-ai-search"]
def sshort(a): return {"shopify-search-discovery": "Shopify Search & Discovery", "searchanise": "Searchanise", "boost-ai-search": "Boost", "fast-simon": "Fast Simon", "wiser": "Wiser", "limespot": "LimeSpot", "rebuy": "Rebuy", "klevu": "Klevu", "nosto": "Nosto"}.get(a["slug"], a["name"])
scomp_links = "".join(f"<li><a href='{cslug(x,y)}'>{e(sshort(SBY[x]))} vs {e(sshort(SBY[y]))} pricing</a></li>" for x, y in SCOMPS) + "".join(f"<li><a href='{x}-alternatives.html'>{e(sshort(SBY[x]))} alternatives by real cost</a></li>" for x in SALTS)
cats_html = (f"<div class='grid cats'><a class=card href='#support'><span class=idx>01 — Category</span><span class=go>→</span><b>AI customer support apps</b><p class=muted>{len(A)} helpdesks and AI agents (Gorgias, Tidio, Intercom Fin, Zendesk…) priced by conversations and AI resolutions.</p></a>"
             f"<a class=card href='{SLAND}'><span class=idx>02 — Category</span><span class=go>→</span><b>AI search & recommendation apps</b><p class=muted>{len(SA)} search, filter and recommendation apps (Searchanise, Boost, Doofinder, Rebuy, LimeSpot…) priced by products, orders, revenue or searches.</p></a></div>")

# ---- home
HL = [BY[k] for k in ["shopify-inbox", "chatty", "zipchat", "hubspot-service-hub", "intercom-fin", "gorgias", "zendesk"] if k in BY and BY[k]["est"][1]["total"] is not None]
_hmx = max(x["est"][1]["total"] for x in HL) or 1
hero_ledger = (f"<aside class=ledger aria-label='Sample: medium store monthly cost'><header><span>{SIZES[1]['label']} · {SIZES[1]['conv']:,} conversations/mo</span><span>Est. / mo</span></header><ol>"
  + "".join(f"<li><span>{i+1:02d}</span>{e(short(x))}<b>{money(x['est'][1])}</b><i style='--w:{max(2, round(x['est'][1]['total'] / _hmx * 100))}%'></i></li>" for i, x in enumerate(HL))
  + f"</ol><footer>AI resolves {int(RATE*100)}% of conversations. <a href='#support'>See all {len(A)} support apps →</a></footer></aside>")
comp_links = "".join(f"<li><a href='{cslug(x,y)}'>{e(short(BY[x]))} vs {e(short(BY[y]))} pricing</a></li>" for x, y in COMPS)
page("index.html", "ShopAI Ledger: What Shopify AI Apps Really Cost (Support, Search & Recommendations, 2026)",
 f"Real monthly cost of {len(A)} AI support apps (Gorgias, Tidio Lyro, Intercom Fin, Zendesk…) and {len(SA)} AI search & recommendation apps (Searchanise, Boost, Doofinder, Rebuy, LimeSpot…) for Shopify at three store sizes, with the math and dated sources.",
 f"<section class='hero home'><div class=wrap><div><p class=eyebrow>( Shopify AI app pricing · checked {S['updated']} )</p><h1>What Shopify AI apps <em>really cost</em></h1><p class=lead>AI apps bill per resolution, per conversation, per search, per order or by your revenue, so the sticker price rarely matches the invoice. We read every official pricing page by hand and show the estimated monthly bill at three store sizes, with the math.</p>"
 f"<p style='margin:0'><a class='btn light' href='#support'>Compare support apps <span class=arr>→</span></a><a class='btn ghost' href='{SLAND}'>Search & recommendation apps</a></p></div>{hero_ledger}</div>"
 f"<div class=wrap><div class=stats><div><b>{len(A)+len(SA)}</b><span>Apps tracked</span></div><div><b>2</b><span>Categories</span></div><div><b>3</b><span>Store sizes</span></div><div><b>{S['updated']}</b><span>Last checked</span></div></div></div>"
 f"<div class=ticker><div class=wrap><span>Official pricing pages only</span><span>Read by hand</span><span>Every price dated</span><span>Math shown</span><span>Not public = we don't guess</span></div></div></section>{HERO_END}{cats_html}"
 f"<h2 id=support>AI customer support apps</h2>{sizes_html}<p class=muted>Prices checked {S['updated']}. Monthly-billing prices unless noted. Sorted by medium-store cost. Click an app to see the full plan list and math.</p>{table(ordered)}"
 f"<div class=callout><b>The free option first.</b> <a href='shopify-inbox-pricing.html'>Shopify Inbox</a> is free and now includes an AI agent trained on your catalog and policies. If you only need storefront chat, start there. Paid apps make sense when you need email/social ticketing, order actions, or higher automation.</div>"
 f"<h2>Support pricing comparisons</h2><ul>{comp_links}<li><a href='gorgias-alternatives.html'>Gorgias alternatives by real cost</a></li></ul>"
 f"<h2>Why the support bill surprises people</h2><div class=grid><div class=card><b>Per-resolution billing</b><p class=muted>Gorgias, Zendesk, Intercom Fin, HubSpot, Re:amaze and Siena charge for each conversation the AI closes. Better automation means a bigger AI line on the bill.</p></div><div class=card><b>Per-conversation or per-reply billing</b><p class=muted>Tidio Lyro, Chatty, Richpanel, Freshdesk and Zipchat count conversations (or messages) the AI touches, resolved or not.</p></div><div class=card><b>Seats still matter</b><p class=muted>Intercom, Zendesk, HubSpot, Re:amaze, Freshdesk and Richpanel also charge per human agent seat, and HubSpot Professional adds a one-time onboarding fee.</p></div></div>"
 f"<h2 id=search>AI search & recommendation apps</h2>{ssizes_html}<p class=muted>Prices checked {S['updated']}. Sorted by medium-store cost. <a href='{SLAND}'>See the full search & recommendations comparison</a>.</p>{stable(sordered)}"
 f"<h2>Search & recommendation comparisons</h2><ul>{scomp_links}</ul>{NEWS}",
 head=ld({"@context": "https://schema.org", "@type": "WebSite", "name": "ShopAI Ledger", "url": S["base_url"] + "/"}))

# ---- app pages
def plans_table(a):
    rows = "".join(f"<tr><td><b>{e(p['name'])}</b></td><td class=n data-l='Monthly'>{m(p['monthly']) if p['monthly'] is not None else '—'}</td><td class=n data-l='Annual /mo'>{m(p['annual']) if p['annual'] is not None else '—'}</td><td>{e(p['includes'])}</td></tr>" for p in a["plans"])
    return f"<div class=tw><table class=plans><thead><tr><th>Plan</th><th>Monthly billing</th><th>Annual (per mo)</th><th>What's included</th></tr></thead><tbody>{rows}</tbody></table></div>"
def est_block(a):
    out = ""
    for s, o in zip(SIZES, a["est"]):
        out += f"<div class=card><b>{s['label']}</b> <span class=muted>({s['conv']:,} conversations, {s['seats']} seat{'s' if s['seats']>1 else ''}, {int(s['conv']*RATE):,} AI-resolved)</span><div class='num{"" if o["total"] is not None else " np"}'>{money(o)}<span class=muted>{'/mo' if o['total'] is not None else ''}</span></div><span class=plan>{e(o['plan'])}</span><ul class=math>" + "".join(f"<li>{e(l)}</li>" for l in o["math"]) + "</ul></div>"
    return f"<div class='grid est'>{out}</div>"
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
     f"<h1>{e(nm)} pricing: what it really costs a Shopify store</h1><p class=lead>{e(a['summary'])}</p><p class=metaline>{conf(a)}{flag(a)}<span class=muted>Price checked on {a['checked']} from the official source.</span></p>{HERO_END}"
     f"<h2>Plans</h2>{plans_table(a)}<h2>How AI usage is billed</h2><p>{e(a['ai_billing'])}</p>"
     f"<h2>Estimated monthly cost by store size</h2>{est_block(a)}<p class=muted>Assumptions: AI resolves {int(RATE*100)}% of conversations; monthly billing unless noted; taxes, add-ons, SMS/voice and phone fees excluded. <a href='methodology.html'>How we calculate</a>.</p>"
     f"{unc}{fa}" + (f"<p class=muted>Note: {e(a['notes'])}</p>" if a["notes"] else "")
     + f"<p><a class=btn href='{e(link(a))}' rel='nofollow noopener' target='_blank'>See {e(nm)}'s official pricing</a>" + (f"<a class='btn alt' href='{e(a['affiliate_url'])}' rel='sponsored noopener' target='_blank'>Try {e(nm)} (affiliate link)</a>" if a.get("affiliate_url") else "") + (f"<a class='btn alt' href='{e(a['shopify_url'])}' rel='nofollow noopener' target='_blank'>Shopify App Store listing</a>" if a.get("shopify_url") and a["shopify_url"] != link(a) else "") + "</p>"
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
     f"<h1>{e(na)} vs {e(nb)} pricing</h1><p class=lead>How {e(na)} and {e(nb)} bill for AI, and what each would cost the same Shopify store, using official prices checked {S['updated']}.</p>{HERO_END}{sizes_html}"
     f"<div class=tw><table class=vs><thead><tr><th></th><th>{e(na)}</th><th>{e(nb)}</th></tr></thead><tbody>{rows}</tbody></table></div><h2>Bottom line on cost</h2><ul>{''.join(lines)}</ul>" + vs_btns({**a, "_n": na}, {**b, "_n": nb}) +
     "<p class=muted>Cost is only one factor. Features, channels, integrations and AI quality differ, and your real volume and resolution rate will move these numbers. See the full math on each app's page.</p>" + NEWS)

# ---- Gorgias alternatives
alts = [o for o in ordered if o["slug"] != "gorgias"]
page("gorgias-alternatives.html", "Gorgias Alternatives 2026: Real Monthly Cost of 12 AI Support Apps for Shopify | ShopAI Ledger",
 "Gorgias alternatives for Shopify compared on real monthly cost at three store sizes: Tidio, Intercom Fin, Zendesk, HubSpot, Richpanel, Re:amaze, Freshdesk, Zipchat, Chatty and Shopify Inbox.",
 f"<h1>Gorgias alternatives, compared on real cost</h1><p class=lead>For reference, Gorgias comes out at about <b>{money(BY['gorgias']['est'][0])}</b> (small), <b>{money(BY['gorgias']['est'][1])}</b> (medium) and <b>{money(BY['gorgias']['est'][2])}</b> (large) a month on our assumptions (<a href='gorgias-pricing.html'>see the math</a>). Here's how the alternatives price out for the same store.</p>{HERO_END}"
 f"{sizes_html}{table(alts)}<p class=muted>Some of these are full helpdesks, and others (Zipchat, Chatty, Shopify Inbox) are chat/AI layers only. Compare like with like. <a href='methodology.html'>How we calculate</a>.</p>{NEWS}")

# ---- search & recommendations: category landing
page(SLAND, "Shopify AI Search & Product Recommendation Apps: Real Monthly Cost Compared (2026) | ShopAI Ledger",
 f"Real monthly cost of {len(SA)} Shopify AI search, filter and recommendation apps (Searchanise, Boost, Fast Simon, Doofinder, Algolia, Wiser, LimeSpot, Rebuy, Klevu, Nosto) at three store sizes, with the math. Checked {S['updated']}.",
 f"<h1>What Shopify AI search & recommendation apps really cost</h1><p class=lead>Search and recommendation apps bill on completely different things: product count, store visits, keystrokes, orders or revenue. We converted each official price list into one monthly bill for the same three stores.</p>{HERO_END}"
 f"{ssizes_html}<p class=muted>Prices checked {S['updated']} from official pricing pages and Shopify App Store listings. Monthly billing unless noted. Sorted by medium-store cost. \"Not public / check site\" means the vendor doesn't publish a price for that size, so we don't guess.</p>{stable(sordered)}"
 f"<div class=callout><b>The free option first.</b> <a href='shopify-search-discovery-pricing.html'>Shopify Search & Discovery</a> is free. It adds filters, synonyms, product boosts and related-product recommendations, and Shopify says semantic (AI) understanding is built into its online store search. Paid apps earn their keep with big catalogs, merchandising rules, personalization and upsell widgets.</div>"
 f"<h2>Comparisons</h2><ul>{scomp_links}</ul>"
 "<h2>What each app bills on</h2><div class=grid><div class=card><b>Product count</b><p class=muted>Searchanise: flat price by catalog size, unlimited searches.</p></div><div class=card><b>Sessions or search requests</b><p class=muted>Fast Simon counts store sessions. Doofinder and Algolia count search requests, which with search-as-you-type means keystrokes, so traffic spikes can push you up a plan.</p></div>"
 "<div class=card><b>Orders or revenue</b><p class=muted>Wiser, LimeSpot Turbo and Rebuy price by monthly orders. Boost (GMV) and LimeSpot Max price by revenue, so the bill grows as you sell more.</p></div><div class=card><b>Quote only</b><p class=muted>Klevu/Searchspring (Athos Commerce) and Nosto don't publish prices and sell annual plans.</p></div></div>"
 f"<p class=muted>Not all of these do the same job: Wiser, LimeSpot and Rebuy are mainly recommendation/upsell tools, while Searchanise, Boost, Fast Simon, Doofinder and Algolia are mainly search & filter tools. <a href='methodology.html#search'>How we calculate</a>.</p>{NEWS}",
 head=ld({"@context": "https://schema.org", "@type": "ItemList", "name": "Shopify AI search & recommendation apps", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{S['base_url']}/{a['slug']}-pricing.html", "name": a["name"]} for i, a in enumerate(sordered)]}))

# ---- search app pages
def splans_table(a):
    rows = "".join(f"<tr><td><b>{e(p['name'])}</b></td><td class=n data-l='Monthly'>{m(p['monthly']) if p['monthly'] is not None else '—'}</td><td class=n data-l='Annual /mo'>{m(p['annual']) if p['annual'] is not None else '—'}</td><td>{e(p['includes'])}</td></tr>" for p in a["plans"])
    return f"<div class=tw><table class=plans><thead><tr><th>Plan</th><th>Monthly billing</th><th>Annual (per mo)</th><th>What's included</th></tr></thead><tbody>{rows}</tbody></table></div>"
def sest_block(a):
    out = ""
    for s, o in zip(SSIZES, a["est"]):
        out += f"<div class=card><b>{s['label']}</b> <span class=muted>({s['products']:,} products, {s['orders']:,} orders, {m(s['revenue'])} revenue, {s['sessions']:,} sessions, {s['requests']:,} search requests a month)</span><div class='num{"" if o["total"] is not None else " np"}'>{smoney(o)}<span class=muted>{'/mo' if o['total'] is not None else ''}</span></div><span class=plan>{e(o['plan'])}</span><ul class=math>" + "".join(f"<li>{e(l)}</li>" for l in o["math"]) + "</ul></div>"
    return f"<div class='grid est'>{out}</div>"
for a in SA:
    nm = sshort(a); rel = [c for c in SCOMPS if a["slug"] in c]
    rel_html = " · ".join(f"<a href='{cslug(x,y)}'>{e(sshort(SBY[x]))} vs {e(sshort(SBY[y]))}</a>" for x, y in rel) + "".join(f" · <a href='{x}-alternatives.html'>{e(sshort(SBY[x]))} alternatives</a>" for x in SALTS if x == a["slug"])
    others = " · ".join(f"<a href='{o['slug']}-pricing.html'>{e(sshort(o))}</a>" for o in SA if o is not a)
    unc = ("<div class=callout><b>Not confirmed / not public:</b><ul>" + "".join(f"<li>{e(u)}</li>" for u in a["unconfirmed"]) + "</ul>Check the vendor's site for these.</div>") if a["unconfirmed"] else ""
    srcs = "".join(f"<li><a href='{e(u)}' rel='nofollow noopener' target='_blank'>{e(l)}</a> (checked {a['checked']})</li>" for l, u in a["sources"])
    fa = (f"<div class=box><b>Free Shopify alternative:</b> {e(a['free_alt'])} <a href='shopify-search-discovery-pricing.html'>See Shopify Search & Discovery</a>.</div>" if a["model"] != "free" else "")
    faq = [(f"How much does {nm} cost per month?", f"On our assumptions: {smoney(a['est'][0])} for a small store, {smoney(a['est'][1])} for a medium store and {smoney(a['est'][2])} for a large store. Prices checked {a['checked']}."),
           (f"How does {nm} charge?", a["ai_billing"])]
    page(f"{a['slug']}-pricing.html", f"{nm} Pricing 2026: Plans & Real Monthly Cost for Shopify Stores | ShopAI Ledger",
     f"{nm} pricing explained: plans, what it bills on ({a['unit'].lower()}), and the estimated monthly cost for small, medium and large Shopify stores, with the math. Checked {a['checked']}.",
     f"<p class=crumb><a href='{SLAND}'>Search & recommendations</a> › {e(nm)}</p><h1>{e(nm)} pricing: what it really costs a Shopify store</h1><p class=lead>{e(a['summary'])}</p><p class=metaline>{sconf(a)}{sflag(a)}<span class=muted>Price checked on {a['checked']} from the official source.</span></p>{HERO_END}"
     f"<h2>Plans</h2>{splans_table(a)}<h2>How it's billed</h2><p>{e(a['ai_billing'])}</p>"
     f"<h2>Estimated monthly cost by store size</h2>{sest_block(a)}<p class=muted>Monthly billing unless noted; taxes, add-ons, setup/developer work and negotiated discounts excluded. <a href='methodology.html#search'>How we calculate</a>.</p>"
     f"{unc}{fa}" + (f"<p class=muted>Note: {e(a['notes'])}</p>" if a["notes"] else "")
     + f"<p><a class=btn href='{e(a['pricing_url'])}' rel='nofollow noopener' target='_blank'>See {e(nm)}'s official pricing</a>" + (f"<a class='btn alt' href='{e(a['affiliate_url'])}' rel='sponsored noopener' target='_blank'>Try {e(nm)} (affiliate link)</a>" if a.get("affiliate_url") else "") + (f"<a class='btn alt' href='{e(a['shopify_url'])}' rel='nofollow noopener' target='_blank'>Shopify App Store listing</a>" if a.get("shopify_url") and a["shopify_url"] != a["pricing_url"] else "") + "</p>"
     f"<h2>Sources</h2><ul class=muted>{srcs}</ul>" + (f"<p>Compare: {rel_html.lstrip(' ·')}</p>" if rel_html else "") + f"<p class=muted>Other search & recommendation apps: {others}</p>{NEWS}",
     head=ld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": t}} for q, t in faq]}))

# ---- search comparison pages
for x, y in SCOMPS:
    a, b = SBY[x], SBY[y]; na, nb = sshort(a), sshort(b)
    lines = []
    for s, oa, ob in zip(SSIZES, a["est"], b["est"]):
        if oa["total"] is None or ob["total"] is None: lines.append(f"<li><b>{s['label']}:</b> can't compare exactly, because one price isn't public at this size ({e(na)}: {e(smoney(oa))}, {e(oa['plan'])}; {e(nb)}: {e(smoney(ob))}, {e(ob['plan'])}).</li>")
        elif oa["total"] == ob["total"]: lines.append(f"<li><b>{s['label']}:</b> same estimated cost ({smoney(oa)}).</li>")
        else:
            lo, hi, ol, oh = (na, nb, oa, ob) if oa["total"] < ob["total"] else (nb, na, ob, oa)
            lines.append(f"<li><b>{s['label']}:</b> {e(lo)} is lower on our assumptions ({smoney(ol)} vs {smoney(oh)}, a {m(round(oh['total']-ol['total'],2))}/mo difference).</li>")
    rows = "".join(f"<tr><th>{lab}</th><td>{fa_}</td><td>{fb}</td></tr>" for lab, fa_, fb in [
        ("Type", e(a["type"]), e(b["type"])), ("Billed on", e(a["unit"]), e(b["unit"])), ("How it's billed", e(a["ai_billing"]), e(b["ai_billing"])),
        *[(f"{s['label']}", f"<b>{smoney(oa)}</b><br><span class=muted>{e(oa['plan'])}</span>", f"<b>{smoney(ob)}</b><br><span class=muted>{e(ob['plan'])}</span>") for s, oa, ob in zip(SSIZES, a["est"], b["est"])],
        ("Free Shopify alternative", e(a["free_alt"]), e(b["free_alt"])), ("Checked", a["checked"], b["checked"]),
        ("Details", f"<a href='{x}-pricing.html'>{e(na)} pricing & math</a>", f"<a href='{y}-pricing.html'>{e(nb)} pricing & math</a>")])
    page(cslug(x, y), f"{na} vs {nb} Pricing (2026): Real Monthly Cost for Shopify Stores | ShopAI Ledger",
     f"{na} vs {nb}: what each bills on, and the estimated monthly cost for small, medium and large Shopify stores side by side. Prices checked {S['updated']}.",
     f"<p class=crumb><a href='{SLAND}'>Search & recommendations</a> › Comparison</p><h1>{e(na)} vs {e(nb)} pricing</h1><p class=lead>{e(na)} bills on {e(a['unit'].lower())}; {e(nb)} bills on {e(b['unit'].lower())}. Here's what each would cost the same Shopify store, using official prices checked {S['updated']}.</p>{HERO_END}{ssizes_html}"
     f"<div class=tw><table class=vs><thead><tr><th></th><th>{e(na)}</th><th>{e(nb)}</th></tr></thead><tbody>{rows}</tbody></table></div><h2>Bottom line on cost</h2><ul>{''.join(lines)}</ul>" + vs_btns({**a, "_n": na}, {**b, "_n": nb}) +
     "<p class=muted>Cost is only one factor. Features, merchandising controls, AI quality and integrations differ, and your real catalog, traffic and orders will move these numbers. See the full math on each app's page.</p>" + NEWS)

# ---- search alternatives pages
for x in SALTS:
    a = SBY[x]; na = sshort(a); alts = [o for o in sordered if o["slug"] != x]
    ref = " / ".join(f"<b>{smoney(o)}</b> ({s['label'].split()[0].lower()})" for s, o in zip(SSIZES, a["est"]))
    page(f"{x}-alternatives.html", f"{na} Alternatives 2026: Real Monthly Cost of {len(alts)} Shopify AI Search & Recommendation Apps | ShopAI Ledger",
     f"{na} alternatives for Shopify compared on real monthly cost at three store sizes: Searchanise, Fast Simon, Doofinder, Algolia, Wiser, LimeSpot, Rebuy, Nosto and the free Shopify Search & Discovery.",
     f"<p class=crumb><a href='{SLAND}'>Search & recommendations</a> › Alternatives</p><h1>{e(na)} alternatives, compared on real cost</h1><p class=lead>For reference, {e(na)} comes out at {ref} on our assumptions (<a href='{x}-pricing.html'>see the math</a>). Here's how the alternatives price out for the same store.</p>{HERO_END}"
     f"{ssizes_html}{stable(alts)}<p class=muted>Some of these are search & filter apps, and others (Wiser, LimeSpot, Rebuy) focus on recommendations and upsells. Compare like with like. <a href='methodology.html#search'>How we calculate</a>.</p>{NEWS}")

# ---- change log
CL = D.get("changelog") or []
page("changelog.html", "Shopify AI App Price Change Log | ShopAI Ledger", "A dated log of pricing and plan changes for Shopify AI apps (customer support, search and product recommendations), updated weekly.",
 "<h1>Price change log</h1><p class=lead>Every pricing or plan change we spot, dated. We re-check every app's official pricing page weekly.</p><!--/hero-->"
 + "".join(f"<div class=box><b>{e(c['date'])}</b>: {e(c['title'])}<ul>" + "".join(f"<li>{e(i)}</li>" for i in c["items"]) + "</ul></div>" for c in CL) + NEWS)

# ---- methodology
page("methodology.html", "How We Calculate Shopify AI App Costs | ShopAI Ledger", "The store sizes, assumptions and formulas ShopAI Ledger uses to estimate the real monthly cost of Shopify AI support, search and recommendation apps.",
 f"""<h1>How we calculate</h1><!--/hero--><div class=box><h2 style="margin-top:0">Sources</h2><ul><li>Every price comes from the vendor's official pricing page or its official Shopify App Store listing, read by hand. No scraping, no third-party price lists.</li>
<li>Each app shows the date we checked it and links the source. If a number isn't published, we say <b>"Not public / check site"</b> instead of guessing.</li><li>We re-check weekly and log changes on the <a href="changelog.html">change log</a>.</li></ul></div>
<div class=box><h2 style="margin-top:0">Support apps: store sizes</h2>{sizes_html}<p>For support apps we size stores by <b>support conversations per month</b>, not orders, because conversations are what these apps bill. Seats are the number of human agents paying for a seat.</p></div>
<div class=box><h2 style="margin-top:0">Assumptions</h2><ul><li><b>AI resolves {int(RATE*100)}% of conversations.</b> Vendors advertise 50–75%+; your rate may be higher or lower, and the cost scales with it.</li>
<li><b>Per-resolution apps</b> (Gorgias, Zendesk, Intercom Fin, HubSpot, Re:amaze, Siena) are charged for the resolved {int(RATE*100)}%.</li><li><b>Per-conversation, per-session or per-reply apps</b> (Tidio Lyro, Chatty, Richpanel, Freshdesk, Zipchat) are charged for every conversation the AI touches, which we assume is all of them.</li>
<li>Included allowances (e.g. 5 resolutions per agent, 3,000 HubSpot credits) are subtracted first.</li><li>We use <b>monthly-billing</b> prices where published; where only annual prices are public we say so. We pick the cheapest published plan that fits the size.</li>
<li>Excluded: taxes, SMS/voice/WhatsApp fees, optional add-ons (Copilot etc.), one-time fees (shown separately) and negotiated discounts.</li></ul></div>
<div class=box id=search><h2 style="margin-top:0">Search & recommendation apps: store sizes</h2>{ssizes_html}<p>These apps bill on different things, so each store size is described by every unit a vendor bills on: <b>active products</b> (Searchanise), <b>monthly sessions</b>, meaning all store visits (Fast Simon), <b>search requests</b> (Doofinder, Algolia), <b>orders per month</b> (Wiser, LimeSpot Turbo, Rebuy) and <b>monthly online revenue/GMV</b> (Boost, LimeSpot Max, Nosto).</p>
<ul><li><b>Search requests</b> assume about 15% of sessions use search and each search session sends about 10 requests (search-as-you-type sends a request per keystroke), so roughly 1.5 requests per session. Your theme and traffic can change this a lot.</li>
<li>We pick the <b>cheapest published plan that covers the store</b> on the app's billing unit, at monthly-billing prices. If the store is above the largest published plan, or the vendor only quotes, we show <b>"Not public / check site"</b>.</li>
<li>Algolia is pay-as-you-go: we price search requests on Grow Plus (its AI tier) and leave out recommendation requests, developer time and connectors.</li>
<li>Excluded: taxes, setup/developer work, optional add-ons (e.g. premium support) and negotiated or annual discounts.</li></ul></div>
<p>Spotted an error? <a href="mailto:{S['contact']}?subject=ShopAI%20Ledger%20correction">Email a correction</a>. App makers are welcome to send corrections too, and we'll verify them against your public pricing page.</p>""")

# ---- disclosure
page("disclosure.html", "Affiliate Disclosure | ShopAI Ledger", "How ShopAI Ledger makes money and how that is kept separate from prices and rankings.",
 """<h1>Affiliate disclosure</h1><!--/hero--><div class=box><p><b>ShopAI Ledger earns a commission from some apps.</b> If you sign up through a link labelled "affiliate link", the app maker may pay us, at no extra cost to you. Every "official pricing" link still goes straight to the vendor with no tracking.</p>
<p>Apps we're currently an affiliate of: Gorgias (since 18 Oct 2026) and Searchanise (since 24 Oct 2026). This list is updated whenever that changes. Affiliate status never changes the prices we show, the math, or the sort order (always by estimated cost).</p>
<p>We may also offer clearly-labelled sponsored placements. Sponsored content is always marked "Sponsored" and never changes an app's price data. See <a href="advertise.html">Advertise</a>.</p></div>""")

# ---- advertise
page("advertise.html", "Advertise or Get Your App Listed | ShopAI Ledger", "App makers: get your Shopify AI app listed, correct your pricing, or sponsor The Ledger newsletter.",
 f"""<h1>Advertise / get your app listed</h1><p class=lead>ShopAI Ledger is read by Shopify merchants comparing what AI apps really cost.</p><!--/hero-->
<div class=grid><div class=card><b>Free listing</b><p class=muted>Have a Shopify AI support, search or recommendation app with public pricing? Send us the link, and we list apps for free if the pricing is public.</p></div>
<div class=card><b>Pricing corrections</b><p class=muted>Changed your plans? Tell us and we'll re-check against your public pricing page within a week.</p></div>
<div class=card><b>Sponsorship</b><p class=muted>Featured placements and sponsor slots in The Ledger, our Monday newsletter with a Thursday deep-dive, on <a href="https://shopailedger.substack.com">Substack</a>. Always labelled as sponsored. Placements never change price data.</p></div></div>
<p><a class=btn href="mailto:{S['contact']}?subject=ShopAI%20Ledger%20listing%20%2F%20sponsorship">Contact us</a></p>""")

(R / "style.css").write_text(CSS)
(R / "favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#0c0c0c"/><rect x="7" y="9" width="18" height="2.6" rx="1.3" fill="#f3efe6"/><rect x="7" y="14.7" width="11.5" height="2.6" rx="1.3" fill="#f3efe6"/><rect x="7" y="20.4" width="14.5" height="2.6" rx="1.3" fill="#f3efe6" fill-opacity=".55"/></svg>')
(R / "404.html").write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Not found | ShopAI Ledger</title><meta name="robots" content="noindex"><link rel="icon" href="/shopai-ledger/favicon.svg" type="image/svg+xml">{FONTS}<link rel="stylesheet" href="/shopai-ledger/style.css"></head><body><section class="hero"><div class="wrap"><p class="eyebrow">( 404 )</p><h1>Page not <em>found</em></h1><p style="margin:0"><a class="btn light" href="/shopai-ledger/">Go to the ShopAI Ledger comparison</a></p></div></section></body></html>')
(R / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{S['base_url']}/{'' if p=='index.html' else p}</loc><lastmod>{S['updated']}</lastmod></url>\n" for p in PAGES) + "</urlset>\n")
(R / "sitemap.txt").write_text("".join(f"{S['base_url']}/{'' if p=='index.html' else p}\n" for p in PAGES))
(R / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {S['base_url']}/sitemap.xml\nSitemap: {S['base_url']}/sitemap.txt\n")
(R / ".nojekyll").write_text("")
print("built", len(PAGES), "pages")
