# 02zzs: the wild region's 30-day live run (10 Nov), written up

37.2's subagent, 20 Nov 2026 (WORK W-29). Zach (20 Nov): "Get a subagent to revisit and do a writeup, see if it can find our
transcripts from around then too, and what we found / what engine gaps were there." Read-only. No model was run. The world's
design and its dry run are in [02zze](02zze_wild_region.md). This note covers the live run. **Measured** means I read it from the
run's own files. **Said** means it comes from the session's replies of 10 and 12 Nov and I did not re-derive it.

## The world as run

- **World:** `cybertron2/specs/make_wild_region.py`, seed 7, generated on 10 Nov at 06:21.
- **Branch:** run on `ecology-hunt2` (wild briefs 1 to 4b), which was merged into main on 16 Nov (7ddc1c8).
- **How it differs from 02zze's tables:** those describe an earlier generation (winter, 31 who act). The world that ran differs in
  three ways:
  - smaller households (3933be8);
  - the default 32-day lifespan, after a first start at 96 days was cancelled on day 5 at $12.90 (a253d9e; Zach: "No I want
    lifespans on the default of 32 days");
  - an autumn start, with the houses stocked with firewood (53fc52b).

| Village | Households | People | Supported at standing (ratio) | Role |
|---|---|---|---|---|
| Corneby | Holt (Opus only), Wood (carriers: Fable 5.2 head, pack oxen), Carter | 14 | 2.64 | granary, crossroads |
| Weirford | Moor (water mill, smith), Dyer (carriers, an ox) | 8 | 0.83 | river, fish, salt by trade |
| Holtham | Cotter (the growth family's memory), Wright (Haiku only) | 7 | 0.73 | timber, game |
| Stanmoor | Hayward (smiths), Hunt | 8 | 0.72 | the only copper |
| Region | 9 | 37 | 1.46 | |

The table is measured from `wild_region.summary.json` and `run.json`.

- **Frontiers:** three, each with wild nodes:
  - the east wildwood and hills (Fleetby, Watby);
  - the north-west fells (Craghurst, Flintley, Scarley);
  - the south-west saltmarsh coast (Fenmouth), the only source of salt.
- **Seats at the start:** Opus 10 (7 heads and three more Holts), Sonnet 5, Haiku 17, Fable 5.2 1 (Ivo), and 4 young children with
  no model.
- **Settings:** 30 days, starting on autumn day 1, with 8-day seasons, the `wild` pack, and 8 workers through Claude Code.

## What happened (measured)

| | Value | Source |
|---|---|---|
| Days, cost | 30; $75.01 (the Hub's index line says $75.02) | `live_run.log` |
| People | 37 at the start, 1 birth (Susanna, to the Cotters on day 6), **29 alive at the end** | `days.jsonl`, `state.json` |
| Deaths | 9: old age 5 (Petronel, Juliana, Clement, Herbert, Colin; aged 38 to 49 days); starvation 2 (Thomasin and Sibyl, both of the Haiku-only Wrights at Holtham, on days 22 and 23); a brown bear at its kill 1 (Gervase, Stanmoor, day 19); a sudden illness 1 (Edith, Weirford, day 8) | `state.json` causes |
| Seats of the dead | 6 Haiku, 2 Opus, 1 Sonnet | `state.json` |
| Agreements | 20. 9 crossed villages: Corneby–Weirford 7, Corneby–Holtham 2, Stanmoor none | `events` (trade) |
| Thefts | 3 | `live_run.log` |
| Road legs | Corneby–Weirford 12, Corneby–Holtham 8, Weirford–Scarley 4; **none to or from Stanmoor** | `days.jsonl` departed |
| Hunting | 48 "hunting in the wild" and 6 stalks worked; 40 hunt results, **every one "came on nothing" or "got away"** | `events`, `turns.jsonl` |
| Set things | 17 snare lines, 8 water traps | `events` |
| The wild and the herds | murrain in the Holtham herds (days 14 to 17); kills of cattle in the night at Holtham and Stanmoor (days 19 to 25); frost on Corneby's barley (day 9); blight at Holtham and Weirford (days 20, 23) | `events` |

The machine was recycled twice during the run. Both times the run resumed from its journal (the segments table has 4 rows) and
replayed the recorded days free.

## Against the null arm

**None was found for this world.** The bot dry run in 02zze (14 days with bots kept at home: 3 deaths, all at Stanmoor) ran on
the earlier generation, which started in winter with 31 who act. Its output folder now holds only 6 days (`scratchpad/region_dry/`).
The only bot run on the world as run is a 2-day start check (`scratchpad/live_check_out/`). So the 9 deaths and the Holtham famine
have no matched baseline.

A matched arm would cost nothing: the same `wild_region.yaml` with `bots=True` for 30 days, on the `ecology-hunt2` checkout
(`scratchpad/hunt2/`). I did not run one, since this task was read-only.

## What the run found

Facts are measured. The readings come from the session's analysis of 10 Nov, which I spot-checked against the data.

1. **The food did not move.**
   - **Corneby's grain stayed home.** Its harvest overflowed into granaries, bins, a new room and storage paid for in grain.
   - **Holtham starved next door.** Help reached it only as wages: Ellen reaped at Corneby for grain.
   - **No ox ever carried food to Holtham.**
   - *Reading:* each household planned against its own store. That store had been sized to the harvest plus seed, so Corneby's
     surplus came after the famine had peaked, and no one at Corneby saw the famine until Durand visited on days 17 to 19.
2. **The two Holtham households differed by cast, and so did their deaths.**
   - The Haiku-only Wrights ate their seed, asked only next door (on day 20), and lost two to hunger.
   - The mixed Cotters slaughtered and dried a calf, salvaged dead cattle, earned wages at Corneby, and lost no one.
   - *Reading:* one pair of households, so this is an anecdote, not a model effect.
3. **Stanmoor was cut off.** No road leg in 30 days. Copper stalled for want of charcoal, which only Weirford knew, 3 days away.
   Matthew proposed the walk on day 6 and Juliana deferred it.
4. **The carriers traded, and few others did.**
   - Ivo (Fable) was in 6 agreements and led the oxen on every leg.
   - His forward order of 3 copper tools from Herbert ended with 1 still owed when Herbert died.
   - On day 28 he took 60 grain from outside the Holts' door, and returned it with an apology.
5. **No one formed a couple.** The seeded couples were near the end of their fertile window. The one birth was the growth family's,
   and there was no `partner` act. *Said:* the cause was the maker's start of -26 against the 32-day lifespan, and `ages: true` was
   not set.
6. **Prices formed.** Coin was worth about 3 grain, a copper tool 10 to 18 grain, salt 4 grain, and hay 2.5 to 5 grain. *Said*, from
   the trades.

## The engine gaps, and their state on main (20 Nov)

| Gap | Found | State now | Evidence |
|---|---|---|---|
| **No loan of goods.** A plough "lent" became a sale (day 13: "10 grain; 1 wooden plough"); Jordan later rented oxen by spoken terms | 10 Nov | **Open** | D2-40's `loan` preset is money with instalments; there is no hire or return-of-goods preset in `spec/economy/agreements.md` or `engine/agreements.py`. D4-114 (8 Nov) lets anyone work a beast that is there, which is not a lend. No OPEN row: 02zzp period_b notes the gap "never reach[ed] OPEN". I did not test whether "give a plough, get the same plough back by a day" is accepted as an offer |
| **Hunting never killed** | 10 Nov | **Partly fixed** | Brief 4c (`proposals/hunt_calibration.md`) was written from this run, built 14 Nov, merged 16 Nov (7ddc1c8) and accepted as built (OPEN Q-46 a). The baseline-times-multipliers form is in `wild/methods.py` and `engine/wild.py`. On this world (80 tries a cell), an armed novice near home takes 0.29 food a unit and kills on 23% of trips (bare-handed, 12%), against a target of about half. Q-46 (b) to (d) and L-113 are still open. Not yet re-run with agents on this world |
| **Snares never lifted**; the remembered "empty" was taken as fact | 12 Nov | **Fixed in code** | Brief 4c §4: the setter sees a catch at the parcel, and the remembered line says "empty" only if it was seen so (`engine/things.py` 276 to 370, `engine/perceive.py` 236, 422). Untested live here |
| **The engine remembers and settles for agents:** state snapshots, a perfect agreements ledger, automatic payment | 12 Nov | **Open, deferred** | OPEN L-106 (major, not decided) |
| **Debts of the dead:** Herbert's agreement with Ivo, one tool owed, stays open | 10 Nov | **Open** | `engine/agreements.py` `_present_for`: "nothing is paid to the dead"; no heir or estate rule; no OPEN row found |
| **No news of famine reaches the rich village** | 10 Nov | **Open** | No row of its own. The peoples run's "news of a death does not spread" is in OPEN Q-43 |
| The maker: the seeded couples' and carriers' ages, `ages: true`, stores only to the harvest, Stanmoor's distance from charcoal | 10 Nov | **Open** (world, not engine) | `make_wild_region.py` is unchanged since 53fc52b (10 Nov); the same questions for the peoples worlds are in OPEN Q-43 |
| The generator's speed (02zzf) | 10 Nov | **Open** | None of the fixes is built (02zzp records.md row 5); the landgen commits since then are unrelated |

## What is left

1. **A matched bot null arm.** It is free, and it would turn this note's numbers into a comparison.
2. **OPEN rows for the gaps above that have none:** goods loans, debts of the dead, and famine news. Adding them is a records step,
   which this read-only task does not cover.
3. **Publishing is already done.** Zach asked on 10 Nov ("Also upload to hugging face"). The run is `runs/wild_region_s7` in
   `zachmacsmith/cybertron2-runs`. I checked it read-only on 20 Nov: 55 files, covering the journal, views, viewer, run and manifest.
   Its index line is committed (ec00276). W-29's "publish on Zach's go" is stale. Any republish, for example with this note linked,
   needs his go.
4. **A rerun after brief 4c and the maker's fixes.** That needs Zach's go, and it is paid.

## Sources

- **The run (in the scratchpad):** `/tmp/claude-0/-home-user/7e098288-bcf5-5d91-98fd-74db17ae2c32/scratchpad/live_region/`:
  - `live_run.log`;
  - `run/`: `run.json`, `days.jsonl`, `turns.jsonl`, `state.json`, `run.db`;
  - `ev_region.json`, 12 Nov.
- **The world:** `wild_region_new/wild_region.summary.json`.
- **The bot runs:** `region_dry/`, `live_check_out/`.
- **The transcript:** `/root/.claude/projects/-home-user/7e098288-bcf5-5d91-98fd-74db17ae2c32.jsonl`, 10 Nov 04:29 to 08:01 and
  12 Nov 21:14 to 21:49.
- **Commits:** 6702cd7, d97811b, 21a939b, 3933be8, a253d9e, 53fc52b, 13dc39c, ec00276, 893f6a1, 7ddc1c8.
- **Documents:**
  - 02zze, 02zzf;
  - 02zzp_audit/period_b.md, 02zzp_audit/records.md;
  - 02zzr_triage.md;
  - proposals/hunt_calibration.md;
  - OPEN Q-43, Q-46, L-106, L-113;
  - D2-40, D4-114.
