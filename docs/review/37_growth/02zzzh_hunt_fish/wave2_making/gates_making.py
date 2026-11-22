"""Read-only probe: for every world spec with people, what the making chains of wave 2 would find within a day of each village."""
import contextlib, copy, io, sys, glob, json, collections
sys.path.insert(0, "/home/user/cybertron2")
from cybertron2.engine.world import World, load_spec
from cybertron2.wild import plants
WET = plants.WET_ECOS
GAME = ("red deer", "roe deer", "wild boar")

def probe(path):
    s = load_spec(path)
    if not s.get("agents"):
        return None
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            w = World(copy.deepcopy(s))
    except Exception as e:
        return {"world": path, "error": repr(e)[:120]}
    S = w.s
    homes = collections.defaultdict(set)
    for bid, b in (s.get("buildings") or {}).items():
        if b.get("household") and b.get("parcel") in S["parcels"]:
            homes[S["parcels"][b["parcel"]]["node"]].add(b["household"])
    if not homes:
        for n, a in (s.get("agents") or {}).items():
            if a.get("household") and S["people"].get(n, {}).get("at"):
                homes[S["people"][n]["at"]].add(a["household"])
    near = collections.defaultdict(set)
    for r in s.get("roads") or []:
        a, b, d = r[0], r[1], r[2]
        if d <= 1:
            near[a].add(b); near[b].add(a)
    land = ((S.get("wild") or {}).get("land") or {})
    areas = land.get("areas") or {}
    pop = ((S.get("wild") or {}).get("state") or {}).get("pop") or {}
    order = list(areas)
    out = []
    fittings_all = collections.Counter()
    for b in S["buildings"].values():
        for f, q in (b.get("fittings") or {}).items():
            fittings_all[f] += 1 if not isinstance(q, (int, float)) else q
    for nid in sorted(homes):
        reach = {nid} | near[nid]
        pars = [p for p in S["parcels"].values() if p["node"] in reach]
        own = [p for p in S["parcels"].values() if p["node"] == nid]
        def has(ps, f):
            return any(f(p) for p in ps)
        wet_own = has(own, lambda p: p["cover"] in ("fen", "water") or p.get("ecosystem") in WET or (p.get("land") or {}).get("river", "none") not in ("none", None))
        waterids = {pid for pid, p in S["parcels"].items() if p["cover"] == "water"}
        bank = has(own, lambda p: p["cover"] in ("meadow", "pasture", "scrub", "forest", "fen") and bool(set(p.get("adj") or []) & waterids))
        willow0 = has(own, lambda p: p["cover"] == "fen" or p.get("ecosystem") in WET - {"hay meadow"} or ((p.get("land") or {}).get("river", "none") not in ("none", None) and p["cover"] != "water"))
        willow = willow0 or bank
        river = has(own, lambda p: p["cover"] == "water")
        still = has(pars, lambda p: p["cover"] == "fen" or p.get("ecosystem") in ("fen", "reedbed", "alder carr"))
        wood_own = has(own, lambda p: p["cover"] in ("forest", "scrub"))
        oak = has(pars, lambda p: p["cover"] == "forest" and "oak" in str(p.get("ecosystem", "")))
        managed = has(pars, lambda p: p["cover"] == "forest" and "managed" in str(p.get("state", {}).get("wood", {}).get("kind", "") or p.get("wood", "")))
        field = has(own, lambda p: p["cover"] == "field")
        rock = has(pars, lambda p: p["cover"] == "rock")
        game = 0.0
        for i, aid in enumerate(order):
            if areas[aid].get("node") in reach:
                for k in GAME:
                    v = pop.get(k)
                    if v and i < len(v):
                        game += float(v[i])
        cows = 0
        for h in (S.get("herds") or {}).values():
            if S["parcels"].get(h.get("parcel") or h.get("at"), {}).get("node") in reach or h.get("node") in reach:
                cows += 1
        anvil = any((b.get("fittings") or {}).get("anvil") for b in S["buildings"].values() if S["parcels"][b["parcel"]]["node"] in reach)
        seeds = collections.Counter()
        for b in (s.get("buildings") or {}).values():
            if S["parcels"].get(b.get("parcel"), {}).get("node") in reach and isinstance(b.get("stock"), dict):
                for k, q in b["stock"].items():
                    seeds[k] += q
        hh = sorted(homes[nid])
        out.append(dict(village=S["nodes"][nid]["name"], households=len(hh), wet=wet_own, willow=willow, river=river, still=still,
                        wood=wood_own, oak=oak, field=field, rock=rock, game=round(game, 1), herds=cows, anvil=anvil,
                        copper=seeds.get("copper", 0), hide=seeds.get("hide", 0), crude=None))
    return {"world": path, "villages": out}

if __name__ == "__main__":
    paths = sorted(glob.glob("/home/user/cybertron2/cybertron2/specs/**/*.yaml", recursive=True))
    res = []
    for p in paths:
        if "goal_probe" in p:      # many copies of one small world; probe one
            if not p.endswith("salt_none.yaml"):
                continue
        try:
            r = probe(p)
        except Exception as e:
            r = {"world": p, "error": repr(e)[:150]}
        if r:
            res.append(r)
    json.dump(res, open(sys.argv[1], "w"), indent=1)
    print(len(res))
