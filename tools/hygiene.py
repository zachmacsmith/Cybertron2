#!/usr/bin/env python3
"""Record hygiene for cybertron2's design documents: a report of what the process leaves undone.

The design process (docs/cybertron2/README.md) keeps proposals, numbered decisions, a spec of what holds, open questions and things
flagged for later. Agents are good at adding to these and poor at closing, merging and updating them. This script reports the
gaps, so they are found at the end of a session instead of by accident:

  1. decisions never cited in any spec file (the spec should hold every decided rule);
  2. decisions that replace an earlier one whose row is not marked "replaced by";
  3. spec files whose "Current as of" line is older than decisions that name them, or missing, or old;
  4. proposals: no Status line, missing from the index, the index naming a file that is not there, or left in discussion;
  5. OPEN.md: rows done or closed but not struck through, flagged rows with no date, flagged rows left long;
  6. paths into a session's scratchpad (files no other session can reach) in the repository;
  7. dates later than today;
  8. relative links to files that do not exist;
  9. the board's last post;
 10. WORK.md: work in progress left untouched, waiting on an ask too long, queued and not begun, paused too long, or without
     where it is and what is left;
 11. asks (OPEN.md's open questions and conflicts) left unanswered, and deferred rows that name nothing they wait on.

It also counts the unfinished work (in progress, paused, asks, deferred, chores); `--record` writes today's counts into WORK.md's
size table, so the size of what is left can be followed over time.

Run from the repository root:  python3 tools/hygiene.py [--all] [--days N] [--today YYYY-MM-DD] [--strict] [--record]
  --all     list every item (default: the first 12 of each)
  --days N  what counts as left long (default 3 for proposals in discussion, 4N for flagged rows and spec files)
  --strict  exit 1 if any check finds something (for a hook or CI)
  --record  write today's counts into docs/cybertron2/WORK.md's size table

A decision row that is deliberately not a spec rule (a process choice, a permission) can carry "[no spec]" anywhere in its text to
be left out of check 1. Stdlib only; reads files and `git log`; changes nothing.
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS = os.path.join(ROOT, "docs")
C2 = os.path.join(DOCS, "cybertron2")
MONTHS = {m: i for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}
DID = r"D\d+-\d+"


def read(path) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def rel(path) -> str:
    return os.path.relpath(path, ROOT)


def day_month(s, year) -> dt.date | None:
    m = re.match(r"\s*(\d{1,2}) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*(?: (\d{4}))?", s)
    if not m:
        return None
    try:
        return dt.date(int(m.group(3) or year), MONTHS[m.group(2)], int(m.group(1)))
    except ValueError:
        return None


def git_date(path) -> dt.date | None:
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%ad", "--date=short", "--", path], cwd=ROOT, capture_output=True,
                             text=True, timeout=30).stdout.strip()
        return dt.date.fromisoformat(out) if out else None
    except Exception:
        return None


def table_rows(text, first_cell) -> list:
    """Markdown table rows whose first cell matches the pattern, as lists of cells."""
    out = []
    for line in text.split("\n"):
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells and re.match(first_cell, cells[0]):
                out.append(cells)
    return out


# ---------------------------------------------------------------------- the checks
def decisions(today):
    text = read(os.path.join(C2, "DECISIONS.md"))
    rows = table_rows(text, r"^~?~?" + DID)
    out = []
    for c in rows:
        did = re.search(DID, c[0]).group(0)
        date = day_month(c[1], today.year) if len(c) > 1 else None
        out.append({"id": did, "date": date, "cells": c, "row": " | ".join(c)})
    return out


def check_not_in_spec(rows):
    spec = "\n".join(read(f) for f in glob.glob(os.path.join(C2, "spec", "**", "*.md"), recursive=True))
    found = []
    for r in rows:
        if "[no spec]" in r["row"] or r["cells"][0].startswith("~~"):
            continue
        if not re.search(r"\b" + re.escape(r["id"]) + r"\b", spec):
            found.append(f"{r['id']} ({r['date'] or '?'}): {re.sub(r'[*]', '', r['cells'][2])[:110] if len(r['cells']) > 2 else ''}")
    return found


def check_replaced_unmarked(rows):
    by_id = {r["id"]: r for r in rows}
    found = []
    for r in rows:
        if len(r["cells"]) < 5:
            continue
        cell = r["cells"][4]
        if re.search(r"replaced|superseded", cell, re.I):                  # this row records that it was replaced: not a "replaces"
            continue
        for old in re.findall(DID, cell):
            o = by_id.get(old)
            if o and old != r["id"] and not re.search(r"replaced|superseded", o["row"], re.I):
                found.append(f"{old} is replaced (in part) by {r['id']} but its row does not say so")
    return found


def check_spec(rows, today, days):
    found = []
    for f in sorted(glob.glob(os.path.join(C2, "spec", "**", "*.md"), recursive=True)):
        if os.path.basename(f) == "README.md":
            continue
        s = read(f)
        m = re.search(r"\*Current as of ([^:*]+)", s)
        if not m:
            found.append(f"{rel(f)}: no 'Current as of' line")
            continue
        asof = day_month(m.group(1), today.year)
        if asof is None:
            continue
        base = os.path.basename(f)
        area = os.path.basename(os.path.dirname(f))
        newer = [r["id"] for r in rows if r["date"] and r["date"] > asof
                 and re.search(r"spec/(?:" + re.escape(area) + r"/)?" + re.escape(base) + r"|\b" + re.escape(area) + "/" + re.escape(base), r["row"])]
        if newer:
            found.append(f"{rel(f)}: current as of {asof}, but later decisions name it: {', '.join(newer[:8])}")
        elif (today - asof).days > 4 * days:
            found.append(f"{rel(f)}: current as of {asof} ({(today - asof).days} days); check it still holds")
    return found


def check_proposals(today, days):
    pdir = os.path.join(C2, "proposals")
    index = read(os.path.join(pdir, "README.md"))
    linked = set(re.findall(r"\]\(([^)#/]+\.md)\)", index))
    found = []
    for f in sorted(glob.glob(os.path.join(pdir, "*.md"))):
        name = os.path.basename(f)
        if name == "README.md":
            continue
        s = read(f)
        m = re.search(r"\*\*Status:\*\*\s*([^\n]*)", s)
        if not m:
            found.append(f"{name}: no Status line")
            continue
        status = m.group(1).lower()
        if name not in linked:
            found.append(f"{name}: not in proposals/README.md")
        if ("discussion" in status or "ready for a decision" in status) and "accepted" not in status:
            d = git_date(f)
            if d and (today - d).days >= days:
                found.append(f"{name}: '{m.group(1)[:50]}', last changed {d} ({(today - d).days} days)")
    for name in sorted(linked):
        if not os.path.exists(os.path.join(pdir, name)):
            found.append(f"proposals/README.md links {name}, which is not there")
    return found


def check_open(today, days):
    text = read(os.path.join(C2, "OPEN.md"))
    found = []
    for c in table_rows(text, r"^(?:~~)?[A-Z]+-[A-Z0-9-]+"):
        struck = c[0].startswith("~~")
        body = " | ".join(c[1:])
        if not struck and re.search(r"\*\*\(?(Closed|Done)\b|~~[^~]{3,}~~\s*\*\*Done", body):
            found.append(f"{c[0]}: marked done or closed but not struck through")
    for c in table_rows(text, r"^L-\d+"):
        body = " | ".join(c)
        if re.search(r"\b(Closed|Done)\b", body):
            continue
        dates = [d for d in (day_month(x, today.year) for x in re.findall(r"\d{1,2} (?:Oct|Nov|Dec|Jan|Feb|Sep)\w*", body)) if d]
        if not dates:
            found.append(f"{c[0]}: flagged with no date ({re.sub(r'[*]', '', c[1])[:70]})")
        elif (today - min(dates)).days > 4 * days:
            found.append(f"{c[0]}: flagged {min(dates)} ({(today - min(dates)).days} days), still open: {re.sub(r'[*]', '', c[1])[:70]}")
        if re.search(r"to be written into|compile .* into spec|into spec/", body, re.I):
            found.append(f"{c[0]}: a write-up into the spec still owed")
    return found


def check_scratchpad():
    found = []
    pat = re.compile(r"/tmp/claude-\d+|scratchpad/[\w./-]+\.(?:py|json|yaml|yml)")
    for f in subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split("\n"):
        if not f or not f.endswith((".md", ".py", ".yaml", ".yml", ".json", ".txt")) or f == "tools/hygiene.py":
            continue
        try:
            s = read(os.path.join(ROOT, f))
        except Exception:
            continue
        for i, line in enumerate(s.split("\n"), 1):
            if pat.search(line):
                found.append(f"{f}:{i}: {line.strip()[:100]}")
    return found


def check_future_dates(today):
    found = []
    pat = re.compile(r"\b(\d{1,2}) (Oct|Nov|Dec)\b(?! \d{4})|\b(20\d\d-\d\d-\d\d)\b")
    for f in glob.glob(os.path.join(C2, "**", "*.md"), recursive=True) + glob.glob(os.path.join(DOCS, "review", "**", "*.md"), recursive=True):
        try:
            s = read(f)
        except Exception:
            continue
        for i, line in enumerate(s.split("\n"), 1):
            for m in pat.finditer(line):
                try:
                    d = dt.date.fromisoformat(m.group(3)) if m.group(3) else dt.date(today.year, MONTHS[m.group(2)], int(m.group(1)))
                except ValueError:
                    continue
                if d > today and (d - today).days < 60:
                    found.append(f"{rel(f)}:{i}: {m.group(0)}")
    return found


def check_links():
    found = []
    for f in glob.glob(os.path.join(C2, "**", "*.md"), recursive=True) + glob.glob(os.path.join(DOCS, "review", "**", "*.md"), recursive=True):
        s = read(f)
        for m in re.finditer(r"\]\(([^)\s]+?\.(?:md|py|yaml|json))(?:#[^)]*)?\)", s):
            target = m.group(1)
            if target.startswith(("http", "/")):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(f), target))):
                found.append(f"{rel(f)}: link to {target}")
    return found


def check_board(today):
    path = os.path.join(DOCS, "coord", "BOARD.md")
    if not os.path.exists(path):
        return []
    d = git_date(path)
    return [f"docs/coord/BOARD.md last changed {d} ({(today - d).days} days ago)"] if d else []


WORK = os.path.join(C2, "WORK.md")


def section(text, head):
    """The text of a `## head` section (to the next `## `)."""
    m = re.search(r"^## " + re.escape(head) + r"[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else ""


def work_rows():
    if not os.path.exists(WORK):
        return {}
    text = read(WORK)
    return {name: table_rows(section(text, name), r"^W-\d+") for name in ("In progress", "Paused", "Done")}


def check_work(today, days):
    found = []
    rows = work_rows()
    if not rows:
        return ["docs/cybertron2/WORK.md is missing"]
    for name in ("In progress", "Paused"):
        for c in rows.get(name, []):
            if len(c) < 8:
                found.append(f"{c[0]}: a row of {len(c)} cells (8 expected)")
                continue
            wid, what, owner, state, started, touched, where, notes = c[:8]
            t = day_month(touched, today.year) or day_month(started, today.year)
            age = (today - t).days if t else None
            label = f"{wid} ({owner}; {state}): {re.sub(r'[*]', '', what)[:70]}"
            if not where.strip() or not notes.strip():
                found.append(f"{label}: says nothing of where it is or what is left")
            if age is None:
                found.append(f"{label}: no date")
            elif name == "In progress" and state.startswith("active") and age > days:
                found.append(f"{label}: untouched {age} days: carry on, or move it to Paused")
            elif name == "In progress" and state.startswith("waiting") and age > days:
                found.append(f"{label}: waiting {age} days: raise the ask again, or take its default")
            elif name == "In progress" and state.startswith("queued") and age > 2 * days:
                found.append(f"{label}: queued {age} days and not begun")
            elif name == "Paused" and age > 5 * days:
                found.append(f"{label}: paused {age} days: resume, defer or drop it")
    return found


def asks_and_deferred(today):
    """(open asks [(id, text)], open deferred [cells])."""
    text = read(os.path.join(C2, "OPEN.md"))
    asks, deferred = [], []
    for c in table_rows(section(text, "Conflicts between documents") + section(text, "Open questions"), r"^[A-Z]+-[A-Z0-9-]+"):
        body = " | ".join(c)
        if c[0].startswith("~~") or re.search(r"\(Closed\b|\*\*Done\b|\(Deferred\b", body):
            continue
        asks.append((c[0], body))
    for c in table_rows(section(text, "Flagged for later"), r"^L-\d+"):
        if re.search(r"\b(Closed|Done)\b", " | ".join(c)):
            continue
        deferred.append(c)
    return asks, deferred


def check_asks(today, days):
    asks, deferred = asks_and_deferred(today)
    found, undated = [], 0
    for rid, body in asks:
        dates = [d for d in (day_month(x, today.year) for x in re.findall(r"\d{1,2} (?:Oct|Nov|Dec|Jan|Feb|Sep)\w*", body)) if d]
        if not dates:
            undated += 1
            continue
        age = (today - max(dates)).days
        if age > days and "default taken" not in body.lower():
            found.append(f"{rid}: last touched {age} days ago, no answer recorded: {re.sub(r'[*]', '', body.split(' | ')[1])[:80]}")
    if undated:
        found.append(f"{undated} open asks carry no date, so their age cannot be told")
    for c in deferred:
        if len(c) > 4 and not c[4].strip():
            found.append(f"{c[0]}: deferred with nothing named that it waits on")
    return found


def record(today, counts):
    text = read(WORK)
    line = f"| {today} | {counts['in progress']} | {counts['paused']} | {counts['asks']} | {counts['deferred']} | {counts['chores']} |"
    lines = [l for l in text.rstrip("\n").split("\n") if not l.startswith(f"| {today} |")]
    with open(WORK, "w", encoding="utf-8") as f:
        f.write("\n".join(lines + [line]) + "\n")


# ---------------------------------------------------------------------- the report
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--days", type=int, default=3)
    ap.add_argument("--today", type=str, default=None)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--record", action="store_true")
    a = ap.parse_args(argv)
    today = dt.date.fromisoformat(a.today) if a.today else dt.date.today()
    rows = decisions(today)
    checks = [
        ("1. Decisions not cited in any spec file", check_not_in_spec(rows)),
        ("2. Replaced decisions not marked", check_replaced_unmarked(rows)),
        ("3. Spec files behind their decisions, or old", check_spec(rows, today, a.days)),
        ("4. Proposals", check_proposals(today, a.days)),
        ("5. OPEN.md", check_open(today, a.days)),
        ("6. Paths into a session's scratchpad", check_scratchpad()),
        ("7. Dates later than today", check_future_dates(today)),
        ("8. Links to missing files", check_links()),
        ("9. The board", check_board(today)),
        ("10. WORK.md: work left", check_work(today, a.days)),
        ("11. Asks unanswered, deferred rows without a trigger", check_asks(today, a.days)),
    ]
    wr = work_rows()
    asks, deferred = asks_and_deferred(today)
    chores = sum(len(f) for t, f in checks if t[:2] in ("1.", "2.", "5.", "6.", "8."))
    counts = {"in progress": len(wr.get("In progress", [])), "paused": len(wr.get("Paused", [])), "asks": len(asks),
              "deferred": len(deferred), "chores": chores}
    print(f"# Record hygiene, {today} ({len(rows)} decisions)\n")
    print("Unfinished: " + ", ".join(f"{v} {k}" for k, v in counts.items()) + "\n")
    print("| Check | Found |\n|---|---|")
    for title, found in checks:
        print(f"| {title} | {len(found)} |")
    for title, found in checks:
        if not found:
            continue
        print(f"\n## {title} ({len(found)})")
        for x in (found if a.all else found[:12]):
            print(f"- {x}")
        if not a.all and len(found) > 12:
            print(f"- ... and {len(found) - 12} more (--all)")
    if a.record:
        record(today, counts)
        print(f"\nRecorded in {rel(WORK)}.")
    serious = sum(len(f) for t, f in checks if not t.startswith("9."))
    return 1 if a.strict and serious else 0


if __name__ == "__main__":
    sys.exit(main())
