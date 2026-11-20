---
id: D1-2
kind: decision
state: live
updated: "2026-11-20"
---

# D1-2 · Everything is written as it happens

*live · 23 Oct · spec: [[core - architecture|core/architecture]], [[record - execution|record/execution]], [[record - views|record/views]]*

## The rule
; a step's commit only makes it official; a run is visible layer by layer through the day, and what happened up to a crash stays readable (aborted attempts kept)

## Where it came from
Zach, 37.1 conversation; spec/record/execution.md

## What it replaced
the proposal's first form (a step written whole or not at all)


## Mentioned by
- [[The engine's architecture|The engine's architecture]]
- [[Running a run steps, requests and commits|Running a run: steps, requests and commits]]
- [[Views of a run|Views of a run]]
- [[02zd cybertron2 as a response to cybertron 1|02zd: cybertron2 as a response to cybertron 1]]
- [[38.32 R2 of the run record built (resume, pause, cancel, replay)|38.32: R2 of the run record built (resume, pause, cancel, replay)]]
