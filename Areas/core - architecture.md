# core/architecture

*The engine's architecture* · the spec: [[The engine's architecture|The engine's architecture]]

> cybertron2 is rebuilt on a general core: everything has a place, every change passes one chokepoint, and the code that serves an agent sees only where the agent is and what it knows. Narrow code that fits one scenario is replaced, not kept beside the general form.

## Decided (8)
- [[D1-2 Everything is written as it happens|Everything is written as it happens (D1-2)]]
- [[D1-4 proposalsrun_record.md is adopted as the spec area record|proposals/run_record.md is adopted as the spec area `record/` (D1-4)]]
- [[D4-1 Start from what 37.2 built and extend it|Start from what 37.2 built and extend it (D4-1)]]
- [[D4-24 The world grows by data, and agents explore and learn it|The world grows by data, and agents explore and learn it (D4-24)]]
- [[D4-34 Rebuild the M1 engine on the designed general core|Rebuild the M1 engine on the designed general core (D4-34)]]
- [[D4-35 Everything happens in a place|Everything happens in a place (D4-35)]]
- [[H-1 Space is a new engine in its own package, cybertron2|Space is a **new engine in its own package**, `cybertron2/` (H-1)]]
- [[H-2 Port the physical systems onto nodes|Port the physical systems onto nodes (H-2)]]
