"""Cost models. Each returns dict(total, plan, math) for a store size, or total=None if not public."""
import math as M
def m(x):
    s = f"{x:,.2f}"
    return "$" + (s[:-3] if s.endswith(".00") else s)

def cheapest(opts):
    opts = [o for o in opts if o["total"] is not None]
    return min(opts, key=lambda o: o["total"])

def gorgias(p, conv, seats, ai):
    opts = []
    for name, base, tix, over, incl_ai in p["plans"]:
        extra_t = max(0, conv - tix); extra_ai = max(0, ai - incl_ai)
        t = base + extra_t * over + extra_ai * p["ai_unit"]
        lines = [f"{name} plan {m(base)}/mo (includes {tix:,} tickets, {incl_ai} AI interactions)",
                 f"Tickets: {conv:,} (AI-handled ones count as tickets too) → {extra_t:,} over × {m(over)} = {m(extra_t*over)}",
                 f"AI interactions: {ai:,} − {incl_ai} included = {extra_ai:,} × {m(p['ai_unit'])} = {m(extra_ai*p['ai_unit'])}"]
        opts.append(dict(total=t, plan=name, math=lines))
    o = cheapest(opts); o["math"].append(f"Cheapest plan at this size: {o['plan']} = {m(o['total'])}/mo. If AI goes over your committed allowance, Gorgias lists {m(p['ai_overage_note'])} per interaction.")
    return o

def tidio(p, conv, seats, ai):
    human = conv - ai; lyro_price, lyro_cap = p["lyro"]; cs_price, cs_cap = p["cs_starter"]
    if conv <= lyro_cap and human <= cs_cap:
        return dict(total=lyro_price + cs_price, plan="Lyro AI Agent + Customer Service Starter",
            math=[f"Lyro conversations: all {conv:,} chats get a Lyro reply → Lyro plan {m(lyro_price)} (up to {lyro_cap})",
                  f"Human-replied conversations: {human:,} → Customer Service Starter {m(cs_price)} (up to {cs_cap})",
                  f"Total {m(lyro_price)} + {m(cs_price)} = {m(lyro_price+cs_price)}/mo"])
    return dict(total=None, plan="Higher Lyro / Customer Service tiers",
        math=[f"Needs about {conv:,} Lyro conversations and {human:,} human conversations a month.",
              f"Tidio's public prices we could confirm stop at {lyro_cap} Lyro conversations ({m(lyro_price)}) and 250 human conversations (from $59). Not public, check site."])

def intercom(p, conv, seats, ai):
    s = seats * p["seat"]; f = ai * p["fin"]
    return dict(total=s+f, plan=f"Essential × {seats} seat{'s' if seats>1 else ''} + Fin",
        math=[f"Seats: {seats} × {m(p['seat'])} (monthly) = {m(s)}", f"Fin outcomes: {ai:,} × {m(p['fin'])} = {m(f)}",
              f"Total {m(s+f)}/mo. Outcomes can exceed full resolutions, since a handoff via a Fin workflow also counts."])

def zendesk(p, conv, seats, ai):
    s = seats * p["seat"]; inc = seats * p["incl_per_seat"]; ex = max(0, ai - inc); u = ex * p["payg"]
    return dict(total=s+u, plan=f"Suite Team × {seats} + pay-as-you-go resolutions",
        math=[f"Seats: {seats} × {m(p['seat'])} (monthly) = {m(s)}", f"Automated resolutions: {ai:,} − {inc} included = {ex:,} × {m(p['payg'])} = {m(u)}",
              f"Total {m(s+u)}/mo. With committed resolutions at {m(p['committed'])}: {m(s + ex*p['committed'])}/mo."])

def hubspot(p, conv, seats, ai):
    s = seats * p["seat"]; ex = max(0, ai - p["incl_res"]); u = ex * p["unit"]
    return dict(total=s+u, plan=f"Professional × {seats} seat{'s' if seats>1 else ''}",
        math=[f"Seats: {seats} × {m(p['seat'])} (monthly) = {m(s)}", f"Resolutions: {ai:,} − ~{p['incl_res']} covered by 3,000 included credits = {ex:,} × {m(p['unit'])} = {m(u)}",
              f"Total {m(s+u)}/mo, plus {m(p['onboarding'])} one-time onboarding."])

