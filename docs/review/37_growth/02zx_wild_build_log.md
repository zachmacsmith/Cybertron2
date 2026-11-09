# 02zx: the wild layer's build log (37.4 building 37.2's briefs, D2-207)

Built by 37.4 at Zach's request (9 Nov: "build the briefs now and flag other things as follow ups"), from the three briefs on main
(proposals/methods_and_encounters.md, wild_raiders_and_works.md, carcass_and_decay.md) on branches from `ecology`. This log records
what was built, every deviation from a brief with its reason, and each gate's results. Run logs stay outside the repository.

## Brief 1: methods and encounters (stages 0 and 1, pack K0). Branch `ecology-methods`.

### What was built
- `cybertron2/wild/methods.py` (new): the method rows (hunt the wild, stalk, drive, snare, net, trap in water, den work, gather young,
  pest work, break a dam, guard the field, shut), each of the engine's technique shape with `needs`, `favours`, `base` and a `note`;
  `build` generates each take method's `yield.takes` at load from the kinds' traits (kinds.TRAITS) and the kinds' `taken.calibrate`;
  familiarity by kind (`familiar`, `factor`, `raise_familiar`, `kin`, `teach_familiar`, `familiar_line`); seeding by the land
  (`seed_by_land`, with `wild.methods_known` to override).
- `wild/kinds.py`: TRAITS for the ten takeable kinds; `home` on the sites (colony, lodge); `on_crop` and the guard numbers (cut,
  days, thin, done) on the crop loads; the fox's litter on its own row (keyed to `home: den`); an eel `taken` row; four
  calibrations; SKILL_CARRY removed.
- `engine/data.py`: the 19 kind-named wild rows removed; the methods built in at load; the range and `looking for` modifiers name
  the methods.
- `engine/wild.py`: `take` reads the generated table unchanged in shape, with familiarity as a factor on a kind's weight and on the
  take chance, the method's cue rows applied only to the kinds that move on that cue, the litter from the kind's row, familiarity
  raised on a take and on a sign noticed; an unknown target refused ("you know of no beast called that"); `den_work` (a lodge's
  trap, else a take), `young` (whichever colony is at the parcel), `pest` (the pest named, else the worst that harms), `pick_scare`
  (the scare named, else the first one has); expert readings of a kind gated by familiarity with it (`familiar:<kind>`).
- `engine/verbs.py`: dispatch of the three new yield kinds; in a wild world a refusal does not list the catalogue.
- `engine/prompt.py`: a method's note in the system text (what it is, its gear and place; no multipliers, no kinds); the
  familiarity line in "What you know how to do". `engine/perceive.py`: `familiar:<kind>` in what one reads by.
  `engine/settle.py`: teaching a method passes on familiarity. `c2viz/js/vocab.js`: poses for the new names.
