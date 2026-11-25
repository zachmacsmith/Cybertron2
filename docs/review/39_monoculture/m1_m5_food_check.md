# Fallowmere (M1) and the Scattering (M5): food, gaps and fixes (25 Nov)

Session bench, W-203. From the engine's capacity model (`cybertron2/capacity`, `analyse(..., horizon=64)`; raw:
`/home/user/mono1/capacity_m{1,5}_h64.json`), the gate's report (`specs/mono/m{1,5}.check.json`) and the world files
(`specs/mono/m1.yaml` rebuilt 25 Nov with households matched to land, `m5.yaml`). World 0b's Highpool, for scale: 0 people
supported at any level, stores to day 19 (Q-222).

## 1. Capacity, home by home

People a home's own land feeds for good (the year simulated five times); "standing" is the fields as they are, little work;
"worked" is good farming (soil broken, weeded, manured, meal ground, bins). The 64-day horizon starts from the stores.

| Home (households) | People | Standing | Worked | Labour at worked | Stores (days) | 64 days, standing | 64 days, worked |
|---|---|---|---|---|---|---|---|
| Fallowmere (Ashby, Reeve, Colle) | 12 | 7.7 (0.64×) | 37.7 (3.2×) | 13% | 12.7 | no shortage | no shortage |
| Holtmouth (Strand) | 4 | 2.3 (0.57×) | 11.3 (2.8×) | 8% | 16.4 | short from day 47, 17 days | no shortage |
| Highcairn (Fell) | 4 | 7.6 (1.9×) | 14.2 (3.5×) | 10% | 27.1 | none | none |
| Lowbury (Meade) | 4 | 10.7 (2.7×) | 31.2 (7.8×) | 9% | 12.4 | short days 0 to 4 | short days 0 to 4 |
| Hartsmoot (Holt) | 4 | 8.4 (2.1×) | 17.3 (4.3×) | 10% | 20.8 | none | none |
| M1 region | 12 | 21.8 | 59.8 | | | | |
| M5 region | 16 | 54.6 | 99.2 | | | | |

Room to grow: at "best" (every technique) the M1 region feeds 91.5 and M5 136.4, 7.6× and 8.5× the founders. Firewood: cut,
every home has 5× to 15× its need; gathered only, Fallowmere has 1.1×.

Reading: food is enough and binds without dominating. Fallowmere and Holtmouth starve in the long run at little work and thrive
at good work, so effort decides; no home needs another to live. Lowbury's short days 0 to 4 are seed held back (4 plots want 64
seed; the store has 51 grain), the seed-or-eat choice (L-185) in its plainest form.

## 2. Gaps, in order

**Blocking (fix before any run):**
1. **Fallowmere has no water.** The design's river runs Hollins, Fallowmere, The Ford, Broadwater, Kingsmead, Eastmarch; the
   built river begins at Kingsmead. Not a food fault (Fallowmere feeds itself without fish), a design one.
2. **Holtmouth has no sea and no salt pan.** The Strands hold 12 wicker traps, 2 hand lines and the salters' crafts; the generator
   names Holtmouth "a clay vale". Their livelihood cannot be worked: they live off 2 plots of barley and a herd.
3. **Households hold land and beasts they cannot work** (one generator template for every household: field 2, meadow 1, pasture 2,
   forest 1, fen 2; 2 cows, 2 oxen, 1 bull):
   - the Holts (hunters) hold a field and a full herd and know no sowing, reaping, herding or milking;
   - the Strands (fishers) and the Fells (herders, smiths) hold fields and know no farming;
   - the herders (Fell) have no more stock than anyone; Fallowmere's dairy household (Reeve) has 2 cows and no bull, so no calves;
   - the hunters' home has one plot of wood with game at K 1 (the world's game, K 660, is elsewhere: a roaming life, if intended).
4. **The start**: every field stands in barley ripe on day 5 (48 a plot), on top of 16 days of stores sized for a harvest about day
   16 to 20; the maker's store reset wipes next year's seed (Q-220).
5. **Vermin**: 394 rats a km² at Fallowmere's homes (the illness term saturates at 120); Emma dies on night 1 in every arm (stable).

**Lesser:**
6. Tools: a crude tool lasts 10 uses; stone comes from hoeing and ploughing (fieldstone) or the rock a day or more away (M4 warns
   for every non-farming household; P11: stone and copper made by none in reach in M1). A 200-day pull to explore, or a slow
   collapse of the households that do not farm.
7. Fields: 7 plots in all of M1's world, 10 in M5's; growth means clearing pasture (Ashby and Meade know clear and plough).
8. The gate's M3 warns of 12 to 18 wicker traps wanted "by the first run in 0 days" for households with no water and no fishing:
   to read (template noise, or a run in reach).
9. P7: crafts held at capable with no lesson rows, whose failures say only "your hands" (the interface fault sent to 37.2).

## 3. Fixes (W-203)

- The design check in `make_mono_worlds.py`: refuse a build unless each home has the water its design names; each livelihood the
  land, beasts and buildings it works (herders the most stock and a bull, fishers water, salters a pan, hunters wood with game);
  each home feeds itself at worked 1.2× or better; the first harvest and seed as designed; no founder lost to a fixed draw before
  day 1.
- Land and herds by livelihood, after matching (the farmer to the fields, already done).
- Q-220's start (default: bare fields, 16 days of food, next year's seed in store).
- Vermin at the homes to the illness term's range.
- The water: find where the generator loses the river at Fallowmere and the sea at Holtmouth (the generator's owner), not patch
  around it.
- Then rebuild both on main's engine (after the World 0b reruns end) and run this check again.

## 4. For the prompt comparison

A before-and-after comparison of the prompt can only be read on World 0b as it stands (the broken prompt's runs are there), and
its population is decided by Highpool's winter (Q-222); its behaviour measures are the comparison. Fallowmere, once fixed, is the
better world for any later comparison: its outcome turns on effort (0.64× at little work, 3.2× at good work), not one dependence.
