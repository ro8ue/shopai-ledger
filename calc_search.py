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
    turbo = None
    for cap, price in p["turbo"]:
        if s["orders"] <= cap:
            turbo = (cap, price)
            break
    else:
        # above last published cap: use last price (open tier)
        turbo = (p["turbo"][-1][0], p["turbo"][-1][1])
    maxp = None
    for cap, price in p["max"]:
        if s["revenue"] <= cap:
            maxp = (cap, price)
            break
    if maxp is None and turbo is None:
        return dict(total=None, plan="Contact us", math=["Above published Turbo/Max tiers: contact LimeSpot."])
    # Pick the cheaper published plan (Turbo is not for Shopify Plus)
    candidates = []
    if turbo is not None:
        candidates.append(("Turbo", turbo[0], turbo[1], "orders"))
    if maxp is not None:
        candidates.append(("Max", maxp[0], maxp[1], "revenue"))
    plan, cap, price, kind = min(candidates, key=lambda x: x[2])
    other = [c for c in candidates if c[0] != plan]
    lines = [f"Your store: {s['orders']:,} orders/mo, {m(s['revenue'])} revenue/mo"]
    if kind == "orders":
        lines.append(f"Turbo up to {cap:,} orders = {m(price)}/mo (not for Shopify Plus)")
    else:
        lines.append(f"Max up to {m(cap)} revenue/30 days = {m(price)}/mo")
    if other:
        op, oc, opr, ok = other[0]
        if ok == "orders":
            lines.append(f"{op} would be {m(opr)}/mo at your order volume")
        else:
            lines.append(f"{op} would be {m(opr)}/mo at your revenue")
        lines.append(f"We show the cheaper plan ({plan}).")
    return dict(total=price, plan=plan, math=lines)

def quote(p, s, i):
    return dict(total=p["totals"][i], plan=p["plans"][i], math=[p["msgs"][i]])

MODELS = dict(free=free, tiered=tiered, algolia=algolia, limespot=limespot, quote=quote)
