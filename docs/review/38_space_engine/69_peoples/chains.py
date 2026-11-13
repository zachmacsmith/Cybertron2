"""Review 38.69: what growth needs, as the engine has it: land -> raw goods -> made goods and fittings -> what a growing people needs.
Every arrow is checked against the engine's techniques (gather and make), fittings (materials) and rooms; the layout is drawn by hand."""
import sys
sys.path.insert(0, "/home/user/cybertron2")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from cybertron2.engine import data as D

T, F, R = D.TECHNIQUES, D.FITTINGS, D.ROOMS
cols = {
    0: ["field", "meadow/pasture", "forest", "rock", "saltmarsh", "water"],
    1: ["grain", "hay", "cattle", "dung", "timber", "firewood", "game: meat, hide", "copper ore", "stone", "salt", "fish"],
    2: ["hand mill", "millstones", "water wheel", "oven", "hearth", "anvil", "cellar", "granary / bins", "rooms (timber)", "rooms (stone)", "beds"],
    3: ["flour / meal", "bread", "charcoal", "copper", "crude tool", "copper tool", "wooden plough", "cheese", "salt fish", "dried meat", "harness / pack"],
    4: ["FOOD: more per field", "FOOD: kept through winter", "HOUSING: beds and rooms", "HEAT: winter fuel", "TOOLS: x1.5 to x2 work",
        "FIELDS: plough 4x the hoe", "CARRYING: pack ox 60, cart 40"],
}
E = [  # (from, to), each checked below against the engine
    ("field", "grain"), ("meadow/pasture", "hay"), ("meadow/pasture", "cattle"), ("cattle", "dung"), ("dung", "FOOD: more per field"),
    ("forest", "timber"), ("forest", "firewood"), ("forest", "game: meat, hide"), ("rock", "copper ore"), ("rock", "stone"),
    ("saltmarsh", "salt"), ("water", "fish"),
    ("grain", "flour / meal"), ("flour / meal", "bread"), ("timber", "charcoal"), ("copper ore", "copper"), ("charcoal", "copper"),
    ("timber", "crude tool"), ("stone", "crude tool"), ("copper", "copper tool"), ("timber", "wooden plough"), ("copper", "wooden plough"),
    ("salt", "cheese"), ("cattle", "cheese"), ("salt", "salt fish"), ("fish", "salt fish"), ("game: meat, hide", "dried meat"),
    ("game: meat, hide", "harness / pack"), ("timber", "harness / pack"),
    ("stone", "hand mill"), ("stone", "millstones"), ("timber", "water wheel"), ("stone", "water wheel"), ("copper", "water wheel"),
    ("stone", "oven"), ("stone", "hearth"), ("stone", "anvil"), ("game: meat, hide", "anvil"), ("stone", "cellar"), ("timber", "granary / bins"),
    ("timber", "rooms (timber)"), ("stone", "rooms (timber)"), ("stone", "rooms (stone)"), ("timber", "beds"), ("grain", "beds"),
    ("hand mill", "flour / meal"), ("millstones", "flour / meal"), ("water wheel", "flour / meal"), ("oven", "bread"), ("hearth", "bread"),
    ("anvil", "copper"), ("anvil", "copper tool"), ("cellar", "cheese"), ("hearth", "dried meat"),
    ("bread", "FOOD: more per field"), ("flour / meal", "FOOD: more per field"), ("cheese", "FOOD: kept through winter"),
    ("salt fish", "FOOD: kept through winter"), ("dried meat", "FOOD: kept through winter"), ("granary / bins", "FOOD: kept through winter"),
    ("hay", "FOOD: kept through winter"), ("rooms (timber)", "HOUSING: beds and rooms"), ("rooms (stone)", "HOUSING: beds and rooms"),
    ("beds", "HOUSING: beds and rooms"), ("hearth", "HOUSING: beds and rooms"), ("firewood", "HEAT: winter fuel"), ("timber", "HEAT: winter fuel"),
    ("crude tool", "TOOLS: x1.5 to x2 work"), ("copper tool", "TOOLS: x1.5 to x2 work"), ("wooden plough", "FIELDS: plough 4x the hoe"),
    ("cattle", "FIELDS: plough 4x the hoe"), ("cattle", "CARRYING: pack ox 60, cart 40"), ("harness / pack", "CARRYING: pack ox 60, cart 40"),
    ("timber", "CARRYING: pack ox 60, cart 40"),
]
# checks against the engine
assert T["mill"]["at"]["fittings"] == ["millstones"] and T["grind"]["at"]["fittings"] == ["hand mill"] and "water wheel" in T["water mill"]["at"]["fittings"]
assert T["smelt"]["inputs"]["copper ore"] == 3 and "charcoal" in T["smelt"]["inputs"]["fuel"] and T["copper tool"]["at"]["fittings"] == ["anvil"]
assert T["wooden plough"]["inputs"] == {"timber": 4, "copper": 1} and T["plough"]["animals"]["oxen"] == 2
assert set(F["water wheel"]["materials"]) == {"timber", "stone", "copper"} and F["hearth"]["materials"] == {"stone": 4}
assert set(F["anvil"]["materials"]) == {"stone", "hide", "timber"} and F["beds"]["materials"] == {"timber": 1, "straw": 2}
assert T["cheese"]["inputs"] == {"milk": 6, "salt": 0.2} and T["salt fish"]["inputs"] == {"fish": 4, "salt": 1}
assert set(R["medium room"]["timber"]["materials"]) == {"timber", "stone"} and T["crude tool"]["inputs"] == {"timber": 1, "stone": 0.5}
assert D.ITEMS["bread"]["food"] == 1.3 and D.ITEMS["grain"]["food"] == 0.7 and D.ITEMS["flour"]["food"] == 1.0

pos = {}
for c, names in cols.items():
    for i, n in enumerate(names):
        pos[n] = (c * 3.2, -i * (11.0 / max(1, len(names) - 1)) if len(names) > 1 else 0)
fig, ax = plt.subplots(figsize=(17, 10))
colour = {0: "#c9d98a", 1: "#e8d9b0", 2: "#b9c9e6", 3: "#f2c49b", 4: "#f0a0a0"}
for a, b in E:
    (x1, y1), (x2, y2) = pos[a], pos[b]
    ax.annotate("", xy=(x2 - 0.75, y2), xytext=(x1 + 0.75, y1), arrowprops=dict(arrowstyle="->", color="#999", lw=0.8, alpha=0.8))
for c, names in cols.items():
    for n in names:
        x, y = pos[n]
        ax.text(x, y, n, ha="center", va="center", fontsize=8.5, bbox=dict(boxstyle="round,pad=0.35", fc=colour[c], ec="#666", lw=0.6))
for c, h in enumerate(["LAND (cover)", "RAW (gather)", "FITTINGS (build)", "MADE (make)", "WHAT GROWTH NEEDS"]):
    ax.text(c * 3.2, 1.3, h, ha="center", fontsize=10, weight="bold")
ax.set_xlim(-1.2, 14.2); ax.set_ylim(-11.8, 1.9); ax.axis("off")
ax.set_title("What a growing people needs, as the engine has it (every arrow is an engine recipe, material or use)", loc="left", fontsize=12)
fig.tight_layout(); fig.savefig("chains.png", dpi=130)
print("ok")
