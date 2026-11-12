"""Review 38.68: the forms of exchange in every local cybertron2 run. Per run: formal agreements (spot, credit in goods, work, instalments;
done, open, in arrears, released); gifts between households (the give verb) and whether they were returned; private notes kept as
ledgers; and the words of debt, trust and gift in what people said. Writes runs.csv, gifts.csv, agreements.csv, quotes.jsonl.
    python3 econ_extract.py RUN_DIR [RUN_DIR ...]"""
import csv, glob, json, os, re, sqlite3, sys, zlib

DIRS = sys.argv[1:]
WORDS = {
    "debt": r"\b(owe[sd]?|owing|debts?|repa(y|id|yment)|pay (you|it|them|him|her) back|in arrears|on account|on credit|a loan|lend|lent|borrow\w*)\b",
    "trust": r"\b(trust\w*|my word|your word|his word|her word|their word|good faith|honou?r\w*|reliab\w*|cheat\w*|swindl\w*|reputation|known for|kept (my|his|her|their|our) (word|promise)|broke (my|his|her|their|our) (word|promise))\b",
    "gift": r"\b(gift\w*|freely|for nothing|no charge|nothing in return|as a kindness|in kindness|charity|neighbou?rl\w*|share\w*|spare you)\b",
    "reciprocity": r"\b(in return|return the favou?r|a favou?r|when you can|when the harvest|after (the )?harvest|repay the kindness|remember (this|it|that))\b",
    "price": r"\b(price|rate|cheap\w*|dear(er)?|bargain\w*|haggl\w*|fair (price|trade|deal|exchange))\b",
}


def final(run):
    if os.path.exists(f"{run}/state.json"):
        try:
            return json.load(open(f"{run}/state.json"))
        except Exception:
            pass
    p = f"{run}/run.db"
    if os.path.exists(p):
        con = sqlite3.connect(f"file:{p}?mode=ro", uri=True)
        r = con.execute("select z from checkpoints order by rowid desc limit 1").fetchone()
        return json.loads(zlib.decompress(r[0]))["world"] if r else None
    return None


def hh_map(w):
    out = {}
    for hid, inst in (w.get("institutions") or {}).items():
        if inst.get("kind") == "household":
            for m in inst.get("members") or []:
                out[m] = hid
    return out


def spoken(r):
    """What the person chose to say: tell and say texts of the reply and the talk waves (not the prompts)."""
    texts = []
    reps = [r.get("reply")] + [t.get("reply") for t in (r.get("talk") or []) if isinstance(t, dict)]
    for rep in reps:
        if not isinstance(rep, dict):
            continue
        for k in ("tell", "say"):
            for t in rep.get(k) or []:
                if isinstance(t, dict) and t.get("text"):
                    texts.append(str(t["text"]))
    return texts


runs, gifts, ags, quotes = [], [], [], []
seen = set()
for d in DIRS:
    for run in sorted(p.rstrip("/") for p in glob.glob(os.path.join(d, "*/"))):
        name = os.path.basename(run)
        if name in seen or not os.path.exists(f"{run}/turns.jsonl"):
            continue
        w = final(run)
        if not w:
            continue
        seen.add(name)
        hh = hh_map(w)
        row = {"run": name, "people": len(w.get("people") or {}), "households": len(set(hh.values())), "days": w.get("day", ""),
               "turns": 0, "offers": len(w.get("offers") or {})}
        for k in WORDS:
            row[f"say_{k}"] = 0
        row["says"] = 0
        n_gift = n_gift_x = 0
        for l in open(f"{run}/turns.jsonl"):
            try:
                r = json.loads(l)
            except Exception:
                continue
            row["turns"] += 1
            who, day = r.get("agent"), r.get("day")
            for x in map(str, r.get("results") or []):
                m = re.match(r"You gave ([\d.]+) (.+?) to ([A-Z][\w' -]*?)\.( \(|$)", x)
                if m:
                    to = m.group(3)
                    a, b = r.get("household") or hh.get(who), hh.get(to)
                    gifts.append({"run": name, "day": day, "by": who, "by_hh": a, "to": to, "to_hh": b, "item": m.group(2), "qty": float(m.group(1)),
                                  "cross": int(bool(a and b and a != b)), "model": r.get("model", "")})
            for t in spoken(r):
                row["says"] += 1
                for k, rx in WORDS.items():
                    if re.search(rx, t, re.I):
                        row[f"say_{k}"] += 1
                        if k in ("debt", "trust", "reciprocity", "gift"):
                            quotes.append({"run": name, "day": day, "by": who, "model": r.get("model", ""), "kind": k, "text": t[:400]})
        ledgers = []
        for n, p in (w.get("people") or {}).items():
            for title, text in (p.get("notes") or {}).items():
                if re.search(WORDS["debt"] + "|" + r"\b(account|tally|ledger|promised|agreed)\b", f"{title} {text}", re.I):
                    ledgers.append(n)
                    quotes.append({"run": name, "day": "end", "by": n, "model": p.get("model", ""), "kind": "note", "text": f"[{title}] {str(text)[:400]}"})
        row["people_with_ledger_notes"] = len(set(ledgers))
        for aid, ag in (w.get("agreements") or {}).items():
            legs = ag.get("legs") or []
            if isinstance(legs, dict) or not isinstance(legs, list):
                continue
            kinds = set()
            for lg in legs:
                if "work" in lg:
                    kinds.add("work")
                elif "plots" in lg:
                    kinds.add("land")
                else:
                    wh = lg.get("when") or {}
                    kinds.add("instalments" if wh.get("every") else "later" if wh.get("by") is not None else "now")
            a_hh = {hh.get(p) for p in ag.get("parties") or []}
            ags.append({"run": name, "agreement": aid, "day": ag.get("day"), "status": ag.get("status"), "seeded": int(bool(ag.get("seeded"))),
                        "parties": "|".join(ag.get("parties") or []), "same_household": int(len(a_hh) == 1),
                        "kinds": "+".join(sorted(kinds)), "credit": int(bool(kinds & {"later", "instalments", "work"})),
                        "work": int("work" in kinds), "arrears": round(sum(float(l.get("arrears", 0) or 0) for l in legs), 3),
                        "work_owed": sum(max(0, int(l.get("work", 0)) - int(l.get("done", 0))) for l in legs if "work" in l),
                        "released": int(any(l.get("released_by") for l in legs)),
                        "items": "|".join(sorted({str(l.get("item")) for l in legs if l.get("item")})),
                        "coin": int(any(l.get("item") == "coin" for l in legs))})
        runs.append(row)

for fn, rows in (("runs.csv", runs), ("gifts.csv", gifts), ("agreements.csv", ags)):
    keys = []
    for r in rows:
        keys += [k for k in r if k not in keys]
    with open(fn, "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=keys); wr.writeheader(); wr.writerows(rows)
with open("quotes.jsonl", "w") as f:
    for q in quotes:
        f.write(json.dumps(q) + "\n")
print(len(runs), "runs;", len(ags), "agreements;", len(gifts), "gives;", len(quotes), "quotes")
