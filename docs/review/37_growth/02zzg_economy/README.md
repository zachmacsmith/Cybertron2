# 02zzg: the economy as a network (13 Nov 2026, Zach: "a visual way to see the entire economy ... as a network so we can design it")

- `economy_graph.py`: reads the engine's tables (ITEMS, TECHNIQUES, FITTINGS, ROOMS, RESOURCES, the wild methods' scares and
  plants, fuel heat) into one network of goods, acts, fittings and rooms, sources and uses. Roles the tables hold as rules elsewhere
  are listed in its `HAND` block with where each rule lives. Run: `CYB_ROOT=<checkout> python3 economy_graph.py out.json`.
- `economy_peoples_worlds_2020b9e.json`: its output on `peoples-worlds` at 2020b9e (briefs 1 to 4b): 185 nodes, 364 links.
- `economy_map_template.html`: the explorer page; `__DATA__` is replaced by the JSON. Published as an artifact (private to Zach).

Findings on that commit: timber feeds 32 acts, fittings and uses and stone 17; 29 goods have a single use; castoreum, beaver
pelt and offal have none; antler and the hen have no source (worlds seed them); outside metal and bread, few chains run past two
steps. See the session's discussion of wild goods as leaves (13 Nov).
