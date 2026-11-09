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

## Brief 2: raiders and works (stages 2 and 3, pack K1). Branch `ecology-raiders` (from `ecology-methods`).

### What was built
- **Displacement** (`engine/wild._groups`): a group whose row has `displace` (boar, red deer) and is turned at its target (watched,
  fenced, scared) tries the nearest unwatched target by the layout's steps the same night; a group without it rests.
- **The lapse probe:** a row with `probe: k` (the fox, 3) tries up to k buildings in order, the one it remembers first, and raids the
  first it can get into.
- **The woodpigeon flock** in the raid loop by a `flock` key; `pick: most` sends it to the field with most crop; it habituates like
  the other raiders and lands where it fed.
- **Set works:** methods with `set` (snare, trap in water) leave a `set` thing on the parcel (things.KINDS, schema v7) that catches each
  night by the take rule with nobody there, holds its catch, can be found and robbed (the setter is told by an event), and is
  sprung after its life (snare 4 nights, trap in water 8).
- **Bodies and gaps:** `kinds.BODY` {gap, climbs} by kind; `kinds.GAPS` by building material (wattle and timber small, stone tiny,
  damaged one size larger); `gaps_pass`; small kinds pass any fence. The raid's door rule: a kind that passes the building's gaps
  gets in 0.9, else 0.02 shut and 0.6 open.
- **Stores by kind:** the ecology reports what each kind ate from the stores (`eaten_by`); `_stores` takes {kind: share} and
  `kinds.STORE_STOPS` stops each by body: granary (climbers and the tiny, keep 0.3), bins (the tiny, 0.5), dog (all, 0.5), cat (the
  tiny, 0.4, a beast in the store), owl (the tiny, 0.6, an occupied owl hole).
