# record/execution

*Running a run: steps, requests and commits* · the spec: [[Running a run steps, requests and commits|Running a run: steps, requests and commits]]

> The runner is a state machine. It advances step by step; everything it needs from outside is a keyed request answered once; everything that happens is written at once; a step's commit makes it official. Crash, cancel and pause all stop after the last commit, and resume picks up from there without as

## Decided (3)
- [[D1-1 The run record supports everything cybertron 1's instrument did|The run record supports everything cybertron 1's instrument did (D1-1)]]
- [[D1-2 Everything is written as it happens|Everything is written as it happens (D1-2)]]
- [[D1-4 proposalsrun_record.md is adopted as the spec area record|proposals/run_record.md is adopted as the spec area `record/` (D1-4)]]
