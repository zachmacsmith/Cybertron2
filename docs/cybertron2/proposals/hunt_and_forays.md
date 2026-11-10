# The hunt over time, and forays: build brief 4

**Status:** draft (10 Nov), for Zach's go. **Build brief 4** for the wild layer:
- the hunt's calibration measured in 02zzd;
- stage 5's forays (C11, as designed in [forays.md](forays.md));
- the first ranks of pack K3 (02zv §4; corrected against the engine by 02zw).

It starts from brief 3's branch (`ecology-carcass`, `cc4d342`).
**Owner:** 37.2 (author; the wild pack's data, `engine/wild.py`, landgen, the ecology). The act, places beyond the village, the
interpreter's model call, nights out and the manual are 37.4's (§6), and need 37.4's agreement on the board.
**Affects:** spec/environment/wildlife.md; spec/agents/actions.md; spec/world/places.md; spec/information/memory.md;
spec/record/execution.md; spec/economy/lodging.md.

## Summary

02zzd measured the hunt in generated worlds and found the problem is structural, not a matter of numbers:
- a trip meets at most one beast;
- the time it spends never counts;
- the range only adds units;
- the meat is 3 to 5 times small against the engine's own cow;
- a master succeeds on three trips in four;
- one hunter empties a 19 km² wood of roe in two weeks.

**Stage A** makes the take a search over time:
- meetings by the ground covered and the game's density there, each with its own chance of a kill;
- a carry limit;
- meat on the cow's scale;
- a hard skill curve for hunting;
- pressure by the ground hunted.

**Stage B** puts that rule under the **foray**:
- a person says in its own words where it goes, and a small model translates that into a route over the land beyond the village;
- the route is walked, searched and told as a short story;
- a person who runs out of day spends the night out.

Places stay in the person's memory, not in an engine table of spots.

## 1. For the builder

**This file holds for this brief.** Read:
- briefs 1 to 3 and their tests;
- [forays.md](forays.md), which holds the design; this brief sets its open points by default (§4);
- 02zzd, with its harness in `docs/review/37_growth/02zzd_ev/`;
- on branch `ecology-carcass`:
  - `engine/wild.py`: `take`, `_reach`, `_notices`, `forage`, `_put_pressure`;
  - `wild/ecology.py`: the pressure step under `HUNTED`;
  - `wild/kinds.py`: `HUNTED`, `WHEN`, `NEAR_PEOPLE`;
  - `engine/knowledge.py`: `SKILL`, `curve`;
  - `engine/data.py`: TECHNIQUES `stalk`, `hunt the wild`, `snare`, `trap in water`, the `range:` rows; ITEMS `pack`; `carry`;
  - `engine/things.py`: carcasses;
  - `engine/run.py` and `infra/`: model calls and their journal;
  - world/roads.md: a stretch as a place, D4-35; sleeping out, D4-12;
- `docs/cybertron2/guides/senses.md`.

**Do not:**
- name kinds in rule code;
- give the interpreter any state the person has not met;
- keep a table of spots per person;
- cap or filter what is noticed.

Dry runs only.

**Branch:** `ecology-forays`, from `ecology-carcass`. **Order:** stage A to its gate (§7), then stage B.

## 2. Stage A: the take as a search over time (`engine/wild.py` `take`)

1. **Search and travel.** A take's units are split into travel and search.
   - In the act as it is (`gather` with `range`), the range's units are travel and the method's units are search.
   - In a foray (§3), the route sets both.
2. **Ground covered.**
   - Search units times the method's `sweep`, a new TECHNIQUES property in km² a unit: about 0.4 for `stalk` and 1.0 for
     `hunt the wild`; calibrate.
   - For a range act, the ground is spent in the farthest area reached (home for `near`, the ring for `the wood around`, the
     bordering wild areas for `far`). The areas crossed on the way are passed at a fifth of the rate.
3. **Meetings.**
   - The number met is drawn from Poisson(λ), with λ the sum over kinds and areas searched of:
     density (heads a km²) x `detect` x the kind's WHEN detect x the method's weight x focus x familiarity
     / (1 + 0.5 x min(4, pressure)) x the ground in that area x `meet` (one constant; calibrate).
   - Meetings are taken in order. Each is drawn as now: danger first, then the kill at
     `take_k x skill x weapon x (1 - flee) x familiarity`. `take_k` is a new constant replacing 0.55, about 0.19; calibrate.
   - A wounded beast lying up is kept as now.
4. **The carry limit.**
   - After a kill, the trip goes on only while the hunter can carry more: goods' weights against `carry` (foot 10, a pack 20).
   - What cannot be carried is left. In stage A it goes into the area's carrion pool (`wild/ecology.py`); in stage B it is a carcass
     thing at the feature (brief 3's machinery).
   - So a red deer ends a lone trip, and a party or a pack ox brings more home.
5. **Meat on the cow's scale.**
   - RESOURCES `taken.goods`, with a slaughtered cow at 40 meat, so about 3 kg a meat: red deer 20, roe 4.5, boar 15, hare 0.7,
     mallard 0.3, woodpigeon 0.1, eel 0.2. The bear goes to about 40.
   - Hides as now. Calibrate within a fifth.
6. **A hard skill curve.**
   - `SKILL["hard"] = [0.4, 3.0]`, with its own `tau` about three times the trade's (slow to learn).
   - TECHNIQUES `curve: "hard"` on `stalk`, `hunt the wild` and the drive. `knowledge.curve` reads it.
7. **Seasons through finding.** Now that meetings scale, WHEN's detect rows show. Add data rows (calibrate):
   - snow lying: deer and boar detect x1.5 (tracks);
   - summer leaf: deer detect x0.8;
   - the rut as built.
8. **Pressure by ground (37.2's ecology).**
   - A take adds `HUNTED["hunt"] x min(1, ground in the area / the area's km²) x the crew factor` to each area searched, not a flat
     0.25 to every area in reach.
   - The flee shares are lowered so that one hunter stalking daily moves 1 to 2% of a 19 km² ring's roe a night, and ten hunters
     about ten times that.
   - Game returns as the pressure fades (built).
9. **Game near people (37.2's ecology).**
   - The shy kinds' density on a village's home area is lowered by people's presence: deer and boar by `NEAR_PEOPLE`'s module data
     (built in K0), a factor of about 0.3; calibrate.
   - Hunting near is then poor because the game keeps away, not only because the area is small.
10. **Snare lines and the eel run.**
    - `snare` sets a line (`line: 5` on the technique), each snare a set thing drawing by the take rule.
    - Check why the eel run's x2 and x3 `when` rows barely show in a set trap's nightly draw (02zzd: 0.09 in autumn against 0.08),
      and fix it.

## 3. Stage B: the foray ([forays.md](forays.md) §1 to §6)

1. **Places beyond the village (37.2 supplies the land).**
   - `landgen/ecology.py` adds `land.features`: for each area, 3 to 8 features from the generated land. These are falls where a
     river drops, a pool or lake shore, a ford, a spring, a crag, the core of an old wood, a clearing, a heath's edge.
   - Each feature holds `{id, kind, area, cell, terrain, phrase}`. The `phrase` is a plain description from the land ("the falls on
     the stream above the alder carr"), never a proper name.
   - The wild pack's sites (dens, setts, wallows, heronries, `wild.sites`) are placed at features.
   - For existing worlds, features are made at load from the land fields the world carries.
   - A feature is a place a person can stand at, like a road's stretch (D4-35). Things can lie there (D2-85); a person there sees
     what is there.
2. **Travel.**
   - About 4 km a unit on mixed ground (a day's walk is 24 km, world/roads.md). Open ground x1.2, wood x0.6, marsh and heath x0.7.
   - A river is crossed at a ford feature or a road's bridge, nowhere else (wading by flow is later).
   - The village's parcels and the ring are within a day. The wild areas leave little search time without a night out.
3. **The act:** `foray {intent, for: hunt | gather | look for, units, with, gear}` as forays.md §1.
   - A party moves at the slowest member's pace, shares one route and one story, and each member spends its own units.
   - A kill goes to the hands of whoever made it; sharing out is the party's own business (give).
4. **The interpreter.**
   - One small-model call per foray a day, the same model for every cast (Haiku 5.5), temperature 0.
   - Its instructions hold the route syntax: legs `go <place>`, `on <direction> from <place> for <units>`,
     `search <place> <units> by <method>`, `follow`, `home`.
   - **It is given:**
     - the intent;
     - the person's memory and kept lines;
     - the stories of its own recent forays, as it received them;
     - its village's parcels and road ends;
     - the features of the areas the person has been in, by phrase only (from its forays' record: where it went, never what lived
       there);
     - the travel costs.
   - It is not given where animals are, or any stock.
   - The engine checks the route against the graph and the units, and repairs it by fixed rules: the nearest valid place; cut the
     last legs when units run short.
   - The request and the reply go in the journal; replay reads the reply.
5. **Walking it.**
   - Each leg spends units.
   - The existing notices (`_notices`, D4-48) run at each place passed (as a passer) and searched (as a searcher).
   - A search leg is stage A's take, with that area's densities and the leg's units.
   - A gather leg draws from the area's forage (37.2 supplies `land.forage`: a stock per area from its ecosystems and the season
     curve, drawn and regrown as a parcel's is, by `forage`'s rule).
   - `follow` goes after a wounded beast, with its own chance of finding it, by skill.
6. **The turn-home rule.**
   - By default the foray keeps the units needed to get home, and turns back when the next leg would spend them.
   - The intent can waive it ("and on, even if I sleep out").
7. **The story.**
   - Three to eight lines, by templates from the walk's events in order, worded as signs are (guides/senses.md).
   - Times of day are a presentation choice, keyed so that replay is exact.
   - It is the act's result.
8. **A night out.**
   - When the units run out before home, the person sleeps at the place it reached (D4-12: 1.5 food, 2 in winter, and the cold;
     the risks of the weather).
   - Next morning it is at that place, and its acts are those the place allows: search or gather there, a foray home or onward,
     or wait.
   - At home nothing is announced (D2-4). A search for it is a foray `for: look for`.
9. **Memory and names.**
   - What the person saw and where is in its memory as it keeps it (D4-61).
   - It may name a place in memory or in kept lines, and use the name in a later intent; the interpreter resolves the name from
     that text.
   - The engine records only the foray: route, events and the intent's words, for the journal, the map and analysis.

## 4. Defaults for forays.md's open questions (OPEN Q-33; Zach may change any)

1. **The story:** templates from events, replayable. Zach (10 Nov): a large part of it is the signs along the way, what was met, the outcomes, and why the person went where it did, with the paths it saw and did not take. Those come from the walk's own state: the options it weighed at each step and the signs that tipped them.
2. **Names:** memory only. The engine keeps the intent's words, so analysis sees the names.
3. **Features:** 3 to 8 an area, from the land, with the pack's sites placed at them. Features made by people (a hide, a cairn)
   come with K7.
4. **Travel:** about 4 km a unit on mixed ground, by terrain as in §3.2. **Every foray returns home (Zach, 10 Nov):** the turn-home rule always holds and cannot be waived; there is no night out in the first version.
5. **The morning after:** the place's acts (search, gather, a foray, wait). Fire wants a fire act at a place, which comes later
   with L-102 and camps.
6. **Times of day (L-102):** no night forays and no dawn starts. A foray is part of a day, and a night out follows from running
   short.
7. **Calls:** one interpreter call per foray. Batching waits on cost data from the gate.

## 5. Not in this brief (next briefs)

- **K3's crafts:** cord, nets, bows, arrows and the boar spear as made goods.
- **K3's other content:** sentinels (the jay, the roe's bark); crows and magpies that remember people; records and teaching;
  drives with crews across villages. Stalking into the wind waits on C4's wind.
- **Camps, settling and new nodes** (forays.md §6, later; OPEN L-104 needs them).
- **K4, river and fen:** the eel run's lag, weirs as works with gaps, wildfowl. It waits on the generator making fen worlds with
  people: none of eight seeds passed its capacity check (02zzd, 37.2's).
- **Dogs** (K6, with 37.4's husbandry).

## 6. Touches in 37.4's files

- **`verbs.py`:** the `foray` act; `gather`'s range as travel and search.
- **`here.py` and `world.py`:** a person at a feature, as at a road's stretch; things lying at features.
- **`run.py` and `infra/`:** the interpreter's call, its journal entry and its replay.
- **`prompt.py` and the view:**
  - the act in the manual of what the person knows (the foray is basic; its methods are as known);
  - the story as the act's result;
  - what a person at a feature sees.
- **`night.py`:** a person out at a feature for the night (D4-12).
- **`data.py`:** TECHNIQUES `sweep` and `curve`; RESOURCES meat; the snare line.
- **`knowledge.py`:** `SKILL["hard"]`.
- **37.2's own:**
  - `landgen/ecology.py`: features and forage by area;
  - `wild/ecology.py`: pressure by ground, the near-people factor;
  - `wild/kinds.py`: HUNTED, the WHEN rows.

## 7. Tests (the gates)

**Stage A, dry.** Rerun 02zzd's harness (`docs/review/37_growth/02zzd_ev/`, with `CYB_ROOT` pointing at the branch) on the same
four worlds and seeds. The targets agreed on 9 Nov:

| Hunter | The wood around a settled village | Far, in wild land |
|---|---|---|
| Novice, armed | 0.1 to 0.2 food a unit; success under 10% a trip | about 0.5 |
| Master, armed, familiar | 1 to 1.5; success about 40% | 4 to 5 (a full day) |

Also, at stage A's gate:
- **Ranges and seasons:** far does better than the wood around when the ring is hunted out, and not before. Hunting in autumn
  (the rut) or under snow differs from summer by at least a fifth.
- **Pressure and refill:** `ev_depletion.py`: one daily hunter moves 1 to 2% of the ring's roe a night; the ring refills within
  about a season after hunting stops.
- **Set works:** a snare line gives 0.3 to 0.5 a unit; an eel trap about 0.3 on the autumn run nights.
- **Unchanged:** farming and gathering.
- **Regression:** the probe5 and probe6 worlds with bots, raids and losses within a third of before; all tests pass.

**Stage B, dry** (forays.md §7):
- The interpreter on about thirty fixed intents is scored against routes drawn by hand: plain, vague, naming known places, naming
  unknown ones, too long, a party, a search. It adds no stop the intent did not ask for.
- A guard test: the interpreter's request holds no population, stock or unseen state.
- Units are spent as the route says. A route too long ends in a night out; the party moves at the slowest.
- Every story line maps to an event, and replay with the recorded replies is exact.
- A person who named a place in memory reaches it again by name; one who did not keep it cannot.
- A foray to a wild area meets stage A's far target. The interpreter's cost a foray is logged.

**Gate:** the above, and a short dry-run report to Zach; then a small live run if he allows one, read against forays off.

## Why

- **Zach (9 Nov):** hunting should be very labour-intensive and uncertain, with a high skill ceiling that is hard to reach.
  Farming gives far more food per land and scales with people and capital. "The distance they can travel (and time spent) and
  thus likelihood of finding animals depends on how many units". Forays are to be described in the person's own words, with a
  small model translating.
- **02zzd:** the built take cannot reach those targets by any parameter, because time spent never counts. Stage A fixes the rule;
  stage B gives it places.
- **Why this brief next:** of the first packs, K0 to K2 are built. K4 waits on fen worlds with people. K3's core (forays) is what
  everything else in K3 rides on. The hunt's calibration has to be in before any world leans on wild food: the descendants
  benchmark's lowest rung (OPEN L-104) does.

## Alternatives considered

- **Calibrate the numbers only:** meat, constants and the curve. That reaches the near targets but never the far ones; range would
  still lose.
- **Forays without stage A:** the foray's searches would inherit the same one-meeting rule.
- **The story by the small model:** more varied, but harder to keep grounded and replayable. It can come later if the templates
  read badly.

## Open questions (for Zach)

1. The defaults in §4 (Q-33).
2. The meat scale (§2.5): one meat is about 3 kg, from the cow's 40.
3. Whether the far novice's target (about 0.5 a unit, against 0.1 to 0.2 near) is right. Untouched wild land is easier for anyone,
   but a novice also wastes travel.
4. The go for 37.4 to build stage A, then B.

## History

- 10 Nov 2026: Zach: the story's content (signs, encounters, outcomes, reasons and paths not taken); every foray returns home for now (§3.6 and §3.8 give way: no night out). His route module (forays.md History) may move stage B into its own design; awaiting his answer.
- 10 Nov 2026: written by 37.2 as brief 4, from 02zzd's measurements, forays.md and 02zv's K3, at Zach's request ("of the phases /
  stages / packs to develop, which should be the next briefs ... Write up the next brief").

## Sources

[forays.md](forays.md); [methods_and_encounters.md](methods_and_encounters.md) (brief 1, D2-204);
[wild_raiders_and_works.md](wild_raiders_and_works.md) (brief 2); [carcass_and_decay.md](carcass_and_decay.md) (brief 3);
docs/review/37_growth/02zzd_hunting_farming_ev.md and 02zzd_ev/; 02zv §2 (C11), §4 (K3); 02zw; 02zx; world/roads.md; D4-12, D4-35,
D4-48, D4-61, D2-4, D2-85.
