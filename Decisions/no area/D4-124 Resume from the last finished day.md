---
id: D4-124
kind: decision
state: live
updated: "2026-11-20"
tags: [decision, open]
---
# Resume from the last finished day:

- **state**: live
- **source**: conversation ("it only replay a from where we are up to")
- **replaces_text**: a resume replayed every committed step from day 1

## Text
**Resume from the last finished day:** `resume RUN --from-last` restores the world and runner from the last `dN.memory` checkpoint and plays on with no replay; interventions after that day not yet applied are applied; exports appended; a `resume_last` segment (proposals/resume_from_last.md)

## Mentioned by
- [[Q-62 recordexecution.md and resume --from-last (D4-124; 37.4, 19 Nov)|Q-62: record/execution.md and `resume --from-last` (D4-124; 37.4, 19 Nov)]]
- [[W-58 The runs world with a model to each household (Zach, 17 Nov; prop|W-58: The runs world with a model to each household (Zach, 17 Nov; proposals]]
- [[resume_from_last Resume from the last finished day, without replay|Resume from the last finished day, without replay]]
