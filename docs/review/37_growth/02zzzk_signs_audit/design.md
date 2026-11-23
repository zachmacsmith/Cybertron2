# What more people could be shown when they observe a thing: a design

23 Nov 2026. Session 37.2, a subagent on thread W-103. Zach: "get an agent writing up the other different types of things they
could be showed about the state of things when observed and translating into signs seen when attended or sometimes interacted
with". The survey it builds on is [survey.md](survey.md); every count here comes from [live1_signs.py](live1_signs.py),
[live1_checks.py](live1_checks.py) and [attend_kinds.py](attend_kinds.py) run against `/home/user/live1/<arm>` (outputs kept beside
them). Nothing here is decided or built; it is a proposal for Zach, written to guides/senses.md's form.

**The rules kept throughout.** A sign reads only what the state holds, at its resolution; it tells a change, not a standing fact; it
comes as a bundle across senses; its chance comes from the one noticing rule, never from the row (D4-53, D4-75). Experts' signs
observe and never direct (D2-269): every proposed line below is a fact or a judgement of a fact, never "do this". The engine never
detects or announces a breach or a theft (L-174): people learn of a taking only by what they sense. Rules are not attendable
(D2-341). The night's meal is told each morning (D2-342), §3.

## The short answer

Three changes to how observing works, then rows for each mechanism.

1. **Attending finds what was named.** A target is resolved from the sentence the person wrote (the first name of a person,
   building, parcel, herd, tagged thing, store or set gear it holds), never falls back to the place's ambient lines, and those lines
   are grounded or removed. Today 128 of 213 attends in the new prompt (60%) found nothing and were answered with "cattle lowing on
   the Leaze" in a village with no herds.
