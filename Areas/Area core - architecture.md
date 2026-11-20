# core/architecture: The engine's architecture

cybertron2 is rebuilt on a general core: everything has a place, every change passes one chokepoint, and the code that serves an agent sees only where the agent is and what it knows. Narrow code that fits one scenario is replaced, not kept beside the general form.

The spec: [[architecture The engine's architecture|The engine's architecture]]

## Decisions
- [[D1-2 Everything is written as it happens|D1-2: Everything is written as it happens]]
- [[D1-4 proposalsrun_record.md is adopted as the spec area record|D1-4: proposals/run_record.md is adopted as the spec area `record/`]]
- [[D4-1 Start from what 37.2 built and extend it; what does not match the|D4-1: Start from what 37.2 built and extend it; what does not match the plan]]
- [[D4-24 The world grows by data, and agents explore and learn it|D4-24: The world grows by data, and agents explore and learn it]]
- [[D4-34 Rebuild the M1 engine on the designed general core|D4-34: Rebuild the M1 engine on the designed general core]]
- [[D4-35 Everything happens in a place|D4-35: Everything happens in a place]]
- [[H-1 Space is a new engine in its own package, cybertron2; the old engi|H-1: Space is a **new engine in its own package**, `cybertron2/`; the old e]]
- [[H-2 Port the physical systems onto nodes; copy the institutional layer|H-2: Port the physical systems onto nodes; copy the institutional layer kee]]

## Open here
