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

Food a unit of work, armed unless said; "near" is the wood around the village:

| Hunter | Near | Far, alone | Far, a party with a pack ox |
|---|---|---|---|
| novice, unarmed | about 0.15 | | |
| novice | **about 0.3**, a kill every 4 to 7 trips | about 0.5 | |
| capable | about 0.7 | about 1.0 | |
| master | 1.2 to 1.5 (unchanged) | about 2 (capped by the carry) | 4 to 5 |

These replace the 9 Nov targets (02zzd) for the novice and the far hunter:
- a novice near home roughly level with winter gathering: a lean-season fallback, still below farming;
- a week of trying shows results, so practice is reachable;
- the far master's 4 to 5 is a party's (OPEN Q-40 a, Q-41 a).

Snare lines stay as they are (0.2 to 1.1 a unit, brief 4), once their catch can be found (§4).

## 3. The levers, in order

Each is calibrated on §8's harness until the targets hold, in this order; stop at the first that fits:
1. **The hunt curve's floor:** `SKILL["hard"]` from (0.4, 3.0) to about (0.8, 3.0). A novice is not helpless, and a master is about
   four times a novice instead of about eight. Practice still counts: tau stays 150.
2. **Unarmed for small game:** `hunt the wild`'s weapon factor `none` from 0.3 to about 0.6 (a throwing stick, stones, a hare in its
   form). `stalk` stays 0.2 and `drive` 0.15: deer and boar need a weapon or a crew.
3. **The far take:** the armed master far is 0.52 to 0.71 here against about 2 alone. Before changing anything, find why. 37.4's gate
   measured 1.45 on its own world, so the far land of each world and the carry are the first suspects.
4. **`take_k` last** (0.25), only if the armed master near still misses after 1 to 3.

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

- `engine/data.py`: `SKILL["hard"]`.
- `engine/things.py`: `own` for a set thing with a catch; the setter's look at a known thing; `_describe`'s remembered wording.
- `engine/perceive.py`: the look at a known thing on the parcel, through the one noticing rule.
- `engine/prompt.py`: none beyond the wording, unless the remembered text is built there.
- `engine/wild.py`: the crew's kill bonus by method (§5).
- The manual: the snare's and the trap's lines (§4.4).
- **37.2's own:** `wild/methods.py` (weapon factors), `wild/kinds.py` (any `flee` or `HUNT` change), the harness and its worlds.

## 7. Tests (the gate)

**Unit:**
- A setter working the parcel of their own line sees its catch on the morning after it is caught (at the calibrated chance); one not
  at the parcel sees nothing new.
- A stranger at the parcel finds a line with a catch more often than an empty one; birds over it after a day raise that.
- A remembered set thing never says "empty" unless that is what was seen, and says when it was seen.
- `lift the snares` at the parcel takes the catch into hand.
- Skill at the new floor; practice still lifts it.

**Calibration** (§8's harness, the region world and 02zzd's worlds, at least 80 tries a cell): §2's targets within about a third.

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
- **Leave the novice near zero as realistic:** an untrained hunter did poorly, but a method that never pays is never practised, so
  no one becomes a hunter.

## Open questions (for Zach)

1. §2's targets.
2. §5: the party bonus for drives only.
3. Whether the region world (02zze) is the calibration world, beside 02zzd's.

## History

- 12 Nov 2026: written by 37.2 from the wild region run (02zze) and Zach's questions on it ("Did they forget / remember they had set
  traps?"; "Surely noticing should fit with signs?"; the wording fix for "empty"; hunting too low for the novice).

## Sources

02zze (the run); 02zzd and its harness; hunt_and_fixes.md (brief 4); hunt_followups.md (brief 4b); 02zx; OPEN Q-36, Q-40, Q-41,
L-106; guides/senses.md; D4-48, D4-70, D4-75.
