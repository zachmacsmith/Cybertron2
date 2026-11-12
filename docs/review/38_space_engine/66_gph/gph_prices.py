"""Exchange rates in the salt worlds (38.66): every offer and every agreement with salt on one side, across the hunger probe's runs
(gph_salt_*) and round 3's salt runs (gp3_salt_*). Writes prices.csv (one row an offer) and trades.csv (one row an agreement).
    python3 gph_prices.py RUNS_DIR"""
import csv, glob, json, os, re, sqlite3, sys, zlib

RUNS = sys.argv[1]
ASHBY, FOWLER = ("Hugh", "Edith"), ("Robert", "Maud", "Wat")


def last(run):
    con = sqlite3.connect(f"file:{run}/run.db?mode=ro", uri=True)
    return json.loads(zlib.decompress(con.execute("select * from checkpoints order by rowid desc limit 1").fetchone()[3]))["world"]


def legs(xs):
    out = {}
    for x in xs or []:
        if x.get("item"):
            out[x["item"]] = out.get(x["item"], 0.0) + float(x.get("qty") or 0)
        elif x.get("work"):
            out["work (days)"] = out.get("work (days)", 0.0) + float(x["work"])
    return out


offers, trades = [], []
for run in sorted(glob.glob(os.path.join(RUNS, "gph_salt_*_r*")) + glob.glob(os.path.join(RUNS, "gp3_salt_*_r1"))):
    if not os.path.exists(f"{run}/state.json") and not os.path.exists(f"{run}/run.db"):
        continue
    name = os.path.basename(run)
    probe = "hunger" if name.startswith("gph") else "round3"
    _, _, pair, rest = name.split("_", 3)
    arm, rep = rest.rsplit("_", 1)
    made = {}                                                            # offer id -> day it was made (from the maker's results)
    for l in open(f"{run}/turns.jsonl"):
        r = json.loads(l)
        for x in map(str, r.get("results") or []):
            m = re.match(r"You offered (O\d+):", x)
            if m:
                made.setdefault(m.group(1), int(r["day"]))
    s = last(run)
    for oid, o in s["offers"].items():
        give, get = legs(o.get("give")), legs(o.get("get"))
        if "salt" not in give and "salt" not in get:
            continue
        side = "Fowler" if o["by"] in FOWLER else ("Ashby" if o["by"] in ASHBY else o["by"])
        selling = "salt" in give                                         # the maker gives salt
        salt = give.get("salt") if selling else get.get("salt")
        other = get if selling else give
        for item, q in other.items():
            offers.append({"probe": probe, "pair": pair, "arm": arm, "rep": rep, "offer": oid, "day": made.get(oid, ""), "by": o["by"],
                           "side": side, "sells_salt": selling, "salt": salt, "for_item": item, "for_qty": q,
                           "price_per_salt": round(q / salt, 3) if salt else "", "lots": o.get("lots"), "taken": o.get("taken", 0),
                           "closed": o.get("closed") or ("open" if o.get("open") else "")})
    for aid, a in s["agreements"].items():
        if a.get("seeded"):
            continue
        salt = sum(float(x["qty"]) for x in a["legs"] if x.get("item") == "salt")
        if not salt:
            continue
        rest_ = {}
        for x in a["legs"]:
            if x.get("item") and x["item"] != "salt":
                rest_[x["item"]] = rest_.get(x["item"], 0.0) + float(x["qty"])
            elif x.get("work"):
                rest_["work (days)"] = rest_.get("work (days)", 0.0) + float(x["work"])
        for item, q in rest_.items():
            trades.append({"probe": probe, "pair": pair, "arm": arm, "rep": rep, "agreement": aid, "day": a.get("day"),
                           "made_by": "+".join(a.get("made_by") or []), "salt": salt, "for_item": item, "for_qty": q,
                           "price_per_salt": round(q / salt, 3)})
out = os.path.dirname(os.path.abspath(__file__))
for fn, rows in (("prices.csv", offers), ("trades.csv", trades)):
    with open(os.path.join(out, fn), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
print(len(offers), "offers;", len(trades), "trades")
