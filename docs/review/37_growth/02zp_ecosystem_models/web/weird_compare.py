import glob, json, numpy as np, test_niche as T, niche as NI
def shannon(lbls):
    u, c = np.unique(lbls, return_counts=True); p = c / c.sum(); return float(-(p * np.log(p)).sum()), len(u)
rows = {}
files = sorted(glob.glob("weird/*.npz")) + ["lands/plain_1.npz", "lands/upland_and_moor_1.npz", "lands/fen_with_islands_1.npz"]
for fn in files:
    d, land, lab0, lab1, a0, a1, v0, v1, cond = T.run(fn)
    gen = d["eco"][land]; nic = lab1[land]
    hg, ng = shannon(gen); hn, nn = shannon(nic)
    fi, fs = v1["field"]; dom = fi[fs.argmax(0)].reshape(d["h"].shape)[land]
    u, c = np.unique(dom, return_counts=True); fk = sorted(zip([NI.NAMES[i] for i in u], c / c.sum()), key=lambda x: -x[1])
    name = fn.split("/")[1][:-4]
    rows[name] = {"gen_H": hg, "gen_n": ng, "niche_H": hn, "niche_n": nn, "agree": float(a1),
                  "F": float(np.median(cond["F"][land])), "R": float(np.median(cond["R"][land])), "N": float(np.median(cond["N"][land])),
                  "T": float(v1["T"].reshape(d["h"].shape)[land].mean()),
                  "niche_top": [(k, round(float(x), 2)) for k, x in sorted(zip(*np.unique(nic, return_counts=True)), key=lambda x: -x[1])[:5]],
                  "field_top": [(k, round(float(x), 2)) for k, x in fk[:5]]}
    r = rows[name]
    print(f"{name:24s} gen H {hg:.2f} ({ng:2d})  niche H {hn:.2f} ({nn:2d})  F {r['F']:.1f} R {r['R']:.1f} N {r['N']:.1f} | field: " +
          ", ".join(f"{k} {x:.0%}" for k, x in fk[:4]))
json.dump(rows, open("weird_compare.json", "w"), default=str)
