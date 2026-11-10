"""Hunting parties (brief 4b §3.1): declared, never inferred.

Two people hunting the same wood on the same day hunt separately: they share its game and add to each other's disturbance. A party
is made only by `with: X` on a hunting act: the follower joins X's party and hunts X's way (X's method, place, range, target and
units); its own settings are only its fallback. X takes followers unless it hunts `alone` or names `only` those it takes. If X does
not hunt that day, or refused this follower, or the follower is not at X's place, the follower hunts alone with its own settings.
Chains (A with B, B with C) follow to the one who leads (C); a circle (A with B, B with A, or longer) is led by its better hunter:
the highest skill at its own chosen method, then familiarity with what it named, then the elder, then a keyed draw.

The day's plans are read once, before the acts (`resolve`): each party's acts are then recorded as they come (`record`, from the
hunting act) and the party's hunt is settled once, after the day's acts (`settle`), as partnerships and joins are: its members learn
how it went together in the day's results. A hunter alone learns at once, as before.
"""
from __future__ import annotations

from cybertron2.engine import knowledge as KN
from cybertron2.engine.data import TECHNIQUES


def hunting(a) -> str | None:
    """The hunting method an act names (a gather by a hunt in the wild layer, not a set work), or None."""
    if not isinstance(a, dict) or str(a.get("do", "")).lower().strip() != "gather":
        return None
    tech = KN.resolve(a.get("what"), "gather")
    if tech is None:
        return None
    d = TECHNIQUES.get(tech) or {}
    if d.get("modifies"):                                                     # a modifier written as the method: its base
        base = next((x.split(":", 1)[1] for x in d["modifies"] if x.startswith("gather:")), None)
        tech, d = base, TECHNIQUES.get(base) or {}
    return tech if (d.get("yield") or {}).get("kind") == "wild_take" and not d.get("set") else None


def _names(x) -> list:
    if isinstance(x, (list, tuple)):
        return [str(v).strip() for v in x if str(v).strip()]
    return [v.strip() for v in str(x or "").replace(" and ", ",").split(",") if v.strip()]


def _person(w, x) -> str | None:
    """The person a name means: exact, else by first name (the people's names as written)."""
    x = str(x or "").strip()
    if x in w.s["people"]:
        return x
    low = x.lower()
    hits = [n for n in w.s["people"] if n.lower() == low or n.lower().split()[0] == low]
    return hits[0] if len(hits) == 1 else None


def _alone(a) -> bool:
    v = a.get("alone")
    return v is True or str(v).strip().lower() in ("true", "yes", "1")


def _better(w, names, acts) -> str:
    """A circle's leader: the highest skill at its own chosen method, then familiarity with what it named, then the elder, then a
    keyed draw."""
    from cybertron2.engine import wild as WL
    from cybertron2.engine.data import RESOURCES
    kinds = [k for k, r in RESOURCES.items() if r.get("taken")]

    def key(n):
        a = acts[n]
        tech = hunting(a)
        skill = float(((w.s["know"].get(n) or {}).get(tech) or {}).get("skill", 0.0))
        fam = (w.s["mind"].get(n) or {}).get("familiar") or {}
        named = WL._wanted(a.get("looking for"), kinds)
        f = max([float(fam.get(k, 0.0)) for k in named] or [0.0])
        elder = -float(w.s["people"][n].get("born") or 0)                     # born earlier: the elder
        return (skill, f, elder, w.rng("party-circle", w.d, n).random())
    return max(sorted(names), key=key)


