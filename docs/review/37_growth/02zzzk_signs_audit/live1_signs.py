"""Live run 1's signs, read from the run directories (W-103, 37.2 subagent, 23 Nov 2026). No model calls.

For each model arm: how often people attended and to what (the raw `attend` against the target the engine resolved), how many
lines attending gave, what reached people at the evening hearth ("saw_day") and the next morning ("saw"), sorted crudely into
mechanisms by keywords; a crude "acted on" share (guides/senses.md's measure: two of a line's content words reappear in the next
morning's reply or that evening's talk); the meal's lines; and the store-diff lines that a meal's draw shows as.

Usage: python3 live1_signs.py [/home/user/live1] > live1_signs.txt
"""
from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/user/live1")
ARMS = ["live1_A_pre", "live1_A_old", "live1_A_new", "live1_B_pre", "live1_B_new"]

# keyword buckets, first match wins (crude: a line is put under the first mechanism it names)
BUCKETS = [
    ("book and rules", r"\brule\b|by the household's|fallback"),
    ("people: body and care", r"looks well|drawn and hungry|gaunt|heavy with child|baby on her|carries a|has a load|blood to the elbows|"
                              r"heavy-eyed|slept out|slept in the open|kept .* close all day|is failing|childbed|moves stiffly|"
                              r"chewing raw|keep close together|spent the day|was about the|at .*'s side|a baby crying|children's voices|newborn"),
    ("racks, lots, fires, salt", r"smoke|racks|salter|\bpan\b|brine|salt|drying|dried at|hearth"),
    ("stores and vermin", r"store|bins|mouse|mice|\brats?\b|droppings|grain scattered|stink|going soft|flies at|gnawed|owl"),
    ("weir", r"\bweir\b|the gap"),
    ("set gear", r"\btraps?\b|snares?|gill net|set line|wicker"),
    ("river and runs", r"\beels?\b|salmon|lamprey|\brun\b|the Isel|spate|in flood|river|herons?"),
    ("shallows and resident fish", r"shallows|minnow|crayfish|margins|fish rising|fished"),
    ("wild: game, predators, fowl", r"wolf|wolves|fox|boar|deer|hare|otter|raven|crows?|kites?|fowl|duck|geese|pigeon|rooks?|tracks|bear|"
                                    r"badger|stoat|magpie|game|kestrel|owl"),
    ("woods and willow", r"timber|firewood|dead wood|sticks|withies|hazel|stumps|trees|coppice|axes"),
    ("fields, crops, herds", r"barley|\brye\b|beans|field|crop|grass|\bhay\b|herd|cows?|sheep|pasture|dung|\bhens?\b|eggs?|meadow"),
    ("buildings", r"wall|daub|thatch|roof|crack|draught|is sound|\bdoor\b|ruin|building|frame|mended|mending|limewash"),
    ("weather and ice", r"frost|rain|snow|\bice\b|wind|fog|cold|warm|storm|gale|bright day|grey day|sky|cloud|drizzle|downpour|heat"),
    ("travel and roads", r"road|travellers?|ford|bridge"),
    ("place, ambient", r"voices and work|water running|reeds hissing|houses round|nothing out of the ordinary"),
]
STOP = set("about after again along their there these those which where while would could should other being every under "
           "still today night water place heard tonight first river house store with from that this have they them your into more "
           "than what when some been were will over down just only like very also each both once then here near".split())


def bucket(line: str) -> str:
    for name, rx in BUCKETS:
        if re.search(rx, line, re.I):
            return name
    return "other"


def content(line: str) -> set:
    return {w for w in re.findall(r"[a-z]+", line.lower()) if len(w) >= 4 and w not in STOP}


def acted(line: str, text: str) -> bool:
    c = content(line)
    return len(c) >= 2 and sum(1 for w in c if w in text) >= 2


