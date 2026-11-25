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

## The live check (25 Nov, Zach's go; acceptance 1)

Run on main at 46790664, `claude_code` backend, 4 days each, logs outside the repository (`/home/user/c2runs/`). The
first launch was discarded: orphaned processes wrote into the same run directories as the relaunch; each was rerun once, alone.

| World | Cast | Days | Alive at the end | Errors | Refusals | Kinds | Cost | Conversations continued / fallbacks |
|---|---|---|---|---|---|---|---|---|
| Eelmouth | its own: 3 Opus 5.5 heads, 1 Sonnet 5.5, 4 Haiku 5.5 | 4 | 12 of 12 | 0 | 22 | 16 | $2.12 | 16 / 0 |
| World 0b, Haiku 4.5's arm | Haiku 4.5 throughout | 4 | 21 of 21 (Alard and Osric hungry on night 4) | 0 | 117 | 35 | $5.70 | 30 / 0 |

**Every refusal read** (`tools/refusals.py`). Most explain themselves: the three-a-day message limit (57 of World 0b's), the notes
cap, the day's work done, the fish fished out for now, nothing in season, a door only its holder's head sets, a hen is not food, a
rule's condition that is no condition. **Five were the engine's, fixed with tests:**

| Refusal | Fault | Fix |
|---|---|---|
| "drive: there is no drive in this world" (Eelmouth) | "drive" is both the herd act and the hunting craft one is shown; the parser took the act | an act word that is also a craft one knows is read as the craft where the act names nothing or is not in this world (d8e70b20) |
| "pin: you have no note called “\"\"”" (Eelmouth) | an empty pin written as quotes | read as no pin (d8e70b20) |
| "tell/say: you know no craft called 'tell'" (World 0b) | a talk wave's reply with "say" or "tell" among its actions skipped reply_fields (L-189 built it for the morning and the evening only) | moved to its field there too (25299098) |
| "rule: could not read who: 'my household'" (World 0b) | "who" did not read one's own words ("for" did) | read (25299098) |
| "work: you carry no smoked fish" x16 (World 0b, care) | true, but unlike move's it did not say where the food was | says a child is fed from the hands, where the food is and how to take it (25299098) |

**Read:** the interface works for both casts; no refusal is unexplained after these fixes. World 0b's hunger by day 4 is the world's
food, as bench read it (Q-105, Q-107), not the engine's.

*Current as of 25 Nov 2026.*
