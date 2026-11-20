---
id: D4-61
kind: decision
state: live
updated: "2026-11-20"
tags: [decision, open]
---
# An agent rewrites its one memory each stretch, within a length that grows with its age:

- **state**: live
- **source**: conversation ("rather than forming a new memory every 3 days, they rewrite their memory section ... a scheduler that decides how the token length ... changes over time ... up to them rather than forced by the engine"; then "you can implement your recommended memory changes"); proposals/memory_rewrite.md; review 38.36 (live tests of seven instructions on two models)
- **replaces_text**: [[D4-28 Agents write their own memory at set times|D4-28]]'s queue of stretch memories (the last six) and the engine's list of marked events, for all but weak models

## Text
**An agent rewrites its one memory each stretch, within a length that grows with its age:** keep what still matters, add from these days only what it will want later, leave the rest; the length rises fastest when young and levels off (ceiling about 600 words); the engine keeps no list of events on its behalf; weak models (Haiku) keep [[D4-28 Agents write their own memory at set times|D4-28]]'s queue

## Mentioned by
- [[D4-28 Agents write their own memory at set times|D4-28: Agents write their own memory at set times]]
- [[L-106 MAJOR what the engine remembers and settles for agents, and sepa|L-106: MAJOR: what the engine remembers and settles for agents, and separatin]]
- [[agent_view What an agent is shown the world and its rules, not choices|What an agent is shown: the world and its rules, not choices]]
- [[forays Forays going out from the village and coming back|Forays: going out from the village and coming back]]
- [[lasting_memory Kept for good a few lines an agent keeps word for word|Kept for good: a few lines an agent keeps word for word]]
- [[memory_rewrite Memory rewritten, its length set by age|Memory rewritten, its length set by age]]
- [[seeing Proposal what an agent is shown each round, attention, and desc|Proposal: what an agent is shown each round, attention, and ]]
- [[memory Memory and reasoning|Memory and reasoning]]
- [[02zc_systems_overview 02zc the systems of cybertron2 as they stand|02zc: the systems of cybertron2 as they stand]]
- [[02zd_v2_justification 02zd cybertron2 as a response to cybertron 1|02zd: cybertron2 as a response to cybertron 1]]
- [[02zv_wild_consolidation 02zv the wild layer consolidated core engine c|02zv: the wild layer consolidated: core engine changes, cont]]
- [[09_engine_mapping 09 Mapping economic layers onto the engine, from for|09: Mapping economic layers onto the engine, from foragers t]]
- [[36_memory_rewrite 38.36 Memory rewritten each stretch live tests of th|38.36: Memory rewritten each stretch: live tests of the inst]]
- [[37_agent_view 38.37 Everything an agent is shown inventory, origins, w|38.37: Everything an agent is shown: inventory, origins, wha]]
- [[38_memory_use 38.38 How agents have used their memory notes, pins, ope|38.38: How agents have used their memory: notes, pins, openi]]
- [[39_lasting_memory 38.39 Lines kept for good a small replay test|38.39: Lines kept for good: a small replay test]]
- [[40_agent_interface 38.40 The agent's interface a taxonomy of what it k|38.40: The agent's interface: a taxonomy of what it knows, h]]
