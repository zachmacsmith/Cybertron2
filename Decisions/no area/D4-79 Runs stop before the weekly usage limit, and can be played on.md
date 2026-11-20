---
id: D4-79
kind: decision
state: live
updated: "2026-11-20"
tags: [decision, open]
---
# Runs stop before the weekly usage limit, and can be played on:

- **state**: live
- **source**: conversation ("don't go past 40% weekly usage"; a long run continued, c2_combe); proposals/run_tools.md (retrospective)

## Text
**Runs stop before the weekly usage limit, and can be played on:** before each live day the run checks the subscription's weekly window and stops cleanly at the world's `llm.week_stop` (env CYBERTRON2_WEEK_STOP; default 0.9), writing STOPPED.md, to be resumed; `continue --days N` plays a finished run on past its world's length

## Mentioned by
- [[L-31 D4-79's rules (the weekly usage stop, llm.week_stop, STOPPED.md;|L-31: D4-79's rules (the weekly usage stop, `llm.week_stop`, STOPPED.md; `co]]
- [[run_tools Runs that stop before the weekly limit, and play on|Runs that stop before the weekly limit, and play on]]
- [[02zz_open_sorting 02zz sorting OPEN.md's open rows into the new kinds|02zz: sorting OPEN.md's open rows into the new kinds (draft,]]
