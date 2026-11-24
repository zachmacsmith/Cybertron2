# The acceptance runs: a first, preliminary pass (session stable, W-111, 24 Nov 2026)

Acceptance 1 of `proposals/stable_engine_for_runs.md` on the two experiment worlds Zach named (Q-101): a 6-day bot pass with every
refusal read. **Preliminary:** run on this thread's branch (11cb8304) before the interface rebuild (W-109) is merged; to be run again
on the merged engine, with the short live check.

| World | Bots | Days | Errors | Refusals | Kinds | Reading |
|---|---|---|---|---|---|---|
| Eelmouth (`specs/nutrition/eelmouth.yaml`) | `--bots runs` (the fishing bots) | 6 | 0 | 0 | 0 | clean; 11 alive at day 6 |
| World 0b, Sonnet 5.5's arm (bench's branch, `specs/mono/world0b_sonnet55.yaml`) | `--bots` (the generic bots) | 6 | 0 | 1,064 | 10 | every kind explains itself: the generic bots' fixed acts (moving goods not in hand, a second gather after the day's work, an offer of what they lack); 21 alive at day 6 |

Read with `python3 tools/refusals.py <run dir>` (refusals by kind, names and numbers in brackets, one example each). D2-298: bot runs
test the interface and basic functioning only.

**The gate at the start** on World 0b: refuse on P6 x19 and P20 x19 only, all from the graded goal line (D5-1); with
`gate: {waive: {P6: ..., P20: ...}}` it passes ("gate: pass; P20 x19 waived (...); P6 x19 waived (...)"). Warnings: P16 x5 (heads
not on the head model, as a monoculture means), P10, P11, P7.

**Still to do for acceptance 1:** the same on the merged engine and on World 0b's other arms; the short live check (one model, a few
days), which waits on Zach's go.

*Current as of 24 Nov 2026.*
