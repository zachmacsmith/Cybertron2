# The hunt over time, and what briefs 1 to 3 left: build brief 4

**Status:** being built (10 Nov) by 37.4 on `ecology-calibrate` (WORK W-27), on Zach's go ("Build the new brief", relayed by 37.4); its open questions take the brief's defaults until Zach says otherwise. No DECISIONS row yet: for Zach to confirm. **Build brief 4** for the wild layer. It covers:
- the hunt's calibration measured in 02zzd;
- the fixes the gates of briefs 2 and 3 found (OPEN Q-37, Q-38);
- preservation at the new scale of meat.

It starts from brief 3's branch (`ecology-carcass`, `cc4d342`).

**Not in this brief:** forays. They were split off as their own track (Zach, 10 Nov), with a route module over the land that the
world now keeps (D2-208, [land_kept.md](land_kept.md)); see [forays.md](forays.md) and OPEN L-105.

Stages B and C need two of 37.2's proposals accepted: [shelter_damage.md](shelter_damage.md) and [cats.md](cats.md) (OPEN Q-37 a
and d). Zach's go on this brief accepts them as far as written here.

**Owner:** 37.2 (author; the wild pack's data, `engine/wild.py`, the ecology). Night breaks, buildings, recipes and the manual are
37.4's (§6).

**Affects:** spec/environment/wildlife.md; spec/economy/buildings.md and lodging.md (D2-168, D2-68); spec/economy/production.md
(drying); on the branch: `engine/wild.py`, `engine/night.py`, `engine/data.py`, `engine/knowledge.py`, `wild/kinds.py`,
`wild/ecology.py`.

## Summary

Briefs 1 to 3 built the wild layer's core. Measuring it in generated worlds (02zzd) and running its gates (02zx) found five kinds of
problem:
- **The hunt cannot pay as agreed.**
  - A trip meets at most one beast, and its time never counts.
  - The range only adds units.
  - The meat is 3 to 5 times small against the engine's own cow.
  - A master succeeds three times in four.
  - One hunter empties a 19 km² wood of roe in two weeks.
- **Houses break too fast for shutting to matter.** A wattle house breaks with 0.12 a frosty night, and a damaged one always lets
  the fox in.
- **Cats** settle at half the stores at once.
- **A left carcass lowers a herd's losses** instead of raising them.
- **The carrion pool** barely registers a carcass.

This brief puts those right. It also makes preservation work at the scale a deer now gives: with 20 meat spoiling at 0.3 a night,
and drying taking a unit for each 2 meat, a deer is mostly wasted.

## 1. For the builder

**This file holds for this brief.** Read:
- briefs 1 to 3 and their tests;
- 02zzd and its harness (`docs/review/37_growth/02zzd_ev/`);
- 02zx's gates;
- [shelter_damage.md](shelter_damage.md) §1 to §3 and [cats.md](cats.md) §3;
- on branch `ecology-carcass`:
  - `engine/wild.py`: `take`, `_reach`, `_groups`, the raid loop, `_set_night`;
  - `wild/ecology.py`: the pressure step, `carrion`;
  - `wild/kinds.py`: `HUNTED`, `WHEN`, `NEAR_PEOPLE`, `STORE_KEEP`, `GAPS`;
  - `engine/knowledge.py`: `SKILL`, `curve`;
  - `engine/data.py`:
    - TECHNIQUES `stalk`, `hunt the wild`, `drive`, `snare`, `trap in water`, `dry meat`, `salt fish`;
    - ITEMS `meat`, `dried meat`;
    - `carry`;
    - `PHYSICS["breaks"]`;
  - `engine/night.py`: breaks and spoilage;
  - `world.CONDITION`.

**Do not:**
- name kinds in rule code;
- add a decay or damage system beside the existing ones;
- cap signs.

Dry runs only.

**Branch:** `ecology-calibrate`, from `ecology-carcass`. **Order:** stages A to D. The gate is at the end, with stage A's own check
first.

## 2. Stage A: the take as a search over time (`engine/wild.py` `take`)

1. **Search and travel.**
   - A take's units are split: the range's units are travel, the method's units are search.
2. **Ground covered.**
   - Search units times the method's `sweep`, a new TECHNIQUES property in km² a unit: about 0.4 for `stalk`, 1.0 for `hunt the
     wild`, 2.0 for a `drive` with its crew; calibrate.
   - The ground is spent in the farthest area the range reaches (home for `near`, the ring for `the wood around`, the bordering
     wild areas for `far`). The areas crossed on the way are passed at a fifth of the rate.
3. **Meetings.**
   - The number met is drawn from Poisson(λ). λ is the sum, over kinds and the areas searched, of:
     density (heads a km²) x `detect` x the kind's WHEN detect x the method's weight x focus x familiarity
     / (1 + 0.5 x min(4, pressure)) x the ground in that area x `meet`.
   - `meet` is one constant; calibrate.
   - Meetings are taken in order. Each is drawn as now: danger first, then the kill at
     `take_k x skill x weapon x (1 - flee) x familiarity`. `take_k` is a new constant replacing 0.55, about 0.19; calibrate.
   - A wounded beast lying up is kept as now.
4. **The carry limit.**
   - After a kill, the trip goes on only while the hunter can carry more: goods' weights against `carry` (on foot 10, with a pack
     20).
   - What cannot be carried is cut and left. It goes into the area's carrion pool, or is a carcass thing at the parcel when it was
     hunted `near` (brief 3).
   - A red deer ends a lone trip; a crew carries more.
5. **Meat on the cow's scale.**
   - In RESOURCES `taken.goods`, with a slaughtered cow at 40 meat (about 3 kg a meat):
     - red deer 20, roe 4.5, boar 15, the bear 40;
     - hare 0.7, mallard 0.3, woodpigeon 0.1, eel 0.2.
   - Hides as now. Calibrate within a fifth.
6. **A hard skill curve.**
   - `SKILL["hard"] = [0.4, 3.0]`, with its own `tau` about three times the trade's.
   - TECHNIQUES `curve: "hard"` on `stalk`, `hunt the wild` and `drive`. `knowledge.curve` reads it.
7. **Seasons through finding** (data rows, calibrate):
   - snow lying: deer and boar detect x1.5;
   - summer leaf: deer detect x0.8;
   - the rut as built.
8. **Pressure by ground** (37.2's ecology).
   - A take adds `HUNTED["hunt"] x min(1, ground in the area / the area's km²) x the crew factor` to each area searched.
   - The flee shares are lowered so that one hunter stalking daily moves 1 to 2% of a 19 km² ring's roe a night.
9. **Game near people** (37.2's ecology).
   - The shy kinds' density on a village's home area is lowered by people's presence: deer and boar by `NEAR_PEOPLE`, a factor of
     about 0.3; calibrate.
10. **Snare lines and the eel run.**
    - `snare` sets a line (`line: 5`), each snare a set thing drawing by the take rule.
    - Find why the eel run's x2 and x3 `when` rows barely show in a set trap's nightly draw (02zzd: 0.09 in autumn against 0.08), and
      fix it.
11. **Stage A's check:** rerun 02zzd's harness against §7's table before going on to stage B.

## 3. Stage B: shelter in levels ([shelter_damage.md](shelter_damage.md) §1 to §3; Q-37 a)

1. **Five levels** in place of three: sound, worn, gappy, holed, failing; then ruined.
   - Each level sets warmth (-0, -10, -20, -40%, as outdoors), the store's damp (spoilage x1, x1, x1.5, x3, as outdoors), and the
     gaps it leaves when shut (`wild.GAPS`):
     - as built through worn;
     - one size larger when gappy;
     - large (the fox, a dog) when holed;
     - anything when failing.
   - The present `condition` 2, 1, 0 maps to sound, holed and ruined; old worlds behave as now.
2. **Minor wear and serious damage**, two chances a night by structure (shelter_damage §2's table of base rates).
   - Each is multiplied by the night's weather at the node (the climate's values, D4-109): frost, heavy rain, strong wind, gale or
     storm, snow, flood, and "left unmended".
   - Wind and storms raise serious damage most.
   - Minor wear takes one level. Serious damage takes as many as its cause is severe (§2's odds by structure), so a gale can flatten
     wattle.
3. **Mending** by level: §3's units and materials, cheap for wattle.
4. **The fox and the shut house:** a shut house that is merely worn keeps the fox out; only holed or worse lets it in. This answers
   Q-37 (a).
5. **Camps** (§4): three states (standing, damaged, down); calm wear 0.08 and 0.05 a night; a gale flattens about half. Built for
   1 timber, brush and 1 unit; mended for brush and a quarter unit; the fire 1.5 timber a night; no animal kept out.
   - Building camps out (lean-tos, windbreak, thorn ring, rack, tents) is later (OPEN L-47).

## 4. Stage C: the fixes the gates found (Q-37, Q-38)

1. **Cats** ([cats.md](cats.md) §3, the first step without husbandry; Q-37 d):
   - the settling chance at a store with mice about 0.15 a season, 0.4 if food was left out at the house in the last days;
   - food left out (milk, meat, offal, fish lying at a house, D2-85) is also a target for rats, the fox and a dog (brief 2's
     targets);
   - a cat leaves a store that had no mice and no food left out for a season;
   - a stray can be found when working away from the houses (a find, keyed, as built).
2. **The fox's probe** (Q-37 b): the fox's hens nearly double with the probe. Calibrate `probe` and the door odds so that one lax
   house raises its neighbours' losses without doubling the hamlet's.
3. **Pigeons** (Q-37 c): their raids mostly add to their grazing, so the same corn is counted twice. Count a raid's take as part of
   the flock's grazing, not on top of it.
4. **Bins:** after brief 2, bins halve store losses. They should cut them by about 30%; calibrate STORE_STOPS.
5. **A left carcass and the herd** (Q-38 a): the wolves eat the carcass instead of a cow, so a left carcass lowers the herd's losses.
   A group that feeds at a carcass should remember the herd it saw from there (`_groups`' memory: `found` and `return_p`, built),
   and come back for it in the next nights. A dead cow left by the fold then raises the fold's losses over the next week.
6. **The carrion pool** (Q-38 b, 37.2's ecology):
   - The pool is a standing stock of about 460 kg a km², against eaters taking 1 to 2 kg a night, so a carcass adds about 0.3% a
     night.
   - Make it a flow: what dies or is left goes in, and eaters and decay take it out within days.
   - A carcass is then a large share of an area's carrion while it lasts, and draws its eaters.

## 5. Stage D: keeping meat at the new scale

1. **Drying in batches.**
   - `dry meat` is now 2 meat to 1 dried meat a unit at a hearth or fire ring. Make it a rack: cutting and hanging takes about 8
     meat a unit.
   - Then 3 nights on the rack, a thing at the fire, during which it is a target for flies (spoilage x0.5 in place of x1), rats, the
     fox and dogs (brief 2's targets), and rain spoils it.
   - After that it is dried meat (food 3 for 2 meat, as now).
   - Smoke over the hearth keeps the flies off (calibrate).
2. **Salting meat.**
   - `salt meat`, alongside `salt fish`: meat and salt to salt meat, keeping for months, by the same rule.
   - Salt is only where it is (a salt pan on saltmarsh, or traded: D2-56), so salting is a dependence between villages, not a free
     answer.
3. **Sharing as the other answer:** nothing is added. Twenty meat that spoils at 0.3 a night is the case for giving it out, and that
   is left to the people.

## 6. Touches in 37.4's files

- **`data.py`:**
  - TECHNIQUES `sweep`, `curve`, `line`; the drying rack and `salt meat`;
  - RESOURCES meat;
  - `PHYSICS["breaks"]` by structure and weather; the camp's rows;
  - ITEMS `salt meat`.
- **`knowledge.py`:** `SKILL["hard"]`.
- **`night.py`:** breaks by level and weather; the rack's nights; spoilage by a building's level.
- **`world.py`:** `CONDITION`'s five levels, with old worlds mapped.
- **`verbs.py`:** mending by level; the camp's build and mend.
- **Signs:** the levels' signs (shelter_damage §1); the rack's.
- **37.2's own:**
  - `wild/ecology.py`: pressure, near people, the carrion flow;
  - `wild/kinds.py`: HUNTED, WHEN, STORE_STOPS, the fox's probe, the cat's rates.

## 7. Tests (the gate)

**Stage A** (02zzd's harness, `CYB_ROOT` at the branch, the same four worlds and seeds):

| Hunter | The wood around a settled village | Far, in wild land |
|---|---|---|
| Novice, armed | 0.1 to 0.2 food a unit; success under 10% a trip | about 0.5 |
| Master, armed, familiar | 1 to 1.5; success about 40% | 4 to 5 (a full day) |

Also, for stage A:
- **Ranges and seasons:** far beats the wood around once the ring is hunted out. Autumn and snow differ from summer by at least a
  fifth.
- **Pressure** (`ev_depletion.py`): one daily hunter moves 1 to 2% of the ring's roe a night, and it refills within about a season
  after hunting stops.
- **Set works:** snare lines give 0.3 to 0.5 a unit; eel traps about 0.3 on run nights.
- **Unchanged:** farming and gathering.

**Stage B:**
- A wattle house is worn within about a season of frost, gappy within two unmended, and holed only by a storm or by long neglect.
- A gale holes or flattens wattle about as §2 says.
- A shut worn house keeps the fox out; a holed one does not.
- Camps flatten in gales and keep nothing out.
- Old worlds unchanged with the levels off.

**Stage C:**
- Cats settle at about one store in six a season with mice, more where food is left out, and leave empty stores.
- Food left out draws rats and the fox too.
- The hamlet's hens under the probe rise by under half.
- The pigeons' total take is unchanged by raids.
- Bins cut store losses by about 30%.
- A cow carcass left by the fold raises the fold's losses over the next week against one burned or buried.
- A carcass is a visible share of its area's carrion.

**Stage D:**
- A red deer dried takes about 3 units and 3 nights; a rack left unwatched loses some to the fox and dogs.
- Salt meat keeps for a season and needs salt.

**Regression:**
- The probe5 and probe6 worlds with bots: raids and losses within a third of before except where a test above moves them.
- All tests pass.

**Gate:** the above and a short dry-run report to Zach; then a small live run if he allows one, read against the pack off.

## 8. After this brief (the order proposed)

- **Brief 5: river and water** ([river_and_water.md](river_and_water.md)): pack K4 without the fen-only parts.
- **Brief 6: the butcher and wild goods:**
  - pack K2's rest: the butcher step and kit; by-products (sinew, bone, horn, offal); the midden and kites; store insects; ravens
    following wolves; the carcass as evidence;
  - pack K8's start: tanning and leather; sinew and glue; horn and bone.
- **Brief 7: methods and knowing without forays** (K3's non-foray ranks):
  - cord and the coppice's products; nets, bows, arrows and the boar spear as made gear;
  - sentinels (the jay, the roe's bark) lowering what is found;
  - crows and magpies that remember people;
  - hares' forms and refill; the roe kid at mowing; lapwing eggs; partridge and quail with nets; the nutting race;
  - decoys and calls; gathering young and eggs at colonies; drives with crews; teaching and records.
- **Brief 8: wood and frontier** (K5, where boar and deer live):
  - the sounder's habits and its leader; red deer at the ricks;
  - the wolf's circuit and dispersers; the bear's year;
  - wild bees and bee trees; hawks' eyries; the badger.
- **Then:** keeping animals (K6, dogs first, with 37.4's husbandry); land works (K7); illness (K10, waiting on illness in people);
  lodgers of buildings (K11); the coast (K9).
- **Forays** run as their own track whenever Zach takes them up (OPEN L-105).

## Why

- **Zach (9 Nov):** hunting should be very labour-intensive and uncertain, with a high skill ceiling that is hard to reach. Farming
  gives far more food per land and scales with people and capital.
- **Zach (10 Nov):** "Stage a can stay as written and building proper forays can be deferred I think. We can build a bunch of the
  other wildlife stuff without forays ... rewrite the briefs to address the other aspects of wildlife in the first briefs before
  any foraging".
- **02zzd:** the built take cannot reach the targets by any parameter.
- **02zx:** brief 2's and brief 3's gates left the four findings that stage C answers.
- **The order:** calibration and fixes come before new content, so the new content is not built on numbers already known to be
  wrong.

## Alternatives considered

- **Calibrate the numbers only:** reaches the near targets, never the far ones.
- **Leave the fixes until after new packs:** every new pack's gate would be read against wrong baselines (the fox, cats, carrion).
- **Leave preservation for later:** with the meat rescaled, most of a deer would rot, and the hunt's value would be an artefact of
  spoilage.

## Open questions (for Zach)

1. The meat scale (§2.5), at about 3 kg a meat from the cow's 40.
2. The far novice's target, about 0.5 a unit.
3. Accepting shelter_damage.md and cats.md as far as stages B and C use them.
4. The drying rack's numbers (§5.1).

## History

- 10 Nov 2026: first written by 37.2 as "the hunt over time, and forays" (hunt_and_forays.md), from 02zzd's measurements, forays.md
  and 02zv's K3.
- 10 Nov 2026: Zach: the route as guided exploration, the story's content, every foray returns home (forays.md History).
- 10 Nov 2026: D2-208, the world keeps its land (land_kept.md).
- 10 Nov 2026: Zach: keep stage A; defer forays as their own track; first build the other wildlife that needs no forays. Rewritten
  as brief 4: stage A as written; stage B forays removed; stages B to D added (shelter, the gates' fixes, preservation); the next
  briefs proposed (§8). Renamed hunt_and_fixes.md.

- 10 Nov 2026: Zach's go relayed by 37.4 ("Build the new brief"); 37.4 building it on `ecology-calibrate` (W-27). The four open questions take the brief's defaults: the meat scale as §2.5, the far novice about 0.5, shelter_damage.md and cats.md accepted as far as stages B and C use them, the rack as §5.1.

## Sources

docs/review/37_growth/02zzd_hunting_farming_ev.md and 02zzd_ev/; 02zx_wild_build_log.md; OPEN Q-37, Q-38; shelter_damage.md;
cats.md; forays.md; land_kept.md; 02zv §4; briefs 1 to 3; D2-56, D2-68, D2-85, D2-168, D4-109.
