"""The prototype's evaluation (generation_redesign.md §5's two risks): does a past built backward to a pinned present read as
likely (against the forward model's truth, and against a null arm with the forward model's weights taken out), is it the same
every time, does an edit move only what it must, and what does it do with odd or impossible pins?

    python -m proto.peoplegen.evaluate [--seeds 40] [--out proto/peoplegen/results]
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import statistics as stt
import time

from . import forward as FW
from . import present as PR
from . import solver as S
from . import stats as ST
from . import write as WR
from .genealogy import Build

REGION = {"villages": {"Northby": {"at": [0, 0]}, "Eastwick": {"at": [1.0, 0.3]}, "Southam": {"at": [0.4, 1.2]},
                       "Westcot": {"at": [-0.8, 0.6]}},
          "off": {"name": "Kingsmarket", "at": [2.6, 0.2]}}


class Flat(Build):
    """The null arm: the same decisions and constraints, every candidate the model allows weighted alike."""

    def cands(self, var):
        return [(k, 1.0) for k, w in super().cands(var) if w > 0]


def run(spec, seed, prev=None, cls=Build):
    b = cls(copy.deepcopy(spec), seed)
    a, st = S.solve(b, seed, prev=prev)
    return b, a, st


def digest(a, b) -> str:
    x = {"a": sorted((k, repr(v)) for k, v in a.items()),
         "p": sorted((i, p.born, p.pc, p.died) for i, p in b.P.items())}
    return hashlib.sha256(json.dumps(x).encode()).hexdigest()[:16]


def flags(b, st, cut=0.5) -> list:
    """Where a pin forced an unlikely past: decisions whose likelier readings (at least half the model's weight) the constraints
    ruled out, couples with nine or more children, villages founded within 25 years."""
    out = []
    for v, r in sorted(st["forced"].items()):
        if r >= cut and v.split(":")[0] in ("par", "pairs", "age"):
            out.append(f"{v}: {100 * r:.0f}% of the model's weight ruled out")
    for c in b.C.values():
        n = len(c.kids)
        if n >= 9:
            out.append(f"{c.id}: {n} children to one couple")
    young = [v for v, F in b.F.items() if F > -25]
    for v in young:
        out.append(f"{v}: founded {-b.F[v]} years ago")
    return out


def check(b) -> list:
    """The past's invariants, checked on the built world: each mother 15 to 47 and each father 16 to 72 at a birth; both alive
    at it (a father up to a year before); births a year apart; no wedding after a spouse's death; no spouses sharing a parent
    or grandparent; a dead spouse's children before the living spouse's; the absent dead before now, the living not dead."""
    bad = []
    P, C = b.P, b.C
    for c in C.values():
        m, f = P[c.m], P[c.f]
        bs = sorted(P[k].born for k in c.kids)
        for k in c.kids:
            y = P[k].born
            if m.born is not None and not 15 <= y - m.born <= 47:
                bad.append(f"{k}: mother {y - m.born}")
            if f.born is not None and not 16 <= y - f.born <= 72:
                bad.append(f"{k}: father {y - f.born}")
            if m.died is not None and m.died < y or f.died is not None and f.died < y - 1:
                bad.append(f"{k}: born after a parent died")
        if c.wed is not None and any(q.died is not None and c.wed > q.died for q in (m, f)):
            bad.append(f"{c.id}: wed after a death")
        if c.res != "OFF" and set(b.anc(c.f)) & set(b.anc(c.m)):
            bad.append(f"{c.id}: spouses share an ancestor")
    for i, p in P.items():
        ks = sorted(P[k].born for cid in p.unions if C[cid].m == i for k in C[cid].kids)
        if any(y - x < 1 for x, y in zip(ks, ks[1:])):
            bad.append(f"{i}: births in one year")
        if p.kind == "present" and p.died is not None:
            bad.append(f"{i}: living but dead")
        if p.kind in ("anc", "ghost") and (p.died is None or p.died >= 0):
            bad.append(f"{i}: absent but not dead")
        gh = [C[u] for u in p.unions if C[u].ghost == i]
        li = [C[u] for u in p.unions if C[u].ghost != i]
        if gh and li:
            gk = [P[k].born for k in gh[0].kids]
            lk = [P[k].born for c in li for k in c.kids]
            if gk and lk and max(gk) >= min(lk):
                bad.append(f"{i}: children of the living union before the dead one's")
    return bad


def agg(rows):
    keys = rows[0].keys()
    out = {}
    for k in keys:
        xs = [r[k] for r in rows if r[k] is not None]
        out[k] = round(stt.mean(xs), 3) if xs else None
    return out


def e1_forward(seeds):
    """The forward run's present pinned; its past rebuilt; compared with the truth and with the null arm."""
    T, R, N, M, MN, times, dets, refusals, bj, null_failed, violations = [], [], [], [], [], [], 0, [], [], [], []
    for s in seeds:
        sim = FW.simulate(REGION, s)
        spec = FW.to_input(REGION, sim)
        spec["hard_years"] = sorted(sim["hard"])
        tr = FW.truth(sim)
        try:
            b, a, st = run(spec, 1000 + s)
            b2, a2, _ = run(spec, 1000 + s)
        except (S.Refusal, RuntimeError) as e:
            refusals.append((s, str(e)))
            continue
        dets += digest(a, b) == digest(a2, b2)
        violations += check(b)
        times.append(st["seconds"])
        bj.append(st["backjumps"])
        rc = b.export()
        T.append(ST.summary(tr))
        R.append(ST.summary(rc))
        M.append(ST.match(tr, rc))
        try:
            bn, an, _ = run(spec, 1000 + s, cls=Flat)
        except (S.Refusal, RuntimeError) as e:
            null_failed.append((s, str(e)[:120]))
            continue
        N.append(ST.summary(bn.export()))
        MN.append(ST.match(tr, bn.export()))
    return {"seeds": len(seeds), "solved": len(R), "refusals": refusals, "deterministic": dets, "seconds_mean": round(stt.mean(times), 3),
            "seconds_max": max(times), "backjumps_total": sum(bj), "worlds_with_backjumps": sum(1 for x in bj if x),
            "null_failed": null_failed, "violations": len(violations), "violation_examples": violations[:10], "truth": agg(T), "built": agg(R), "null": agg(N), "match_built": agg(M), "match_null": agg(MN)}


MIXES = {
    "default": {"villages": {v: {**d, "households": n} for (v, d), n in zip(REGION["villages"].items(), (9, 6, 5, 4))},
                "off": REGION["off"], "forms": {"couple_children": 0.7, "couple_old": 0.15, "three_generations": 0.15}},
    "test_conditions": {"villages": {v: {**d, "households": n} for (v, d), n in zip(REGION["villages"].items(), (8, 6, 6, 4))},
                        "off": REGION["off"], "forms": {"widow_alone": 3, "stem": 2, "three_generations": 2, "widower_children": 2,
                                                        "single_man": 2, "siblings": 1, "couple_old": 0.2, "couple_children": 0.8}},
}


def e2_mixes(seeds):
    out = {}
    for name, mix in MIXES.items():
        ok, refused, exact, fl, sec, viol = 0, [], 0, [], [], []
        for s in seeds:
            spec = PR.draw(mix, s)
            want = {f: int(n) for f, n in mix["forms"].items() if n >= 1}
            got = {f: sum(1 for h in spec["households"] if h["form"] == f) for f in want}
            exact += got == want
            try:
                b, a, st = run(spec, s)
            except S.Refusal as e:
                refused.append((s, str(e)))
                continue
            ok += 1
            viol += check(b)
            sec.append(st["seconds"])
            fl += flags(b, st)
        out[name] = {"seeds": len(seeds), "solved": ok, "refusals": refused, "counts_exact": exact, "seconds_mean": round(stt.mean(sec), 3),
                     "flags_per_world": round(len(fl) / max(1, ok), 2), "flag_examples": fl[:8],
                     "violations": len(viol), "violation_examples": viol[:6]}
    return out


def edit(spec, kind):
    sp = copy.deepcopy(spec)
    hh = sp["households"]
    if kind == "baby":                                   # a newborn in the first household with a wife under 40
        for h in hh:
            ws = [m for m in h["members"] if m["sex"] == "f" and 20 <= m["age"] <= 38]
            ms = [m for m in h["members"] if m["sex"] == "m" and m["age"] >= 20]
            if ws and ms and all(m["age"] >= 2 for m in h["members"]):
                h["members"].append({"id": f"{h['id']}.new", "age": 0, "sex": "f"})
                return sp, h["id"]
    if kind == "seven":                                  # the second household made a family of seven
        h = hh[1]
        h["members"] = [{"id": f"{h['id']}.s{k}", "age": a, "sex": x} for k, (a, x) in
                        enumerate([(38, "m"), (35, "f"), (14, "m"), (11, "f"), (8, "m"), (5, "f"), (2, "m")])]
        return sp, h["id"]
    if kind == "drop":                                   # the last household gone
        h = hh.pop()
        return sp, h["id"]
    raise ValueError(kind)


def moved(a0, b0, a1, b1):
    keys = set(a0) & set(a1)
    dec = sum(1 for k in keys if a0[k] != a1[k]) / max(1, len(keys))
    par = lambda b, i: (b.C[b.P[i].pc].f, b.C[b.P[i].pc].m) if b.P[i].pc else None
    pres = [i for i, p in b0.P.items() if p.kind == "present" and i in b1.P]
    pc = sum(1 for i in pres if par(b0, i) != par(b1, i)) / max(1, len(pres))
    return round(dec, 3), round(pc, 3), len(set(a1) - set(a0)), len(set(a0) - set(a1))


def e3_stability(seeds):
    rows = {k: {"soft": [], "fresh": [], "same_seed_fresh": []} for k in ("baby", "seven", "drop")}
    for s in seeds:
        sim = FW.simulate(REGION, s)
        spec = FW.to_input(REGION, sim)
        spec["hard_years"] = sorted(sim["hard"])
        b0, a0, _ = run(spec, 1000 + s)
        for k in rows:
            sp, hid = edit(spec, k)
            try:
                b1, a1, st1 = run(sp, 1000 + s, prev=a0)
                b2, a2, _ = run(sp, 1000 + s)
            except S.Refusal as e:
                rows[k]["soft"].append(("refused", str(e)))
                continue
            rows[k]["soft"].append(moved(a0, b0, a1, b1) + (st1["soft_kept"], st1["soft_moved"]))
            rows[k]["fresh"].append(moved(a0, b0, a2, b2))
    out = {}
    for k, r in rows.items():
        ok = [x for x in r["soft"] if x[0] != "refused"]
        out[k] = {"decisions_changed_soft": round(stt.mean(x[0] for x in ok), 3),
                  "living_with_other_parents_soft": round(stt.mean(x[1] for x in ok), 3),
                  "decisions_changed_fresh": round(stt.mean(x[0] for x in r["fresh"]), 3),
                  "living_with_other_parents_fresh": round(stt.mean(x[1] for x in r["fresh"]), 3),
                  "decisions_new_mean": round(stt.mean(x[2] for x in ok), 1), "decisions_gone_mean": round(stt.mean(x[3] for x in ok), 1),
                  "refused": [x for x in r["soft"] if x[0] == "refused"]}
    return out


def odd_specs():
    V = {v: {"at": d["at"]} for v, d in REGION["villages"].items()}
    base = PR.draw(MIXES["default"], 7)
    cases = {}
    sp = copy.deepcopy(base)                             # nine living children in one house
    sp["households"][0]["members"] = [{"id": "big.0", "age": 46, "sex": "m", "role": "head"}, {"id": "big.1", "age": 44, "sex": "f", "role": "spouse"}] + \
        [{"id": f"big.{k + 2}", "age": a, "sex": "mf"[k % 2]} for k, a in enumerate([24, 22, 20, 18, 16, 13, 11, 8, 5])]
    cases["nine_children"] = sp
    sp = copy.deepcopy(base)                             # a village of widows living alone
    for h in sp["households"]:
        if h["village"] == "Southam":
            h["members"] = [{"id": f"{h['id']}.w", "age": 50 + int(h["id"][2:]) * 7 % 25, "sex": "f", "role": "widowed"}]
    cases["village_of_widows"] = sp
    sp = copy.deepcopy(base)                             # a village founded twenty years ago, its adults older than that
    sp["pins"] = {"found": {"Westcot": -20}}
    cases["young_village"] = sp
    sp = copy.deepcopy(base)                             # founded twelve years ago, with a child of thirteen: refused, by name
    sp["pins"] = {"found": {"Westcot": -12}}
    cases["young_village_older_child"] = sp
    sp = copy.deepcopy(base)                             # twins, with no roles: one must be read another way
    sp["households"][0]["members"] = [{"id": "tw.0", "age": 34, "sex": "m"}, {"id": "tw.1", "age": 31, "sex": "f"},
                                      {"id": "tw.2", "age": 6, "sex": "m"}, {"id": "tw.3", "age": 6, "sex": "f"}]
    cases["twins_unpinned"] = sp
    sp = copy.deepcopy(base)                             # twins pinned as the head's children: the model has no twins, so refused
    sp["households"][0]["members"] = [{"id": "tp.0", "age": 34, "sex": "m", "role": "head"}, {"id": "tp.1", "age": 31, "sex": "f", "role": "spouse"},
                                      {"id": "tp.2", "age": 6, "sex": "m", "role": "child"}, {"id": "tp.3", "age": 6, "sex": "f", "role": "child"}]
    cases["twins_pinned_children"] = sp
    sp = copy.deepcopy(base)                             # impossible: a child of the head who is only ten years younger
    sp["households"][0]["members"] = [{"id": "x.0", "age": 25, "sex": "m", "role": "head"}, {"id": "x.1", "age": 15, "sex": "f", "role": "child"}]
    cases["impossible_child"] = sp
    sp = copy.deepcopy(base)                             # no village is old enough: the span is short and every village pinned young
    sp["pins"] = {"found": {v: -20 for v in V}}
    cases["all_young"] = sp
    return cases


def odd_cases():
    out = {}
    for name, sp in odd_specs().items():
        try:
            b, a, st = run(sp, 7)
        except S.Refusal as e:
            out[name] = {"result": "refused", "pins": e.pins, "message": str(e)}
            continue
        r = {"result": "built", "backjumps": st["backjumps"], "max_jump": st["max_jump"], "flags": flags(b, st)[:6], "violations": check(b)}
        if name.startswith("twins"):
            ids = [m["id"] for m in sp["households"][0]["members"]]
            r["readings"] = {i: (b.P[i].pc, b.C[b.P[i].pc].res if b.P[i].pc else None) for i in ids}
        if name == "young_village":
            ad = [i for i, p in b.P.items() if p.kind == "present" and p.village == "Westcot" and p.age >= 12]
            r["westcot_adults_origin"] = {i: ("came" if b.P[i].came else b.C[b.P[i].pc].res if b.P[i].pc else "before the span") for i in ad}
        out[name] = r
    return out


def sample(seed, outdir):
    sim = FW.simulate(REGION, seed)
    spec = FW.to_input(REGION, sim)
    spec["hard_years"] = sorted(sim["hard"])
    b, a, st = run(spec, 1000 + seed)
    t = time.time()
    w = WR.spec(b)
    wy = WR.spec(b, years=True)
    w["seconds_to_write"] = round(time.time() - t, 2)
    keep = sorted(w["agents"])[:5]                         # the full tree and history, five agents (all of them is 0.7 MB)
    with open(os.path.join(outdir, f"sample_seed{seed}.json"), "w") as f:
        json.dump({**w, "agents": {n: w["agents"][n] for n in keep}}, f, indent=1)
    lines = [f"# A built past (forward seed {seed}, its present pinned)", ""]
    lines.append("Village foundings, built against true: " + ", ".join(f"{v} {b.F[v]} ({sim['founded'].get(v)})" for v in sorted(b.F)))
    lines += ["", "## Foundings, marriages and the last 15 years' deaths, in order (year 0 is now)", ""]
    for h in w["history"]:
        if h["kind"] in ("founding", "marriage", "left") or (h["kind"] == "death" and h["year"] > -15):
            lines.append(f"- {h['year']}: {h['text']}")
    lines += ["", "## Three heads as they will be told it (memories in years here; the spec writes the engine's winters)", ""]
    heads = [n for n, x in wy["agents"].items() if x.get("role") == "head"][:3]
    for n in heads:
        x = wy["agents"][n]
        kin = {m: r for m, r in x["relations"].items() if not r.startswith("of the")}
        lines.append(f"**{n}** ({x['stage']}, {x['household']}): kin living: " + "; ".join(f"{m} ({r[5:]})" for m, r in list(kin.items())[:8]))
        lines += [f"  - {m}" for m in x["memories"]]
    with open(os.path.join(outdir, f"sample_seed{seed}.md"), "w") as f:
        f.write("\n".join(lines) + "\n")
    return {"agents": len(w["agents"]), "tree": len(w["tree"]), "history": len(w["history"]), "seconds_to_write": w["seconds_to_write"]}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=40)
    ap.add_argument("--out", default="proto/peoplegen/results")
    a = ap.parse_args(argv)
    os.makedirs(a.out, exist_ok=True)
    seeds = list(range(1, a.seeds + 1))
    res = {"e1_forward_pinned": e1_forward(seeds), "e2_mixes": e2_mixes(seeds[:20]), "e3_stability": e3_stability(seeds[:15]),
           "e4_odd_pins": odd_cases(), "e5_sample": sample(1, a.out)}
    with open(os.path.join(a.out, "results.json"), "w") as f:
        json.dump(res, f, indent=1, default=str)
    print(json.dumps(res, indent=1, default=str))


if __name__ == "__main__":
    main()
