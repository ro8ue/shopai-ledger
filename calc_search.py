"""Cost models for the Search & recommendations category. Each returns dict(total, plan, math); total=None means not public."""
from calc import m
LAB = dict(products="products", sessions="monthly sessions", orders="orders/mo", revenue="revenue/mo", requests="search requests/mo")
def fmt(metric, v): return m(v) if metric == "revenue" else f"{v:,}"

def free(p, s, i):
    return dict(total=0, plan="Free", math=["Free app, no usage fee. $0/mo (your Shopify plan is a separate cost)."])

def tiered(p, s, i):
    k = p["metric"]; v = s[k]
    for name, price, cap in p["plans"]:
        if v <= cap:
            return dict(total=price, plan=name, math=[f"Your store: {fmt(k, v)} {LAB[k]}", f"Cheapest plan that covers it: {name} (up to {fmt(k, cap)} {LAB[k]}) = {m(price)}/mo, monthly billing"])
    top = p["plans"][-1]
    return dict(total=None, plan="Above published plans", math=[f"Your store: {fmt(k, v)} {LAB[k]}", f"The largest published plan, {top[0]}, stops at {fmt(k, top[2])} {LAB[k]} ({m(top[1])}/mo). Above that it's a custom quote. Not public, check site."])

def algolia(p, s, i):
    r = s["requests"]; ex = max(0, r - p["incl"]); u = ex / 1000 * p["unit"]; ub = ex / 1000 * p["unit_basic"]
    return dict(total=round(u, 2), plan="Grow Plus (pay as you go)", math=[f"Search requests: {r:,} − {p['incl']:,} included = {ex:,} extra", f"{ex/1000:,.0f}K × {m(p['unit'])} per 1K = {m(round(u,2))}/mo (Grow Plus, with AI ranking/synonyms)",
        f"Records: {s['products']:,} products fit within the {p['records_incl']:,} included records (variants/replicas can add more)", f"Keyword-only Grow would be {m(round(ub,2))}/mo. Developer/integration time not included."])

def limespot(p, s, i):
    if s["orders"] <= p["turbo"][-1][0]:
        for cap, price in p["turbo"]:
            if s["orders"] <= cap:
                return dict(total=price, plan="Turbo", math=[f"Your store: {s['orders']:,} orders/mo", f"Turbo up to {cap:,} orders = {m(price)}/mo (LimeSpot's published example; not for Shopify Plus)", "Max (revenue-based) would be " + next(m(pr) for c, pr in p["max"] if s["revenue"] <= c) + "/mo at your revenue"])
    for cap, price in p["max"]:
        if s["revenue"] <= cap:
            return dict(total=price, plan="Max", math=[f"Your store: {s['orders']:,} orders/mo, {m(s['revenue'])} revenue/mo", f"Turbo prices above 250 orders aren't public, so we price Max: up to {m(cap)} revenue = {m(price)}/mo"])
    return dict(total=None, plan="Contact us", math=["Revenue above $5M/30 days: contact LimeSpot."])

def quote(p, s, i):
    return dict(total=p["totals"][i], plan=p["plans"][i], math=[p["msgs"][i]])

MODELS = dict(free=free, tiered=tiered, algolia=algolia, limespot=limespot, quote=quote)