- **K1:** the stoat (kind, traits, a taken row, a near-people row; through wattle at the hen house); the cat (`kinds.CAT`: settles by
  itself at a store with mice and no dog, at a season's turn; a stray can be found on a hunt; item `cat`); the owl hole (fitting;
  `kinds.OWL`: a barn owl takes an empty one in spring in a building nobody sleeps in, recorded in `wild.nests`); moles (a load that
  harms grass through `harm_res`); leatherjackets (a load on field and pasture; a rookery works it off within reach through
  `site_eats`); the markers' sowing sayings (blackthorn, cuckoo: `times` and `say` from the families' lore, shown when the lore's
  window holds the half-season); cattle gadding in heat (`herds.gadding`, HERDS `gad`: over 22 degrees and little wind, a herd
  goes through a fence with odds 0.7 of the fence's).
- Tests: `tests/test_cybertron2_wild_raiders.py` (13: the units of §7 and the two society-level tests).

### Deviations from the brief
1. **Pigeons join the raid loop by a `flock` key**, not by becoming a whole-counted kind: their numbers stay density-counted in the
   ecology; the flock's size is read from the density at the target.
2. **The woodpigeon's diet share of crops is halved** (3 to 1.5), so the flock's raids replace part of its diffuse grazing rather
   than adding to it. The regression shows the diffuse crop loss fell only 1.7%, so the raids are mostly additive (below).
3. **Store losses go by kind** through a new ecology output, `eaten_by` (the brief names stops by property, not how the ecology
   says who ate what).
4. **Bins now stop the tiny kinds** (keep 0.5). Before, `STORE_KEEP` had only the dog and the granary, so bins did nothing; the
   generated villages have bins in most houses, so their store losses halve (below). `STORE_KEEP` is removed.
5. **Set things are marked sprung, not removed**, and there is no lifting act: a sprung snare stays as a thing until it decays.
6. **The cat lives as goods in the store** (item `cat`), not as a herd or a person; it is moved or traded as goods.
7. **Owls are recorded in `wild.nests`** by building, not as a site.
8. **Damaged houses let foxes in** (damaged is one gap size larger), so the existing fox test now keeps its houses at condition 2,
   and sets stoats to 0 (a stoat gets through shut wattle).
9. **The load is named `leatherjackets`**, not the brief's `grubs`: `grubs` already names the ladybirds' larvae. The old alias
   "clear the grubs off the beans" no longer targets ladybirds unless they are named.
10. **Moles harm the grass's stock**, not the hay cut itself; the cut follows from the stock.
11. **World schema v7** (containers gain `set`).
12. **Work on the ground named by a building** (found running 37.2's T2): `shut at Holt House` was refused ("done at the Green").
    Now a building named as `at` for work done on parcels means the parcel the building stands on. This is general, not only for
    `shut`.
13. **Two rules for the scripted bots, for dry tests** (found running T1):
    - With the world key `bot_reap: "ripe"`, bots reap only when some field at their place is ripe. The bots reaped green corn
      from day 1, so Meadcombe had no standing crop for raiders by night 4.
    - A person with scripted acts that day no longer travels by the bot's plan. Thomasin left on day 1, so her watch lapsed.
    Worlds without a script or the key are unchanged.
14. **The fox's probe records the houses it tried**, up to the one it got into, not all three.
15. **A set's life is on the day clock** (`clocks.RATES`).
16. **Brief 1's seeding tightened** (found running T7). A household now knows a method its land holds only if both hold:
    - one of the method's main kinds is about (at least half its largest weight);
    - the village has ground of a kind the method is worked on.
    Before, any kind in the table counted, so a net's side weight on pigeons made every village know netting, and eels in the ring
    made a village with no water know eel traps.
17. **Pest work picks a pest of the ground worked** (found running T8). On a meadow that means the moles; on a field, the pests of
    its crop. Before, it chose only among crop pests, so moles were never worked. The mole guard now kills some moles (`thin` 0.3,
    calibrate). A load thinned on a parcel is reckoned against the village's ground of that cover, not its fields.
18. **Gadding at 18 degrees, still and dry** (calibrate; was 22). Found running T6: this climate's summer never reached 22.

### Gate results (9 Nov)
- **Tests:** 491 pass on the branch (`f290e2c`): brief 1's 478, brief 2's 13, two existing tests isolated (stoats; sound houses), the
  method-knowledge test changed to deviation 16's rule, and the clocks guard (deviation 15).
- **Older worlds replay exactly:** bot runs of the valley and Region C (no wild pack), 10 days, have the same state and days as
  brief 1's tip, apart from the schema number.
- **Guard:** no kind name in rule code (the guard test; `_cats_and_owls` was renamed `_store_beasts` and the names moved into
  `kinds.CAT` and `kinds.OWL`). The one new sign, the sowing saying, is appended to a marker sign that is already a change (the
  blackthorn flowering, the cuckoo heard), grounded in the families' lore and worth acting on (it says when to sow).
- **Regression** (wild_probe5 and wild_probe6, scripted bots, 8 days, seeds 7, 8, 9; brief 1's tip against brief 2):

  | Loss (6 runs) | before | after | |
  |---|---|---|---|
  | crops eaten (diffuse) | 75.8 | 74.5 | x0.98 |
  | stores eaten | 27.3 | 13.1 | x0.48: bins now stop the tiny (deviation 4) |
  | crop lost to raids | 19.9 | 49.6 | red deer 19.9 to 19.6; woodpigeon 0 to 30.0 (meant: pigeons answerable) |
  | other takes from buildings | 8.7 | 8.7 | x1.00 |
  | loads (slugs, aphids; moles and leatherjackets new) | 9.7 | 13.2 | moles 3.6 new |
  | **all food lost** | **141.4** | **159.1** | **x1.13** |
  | hens taken | 24 | 48 | fox 24 to 44 (the probe), stoat 4 (new) |
  | beasts killed | 2 | 2 | |

  The total is within a third. Three parts move by more, each where the brief means them to: the pigeons' raids, the fox's probe
  and the stoat. Boar losses were 0 before and after: the bots' worlds give the boar no raid in 8 days, so its move to target is
  not tested here.
- **Society-level** (dry, scripted): a watched field sends the boar's loss to the next field (field B loses more with A watched
  than with neither); one lax house draws the fox to its neighbours (the other houses lose at least as many hens over 30 nights).
  Both pass.
- **Open for Zach:** (a) the fox's hens nearly double with the probe (1.8 to 3.4 a visit where the bots leave hens out); (b) the
  pigeons' raids are mostly added to their grazing, not taken from it; (c) bins halving store losses in every generated village.
  All three are calibration; built as the brief says.

### 37.2's dry test arms (02zy), 9 Nov

These are 61 dry runs: 20 arms plus one mirror arm, on seeds 7, 8 and 9 (T8 on 7 and 9). Scripted acts were done first; everyone else
was a bot. Run logs and the reader are outside the repository. Each arm is read against its control.

**Running them needed changes to the worlds,** made in the runner's copy and not in `make_wild_tests.py`:
- Every world has `bot_reap: "ripe"`.
- T1: East Field is sown like Middle Field (it is generated fallow), and both ripen after the test (generated: day 5).
- T2 and T3: night breaks are off, since they test sound houses (see below).
- T5: the cat is goods in Carter House's store, not a fitting.
- A mirror arm, `watch_east`, was added.

| Test | Read | Result |
|---|---|---|
| T1 displacement | Middle Field watched: East Field's loss (seeds 7, 8, 9) | 2.5, 33.5, 29.7, against 0, 0, 7.6 unwatched; each turned raid went to East the same night. **Pass** |
| | both watched | both lose less than unwatched (Middle 3.7, 0, 0 against 6.0, 33.5, 23.2). **Pass** |
| T2 lapse probe | Meadcombe's three houses: hens lost | all shut 0, 0, 0; one lax: the Carters 4, 6, 2 and the others 0; none shut 12, 6, 2. **Pass** |
| | neighbours of the lax house tried more often | **Not shown**: they are tried less (1, 0, 1 against 2, 1, 2), because the fox, fed at the lax house, goes back to it first. Their loss is 0 either way |
| T3 gaps | fox at shut sound houses | kept out of every one. **Pass** |
| | damaged Holt House, shut | the fox gets in on every seed (6 hens each). **Pass** |
| | stoat through wattle, not stone | **Not tested**: no stoat group went for Meadcombe; the one at Brookford took 2 hens at Moor House, which was not shut |
| | rats and mice | into every house. **Pass** |
| T4 set works | catch with nobody there; the catch waits | yes (snares 1 hare in 12 snare-nights; eel traps 4 to 7 catches in 8 nights). **Pass** |
| | robbed | Osric takes the hare from Thomasin's snare, with an event that concerns Thomasin; she finds it empty the next day. **Pass** |
| | unchecked | catches spoil in the set (0.07 to 0.23). **Pass** |
| | ends after its life | sprung after 4 nights (snares) and 8 (traps). **Pass** |
| T5 stores | each kept store loses less | Wood House with a granary 0.29, 0.22, 0.18 against 0.95, 0.72, 0.58; Carter House with a cat 0.19, 0.24, 0.25 against 0.23, 0.43, 0.50. **Pass** |
| | a cat settles by itself | yes, at 3 of 6 stores on the first season's turn, on every seed (settle_p 0.25 each: more than expected; to check) |
| | owl takes the hole | **Not testable**: the owl takes one only in spring, and T5 runs from summer into autumn |
| T6 summer | cattle gadding | seed 9 only (the only warm still days): the Holt herd gads on Cow Close 3 days, goes through into Middle Field and East Field and tramples 10.6 of the corn; herded, it does not; the Leaze herds never gad. **Pass**, after the threshold change (deviation 18) |
| | boar at the corn | **Not testable**: no boar group near either village (this land holds them only by the wild node) |
| T7 methods | familiarity rises | Petronel's with red and roe deer rises from 0.35 to 0.41 to 0.44. **Pass** |
| | who knows what | Brookford's households know `trap in water` and Meadcombe's do not; nobody knows `net` (no wildfowl in this land). **Pass**, after deviation 16 |
| | takes | none in 8 days for Petronel (stalk), Alys (net) or Denise (who sets snares and never checks them); Petronel's stalk fails on the days the bot also speaks (4 units with 3 left) |
| | taught | **Not tested**: Petronel never sets time aside to learn, so the teaching does not happen |
| | system text | no kind table or tool multiplier in any prompt. **Pass** |
| T8 soil | moles worked | Leven Meadow's mole harm 0.16 and 0.09 left, 0 worked; Brookford's mole level 0.66 and 0.62 left, 0.51 and 0.60 worked. **Pass**, after deviation 17 |
| | the rooks' grubs | **Not testable**: autumn rooks have no young to take and fed on no grubs |
| | marker sayings | **Not testable**: the markers (blackthorn, cuckoo) are spring signs |

**Found by the arms, for Zach:**
1. **Houses break fast.** D2-168's breaks (proposed) run at 0.02 a night, or 0.08 on a cold night, times 1.5 for wattle. In a frosty
   spring that is 0.12 a night, so most houses are damaged within a week. With brief 2's gap rule a damaged wattle house lets the
   fox in even when shut, so in the generated village shutting up protects only until the house breaks. The arms ran with breaks
   off. Either a damaged house should not always have a fox-sized hole, or breaks should be rarer. Either way it puts mending in
   the hen's way, which may be wanted.
2. **Hunting yields little per day.** In 8 days no scripted hunter took anything, which is consistent with brief 1's tables:
   about one take in ten stalking days.
3. **Cats come quickly**: half the stores at the first season's turn.
