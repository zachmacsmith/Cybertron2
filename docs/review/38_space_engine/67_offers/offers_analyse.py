"""Review 38.67: what moves the terms of an offer. Reads offers.csv (offers_extract.py); prints the tables quoted in 67_offers.md.
price p = qty asked / qty given, for single-item offers; rel = log p less the mean log p of the same pair (item given -> item asked)
in the same run ("the going rate there"). Within-maker: less the same maker's mean for that pair in that run."""
import sys, numpy as np, pandas as pd
import statsmodels.api as sm
sys.path.insert(0, "/home/user/cybertron2")
from cybertron2.engine.data import ITEMS
FOOD = {k for k, v in ITEMS.items() if float(v.get("food", 0) or 0) > 0}

d = pd.read_csv("offers.csv")
d = d[d.model != "bot"].copy()
one = d[(d.n_give == 1) & (d.n_get == 1) & (d.give_qty > 0) & (d.get_qty > 0)].copy()
one["pair"] = one.give_item + " -> " + one.get_item
one["lp"] = np.log(one.get_qty / one.give_qty)
one["acc"] = (one.taken > 0).astype(int)
spot = one[(one.give_later != 1) & (one.get_later != 1) & (one.give_item != one.get_item)].copy()

print("== 1. Sizes"); print(f"offers {len(d)}  runs {d.run.nunique()}  single-item {len(one)}  spot swaps {len(spot)}  with market {spot.people_here.notna().sum()}")
print("taken at least once:", round(d.taken.gt(0).mean(), 3))

print("\n== 2. Round numbers")
from fractions import Fraction
def simple(r, n=4):
    f = Fraction(float(r)).limit_denominator(24); return abs(float(f) - r) < 1e-6 and max(f.numerator, f.denominator) <= n
q = pd.concat([one.give_qty, one.get_qty])
print("quantities whole:", round((q % 1 == 0).mean(), 3), " ratio with both terms <= 4:", round((one.get_qty / one.give_qty).map(simple).mean(), 3))
print(one.assign(r=(one.get_qty / one.give_qty).round(3)).r.value_counts().head(8).to_string())

print("\n== 3. How consistent is a pair's price? (spread of log p, as a factor: exp(sd))")
rows = []
for pr, g in spot.groupby("pair"):
    if len(g) < 15: continue
    wr = g.groupby("run").lp.transform(lambda x: x - x.mean())
    wm = g.groupby(["run", "by"]).lp.transform(lambda x: x - x.mean())
    rows.append({"pair": pr, "n": len(g), "runs": g.run.nunique(), "median p": round(np.exp(g.lp.median()), 2),
                 "all runs x": round(np.exp(g.lp.std()), 2), "within run x": round(np.exp(wr.std()), 2),
                 "within maker x": round(np.exp(wm.std()), 2), "taken": round(g.acc.mean(), 2)})
print(pd.DataFrame(rows).sort_values("n", ascending=False).to_string(index=False))

# relative price against the run's going rate for the pair
m = spot[spot.people_here.notna()].copy()
m["grp"] = m.run + "|" + m.pair
m = m[m.groupby("grp").lp.transform("size") >= 2]
m["rel"] = m.lp - m.groupby("grp").lp.transform("mean")
m["own_give"] = np.log1p(m.give_household / m.hh_size.clip(lower=1))
m["own_get"] = np.log1p(m.get_household / m.hh_size.clip(lower=1))
m["place_give"] = np.log1p(m.give_place_per_head)
m["place_get"] = np.log1p(m.get_place_per_head)
m["food_days"] = np.log1p(m.hh_food_days.clip(lower=0))
m["hungry"] = (m.maker_hunger < 0).astype(int)
m["ment_give"] = np.log1p(m.give_mentions); m["ment_get"] = np.log1p(m.get_mentions)
for c in ("rival_sellers", "demand_for_give", "supply_of_get", "rival_buyers"):
    m[c + "_l"] = np.log1p(m[c])
m["day_z"] = m.day

def fe(df, y, xs, grp, label):
    z = df[[y] + xs].astype(float)
    z = z - df.groupby(grp)[[y] + xs].transform("mean").astype(float)
    keep = z[xs].std() > 0
    xs = [x for x in xs if keep[x]]
    r = sm.OLS(z[y], z[xs]).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(df.run + df.by)[0]})
    out = pd.DataFrame({"coef": r.params.round(3), "se": r.bse.round(3), "p": r.pvalues.round(3)})
    print(f"\n-- {label}: n={len(df)}, groups={df[grp].nunique()}, makers={df.groupby(['run','by']).ngroups}"); print(out.to_string())

X = ["own_give", "own_get", "place_give", "place_get", "food_days", "hungry", "rival_sellers_l", "demand_for_give_l", "supply_of_get_l",
     "rival_buyers_l", "ment_give", "ment_get", "day_z"]
