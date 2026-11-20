# The nutrition worlds

Worlds where a village lives off one livelihood alone (proposals/subsistence_worlds.md; D2-242, D2-256; WORK W-69). Each comes in
arms on the same land and people, differing only in seeded skill and capital.

## The runs (`runs_low.yaml`, `runs_medium.yaml`, `runs_high.yaml`)

Made by `cybertron2/specs/make_nutrition_runs.py`, seed 5.

- **The world:**
  - Eelmouth, one village of 12 people in three households, low on a large river. The river rises in wild upland, where the
    salmon spawn, and leaves the window to the south.
  - Two compressed years (64 days at 32 a year) from late summer, so two autumn runs and two winters.
  - The runs on their windows' set nights (D2-231).
  - The cast: Opus at each household head, Sonnet in the middle, Haiku for the rest.
- **What makes it runs-only:**
  - no fields, seed or herds, and no farm goods in store;
  - no resident fish stocked;
  - a larder of about 8 days of food (dried meat and roots), enough to reach the autumn runs and no more;
  - game and wild plants at the land's own level.

  The people know only their fishing crafts at the arm's level. This isolation is approximate: exact per-world switches for game
  and fish are 37.4's prerequisite (D2-256).

| Arm | Skill | Crafts known | Capital |
|---|---|---|---|
| low | novice (rough, 0.6) | traps in the water | none: nothing can be kept but by eating it |
| medium | capable (known, 1.0) | traps, nets, smoking | smoke racks at each house |
| high | master (known, 1.6) | traps, nets, the weir, smoking, salting, boiling salt | a weir of three timber sections on the village's river water, the first in timber too, worked by its crew (the holding household's adults who know the weir, so its traps are known to them); smoke racks at each house; a salt house with a brine pan at the village's brine spring, 10 salt in store |

- **The high arm's weir is all timber.** Since the water fixes (W-69, 20 Nov) a section's place decides what it takes and holds
  (the first 30% of a run and 100 kg a night, each added one 7% and 70 kg) and its material decides its wear and cost, so the
  first section can be timber. A master's village on a flood river would build it so: a timber section wears at half wattle's
  rate (about a quarter of its cost a year to keep here, against half for wattle).
- **Applied:** the food values on one basis, the runs at a real river's size and the gear's holds in kg (D2-258, D2-259), milking
  and the game stocks (D2-260, D2-261), and the water fixes (W-69: sections by position and material, the gear sharing a run, the
  wear calibrated to D2-210's year). The larder is 8 days of the village's food at the new values (dried meat and roots).
- **Not yet applied:** salting at a real rate (OPEN Q-73: kept at 4 kg a unit for now); the river's level as the runs' cue
  (D2-215; the runs are on set nights here, D2-231).
- **Calibrate:** the skill values and the salt in store are first guesses.
- **Generated, not run:** a live run needs Zach's go. The first 12 live runs of the series (D2-256) take this world's low and high
  arms.
