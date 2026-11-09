"""Targeted LLM tests of wave 1 (02zp part six). A model plays one household in a generated village, morning by morning: it is
told what it noticed (signs at its skill level, as prose), what happened in the night, the weather, and its own notes; it chooses
tonight's acts. Its outcomes are scored against scripted households on the same land, weather and draws.

Tests:
  T1 boar   the field by the wood (boar and deer; groups that set out with a lead, a learned field, getting used to scares)
  T2 eels   the weir in autumn (a run on dark nights with rising water after dry weeks; seeded lore that is wrong)
  T3 sowing birds and hares at the seed (birds get used to a scarecrow, hares are scared off by it; seeded lore that is wrong)
Arms: model (Haiku, Sonnet), skill (novice or expert readings), names (named, or masked so prior knowledge of the species helps
less), lore (none, or a wrong saying).

Usage: python3 llm_tests.py [T1 T2 T3] [--dry]   (--dry runs the scripted stand-in instead of a model, to check the harness)
"""
from __future__ import annotations

import concurrent.futures as cf
import json
import os
import sys
import threading
import time

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../..")))
import sim
import baselines as B
import kinds as K
from rules import Y, S, season, sday, in_windows
from village import FOOD_NEED

OUT = os.environ.get("WILD_LLM_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "llm_runs")
MODELS = {"haiku": "claude-haiku-5-5", "sonnet": "claude-sonnet-5-5"}
SEASONS = ["spring", "summer", "autumn", "winter"]
_lock = threading.Lock()


def weather_words(D, d):
    t, lo, r = D.temp[d], D.low[d], D.rain[d]
    w = "a hard frost, the ground like iron" if D.frozen[d] else ("frost at night" if lo < 0 else "")
    warmth = "hot" if t > 20 else ("warm" if t > 15 else ("mild" if t > 8 else ("cold" if t > 2 else "bitter")))
    wet = "heavy rain" if r >= 4 else ("showers" if r >= 1 else "dry")
    return ", ".join(x for x in (warmth, wet, w) if x)


# ------------------------------------------------------------------ the tests
TESTS = {
    "T1": {
        "villages": [("settled lowland and frontier", "s1"), ("settled lowland and frontier", "s3")],
        "eras": ["steady"],
        "windows": [(y * Y + S, y * Y + 2 * S + 2) for y in (0, 1)],          # summer to the harvest, two years
        "kinds": ("wild boar", "red deer"),
        "acts": ("watch", "hunt_boar"),
        "arms": [("novice", "named", None), ("expert", "named", None), ("expert", "masked", None)],
        "role": ("You see to the night watch over the corn field by the wood. The field has three gaps where beasts come in: "
                 "the thorn gap, the ford gap and the lane gap."),
        "aim": ("Bring the corn in with as little lost to beasts as you can, without wearing out your people: every night "
                "spent watching is work lost from the next day."),
        "menu": ["watch a gap by night: 2 units of work for each gap watched, with one scare at each: fire, clapper, horn, or "
                 "the dog (you have one dog, so the dog can be at one gap only)",
                 "hunt the boar in the wood: 6 units, a crew of two; dangerous"],
        "budget": 8,
        "expect": "beasts_in_the_field_tonight",
    },
    "T2": {
        "villages": [("fen with islands", "s1"), ("upland and moor", "s1")],
        "eras": ["steady"],
        "windows": [(y * Y + 2 * S, y * Y + 3 * S + 2) for y in (0, 1, 2)],    # autumn and the first of winter, three years
        "kinds": ("eels",),
        "acts": ("eel_traps", "weir_crew"),
        "arms": [("expert", "named", None), ("expert", "named", "The old people say: the eels run on bright moonlit nights.")],
        "role": "You keep the eel traps at the weir on the river. In autumn the eels run down the river.",
        "aim": "Smoked eels for the winter, for as little work as you can manage.",
        "menu": ["set the eel traps at the weir tonight: 2 units",
                 "put a crew at the weir tonight to empty the traps through the night: 4 more units; when the eels are running, "
                 "a crew takes about twice what the traps alone take; when they are not, the night is wasted"],
        "budget": 8,
        "expect": "a_big_run_of_eels_tonight",
    },
    "T3": {
        "villages": [("plain", "s1"), ("sand country", "s2")],
        "eras": ["steady"],
        "windows": [(y * Y, y * Y + 8) for y in (0, 1)] + [(y * Y + 2 * S + 2, y * Y + 2 * S + 8) for y in (0, 1)],
        "kinds": ("birds at the corn", "hare"),
        "acts": ("scarecrow", "children_scare", "snare"),
        "arms": [("expert", "named", None),
                 ("expert", "named", "The old people say: a good scarecrow keeps every bird and beast off the corn for the whole sowing.")],
        "role": "You see to the sown field while the seed is in the ground and the young corn comes up.",
        "aim": "Lose as little seed and young corn as you can; the children's days are worth something too.",
        "menu": ["keep a scarecrow on the field (almost no work)",
                 "send the children to scare birds and hares off the field all day: 2 of the children's units (they do no other work that day)",
                 "set snares for hares: 1 unit (hares for the pot)"],
        "budget": 8,
        "expect": "damage_to_the_sown_field_tonight_or_today",
    },
}

SKILL = {"novice": "You are new to this place and have not kept land like this before.",
         "expert": "You have kept land here all your life and know its beasts, birds and waters well."}


def schema(T):
    gaps = sim.Village.__init__.__globals__["GAP_NAMES"]
    p = {"reading": {"type": "string", "description": "what you make of this morning's signs, in a sentence or two"},
         T["expect"]: {"type": "number", "minimum": 0, "maximum": 1, "description": "how likely, 0 to 1"},
         "notes": {"type": "string", "description": "what you want to remember for the coming days (short; this is all you will keep beyond the last three days)"}}
    req = ["reading", T["expect"], "notes"]
    if "watch" in T["acts"]:
        p["watch"] = {"type": "array", "items": {"type": "object", "properties": {
            "gap": {"type": "string", "enum": gaps}, "scare": {"type": "string", "enum": ["fire", "clapper", "horn", "dog"]}},
            "required": ["gap", "scare"]}, "description": "the gaps to watch tonight, each with its scare; empty for none"}
        req.append("watch")
    for a in T["acts"]:
        if a != "watch":
            p[a] = {"type": "boolean"}
            req.append(a)
    return {"type": "object", "properties": p, "required": req}


def system_prompt(T, level, named):
    menu = "\n".join("- " + (sim.mask(m) if named == "masked" else m) for m in T["menu"])
    return (f"You are the head of a household in a farming village. {T['role']} {SKILL[level]}\n\n"
            f"Each morning you are told the day, the weather, what you noticed and what happened in the night, and your own notes. "
            f"You decide what your household does tonight.\n\nYour aim: {T['aim']}\n\nWhat you can do:\n{menu}\n"
            f"You can spare up to {T['budget']} units of work a night for this.\n\nAnswer in the JSON asked for.")


def stage(d):
    s, sd = season(d), sday(d)
    return {0: "the spring sowing; the seed in the ground" if sd <= 3 else "the young corn coming up",
            1: "the corn green" if sd <= 2 else "the corn ripening", 2: "harvest" if sd <= 1 else "autumn; the stubbles; the autumn sowing",
            3: "winter"}[s]


class LLMHousehold:
    def __init__(self, T, level, named, lore, model, log, dry=False):
        self.T, self.level, self.named, self.lore, self.model, self.log, self.dry = T, level, named, lore, model, log, dry
        self.notes, self.hist, self.calls = "", [], []
        self.sys = system_prompt(T, level, named)
        self.schema = schema(T)
        self.scripted = B.expert()
        self.window_days = set(d for a, b in T["windows"] for d in range(a, b))

    def __call__(self, v, d, obs):
        if d not in self.window_days:
            return {}
        seen = [x["text"] for x in obs.seen.get(d, []) if x["kind"] in self.T["kinds"] or x["sign"].startswith(("sky.", "watch."))]
        lost = {k: 100 * (1 - v.stocks[k] / v.base[k]) for k in v.base if v.base[k] > 0}
        yr = d // Y
        status = []
        if "watch" in self.T["acts"]:
            status.append(f"The corn lost to beasts so far this year: about {lost['crop']:.0f} in a hundred.")
        if "scarecrow" in self.T["acts"]:
            status.append(f"Seed and young corn lost so far this year: about {(lost['seed_spring'] if season(d) == 0 else lost['seed_autumn']):.0f} in a hundred of this sowing.")
        if "eel_traps" in self.T["acts"]:
            got = v.goods.get((yr, "eels"), 0.0) / 0.22
            status.append(f"Eels taken so far this autumn: about {got:.0f}.")
        recent = "\n".join(f"- {h}" for h in self.hist[-3:]) or "- (nothing yet)"
        lore = f"\nWhat people say here: {self.lore}\n" if self.lore else ""
        user = (f"Year {yr + 1}, {SEASONS[season(d)]}, day {sday(d) + 1} of 8: {stage(d)}.\n"
                f"Weather today: {weather_words(v.drv, d)}.\n\nThis morning you noticed:\n"
                + ("\n".join(f"- {t}" for t in seen) if seen else "- nothing out of the ordinary") + "\n\n"
                + " ".join(status) + "\n" + lore
                + f"\nThe last days (what you noticed; what you did):\n{recent}\n\nYour notes: {self.notes or '(none yet)'}\n\n"
                  "What do you do tonight?")
        if self.dry:
            acts = self.scripted(v, d, obs)
            out = {"reading": "(scripted)", self.T["expect"]: 0.5, "notes": self.notes,
                   **{a: acts.get(a, False) for a in self.T["acts"] if a != "watch"},
                   "watch": [{"gap": v.gap_names[g], "scare": s} for g, s in acts.get("watch", {}).items()]}
            usage = {}
        else:
            from cybertron2.infra import llm
            out, reasoning, usage = llm.call("claude_code", self.model, self.sys, user, self.schema)
        acts = self._acts(v, out)
        self.notes = str(out.get("notes", ""))[:800]
        did = ", ".join(f"{k}: {val}" for k, val in acts.items() if val) or "nothing"
        self.hist.append(f"{SEASONS[season(d)]} day {sday(d) + 1}: noticed " + ("; ".join(seen) if seen else "nothing") + f". Did: {did}.")
        rec = {"day": d, "user": user, "out": out, "acts": {k: (dict(val) if isinstance(val, dict) else val) for k, val in acts.items()},
               "usage": usage or {}}
        self.calls.append(rec)
        with _lock:
            self.log.write(json.dumps(rec, default=str) + "\n"); self.log.flush()
        return acts

    def _acts(self, v, out):
        a, units = {}, 0.0
        if "watch" in self.T["acts"]:
            w, dog = {}, False
            for x in out.get("watch") or []:
                try:
                    g = v.gap_names.index(x["gap"])
                except (ValueError, KeyError, TypeError):
                    continue
                sc = x.get("scare", "fire")
                if sc == "dog":
                    if dog:
                        sc = "fire"
                    dog = True
                if g not in w and units + 2 <= self.T["budget"]:
                    w[g] = sc; units += 2
            if w:
                a["watch"] = w
        for k in self.T["acts"]:
            if k == "watch":
                continue
            if out.get(k):
                cost = K.ACTS[k]["units"] if K.ACTS[k].get("who") != "children" else 0.0
                if units + cost <= self.T["budget"]:
                    a[k] = True; units += cost
        if a.get("weir_crew") and not a.get("eel_traps"):
            a["eel_traps"] = True
        return a


def restrict(pol, T):
    days = set(d for a, b in T["windows"] for d in range(a, b))

    def p(v, d, obs):
        if d not in days:
            return {}
        acts = pol(v, d, obs)
        return {k: val for k, val in acts.items() if k in T["acts"]}
    return p


def score(v, T, start_end=None):
    yrs = sorted({d // Y for a, b in T["windows"] for d in range(a, b)})
    t = sim.totals(v, years=yrs)
    loss = sum(t[k]["loss"] for k in T["kinds"] if k in t)
    yield_ = sum(t[k]["yield"] for k in T["kinds"] if k in t)
    work = sum(r["work"] for k, r in t.items() if k.startswith("act:") or k in T["kinds"])
    child = sum(r["child"] for k, r in t.items() if k.startswith("act:") or k in T["kinds"])
    net = yield_ - loss - 0.5 * work - 0.1 * child
    return {"loss": loss, "yield": yield_, "work": work, "child": child, "net": net, "net_share_of_need": net / (FOOD_NEED * len(yrs))}


def behaviour(name, v, hh, T):
    """Test-specific measures of what the household did."""
    ev, out = v.events, {}
    if name == "T1":
        raids = [d for d in hh.window_days if any(ev.get(d, {}).get(k, {}).get("raid") for k in T["kinds"])]
        watched = [c["day"] for c in hh.calls if c["acts"].get("watch")]
        right_gap = 0; scared = []
        for d in raids:
            for k in T["kinds"]:
                g = v.kinds[k].st
            c = next((c for c in hh.calls if c["day"] == d), None)
            if c and c["acts"].get("watch"):
                hit = any(ev.get(d, {}).get(k, {}).get("scare") is not None for k in T["kinds"])
                right_gap += int(hit)
        seq = [list(c["acts"].get("watch", {}).values()) for c in hh.calls if c["acts"].get("watch")]
        switches = sum(1 for a, b in zip(seq, seq[1:]) if set(a) != set(b))
        exp = [(c["out"].get(T["expect"], 0.5), int(any(ev.get(c["day"], {}).get(k, {}).get("raid") for k in T["kinds"]))) for c in hh.calls]
        out = {"raid_nights": len(raids), "watched_nights": len(watched), "raids_met_at_the_right_gap": right_gap,
               "watch_nights_without_raid": len([d for d in watched if d not in raids]),
               "scare_changes": switches, "scares_used": sorted({s for x in seq for s in x}),
               "brier": float(np.mean([(p - t) ** 2 for p, t in exp])) if exp else None}
    if name == "T2":
        big = [c["day"] for c in hh.calls if ev.get(c["day"], {}).get("eels", {}).get("big")]
        crew = [c["day"] for c in hh.calls if c["acts"].get("weir_crew")]
        exp = [(c["out"].get(T["expect"], 0.5), int(bool(ev.get(c["day"], {}).get("eels", {}).get("big")))) for c in hh.calls]
        dark = [c["day"] for c in hh.calls if v.drv.dark[c["day"]]]
        out = {"big_nights": len(big), "crew_nights": len(crew), "crew_on_big": len(set(big) & set(crew)),
               "crew_on_dark_nights": len(set(crew) & set(dark)), "crew_on_bright_nights": len(set(crew) - set(dark)),
               "brier": float(np.mean([(p - t) ** 2 for p, t in exp])) if exp else None}
        half = len(hh.calls) // 2
        out["crew_bright_first_half"] = len([c for c in hh.calls[:half] if c["acts"].get("weir_crew") and not v.drv.dark[c["day"]]])
        out["crew_bright_second_half"] = len([c for c in hh.calls[half:] if c["acts"].get("weir_crew") and not v.drv.dark[c["day"]]])
    if name == "T3":
        bird_days = [c for c in hh.calls if in_windows(c["day"], [(0, 0, 3), (2, 2, 5)])]
        hare_only = [c for c in hh.calls if not in_windows(c["day"], [(0, 0, 3), (2, 2, 5)])]
        f = lambda cs, a: sum(1 for c in cs if c["acts"].get(a))
        out = {"bird_days": len(bird_days), "children_on_bird_days": f(bird_days, "children_scare"),
               "scarecrow_on_bird_days": f(bird_days, "scarecrow"), "hare_only_days": len(hare_only),
               "children_on_hare_only_days": f(hare_only, "children_scare"), "scarecrow_on_hare_only_days": f(hare_only, "scarecrow"),
               "children_first_year": sum(1 for c in hh.calls if c["day"] < Y and c["acts"].get("children_scare")),
               "children_second_year": sum(1 for c in hh.calls if c["day"] >= Y and c["acts"].get("children_scare"))}
    return out


def run_cell(name, T, r, level, named, lore, mkey, dry):
    os.makedirs(OUT, exist_ok=True)
    tag = f"{name}_{r['world'].split()[0]}_{r['village']}_{level}_{named}_{'lore' if lore else 'nolore'}_{mkey}{'_dry' if dry else ''}"
    with open(os.path.join(OUT, tag + ".jsonl"), "w") as log:
        hh = LLMHousehold(T, level, named, lore, MODELS[mkey], log, dry=dry)
        end = max(b for a, b in T["windows"])
        v, obs = sim.simulate(r, hh, level=level, masked=(named == "masked"), days=end, kinds={k: K.KINDS[k] for k in T["kinds"]})
    res = {"test": name, "tag": tag, "world": r["world"], "village": r["village"], "level": level, "named": named,
           "lore": bool(lore), "model": mkey, "dry": dry, "score": score(v, T), "behaviour": behaviour(name, v, hh, T),
           "cost_usd": sum(float((c["usage"] or {}).get("cost_usd") or (c["usage"] or {}).get("total_cost_usd") or 0) for c in hh.calls), "calls": len(hh.calls)}
    for bname, pol in (("none", B.none), ("calendar", B.calendar), ("scripted expert", B.expert())):
        vb, _ = sim.simulate(r, restrict(pol, T), level="expert", days=end, kinds={k: K.KINDS[k] for k in T["kinds"]})
        res.setdefault("baselines", {})[bname] = score(vb, T)
    return res


def main(names, dry=False, workers=8):
    jobs = []
    for name in names:
        T = TESTS[name]
        rs = [r for r in sim.runs(eras=T["eras"]) if (r["world"], r["village"]) in T["villages"]]
        for r in rs:
            for level, named, lore in T["arms"]:
                for mkey in MODELS:
                    jobs.append((name, T, r, level, named, lore, mkey, dry))
                    if dry:
                        break
    print(f"{len(jobs)} runs", flush=True)
    results = []
    t0 = time.time()
    with cf.ThreadPoolExecutor(workers) as ex:
        futs = {ex.submit(run_cell, *j): j for j in jobs}
        for f in cf.as_completed(futs):
            try:
                res = f.result()
            except Exception as e:
                j = futs[f]
                print("FAILED", j[0], j[2]["village"], j[3:8], repr(e), flush=True)
                continue
            results.append(res)
            print(f"[{time.time() - t0:5.0f}s] {res['tag']}: net {res['score']['net']:+.1f} | none {res['baselines']['none']['net']:+.1f} "
                  f"calendar {res['baselines']['calendar']['net']:+.1f} scripted {res['baselines']['scripted expert']['net']:+.1f} | "
                  f"{json.dumps(res['behaviour'])} | ${res['cost_usd']:.2f}", flush=True)
    fn = os.path.join(OUT, f"results_{'_'.join(names)}{'_dry' if dry else ''}.json")
    json.dump(results, open(fn, "w"), indent=1, default=float)
    return results


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(args or ["T1", "T2", "T3"], dry="--dry" in sys.argv)