- Tests: tests/test_cybertron2_wild_methods.py (the gate's guard and unit tests); tests/test_cybertron2_wild.py amended for the
  renames (and two tests for intended changes, below).

### Deviations, with reasons (defaults taken: OPEN Q-36)
1. **Two keys differ from the brief's names.** `hunt` is already the key of the hunt in worlds without the wild pack (off with it),
   which older worlds still read, so the wild hunt keeps its key `hunt the wild` (alias `hunt`). `guard` is a verb (standing guard
   over a building at night), so the method is `guard the field` (alias `guard`).
2. **Familiarity lives in the person's mind store, not the know store.** Seven loops over the know store (crafts lines, labour's
   fading, life's inheritance, here, the mason rule, perceive, capacity levels) assume every entry is a technique; the mind store
   already holds free records (`found`).
3. **hunt needs `water: false` and favours `runs` (x3, base 0.33).** With the brief's rule alone the hunt took eels and wildfowl,
   and woodpigeons came out at 2 to 3.5 times their old share (the old table weighted pigeons and bears 0.1 to 0.3); beasts that
   keep to runs reproduce the old weights without naming a kind.
4. **Familiarity carries by sort, not by the method's needed traits.** The brief's two examples (red deer to roe; hares not to
   foxes) cannot both hold by needed traits: red deer and roe differ in size as hares and foxes do. A shared particular sort in
   `taken.family` (deer; not the generic game, big game, small game, birds, vermin) gives both.
5. **stalk needs `home: none` and has no solitary favour.** The brief's rule let the stalk take foxes; you stalk beasts that lie
   out, not den animals. The x1.5 for solitary beasts halved red deer's share (0.28 to 0.15).
6. **Five calibrations** (one a kind, each with a comment on the kind's row): red deer x0.15 for the drive (deer break back through
   the beaters), roe x0.03 for the snare, woodpigeon x0.1 for the net, wildfowl x0.1 for a trap in water, wild boar x0.12 for the
   stalk.
7. **Eels give food.** The eel had no `taken` row, so an eel trap's take gave nothing; it now gives 0.1 meat a lift (calibrate).
8. **Units:** gather young 1 (the heronry's was 2), pest work 1 (picking slugs was 2).
9. **The refusal without the catalogue only in worlds with the wild pack**, so older worlds' text is unchanged.
10. **A method's cue rows** (`when`) carry `for: {trait}` and apply to the kinds with it (an eel night does not double wildfowl).
11. **break a dam** is known with den work where the village has a lodge (the brief names it in the table but not in §6).
12. **A guard with nothing to scare them with is refused**; one naming a scare it lacks is told what it needs.
13. **The bot regression cannot test the methods' shares**: the scripted bots only hunt with `hunt the wild`. The shares were
    measured by a harness (scratchpad, outside the repository): every method tried by up to 12 villagers at a fitting parcel of each
    village on every day of a year, from fresh copies of the world, on the old code and the new.
14. **Familiarity's numbers** (calibrate): its factor 0.35 (the brief's 0.5 put wild food 30 to 50% over before); starting
    familiarity youth 0.3, adult 0.35, elder 0.5 (within the brief's 0.3 to 0.6).
15. **A bug found and fixed outside the brief:** `knowledge.options` offered crew work to everyone without checking its pack, so in
    worlds without the wild pack the bots tried a `drive`; crew work is now offered only in its pack's worlds.
16. **Two existing tests changed for intended effects**: a reader who "knows nothing" is now raised to the methods their land
    holds (so the test sets `methods_known: {}`); an expert hunter's readings of a kind now come from familiarity with it.

### Gate results (9 Nov)

- **Tests:** 478 pass on the branch (the 467 before, amended only for renames and the two intended effects above; brief 1's 7 new;
  the capacity model's guard of yield kinds, which caught the three new ones until they were placed).
- **Older worlds replay exactly:** bot runs of the valley and Region C (no wild pack), 10 days, are identical to the branch before
  the build. A wild world run twice is identical.
- **Take shares** (the harness, the share of each kind among takes, old technique against its method; up to 12 villagers a village
  a day for a year): within about a third in every cell but one. Stalk in run 5's world: red deer 0.16 against 0.28 before, with
  the same weights as the old table (red deer and roe 2.5 each): a different random stream (the draws are keyed by the technique's
  name), within run 6's world's target.

  | Method (old) | run 5's world: takes, food | run 6's world: takes, food |
  |---|---|---|
  | hunt the wild | 84 to 103, x1.16 | 131 to 146, x1.42 |
  | stalk (stalk deer) | 72 to 92, x1.08 | 86 to 84, x0.90 |
  | drive (boar hunt) | 15 to 36, x2.40 | 15 to 15, x1.00 |
  | snare (snare hares) | 209 to 240, x1.18 | 434 to 479, x1.10 |
  | net (fowling) | 235 to 256, x1.08 | 198 to 229, x1.16 |
  | trap in water (set eel traps) | no water | 100 to 184, food 0 to 18 (the eel fix) |
  | den work (dig out the fox earth) | 42 to 58 | 101 to 121 |
- **Food from wild takes:** within about a third but three cells: hunt in run 6's world (x1.42: more deer in the mix), and the
  drive in run 5's (x2.40, 15 to 36 takes). The drive's rise is **not explained**: not the crew flag, not wolves, not familiarity
  (with it off, 29 takes), with the same weights as before; run 6's world shows none. Left open.
- **The bot regression** cannot measure wild food: the scripted bots hunted 2 or 3 times in 8 days and took nothing, before and
  after. The harness is the measure.
- **The report to Zach:** in conversation, 9 Nov.
