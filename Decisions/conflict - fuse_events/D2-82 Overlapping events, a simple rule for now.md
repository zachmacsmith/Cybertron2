---
id: D2-82
kind: decision
state: live
updated: "2026-11-20"
---

# D2-82 · Overlapping events, a simple rule for now

*live · 23 Oct · spec: [[conflict - fuse_events|conflict/fuse_events]]*

## The rule
**Overlapping events, a simple rule for now:** every event detected at one node (or one stretch of road) in one night shares one wave of calls, and each woken agent sees every event it detected; they resolve by start time, ties by a keyed draw. Flagged to review in more depth (OPEN [[Q-19 Overlapping fuse events in more depth|Q-19]])

## Where it came from
conversation ("implement something but flag this")


## Mentioned by
- [[Q-19 Overlapping fuse events in more depth|Q-19 · Overlapping fuse events in more depth]]
- [[L-6 Overlapping fuse events in depth|L-6 · Overlapping fuse events in depth]]
- [[Proposal fuse events (time to respond)|Proposal: fuse events (time to respond)]]
- [[Fuse events time to respond|Fuse events: time to respond]]
