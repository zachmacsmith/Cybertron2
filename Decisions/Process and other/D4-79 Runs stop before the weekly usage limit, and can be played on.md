---
id: D4-79
kind: decision
state: live
updated: "2026-11-20"
---

# Runs stop before the weekly usage limit, and can be played on (D4-79)

*live · 1 Nov*

## The rule
**Runs stop before the weekly usage limit, and can be played on:** before each live day the run checks the subscription's weekly window and stops cleanly at the world's `llm.week_stop` (env CYBERTRON2_WEEK_STOP; default 0.9), writing STOPPED.md, to be resumed; `continue --days N` plays a finished run on past its world's length

## Where it came from
conversation ("don't go past 40% weekly usage"; a long run continued, c2_combe); proposals/run_tools.md (retrospective)


## Mentioned by
- [[L-31 D4-79's rules|D4-79's rules (L-31)]]
- [[Runs that stop before the weekly limit, and play on|Runs that stop before the weekly limit, and play on]]
- *and 1 index or audit notes*
