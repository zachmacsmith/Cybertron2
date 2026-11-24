"""The present population as an input: an explicit list of households, or a mix drawn into one by keyed draws (per village, per
household), so the list is reproducible and can be edited before the past is built.

A mix:
    villages: {Northby: {at: [0, 0], households: 8}, ...}
    forms: {couple_children: 0.6, couple_old: 0.1, widow_alone: 2, three_generations: 1, ...}
        a share (below 1) is spread over the households left; a count (1 or more) is placed exactly, in the villages by keyed draws
    size: [3, 7]                        household sizes for forms with children
Forms: couple_children, couple_old, widow_alone, widower_children, three_generations, stem, single_man, siblings.
Roles are written as pins only where the form names them (a widow is pinned 'widowed'; the others are inferred)."""
from __future__ import annotations

from .keyed import pick, u

FORMS = ("couple_children", "couple_old", "widow_alone", "widower_children", "three_generations", "stem", "single_man", "siblings")


def ri(seed, key, lo, hi):
    return lo + int(u(seed, *key) * (hi - lo + 1))


def children(seed, key, mother_age, n):
    """n children born to a mother now mother_age, two to four years apart, the eldest when she was 19 to 25."""
    out, a = [], mother_age - ri(seed, key + ("first",), 19, 25)
    for k in range(n):
        if a < 0:
            break
        out.append(a)
        a -= ri(seed, key + ("gap", k), 2, 4)
    return out


def household(seed, hid, form, size):
    k = (hid,)
    S = lambda *x: "m" if u(seed, hid, "sex", *x) < .5 else "f"
    n_kids = max(0, ri(seed, k + ("n",), size[0], size[1]) - 2)
    if form == "couple_children":
        h = ri(seed, k + ("h",), 24, 48)
        w = max(18, h - ri(seed, k + ("g",), 0, 6))
        return [{"age": h, "sex": "m", "role": "head"}, {"age": w, "sex": "f", "role": "spouse"}] + \
               [{"age": a, "sex": S(j)} for j, a in enumerate(children(seed, k, w, n_kids))]
    if form == "couple_old":
        h = ri(seed, k + ("h",), 55, 70)
        return [{"age": h, "sex": "m", "role": "head"}, {"age": h - ri(seed, k + ("g",), 0, 6), "sex": "f", "role": "spouse"}]
    if form == "widow_alone":
        return [{"age": ri(seed, k + ("h",), 50, 75), "sex": "f", "role": "widowed"}]
    if form == "widower_children":
        h = ri(seed, k + ("h",), 30, 45)
        return [{"age": h, "sex": "m", "role": "widowed"}] + [{"age": a, "sex": S(j)} for j, a in enumerate(children(seed, k, h - 3, n_kids))]
    if form == "three_generations":
        base = household(seed, hid, "couple_children", size)
        el = base[0]["age"] + ri(seed, k + ("e",), 20, 30)
        return base + [{"age": el, "sex": "f", "role": "parent"}]
    if form == "stem":
        h = ri(seed, k + ("h",), 55, 66)
        w = h - ri(seed, k + ("g",), 0, 5)
        son = w - ri(seed, k + ("s",), 20, 26)
        dw = son - ri(seed, k + ("dg",), 0, 5)
        return [{"age": h, "sex": "m", "role": "head"}, {"age": w, "sex": "f", "role": "spouse"}, {"age": son, "sex": "m", "role": "child"},
                {"age": dw, "sex": "f"}] + [{"age": a, "sex": S(j)} for j, a in enumerate(children(seed, k, dw, max(0, n_kids - 2)))]
    if form == "single_man":
        return [{"age": ri(seed, k + ("h",), 20, 35), "sex": "m", "role": "single"}]
    if form == "siblings":
        a = ri(seed, k + ("h",), 18, 30)
        return [{"age": a, "sex": "m", "role": "head"}, {"age": a - ri(seed, k + ("g",), 2, 5), "sex": "f", "role": "single"}]
    raise ValueError(form)


def draw(mix: dict, seed: int) -> dict:
    """A mix into an explicit present: each household's form, then its members, all by keyed draws."""
    V = mix["villages"]
    slots = [(v, j) for v in sorted(V) for j in range(int(V[v]["households"]))]
    forms = mix.get("forms") or {"couple_children": 1.0}
    size = mix.get("size") or [3, 7]
    assigned = {}
    for f, n in sorted(forms.items()):                               # counts first, into keyed slots
        if n >= 1:
            for k in range(int(n)):
                free = [s for s in slots if s not in assigned]
                s = pick(seed, ("slot", f, k), [(s, 1.0) for s in free])
                assigned[s] = f
    shares = [(f, n) for f, n in sorted(forms.items()) if n < 1]
    for s in slots:
        if s not in assigned:
            assigned[s] = pick(seed, ("form",) + s, shares) if shares else "couple_children"
    hh = []
    for v, j in slots:
        hid = f"{v[:2]}{j + 1}"
        ms = household(seed, hid, assigned[(v, j)], size)
        for k, m in enumerate(ms):
            m["id"] = f"{hid}.{k}"
        hh.append({"id": hid, "village": v, "form": assigned[(v, j)], "members": ms})
    return {"villages": {v: {"at": d["at"]} for v, d in V.items()}, "off": mix.get("off"), "span": mix.get("span", 100),
            "households": hh, "pins": mix.get("pins") or {}}
