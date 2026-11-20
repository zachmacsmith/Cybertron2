# Resume from the last finished day, without replay

**Status:** retrospective, accepted: D4-124 (19 Nov 2026)

**Owner:** 37.4 (the code). The record spec (record/execution.md) is 37.1's.

## Summary

`python -m cybertron2.engine resume RUN --from-last` restores the world and the runner from the checkpoint at the end of the last finished day (`dN.memory`) and plays on from the next dawn. It does not replay the days before. Interventions put in after that day and not yet applied are applied first. The run's jsonl exports are appended to, not rewritten. The journal gets a `resume_last` segment that names the checkpoint and the first live step, and open attempts are marked aborted.

## The proposal (as built)

- `run.py`: mode `resume_last` uses the restore path that `continue` already has, on the run itself.
  - The world comes from the checkpoint, and `WA.link` re-joins the water bodies.
  - The runner comes back the same way: conversations (with a new CLI session), cost, systems.
  - The exports open in append mode.
  - `STOPPED.md` moves to the stop history as on a resume.
- `branch.after_commit(..., only_new=True)` applies only the interventions due after that step that are not yet applied. The checkpoint already holds the earlier ones.
- `journal.go_on(at, first)` records the segment and aborts open attempts.
- Test: `tests/test_cybertron2_branch.py::test_resume_from_last_...`. It checks three things:
  - a run rewound to day 2 and resumed from last reaches the same end as the run played through;
  - the exports are appended with days 3 and 4 only;
  - an intervention put in after day 2 is applied once.

## Why

Zach (19 Nov): "You should be able to replay so that it only replay a from where we are up to."

A plain resume replays every committed step from day 1. That is free in model calls, but it takes time. Under changed code it also checks each checkpoint again, and a rule change could reach back into days already played. It also rewrites the exports, and an interrupted resume left the runs world's day files cut back to day 8.

## Alternatives considered

- **`continue`.** It makes a new run directory from a checkpoint. That is right for a branch, but not for going on with the same run.
- **Keep the replaying resume.** It stays as the default, since it checks the record against the code.

## Open questions

- record/execution.md says a resume "loads the last committed checkpoint". That fits `--from-last`. Whether the spec should name both forms is 37.1's call (OPEN).

## Affects

cybertron2/engine/run.py, branch.py, journal.py; tests/test_cybertron2_branch.py.

## History

- **19 Nov 2026:** built at Zach's request on branch `runs-models`, for the runs world's model run (W-58); recorded as D4-124.

## Sources

Zach in conversation, 19 Nov; record/execution.md; record/branching.md (`continue`).
