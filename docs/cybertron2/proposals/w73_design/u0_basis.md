# U0: the basis in code (stage 1)

**Status:** discussion; written by 37.2 in the integration review (23 Nov 2026), because every other spec defers part of its code to
"U0" and no spec held it. Nothing built.
**Owner:** 37.2 for the numbers and the goods' table; 37.4 for the engine files named (clocks.py, verbs.py, night.py, prompt.py,
view.py, buildings.py), named on any merge.


> **Decisions since this spec was written (binding over its text; the build reads this table first):**
> - **D2-309:** one capital factor for every lasting thing; existing works held until their companions.
> - **D2-310:** lives in nights at 1/11.4; lives in acts at the factor.
> - **D2-313:** 37.2 owns every engine file this wave changes (read every '37.4' in the code tables as 37.2 for this wave).
> - **D2-315:** wild rates still on the day clock stay as calibrated, read in live runs.
> - **D2-324:** a build act costs what is left (1 or 2 units).
> - **D2-327:** tanning and leather deferred until the wave is tested (frame, harness and bellows in leather, tanning's pollution with it).

## Extends

basis.md (every row); spec/core/clocks.md (D2-273, D2-275, D2-276); D2-281 (the factor staged); D2-288 (handling units); D2-289 (the
keeping curve); D2-290 (fuel a night); D2-292 (the food unit); D2-295 (depths as goods); D2-286 (the options list removed); O-2 (the
batches); D2-297 and D2-298 (the catch kept; bots for interfaces); wave1_physical_basis.md §1 to §5 (the tables this draws on).

## Departures

- None from a decision. The function `capital_units` is defined once, as u7 §1 writes it (`capital_units(row, w, n=1)`); u3 §2's call
  `capital_units(hours, w)` and its `batch_of` are read as that function and `batch_of(row, w)` below.

## Purpose

Put the basis into the engine before anything else is built on it, and remove the faults that would confound any reading of the
units built after it. Everything here is stage 1 of the README's order.

## The design

### 1. The goods resized (D2-288)

- ITEMS' `weight` for the bulk goods: timber 25, stone 25, firewood 10, straw 16, hay 10, charcoal 20, withies 10, bark 10 (basis §2);
  food goods as now (about 1 kg a unit; bread 1.4); new goods from u3 (cord 1 kg, hide by beast) and u4 (the cured goods).
- **Every recipe, build, fitting, room, work and ration rewritten in the new units**, from wave1 §1.8's list of what the resize
  touches beyond ITEMS and the cost tables of wave1 §3, u3 §3 and u7 §2. A recipe that read "timber 1" in the old unit is converted by
  what it was made of in kilograms, not by a fixed ratio: the old units were game numbers (wave1 §1.3, §1.4).
- Carrying limits read against the new weights (basis §5).

### 2. Fuel a night (D2-290)

The house's heat need becomes 1 firewood bundle (10 kg) a normal night and 3 on a cold one (`data.py` heat and camping rows); the
kinds of fuel and their heats wait on the timber thread (W-76).

### 3. The keeping curve (D2-289, D2-295)

- Each food's `spoil` is its base rate a night from the curve: nights = min(d, 2) + (d − 2) / 11.4 for a food that keeps d real
  days, "keeps" read as a quarter lost by then (basis §3's rates).
- The cured depths are goods of their own (u4 §3).
- Stores' flat multipliers go (u5): this unit only sets the base rates; u5 removes `house_spoil`, `cellar_spoil` and the fittings'
  `spoil` and puts the named penalties in.

### 4. The clocks (D2-273, D2-276, D2-281)

In `engine/clocks.py`, as u7 §1 defines them: the `CAPITAL` lever (in data.py), `capital_factor(w)`, `capital_units(row, w, n=1)`,
`capital_life(uses, w)`, `night_life(nights)`; and here `batch_of(row, w)`: the most pieces one unit makes, from the row's real
hours a piece and the factor (u3 §2.1). Every capital row carries `hours` (and `uses`); units are never copied at import (u7: W-82's
fault 4). Existing works are held at today's units until their companions are in (u7 stages).

### 5. The floor and the batches (O-2)

`verbs.cost`: every act at least 1 unit; a make of `qty` pieces costs `units x ceil(qty / batch)` (u3 §2.1), replacing the `int()`
truncation that made sub-unit recipes free (`verbs.py:142`, `:156`); a build act costs what is left of the work, 1 or 2 units (u7
§5.4); the eleven bulk processes of O-2 take "up to" their batch.

### 6. The faults that mislead, fixed first

| Fault | Fix | Spec |
|---|---|---|
| the options list ("Today you could", "Not yet") | removed from the code, including the beliefs view's fallback to the old prompt at no place (`prompt.py:790-796`, `view.py:175-176`) | D2-286 |
| the five fishing bugs (Q-79) and faults 6 to 8, 11, 12, 14, 15 | as u2 §3 gives each | u2 |
| a run's fish learning wariness | wariness and pressure for resident animals only | u1 |
| the weir's cost held twice (MONUMENTS and WATER_WORKS) | one copy, at D2-302's numbers | u7; D2-302 |
| sub-unit recipes free | §5 | u3 |
| signs that tell people what to do (five rows) | reworded as observations (D2-269) | u8 |
| the build's practice counted once a work | practice for every build act | u7 §5.2 |

### 7. The wild's rates and the year clock (open)

D2-273 puts the wild's production and regrowth on the year clock; some rates are still on the day clock (u1: `fish` regrows at r 0.3 a
night, wave_conflicts E1). Re-deriving them would make the resident stocks several times richer, against D2-297's catch kept as
calibrated. **Default:** this unit leaves every wild rate as calibrated and lists those still on the day clock; their re-derivation
is read in the calibration live runs with the rest (D2-297). Asked (questions.md).

## Code changes

| File | Change | Owner |
|---|---|---|
| `engine/data.py` ITEMS, TECHNIQUES, FITTINGS, ROOMS, BLUEPRINTS, MONUMENTS, WATER_WORKS, heat and camping rows | §1 to §3; `CAPITAL` | 37.2 (numbers); 37.4 (structure) |
| `engine/clocks.py` | §4 | 37.4 |
| `engine/verbs.py` `cost` | §5 | 37.4 |
| `engine/night.py` spoilage | base rates only; penalties per u5 | 37.4 |
| `engine/prompt.py`, `engine/view.py` | the options list removed | 37.4 |
| `wild/`, `engine/wild.py`, `engine/things.py`, `engine/here.py`, `engine/knowledge.py` | the faults of §6 as u1, u2 give them | 37.2 (wild), 37.4 (core) |

## Tests

Interface tests with bots and unit tests only (D2-298): every recipe resolves in the new units; no act costs 0; a make of n pieces
costs as §5; spoil rates match basis §3; no prompt contains "Today you could"; each fixed fault has its regression test (u2 §3).

## Open questions

1. The wild's rates still on the day clock (§7): leave as calibrated and read in live runs (default), or re-derive in stage 1?

## Sources

basis.md; wave1_physical_basis.md; u1 to u11's "U0" references (u1 §Gaps, u3 §2 and code table, u4 §3 and code table, u5 code
table, u7 §1 and stages, u9 §2.6, u11 B11-7).
