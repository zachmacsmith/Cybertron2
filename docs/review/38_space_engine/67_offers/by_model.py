"""Review 38.67 §7: are bigger models' offers less variable? Uses rates_rows.csv (rates_between.py): each spot offer as the log price of
a good in a common unit (lprice), with its side (sell/buy). A maker's 'series' is its offers in one market, one side, one run."""
import numpy as np, pandas as pd
from fractions import Fraction
import statsmodels.api as sm

d = pd.read_csv("rates_rows.csv")
d = d[d.model.isin(["haiku", "sonnet", "opus"])].copy()
d["series"] = d.run + "|" + d.market + "|" + d.side + "|" + d.by
d = d.sort_values(["run", "day", "offer"])
x = lambda s: float(np.exp(s))

def simple(r):
    f = Fraction(float(r)).limit_denominator(24); return abs(float(f) - r) < 1e-6 and max(f.numerator, f.denominator) <= 4

print("== 1. Each maker against itself: its offers in one market, one side, one run")
rows = []
for mdl, g in d.groupby("model"):
    s = g[g.groupby("series").lprice.transform("size") >= 2].copy()
    dev = s.lprice - s.groupby("series").lprice.transform("mean")
    step = s.groupby("series").lprice.diff().dropna()
    rows.append({"model": mdl, "offers": len(g), "makers": g.groupby(["run", "by"]).ngroups, "repeat series": s.series.nunique(),
                 "sd within series (x)": round(x(dev.std()), 2), "repost unchanged": round((step.abs() < 1e-9).mean(), 2),
                 "median step when changed (x)": round(x(step[step.abs() > 1e-9].abs().median()), 2),
                 "steps > x2": round((step.abs() > np.log(2) - 1e-9).mean(), 2),
                 "simple ratio": round((np.exp(g.lprice)).map(simple).mean(), 2)})
print(pd.DataFrame(rows).to_string(index=False))

print("\n== 2. Each maker against the others: |log price - mean of the other makers' offers in that run, market and side|")
d["others"] = np.nan
for key, g in d.groupby(["run", "market", "side"]):
    tot, n = g.groupby("by").lprice.agg(["sum", "size"]).sum()
    for by, gb in g.groupby("by"):
        o = g[g.by != by]
        if len(o):
            d.loc[gb.index, "others"] = o.lprice.mean()
c = d.dropna(subset=["others"]).copy()
c["gap"] = (c.lprice - c.others).abs()
print(c.groupby("model").agg(offers=("gap", "size"), median_gap=("gap", lambda s: round(x(s.median()), 2)),
                              gap_over_x2=("gap", lambda s: round((s > np.log(2) - 1e-9).mean(), 2))).to_string())

print("\n== 3. Same run, same market, same side, both models present: pairwise gap of each model's mean from the other makers'")
pairs = []
for key, g in c.groupby(["run", "market", "side"]):
    ms = g.groupby("model").gap.mean()
    if len(ms) >= 2:
        pairs.append(ms)
P = pd.DataFrame(pairs)
for a, b in [("haiku", "opus"), ("sonnet", "opus"), ("haiku", "sonnet")]:
    q = P[[a, b]].dropna()
    if len(q):
        t = (q[a] - q[b]).abs() < 1e-9
        print(f"{a} vs {b}: {len(q)} run-markets; mean gap {a} x{x(q[a].mean()):.2f}, {b} x{x(q[b].mean()):.2f}; {a} further off in"
              f" {((q[a] > q[b]) & ~t).mean():.0%}, closer in {((q[a] < q[b]) & ~t).mean():.0%}, tied (two makers only) {t.mean():.0%}")

print("\n== 4. Noise left after the maker's own state (offers with a market): within-series sd of the residual of")
print("   lprice ~ own stock of the good + household food + place stock of the numeraire, by model (fixed effect per series)")
m = d[d.people_here.notna()].copy()
m["own_good"] = np.where(m.side == "sell", m.give_household, m.get_household) / m.hh_size.clip(lower=1)
m["own_num"] = np.where(m.side == "sell", m.get_household, m.give_household) / m.hh_size.clip(lower=1)
for c_ in ("own_good", "own_num", "hh_food_days"):
    m[c_ + "_l"] = np.log1p(m[c_].clip(lower=0))
X = ["own_good_l", "own_num_l", "hh_food_days_l"]
for mdl, g in m.groupby("model"):
    g = g[g.groupby("series").lprice.transform("size") >= 2]
    z = g[["lprice"] + X] - g.groupby("series")[["lprice"] + X].transform("mean")
    xs = [v for v in X if z[v].std() > 0]
    r = sm.OLS(z.lprice, z[xs]).fit()
    print(f"{mdl}: series {g.series.nunique()}, offers {len(g)}; raw sd x{x(z.lprice.std()):.2f}, residual sd x{x(r.resid.std()):.2f}, share explained {r.rsquared:.2f}")

print("\n== 5. Section 1 with the role held: short series (2-3 offers) only, by side; and the salt and hunger probes' targets (Haiku,")
print("   Sonnet or Opus pairs in the same role) against the fixed Opus holders")
d["n_series"] = d.groupby("series").lprice.transform("size")
s5 = d[d.n_series.between(2, 3)].copy()
s5["dev"] = s5.lprice - s5.groupby("series").lprice.transform("mean")
s5["step"] = s5.groupby("series").lprice.diff()
print(s5.groupby(["side", "model"]).agg(series=("series", "nunique"), sd=("dev", lambda v: round(x(v.std()), 2)),
      unchanged=("step", lambda v: round((v.dropna().abs() < 1e-9).mean(), 2))).to_string())
p = d[d.run.str.match(r"gp[3h]_") & (d.n_series >= 2)].copy()
p["role"] = np.where(p.run.str.extract(r"gp[3h]_\w+?_(\w+?)_")[0] == p.model, "target pair", "holder household")
p["dev"] = p.lprice - p.groupby("series").lprice.transform("mean")
p["step"] = p.groupby("series").lprice.diff()
print(p.groupby(["role", "model"]).agg(series=("series", "nunique"), offers=("dev", "size"), sd=("dev", lambda v: round(x(v.std()), 2)),
      unchanged=("step", lambda v: round((v.dropna().abs() < 1e-9).mean(), 2))).to_string())

print("\n== 6. What a change follows: the step from one offer to the next in a series, signed so that + is better for the taker")
print("   (a seller cuts, a buyer offers more), by whether the earlier offer was taken")
q = d[d.groupby("series").lprice.transform("size") >= 2].copy()
q["prev_taken"] = q.groupby("series").taken.shift().gt(0)
q["step"] = q.groupby("series").lprice.diff()
q = q.dropna(subset=["step"])
q["concede"] = np.where(q.side == "sell", -q.step, q.step)
q["move"] = np.select([q.concede > 1e-9, q.concede < -1e-9], ["concedes", "hardens"], "same")
t = q.groupby(["model", "prev_taken"]).move.value_counts(normalize=True).unstack().fillna(0).round(2)
t["n"] = q.groupby(["model", "prev_taken"]).size()
print(t.to_string())
