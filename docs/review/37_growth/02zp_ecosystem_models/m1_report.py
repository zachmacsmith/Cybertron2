"""M1 report: agreement by label over all seeds, the within-label variety, and the near-ties (mixes)."""
import glob, json, collections, numpy as np, niche as NI, test_niche as T
res = {"files": [], "conf_settled": collections.Counter(), "conf_natural": collections.Counter(), "variety": collections.defaultdict(collections.Counter),
       "tie": collections.Counter(), "n": collections.Counter()}
for fn in sorted(glob.glob("lands/*.npz")):
    d, land, lab0, lab1, a0, a1, v0, v1, cond = T.run(fn)
    res["files"].append((fn.split("/")[1][:-4], round(float(a0), 3), round(float(a1), 3)))
    fi, fs = v1["field"]
    top = np.sort(fs, 0)[-2:]                     # the two largest shares in the field layer
    tie = (top[0] > 0.7 * top[1]).reshape(d["h"].shape)
    dom = fi[fs.argmax(0)].reshape(d["h"].shape)
    for lab in np.unique(d["eco"][land]):
        m = land & (d["eco"] == lab)
        res["n"][lab] += int(m.sum()); res["tie"][lab] += int((m & tie).sum())
        u, c = np.unique(dom[m], return_counts=True)
        for a, b in zip(u, c): res["variety"][lab][NI.NAMES[a]] += int(b)
    for x, y in zip(d["eco"][land].ravel()[::7], lab1[land].ravel()[::7]): res["conf_settled"][(x, y)] += 1
    for x, y in zip(d["eco0"][land].ravel()[::7], lab0[land].ravel()[::7]): res["conf_natural"][(x, y)] += 1
acc = lambda conf: sum(n for (x, y), n in conf.items() if x == y) / sum(conf.values())
print("files", len(res["files"]), "agreement natural %.3f settled %.3f" % (acc(res["conf_natural"]), acc(res["conf_settled"])))
by = collections.defaultdict(lambda: [0, 0])
for (x, y), n in res["conf_settled"].items():
    by[x][1] += n; by[x][0] += n if x == y else 0
for lab, (a, n) in sorted(by.items(), key=lambda kv: -kv[1][1]):
    v = res["variety"][lab]; tot = sum(v.values())
    print(f"{lab:22s} agree {a/n:4.0%}  mixes {res['tie'][lab]/max(res['n'][lab],1):4.0%}  field layer: " +
          ", ".join(f"{k} {c/tot:.0%}" for k, c in v.most_common(5)))
json.dump({"files": res["files"], "settled": {f"{x}|{y}": n for (x, y), n in res["conf_settled"].items()},
           "natural": {f"{x}|{y}": n for (x, y), n in res["conf_natural"].items()},
           "variety": {k: dict(v) for k, v in res["variety"].items()}, "tie": dict(res["tie"]), "n": dict(res["n"])},
          open("m1_results.json", "w"))
