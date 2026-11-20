---
id: D2-173
kind: decision
state: live
updated: "2026-11-20"
---

# D2-173 · The generator fills in around what a world file gives

*live · 3 Nov*

## The rule
**The generator fills in around what a world file gives:** a world file is the input with gaps; whatever it gives is pinned (exact values, ranges, or descriptions from a vocabulary mapped to ranges: "short of wood", "on a river"), the rest is generated layer by layer around the pins, with draws keyed per element so a change touches only what depends on it, and targets (capacity, food's share) are met by adjusting what is unpinned, not by searching seeds; a pin wins where the physics allows, and a pin the physics cannot meet is refused with the reason; descriptions of places are written by a model once and frozen into the output; the output is a complete world file, frozen with the run; the land and region first, pins for people second

## Where it came from
conversation ("1. I agree with this. 2. sure 3. written by model and frozen 4. yes"); proposals/generator.md

## What it replaced
seed searches for a world that fits


## Mentioned by
- [[Q-7 First land kinds|Q-7 · First land kinds]]
- [[W-9 Compile the generator into specworldgeneration.md|W-9 · Compile the generator into spec/world/generation.md]]
- [[L-101 Compile the generator into specworldgeneration.md|L-101 · Compile the generator into spec/world/generation.md]]
- [[Environment systems the land at three speeds, on the places the…|Environment systems: the land at three speeds, on the places the…]]
- [[Proposal world generation as one history, with pins met in the loop|Proposal: world generation as one history, with pins met in the loop]]
- [[Proposal the landscape generator (a world under the graph)|Proposal: the landscape generator (a world under the graph)]]
- [[Proposal the generator, stage 1 (a spec for review before it is…|Proposal: the generator, stage 1 (a spec for review before it is…]]
- [[Proposal the economics of information|Proposal: the economics of information]]
- [[Proposal the layout inside a node (parcels, features, and things on…|Proposal: the layout inside a node (parcels, features, and things on…]]
- [[02zj the landscape generator, stage 1, as built|02zj: the landscape generator, stage 1, as built]]
- [[02zzl the environment as the engine runs it, and as the generator…|02zzl: the environment as the engine runs it, and as the generator…]]
- [[Audit of 37.2's replies, 22 Oct to 8 Nov 2026 commitments and…|Audit of 37.2's replies, 22 Oct to 8 Nov 2026: commitments and…]]
- *and 2 index or audit notes*
