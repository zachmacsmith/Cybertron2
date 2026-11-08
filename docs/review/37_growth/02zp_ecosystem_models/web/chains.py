"""Food chains: where the food flows, by chain, in each world (the fitted round-3 web). A plant food belongs to one chain; an animal
eaten belongs to the chain of its own largest food (so a fox eating voles is fed by the grass chain)."""
import json, pickle, numpy as np, web as W, rounds as R
CHAIN = {"grass": "grass", "sward": "grass", "seeds": "grass", "crops": "people", "livestock": "people", "stores": "people",
         "browse": "wood", "mast": "wood", "nuts": "wood", "fruit": "wood", "conifer seed": "wood", "heather": "heather",
         "aquatic": "wetland", "fish": "wetland", "seafish": "sea", "shore": "sea", "inverts": "soil", "roots": "soil", "carrion": "carrion"}

def chain_of(kinds, n, seen=()):
    d = kinds[n]["diet"]
    top = max(d.items(), key=lambda x: x[1])[0]
    if top in CHAIN: return CHAIN[top]
    if top in kinds and top not in seen: return chain_of(kinds, top, seen + (n,))
    return "other"

if __name__ == "__main__":
    k = pickle.load(open("kinds_r3.pkl", "rb"))
    worlds = ["plain_1", "upland_and_moor_1", "fen_with_islands_1", "sand_country_1", "scarp_and_vale_1", "settled_lowland_and_frontier_1",
              "w:flat_marsh", "w:alpine", "w:ancient_wildwood", "w:drowned_isles", "w:dry_chalk_plateau", "w:stripped_land", "w:cold_north_moor"]
    out = {}
    for w in worlds:
        fr = R.feat(w)
        o, rec = W.run(fr["f"], fr["r"], k, years=40, knobs={"selfcap": 2.5, "flux": True})
        tot = {}; pred = {}
        for (n, key), v in rec["flux"].items():
            item = key[5:] if key.startswith("kind:") else key
            ch = CHAIN.get(item) if item in CHAIN else chain_of(k, item)
            tot[ch] = tot.get(ch, 0.0) + v
            if key.startswith("kind:"):
                pred.setdefault(n, {}); pred[n][ch] = pred[n].get(ch, 0.0) + v
        s = sum(tot.values())
        out[w] = {"chains": {c: v / s for c, v in sorted(tot.items(), key=lambda x: -x[1])},
                  "predators": {n: {c: v / sum(d.values()) for c, v in d.items()} for n, d in pred.items()}}
        print(f"{w:32s} " + ", ".join(f"{c} {v:.0%}" for c, v in out[w]["chains"].items() if v >= 0.02))
    json.dump(out, open("chains.json", "w"))
    print("\npredators' food by chain (plain_1 / settled frontier / alpine):")
    for n in ["fox", "wolf", "lynx", "golden eagle", "sea eagle", "otter", "stoat and polecat", "owls", "raven"]:
        row = []
        for w in ["plain_1", "settled_lowland_and_frontier_1", "w:alpine"]:
            p = out[w]["predators"].get(n, {})
            row.append(", ".join(f"{c} {v:.0%}" for c, v in sorted(p.items(), key=lambda x: -x[1])[:3]))
        print(f"  {n:18s} | " + " | ".join(row))
