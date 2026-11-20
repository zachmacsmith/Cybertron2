---
id: D4-124
kind: decision
state: live
updated: "2026-11-20"
---

# D4-124 · Resume from the last finished day

*live · 19 Nov*

## The rule
**Resume from the last finished day:** `resume RUN --from-last` restores the world and runner from the last `dN.memory` checkpoint and plays on with no replay; interventions after that day not yet applied are applied; exports appended; a `resume_last` segment (proposals/resume_from_last.md)

## Where it came from
conversation ("it only replay a from where we are up to")

## What it replaced
a resume replayed every committed step from day 1


## Mentioned by
- [[Q-62 recordexecution.md and resume --from-last|Q-62 · record/execution.md and `resume --from-last`]]
- [[W-58 The runs world with a model to each household|W-58 · The runs world with a model to each household]]
- [[Resume from the last finished day, without replay|Resume from the last finished day, without replay]]
