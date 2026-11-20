---
id: D2-180
kind: decision
state: live
updated: "2026-11-20"
---

# D2-180 · The generator's checks in two kinds

*live · 3 Nov*

## The rule
**The generator's checks in two kinds:** physics checks (rivers downhill, terrains that fit, every pin met) refuse a world that fails them; design checks (capacity, dependence, supply chains, chokepoints, access gates, parcels a node) warn, unless the world file requires them (`require: [...]`), so a null arm can break them on purpose; by default access gates and capacity are required

## Where it came from
conversation ("yes")


## Mentioned by
- [[Proposal world generation as one history, with pins met in the loop|Proposal: world generation as one history, with pins met in the loop]]
- [[Proposal the landscape generator (a world under the graph)|Proposal: the landscape generator (a world under the graph)]]
- [[Proposal the generator, stage 1 (a spec for review before it is…|Proposal: the generator, stage 1 (a spec for review before it is…]]