def kind_of(label: str | None, raw) -> str:
    if not raw:
        return "none"
    if label is None:
        return "none"
    if "could not find" in label:
        return "not found: the place in general"
    if label.startswith("how ") and "fits together" in label:
        return "the village (its layout)"
    if label == "the place in general":
        return "the place in general"
    if label == "the land and sky":
        return "the sky"
    if label.startswith("what lies there"):
        return "a thing by its tag"
    return "named: " + label


def target_class(label: str, state) -> str:
    """A resolved target's kind: a person, a building, a parcel or a herd (by the names in the final state)."""
    if not label:
        return "none"
    people = set(state["people"])
    if label in people:
        return "a person"
    if label in {b["name"] for b in state["buildings"].values()}:
        return "a building"
    if label in {p["name"] for p in state["parcels"].values()}:
        return "a parcel"
    if label in {h["name"] for h in state["herds"].values()}:
        return "a herd"
    return "other"


def section_lines(saw_day: list) -> dict:
    """Split a hearth block into its sections."""
    out = collections.defaultdict(list)
    sec = "felt or learned"
    for x in saw_day:
        if x == "What concerned you:":
            sec = "concerned"
        elif x == "What stood out:":
            sec = "stood out"
        elif x.startswith("You paid close attention to"):
            sec = "attended"
        elif x.startswith("In passing: "):
            out["in passing"] += [y.strip(" .") for y in x[len("In passing: "):].split(";")]
        elif x.startswith("- "):
            out[sec].append(x[2:])
    return out


def arm(name: str) -> dict:
    d = ROOT / name
    turns = [json.loads(l) for l in open(d / "turns.jsonl")]
    perc = [json.loads(l) for l in open(d / "perception.jsonl")]
    state = json.load(open(d / "state.json"))
    tgt = {(p["day"], p["agent"]): p for p in perc if p.get("phase") == "day"}
    by = {(t["day"], t["agent"]): t for t in turns}
    r = {"turns": len(turns)}
    r["attend_set"] = sum(1 for t in turns if t.get("attend"))
    kinds = collections.Counter()
    classes = collections.Counter()
    raw_examples = collections.Counter()
    lines_n, nothing = [], 0
    for t in turns:
        p = tgt.get((t["day"], t["agent"])) or {}
        k = kind_of(p.get("target"), t.get("attend"))
        kinds[k.split(":")[0] if k.startswith("named") else k] += 1
        if k.startswith("named"):
            classes[target_class(p.get("target"), state)] += 1
        if t.get("attend"):
            raw_examples[str(t["attend"])[:70]] += 1
    r["attend_kinds"] = kinds
    r["attend_classes"] = classes
    r["attend_raw_top"] = raw_examples.most_common(25)
    secs = collections.Counter()
    by_mech = collections.defaultdict(collections.Counter)
    acted_n = collections.defaultdict(lambda: [0, 0])
    lines = collections.Counter()
    meal = collections.Counter()
    store_diffs = 0
    nothing_att = 0
    att_turns = 0
    for who, m in state["mind"].items():
        for day in m.get("days") or []:
            dd = int(day["day"])
            nxt = by.get((dd + 1, who)) or {}
            tod = by.get((dd, who)) or {}
            evening = " ".join(str(x.get("reply") or "") for x in (tod.get("talk") or []) if isinstance(x, dict)
                               and str(x.get("wave", "")).startswith("evening"))
            reply = (json.dumps(nxt.get("reply") or {}) + " " + evening).lower()   # replies only, never the prompts
            sl = section_lines(day.get("saw_day") or [])
            if "attended" in sl:
                att_turns += 1
                if sl["attended"] == ["nothing out of the ordinary"]:
                    nothing_att += 1
                lines_n.append(len(sl["attended"]))
            for sec, xs in sl.items():
                for x in xs:
                    secs[sec] += 1
                    b = bucket(x)
                    by_mech[b][sec] += 1
                    lines[x] += 1
                    a = acted_n[(b, sec)]
                    a[1] += 1
                    a[0] += acted(x, reply)
            for x in day.get("saw") or []:
                x = x[2:] if x.startswith("- ") else x
                if x.endswith(":"):
                    continue
                secs["next morning"] += 1
                b = bucket(x)
                by_mech[b]["next morning"] += 1
                lines[x] += 1
                a = acted_n[(b, "next morning")]
                a[1] += 1
                a[0] += acted(x, json.dumps(nxt.get("reply") or {}).lower())   # seen next morning: that reply
            for x in day.get("did") or []:
                if "you ate" in x or "missed meal" in x or "less than a cold night" in x:
                    meal[re.sub(r"[0-9.]+", "N", x)[:110]] += 1
    for t in turns:
        p = t.get("prompt") or ""
        store_diffs += len(re.findall(r"store since you last looked", p))
    r["attended_turns"] = att_turns
    r["attend_nothing"] = nothing_att
    r["attend_lines_mean"] = round(sum(lines_n) / max(1, len(lines_n)), 2)
    r["sections"] = secs
    r["by_mech"] = by_mech
    r["acted"] = acted_n
    r["top_lines"] = lines.most_common(30)
    r["meal_lines"] = meal.most_common(8)
    r["store_diff_lines"] = store_diffs
    vanish = [(t["day"], t["agent"], (t.get("reply") or {}).get("why", "")[:160]) for t in turns
              if re.search(r"vanish|gone from the store|going fast|mice are at|rotting or mice|eaten by rats|disappear",
                           json.dumps(t.get("reply") or {}), re.I)]
    r["vanishing"] = vanish
    watch = sum(1 for t in turns for a in ((t.get("reply") or {}).get("actions") or []) if isinstance(a, dict)
                and str(a.get("do", "")).lower() in ("watch", "search", "look", "look closely", "examine", "inspect"))
    r["unit_looks"] = watch
    return r