print("\n== 4. What moves the price: log(asked/given), fixed effect for run x pair (across makers and days); se clustered by maker")
print("Signs a trader who prices by need would show: own_give -, own_get +, place_give -, demand_for_give +, rival_sellers -,")
print("supply_of_get +, rival_buyers -.")
fe(m, "lp", X, "grp", "all spot swaps")
m["mgrp"] = m.grp + "|" + m.by
mm = m[m.groupby("mgrp").lp.transform("size") >= 2]
fe(mm, "lp", X, "mgrp", "within one maker's own offers of the pair (the same person, as conditions change)")

print("\n== 5. Food: offers asking for food, by the maker's state")
m["asks_food"] = m.get_item.isin(FOOD); m["gives_food"] = m.give_item.isin(FOOD)
af = m[m.asks_food & ~m.gives_food]
af = af.assign(state=np.select([af.maker_hunger <= -2, af.maker_hunger == -1, af.hh_food_days < 2], ["starving", "hungry", "fed, <2 days food"], "fed, food in store"))
print(af.groupby("state").agg(n=("rel", "size"), rel_mean=("rel", "mean"), pays_more_share=("rel", lambda x: (x < -0.05).mean()), taken=("acc", "mean")).round(2).to_string())
gf = m[m.gives_food & ~m.asks_food]
gf = gf.assign(state=np.select([gf.maker_hunger < 0, gf.hh_food_days < 2], ["hungry", "fed, <2 days food"], "fed, food in store"))
print("\noffers giving food, by the maker's state (rel > 0 asks more than the going rate)")
print(gf.groupby("state").agg(n=("rel", "size"), rel_mean=("rel", "mean"), taken=("acc", "mean")).round(2).to_string())
print("\nwhat the hungry offer: share of offers by kind")
allm = d[d.people_here.notna()].copy()
allm["state"] = np.where(allm.maker_hunger < 0, "hungry", "fed")
allm["kind"] = np.select([allm.give_item.isin(FOOD) & ~allm.get_item.isin(FOOD), allm.get_item.isin(FOOD) & ~allm.give_item.isin(FOOD),
                          allm.give_item.isin(FOOD) & allm.get_item.isin(FOOD)], ["sells food", "buys food", "food for food"], "no food")
allm.loc[allm.give_item == "work (days)", "kind"] = allm.loc[allm.give_item == "work (days)", "kind"].replace({"buys food": "works for food", "no food": "works for other"})
print(pd.crosstab(allm.kind, allm.state, normalize="columns").round(2).to_string())
print(pd.crosstab(allm.kind, allm.state).to_string())

print("\n== 6. Acceptance against price (rel: how the asking compares with the run's going rate for the pair)")
m["band"] = pd.cut(m.rel, [-9, -0.2, -0.02, 0.02, 0.2, 9], labels=["much cheaper", "cheaper", "at the rate", "dearer", "much dearer"])
print(m.groupby("band", observed=True).agg(n=("acc", "size"), taken=("acc", "mean")).round(2).to_string())
lo = sm.Logit(m.acc, sm.add_constant(m[["rel"]])).fit(disp=0, cov_type="cluster", cov_kwds={"groups": pd.factorize(m.run)[0]})
print("logit taken ~ rel:", lo.params.round(2).to_dict(), "p", lo.pvalues.round(3).to_dict())

print("\n== 7. Credit: the same good later for some now (implied interest)")
cr = one[(one.give_item == one.get_item) & (one.give_later == 1)]
print(f"{len(cr)} offers; repay/borrow median {np.exp(cr.lp.median())**-1:.2f}, range {(cr.give_qty/cr.get_qty).min():.2f}-{(cr.give_qty/cr.get_qty).max():.2f}; taken {cr.acc.mean():.2f}")
print(cr.assign(rate=(cr.give_qty / cr.get_qty).round(2))[["run", "by", "model", "day", "give_item", "give_qty", "get_qty", "rate", "taken"]].to_string(index=False))

print("\n== 8. By model: spread within maker, and the price's response to own holdings (pooled fixed effect)")
for mdl, g in m.groupby("model"):
    if len(g) < 40: continue
    gg = g[g.groupby("mgrp").lp.transform("size") >= 2]
    wm = (gg.lp - gg.groupby("mgrp").lp.transform("mean"))
    print(f"{mdl}: offers {len(g)}, repeat-pair makers {gg.mgrp.nunique()}, within-maker spread x{np.exp(wm.std()):.2f}, share unchanged on repost {(wm.abs() < 1e-9).mean():.2f}")
    fe(g, "lp", ["own_give", "own_get", "food_days", "rival_sellers_l", "rival_buyers_l"], "grp", f"{mdl} only")

print("\n== 9. Robustness of section 4 (all spot swaps, run x pair fixed effect)")
print("share of the sample from the salt probes (gp3/gph):", round(m.run.str.match(r"gp[3h]_").mean(), 2), " by the Fowler head Robert:", round((m.by == "Robert").mean(), 2))
m["size_l"] = np.log(m.give_qty)
fe(m, "lp", X + ["size_l"], "grp", "with the offer's size (log qty given) as a control")
o = m[~m.run.str.match(r"gp[3h]?_")]
fe(o, "lp", X, "grp", "without the goal and hunger probes")
