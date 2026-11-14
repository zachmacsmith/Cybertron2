"""Statistics of a past, read the same way from the forward run's truth and from the backward build (both in the common form:
{"P": {id: {sex, born, died, left, father, mother, present, village, hh, born_in, kind}}, "unions": [...], "founded", "span"})."""
from __future__ import annotations

import statistics as st


def mean(xs):
    return round(st.mean(xs), 2) if xs else None


def window(g):
    return -g["span"] + 30                                        # births from here on are fully in both pasts


def summary(g) -> dict:
    P = g["P"]
    w0 = window(g)
    births = [p for p in P.values() if p["born"] is not None and p["born"] >= w0 and p["mother"]]
    ma = [p["born"] - P[p["mother"]]["born"] for p in births if P[p["mother"]]["born"] is not None]
    by_m = {}
    for p in births:
        by_m.setdefault(p["mother"], []).append(p["born"])
    gaps = [b - a for bs in by_m.values() for a, b in zip(sorted(bs), sorted(bs)[1:])]
    done = []                                                     # completed families: mother born in the window, past 45 or dead
    for m, bs in by_m.items():
        pm = P[m]
        if pm["born"] is None or pm["born"] < w0 - 20:
            continue
        if pm["born"] <= -46 or (pm["died"] is not None and pm["died"] < 0):
            done.append(sum(1 for p in P.values() if p["mother"] == m))
    early = [p for p in P.values() if p["born"] is not None and w0 <= p["born"] <= -16]
    child_dead = [p for p in early if p["died"] is not None and p["died"] - p["born"] < 15]
    adult_deaths = [p["died"] - p["born"] for p in P.values() if p["died"] is not None and p["died"] >= w0 and p["died"] - p["born"] >= 15]
    pres = {i: p for i, p in P.items() if p["present"]}
    adults = [i for i, p in pres.items() if -p["born"] >= 16]
    alive_par = [i for i in adults if any(P[i][k] and P[P[i][k]]["present"] for k in ("father", "mother"))]
    wives = [i for i in adults if P[i]["sex"] == "f" and any(u["m"] == i and u["f"] in pres for u in g["unions"])]
    wives_out = [i for i in wives if P[i]["born_in"] not in (P[i]["village"], None)]
    wives_off = [i for i in wives if P[i]["born_in"] == "OFF"]

    def sibs(i):
        p = P[i]
        return {j for j, q in pres.items() if j != i and ((p["mother"] and q["mother"] == p["mother"]) or (p["father"] and q["father"] == p["father"]))}

    def cousins(i):
        par = [P[i][k] for k in ("father", "mother") if P[i][k]]
        gp = {P[x][k] for x in par for k in ("father", "mother") if P[x][k]}
        return {j for j, q in pres.items() if j != i and j not in sibs(i)
                and gp & {P[x][k] for x in (q["father"], q["mother"]) if x for k in ("father", "mother") if P[x][k]}}

    sib_other_v = [i for i in adults if any(pres[j]["village"] != pres[i]["village"] for j in sibs(i))]
    sib_other_h = [i for i in adults if any(pres[j]["village"] == pres[i]["village"] and pres[j]["hh"] != pres[i]["hh"] for j in sibs(i))]
    kin_other_v = [i for i in adults if any(pres[j]["village"] != pres[i]["village"] for j in sibs(i) | cousins(i))]
    par_couples = {(P[i]["father"], P[i]["mother"]) for i in pres if P[i]["mother"]}
    gpar = {(P[x]["father"], P[x]["mother"]) for c in par_couples for x in c if x and P[x]["mother"]}
    n = lambda xs: len(xs) / max(1, len(adults))
    return {
        "mother_age_mean": mean(ma), "mother_age_sd": round(st.pstdev(ma), 2) if ma else None,
        "first_birth_age": mean([min(bs) - P[m]["born"] for m, bs in by_m.items() if P[m]["born"] is not None]),
        "birth_gap_median": st.median(gaps) if gaps else None,
        "completed_family": mean(done), "families_9plus": sum(1 for d in done if d >= 9),
        "died_under_15": round(len(child_dead) / max(1, len(early)), 3),
        "adult_age_at_death": mean(adult_deaths),
        "adults_with_living_parent": round(n(alive_par), 3),
        "wives_from_other_village": round(len(wives_out) / max(1, len(wives)), 3),
        "wives_from_off_map": round(len(wives_off) / max(1, len(wives)), 3),
        "adults_sibling_other_household": round(n(sib_other_h), 3),
        "adults_sibling_other_village": round(n(sib_other_v), 3),
        "adults_sib_or_cousin_other_village": round(n(kin_other_v), 3),
        "parent_couples_per_present": round(len(par_couples) / max(1, len(pres)), 3),
        "grandparent_couples_per_present": round(len(gpar) / max(1, len(pres)), 3),
        "persons_in_past": len(P),
    }


def match(truth, rec) -> dict:
    """How often the build gave a living person the same living parents as the truth (where the truth has a living parent), and
    how often it said 'no living parent' where the truth agrees."""
    T, R = truth["P"], rec["P"]
    same = tot = none_ok = none_tot = 0
    for i, p in T.items():
        if not p["present"] or i not in R:
            continue
        tl = {p[k] for k in ("father", "mother") if p[k] and T[p[k]]["present"]}
        rl = {R[i][k] for k in ("father", "mother") if R[i][k] and R[R[i][k]]["present"]}
        if tl:
            tot += 1
            same += tl == rl
        else:
            none_tot += 1
            none_ok += not rl
    return {"living_parents_same": round(same / max(1, tot), 3), "no_living_parent_same": round(none_ok / max(1, none_tot), 3)}
