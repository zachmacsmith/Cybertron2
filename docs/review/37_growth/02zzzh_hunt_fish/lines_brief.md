# Brief: the founders' seeded lines for every built livelihood (thread W-105)

You are a build subagent of session 37.2 on Cybertron 2. Work ONLY in the git worktree `/home/user/c2-lines` (branch `w105-lines`,
made from `main`). Never edit the main checkout. Do not push or merge. Commit on the branch in small commits; each message's last
paragraph is exactly:

```
Agent: 37.2
Thread: W-105
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

No other trailer lines. No model calls, no live runs, no Hugging Face; bot runs only to test interfaces (D2-298).

## The problem

u9 §5.5 designs the seeded lines for fifteen livelihoods, but stage 4 (W-100) built templates in `cybertron2/engine/founders.py`
only for BS, PE, HH, FI and SA, and neighbour lines (`NB`) only for the fisher, salter, farmer and herder. `livelihoods.ROWS` already
names FA, HE, HU, SM, MI, BU, WO, BA, CO, TR and CT ids (and FI13, FI14), and `founders.render` drops any id without a template
silently, as "skipped". So a farming, herding, smithing or milling household today gets the base and household lines and nothing
of its craft. Zach (23 Nov): "seeded memories weren't built for all the different livelihoods and crafts and only fishing / salting?
Can you build this out now."

## Read first

- CLAUDE.md; `docs/cybertron2/proposals/w73_design/u9_people.md` §5 in full (5.1 how a line is written, 5.2 the cap and drop order,
  5.5.1 to 5.5.15, 5.6 the holdings line) and its opening "Decisions since" table, which binds over its text; `u11_worlds.md` §2 to
  §4 (who gets what; the holdings registry) and its "Decisions since" table; `basis.md` (keeping words, units).
- `docs/review/37_growth/02zzzh_hunt_fish/wave4_people.md` (the earlier drafts of these rows, with their sources).
- The code as it is: `engine/founders.py` (templates, `Ctx`, `wanted`, `render`, `protected`, `DROP`, `KEEPER`, `SOURCE`),
  `engine/livelihoods.py` (`ROWS`, `HOLDINGS`, `fill`, `livelihood_line`), `engine/lore.py` (`sowing_times`, the pattern for a
  tested template), and the tests that pin the FI and SA lines (`tests/test_cybertron2_stage4_people.py`, `test_cybertron2_kept.py`).
- `docs/cybertron2/guides/senses.md` only for wording (lines are memories, never directions to act; D2-269).

## Build

1. **Every template of u9 §5.5 for the built livelihoods:** farmer (FA1 to FA11), herder (HE1 to HE8), hunter (HU1 to HU8), salter's
   missing rows (SA6, SA7), smith (SM1 to SM6), miller and baker (MI1 to MI5), builder (BU1 to BU8), woodsman (WO1 to WO5), basket
   maker (BA1 to BA5), cord and nets (CO1 to CO5), trader (TR1 to TR4), cottager (CT1 to CT4), the fisher's FI13 and FI14, and a
   neighbour line `NB` for every built livelihood. **Not** the fowler (FO, D2-318) or the tanner (TA, D2-327): deferred; leave their
   ROWS as they are.
2. **Filled from the engine, never invented (D2-268; CLAUDE.md "take data tables from the engine").** Every figure, season, keeping
   time, rate or place in a line is read from the engine's data or the world's state at build (ITEMS, the techniques, the keeping
   curve via `keep_words`, the covers, the world's places and buildings). Before writing each line, check its claim against the code.
   Where the design's wording is false against the engine (a ratio, a season, a keeping time, what a craft needs), write the line to
   the engine's truth, and list each such change in your report with the design's words, the engine's fact and the file:line.
3. **Conditions** as the rows mark them (`[fields]`, `[a mill within a day]`, `[built: x]`, ...): a false condition drops the line,
   reported in `skipped`, never a stand-in. A `[built: x]` whose x the engine lacks drops the line; say which in the report.
4. **Wire the ids into `ROWS`** where u9 puts them (bands B, C, Y, the specialisms' `lines`, `keeper_lines`, `second`), keeping the
   existing FI and SA wiring as it is. Keeper lines (each holding's line in `HOLDINGS.keeper_line` and `keeper_lines`, e.g. FA7, FA9,
   HE7, SM4, MI3, MI5, BA5) join `KEEPER` so they are protected. `SOURCE` gets each new prefix.
5. **The cap and drop order (u9 §5.2, D2-308, D2-340):** every founder fits 20 lines, 40 words a line, about 800 words, by the drop
   order as built (including step 6, a broad livelihood beyond its first line when a deeper band is held elsewhere, if it is not yet
   built). A set over the cap after the last step is a gate refusal, as now.
6. **Tests (D2-268):** each template renders on a fixture world and each stated figure is checked against the state or data it
   names. Build a small mixed fixture village in the tests (through `livelihoods.fill`, or by hand as the stage 4 tests do) holding
   each built livelihood at least once, with its holdings (a mill, an oven, a forge, fields and an ox pair, a herd and a cellar, a
   withy bed), so every template fires; and one with the conditions false, so each drops. A test that every id named anywhere in
   `ROWS` for a built livelihood has a template (so nothing is silently skipped again). A test that every founder of the fixture
   fits the cap.
7. **Eelmouth unchanged in substance:** regenerate `specs/nutrition/eelmouth.yaml` and `eelmouth_small.yaml` only if a line they
   hold changes (FI13, FI14 and the neighbour lines may now appear); first check regenerating is byte-identical before your change,
   and report the diff of seeded lines per person after it.
8. **The suite** in six shards (`ls tests/test_cybertron2_*.py | split -n r/6`), all passing; a 4-day bot run of Eelmouth
   (`python3 -m cybertron2.engine run cybertron2/specs/nutrition/eelmouth.yaml --days 4 --out <scratch> --bots runs`).

## Report

`docs/review/37_growth/02zzzh_hunt_fish/lines_report.md`, committed: per livelihood, each line as rendered on the fixture (the text),
what it reads, its condition; every place the design was corrected to the engine's truth; what was dropped for want of a built
thing; the cap per founder role on the fixture (lines and words, which drop steps fired); the Eelmouth diff; the suite count. List
anything that needs Zach's choice as a question with a recommendation and the default you took.
