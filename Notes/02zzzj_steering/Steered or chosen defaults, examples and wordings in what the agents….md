---
id: docs/review/37_growth/02zzzj_steering/steering.md
kind: note
updated: "2026-11-22"
---
# Steered or chosen: defaults, examples and wordings in what the agents do, and neutralising fixes tried by replay

*note · `docs/review/37_growth/02zzzj_steering/steering.md`*


22 Nov 2026, 37.2 (review subagent), thread [[W-84 Behaviour steered by defaults, examples and wording|W-84]]. Asked by Zach (22 Nov): "analysing runs to try and find other common behaviors
of things that were / weren't done either due to defaults, examples or simple prompt wordings and trial targeted fixes to
neutralise these sorts of effects so the agents are deciding as much as possible themselves", with the firewood fallback and the
neutral-against-today wording (38.79) as his examples. A session note: nothing decided, no engine, proposal, spec or record edited.

## The short answer

- **The fallback is the biggest steer still live.** It did 33% of all acts done in the river run (20 Nov) and 57 to 60% in the
  lake runs; 56 to 66% of Haiku 5.5's. Its first act is firewood more than anything else, and it names firewood on 62% of mornings
  whose house holds fuel for over 80 nights, against 78% under 10: it does not follow need, where the plan's own acts do (6%
  against 11%).
- **The example "(say, gather firewood)" is not what holds it there.** Dropped, 5 of 12 replayed fallbacks name firewood against 7
  and 7, a shift inside the noise of two identical draws (4 of 12). Firewood was the agents' own filler before the field existed.
