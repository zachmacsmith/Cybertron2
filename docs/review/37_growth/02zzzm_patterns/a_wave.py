"""Survey A (W-110): which of a_named.py's hits came in the W-73 wave (lines changed since f728a3b7, by git blame).
Run from the repo root: python3 docs/review/37_growth/02zzzm_patterns/a_wave.py"""
import subprocess, sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.getcwd())
import a_named as A

BASE = "f728a3b7"

def wave_lines(path):
    out = subprocess.run(["git", "blame", "-s", "--line-porcelain", f"{BASE}..HEAD", "--", path], capture_output=True, text=True).stdout
    new, ln = set(), 0
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 3 and len(parts[0]) == 40 and parts[1].isdigit() and parts[2].isdigit():
            ln = int(parts[2])
            if not line.startswith("^"):
                new.add(ln)
        elif line.startswith("boundary"):
            new.discard(ln)
    return new

tot = collections.Counter()
for f in A.FILES:
    hits = [h for h in A.scan(f) if h[0] in ("compare", "lookup", "dict", "via-constant")]
    if not hits:
        continue
    nw = wave_lines(f)
    n = sum(1 for h in hits if h[1] in nw)
    tot["all"] += len(hits)
    tot["wave"] += n
    print(f"{f:40s} {len(hits):4d} named branches, {n:4d} in the wave; lines changed in the wave {len(nw)}")
print(dict(tot))