def resolve(w, plans: dict) -> dict:
    """Read the day's plans before the acts: who hunts with whom. Writes today's `parties` ({member: leader}, for parties of two or
    more) and rewrites each follower's hunting act in `plans` to its leader's, keeping its own as the fallback (`_own`). Returns the
    parties as {leader: [followers]}."""
    today = w.s["today"]
    acts = {}
    for n, plan in sorted(plans.items()):
        for j, a in enumerate(plan or []):
            if hunting(a):
                acts[n] = a
                break
    at = {n: w.at(n) for n in acts}
    follow = {}
    for n, a in sorted(acts.items()):
        x = _person(w, a.get("with")) if a.get("with") not in (None, "", False) else None
        if x and x != n and x in acts and at[x] == at[n] and at[n] is not None:
            follow[n] = x
    while True:                                                               # circles: led by the better hunter
        changed = False
        for start in sorted(follow):
            seen, n = [], start
            while n in follow and n not in seen:
                seen.append(n)
                n = follow[n]
            if n in seen:
                circle = seen[seen.index(n):]
                lead = _better(w, circle, acts)
                for c in circle:
                    if c != lead:
                        follow[c] = lead
                follow.pop(lead, None)
                changed = True
                break
        if not changed:
            break

    def root(n):
        while n in follow:
            n = follow[n]
        return n
    while True:                                                               # the leader takes followers unless it chose otherwise
        drop = None
        for n in sorted(follow):
            r = root(n)
            ra = acts[r]
            only = {_person(w, x) for x in _names(ra.get("only"))} if ra.get("only") not in (None, "", False) else None
            if _alone(ra) or (only is not None and n not in only):
                drop = n
                break
        if drop is None:
            break
        follow.pop(drop)
    parties = {}
    for n in sorted(follow):
        parties.setdefault(root(n), []).append(n)
    members = {}
    for lead, fs in sorted(parties.items()):
        members[lead] = lead
        la = acts[lead]
        for f in fs:
            members[f] = lead
            own = acts[f]
            new = {k: v for k, v in la.items() if k not in ("with", "alone", "only", "lead")}   # the led beast is the leader's
            new.update(_party=lead, _own={k: v for k, v in own.items() if not str(k).startswith("_")})
            plan = plans[f]
            plan[plan.index(own)] = new
        plans[lead][plans[lead].index(la)] = {**la, "_party": lead}
    if members or today.get("parties"):                                       # nothing written on a day with no parties
        today["parties"] = members
    return parties


def member_of(here) -> str | None:
    """The leader of the party one hunts in today, if one hunts in a party of two or more."""
    return (here.today().get("parties") or {}).get(here.name)


def cost(here, a, c, left) -> int:
    """A follower with fewer units than its leader's hunt goes out with the party for what it has (at least the walk and a unit of
    search) and turns back when they are spent."""
    if not a.get("_party") or a.get("_party") == here.name or c <= left:
        return c
    tech = hunting(a)
    search = int(TECHNIQUES[tech]["units"]) if tech else c
    walk = c - search
    return left if left >= walk + 1 else c


def record(here, mind, tech, key, place_name, out, m_skill, a) -> str:
    """A hunting act in a party: kept to be settled after the day's acts. The units are spent and the method practised now."""
    lead = member_of(here)
    full = int(TECHNIQUES[tech]["units"])
    spent = a.get("_units")
    t = full if spent is None else max(1, full - max(0, int(_cost_full(here, a)) - int(spent)))
    ox = (a.get("_mods") or {}).get("_ox")
    acts = here.today().setdefault("party_acts", {}).setdefault(lead, {})
    acts[here.name] = {"tech": tech, "key": key, "place": place_name, "out": out, "skill": round(float(m_skill), 4), "t": t, "ox": ox,
                       "node": here.node, "a": {k: v for k, v in a.items() if k != "_own"}}
    who = [n for n, l in sorted((here.today().get("parties") or {}).items()) if l == lead and n != here.name]
    with_ = ", ".join(who)
    return (f"You set out {KN.label(tech)} with {with_}" + ("" if lead == here.name else f", {lead} leading")
            + (f", for the {t} unit{'s' if t != 1 else ''} you had before turning back" if t < full else "")
            + "; how the hunt went is told at the day's end.")


def _cost_full(here, a) -> int:
    from cybertron2.engine import verbs as V
    return V.cost(here, {k: v for k, v in a.items() if k != "_units"})


def settle(w) -> dict:
    """Each party's hunt, once, after the day's acts (brief 4b §3.1): led by its leader (if the leader's hunt was not done, each
    follower hunts alone as it went out). Returns {person: [lines]} for the day's results."""
    from cybertron2.engine import wild as WL
    from cybertron2.engine.here import Here, Mind
    today = w.s["today"]
    out = {}
    for lead, acts in sorted((today.get("party_acts") or {}).items()):
        groups = [[lead] + sorted(n for n in acts if n != lead)] if lead in acts else [[n] for n in sorted(acts)]
        for names in groups:
            names = [n for n in names if w.s["people"][n]["alive"] and w.at(n) == acts[names[0]]["node"]]
            if not names:
                continue
            first = acts[names[0]]
            here0 = Here(w, names[0])
            ms = [WL.member(Here(w, n), Mind(w, n), acts[n]["out"], acts[n]["skill"], acts[n]["t"], acts[n].get("ox")) for n in names]
            tech = first["tech"]
            r = WL.hunt(here0, ms, tech, first["key"], first["place"], TECHNIQUES[tech]["yield"], first["a"])
            for n in names:
                out.setdefault(n, []).append(r["lines"][n] + r["tails"][n])
    if today.get("party_acts"):
        today["party_acts"] = {}
    return out
