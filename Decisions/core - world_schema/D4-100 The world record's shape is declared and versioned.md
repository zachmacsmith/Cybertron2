---
id: D4-100
kind: decision
state: live
updated: "2026-11-20"
---

# D4-100 · The world record's shape is declared and versioned

*live · 4 Nov · spec: [[core - world_schema|core/world_schema]]*

## The rule
**The world record's shape is declared and versioned:** `world_schema` in every world and checkpoint and in the journal's meta; schema.py declares the fields of every table, the top-level keys and the day's record; every change bumps the number and is written in spec/core/world_schema.md; a test fails on an undeclared field or a shape changed without its version

## Where it came from
conversation ("Go ahead with the world schema number and changelog and write a proposal for the rest"); proposals/run_data_interface.md (part 1, retrospective)

## What it replaced
none (the world's shape was unversioned; only the journal's tables had a schema)


## Mentioned by
- [[Q-48 The engine as feature packages|Q-48 · The engine as feature packages]]
- [[The engine as a small core and feature packages design specification|The engine as a small core and feature packages: design specification]]
- [[A fixed data interface for runs versioned shapes, one read layer…|A fixed data interface for runs: versioned shapes, one read layer…]]
- [[Proposal the wild layer, one general system for ecosystems and…|Proposal: the wild layer, one general system for ecosystems and…]]
- [[The world record's shape and its version|The world record's shape and its version]]
