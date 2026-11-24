"""Survey A (W-110): the named branches of a_named.py by the date their line was last written (git blame), against the area's
lines written on those dates: the density of branches on names over time. Run from the repo root."""
import subprocess, sys, os, collections, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.getcwd())
import a_named as A

def blame_dates(path):
    out = subprocess.run(["git", "blame", "--line-porcelain", "--", path], capture_output=True, text=True).stdout
    dates, cur, ln = {}, {}, 0
    for line in out.splitlines():
        p = line.split()
        if len(p) >= 3 and len(p[0]) == 40 and p[1].isdigit() and p[2].isdigit():
            ln = int(p[2]); sha = p[0]
        elif line.startswith("committer-time "):
            cur[sha] = datetime.date.fromtimestamp(int(p[1]))
        elif line.startswith("\t"):
            dates[ln] = cur.get(sha)
    return dates

def period(d):
    if d is None: return "?"
    if d <= datetime.date(2026, 10, 31): return "a 23-31 Oct (core, packages A-F)"
    if d <= datetime.date(2026, 11, 8): return "b 1-8 Nov (landgen, climate, renewal)"
    if d <= datetime.date(2026, 11, 14): return "c 9-14 Nov (wild layer, briefs 1-4c)"
    if d <= datetime.date(2026, 11, 19): return "d 15-19 Nov (river brief 5, waters, W-69 part)"
    return "e 20-24 Nov (W-69 fixes, the W-73 wave)"

lines, hits = collections.Counter(), collections.Counter()
only = sys.argv[1] if len(sys.argv) > 1 else ""
for f in [f for f in A.FILES if only in f]:
    dates = blame_dates(f)
    for ln, d in dates.items():
        lines[period(d)] += 1
    for h in A.scan(f):
        if h[0] in ("compare", "lookup", "dict", "via-constant"):
            hits[period(dates.get(h[1]))] += 1
for k in sorted(lines):
    print(f"{k:50s} lines now standing {lines[k]:6d}  named branches {hits[k]:4d}  per 100 lines {100 * hits[k] / max(1, lines[k]):.2f}")
