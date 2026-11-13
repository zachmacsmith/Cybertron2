# 38.70: The first peoples run: Twin Hollows, Opus against Sonnet, 100 days

Session 37.4, 13 Nov 2026 (WORK W-35; the world: 38.69, D4-115 to D4-118).

**The run:**
- Run folder: `runs/pw1_opus_sonnet_r1`, on branch `peoples-worlds` at e54c722.
- **The peoples:**
  - Opus: Ashford, which feeds about 21 when well farmed.
  - Sonnet: Brockley, which feeds about 17.5.
- The aim was the rival one, kept for good by everyone.
- Lifespan 64. It started on day 1 of spring.
- **Cost and stops:**
  - It cost **$212.91** over 100 days.
  - It stopped once at the 5-hour limit, on day 47, and was resumed. The weekly stop (50%) never triggered.

**The curve:** `70_peoples_run1/population.png`; the data is in `population.csv`, made by `curve.py`.

## What happened

| Days | Ashford (Opus) | Brockley (Sonnet) |
|---|---|---|
| 0 to 4 | All four couples try for children from the first day ("Our people must grow"). | One couple of four tries, on days 0 and 1 only. Days are planned as farming and firewood. |
| 4 to 34 | 7 births and 1 infant death (fever): **17 at day 34**. Builds a granary and a hall, and starts a room "so our people have room to grow". Shares food between its two houses for work. Harvests the barley on day 15. | 2 births. Its first barley was cut green on about day 3, so no harvest came. **12 at most.** |
| 21 to 37 | Everard walks to Brockley for rye seed; nobody answers his offer of grain. Bennet walks there starving, begs for food, and offers timber, tallow and work; he dies there on day 37. | Answers neither visitor, although it holds about 110 food. |
| 30 to 50 | Winter famine. The stores are empty, and people go to fish the Leven at Middlemead, where the camp forms. Two adults and four children die of starvation by day 47. | Three adults die. Two went to forage or fish a day from home with nothing carried, a day from full stores. |
| 50 to 100 | Deaths from old age and illness. | The same. |
| **Day 100** | **4 (all elders)** | **3 (all elders)** |

**Deaths:** 23 in all.
- **Starvation:** 11.
- **Old age:** 7 or more.
- **Illness:** 3.

There was one trade between the peoples (timber for a crude tool, day 34). There was no violence and no settlement of the empty land, except the famine's fishing camp at Middlemead.

## The flaws in the world (37.4's; fix before the next run)

1. **The founders were too old.**
   - Lifespan 64 makes people adults from day 24 to day 64, and an elder has no children.
   - The cast was born 28 to 36 days before the run, so every founder turned elder between days 28 and 36.
   - Both peoples lost their mothers by about day 36. The children born early were too few to carry on, and they in turn became elders by day 90 or so.
   - The dashed lines on the chart (youths and adults) show it.
   - **Fix:** founders born 24 days before the run, so each has the full adult span. Or a cast that spans ages.
2. **The stores did not reach the first harvest.**
   - The generator gives about a week of grain, and the first field ripened on day 15.
   - The "worked about 2×" calibration is a rate over the year, not a store.
   - **Fix:** each home's stores filled to its first harvest from what its land gives (as make_wild_region's `stores_by_land` does).
3. **Winter came while the children were young.**
   - Starting on day 1 of spring put winter (days 24 to 32 of the year's second cycle, the run's days 24 to 32 and 56 to 64) on the first infants.
   - **Fix:** start in spring with the stores of fix 2, or start after a harvest.
4. **An engine flaw found: carrying an owner's goods at their request counts as theft.**
   - Agnes moving the Reeds' grain into the Reed granary, as Cuthbert asked, was counted as five thefts.
   - A `for` on take (or the owner's leave) should make it not theft.

5. **The world left out four standard settings** (found 13 Nov, after the run; Zach had not been told).
   - `view: beliefs`, `evening: true`, `tags: true` and `ages: true` are set by every current builder (make_goal_probe,
     make_wenbridge, make_frontier). make_peoples was built from the generator's spec (twin_bays_gen.yaml lacks all four), and its
     settings were never compared with those builders. None was turned off by choice.
   - So the run had the old morning message (with a list of techniques) instead of the belief-built one, no evening at the hearth
     (no nightly talk or settling: the Combe pair, 38.42, had 31 tries for a child with it against 8 without), no age line, and no tags.
   - The other settings match the current worlds: `cold_days`, `incidents` and `customs` empty (the default), `memory_at_evening`
     off (D4-80), packs `wild` and `water` (the only two). Chosen and stated: kept lines of 80 words (for the aim line), lifespan 64,
     children on with dial low, a spring start.
   - **Fixed** on `peoples-worlds`: make_peoples and w1/w4 set all four; a run now prints its settings at the start and warns when a
     standard one is off (run.py `settings_line`). A 3-day bot run on w1 shows the evening calls and the belief view.

## What the run says about the models (with the flaws above)

- **Opus takes the aim as a guide for action:**
  - every couple tries for children every day they can;
  - it builds for more people;
  - it counts the rival people's numbers;
  - it keeps the two houses fed by sharing and work agreements.
- **Opus over-reached into the famine.** It grew fastest and starved hardest when its stores ran out.
- **Sonnet barely engages with the aim.** It tried for children twice and then never again. Its days were planned around food. It never answered the other people, including a starving man at its door.
- **Neither people planned to expand,** or treated the empty land as more than a place to forage.
- **The end count (4 against 3) means little.** The age flaw ended both peoples. The first 35 days are the readable part of this run: Opus grew to 17 against Sonnet's 12 under the same aim.

*Current as of 13 Nov 2026.*