def main() -> None:
    out = []
    for a in ARMS:
        if not (ROOT / a).exists():
            continue
        r = arm(a)
        out.append(f"# {a}")
        out.append(f"turns {r['turns']}; attend given {r['attend_set']} ({100 * r['attend_set'] / max(1, r['turns']):.0f}%); "
                   f"attended at the hearth {r['attended_turns']}, of them 'nothing out of the ordinary' {r['attend_nothing']}; "
                   f"lines an attended day {r['attend_lines_mean']}; acts that spend units to look (watch, search, look) {r['unit_looks']}")
        out.append("attend resolved to: " + ", ".join(f"{k} {v}" for k, v in r["attend_kinds"].most_common()))
        out.append("named targets by kind: " + ", ".join(f"{k} {v}" for k, v in r["attend_classes"].most_common()))
        out.append("raw attend, most common: " + "; ".join(f"{k!r} x{v}" for k, v in r["attend_raw_top"][:15]))
        out.append("lines by section: " + ", ".join(f"{k} {v}" for k, v in r["sections"].most_common()))
        out.append("by mechanism (section: lines, acted-on share):")
        for b, cs in sorted(r["by_mech"].items(), key=lambda kv: -sum(kv[1].values())):
            bits = []
            for sec, n in cs.most_common():
                a = r["acted"][(b, sec)]
                bits.append(f"{sec} {n} ({a[0] / max(1, a[1]):.2f})")
            out.append(f"  {b}: " + "; ".join(bits))
        out.append("most repeated lines:")
        out += [f"  {n:4d}  {x[:150]}" for x, n in r["top_lines"][:22]]
        out.append("meal lines (numbers as N): " + "; ".join(f"{x!r} x{n}" for x, n in r["meal_lines"]))
        out.append(f"'store since you last looked' lines in morning prompts: {r['store_diff_lines']}")
        out.append(f"replies reading the store's draw as things vanishing: {len(r['vanishing'])}")
        out += [f"  day {d} {a_}: {w}" for d, a_, w in r["vanishing"][:6]]
        out.append("")
    print("\n".join(out))


if __name__ == "__main__":
    main()
