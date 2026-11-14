# The trace behind brief 4c §7.1 (14 Nov). It needs a scratch copy of wild/ecology.py with a DEBUG hook appending, for wolf and boar after
# each night's survival, the deaths by cause (base mortality, starvation, crowding, territory, named disease). The hook is not in the
# engine; the patch used is described in hunt_calibration.md §7.1.
import sys, json
S = "/tmp/claude-0/-home-user/7e098288-bcf5-5d91-98fd-74db17ae2c32/scratchpad"
sys.path.insert(0, f"{S}/peoples")
from cybertron2.wild import ecology as EC
EC.DEBUG = []
from cybertron2.engine import run as R
R.run(f"{S}/peoples/cybertron2/specs/peoples/w1.yaml", f"{S}/eco_trace_out", days=int(sys.argv[1]), bots=True)
json.dump(EC.DEBUG, open(f"{S}/eco_trace.json", "w"))
for r in EC.DEBUG:
    print(r["day"], r["k"][:6], f"N {r['N']:7.1f} eat {r['eat']:.2f} E {r['E']:.2f} | base {r['d_base']:.4f} starve {r['d_starve']:.4f} crowd {r['d_crowd']:.4f} terr {r['d_terr']:.4f} disease {r['d_extra']:.4f} | dead {r['dead']:.2f}")
