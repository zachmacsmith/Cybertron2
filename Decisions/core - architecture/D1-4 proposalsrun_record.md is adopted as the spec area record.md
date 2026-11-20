---
id: D1-4
kind: decision
state: live
updated: "2026-11-20"
---

# proposals/run_record.md is adopted as the spec area `record/` (D1-4)

*live · 24 Oct · spec: [[core - architecture|core/architecture]], [[record - branching|record/branching]], [[record - exchange|record/exchange]], [[record - execution|record/execution]], [[record - human_play|record/human_play]], [[record - journal|record/journal]], [[record - views|record/views]]*

## The rule
the runner as a state machine over keyed requests answered by responders (recorded, model, bot, human); steps with attempts and commits; checkpoints, events and changes with causes; frozen data tables; views (state, beliefs, exact context, map frames, history); fork, replicates, interventions; export with lossless journal tables and view tables; import and fetch; replay promised within one code version

## Where it came from
Zach, 37.1 conversation ("compile these proposals into a spec"); spec/record/


## Mentioned by
- [[D1-5 Storage|Storage (D1-5)]]
- [[C-10 Run files, checkpoints, replay, versioning|Run files, checkpoints, replay, versioning (C-10)]]
- [[The engine's architecture|The engine's architecture]]
- [[Branching rewind, fork, replicates, interventions|Branching: rewind, fork, replicates, interventions]]
- [[Export, publish, import|Export, publish, import]]
- [[Running a run steps, requests and commits|Running a run: steps, requests and commits]]
- [[A human playing as an agent|A human playing as an agent]]
- [[The journal|The journal]]
- [[Views of a run|Views of a run]]
- [[38.32 R2 of the run record built (resume, pause, cancel, replay)|38.32: R2 of the run record built (resume, pause, cancel, replay)]]
- [[38.33 R4 of the run record built (rewind, fork, replicates…|38.33: R4 of the run record built (rewind, fork, replicates…]]
- [[38.34 R5 of the run record built (views, export, import, publish…|38.34: R5 of the run record built (views, export, import, publish…]]
- [[38.35 R3 of the run record built (a person plays an agent, through a…|38.35: R3 of the run record built (a person plays an agent, through a…]]
