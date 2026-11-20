---
id: D2-177
kind: decision
state: live
updated: "2026-11-20"
tags: [decision, open]
---
# The generator's first stage writes today's world format plus the mesh, with no engine change;

- **state**: live
- **source**: conversation ("1. yes 2. sure"; "the land should also be generating coasts, thus with oceans, and lakes"; "these should be somewhat configurable")

## Text
**The generator's first stage writes today's world format plus the mesh, with no engine change;** its input is the world file with a `generate:` block and a vocabulary of words mapped to ranges (generator_stage1.md §1); it generates seas, coasts and lakes as well as land and rivers; every number in it is a world setting with a default, so worlds can be much larger

## Mentioned by
- [[generation_redesign Proposal world generation as one history, with pin|Proposal: world generation as one history, with pins met in ]]
- [[generator Proposal the landscape generator (a world under the graph)|Proposal: the landscape generator (a world under the graph)]]
- [[generator_stage1 Proposal the generator, stage 1 (a spec for review be|Proposal: the generator, stage 1 (a spec for review before i]]
- [[living_populations Proposal living populations on the land (a generali|Proposal: living populations on the land (a generalised ecol]]
