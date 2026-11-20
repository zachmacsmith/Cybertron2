---
id: D2-173
kind: decision
state: live
updated: "2026-11-20"
tags: [decision, open]
---
# The generator fills in around what a world file gives:

- **state**: live
- **source**: conversation ("1. I agree with this. 2. sure 3. written by model and frozen 4. yes"); proposals/generator.md
- **replaces_text**: seed searches for a world that fits

## Text
**The generator fills in around what a world file gives:** a world file is the input with gaps; whatever it gives is pinned (exact values, ranges, or descriptions from a vocabulary mapped to ranges: "short of wood", "on a river"), the rest is generated layer by layer around the pins, with draws keyed per element so a change touches only what depends on it, and targets (capacity, food's share) are met by adjusting what is unpinned, not by searching seeds; a pin wins where the physics allows, and a pin the physics cannot meet is refused with the reason; descriptions of places are written by a model once and frozen into the output; the output is a complete world file, frozen with the run; the land and region first, pins for people second

## Mentioned by
- [[L-101 Compile the generator into specworldgeneration.md|L-101: Compile the generator into spec/world/generation.md]]
- [[Q-7 (Closed 2 Nov settled by the landscape generator (D2-173 to D2-188|Q-7: (Closed 2 Nov: settled by the landscape generator (D2-173 to D2-188) a]]
- [[W-9 Compile the generator into specworldgeneration.md (OPEN L-101)|W-9: Compile the generator into spec/world/generation.md (OPEN L-101)]]
- [[environment_systems Environment systems the land at three speeds, on t|Environment systems: the land at three speeds, on the places]]
- [[generation_redesign Proposal world generation as one history, with pin|Proposal: world generation as one history, with pins met in ]]
- [[generator Proposal the landscape generator (a world under the graph)|Proposal: the landscape generator (a world under the graph)]]
- [[generator_stage1 Proposal the generator, stage 1 (a spec for review be|Proposal: the generator, stage 1 (a spec for review before i]]
- [[information_economics Proposal the economics of information|Proposal: the economics of information]]
- [[layout Proposal the layout inside a node (parcels, features, and thing|Proposal: the layout inside a node (parcels, features, and t]]
- [[02zj_generator_build 02zj the landscape generator, stage 1, as built|02zj: the landscape generator, stage 1, as built]]
- [[02zzl_environment_gaps 02zzl the environment as the engine runs it, an|02zzl: the environment as the engine runs it, and as the gen]]
- [[period_a Period A (22 Oct to 3 Nov 2026) initiatives against their rec|Period A (22 Oct to 3 Nov 2026): initiatives against their r]]
- [[records Records audit what the documents say against what is true (19|Records audit: what the documents say against what is true (]]
- [[replies_1_audit Audit of 37.2's replies, 22 Oct to 8 Nov 2026 commitme|Audit of 37.2's replies, 22 Oct to 8 Nov 2026: commitments a]]
