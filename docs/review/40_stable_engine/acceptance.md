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

## The second pass, on the merged engine (24 Nov, after W-109; branch at a88f4b4e)

| World | Bots | Days | Errors | Refusals | Kinds | Gate at the start |
|---|---|---|---|---|---|---|
| Eelmouth | `--bots runs` | 6 | 0 | 0 | 0 | pass (warn P7, P10, P11, P18) |
| World 0b, Sonnet 5.5's arm (bench's branch, with D5-3's tagged goal line) | `--bots` | 6 | 0 | 1,187 | 11 | pass, no waiver |
| World 0b, Haiku 4.5's arm | `--bots` | 6 | 0 | 1,187 | 11 | pass, no waiver |

Every World 0b kind explains itself, as before; the generic bots now try working and making too (L-188), so "the day's work is done"
for work and make joins the gathers'. 21 alive at day 6 in each arm, 11 at Eelmouth.

**Left for acceptance:** 1, the short live check (one model, a few days), on Zach's go; 2, the replay of live run 1's and World 0b's
replies on this engine (37.2's replay of live run 1's 2,509 acts after W-109 refused none accepted before; this thread's later
changes to reading are deliberate: an unnamed slaughter refused, D2-304; "target" read as the partner); the runs' records are not on
this machine (fetched from the dataset when run); 3, old worlds load, run and render (the bot-run modules pass); 4, the fault table
closed or recorded (fault_table.md); 5, the full suite once, at the tag.

*Current as of 24 Nov 2026.*
