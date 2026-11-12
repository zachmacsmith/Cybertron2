"""Every offer in every local cybertron2 run (review 38.67), with its market where the run keeps a state for each dawn (run.db).
    python3 offers_extract.py OUT.csv RUN_DIR [RUN_DIR ...]
One row per offer: the run, day, place, maker and household; what is given and asked (item and quantity, or days of work, or coin);
lots and lots taken; and, from the dawn of the offer's day where the run has it:
  - for the main item given and the main item asked: how much of it the place holds a head (stores, hands of those there, things
    lying there), and how much the maker's household holds;
  - the maker's hunger (0 fed, -1 hungry, -2 starving) and meals missed in a row; the household's food in days (food value / heads);
  - competition: the other offers open at the same place at dawn that give or ask the item given, and that give or ask the item
    asked;
  - mentions: how often the item's name is in what everyone said that day (their replies, not their prompts).
Runs from the first engine (m1_*) keep a different offer form and no day states: their rows carry no market."""
import csv, glob, json, os, re, sqlite3, sys, zlib

sys.path.insert(0, "/home/user/cybertron2")
from cybertron2.engine.data import ITEMS

OUT, DIRS = sys.argv[1], sys.argv[2:]
FOOD = {k: float(v.get("food", 0) or 0) for k, v in ITEMS.items()}


def legs(xs):
    """{item: qty}; days of work as 'work (days)'. Accepts the rebuilt engine's legs list or M1's dict."""
    if isinstance(xs, dict):
        return {k: float(v) for k, v in xs.items()}
    out = {}
    for x in xs or []:
        if x.get("item"):
            out[x["item"]] = out.get(x["item"], 0.0) + float(x.get("qty") or 0)
        elif x.get("work") is not None:
            out["work (days)"] = out.get("work (days)", 0.0) + float(x.get("work") or 0)
    return out


def later(xs):
    """1 if any leg is due later (a 'when' that is not now), else 0; '' for M1's form."""
    if isinstance(xs, dict):
        return ""
    return int(any(isinstance(x.get("when"), dict) and not x["when"].get("now") for x in xs or [] if x.get("item")))


def main_item(d):
    return max(d.items(), key=lambda kv: kv[1])[0] if d else ""


def checkpoints(run):
    p = f"{run}/run.db"
    if not os.path.exists(p):
        return None
    try:
        return sqlite3.connect(f"file:{p}?mode=ro", uri=True)
    except Exception:
        return None


def state_at(con, step):
    r = con.execute("select z from checkpoints where step=? order by attempt desc limit 1", (step,)).fetchone()
    return json.loads(zlib.decompress(r[0]))["world"] if r else None


def final_state(run, con):
    if os.path.exists(f"{run}/state.json"):
        try:
            return json.load(open(f"{run}/state.json"))
        except Exception:
            pass
    if con is not None:
        r = con.execute("select z from checkpoints order by rowid desc limit 1").fetchone()
        return json.loads(zlib.decompress(r[0]))["world"] if r else None
    return None


def household_of(w, name):
    for hid, inst in (w.get("institutions") or {}).items():
        if inst.get("kind") == "household" and name in (inst.get("members") or []):
            return hid
    return None


def market(w, node, maker, items):
    """The place's and the maker household's holdings of each item, a head; the maker's hunger; the household's food in days."""
    people = w.get("people") or {}
    here = [n for n, p in people.items() if p.get("alive", True) and p.get("at") == node]
    cids = set()
    for b in (w.get("buildings") or {}).values():
        if b.get("node") == node and b.get("stock"):
            cids.add(b["stock"])
    for n in here:
        if people[n].get("hands"):
            cids.add(people[n]["hands"])
    for cid, c in (w.get("containers") or {}).items():
        if c.get("node") == node and c.get("kind") not in ("hands",):
            cids.add(cid)
    goods = lambda cid: ((w.get("containers") or {}).get(cid) or {}).get("goods") or {}
    hh = household_of(w, maker)
    members = [n for n in ((w.get("institutions") or {}).get(hh) or {}).get("members", []) if people.get(n, {}).get("alive", True)] if hh else [maker]
    hcids = {people[n]["hands"] for n in members if people.get(n, {}).get("hands")}
    blds = w.get("buildings") or {}
    for c in (w.get("claims") or {}).values():                                # the household's stores: buildings it holds
        th = c.get("thing") or []
        if hh and c.get("claimant") == hh and len(th) == 2 and th[0] == "building" and "withdrawal" in (c.get("rights") or []):
            st = (blds.get(th[1]) or {}).get("stock")
            if st:
                hcids.add(st)
    out = {"people_here": len(here), "hh_size": len(members)}
    for tag, it in items.items():
        out[f"{tag}_place_per_head"] = round(sum(float(goods(c).get(it, 0)) for c in cids) / max(1, len(here)), 3) if it else ""
        out[f"{tag}_household"] = round(sum(float(goods(c).get(it, 0)) for c in hcids), 3) if it else ""
    food = sum(float(q) * FOOD.get(i, 0) for c in hcids for i, q in goods(c).items())
    out["hh_food_days"] = round(food / max(1, len(members)), 2)
    me = people.get(maker) or {}
    out["maker_hunger"] = me.get("hunger", "")
    out["maker_missed"] = me.get("missed", "")
    return out


