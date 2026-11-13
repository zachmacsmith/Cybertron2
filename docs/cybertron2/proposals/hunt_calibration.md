# Hunting that pays something to a beginner, and snares that are lifted: build brief 4c

**Status:** draft (12 Nov), for Zach's decision on the targets (§2) and the party bonus (§5). Nothing decided or built.
**Build brief 4c** for the wild layer, after brief 4b (`hunt_followups.md`) and before brief 5 (`river_and_water.md`).
**Owner:** 37.2:
- the author;
- the data in `wild/kinds.py` (`HUNT`, `HUNTED`, kinds' `flee`) and `wild/methods.py` (method rows, weapon factors) is 37.2's;
- 37.4 builds it, as for briefs 4 and 4b; the skill curve (`engine/data.py` `SKILL`), noticing (`engine/things.py`) and the
  remembered line (`engine/prompt.py`) are 37.4's (§6).

**Affects:**
- spec/environment/wildlife.md (on the merge of briefs 1 to 4b);
- on the branch: `wild/kinds.py`, `wild/methods.py`, `engine/data.py` (`SKILL`), `engine/wild.py` (`hunt`, `_set_night`),
  `engine/things.py` (`own`, `_describe`, the remembered text), `engine/perceive.py`.

## Summary

The wild region's 30-day live run (02zze; 38 people, four villages, briefs 1 to 4b as built) took **nothing by hunting**:
- 57 planned hunts of the wild and 6 stalks. Hunters met 2 or 3 beasts a trip (roe, hare, woodpigeon), and every one "got away".
- 25 snare lines and water traps were set. They caught about 17 hares and 5 eels, and **none was ever lifted**: the catches rotted
  in the snares.

Measured on the region's own world (the harness of 02zzd, 80 tries a cell; §8), the hunt as built gives a novice almost nothing:

| Method, the wood around | Novice (skill 0.4) | Capable (1.0) | Master (2.3) |
|---|---|---|---|
| hunt the wild, unarmed | 0.00 to 0.03 | 0.03 to 0.07 | 0.09 to 0.17 |
| hunt the wild, armed | 0.03 to 0.09 | 0.06 to 0.21 | 0.23 to 0.32 |
| stalk, unarmed | 0.00 to 0.08 | 0.08 to 0.11 | 0.13 to 0.19 |
| stalk, armed | 0.06 to 0.14 | 0.33 to 0.55 | 0.70 to 1.06 |
| hunt the wild far, armed | 0.04 to 0.11 | 0.19 to 0.32 | 0.52 to 0.71 |

(food a unit of work, the range across the four villages; for scale, winter gathering gives 0.2 to 0.3, farming 1.4 to 2.8.)

Why:
1. **The factors multiply to almost nothing.** A beast met is taken with `take_k` 0.25 x skill x the weapon factor x (1 - flee) x
   familiarity: for a novice unarmed after a hare, 0.25 x 0.4 x 0.3 x 0.5 x 1.12 = 1.7%. None of the factors is wrong by itself.
2. **Almost no one carries a weapon.** A crude weapon is 1 timber and 1 unit and multiplies the take three to five times; the methods
   line says "a weapon helps"; four existed in the region.
3. **Practice cannot lift a novice out of it.** The hunt's curve runs 0.4 to 3.0 with tau 150 units, so capable (1.0) needs about 40
   units of hunting. At these odds that is 40 units with nothing to show, and agents give up first (Durand: "Snares and hunting have
   failed all along").
4. **A catch in a snare is never seen.** The setter stood at the parcel while the catch lay there (Colin at the Ham on five days,
   Sabina at the Mere on three, Ancel on Holtham Common on three), and no prompt ever showed it: a set thing's conspicuousness is
   0.12 and a catch adds only its bulk. The remembered line said "a line of snares set at the Ham, **empty** (you put it there, winter
   day 4)", and that word passed into the agents' own memories as fact ("Snares at Holtham Common and Cow Close stay empty").

Snares, once lifted, were the one method that paid: about 0.9 food a unit in the run.

## 1. For the builder

**Read:**
- briefs 4 and 4b and their gates (02zx; OPEN Q-40, Q-41);
- 02zzd and its scripts (`docs/review/37_growth/02zzd_ev/`), with `ev_region.py` (§8);
- `docs/cybertron2/guides/senses.md` before §4;
- on the branch:
  - `engine/wild.py`: `hunt` (`p_take`), `_set_night`;
  - `wild/kinds.py`: `HUNT`, `HUNTED`, the kinds' `flee` and `detect`;
  - `wild/methods.py`: the method rows and `weapon` factors, `FAMILIAR`;
  - `engine/data.py`: `SKILL`;
  - `engine/knowledge.py`: `curve`, `skill_of_practice`, `tried`;
  - `engine/things.py`: `own`, `_describe`, `remember`;
  - `engine/prompt.py`: `_things_lines`.

**Do not:**
- tell anyone about a catch they are not at;
- name kinds in rule code;
- change farming or gathering;
- change the master's near target.

Dry runs only.

**Branch:** from main after briefs 1 to 4b are merged; otherwise `ecology-hunt3` from `ecology-hunt2`.

## 2. Targets (for Zach)

**How often, and what.** A trip near home is 3 units (the hunt's 2 and the wood around's 1). Targets for a wood not hunted lately:

| Hunter | A kill on | Mostly | Food a unit | A trip gives |
|---|---|---|---|---|
| novice, bare hands | about 1 trip in 4 | hares and birds | about 0.1 | about 0.3 |
| novice, armed | **about 1 trip in 2** | hares and birds; a roe now and then | 0.2 to 0.3 | about 0.75 |
| capable, armed | most trips | a roe about 1 trip in 4 | about 0.7 | about 2 |
| master, armed | nearly every trip | deer, capped by the carry near home | 1.2 to 1.5 (unchanged) | about 4 |
| far, alone (6 units a trip) | novice about 0.5, capable about 1.0, master about 2 (the carry) | | | |
| far, a party with a pack ox | | | 4 to 5 a person-unit (the master's 4 to 5 is a party's: OPEN Q-40 a, Q-41 a) | |

Why a novice kills on about half their trips: in the run, hunters gave up after 3 to 5 blank trips (Durand, Thomasin, Gillian, Osric).
At a kill in 1 trip of 2, four blank trips in a row happen to about 6% of novices; at 1 in 5, to 41%, and practice never starts.
Big game stays gated by skill, so practice pays.

**Against farming and the rest** (food a unit of work, 02zzd; a person eats 1 food a day and has 5 to 7 units):

| Way of getting food | Food a unit | A day's work (6 units) feeds | When it comes |
|---|---|---|---|
| farming, plough and copper reap | 2.8 | about 17 person-days | at the harvest, once a year; bounded by land |
| farming, unbroken ground, crude reap | 1.8 | about 11 | the same |
| farming, hoe-broken | 1.4 | about 8 | the same |
| milk, three cows | up to 2.4 | up to 14 | daily, by the herd |
| gathering, autumn | 1.1 to 1.7 | 7 to 10 | a few days a parcel |
| snares, lifted (the run) | about 0.9 | about 5 | by night, for days |
| **hunting, master near** | **1.2 to 1.5** | **7 to 9** | **at once; any season; spoils unless dried** |
| **hunting, capable near** | **about 0.7** | **about 4** | |
| gathering, winter | 0.2 to 0.4 | 1 to 2.5 | |
| **hunting, novice armed near** | **0.2 to 0.3** | **1.2 to 1.8** | |
| hunting, novice now (as built) | 0.01 to 0.09 | under 0.5 | |

So:
- a novice hunter is level with winter gathering: a lean-season fallback, not a living;
- a capable hunter is about a third of a farmer, and a master about three quarters of a farmer on unbroken ground and half of one
  with a plough;
- hunting's advantages are that it comes at once and in any season, and needs no land; its costs are depletion, spoilage and the
  carry.

**These are rates on fresh ground.** Hunting the same wood every day falls well below them as it empties and the game grows wary
(02zzd: daily stalking fell to 0.18 a unit over 16 days; brief 4b's wariness and slow recovery). The sustained yield of a village's
woods is what keeps hunting from replacing farming, not the per-trip rate.

Snare lines stay as they are (0.2 to 1.1 a unit, brief 4), once their catch can be found (§4).

## 3. The form, and the levers

### 3.1 The chance as a baseline times multipliers (Zach, 13 Nov)

Today a beast met is taken with `take_k` 0.25 x skill (0.4 to 3.0) x the weapon factor (`none` 0.2 to 0.3, `armed` 1.0) x
(1 - flee) x familiarity (1 + 0.35 x familiar), clipped at 0.95. "Armed = 1.0" is a ceiling: a bow would need a factor above 1 or
every factor rescaled, and the ceiling moves with each mechanic added. Instead:

- **The baseline is what everyone always has:** bare hands, a novice, a kind not known. Its rate is `base` (by method), calibrated to
  §2's bare-handed novice.
- **Everything else multiplies above it:**
  - **gear:** a crude weapon about x3 (club or crude spear; calibrate), and later a hunting spear, a bow, nets and a dog each their own
    multiplier on the methods they serve, as data on the gear (02zv C1: properties on gear);
  - **skill:** a novice x1, rising with practice to about x4 for a master (the hunt's curve as a multiplier: `SKILL["hard"]` from
    (0.4, 3.0) to (1.0, about 4.0), tau 150 units; calibrate);
  - **familiarity:** as built (1 + 0.35 x familiar);
  - **the kind:** its `flee` stays a share, (1 - flee), since it is a property of the beast and not a gain.
- **The chance from the product:** p = 1 - exp(-base x the product of the multipliers), in place of the product clipped at 0.95.
  Multipliers then compose without a ceiling, returns diminish as the chance nears certainty, and at low odds it is almost the
  product itself, so the novice end calibrates directly.

The same form for a set thing's catch (`_set_night`) and for the party's members (`detect` by more eyes, as built).

Farming's tools are already close to this: the crude tool is 1.0, copper x1.5 to 2, bare hands a reduction (reap 0.6, hay 0.3, fell
0.25); a better tool goes in above copper without rescaling. They stay as they are; making bare hands their baseline would be for
consistency only.

### 3.2 The levers, in order

Calibrated on §8's harness until §2 holds; stop at the first that fits:
1. **`base` by method** for the bare-handed novice (§2's first row).
2. **The crude weapon's multiplier** for the armed novice (about x3; calibrate).
3. **The skill multiplier's top** for the capable and the master (about x4 at the top; capable at about 40 units of practice).
4. **The far take:** the armed master far is 0.52 to 0.71 here against about 2 alone. Before changing anything, find why: 37.4's gate
   measured 1.45 on its own world, so the far land of each world and the carry are the first suspects.

Also look into two open findings:
- the drive's food in run 5's world (x2.40, unexplained, OPEN Q-36);
- the far novice at 0.19 against about 0.5 (OPEN Q-41 d).

## 4. Set things: a catch found by going to it

The engine never tells a setter what their snares hold. They find out by going there, through the one noticing rule (D4-75).
1. **One knows where one's own set things are.** Someone at a parcel (working it, or on it) who set a thing there, or has seen it
   there, looks it over:
   - its state shows as a sign at that parcel ("a hare hangs in your snares at the Ham"; "eels in the wicker traps at the Mere");
   - the conspicuousness for one who knows the place is high (about 0.9; calibrate);
   - for others, the noticing rule is as built.
2. **A catch shows itself.** A beast caught raises the thing's own conspicuousness (about 0.4 while fresh; calibrate). After a day,
   birds come to it as to a carcass (brief 3's `birds`), so a passer-by may find it and take it, leaving the theft trace (D4-48) for
   those who know the line.
3. **The remembered line, wording only** (Zach, 12 Nov):
   - a set thing is remembered without "empty": "a line of snares you set at the Ham (winter day 4)";
   - when it is seen again, as it was then: "with a hare caught in them (as you saw it on winter day 6)", or "nothing caught in them
     (as you saw it on winter day 6)".
   - Nothing else in the remembered things changes. OPEN L-106 holds the wider question of what the engine keeps for agents.
4. **Lifting:** `take {"from": "the snares at the Ham"}` already empties a known thing. The method's line in the manual says it in
   world terms: "come back to your snares and take what is in them". "Lift the snares" and "check the snares" become aliases of that
   take.

Signs follow `guides/senses.md`: grounded in the thing's state, a change, worth acting on, shown only at the parcel.

## 5. The party bonus (for Zach; OPEN Q-41 b)

A party of three takes about 1.9 times a lone hunter's food a person-unit in the wood around, from the crew's kill bonus
(x1.25 a member).

Proposed:
- the bonus for `drive` only, where a crew is the method;
- for other methods, a party's gain is the carry and the danger shared (brief 4b), and finding beasts by more eyes (`detect` per
  member, as built).

## 6. Touches in 37.4's files

- `engine/data.py`: `SKILL["hard"]` as a multiplier (§3.1).
- `engine/wild.py`: `hunt`'s `p_take` and `_set_night`'s catch as 1 - exp(-base x multipliers) (§3.1).
- `engine/things.py`: `own` for a set thing with a catch; the setter's look at a known thing; `_describe`'s remembered wording.
- `engine/perceive.py`: the look at a known thing on the parcel, through the one noticing rule.
- `engine/prompt.py`: none beyond the wording, unless the remembered text is built there.
- `engine/wild.py`: the crew's kill bonus by method (§5).
- The manual: the snare's and the trap's lines (§4.4).
- **37.2's own:** `wild/methods.py` (`base` by method; gear multipliers in place of the `weapon` rows), `wild/kinds.py` (any `flee`
  or `HUNT` change), the harness and its worlds.

## 7. Tests (the gate)

**Unit:**
- A setter working the parcel of their own line sees its catch on the morning after it is caught (at the calibrated chance); one not
  at the parcel sees nothing new.
- A stranger at the parcel finds a line with a catch more often than an empty one; birds over it after a day raise that.
- A remembered set thing never says "empty" unless that is what was seen, and says when it was seen.
- `lift the snares` at the parcel takes the catch into hand.
- The chance is 1 - exp(-base x multipliers): bare-handed novice at `base`; each gear and skill multiplier raises it; no clip.
- Practice raises the skill multiplier from 1 toward its top.

**Calibration** (§8's harness, the region world and 02zzd's worlds, at least 80 tries a cell): §2's kill rates and food a unit within
about a third, on fresh ground; and daily hunting of one wood over 16 days falling well below them (as 02zzd).

**Society-level** (dry, scripted bots set and lift lines): the catch lifted in the bots' arm against the catch left in the run.

**Regression:**
- worlds without the wild pack unchanged;
- the probe worlds with bots;
- all tests pass.

**Gate:** the above and a short dry-run report to Zach. A live arm only if he allows it: the region world again against the 30-day
run, reading kills, snares lifted, weapons made, and hunting kept up past the first week.

## 8. The harness

`docs/review/37_growth/02zzd_ev/ev_region.py` (CYB_ROOT = a checkout of the branch): for each village's wood, `hunt the wild` and
`stalk` near and `hunt the wild` far, by novice, capable and master, armed and unarmed, on fresh copies of the world at its start
(nothing depletes between tries). Its results on brief 4b as built are in `ev_region_4b.json` beside it.

## Why

- Zach (12 Nov): "I feel like overall hunting numbers are too low, especially with the novice being practically zero right now?"
- The region run: no kill in 63 hunts and stalks; 22 catches never lifted.
- Hunting matters to the design as a skill that grows, a reason for parties, weapons and dogs, and a lean-season fallback; at about
  0.01 a unit it is none of these.

## Alternatives considered

- **Tell the setter each morning what their sets hold:** rejected (Zach, 12 Nov: "the engine shouldn't tell them. They should have to
  decide to go and check").
- **Raise `take_k` alone:** lifts the master as much as the novice and leaves the practice ladder as steep.
- **Keep reductions from a ceiling** (armed = 1.0, unarmed x0.3): numerically the same for one factor, but the ceiling moves with
  every new gear or mechanic (Zach, 13 Nov).
- **Keep the product clipped at 0.95:** stacked multipliers (gear, skill, a dog, a party) pass certainty and pile up at the clip.
- **Leave the novice near zero as realistic:** an untrained hunter did poorly, but a method that never pays is never practised, so
  no one becomes a hunter.

## Open questions (for Zach)

1. §2's targets: kill rates (a novice armed on about half their trips) and food a unit, against farming.
2. §5: the party bonus for drives only.
3. Whether the region world (02zze) is the calibration world, beside 02zzd's.

## History

- 13 Nov 2026: §2 and §3 rewritten (Zach, 13 Nov: "rather than times 0.3 for being unarmed, surely it should be increased if you
  are armed"; "Is a kill every 4 to 7 trips too bad?"; "Compare to the amount of food to get from farming"): the chance as a baseline
  (bare hands, a novice) times multipliers for gear, skill and familiarity, as 1 - exp(-x); kill-rate targets beside food a unit (a
  novice armed on about half their trips, since agents quit after 3 to 5 blank trips; the earlier 4 to 7 trips did not match 0.3 a unit
  for small game); the comparison with farming, milk and gathering; the targets as rates on fresh ground.
- 12 Nov 2026: written by 37.2 from the wild region run (02zze) and Zach's questions on it ("Did they forget / remember they had set
  traps?"; "Surely noticing should fit with signs?"; the wording fix for "empty"; hunting too low for the novice).

## Sources

02zze (the run); 02zzd and its harness; hunt_and_fixes.md (brief 4); hunt_followups.md (brief 4b); 02zx; OPEN Q-36, Q-40, Q-41,
L-106; guides/senses.md; D4-48, D4-70, D4-75.