def free(p, conv, seats, ai):
    return dict(total=0, plan="Free", math=["Free app, no usage fee listed. $0/mo."])

def richpanel(p, conv, seats, ai):
    s = seats * p["seat"]; use = conv * p["per_conv"]; a = max(p["ai_min"], use)
    return dict(total=s+a, plan=f"{seats} helpdesk seat{'s' if seats>1 else ''} + AI meter",
        math=[f"Seats: {seats} × {m(p['seat'])} (monthly) = {m(s)}", f"AI: {conv:,} AI-handled conversations × ~{m(p['per_conv'])} = {m(use)}; minimum {m(p['ai_min'])} → {m(a)}",
              f"Total ≈ {m(s+a)}/mo (approximate: AI cost depends on tokens)."])

def reamaze(p, conv, seats, ai):
    s = seats * p["seat"]; inc = seats * p["incl_per_seat"]; ex = max(0, ai - inc); u = ex * p["unit"]
    return dict(total=s+u, plan=f"Basic × {seats} user{'s' if seats>1 else ''}",
        math=[f"Users: {seats} × {m(p['seat'])} = {m(s)}", f"AI resolutions: {ai:,} − {inc} included = {ex:,} × {m(p['unit'])} = {m(u)}", f"Total {m(s+u)}/mo"])

def freshdesk(p, conv, seats, ai):
    s = seats * p["seat"]; packs = M.ceil(conv / p["pack_size"]); u = packs * p["pack"]
    return dict(total=s+u, plan=f"Growth × {seats} (annual) + session packs",
        math=[f"Seats: {seats} × {m(p['seat'])} (annual billing) = {m(s)}", f"AI sessions: {conv:,} AI-handled conversations → {packs} packs × {m(p['pack'])} = {m(u)}", f"Total {m(s+u)}/mo"])

def zipchat(p, conv, seats, ai):
    for name, price, cap in p["plans"]:
        if conv <= cap:
            return dict(total=price, plan=name, math=[f"{conv:,} conversations fits {name} (~{cap:,} conversations) → {m(price)}/mo (monthly billing)"])
    return dict(total=p["scale_plus_annual"], plan="Scale Plus (annual)", math=[f"{conv:,} conversations exceeds Scale (~2,500). Scale Plus covers ~6,000 → {m(p['scale_plus_annual'])}/mo billed annually (monthly-billing price not public)."])

def siena(p, conv, seats, ai):
    u = ai * p["unit"]
    return dict(total=p["platform"] + u, plan="Platform + automation pack",
        math=[f"Platform fee {m(p['platform'])}", f"Automated tickets: {ai:,} × {m(p['unit'])} = {m(u)}", f"Total {m(p['platform']+u)}/mo + support/implementation (not public)"])

def chatty(p, conv, seats, ai):
    opts = []
    for name, price, cap in p["plans"]:
        ex = max(0, conv - cap); t = price + ex * p["unit"]
        opts.append(dict(total=t, plan=name, math=[f"{name} {m(price)} includes {cap:,} AI conversations; {ex:,} extra × {m(p['unit'])} = {m(ex*p['unit'])} → {m(t)}"]))
    o = cheapest(opts); o["math"].append(f"Cheapest plan at this size: {o['plan']} = {m(o['total'])}/mo"); return o

def helpcenter(p, conv, seats, ai):
    opts = []
    for name, price, cap, over in p["plans"]:
        ex = max(0, conv - cap); t = price + ex * over
        opts.append(dict(total=t, plan=name, math=[f"{name} {m(price)} includes {cap:,} tickets; {ex:,} extra × {m(over)} = {m(ex*over)} → {m(t)}"]))
    o = cheapest(opts); o["math"].append(f"Cheapest plan at this size: {o['plan']} = {m(o['total'])}/mo (no AI agent, AI FAQs only)"); return o

MODELS = dict(gorgias=gorgias, tidio=tidio, intercom=intercom, zendesk=zendesk, hubspot=hubspot, free=free, richpanel=richpanel,
              reamaze=reamaze, freshdesk=freshdesk, zipchat=zipchat, siena=siena, chatty=chatty, helpcenter=helpcenter)