2. **A close look costs a unit and shows second-order facts.** A new act, `look` (1 unit, at one's spot that day), reads rows
   marked `look`: how long a store portion keeps, how many nights a trap has left, what the weir turned away, how a pool comes back,
   a member's nights gone short. Free attending keeps the first-order rows (what is there now). Working with a thing reads its
   `look` rows too, since handling it is looking; and its lines are shown at that evening's hearth, not only the next morning.
3. **One's own things are known as one last handled them.** Gear's remaining life, a store portion's keeping and the night's meal
   are household knowledge (as `house_known` is today), shown without a roll, dated.

**The five that matter most** (§2): the meal told (D2-342); a store portion's keeping time; attending that finds its target, with
no false ambient lines; what the weir turned away and what one's traps took of the run; gear's remaining nights and a chore's
true yield.

## 0. The machinery

### 0.1 Resolving an attend (perceive.resolve_target, `perceive.py:659-687`)

**Now:** an exact name or a few fixed phrases; anything else is "the place in general (you could not find ...)", which reads the
covers' ambient lines (`perceive.py:501-504`).

**Proposed:**
- Scan the sentence for known names in this order: a person here, a building, a parcel, a herd, a tag (T7), then the nouns
  "store" (a building's store: the building, with its store rows), "traps", "net", "line", "snares" (one's own set gear at the
  named or nearest parcel), "racks" (the building with smoke racks named, else one's household's), "the run", "the eels", "the
  salmon" (the village's water). The first found is the target; the label is the name found, so the hearth says "You paid close
  attention to Marsh House's store".
- **Nothing found: nothing shown,** one line of one's own act: "You looked for {what} and found nothing there to look at closely."
  (No ambient lines in its place.)
- **Rules (D2-341):** "rule", "rules", "the book" and a rule's number are not subjects. A sentence naming only a rule resolves to
  nothing, with the line above; one naming a rule and a thing ("rule 2 and the salt fish in the store") resolves to the thing.
  Rules stay shown where they are: the system prompt's block (`book.py:1332`), the evening's "The standing rules" with the day's
  firings (`evening.py:84-90`), "Waiting today" (`book.py:1356`). No attend in live run 1 named a rule (attend_targets.txt).
- Live run 1's unfound attends, by what they named (attend_kinds.txt): a store's goods or vermin 39, a wall or crack 28, set gear
  15, racks and lots 13, a person's body 6, the water or weir 6, a person at a craft 6, greens 6, offers 5. Every one but offers has
  a target under this scan.

### 0.2 The covers' ambient lines (`data.py:228-241`)

Ground each in state or drop it. "cattle lowing on {pasture}" and "dung and trodden grass" only with a herd on the parcel today
(the HERD bundle already covers it: drop them); "the ring of picks from {rock}" only on a day someone quarried (WILD's own
quarrying rows at `signs.py:734-737` already do: drop it); "water running over stones" only for a brook or a river at low or normal
flow ("{water} running quick over its stones"), never a broad slow river; "voices and work about the houses" only with three or
more people on the built ground that day. Live run 1 showed these 88, 40, 46 and 29 times in set B's new arm, acted on 0.00 to 0.07
in every arm (live1_signs.txt, live1_checks.txt §1).

### 0.3 A close look with units: the `look` act

`{"do": "look", "at": X}`: 1 unit; X as attend resolves it; one is at X's parcel for the day's presence (as work places one). It
is the only way to read rows marked `look: True`, by scope (as `only`), and the rule gives their chance. With presence 0.5 (one
at work there) and attention close x2 times subject x5, a `look` row's chance is own x visibility x 5: own 0.4 lands near certain on
open water or a fen in clear day (1.0, 1.0), 0.7 in a wood (visibility 0.35), 0.6 on water in fog (0.3); for one's own house
(inside, presence 1) own 0.4 gives 1.0 in any weather. Shown that evening as "You looked closely at {X}:" under the day's sights
(D4-82), and remembered against X like any belief. Calibrate with `perceive.chance_of` before building (guide item 4).

Why a unit: the second-order facts are worth acting on and cost something to learn; a unit makes looking a choice with a price, as
Zach's "attending with units" names. Today nobody ever spends one to look (0 in every arm), because nothing is sold for it.

### 0.4 Working with a thing (`perceive.py:598-613`)

Read the thing's `look` rows too (attention x6 already lands them), include set things one tended (now excluded, `not
f.get("thing")`, line 601), and show the lines at that evening's hearth as "Working at {X} you saw:" as well as in the beliefs.
The day's result line stays the doer's; a row never repeats it (guide item 7).

## 1. Each mechanism: free attending, a close look, working with it, passing by

Each proposal: the state it reads, the sense, its own (and reach or scope), the words. "Known" means shown to the owner or the
household without a roll, dated (as `house_known`). Rows with `look` are read only by a close look or by working with the thing.

### 1.1 The river and the runs

Free attending to the water already reads u8's rows (`river.py:194-251`), most of own 2 to 5 (near certain on the parcel). Adds:

| Mode | State read | Sense, own | Words |
|---|---|---|---|
| look (fish) | `river.record[node].passed` (heads last night, by kind), in bands of tens | sight 0.4, `look`, knows fish | "last night's run past the village: dozens of eels" / "a hundred or more" / "hundreds" / "more than anyone could count" |
| look (fish) at one's traps, or tending them | `taken[cid]` against `passed` for the station | sight 0.4, `look` | "your six traps took four eels of the many that went past: the water held far more than they met" (when taken under a tenth of passed x the trap's share); "your traps took a fair share of what came down" (otherwise) |
| look (expert) | `RUNS` window and `runs.due` (the year's quota still to run) | sight 0.4, `look`, expert:fish | "most of this year's eels are still to come down" / "the run is half gone by" / "little of this year's run is left to come" |
| passing by | — | — | u8's rows already carry (own 2.4 to 3.8 "around"): nothing to add |

Not proposed: the runs' timing as advice ("set your traps tonight").

### 1.2 The shallows and resident fish

| Mode | State read | Sense, own | Words |
|---|---|---|---|
| attend (free) | `res.shallows` S/K above 0.75 | sight 0.5 | "minnows thick under every stone in the margins of {nm}" (the missing plenty row) |
| look | S/K and `water.renew` for the season (days to 0.75 K) | sight 0.4, `look`, knack fish by hand | "the margins of {nm} will be worth working again in about {n} days" (a judgement, as the reaper's "fit to reap in about") / "nothing will come back to these margins till spring" (winter, under ice) |
| working with (hand fishing) | S/K after the take, crossing 0.5 | touch 2.0, doer | "fewer under each stone by the end: the margins are thinning" |
| look | `res.fish` S/K | sight 0.4, `look`, knack angle | "the river's own fish are about half what they were" / "the river's own fish are few, and slow to come back" |

### 1.3 The weir

| Mode | State read | Sense, own | Words |
|---|---|---|---|
| working with (the crew emptying it), look | `river.record[node].turned[bid]` (kg) against `WL.weir_hold(b)` | sight 0.4, `look`, crew | "the traps were full by morning, and about as much again went past them" (turned 0.5 to 1.5 x hold) / "twice what the traps held went past" / "most of what came down went past the full traps" (over 3 x) |
| look (crew) | sections' wear (`wild/gear.wear_of`) past half | sight 0.4, `look` | "the {second} section's stakes loose at the foot and its wattle torn in places" (worn); "the {second} section sound" |
| look (crew) | the weir's share of a run with the gap shut (`WL.weir_share`) | sight 0.4, `look`, expert:fish | "with the gap shut it takes about a third of what comes down" (by share band) |
| passing by | turned (as now, `river.py:246`, own 2.9 around) | — | as now |

Live: "scales and torn weed piled against the weir's wattle: more came down in the night than its traps would hold" was shown 19
times in set A new, and no section was added in any arm (live run 1 report, "Building"). The amount is what a crew needs to
weigh a section (70 kg of hold each) against emptying twice.

### 1.4 Set gear: traps, snares, nets, lines

| Mode | State read | Sense, own | Words |
|---|---|---|---|
| known, daily, one's own sets in "Lying about" (`things.set_line` `things.py:407-441`) | laid pieces' `life` and `rot` (`gear.state_words` `gear.py:595-613`) as of one's last tend | — | "your wicker traps at the Isel (T2) (6 standing: good for about 5 more nights set; 1 near worn through) (summer day 6)" |
| known, in hand | `gear.held_words` (`gear.py:616-625`), already written for the old prompt (`prompt.py:774`) | — | "6 wicker traps: 2 broken, wanting mending; the rest good for about 8 more nights set" in "## You" (0 such lines reached anyone in live run 1, live1_checks.txt §2) |
| working with (tend) | the same, in the result (`placed.tend_one`) | — | "... You set them again: good for about 5 more nights set." |
| the tend result, an otter at them | `robbed_by` | — | "An otter had been at them first: scales on the withies, and less in them than the night should have left." (drop the count "1 gone": the setter did not see what was there, survey §2.4) |
| look at another's gear (stranger) | catch, state | as now (`signs.py:1332-1341`) | as now |

### 1.5 The wild: game, predators, scavengers, fowl

The wild's bundles are rich. Two changes and one addition:

- **Rewrite the six lines that direct (D2-269)** as observations: "the sounder's run comes out of {place} by one gap in the thorn,
  the same each night" (`kinds.py:382`); "the sounder will be back tonight, by the same gap; the same scare holds them only a few
  nights" (383); "they come back to the young corn while it is tender" (386); "rats breeding in the thatch and under the floors:
  full barns and a mild winter will double them by spring" (622); "a mast year in {place}: acorns enough under the oaks for swine
  and boar both" (572); "a wounded boar lying up in the thicket: the most dangerous beast in the wood" (426).
- **A close look at a wood** (expert:hunt, `look`, sight 0.4) reads what `HUNT_NOTICES` reads only while hunting (`kinds.py:580-603`):
  "about {n} red deer use this ground by the slots and the beds, {fat}; they are {wary}". The hunt's own notices stay.
- **A presence row's sense from data,** not from its words (`signs.py:2066`): "a raven pair croaking over the crags" is sound.

### 1.6 Woods, willow and cord

| Mode | State read | Sense, own | Words |
|---|---|---|---|
| attend (free), working at | `res.willow` S/K under 0.35 | sight 0.6 | "the willow at {nm} is cut over: bare stools, the new rods not till spring" |
| attend (free) | `res.willow` S/K over 0.75 | sight 0.4 | "willow thick at {nm}, the rods long and straight" |
| working with (cutting in summer) | `willow.harm` lowered K (`willow.py:63-73`) | touch 2.0, doer | "the rods are soft and in leaf: the stools bleed where you cut, and will throw fewer next year" |
| look | `res.young` / `res.dead` S/K and the renewal | sight 0.4, `look`, knack fell or firewood | "the coppice shoots in {nm} will be fit to cut again in about {n} days" / "dead wood gathered here does not come again: what lies is what there is" |
| the cord result (`verbs.py:905`) | the kg got, never rounded to 0 | — | "You twisted a few strands of nettle cord at the Street, about 0.04 kg (you hold 0.3 kg; a gill net takes about 1 kg)." The recipe's input is a fact of the craft one knows (`gear.py` RECIPES gill nets: cord 1) |

Live: "You took 0 cord" fired 130 times by fallback in set B new, 44 in A new (live1_checks.txt §3); "Twisting cord at Clay Field
gave nothing: four tries and no cord. I do not yet know why" (set A new, evening).

### 1.7 Fields, crops and herds

The crop and herd bundles are the guide's model; little to add. A close look at a ripening crop (`look`, knack reap, sight 0.4):
"a fair stand: about four times the seed, if it is got in" from quality x stand x the crop's yield (a judgement in words: twice,
three, four, five times or more). A close look at a herd (`look`, knack herd): its condition and the cows near calving, which HERD
reads by chance (`signs.py:205-212`).

### 1.8 Buildings, rooms and fittings

| Mode | State read | Sense, own | Words |
|---|---|---|---|
| known (the household) and look (others) | `level_since` past `wear.unmended_days` at level 3 or 4 (`night.py:621-624`) | sight 0.6 | "the crack in {nm}'s wall left unmended these {n} days, the daub falling away round it" (the state's own cause: it wears faster now) |
| working with (boiling salt), look | the brine pan's uses against its life (`wear.py:28-43`, life 60) | touch 1.0, doer | "the pan's bottom thin and pitted where the fire takes it" (past three quarters of its life); the result already says once it is worn |
| attend (free) | a building one does not hold: its store's goods by portion as now only through an open door (`signs.py:898`, p 0.05) | — | as now: a store is a household's own |

### 1.9 Stores, containers and vermin

| Mode | State read | Sense, own | Words |
|---|---|---|---|
| known, daily, one's own store (`stores.store_line`, `prompt.py:681-687`) | each portion's spoil rate tonight (`stores.rates` `stores.py:276-298`), as a share lost by tomorrow | — | "76.8 fish in the bins (fresh: about half of it will be gone by tomorrow night)"; "31 roots on the floor (keeping)"; for goods keeping a season or more, nothing added |
| look, one's own or a store one may take from | the portions' vermin exposure (`stores.exposure`, `vermin_portions` `stores.py:312-326`) with rats or mice about | sight 0.4, `look` | "the sacks on the floor gnawed at the corners; the chest untouched" / "rat runs along the wall to the grain on the floor" |
| known, daily | the meal's draw (§3) | — | §3 |
| passing by another's store | as now: smell of fish going off, a stink of rot (`signs.py:875-880`) | — | as now |

Live: on the glut nights fresh fish went off by the store-full while racks stood idle: set A new day 9, 47.3 kg (21.8 food) with
only the Marsh Smokehouse smoking; set A old the same night 85.4 kg; set B new days 10 to 12, 52.6, 44.7 and 61.1 kg with the
Brook Smokehouse idle each night (live1_checks.txt §4). The only cue was "the fish ... going soft and starting to smell: it will
not keep", the morning after the loss (its Shepherd House form alone shown 60 times in set A new, live1_signs.txt).

### 1.10 Racks, lots, fires and the salt pan

| Mode | State read | Sense, own | Words |
|---|---|---|---|
| passing by, next door | another household's smokehouse with no lot and no fire (`process.lots`, `b.smoke`) | sight 0.8 | "no smoke from the Brook Smokehouse, its racks bare" (a change: the morning after a lot came down, or the first day of a glut night's run) |
| attend (free) | another's racks: kg waiting and room (`process.room`) | sight 1.0 | "the racks in the Brook Smokehouse half hung with fish, room for as much again" |
| known | as now (`process.house_lines`), with "0 kg" never shown for a lot that rounds to nothing | — | "on the smoke racks: a little smoked fish, done 3 nights ago, waiting to be taken down" |

### 1.11 People: hunger, health, work, care, children

| Mode | State read | Sense, own | Words |
|---|---|---|---|
| known, the household at its hearth | each member's hunger and `missed` (nights short in a row) | — | "Petronel went to bed short two nights running" (in the household line of §3) |
| look at a person | `hunger`, `missed`, `wounded`, the day's `ate` | sight 0.4, `look` | "Petronel is thin in the face and slow to rise: little eaten for days"; "Petronel ate a half share last night" (one who ate at the same hearth) |
| attend (free) a person at a craft | as now (their acts and results there); `watch` remains the day beside them | — | as now |
| oneself | the meal | — | §3 |

Live: set B new, days 30 to 39, "Petronel, who is gaunt and unsteady on their feet", "Henry and Nigel, who are gaunt" were attended
and not found (attend_targets.txt); the Brook household starved on days 33 to 37 (live run 1 report).

### 1.12 The book and its rules (D2-341)

Rules are not attended (0.1). Two changes to what is shown, both under L-174:
- **"Against the household's rule n: ..."** (`book.py:1385-1387`) announces a breach. Replace it with what the household senses:
  the store line says what the rule keeps back against what is there ("salt fish 10 in the bins; the household keeps 20 back by rule
  3"), and those who ate at the hearth see who ate what (§3).
- **A rule's firing that yielded nothing** says so as the cord result does (1.6), and the live run's flag that such a chore stops
  stands (live run 1 report).

### 1.13 Weather and ice; travel and roads

Nothing to add. The sky's forecasts were never acted on (guide); the road's bundles were not exercised in live run 1. One fix: the
great freeze's "the river frozen from bank to bank" (`kinds.py:536`) to say only what holds: "ice from bank to bank in the slack
water; birds lying dead on it".

## 2. Ranked by how much they would change decisions

| Rank | Addition | Evidence (live run 1) | Cost |
|---|---|---|---|
| 1 | The meal told, and the store's diff split by the meal (§3; D2-342) | 294 to 311 store diffs a long arm; "Roots are vanishing ... rotting or mice" (B new day 3, Oliver and Peter; A new days 2 and 3), a rule defended on the misreading ("so it's right that the household eats them first") | a record in `night.night`, two lines |
| 2 | A store portion's keeping, known daily (1.9) | 47 to 85 kg of fresh fish lost on glut nights with racks idle (live1_checks.txt §4) | one call to `stores.rates` in `store_line` |
| 3 | Attending finds its target; no false ambient (0.1, 0.2) | 128 of 213 attends unfound; 88 "cattle lowing" with no herd | `resolve_target`, `COVERS` |
| 4 | What the weir turned away, and one's traps' share of the run (1.3, 1.1) | the "scales" line 19 times, no section added; trappers set 6 traps and took a few eels a night | rows reading `river.record` |
| 5 | Gear's remaining nights; a chore's true yield (1.4, 1.6) | gear life shown 0 times; "0 cord" 130 times | `gear.held_words` in the view; the result's rounding |
| 6 | A member's nights short (1.11) | gaunt members attended and not found; a household starved | the household line |
| 7 | The `look` act and its rows (0.3) | units spent to look: 0 in every arm, because nothing is sold for one | a verb, a row flag, the evening section |
| 8 | Others' idle racks seen in passing (1.10) | Brook Smokehouse idle on set B's glut nights | one row |
| 9 | Willow, the shallows and the coppice coming back (1.2, 1.6) | the Fen's withies and shallows worked every day in set A new | rows on existing stocks |
| 10 | The six expert lines rewritten (1.5); "Against the household's rule" replaced (1.12) | rules: D2-269, L-174 | text |

## 3. The night's meal, told each morning (D2-342)

### 3.1 What the engine must keep

In `night.night` (`night.py:136-176`), for each person fed: `rec["meal"][name] = {"from": {cid: {item: qty}}, "first": [[item, rule
ref]], "ration": [qty, rule ref] | None, "need": need, "base": the ration without the work, "ate": ate, "fill": "full" | "short" |
"hungry" | "missed", "raw": [items]}`. `_eat` (`night.py:494-513`) returns its draws by container and item as well as the total;
`book.meal` (`book.py:1065-1088`) returns which rule (own or household, its number) put each good first and set the ration. The
household's draw is the sum over its members of `from` for each of its stores: `rec["drawn"][bid] = {item: qty}`. Deterministic and
replay-safe: the same draws the meal already makes, now written down.

### 3.2 The words

**One's own meal**, first in "## You" (replacing the hard-work line, `run.py:629-648`, which it subsumes):

- Full, by the default order: "Last night you ate 3.1 roots and 0.4 dried meat from Brook House's store, as the meal goes when no
  rule says (what spoils soonest first): food worth 1.28 meals, after a hard day where a lighter one would have needed 1. You went to
  bed full."
- By a rule: "Last night you ate 2.2 salt fish from Brook House's store, salt fish first by the household's rule 2, and 1.4 roots
  after it: food worth 1 meal. You went to bed full."
- A ration by rule: "Last night you ate 0.5 roots from Brook House's store, a half share by the household's rule 4: food worth 0.5
  meals. You went to bed still hungry."
- Short of the work: "... food worth 1 meal, a ration's worth but less than the day's work asked (1.28). You went to bed still
  hungry."
- A cold night: "... less than a cold night asks (1.3). You went to bed still hungry."
- Missed: "Last night you ate 0.3 roots from what you carried, food worth 0.3 meals: not enough. You went to bed hungry, a missed
  meal."
- Raw: add "With no fire lit, the roots went down raw and fed you about half what they would cooked."
- From hands and a store: "... 0.6 fish from your own hands and 2 roots from Brook House's store ..."

**The household's draw**, in "Since your last morning", with the store's diff split (`view.py:155-168`):

- "Brook House's store fed 5 last night: 17.9 roots and 0.4 dried meat (food worth 4.72 meals). Petronel and Basilia went to bed
  short." (who went short: seen at the shared hearth, the household inside)
- The diff: "Brook House's store since you last looked: roots -19.4 (17.9 eaten at the meal; now 31.1), egg +0.9 (now 3), firewood
  -4 (now 38)." The rest of a change is left unexplained: the household judges it (vermin, spoil and takings show by their own
  signs, L-174).

Every number is one the household handled. The default order is named in words the person can use to set a rule.

### 3.3 Who is told

Each person their own meal; every member of a household that ate from a store, its draw; one away from home, only their own. A
guest who ate from another's store learns their own meal and "from {house}'s store".

## 4. Calibration and tests (for whoever builds)

- Every `look` row: chance through `perceive.chance_of` for one at the spot with the look act (clear, fog, a wood) and for one
  attending free (must be 0, by scope).
- The meal: a world with a household of five on roots and a `first` rule; the lines and the split diff match the store's change
  less spoil to the item; a replay with no mismatches.
- `resolve_target`: live run 1's 128 unfound sentences (attend_targets.txt) as a test table: each resolves to the subject named
  first, rules to nothing.

## Open questions for Zach

1. **Should a close look cost a unit** (the `look` act, 0.3), or should attending itself cost a unit when it reads second-order
   facts, keeping one act?
2. **Should a store portion's keeping ("about half of it will be gone by tomorrow night") be known daily to the household**, or only
   on a close look at the store?
3. **Should a household's members see what each other ate**, or only who went to bed short?
4. **Should the store's diff name only the meal's share** and leave the rest unexplained, or also name spoilage ("2.1 went off"),
   which the household could smell?
5. **Should a run's size be read in rough heads** ("hundreds of eels went past last night") by one who fishes, or stay in the bands'
   words only?
6. **Should one's own gear's remaining nights be known daily**, or only when one tends or holds it?
7. **Should the covers' ambient lines be grounded (a herd there, someone quarrying) or removed** in favour of the bundles that
   already show those states?
8. **Should a sentence naming only a rule, as an attend, say "you found nothing there to look at closely"** or say nothing at all?
