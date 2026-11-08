"""M6a: what the engine's own renewal rules give a year, per unit of size, under a steady take (no LLM, the engine's pure functions)."""
import sys; sys.path.insert(0, "/home/user/cybertron2")
from cybertron2.engine import night as NI
from cybertron2.engine.data import PHYSICS
p = dict(PHYSICS)

def year_take(rule, K, r, effort, season_days=8, years=6, base=1.2, b=1.0, refuge=0.1):
    """Steady effort (units of work a night); take = base*effort*(S/K)**b, never below the refuge. Returns the last year's take."""
    S = K; tot = 0.0
    for y in range(years):
        tot = 0.0
        for d in range(4 * season_days):
            winter = (d // season_days) == 3
            want = base * effort * (S / K) ** b
            take = min(want, max(0.0, S - refuge * K))
            S -= take; tot += take
            S = NI.regrow(p, rule, S, K, r, winter)
    return tot, S / K

for name, rule, r, base in [("plants", "fast", 0.3, 1.2), ("game", "threshold", 0.25, None), ("grass", "fast", 0.32, 1.0)]:
    best = (0, 0, 0)
    for e100 in range(1, 400):
        e = e100 / 1000.0                      # effort per unit of K a night
        t, s = year_take(rule, 1.0, r, e, base=base or 1.0)
        if t > best[0]:
            best = (t, e, s)
    print(f"{name:7s} r={r}: best steady take {best[0]:.2f} a unit of K a year (32-day year) at effort {best[1]:.3f}/night, stock {best[2]:.2f} K")
