"""Road-network figures for the designed worlds (design.py): loops (roads - places + 1), dead ends, the farthest place from the first
home, the homes' distances apart, and each place's days from home before and after the cross-roads.

    cd docs/review/39_monoculture && python3 topology.py
"""
import collections
import heapq

import design as D


def dist(roads, s):
    adj = collections.defaultdict(list)
    for a, b, d, _ in roads:
        adj[a].append((b, d))
        adj[b].append((a, d))
    out, q = {s: 0}, [(0, s)]
    while q:
        c, u = heapq.heappop(q)
        if c > out[u]:
            continue
        for v, d in adj[u]:
            if c + d < out.get(v, 1e9):
                out[v] = c + d
                heapq.heappush(q, (c + d, v))
    return out, adj


def stats(w, roads):
    homes = [p["name"] for p in w["places"] if p["kind"].startswith("home")]
    dh, adj = dist(roads, homes[0])
    names = [p["name"] for p in w["places"]]
    apart = [dist(roads, a)[0][b] for i, a in enumerate(homes) for b in homes[i + 1:]]
    return {"places": len(names), "roads": len(roads), "loops": len(roads) - len(names) + 1,
            "dead ends": sum(1 for n in names if len(adj[n]) == 1), "farthest": max(dh.values()),
            "homes apart": (min(apart), max(apart)) if apart else "-", "from home": dh}


if __name__ == "__main__":
    print("| World | Places | Roads before → after | Loops before → after | Dead ends before → after | Farthest from home | Homes apart (days) |")
    print("|---|---|---|---|---|---|---|")
    for k, w in D.WORLDS.items():
        a, b = stats(w, w.get("tree_roads", w["roads"])), stats(w, w["roads"])
        changed = [n for n in a["from home"] if a["from home"][n] != b["from home"][n]]
        print(f"| {k} | {a['places']} | {a['roads']} → {b['roads']} | {a['loops']} → {b['loops']} | {a['dead ends']} → {b['dead ends']} "
              f"| {a['farthest']} → {b['farthest']} | {a['homes apart']} → {b['homes apart']} |" + (f" changed: {changed}" if changed else ""))
