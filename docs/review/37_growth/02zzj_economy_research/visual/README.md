# Flint to Fab: the 02zzj research as an interactive web (15 Nov 2026)

Zach (15 Nov): "Make an interactive visual of the economy research. Showing the transition of different economic paradigms and the
web of dependencies across different societal paradigms, as new things are unlocked."

Page: https://claude.ai/artifact/MGPhiBe42BscFep6MB8VrN (private to Zach; `index.html` here is the same page).

> **A map, not a plan** (Zach, 15 Nov: "a map of all of the future to come back and have better clarity of where to draw the
> borders for now ... so I don't accidentally scope creep into trying to build the entirety of human history"). Nothing here
> is proposed for building because it appears here. The border for now, and how something crosses it, is in
> [02zzk_medieval_border.md](../../02zzk_medieval_border.md).

## What it shows

- **Dependency web:** 1,335 techniques, industries, goods, infrastructures and institutions in ten domain lanes, placed at their
  first significant appearance anywhere, with 3,114 links between them (16 Nov: parts 14 to 18 added, and a linking pass of
  356 links and 20 bridge nodes between civilisations and periods, 278 of them from general knowledge and marked so):
  - "needs" (2,208): a technique, capital, institution or route;
  - "input" (630): a material, fuel or power;
  - "switch" (244): a substitution that freed a chain;
  - "by-product" (32): a joint product that became an industry.
- **Time and unlocking:** the time axis is piecewise, and each era is widened by how much happened in it. A year scrubber with a
  sparkline unlocks things as time passes.
- **A node:** clicking one shows its direct links, the whole chain behind it, or everything it led to, with its notes and the part
  it came from. 90 nodes are marked as chokepoints the parts name.
- **Societies:** the 11 types and 6 branches of part 06 as markers above the lanes. A separate tab shows their spans, the 22
  transitions, 5 collapses, 31 theories, and part 09's reading of the engine's distance from each.

## How it was made, and how far to trust it

Six extraction passes each read two parts in full (part 13 with part 06's types) and wrote nodes and edges to a shared schema and
seed vocabulary (`passes/BRIEF.md`, outputs in `passes/`). `build.py` merges them:
- `aliases.json` folds duplicate ids made by different passes;
- `date_overrides.json` re-dates five shared nodes to their earliest form anywhere;
- `seed_fallback.tsv` gives a short general entry for 35 shared nodes that passes linked to but none defined (charcoal, coal, the
  watermill, the blast furnace among them). Each says so on the page.

Rebuild with `python3 build.py passes` from this folder.

Limits:
- **Dates:** 739 of the 1,335 come from general knowledge rather than the part (marked "date: general"; 450 of 908 before 16 Nov), because several parts date
  by decade or not at all.
- **Backward links:** about 60 links run backwards in time, because a node is dated to its earliest form while the link concerns
  a later one (the bloomery's charcoal, wage labour's spread).
- **Depth counts:** chain depths are longest paths and are inflated where passes made fine-grained steps.
- **What a node is:** a reading of the parts, not a check of them. The figures keep the parts' own tags.

Nothing here is a Cybertron 2 decision.
