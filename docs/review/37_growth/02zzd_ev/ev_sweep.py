"""The sweep (02zzd): each world x season x settlement x method x range x hunter. Writes one JSON row a cell.
    CYB_ROOT=<checkout> python3 ev_sweep.py OUT.jsonl [--armed] [--worlds 7:settled lowland and frontier,11:upland and moor]"""
import sys, json, time, statistics as st
import ev_harness as E

HUNTERS = {"novice": ("lo", 0.0), "skilled": ("hi", 0.8)}
WORLDS = [(7, "settled lowland and frontier"), (11, "upland and moor"), (5, "settled lowland and frontier"), (3, "sand country")]
SEASONS = ["spring", "summer", "autumn", "winter"]


def plan(w, armed):
    for node in sorted({p["node"] for p in w.s["parcels"].values()}):
        adults = [n for n, p in w.s["people"].items() if p.get("at") == node and p.get("stage") == "adult" and p.get("alive", True)]
        if not adults:
            continue
        par = {c: next((p["name"] for p in w.s["parcels"].values() if p["node"] == node and p["cover"] == c), None)
               for c in ("forest", "pasture", "meadow", "water", "heath")}
        acts = []
        if par["forest"]:
            for r in ("near", "the wood around", "far"):
                acts.append(("hunt the wild", r, {"do": "gather", "what": "hunt the wild", "at": par["forest"], "range": r}, False))
                acts.append(("stalk", r, {"do": "gather", "what": "stalk", "at": par["forest"], "range": r, "looking for": "deer"}, False))
            if not armed:
                acts.append(("gather wild food", "forest", {"do": "gather", "what": "gather wild food", "at": par["forest"]}, False))
        op = par["pasture"] or par["meadow"] or par["heath"]
        if op and not armed:
            acts.append(("snare", "open", {"do": "gather", "what": "snare", "at": op}, True))
            acts.append(("gather wild food", "open", {"do": "gather", "what": "gather wild food", "at": op}, False))
        if par["water"] and not armed:
            acts.append(("trap in water", "water", {"do": "gather", "what": "trap in water", "at": par["water"]}, True))
        yield node, adults[0], acts


def main():
    out = sys.argv[1]; armed = "--armed" in sys.argv
    worlds = WORLDS
    if "--worlds" in sys.argv:
        worlds = [(int(x.split(":")[0]), x.split(":", 1)[1]) for x in sys.argv[sys.argv.index("--worlds") + 1].split(",")]
    f = open(out, "a")
    for seed, cfg in worlds:
        for season in SEASONS:
            t0 = time.time()
            wd = E.gen(seed, cfg, season)
            if not wd.get("agents"):
                print(seed, cfg, "refused people by the generator's checks; skipped", flush=True)
                break
            w0 = E.World(wd)
            for node, who, acts in plan(w0, armed):
                for method, where, act, setwork in acts:
                    for hk, (end, fam) in HUNTERS.items():
                        lo, hi = E.KN.curve(method)
                        res = [E.attempt(w0, who, act, method, hi if end == "hi" else lo, fam, i, setwork, armed)
                               for i in range(20 if setwork else 60)]
                        ok = [r for r in res if r is not None]
                        f.write(json.dumps({"seed": seed, "cfg": cfg, "season": season, "node": node, "method": method, "where": where,
                                            "hunter": hk, "armed": armed, "tries": len(ok), "refused": len(res) - len(ok),
                                            "success": round(sum(r > 1e-9 for r in ok) / len(ok), 3) if ok else None,
                                            "food": round(st.mean(ok), 3) if ok else None, "units": E.units(method, where)}) + "\n")
                        f.flush()
            print(seed, cfg, season, round(time.time() - t0), "s", flush=True)


if __name__ == "__main__":
    main()
