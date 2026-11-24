*The code moved to `cybertron2/peoplegen/` (23 Nov, W-107), bridged into world generation as `population: {build: backward}` (generation_redesign.md §6). This report and its results stay here.*

# Prototype: the past built backward to a pinned present

`docs/cybertron2/proposals/generation_redesign.md` §5 named two risks to settle before build briefs: (1) whether a past built
backward to a pinned present reads as likely, and (2) whether a graph of keyed decisions (fill, backjump on conflict, prefer the
previous world, never reject) works. This prototype tests both, for people only, outside the engine. The c2viz session built it
on 14 Nov 2026 at Zach's request ("prototype it"). Nothing under `cybertron2/` was changed.

Run: `python3 -m cybertron2.peoplegen.evaluate --seeds 40` (about 80 s). The results are in `results/results.json`, the
held-out seeds in `results/heldout_41_80.txt`, and a sample past in `results/sample_seed1.md` and `.json`.

## What was built

| File | What it does |
|---|---|
| `keyed.py` | Keyed draws (D2-70) and the keyed weighted order: Efraimidis and Spirakis, `log(u) / w`. The first candidate is a draw in proportion to weight. Candidates keep their relative order when others come or go. |
| `demog.py` | The forward model's tables (calibrate), read by both directions: marital fertility, mortality with hard years, marriage, the spouse age gap, the marriage market's reach. It also holds the backward weights fitted to the forward run. |
| `forward.py` | The reference: a region of four village sites, simulated year by year for 100 years from six founding couples. Rules: patrilocal; a new household if the village has room, else move to a village with room, found a new one, or (the heir) stay; no house, no marriage; the off-map node. Its present is pinned for the backward build, and its past is the truth to compare with. |
| `present.py` | The present as an input: an explicit list, or a mix drawn into one by keyed draws (per village and household). Forms: couple with children, old couple, widow alone, widower with children, three generations, stem, single man, siblings. Counts are placed exactly; shares fill the rest. |
| `solver.py` | The decision graph: an agenda of keyed decisions, a trail of undoable changes, and conflict-directed backjumping. The previous world's choices are tried first (soft pins). It refuses only when a conflict set holds nothing but pins, and names them. |
| `genealogy.py` | The backward build as decisions: `found` (a village's founding year), `pairs` (who in a household is married to whom), `par` (each person's parents, newest births first: the coalescent order), `age` (a new couple's other spouse), `wid` (a dead spouse for a pinned widow), `death`, and `fill` (the marriage year and the children not living now). Candidates are weighted by the forward model. |
| `stats.py`, `write.py`, `evaluate.py` | The same statistics read from the truth and from the build. A writer in `generate.py`'s format (tree, history, agents with kin from `generate.kin`, memories). The evaluation. |

A person's parents are one of:
- an existing couple: the household's own couple, or an ancestral couple already made. Siblings merge here, across households and villages.
- a new couple in some village;
- one living person and a dead spouse;
- a couple at the declared off-map node;
- "came from outside the record", for someone born before their village was founded.

Each candidate weighs:
- fertility at the mother's age, and spacing after a birth;
- the chance each parent is alive now (if living) or dead now (if not);
- the marriage market by distance;
- the couples the village had then (its present households grown back to its founding) less those already made. This is the coalescent's merge rate.
- living in one household as evidence of kin;
- a child with both parents dead being raised by others.

## Results

### 1. Never rejected; refused only by name

- **Forward presents pinned:** 40 of 40 built on seeds 1 to 40, and 40 of 40 on held-out seeds 41 to 80. None was refused.
  - Mean time 0.11 s, at most 0.7 s, for 60 to 250 living people and 230 to 300 people in the past.
  - Backjumps: 3 in all 80 worlds. Realistic presents rarely conflict.
- **Mixes:** two mixes, 20 seeds each.
  - The default mix: 70% couples with children, 15% old couples, 15% three generations.
  - Zach's kind of test conditions: 3 widows alone, 2 stem households, 2 three-generation households, 2 widowers with children, 2 single men and 1 pair of siblings, then shares.
  - All 40 built, and every pinned count was exact in all 40.
- **Impossible pins are refused at once, naming the pins:**
  - a village pinned as founded 12 years ago, with a child of 13 in it;
  - twins pinned as the head's children (the model has no twins);
  - a "child" of the head only ten years younger than him.

  The twins case names: `pin:age:tp.0`, `tp.2`, `tp.3` and `pin:role:tp.0` to `tp.3`.

### 2. Deterministic and consistent

- **Deterministic:** 40 of 40 worlds gave the same hash on a second build.
- **Consistent:** no invariant was broken in any of the 120 worlds (80 forward, 40 mixes), nor in the odd cases. `evaluate.check` tests:
  - each mother 15 to 47 and each father 16 to 72 at a birth;
  - both parents alive at it;
  - births a year apart;
  - no wedding after a spouse's death;
  - no spouses sharing a parent or grandparent;
  - a dead spouse's children before the living spouse's;
  - the absent dead before now.

  The check found two real faults while building, both fixed: a wedding dated after the spouse's death, and a dead spouse's
  unrecorded children dated into the living marriage's years.

### 3. Plausibility, against the truth and a null arm

The null arm keeps the same decisions and constraints but weights every allowed candidate alike. Means over seeds 1 to 40; seeds
41 to 80 agree to within a few points (`heldout_41_80.txt`).

| | Truth (forward) | Built | Null |
|---|---|---|---|
| Mother's age at a birth (mean / sd) | 30.0 / 6.7 | 28.9 / 7.0 | 30.1 / 7.5 |
| Mother's age at first birth | 24.7 | 23.2 | 26.8 |
| Birth interval (median, years) | 2.7 | 2.9 | 3.0 |
| Births to a completed family | 4.73 | 4.87 | 2.61 |
| Couples with 9 or more births, per world | 1.45 | 1.8 (2.0 held out) | 0.8 |
| Died under 15 | 22% | 27% | 32% |
| Age at death, adults | 50.7 | 54.7 | 51.5 |
| Adults with a living parent | 54% | 56% | 9% |
| Wives born in another village | 63% | 57% | 78% |
| Wives born off the map | 7% | 5% | 28% |
| Adults with a sibling in another household of the village | 40% | 51% | 6% |
| Adults with a sibling in another village | 59% | 58% | 15% |
| Adults with a sibling or cousin in another village | 89% | 92% | 40% |
| Parent couples per living person | 0.36 | 0.38 | 0.89 |
| Grandparent couples per living person | 0.28 | 0.30 | 1.10 |
| People in the past | 239 | 235 | 803 |
| Living people given the true living parents (only the test has a truth: see below) | | 60% (56% held out) | 2% |

**How to read it:**
- **Demography:** the built pasts match the forward model on every count, to within about a year or a tenth.
- **Structure:**
  - the share with a living parent matches;
  - the coalescence (parent and grandparent couples, people in the past) is close;
  - most kin across villages is reproduced.
- **The null arm** is wrong on all the structural counts, by a factor of 3 to 10. The forward model's weights do the work; the
  constraints alone do not.
- **Living people given the true living parents: 60%** (49% in the first version; corrected 16 Nov, below).
  - **Only the test has a true past.** A forward simulation makes a world. Everything but each person's age, sex and household
    is hidden, and the build makes a past for what is left. In use there is no truth: the build's past is the past.
  - **Measured over 3,194 living people whose true parent is also living:**

    | Where the true living parent lives | Share given the same living parents |
    |---|---|
    | Children, both parents at home | 88% |
    | Children, one parent at home | 60% (most of the rest are given the parent's present spouse: a step-parent read as a parent) |
    | Adults, both parents at home | 63% |
    | Adults, a parent elsewhere in the village | 8 to 21% |
    | Adults, a parent in another village | 2 to 8% |

  - **What cannot be read from ages:** a parent who lives in another household or village, a step-parent, and which of two
    couples in one house a child belongs to (11% of children living with both parents go to the house's other couple).
  - **What was wrong and is fixed:** in the first version only 73% of children living with both parents got them. Four faults
    in the weights:
    - a child living apart from a living parent cost 0.03, against the forward model's 0.0015;
    - a child joining a couple that was already dead paid no cost for being fostered;
    - a dead first spouse for a married parent was charged nothing for the childless marriage it implies, and when the
      youngest child drew it, the older siblings had to follow;
    - a brother and sister living with their mother could be paired as a couple (the forward model says such a pair is a couple
      a fifth as often).
  - **A household's own couples and children now take the likeliest reading** (weights cubed, SHARP); adults and the past are
    still drawn. Taking the likeliest parents for everyone gave unlikely populations: families of 5.6 against 4.7, and no
    off-map wives.
  - **If a test needs exact living kin, pin it:** the mix forms pin head, spouse, child and parent roles. This test pinned none.

**The biases that remain:**
- **Kin across villages now matches** (58% against 59%, and 92% against 89% with cousins), since daughter villages are founded
  from their mother village (§7). Siblings in other households of the same village are over-made: 51% against 40%.
- **Adults die four years too old** (54.7 against 50.7). Ancestors marry once, so the young first spouses who die and are
  replaced never appear: married parents dying under 40 are half the truth's count. Until 16 Nov this was hidden by a fill
  fault (unrecorded children living to old age without marrying), which also inflated families. That fault is fixed; the gap
  waits on second marriages for ancestors (L-108).
- **First births come 1.5 years young.** The marriage year is drawn after the children, so fill can add an early birth.
- **Slightly too many very large families:** 1.8 per world against 1.45 (2.0 against 1.4 held out). More children die under 15: 27% against 22%.

### 3a. Village ages come from the settlement history (16 Nov)

**Before:** each village's founding year was drawn from its present size alone. The genealogy then mostly gave the founders
"came from elsewhere". The founding order agreed with the truth at Kendall tau 0.43, and only 12% of daughter villages were
founded by someone born in an older village.

**Now:** the settlement is part of the built history, read from the evidence and built by the forward model's rule.
- **A `settle` decision** picks the order of settlement. Each later village buds from the nearest older one.
- **Each order implies founding years.** The k-th village is founded when those before it have filled.
- **Orders are weighed by what the present shows of a village's age,** with relations fitted on 120 forward runs:
  - an old village is full, at about 1 - exp(-A / 35) of the largest village's households;
  - it has elders: its third-oldest resident is about 12 + 0.58 A years old.
  - The likeliest order is taken.
- **Founders come from the mother village.** A daughter village's founders get their parents there. Founders born before the
  record are recorded as born there. "Came from elsewhere" is kept for the first village's founders and is rare otherwise.
- **The chronicle** dates a founding when its first couple settled, and names where they came from.

| 80 forward worlds | Before | Now |
|---|---|---|
| Founding order against the truth (Kendall tau) | 0.43 | 0.71 |
| First village right | 37 of 80 | 47 of 80 |
| Founding year error (mean) | 21 years | 15 years |
| Daughter villages founded from an older village | 12% | 85% |

**Limits:**
- The present carries little of a village's age. The best that can be read from it is tau 0.73 on the fitted seeds and 0.66
  held out.
- The third-oldest resident is fragile in small villages: two widows of 66 and 67 over a man of 37 read as young.
- In a mix the ages are drawn, not lived, so the order follows whatever they show.
- Founding years and the order can be pinned.

### 4. Stability under edits

Means over 15 worlds. "Soft" builds the edited present with the previous world's choices first; "fresh" builds it again from the
same seed without them.

| Edit | Decisions changed (soft / fresh) | Living people given other parents (soft / fresh) |
|---|---|---|
| A newborn added to one household | 0% / 1.7% | 0% / 1.6% |
| The second household made a family of seven | 2.9% / 10.6% | 1.8% / 8.6% |
| The last household removed | 1.5% / 9.1% | 1.3% / 6.8% |

Keyed orders alone keep about 90% of a world; the soft pins keep about 98%. A household change can change the settlement order, which moves more on a fresh build.

**What still moves:** the decisions downstream of a changed one, whose candidates changed. For example, a couple the edit removed
was someone's parents.

### 5. Odd pins

| Case | Result |
|---|---|
| Nine living children to one couple | Built. Flagged as a couple of nine. |
| A village of widows living alone | Built. Each widow is given a dead husband (its own decision, `wid`, when no living child calls for one) and that marriage's children who died or left. The first draft made no husband for a childless widow; that was fixed. |
| A village pinned as founded 20 years ago, all its adults older | Built. Its adults "came", or were born in Northby or Southam; its children were born there. |
| The same, 12 years ago, with a child of 13 | Refused: `pin:found:Westcot`, `pin:age:We3.2`. |
| Two children of 6 in one house, no roles | Built. One is the couple's; the other is read as a child of another Eastwick household, living with them. |
| The same, pinned as the head's children | Refused, naming the pins. |
| Every village pinned as founded 20 years ago | Built. Everyone over 20 came from outside the record. |

**The flags** mark decisions where the constraints ruled out at least half of the model's weight, couples of nine or more, and
villages under 25 years old. A mix world has 9 to 10 flags. Most are founders whose strongly preferred parents in the mother village were ruled out by ages. This is the report the proposal asked for: where a pin forced an
unlikely past.

### 6. Reading the histories

`results/sample_seed1.md` holds a built past for a forward present: foundings, marriages with origins, deaths by cause, and three
heads' kin and memories. It reads as a history, and it is consistent by construction:
- a widow's second marriage comes after her first husband's death;
- a half-brother carries his father's surname;
- deaths gather in the world's hard years;
- founders arrive from an older village or from Kingsmarket.

**What reads badly:**
- **The founding order:** the founding years come from a size prior, so Westcot is founded before Northby while the truth has Northby first.
- **Generic causes:** "a fever" covers many deaths.

## What this does not show

- **The forward model is the prototype's own, and demographic only.** It has no land, food, holdings or crafts, and the hard years are a keyed
  stand-in for the climate scheduler's past. Both directions read the same tables. So this tests the backward method against its
  own forward model, not the tables' realism, and not §4.3's land-fed demography.
- **Six backward weights were calibrated on seeds 1 to 40:** KFRAC, OUT, MOVE, CO, FOSTER and FLOOR, all in `demog.py`. Seeds 41 to 80 hold
  out. Each weight is a likelihood factor the forward model implies but that I measured rather than derived.
- **Incremental rebuilding re-checks every decision; it does not skip the unchanged ones.** That is cheap here (0.1 to 0.2 s). Skipping by recorded inputs
  (§4.5 point 3) is not built, and it is untested at the land's scale.
- **Backjumping is hardly exercised by realistic presents:** 3 backjumps in 80 worlds. It is exercised by odd and impossible pins.
- **Completeness of the conflict sets is the engineering risk.** Three faults were found and fixed while building:
  - candidates dropped at weight zero by another decision's state left no trace, so a feasible world was refused;
  - a couple's maker was blamed for its ages, so the search ran through every matching of an unrelated household;
  - its place was blamed when no decision chose it, with the same result.

  An incomplete conflict set silently skips solutions; a padded one thrashes. The rules that came out of it are under "For the
  build". The null arm still runs to the step limit once in 80 worlds: the weights also keep the search short.
- **Not modelled:**
  - twins;
  - more than one dead spouse;
  - fostering by kin rather than by any household;
  - inheritance of holdings and houses;
  - a past for the off-map node.

## Verdict on §5's two risks

1. **Backward genealogy: settled enough for a build brief.**
   - Pinned presents, explicit or mixed, are always met.
   - The pasts match the forward model's demography.
   - They are close on its structure, far better than the null.
   - The remaining biases are named calibrations with their knobs.
2. **The decision graph for people: works at this scale.** It is deterministic, stable under edits (98% kept with soft pins),
   never rejects, and refuses an impossible pin at once by name.

   The design risk has moved from "does it work" to "are the conflict sets complete". The build should carry the rules below, and
   a test that checks refusals against brute force on small cases.

## For the build (37.4, `engine/generate.py`)

- **Order:** foundings, then pairings, then parents newest-first, then the other spouse's age, deaths, and fills. Each decision
  reads only what is above it.
- **Blame rules:**
  - Never drop a candidate at weight zero because of another decision's state. Give it a floor weight and let the check reject
    it, so the conflict set names the cause.
  - Blame a decision only for what it set (an age, a chosen place), never for the existence of a candidate it made.
  - Pins filter candidates directly; a pin is never revisited, so there is nothing to blame.
  - A decision with no candidates blames its inputs (`blame()`).
- **Likelihood factors the forward model implies,** each worth its own calibration:
  - co-residence as evidence of kin;
  - a fostering cost;
  - out-marriage beyond distance (kin at home are barred);
  - men's moves;
  - the past couples per household.
- **Next calibration:** merges across villages (siblings in other villages) and the marriage year before the children.

Example pasts to read: `results/examples.md` (`python -m proto.peoplegen.examples`).

*Current as of 16 Nov 2026 (settlement history).*
