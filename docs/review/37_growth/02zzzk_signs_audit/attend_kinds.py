"""Sort the new arms' unresolved attends (attend_targets.txt) into what people wanted to look at (crude keywords, first match)."""
import collections
import re
import sys

B = [("set gear and its catch", r"traps|trap\b|\bT\d"),
     ("a person's body", r"gaunt|hungry|fare after|unsteady|fed and sleeping"),
     ("racks and lots", r"\bracks|heap|\blot\b|Smokehouse fire|smokehouse fire"),
     ("a store's goods or vermin", r"store|roots|bins|sacks|rats|mouse|grain scattered|fish in my hands|going soft|soft fish"),
     ("a wall, crack or house", r"wall|crack|daub|draught|cold far end|cold end|Byre"),
     ("the water, the weir, a spate", r"Isel|weir|water level|spate|flood|eels"),
     ("a person at a craft, to learn", r"hands|sets his hands|at the pan|making the wicker|handles|salting|lifting|tending|cutting|"
                                       r"gives the orders|at the hearth|withy|going out"),
     ("greens, grass, nettle, beans", r"nettle|greens|grass|grubs|beans|nuts"),
     ("offers, leave, what a person will do", r"offer|leave|agree|speaks|sets the day"),
     ("weather", r"fog")]
rows = [l for l in open(sys.argv[1] if len(sys.argv) > 1 else "attend_targets.txt") if "NOTFOUND" in l]
c, ex = collections.Counter(), {}
for l in rows:
    t = l.split("|", 1)[1].split("=>")[0].strip()
    for n, rx in B:
        if re.search(rx, t):
            c[n] += 1
            ex.setdefault(n, []).append(t)
            break
    else:
        c["other"] += 1
        ex.setdefault("other", []).append(t)
print(f"{len(rows)} unresolved attends in the new arms")
for k, v in c.most_common():
    print(f"{v:3d}  {k}: " + " | ".join(x[:70] for x in ex[k][:3]))
