"""Review 38.67 §6: going rates within and between worlds. Each spot single-item offer is turned into the price of one good in another
(a canonical direction for the pair: 'grain per salt' whether salt is sold or bought), with the side recorded. Levels:
  family: the world a run was made from (gp3_salt, gph_salt, e2, wenbridge, ...);
  cell:   the exact spec (family + target model + wording, or the arm);
  run:    one run (gph's cells have replicates r1-r3 with seeds +100);
  offer.
Prints the spread at each level and the patterns between worlds."""
import re, numpy as np, pandas as pd

d = pd.read_csv("offers.csv")
d = d[(d.model != "bot") & (d.n_give == 1) & (d.n_get == 1) & (d.give_qty > 0) & (d.get_qty > 0) & (d.give_later != 1) & (d.get_later != 1)
      & (d.give_item != d.get_item)].copy()

def family(r):
    for pat, f in [(r"^gph_salt", "hunger salt (38.66)"), (r"^gp3_(\w+?)_", r"round 3 \1 (38.65)"), (r"^gp_(food2|food|salt|copper|timber)_", r"round 1-2 \1 (38.53)"),
                   (r"^e1_fish", "e1 fish"), (r"^e2a?_", "e2 labour"), (r"^wb\d", "wenbridge"), (r"^p\d_brookend", "brookend"),
                   (r"^c\d_barleyfield|^a2_barleyfield", "barleyfield"), (r"^[bc]\d_valleys|^s1_valleys", "valleys")]:
        m = re.match(pat, r)
        if m:
            return m.expand(f) if "\\" in f else f
    return r

def cell(r):
    return re.sub(r"_r\d$", "", r)

d["family"], d["cell"] = d.run.map(family), d.run.map(cell)
NUM = ["grain", "coin", "work (days)"]                      # the numeraire, first match: prices are in grain, else coin, else work
def canon(row):
    a, b = row.give_item, row.get_item
    num = next((n for n in NUM if n in (a, b)), min(a, b))
    good = b if a == num else a
    if a == good:   # selling the good for the numeraire
        return pd.Series({"good": good, "num": num, "side": "sell", "lprice": np.log(row.get_qty / row.give_qty)})
    return pd.Series({"good": good, "num": num, "side": "buy", "lprice": np.log(row.give_qty / row.get_qty)})
d = pd.concat([d, d.apply(canon, axis=1)], axis=1)
d["market"] = d.good + " in " + d.num
d.to_csv("rates_rows.csv", index=False)

print("== Spread of log price at each level, by market (sd as a factor). Side (selling or buying the good) removed within each run.")
out = []
for mk, g in d.groupby("market"):
    if len(g) < 30 or g.run.nunique() < 6:
        continue
    g = g.copy()
    side = g.groupby(["run", "side"]).lprice.transform("mean") - g.groupby("run").lprice.transform("mean")
    g["lp"] = g.lprice - side                                  # a run's two sides pulled together
    within_run = g.lp - g.groupby("run").lp.transform("mean")
    runs = g.groupby(["family", "cell", "run"]).lp.mean().reset_index()
    fam = runs.groupby("family").lp.transform("mean")
    rep = runs[runs.groupby("cell").lp.transform("size") >= 2]
    within_cell = rep.lp - rep.groupby("cell").lp.transform("mean")
    multi = runs[runs.groupby("family").lp.transform("size") >= 2]
    within_fam = multi.lp - multi.groupby("family").lp.transform("mean")
    fams = runs.groupby("family").lp.mean()
    x = lambda s: round(float(np.exp(s.std(ddof=1))), 2) if len(s) > 1 else ""
    out.append({"market": mk, "offers": len(g), "runs": len(runs), "families": len(fams), "median": round(float(np.exp(g.lprice.median())), 2),
                "within run": x(within_run), "replicates of one spec": f"{x(within_cell)} ({rep.cell.nunique()} specs)" if len(rep) else "",
                "between runs in a world": x(within_fam), "between worlds (world means)": x(fams)})
print(pd.DataFrame(out).sort_values("offers", ascending=False).to_string(index=False))

print("\n== Run going rates per world, for the main markets (geometric means; sell and buy sides separately)")
for mk in ["salt in grain", "timber in grain", "work (days) in grain", "coin in grain".replace("coin in grain", "grain in coin"), "copper in grain", "firewood in grain"]:
    g = d[d.market == mk]
    if g.empty:
        continue
    t = g.groupby(["family", "side"]).agg(runs=("run", "nunique"), n=("lprice", "size"), price=("lprice", lambda s: np.exp(s.mean()))).round(2).unstack("side")
    print(f"\n-- {mk} (units of {g.num.iloc[0]} for one {g.good.iloc[0]})"); print(t.to_string())

print("\n== Anchoring: the run's first offer in a market against the mean of its later offers (runs with >= 4 offers there)")
rows = []
for (run, mk), g in d.sort_values(["day", "offer"]).groupby(["run", "market"]):
    if len(g) < 4: continue
    rows.append({"market": mk, "family": g.family.iloc[0], "first": g.lprice.iloc[0], "rest": g.lprice.iloc[1:].mean(), "last": g.lprice.iloc[-1],
                 "same_maker": g.by.iloc[0] == g.by.iloc[-1]})
a = pd.DataFrame(rows)
fe = a.copy()
for c in ("first", "rest", "last"):
    fe[c] = a[c] - a.groupby("market")[c].transform("mean")
print(f"run-markets {len(a)}; corr(first, rest) {fe['first'].corr(fe['rest']):.2f}; corr(first, last) {fe['first'].corr(fe['last']):.2f};"
      f" |rest - first| median x{np.exp((a.rest - a['first']).abs().median()):.2f}; drift rest-first mean x{np.exp((a.rest - a['first']).mean()):.2f}")

print("\n== Bid and ask: in runs with both sides of a market, the sellers' price over the buyers'")
ba = d.groupby(["market", "run", "side"]).lprice.mean().unstack("side").dropna()
ba["spread"] = np.exp(ba.sell - ba.buy)
print(ba.groupby("market").spread.agg(["size", "median"]).query("size >= 4").round(2).to_string())

print("\n== Hunger probe (one world, Opus Fowlers fixed): salt's price by the Ashby parents' model and wording")
h = d[(d.family == "hunger salt (38.66)") & (d.market == "salt in grain")].copy()
h["pair"] = h.run.str.extract(r"gph_salt_(\w+?)_")[0]
h["wording"] = h.run.str.extract(r"gph_salt_\w+?_(\w+)_r\d")[0]
h["fowler"] = h.by.isin(["Robert", "Maud", "Wat"])
print(h.groupby(["pair"]).agg(runs=("run", "nunique"), n=("lprice", "size"), price=("lprice", lambda s: np.exp(s.mean()))).round(2).to_string())
print(h.groupby(["wording"]).agg(runs=("run", "nunique"), n=("lprice", "size"), price=("lprice", lambda s: np.exp(s.mean()))).round(2).to_string())
print("Fowlers' first salt offer in each run (grain per salt):")
f = h[h.fowler & (h.side == "sell")].sort_values(["day", "offer"]).groupby("run").first()
print(f.assign(p=np.exp(f.lprice).round(2)).groupby("p").size().to_string())
