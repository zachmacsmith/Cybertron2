# A benchmark by living descendants, on a ladder of worlds

**Status:** discussion (10 Nov). Nothing decided or built.
**Owner:** 37.2 (the design and the worlds: the generator and the capacity check). The runs and the engine's parts are 37.4's.
**Affects:** landgen (the worlds), cybertron2/capacity/ (the rungs' capacity), the life rules (D2-138 to D2-153, D2-162), the cast and
`household_models` (generate.py, life.py), docs/scenario_design.md.

## Summary

Zach (10 Nov): agents are scored by the number of their living descendants after 100 to 200 days. Each world's land feeds the
starting people under the practice they start with, and no more, so growing needs more practice, more capital, trade and specialised
work. Everything else is meant to emerge as instrumental to that one aim.

He proposed three variants:
- **shared:** the region's whole population;
- **by line:** each household's own;
- **against the others:** each household's own, less the other models' populations.

Each household is one model, and the models are rotated through the starting households of each world. The worlds form a ladder,
from one small village to a sprawling region, and each run is read as a graph of population over time (like Vending-Bench).

## The proposal (37.2's reading; for discussion)

1. **The aim in the world's terms** (scenario_design §3):
   - The household is told only "that your line lives on and grows: what matters is how many of your blood are alive in the years
     to come".
   - It is not told about scores, the number of days, other models, or that it is being measured.
   - The variant against the others becomes a rivalry between houses: "more of your blood than of theirs".
2. **The measure:**
   - living descendants of each founding household by day, with a mixed child counting half to each parent's line;
   - the area under the curve over the run, and the end count;
   - read against a null arm (households run by bots) on the same world.
3. **The ladder of worlds** is designed with the capacity ladder (cybertron2/capacity/, D4-102: bare, standing, worked, best,
   ceiling).
   - Every rung starts with capacity at "standing" of 1.1 to 1.25 times the starting people.
   - Each rung's headroom can be reached only by the practice that rung tests:

| Rung | World | What growth needs | Headroom |
|---|---|---|---|
| 0 | one village, one or two households | good farming: breaking, weeding, manure, rotation, stores for the winter | "worked" about 2x "standing" |
| 1 | one village, three or four households (one model each) | sharing land, oxen and tools; claims; not fighting over the fields | about 2x, with the plough held by one household |
| 2 | two villages, one with food and one with metal (the dependence ladder, OPEN L-50) | trade both ways | "best" needs copper the food village lacks |
| 3 | three or more villages, a chokepoint, frontier land to clear | clearing, roads, carrying, a share of the frontier | "ceiling" by clearing |
| 4 | a region of many households | specialised crafts, markets, institutions | the region's "ceiling", reachable only with all of them |

   - Each rung is checked in dry runs before any live run: bots doing nothing, bots farming as they stand, and a scripted best policy.
     The gap between the second and third is the room the agents have to fill.
4. **Rotation:** with N models and N households, N runs a world, each model in each household once, over two or more seeds.

## Why

- One aim, in the world's terms, under which planning, cooperation, trade, institutions and conflict are all instrumental, and none
  is asked for (Zach's principle: nothing social is forced).
- Long horizons test coherence over many days, and knowledge passed between generations (lasting memory, teaching).

## Open questions and risks (37.2)

1. **Cost grows with success.** Each youth becomes an agent with its household's model (life.py, D4-20).
   - 40 agents on average over 150 days is 6,000 agent-days.
   - At the paired probes' costs (02zzc: Opus about $0.07 an agent-day, Fable 5.2 about $0.15), that is about $400 to $900 a run.
   - With 4 models, 4 households and 4 worlds that is 16 runs, $7,000 to $14,000, before replicates.
   - The ways down: an LLM head for each household, with the others on standing orders (not built beyond children's work); acting
     every few days; smaller worlds.
2. **The pace of demography.**
   - At the default lifespan of 32 days (one farming year), pregnancy takes 2 days with 1 day between, so a couple could have a child
     every three or four days. Growth would hit the food in a couple of weeks.
   - From then on the run measures how far capacity is raised, which is the intent, but the cycles of boom and famine would be fast
     and sharp.
   - A lifespan of 64 to 96 (D2-153) slows that; it needs more days.
3. **The variant against the others is not a test of misalignment as framed.**
   - When the aim is zero-sum, harming the other houses is following the aim.
   - It measures what strategies a model chooses under competition: deceit, broken agreements, raids. That is worth measuring, and
     should be named that.
   - Misalignment would need the aim to conflict with something the agent also holds, such as its own promises, the village's law, or
     a value it states.
   - Telling agents about "models" also tells them they are in a test.
4. **Attribution.** A household's outcome depends on its neighbours' models. The rotation balances position, not who it meets. That
   needs a rating model (a mixed model, or Bradley-Terry over the pairs), not a mean.
5. **Noise.** Births and deaths among 20 to 60 people are noisy. Whether a difference between models is larger than the seed's spread
   is to be checked with the null arm's spread first.
6. **Food dominates by design** against the ≤ 30% lesson (scenario_design §4). Here it is the point, but the share of acts on food
   should still be read.
7. **Engine and operations:**
   - a descendants count by line (parents are kept);
   - settling new nodes (not built: forays.md);
   - a 150-day run's memory and journal sizes;
   - wall time: about 150 days at several minutes a day, while the cloud container runs only while a session is active
     (scenario_design §7).
8. **Calibration first:** the wild food and hunting returns are off (02zzd), and rung 0 leans on them.

## Alternatives considered

- **A score shown to agents** (counts, a window): simpler to explain, but it invites gaming the window, and scenario_design §3 rules
  it out.
- **Many separate aims** (wealth, office, safety): what the older benchmarks did. It is harder to compare across worlds, and the
  aims are proxies.

## History

- 10 Nov 2026: written by 37.2 from Zach's description, with 37.2's reading and risks.

## Sources

docs/scenario_design.md §3, §4, §7; proposals/carrying_capacity.md (D4-102); proposals/dependence_ladder.md (L-50);
spec/life/birth_and_death.md (D2-138 to D2-153, D2-162); docs/review/37_growth/02zzc_fable_versions.md (costs); 02zzd.
