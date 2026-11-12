"""Adds each offer's market at the dawn of its day (38.66): the Fowlers' salt and grain, the Ashbys' grain. Reads prices.csv, writes
prices_state.csv.  python3 gph_prices_state.py RUNS_DIR"""
import csv, json, os, sqlite3, sys, zlib
RUNS = sys.argv[1]
rows = list(csv.DictReader(open("prices.csv")))
cache = {}


def dawn(run, day):
    key = (run, day)
    if key not in cache:
        con = sqlite3.connect(f"file:{os.path.join(RUNS, run)}/run.db?mode=ro", uri=True)
        r = con.execute("select z from checkpoints where step=? order by attempt desc limit 1", (f"d{day}.dawn",)).fetchone()
        w = json.loads(zlib.decompress(r[0]))["world"] if r else None
        if w:
            g = lambda b: w["containers"][w["buildings"][b]["stock"]]["goods"]
            hands = lambda ns, it: sum(w["containers"][w["people"][n]["hands"]]["goods"].get(it, 0) for n in ns if n in w["people"])
            cache[key] = {"fowler_salt": round(g("fowler_house").get("salt", 0) + hands(("Robert", "Maud", "Wat"), "salt"), 1),
                          "fowler_grain": round(g("fowler_house").get("grain", 0) + hands(("Robert", "Maud", "Wat"), "grain"), 1),
                          "ashby_grain": round(g("ashby_house").get("grain", 0) + hands(("Hugh", "Edith"), "grain"), 1)}
        else:
            cache[key] = {"fowler_salt": "", "fowler_grain": "", "ashby_grain": ""}
    return cache[key]


for r in rows:
    run = ("gph" if r["probe"] == "hunger" else "gp3") + f"_salt_{r['pair']}_{r['arm']}_{r['rep']}"
    r.update(dawn(run, r["day"]) if r["day"] != "" else {"fowler_salt": "", "fowler_grain": "", "ashby_grain": ""})
with open("prices_state.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print("ok", len(rows))
