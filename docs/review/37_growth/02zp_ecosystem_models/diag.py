import glob, numpy as np, collections, niche as NI
rows = collections.defaultdict(list)
for fn in sorted(glob.glob("lands/*_1.npz")):
    d = dict(np.load(fn, allow_pickle=True)); c = NI.conditions(d)
    land = ~d["sea"] & (d["eco"] != "water")
    for lab in np.unique(d["eco"][land]):
        m = land & (d["eco"] == lab)
        idx = np.flatnonzero(m.ravel()); idx = idx[:: max(1, idx.size // 3000)]
        rows[lab].append(np.stack([c["F"].ravel()[idx], c["R"].ravel()[idx], c["N"].ravel()[idx], d["h"].ravel()[idx], d["wet"].ravel()[idx]]))
for lab, xs in sorted(rows.items()):
    x = np.concatenate(xs, 1)
    q = lambda a: f"{np.percentile(a,25):4.1f} {np.median(a):4.1f} {np.percentile(a,75):4.1f}"
    print(f"{lab:22s} n={x.shape[1]:6d}  F {q(x[0])} | R {q(x[1])} | N {q(x[2])} | h {np.median(x[3]):4.0f} wet {np.median(x[4]):.2f}")
