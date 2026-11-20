# The fuel budget (build brief 5 §4c; D2-209): a year on the river world

Run report (37.4, 16 Nov 2026). The harness is `cybertron2/fuel_budget.py` (any world path); its docstring says what it does. Dry,
bots, no model calls, about 10 seconds a year.

    python3 -m cybertron2.fuel_budget cybertron2/specs/water/river.yaml --smokehouse Saltwell --salter Saltwell --out river_year.json

**Set-up.** 37.2's river world (seed 9, 27 people, Saltwell's brine spring on the Brine Meadow held by Cole; Millham downstream),
one world year (32 days) from summer day 4. Everyone a bot without travel or felling; each household's first adult keeps its hearth
in firewood. Saltwell gets a wattle smokehouse (Hale; Tiffany smokes a 40-fish glut every 8 days, standing in for a run, tends it
daily and keeps it in firewood) and a salt house on the spring (Cole; Isolde boils salt once a day). Three arms:

| Arm | Hearths (both villages) | Smokehouse | Salt pan | Salt made | Smoked fish | Saltwell's dead wood (start 500) | Taken there by people | Fuel left in Saltwell's stores |
|---|---|---|---|---|---|---|---|---|
| null (no smokehouse, no salter) | 672 | 0 | 0 | 0 | 0 | 195 | 351 | 169 |
| as above (`river_year.json`) | 670 | 12 | 76 | 76 | 77.5 | 183 | 365 | 128 |
| heavy (`--boils 3 --every 4`) | 672 | 24 | 136 | 136 | 155 | 172 | 379 | 119 |

Firewood-equivalent (heat / 0.5); hearths burned firewood and some timber. Millham's dead wood ends at 195 in every arm.

**Reading.**
- The hearth is the largest draw, as the brief expects of fuel in a cool climate: about 335 firewood a village a year here. The
  smokehouse adds 1 firewood a night of fire (12 a year for 4 batches); the pan 1 a salt. A village that smokes and boils draws
  25 to 45% more fuel than one that does not; it comes first out of its stores (169 to 119 left), then its near woods.
- The near woods bind already: the dead wood a village gathers falls to about a third in one year in every arm, against a regrowth
  of about 48 a year (shed by the trees, less rot). Without cutting young growth or gathering further out, a second year would
  strip it. That is the brief's target (§4c.2), reached here by the hearths alone; the smokehouse and pan bring it forward by a
  few weeks. No hearth was starved in the year.
- The wild takes young growth (browsing: 870 to 925 a year at each village), not dead wood, so it does not compete with gathering.
- Not calibrated further: the smokehouse's and the pan's draws stand at the brief's numbers (1 firewood a night; 1 a salt, OPEN L-110).
  The bots' "make clappers" used 61 timber as material, listed apart in the JSON.

Sources: `river_year*.json` beside this note (the daily series, by wood and by village).
