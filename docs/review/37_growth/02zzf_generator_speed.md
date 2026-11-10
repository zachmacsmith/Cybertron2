# 02zzf: why the generator is slow, and how to make it fast

37.2, 10 Nov 2026. Zach: "Why does everything with the generator take infinite time ... I'm sure it's thrown together with a bunch of
things that could be massively optimised."

One generation of the wild region (seed 7, four villages, people on) takes about 60 s, or 108 s under the profiler. A seed the checks
refuse costs all of it, because the capacity check runs at the end. My world script then adds 30 to 60 s: the capacity ladder three
times, and an ecology built just to read the game.

## Where the time goes (cProfile, 108 s)

| What | Time | Why |
|---|---|---|
| The people tree (`engine/generate.py` `build`) | 72 s (67%) | rejection sampling: 17,110 `simulate` tries, each first deep-copying the whole tree (38 s in `copy.deepcopy`, 32 s simulating) |
| Roads (`landgen/roads.py` `dijkstra`) | 18 s | 20 shortest-path searches in pure Python over the 111,556 cells (0.9 s each) |
| Physical land (`physical.build`, flood, fbm noise, travel) | 9 s | numpy, but done twice |
| Settlement, ecology depth, economy check, lore | about 8 s | |
| **Everything above, done twice** | | `generate(people=True)` runs the whole pipeline once to count the people the tree makes, then again to size the land for them. The land, the roads and the tree are the same both times. |

## Fixes, largest first

1. **Generate the land and roads once.** Keep pass 1's land, roads and tree, and redo only the settlement's sizing in pass 2. This
   halves everything (37.2's `landgen/write.py`).
2. **Make the tree sampling cheap.** About 70 s goes here.
   - Copy only what a try changes: `simulate` adds people and events, so a try can start from a shallow copy of the people dict,
     or record what it added and undo it.
   - Stop a place's try as soon as it breaks a bound, instead of simulating to year 0 and checking at the end.
   - Use one tree for both passes (D2-161 already says the people are the same both times).

   This is 37.4's `engine/generate.py`, so it needs their agreement.
3. **Roads on a coarser grid**, or the 20 searches folded into one multi-source search. They need about 0.5 km of grain, not 150 m.
   That saves about 15 s (37.2's).
4. **Check the cheap things first:**
   - pins, then capacity on pass 1, before the people and the descriptions;
   - a refused seed then costs a few seconds, not a minute (37.2's).
5. **Try seeds in parallel** on the 4 cores, taking the first that passes (37.2's script).
6. **In the world script,** run the capacity ladder once, not three times, and build the game summary only for the chosen seed.

Expected: a seed in about 10 to 15 s, a refused seed in a few seconds, and a search over seeds about four times faster again.

## Asks

- Go-ahead for items 1 and 3 to 6, which are in 37.2's landgen and script.
- Item 2 goes to 37.4, or 37.2 builds it with their agreement.

The generator's tests (`tests/test_cybertron2_landgen.py`, 30, about 100 s) check that the worlds stay the same.
