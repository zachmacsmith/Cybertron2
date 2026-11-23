# 39: monoculture worlds (session bench, W-103)

Session notes for proposals/monoculture_worlds.md and proposals/monoculture_five_worlds.md.

| File | What it is |
|---|---|
| `world0_map.py` → `world0_map.png`, `world0_flows.png` | World 0 (Highpool and Middleham) from `specs/water/runs.yaml`: the engine's places, covers, resources, wild land and rivers, with the design's households over them; and its dependencies |
| `design.py` | the five designed worlds as data (places, land, soil, resources, room, known or unexplored, roads in days), fitted in km with `specs/peoples_design.fit` |
| `draw.py` → `M1.png` to `M5.png` | their maps, in the form of the peoples maps (38_space_engine/69_peoples) |

Run from this folder: `python3 world0_map.py; python3 draw.py` (needs matplotlib and PyYAML).