- **The fallback fills a real gap.** With no fallback at all the plans named 2.8 of 4.9 units, no more than with it: about two
  units in five would go unused. So the fix is the form, not the deletion: a standing fallback, shown each morning beside what it
  did and what the store holds, asked for until set ([[L-142 Fallbacks as a person's standing setting|L-142]]).
- **The question's word is the answer's word.** The evening asks "what you mean to do tomorrow"; 70 to 87% of evening whys say
  tomorrow, 33% once the word is dropped. 38.79's "today and further ahead" is a counter-lean, not neutral: it doubles the why and
  "today" is echoed more. The neutral wording is the word dropped ("what you mean to do and why"); it costs nothing, keeps the
  why's length and leaves the day's acts as they were. Opening the horizon made more people stock firewood for the cold (10 and
  11 of 12 against 7).
- **For the memory types, take the no-horizon wording for every line that asks for an intent** (the why lines, the closing, the new
  core's reply) and keep the lines that describe the turn (units today, seen tomorrow morning); keep keep_change for the memory,
  not the forward-looking variants (§4).
- **Smaller live steers:** "the village" is the one described attend target and the most chosen; "push on" (listed first) is 80%
  of travels; the evening's list is answered item by item every night (doors barred again and again though a door stays barred,
  sleep stated in 92% of evenings); offers copy their example's form ("work 1 days").
- **Already fixed or not current:** the day's options list ([[D2-286 The list of what one could do today|D2-286]]; `view: beliefs` shows none); the river run's scored goal ([[C-12 The river run seeded a scored goal|C-12]],
  not in the current runs world).
- **111 model calls** (Opus, Sonnet and Haiku, nine models), weekly window 80% to 82%.

**Files here:** `load.py` (reads the published journals), `survey_fallback.py`, `survey_fallback_models.py`, `survey_fuel.py`,
`survey_all.py` (the surveys; their outputs `*.txt`, `*.json`), `render_now.py` and `rendered_now_runs_high.txt` (the runs world's
system prompt and day-0 morning as the code renders them now), `probe_lib.py`, `probe1_fallback_horizon.py`,
`probe2_evening_horizon.py` (the replays; raw results `probe1.jsonl`, `probe2.jsonl`, logs `probe*.log`), `read_probes.py`,
`read_units.py` (the tables below; outputs `probes_read.txt`, `probes_units.txt`, `probes_flips.txt`); `survey_planlength.txt`.

**Runs read** (dataset zachmacsmith/cybertron2-runs, read only; the journals' recorded system texts, messages and replies): the
river run `water_runs_models_r1` (20 Nov, 1,256 morning plans, nine models), `water_lake_r1` and `_r2` (16 and 17 Nov),
`pw1_opus_sonnet_r1` (13 Nov), `e2_labour`, `p1_brookend` (8 Nov), `orwell`, `takeover`, `violent_opus` (7 Nov), `f1_frontier`,
`wb2_wenbridge`, `c3_combe_rich` (4 Nov): 5,656 morning plans in all (3,345 evenings counted in the river run, lake r2 and takeover). No run is on disk in
`runs/` (lost with the container, [[L-147 Live runs kept durably as soon as they finish|L-147]]); the [[W-82 The building clock's first stage read with bots|W-82]] bot runs in `/home/user/c2-w82` have no model replies.

## How each finding was checked against later fixes ([[D2-287 Reviewing past runs|D2-287]])

- **The view.** Every run read uses `view: beliefs` but `pw1_opus_sonnet_r1`, which has no `view` key and so the old
  `prompt.turn_prompt`: all 1,637 of its mornings carry "Today you could"; none of the 4,019 mornings of the other runs does. Any
  finding that needs pw1 is marked *old prompt*, and the options list itself is reported as fixed ([[D2-286 The list of what one could do today|D2-286]]: removed from the code;
  as of today `prompt.py:790-796` still holds it, reachable only through `view.py:175-176` at no place).
- **The wording.** `git log` on prompt.py, view.py, evening.py, memory.py since 13 Nov: the reply format (REPLY_LINES), the why
  line, "Plan your day.", the evening's why and the memory request are unchanged; the commits since touched numbers (the food
  values, [[D2-258 The food values are put on one physical basis|D2-258]]/259, 20 Nov), the weir's words and settings. Checked the other way too: the river run's recorded system text
  contains today's REPLY_LINES verbatim (up to "tell"), its evening message today's why line, its memory request today's
  keep_change and KEPT_ASK text. So the river run's prompts are, in wording, what the code renders now;
  `rendered_now_runs_high.txt` (the runs world `specs/nutrition/runs_high.yaml`, rendered today) carries the same reply format
  word for word, the same closing line and the same house line ("fuel for about 77 such nights").
- **The engine.** The fallback still runs as in the runs: up to three acts, tried in order and again until the units are used
  (`run.py:1036-1056`, [[D4-76 A fallback each person sets|D4-76]]). Fixes since the runs that could change a finding are named on its row.
- **Not live in the current runs world:** the river run's seeded scored goal ("YOUR GOAL, on which you will be graded", in 515 of
  its stretch openings; [[C-12 The river run seeded a scored goal|C-12]], open, 37.4's), which `runs_high.yaml` does not carry. It is the strongest steer found in any run, but
  it is known and not repeated here beyond a note: it sits in every probe-1 point's kept lines, the same in every arm.

## 1. Survey: what looks steered

Confidence: **high** = a count that cannot come from the world alone and a prompt text that names it; **medium** = a count and a
plausible text; **low** = a pattern worth a probe.

### 1.1 The fallback fills a third to two thirds of the day, and it is mostly firewood whatever the store holds (live; high)

- **How much of the day it does.** Of the acts done (the evening's "Your day" lists, refusals left out), the fallback did 33% in the
  river run (1,979 of 5,955), 57% and 60% in the lake runs, 39 to 53% in the 7 to 8 Nov runs (`survey_fallback.txt`). By model
  (`survey_fallback_models.txt`): Haiku 5.5 56% (river), 61 and 66% (lakes); Sonnet 5.5 50%, 48%, 71%; Opus 5.5 32%, 52%, 36%;
  the older and other models of the river run 17% (Opus 5) to 45% (Opus 4.5). The plan itself names about 2 to 3 work acts for 5
  units (`survey_planlength.txt`: Haiku 5.5 1.8 work acts for 5.3 units, Opus 4.5 1.9 for 5.2): the rest is left to the fallback.
- **What it is.** It is written in 98% of plans (1,227 of 1,256 in the river run). Its first act: firewood 444, wild food 297, fish
  by hand 89, rest 52 (river); across the 7 Nov to 20 Nov runs firewood is first in every run but the lakes, where wild food leads.
  Of the fallback's done acts, firewood was half in the river run (982 of 1,979).
- **It does not follow need.** The house line tells everyone how many nights of fuel the store holds. In the river run the
  fallback named firewood on 78% of mornings with under 10 nights of fuel and still on **62% with over 80 nights** (259 mornings;
  houses held 100 to 200 firewood from day 10 on). The plan, which they choose act by act, named firewood on 11% and 6%
  (`survey_fuel.txt`). The lakes and the 7 Nov runs show the same flat line (40 to 80% across every band). What they choose
  deliberately follows the store; what they set as filler does not.
- **What names it.** The reply format's only example: `"fallback": [actions] what to do with units left over if an act is refused
  or the plan runs out (say, gather firewood)`, in every system text read since the fallback was built (11 of 11 runs with a
  fallback; none in c3, which predates it). But firewood was already the agents' own filler before the field existed: in c3 (Opus
  5.5, no fallback field, no example) 24 whys say "firewood is the fallback" ("Firewood is the fallback once the crop is in"), and
  that is where the example came from (proposals/fallback.md, Why). So the example and the habit reinforce each other; the probe
  (§3.1) finds the habit does most of it (the example dropped: 5 of 12 against 7 and 7).
- **Why it matters.** Firewood is the cheapest act that is never refused (a wood is always near, it never runs out in a day), so as
  a filler it is rational, and with a longer horizon some of it is foresight (§3.1 reading 3); but a filler that fills half of
  Haiku's day and is the same in a full and an empty house is set by the form (one slot, written once, repeated until the units are
  gone, never shown beside what it did), not decided against the state each day. [[L-142 Fallbacks as a person's standing setting|L-142]] (Zach, 21 Nov: "everyone seems always to fall back to firewood") has it waiting on
  the standing rules ([[W-37 Standing rules|W-37]]).

### 1.2 The horizon follows the word in the question (live; high for the evening, medium for the morning)

- **The evening.** The evening asks `"why": what you make of the day and what you mean to do tomorrow.` Its whys say "tomorrow" in
  87% (river), 81% and 84% (lakes), 70 to 79% (7 to 8 Nov runs); a long horizon (season, winter, year, generations, weeks) in 12%,
  9%, 6% and 1 to 7%. The morning whys of the same runs say "tomorrow" in 1 to 11% (`survey_all.txt`). The word asked for is the
  word given, nearly every time.
- **The morning.** `"why": a sentence or two on what you mean to do today and why` and the closing "Plan your day.": the river
  run's whys say "today" in 40% (others 8 to 15%) and a long horizon in 19% (others 7 to 22%). 38.79 replayed seven day-1 openings
  with the why opened to "today and further ahead" and the closing "Decide what to do.": the whys tripled in length and named
  seasons, the day's acts were unchanged within noise, notes doubled.
- **Caution on 38.79's "neutral":** its wording ("today and further ahead") names a longer horizon; it is a counter-lean, not
  neutral. §3 tries both: the counter-lean (H) and the word simply dropped (N).

### 1.3 "the village" is the one attend choice with a description (live; medium)

`"attend": ... "the village": how the place fits together, what lies next to what and where the ways out leave.` Of the river
run's 1,256 attends, "the village" is the most chosen single target (84; then fields and houses at 30 to 49); 56 of 327 in lake r2
(17%), the first or second choice in every run. 14 of the 25 river agents who chose it chose it again, one 17 times, though the
village's layout does not change. The other specials ("the sky", "the place in general") carry no description and are chosen a
few times. No order effect in the attend list (people come first in the enum and are chosen least).

### 1.4 The offer examples are copied as syntax (live; low as a steer)

`Goods as "2 bread"; a promise as "1 copper tool by day 10"; payments as "2 grain every 3 days for 4 times"; work as "work 2
days".` 300 of 941 offers give work in that form, written "work 1 days" 142 times in the river run (the example's plural kept with
the number changed: a template filled in). "2 grain" is the commonest thing asked for (86). Labour offers are a real choice the
world offers and need a form; the copying shows the form is read as a template, not that labour is chosen because of it. Low.

### 1.5 First in the list: "push on" (live; low to medium)

`"on trouble"?: push on | wait | turn back | go round`: of 805 travels, 573 push on (80% of those that set it), in that enum order in
both the verb line and the schema. Pushing on is a reasonable first choice; whether its place in the list adds to it is untested.
The `meeting` choice (stop | pass by) is not one-sided (380 to 219).

### 1.6 Defaults never changed, and settings re-chosen every night (live; medium)

- **Overwork**: 0 in 2,328 of 2,382 replies that set it (98%); the field invites an explicit 0. Not a steer toward anything, but
  pushing on is all but never chosen.
- **The door**: 967 "set door barred" against 5 "open" across the runs, 335 in the river run: a door stays barred once set
  (`world.py:611`, `verbs.py:2006`), yet people bar it again night after night. The evening lists "set the door" among the night's
  acts; the house line shows "door open" at the opening. A re-asserted setting, cost nothing; it shows they read the evening's list
  as things to do each night.
- **Sleep**: 3,085 sleep acts in 3,345 evenings of the three newest runs, though one sleeps at home by default
  (`night.py`, [[D4-36 Moving is general, not a feature|D4-36]]). The same: the evening's list ("sleep, host, grant, ...") is answered item by item.
- **Who eats, from which store**: never chosen, because there is no choice: the night's eating order is the engine's
  (spec, [[D4-36 Moving is general, not a feature|D4-36]]); it is the standing rules' work ([[W-37 Standing rules|W-37]], [[D2-274 One book of standing rules per household and per person covers both…|D2-274]]). Not a steer, an absence.
- **Children's work** (`order`): 17 uses in all runs; heirs (`name`): 90. Rarely set; the prompt lists them.

### 1.7 Never tried, though offered (live; medium)

Across 5,656 plans: `write` and `erase` 0 (offered in every system text read), `found` 0, `leave_household` 0, `part` 0, `meet` 5,
`join` 7, `admit` 14, `watch` 18, `claim` 23, `explain` 14, `look_up` 47 (0.8%). Not steering by a word: these are offered as
plainly as the rest. What they share is that nothing in the morning points at them (no state line says a household is crowded, a
wall is blank, a meeting would help) and the reply format describes the daily fields at length. "Pull does not happen" (37 §3.3)
holds for verbs too. The fix is not wording; it is signs and seeded knowledge (wave4 §3) that make them worth choosing, and is not
pursued here.

### 1.8 Already fixed or not current

| Finding | In | Status now |
|---|---|---|
| The day's options list ("Today you could") decided 87% of work (37 §3.1) | d1_duo; pw1 (old prompt) | fixed: `view: beliefs` shows none; removed from the code by [[D2-286 The list of what one could do today|D2-286]] (still in prompt.py:790-796 until the rebuild; reachable only at no place, view.py:175-176) |
| pw1's fallback led by wild food (858 of 1,564) | pw1 | old prompt, with the options list; not read as evidence |
| The scored goal in kept lines (36% of kept lines) | river run | [[C-12 The river run seeded a scored goal|C-12]], open (37.4's); not in the current runs world |
| Memory restarts with each schema change (37 §7b) | d1_duo | not re-read here |

## 2. Fixes: one each, with what it costs

| # | Steer | Fix | Cost |
|---|---|---|---|
| F1 | the fallback's example names firewood | drop "(say, gather firewood)" from the reply format | none |
| F2 | the fallback fills half of a weak model's day with one habit, the same in a full house and an empty one | make the fallback a standing setting ([[L-142 Fallbacks as a person's standing setting|L-142]]): "what you do with units left over, until you change it", shown each morning with what it did yesterday ("Your fallback, gather firewood, took 3 units yesterday; the store holds fuel for about 90 nights"), so the filler is seen beside the state it ignores; unset at the start, asked for each morning until set (§3.1 C: with no fallback about 40% of units go unplanned) | one choice once, kept; one morning line |
| F3 | the evening's why names tomorrow | `"why": what you make of the day and what you mean to do.` | none |
| F4 | the morning's why names today; "Plan your day." | `"why": a sentence or two on what you mean to do and why.`; "Decide what to do." | none |
| F5 | "the village" is the only described attend target | describe none in the reply line (keep "the village" in the enum), or describe each special the same way | none or 20 words |
| F6 | the offer examples are a template | keep one example per form, with numbers that differ per person (drawn from what they hold), or placeholders: `"<n> <good>"`, `"work <n> days"` | none |
| F7 | first-listed choices (push on) | rotate the enum order per person (deterministic by name) in the verb line and the schema, or name the default without listing it first | none; a schema that differs by person (already does) |
| F8 | the evening's list answered item by item (sleep, door) | say once that settings stand ("a door stays as you set it; you sleep at home unless you say otherwise") | about 20 words |

F2 is the only one that changes the engine; it is [[L-142 Fallbacks as a person's standing setting|L-142]]'s design and waits on [[W-37 Standing rules|W-37]]. F1, F3 and F4 are words, and §3 tries them
(F1 as B, F3 and F4 as N, and 38.79's counter-lean as H; F2's "no fallback" end as C).

## 3. Trials

**Method** (as 38.79): real prompts from the river run (20 Nov; its wording is the code's wording now: see the check above), each replayed on the
model that played it through `cybertron2/infra/llm.py` (the claude_code backend the runs use), with the fix against without and a
repeat draw (A2) for the noise between two identical calls. The guard stopped at a weekly window of 90%; it read 80% at the start
and 82% at the end (the five-hour window 71% to 85%). **111 model calls** in all: 72 in probe 1, 36 in probe 2, one to read the
window, and about two lost when I restarted the probes in parallel (their in-flight calls); about $17 at API prices. Raw results:
`probe1.jsonl`, `probe2.jsonl`; tables: `probes_read.txt`, `probes_units.txt`, `probes_flips.txt`.

### 3.1 Probe 1: the fallback and the morning's horizon (12 points x 6 arms = 72 calls)

**Points:** stretch openings (a new conversation, so the message is self-contained and carries memory and kept lines) on days 16 to
22, with at least 4 units and a house line showing at least 20 nights of fuel, chosen by a fixed seed and regardless of the
recorded reply: Opus 5.5 (Drew, Hawise), Sonnet 5.5 (Elena, Cecily), Haiku 5.5 (Clement, Odo), Opus 5 (Aldric), Opus 4.5 (Avice),
Sonnet 5 (Alice), Sonnet 4.5 (Rose), Haiku 4.5 (Hamo), Fable 5.2 (Mabel). Their houses held 29 to 113 nights of fuel.

**Arms:** A and A2 as run; **B** the fallback's example dropped; **C** no fallback at all (its reply line and schema field removed);
**H** 38.79's wording (why "today and further ahead", "Decide what to do."); **N** no horizon named (why "a sentence or two on
what you mean to do and why", "Decide what to do.").

| arm | n | has a fallback | fallback names firewood | plan names firewood | acts | investing acts | units the plan names (of 4.9) | left to the fallback | why words | why says today | long-horizon words | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | 12 | 100% | 58% (7) | 25% | 3.6 | 0.42 | 3.25 | 34% | 54 | 8% | 0.08 | 0.50 |
| A2 | 12 | 100% | 58% (7) | 8% | 3.4 | 0.50 | 3.08 | 37% | 48 | 17% | 0.33 | 0.42 |
| B no example | 12 | 100% | 42% (5) | 0% | 3.3 | 0.50 | 2.92 | 41% | 55 | 25% | 0.25 | 0.50 |
| C no fallback | 12 | 0% | | 0% | 3.9 | 0.75 | 2.83 | 42% (unused) | 55 | 17% | 0.08 | 0.33 |
| H further ahead | 12 | 100% | 92% (11) | 0% | 3.6 | 0.58 | 3.00 | 39% | 122 | 58% | 0.58 | 0.50 |
| N no horizon | 12 | 100% | 83% (10) | 0% | 3.4 | 0.58 | 2.92 | 41% | 53 | 25% | 0.42 | 0.50 |

Point by point (firewood in the fallback, against A): A2 differs from A on 4 of 12 points (2 each way), the noise floor. B differs
on 6 (2 to firewood, 4 away): Avice set `rest` in place of firewood, Odo `herd`, Alice care and wild food. H differs on 6 (5 to
firewood, 1 away), N on 5 (4 to firewood, 1 away).

**Reading (n = 12, one draw each, single turns):**
1. **Dropping the example does not clearly change the fallback.** 5 of 12 name firewood against 7 and 7: a shift of two points
   where two identical draws already differ on four. If the example has an effect it is small next to the habit; firewood was the
   agents' own filler before the example existed (c3, §1.1). Keep the fix (it costs nothing and is one less nudge), but do not
   expect it to end [[L-142 Fallbacks as a person's standing setting|L-142]].
2. **Without a fallback the plan does not fill the day.** In C the plans name 2.8 of 4.9 units, no more than A's 3.1 to 3.3: about
   two units in five would go unused, though the system text still says "Any units you do not use are wasted". Drew (Opus 5.5) was
   the one who filled his day (four ploughings); Aldric (Opus 5) added carrying; the rest wrote the same short plan with nothing
   after it. So the fallback is not only a steer: it fills a gap the agents leave every day. A fallback left unset by default
   ([[L-142 Fallbacks as a person's standing setting|L-142]]) would waste about 40% of units unless the morning makes them set one.
3. **Opening the horizon raised firewood.** Under H 11 of 12 fallbacks name firewood, under N 10 (against 7 and 7), and the whys
   say why: "gather firewood for the cold nights", "dry it ... to keep it for the hard weeks" (Orabel, probe 2, N). Looking further
   ahead, firewood becomes stocking for winter, a reason rather than a reflex. One cannot tell here whether the why line or the
   closing ("Decide what to do.", common to H and N) did it. It cuts against reading the survey's flat firewood line as pure
   habit: some of it is foresight with nothing better named to do with the units.
4. **H's words are 38.79's again:** the why more than doubles (122 words against 48 to 55), "today" is echoed more, not less (58%:
   "today and further ahead" is copied), long-horizon words rise. N leaves length and "today" within the A-to-A2 range and
   long-horizon words at the top of it (0.42 against 0.08 and 0.33). The day's acts and investing acts are the same in every arm
   within noise.

### 3.2 Probe 2: does the evening's "tomorrow" carry into the next morning? (6 points x 3 arms x 2 calls = 36 calls)

**Points:** evenings in the middle of a stretch, days 13 to 24, whose next call is the next morning's plan in the same
conversation: Orabel (Opus 5.5), Elena (Sonnet 5.5), Clement (Haiku 5.5), Avice (Opus 4.5), Fulk (Sonnet 4.5), Piers (Haiku 4.5).
Each draw is two calls: the evening (the conversation rebuilt from the journal up to it), then the next morning with the new
evening reply in place of the recorded one. **N** drops the horizon in all three places: the system why line ("today"), the
evening's why ("tomorrow"), the morning's closing.

| arm | evening why words | evening says tomorrow | evening long-horizon words | morning why words | morning long-horizon words | morning acts | morning investing acts | morning fallback names firewood |
|---|---|---|---|---|---|---|---|---|
| A | 79 | 100% | 0.17 | 67 | 0.33 | 3.3 | 0.83 | 67% |
| A2 | 78 | 83% | 0.33 | 64 | 0.17 | 3.8 | 0.83 | 50% |
| N | 65 | 33% | 0.33 | 77 | 0.50 | 4.3 | 1.00 | 67% |

**Reading (n = 6):** the evening's "tomorrow" is the word asked for: with it 83 to 100% of evening whys say it, without it 33%
(the evenings still look to the next day where the next day is what matters: "tomorrow I herd the Wood cattle"). The next
morning under N has a slightly longer why, more long-horizon words and one more act on average, all inside what six points and
two baseline draws can separate. Nothing here shows the evening wording changing the next day's acts; it shows the evening's
words are steered by the question and that removing the word costs nothing.

### 3.3 What a paired run would need

Single-turn replays cannot see what compounds: notes written, a store laid by, a plan carried across a stretch. Two effects are
worth a run: (a) the fallback as a standing setting against today's daily field, read on the share of units done by the fallback,
what it holds by store level, and units wasted; (b) the horizon wording (N) against today's, read on notes, stores at the first
winter, investing acts over a season. The runs world (`specs/nutrition/runs_high.yaml`, 8 acting people, Opus heads, Sonnet
middle, Haiku rest) for 16 days (two seasons, so a winter comes) is long enough. The noise between two identical draws here was 4
of 12 on a yes-or-no reading; to see a 15-point shift in the fallback's firewood share at the person level needs on the order of
20 people-runs an arm: two seeds an arm (four runs of 16 days, or the null arm shared: three). Each such run is roughly 1,500 calls
(water_lake_r2 made 1,220 in 22 days with 11 acting people). Cheaper: fold both as arms into the next runs world run already
planned, with a shared null.

## 4. Memory types: the lines that frame time or choice, and a neutral wording for each

Zach asked whether, when the memory types change (wave4_people.md §1.4, §1.5, §2.6; proposals/knowledge_in_their_own_words.md),
the neutral horizon wording should be taken for the similar lines. My answer: yes, with "neutral" meaning **no horizon named**,
not a longer one named. The evidence: the evening's "tomorrow" is echoed in 70 to 87% of its whys (§1.2); 38.36 found the
forward-looking memory wordings (future_days, future_self) "make plans and lists" but bring "more rewriting from scratch and more
invention", and kept keep_change, which names no horizon ("what you will want later"); and §3.

| Where | Line now (or proposed) | Frames | Recommend |
|---|---|---|---|
| system, How life works | "A day: you plan in the morning ... then you work. ... Any units you do not use are wasted." | the turn (frame) | keep: the day is the engine's turn; "wasted" stays (scenario_design §3) |
| reply format | `"why": a sentence or two on what you mean to do today and why.` | horizon | `"why": a sentence or two on what you mean to do and why.` |
| proposed core reply (wave4 §1.5) | `"why": what you mean to do today, and why.` | horizon (keeps "today") | `"why": what you mean to do, and why.` |
| reply format | `"actions": today's plan, in order` | the turn | keep (the acts are the day's); or "the day's acts, in order" |
| reply format | `"fallback": ... (say, gather firewood)` | an example act | drop the example (F1); the standing setting later (F2) |
| proposed core reply | `"actions": ... as {"do": "snares", "at": "the Common"} or {"do": "lift", "thing": "T12"}` | example acts | replace with placeholders (`{"do": a craft you know, "at": a place}`) or the person's own first craft; the same risk as firewood, now for snares |
| reply format | `"attend": the one thing you pay close attention to today. You will see it in detail tomorrow morning.` | the turn | keep (that is when it is seen); drop the description of "the village" alone (F5) |
| reply format | `"note": ... "pin": a title to show every morning` | the turn | keep |
| morning (view.py) | "## Now ... You have N units of work today" | the turn | keep |
| morning (view.py) | "Plan your day. Reply with JSON only." | horizon, mildly | "Decide what to do. Reply with JSON only." |
| talk | "give your whole plan for the day again" | the turn | keep |
| evening | `"why": what you make of the day and what you mean to do tomorrow.` | horizon | `"why": what you make of the day and what you mean to do.` |
| evening | "Work, gathering and making wait for tomorrow." | the turn | keep |
| evening (plans at the hearth) | "Put tomorrow's plan of work in "actions" too" | the turn | keep |
| evening | the night's list "sleep, host, grant, admit, ..." | invites re-choosing standing settings | say settings stand (F8) |
| memory request | "Tomorrow you will remember only your memory, your notes, what you keep for good and what you have always known" | the frame | keep (it is the frame, and it is true) |
| memory request (keep_change, the default) | "keep what still matters, add from these days only what you will want later, and leave the rest" | neutral | keep; do not move to future_days ("in the days to come") or future_self ("in a season's time") |
| memory request (append mode) | "what happened, what was agreed or promised, who owes what, what you mean to do" | a content list | shorten to "what you want to remember of them" (the list steers memory toward ledgers: 38.36 §6.7 "all instructions hoard mechanics") |
| kept for good | "what you want to remember for good" | the line's nature | keep |
| proposed core line 10 | "a memory you rewrite every few days, lines you keep for good word for word, and notes. Nothing else of past days stays with you." | the frame | keep: it says what lasts, which is what lets them choose a horizon themselves |
| proposed core line 2 | "Any units you do not use are wasted." | the frame | keep |
| seeded lines (founders) | "Hard winters you remember, when the frost came early and the stores ran out: last winter." (the same sentence for 36 of 45 founders, wave4 §2.6) | a lean toward stocking | per household, from the world's history (wave4 §3.3 already proposes it) |

## 5. Questions for Zach

1. **Whether to drop the fallback's example "(say, gather firewood)" from the reply format now** (no id; the reply format is
   37.4's). Options: (a) drop it now; (b) replace it with a neutral placeholder ("acts of yours, in the order to try them"); (c)
   leave it until the standing fallback is built. Recommend (a): it costs nothing and is one nudge fewer, though the probe shows the
   habit, not the example, does most of the work (§3.1: 5 of 12 against 7). Blocks nothing.
2. **How the fallback becomes a standing setting: what happens to units left over while none is set** ([[L-142 Fallbacks as a person's standing setting|L-142]], with the standing
   rules [[W-37 Standing rules|W-37]]). Options: (a) unset at the start, leftover units wasted, the next morning says how many were lost; (b) unset at the
   start, and each morning asks for one until it is set (a forced choice until made once); (c) an engine default (rest, firewood).
   Recommend (b), then (a): without a fallback the agents left about 40% of units unplanned (§3.1, arm C), so an unset fallback
   that only wastes would cost a weak model much of its day before it learns; (c) is the engine choosing, which [[D4-76 A fallback each person sets|D4-76]] rejected.
   Blocks [[L-142 Fallbacks as a person's standing setting|L-142]]'s design.
3. **The horizon wording: drop "today" and "tomorrow" from the why lines and close the morning with "Decide what to do."**, now
   and in the new core (wave4_people.md §1.5's why still says "today"). Options: (a) no horizon named (N: "what you mean to do and
   why"; the evening "what you make of the day and what you mean to do"); (b) 38.79's "today and further ahead" (a counter-lean:
   it doubles the why and is copied); (c) as now. Recommend (a): it removes the echo (the evening's "tomorrow" in 83-100% of whys,
   33% without) at no cost in words or acts, and leaves the horizon to them. Note it may raise firewood stocking (§3.1 reading 3).
   Blocks the new core prompt and the memory types' wording (§4).
4. **Example acts in the new core's reply format** ({"do": "snares", "at": "the Common"}, {"do": "lift", "thing": "T12"}, and the
   offers' "2 bread", "1 copper tool by day 10", "work 2 days"; wave4_people.md §1.5). Options: (a) placeholders ("a craft you
   know", "<n> <good>"); (b) the person's own crafts and goods filled in; (c) keep. Recommend (b) for acts (a real word they can
   use, never the same one for everyone), (a) for offers. Blocks nothing now; due when the core is written.
5. **The small steers: "the village" as the only described attend target, the first-listed travel choice ("push on", 80%), and
   the evening list re-chosen every night (doors barred 967 times though a door stays barred; sleep 3,085 times in 3,345 evenings
   though one sleeps at home by default)**. Options: (a) fix all in words now (describe no attend special, or all; rotate enum
   order per person; one line that settings stand); (b) only the attend and settings lines; (c) leave. Recommend (b): cheap and
   clear; rotating enums is untested and changes the schema per person. Blocks nothing.
6. **Whether to pay for a paired run of the fallback setting and the horizon wording** (§3.3). Options: (a) fold both as arms into
   the next runs world run, with a shared null (three runs of 16 days); (b) a run of their own now; (c) no run, decide on the
   replays. Recommend (a). Blocks only knowing whether the wording compounds over days.