def competition(w, node, oid, give_item, get_item):
    """Other offers open at the place at dawn: giving what this one gives (rival sellers), asking what it gives (others' demand for
    it), giving what it asks (others' supply of it), and asking what it asks (rival buyers)."""
    n = {"rival_sellers": 0, "demand_for_give": 0, "supply_of_get": 0, "rival_buyers": 0}
    for k, o in (w.get("offers") or {}).items():
        if k == oid or not o.get("open") or o.get("node") != node:
            continue
        g, t = legs(o.get("give")), legs(o.get("get"))
        n["rival_sellers"] += bool(give_item and give_item in g)
        n["demand_for_give"] += bool(give_item and give_item in t)
        n["supply_of_get"] += bool(get_item and get_item in g)
        n["rival_buyers"] += bool(get_item and get_item in t)
    return n


rows, seen = [], set()
runs = []
for d in DIRS:
    runs += sorted(p.rstrip("/") for p in glob.glob(os.path.join(d, "*/")))
for run in runs:
    name = os.path.basename(run)
    if name in seen or not os.path.exists(f"{run}/turns.jsonl"):
        continue
    seen.add(name)
    con = checkpoints(run)
    w = final_state(run, con)
    if not w or not w.get("offers"):
        continue
    made, said = {}, {}
    for l in open(f"{run}/turns.jsonl"):
        try:
            r = json.loads(l)
        except Exception:
            continue
        day = int(r.get("day", -1))
        for x in map(str, r.get("results") or []):
            m = re.match(r"You offered (O\d+)", x)
            if m:
                made.setdefault(m.group(1), day)
        txt = json.dumps(r.get("reply") or {}) + " ".join(json.dumps(t.get("reply") or {}) for t in (r.get("talk") or []) if isinstance(t, dict))
        txt += json.dumps(r.get("talk_reply") or {})
        said[day] = said.get(day, "") + " " + txt.lower()
    states = {}
    for oid, o in w["offers"].items():
        give, get = legs(o.get("give")), legs(o.get("get"))
        gi, ti = main_item(give), main_item(get)
        day = o.get("day", made.get(oid, ""))
        row = {"run": name, "offer": oid, "day": day, "node": o.get("node", w.get("node", "")), "by": o.get("by"), "model": str(((w.get("people") or {}).get(o.get("by")) or {}).get("model", "")).replace("claude-", "").split("-")[0], "for": o.get("for", ""),
               "to": o.get("to") or "", "give": json.dumps(give), "get": json.dumps(get), "give_item": gi, "give_qty": give.get(gi, ""),
               "get_item": ti, "get_qty": get.get(ti, ""), "n_give": len(give), "n_get": len(get), "lots": o.get("lots", 1),
               "taken": o.get("taken", 1 if o.get("held") else 0), "closed": o.get("closed", ""),
               "give_later": later(o.get("give")), "get_later": later(o.get("get"))}
        if con is not None and day != "" and row["node"]:
            if day not in states:
                states[day] = state_at(con, f"d{day}.dawn")
            ws = states[day]
            if ws:
                row.update(market(ws, row["node"], o.get("by"), {"give": gi, "get": ti}))
                row.update(competition(ws, row["node"], oid, gi, ti))
        txt = said.get(day, "") if day != "" else ""
        for tag, it in (("give", gi), ("get", ti)):
            row[f"{tag}_mentions"] = len(re.findall(r"\b" + re.escape(it.lower()) + r"\b", txt)) if it and txt else ""
        rows.append(row)
    if con is not None:
        con.close()
keys = []
for r in rows:
    for k in r:
        if k not in keys:
            keys.append(k)
with open(OUT, "w", newline="") as f:
    wr = csv.DictWriter(f, fieldnames=keys)
    wr.writeheader(); wr.writerows(rows)
print(len(rows), "offers from", len({r['run'] for r in rows}), "runs;", sum(1 for r in rows if r.get("people_here", "") != ""), "with a market")
