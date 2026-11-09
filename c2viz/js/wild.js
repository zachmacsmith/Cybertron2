// c2viz/js/wild.js: the wild layer (37.2's, D2-199; the `wild` pack): wild kinds in the land's areas by their counts, the groups near people at the wood's edge or in the corn, their traces, the watches kept. ENGINE.md §15.
(function (X) {
  "use strict";
  const { hstr, noise, rng } = X;
  // ---------------------------------------------------------------------------------------------------- how each kind looks
  // The engine's kinds (RESOURCES rows with renewal "population") by name. `per`: heads a sprite stands for on the region's map, `cap`
  // sprites an area at most (a presentation choice: the map shows where a kind is and how thick, not every head); `near`: heads a sprite
  // close up; `on`: where it is drawn (the habitat keys of the kind's own row, read against the ground). A kind not listed is not drawn
  // (voles and mice, eels: too small or under water to see from above).
  const WILD = {
    "red deer":   { per: 12, cap: 5, near: 1, cap2: 6 },
    "roe deer":   { per: 20, cap: 4, near: 1, cap2: 3 },
    "wild boar":  { per: 8, cap: 4, near: 1, cap2: 6 },
    "brown hare": { per: 250, cap: 3, near: 20, cap2: 3 },
    "woodpigeon": { per: 600, cap: 3, near: 60, cap2: 6, flock: 5 },
    "rats":       { per: 0, cap: 0, near: 120, cap2: 3 },
    "wildfowl":   { per: 30, cap: 5, near: 10, cap2: 6, flock: 3, water: true },
    "fox":        { per: 10, cap: 2, near: 3, cap2: 1 },
    "wolf":       { per: 2, cap: 3, near: 1, cap2: 4 },
    "raven":      { per: 12, cap: 2, near: 4, cap2: 2, flock: 2 },
    "brown bear": { per: 1, cap: 2, near: 1, cap2: 1 },
  };
  const BIG = new Set(["red deer", "roe deer", "wild boar", "fox", "wolf", "brown bear"]);   // drawn whole on the region's map too
  // ---------------------------------------------------------------------------------------------------- sprites (close up; `s` 0 for the region's map)
  function beastOf(P, x, y, kind, R, f = 0, big = true) {
    x |= 0; y |= 0; const put = (pts, c) => { for (const [dx, dy] of pts) P.put(x + dx, y + dy, c); }, shade = (n) => { for (let dx = 0; dx < n; dx++) P.dark(x + dx + 1, y + 1, .25); };
    if (!big) {                                                                                     // the region's map: a mark of the kind's colour
      const c = { "red deer": "#8a5a36", "roe deer": "#a8703e", "wild boar": "#2e2620", "brown hare": "#a8845a", woodpigeon: "#9aa0b0", wildfowl: "#5a6a40",
        fox: "#c8602a", wolf: "#5e6066", raven: "#141418", "brown bear": "#4a3020" }[kind] || "#6a5a4a";
      const L = kind === "brown bear" || kind === "red deer" || kind === "wolf" || kind === "wild boar" ? 3 : 2;
      for (let dx = 0; dx < L; dx++) { P.put(x + dx, y, c); P.dark(x + dx, y + 1, .2); } if (L === 3) P.put(x + 2, y - 1, c); return;
    }
    const head = f & 1;                                                                             // two frames: head up, head down (grazing)
    if (kind === "red deer" || kind === "roe deer") {
      const roe = kind === "roe deer", L = roe ? 4 : 6, body = roe ? "#a8703e" : "#8a5a36", rump = "#e8dcc0"; shade(L + 1);
      for (let dx = 0; dx < L; dx++) { P.put(x + dx, y - 3, body); P.put(x + dx, y - 2, body); }
      P.put(x, y - 3, rump); put([[0, 0], [1, -1], [L - 2, -1], [L - 1, 0]], "#4a3020");
      if (head) put([[L, -2], [L + 1, -1]], body); else { put([[L, -4], [L, -5], [L + 1, -5]], body); if (!roe && (hstr(String(x * 7 + y)) & 1)) put([[L - 1, -7], [L, -6], [L + 1, -7], [L + 2, -6]], "#d8c8a0"); }
      return;
    }
    if (kind === "wild boar") { shade(6);
      for (let dx = 0; dx < 6; dx++) { P.put(x + dx, y - 3, "#3a3028"); P.put(x + dx, y - 2, "#2e2620"); P.put(x + dx, y - 1, "#2e2620"); }
      put([[1, -4], [2, -4], [3, -4]], "#4a3e34");                                                 // the bristled ridge
      put(head ? [[6, -1], [7, -1]] : [[6, -2], [7, -2]], "#5a4a3e"); P.put(x + 7, y - (head ? 0 : 1), "#d8c8b0");   // snout and tusk
      put([[1, 0], [4, 0]], "#1e1814"); return; }
    if (kind === "brown hare") { P.dark(x + 1, y + 1, .2);
      put([[0, -1], [1, -1], [2, -1], [1, -2], [2, -2]], "#a8845a"); put(head ? [[3, -1]] : [[3, -2], [3, -3], [4, -4]], "#a8845a"); P.put(x, y - 2, "#e8e0d0"); return; }
    if (kind === "woodpigeon") { put([[0, -1], [1, -1], [2, -1]], "#9aa0b0"); P.put(x + 2, y - 2, "#7a8090"); P.put(x + 1, y - 2, "#e8e8f0"); if (head) P.put(x + 3, y - 1, "#7a8090"); return; }
    if (kind === "rats") { put([[0, 0], [1, 0]], "#4a3a30"); P.put(x + 2 + (head ? 1 : 0), y, "#6a5a50"); return; }
    if (kind === "wildfowl") { put([[0, 0], [1, 0], [2, 0]], "#8a7458"); put(head ? [[3, 0]] : [[3, -1]], "#2e6a3a"); P.mix(x - 1, y + 1, "#ffffff", .3); P.mix(x + 3, y + 1, "#ffffff", .3); return; }
    if (kind === "fox") { shade(5); put([[0, -2], [1, -2], [2, -2], [3, -2], [1, -1], [2, -1]], "#c8602a"); put([[-1, -1], [-2, -1]], "#c8602a"); P.put(x - 3, y - 1, "#f0e8e0");
      put(head ? [[4, -2], [5, -2]] : [[4, -3], [5, -3]], "#c8602a"); put([[1, 0], [3, 0]], "#2a1a10"); return; }
    if (kind === "wolf") { shade(6);
      for (let dx = 0; dx < 6; dx++) { P.put(x + dx, y - 3, "#4e5056"); P.put(x + dx, y - 2, "#6e7076"); }
      put([[-1, -2], [-2, -1]], "#5e6066"); put(head ? [[6, -2], [7, -2]] : [[6, -3], [7, -3], [6, -4]], "#5e6066"); put([[0, 0], [1, -1], [4, -1], [5, 0]], "#3a3a40"); return; }
    if (kind === "raven") { put([[0, -1], [1, -1], [2, -1], [1, -2]], "#141418"); if (head) { P.put(x - 1, y - 2, "#141418"); P.put(x + 3, y - 2, "#141418"); } return; }
    if (kind === "brown bear") { shade(7);
      for (let dx = 0; dx < 7; dx++) for (let dy = -4; dy < 0; dy++) if (!(dy === -4 && (dx === 0 || dx === 6))) P.put(x + dx, y + dy, "#4a3020");
      put(head ? [[7, -2], [8, -2]] : [[7, -3], [8, -3]], "#5a3a28"); P.put(x + 8, y - (head ? 2 : 3), "#2a1a10"); put([[1, 0], [5, 0]], "#2a1a10"); return; }
  }
  // ---------------------------------------------------------------------------------------------------- the habitat under a point
  // the habitat keys of the engine's kinds (wood, shrub, open, grassy, farm, heath, wet) read off what is drawn: a presentation of the
  // generator's areas' features, which the engine reads as shares, not places
  const HAB_OF_COVER = { forest: "wood", scrub: "shrub", pasture: "grassy", meadow: "grassy", field: "farm", heath: "heath", moor: "heath", fen: "wet", saltmarsh: "wet", built: null };
  const habWeight = (row, h) => !row || !h ? 0 : (row[h] ?? (h === "grassy" ? row.open : h === "open" ? row.grassy : 0) ?? 0);
  // ---------------------------------------------------------------------------------------------------- the region's map
  // Each wild area's kinds, as the engine counts them that day, scattered over the ground nearest the area's own point (its place in the
  // generator's land summary) where the ground suits the kind; a village's ring at the village. Rings and wild areas only: a village's
  // home area is its close up.
  function wildRegion(P, V, d, RP, items, avoid) {
    const WA = V.static.wild_areas, wd = d.wild, LD = V.land; if (!WA || !wd || !LD) return;
    const { W, H } = RP, PXg = X.GROUND_PX || 4, km = LD.grid.km, ny = LD.grid.ny, KR = (V.tables || {}).wild || {};
    const at = WA.ids.map((a) => { const A = WA.areas[a]; if (A.kind === "ring" && RP.pos[A.node]) return RP.pos[A.node];
      return [(A.xy_km[0] / km + 0.5) * PXg, (ny - 1 - A.xy_km[1] / km + 0.5) * PXg]; });
    const use = WA.ids.map((a) => WA.areas[a].kind !== "home");
    const step = 7, cand = WA.ids.map(() => []);
    for (let y = 3; y < H; y += step) for (let x = 3; x < W; x += step) { const i = y * W + x; if (RP.cellPar[i] >= 0 || (avoid && avoid(x, y))) continue;
      let best = -1, bd = 1e18; for (let j = 0; j < at.length; j++) { if (!use[j]) continue; const dd = (x - at[j][0]) ** 2 + (y - at[j][1]) ** 2; if (dd < bd) { bd = dd; best = j; } }
      if (best >= 0) cand[best].push(i); }
    const habAt = (i) => RP.level[i] === 0 ? "water" : RP.wood[i] ? "wood" : RP.kind[i] === 3 ? "wet" : RP.kind[i] === 4 ? "heath" : RP.kind[i] === 1 ? "shrub" : "open";
    for (const [kind, look] of Object.entries(WILD)) { const cnt = wd.counts[kind]; if (!cnt || !look.per) continue; const row = (KR[kind] || {}).hab || {};
      WA.ids.forEach((a, j) => { if (!use[j] || !cand[j].length) return; const n = Math.min(look.cap, Math.floor(cnt[j] / look.per)); if (n <= 0) return;
        const R = rng(hstr(kind + "|" + a + "|" + d.day)), ok = cand[j].filter((i) => look.water ? habAt(i) === "water" : habWeight(row, habAt(i)) > 0.15);
        for (let k = 0; k < n && ok.length; k++) { const i = ok[(R() * ok.length) | 0], x = i % W, y = (i / W) | 0, fl = look.flock || 1;
          const big = BIG.has(kind), f0 = (R() * 2) | 0;                                              // the larger beasts as themselves, small ones as marks
          for (let q = 0; q < fl; q++) { const xx = x + (q ? (R() - 0.5) * 6 : 0), yy = y + (q ? (R() - 0.5) * 4 : 0); items.push({ y: yy, f: () => beastOf(P, xx, yy, kind, R, f0 + q, big) }); } } }); }
  }
  // ---------------------------------------------------------------------------------------------------- close up
  // A village's own wild (its home area's counts, spread over the parcels where each kind's habitat is, as many as the place's share
  // of the area); the groups near people at the wood's edge (the parcel the engine has them come out of) when they are on their way;
  // their traces on the parcels (rooting, raid, turned back, fading over the three days the engine keeps them); a watch's fire.
  function wildNode(P, V, d, nid, G, ctx, items, opts = {}) {
    const WA = V.static.wild_areas, wd = d.wild; if (!WA || !wd) return [];
    const KR = (V.tables || {}).wild || {}, hot = [], ST = V.static, N = G.pids.length;
    const homeIx = WA.ids.findIndex((a) => WA.areas[a].kind === "home" && WA.areas[a].node === nid); if (homeIx < 0) return [];
    const areaKm2 = +WA.areas[WA.ids[homeIx]].km2 || 1, pidIx = (pid) => G.pids.indexOf(pid);
    const pts = (k, i, R, filt) => { const a = G.area[k] || []; const ok = filt ? a.filter(filt) : a; return ok.length ? ok[(R() * ok.length) | 0] : null; };
    // traces first: they are on the ground
    for (const [pid, lst] of Object.entries(wd.traces || {})) { const k = pidIx(pid); if (k < 0) continue;
      for (const t of lst) { const age = d.day - (+t.day), a = Math.max(0.25, 1 - age / 3.5), R = rng(hstr(pid + t.kind + t.what + t.day));
        const n = t.what === "raid" ? 26 : t.what === "edge" ? 22 : 10, c = t.kind === "wild boar" ? "#5a3e24" : "#4a3a2a";
        const near = t.what === "edge" ? edgePts(G, k, pid, ST) : null;
        for (let j = 0; j < n; j++) { const p = near && near.length ? near[(R() * near.length) | 0] : pts(k, j, R); if (!p) break; const [x, y] = p;
          if (t.what === "raid") { for (let q = -3; q < 4; q++) for (let r = 0; r < 2; r++) P.mix(x + q, y + r, (q + r) & 1 ? "#6b4a2a" : "#b8a070", 0.8 * a); }   // corn flattened and rooted, in patches
          else if (t.kind === "wild boar") { P.mix(x, y, c, 0.8 * a); P.mix(x + 1, y, "#6b4a2a", 0.7 * a); P.mix(x, y + 1, "#3e2a18", 0.5 * a); }   // turf rooted over
          else { P.mix(x, y, c, 0.6 * a); P.mix(x + 2, y + 1, c, 0.6 * a); } }                   // slots
        const [cx, cy] = G.centre[k]; hot.push({ kind: "trace", id: pid + "|" + t.kind + t.day + t.what, x: cx - 6, y: cy - 6, w: 12, h: 12,
          label: `${t.what === "raid" ? "raided in the night" : t.what === "edge" ? "fresh rooting at the edge" : "turned back"}: ${t.kind}, about ${t.n} (${age ? age + " night" + (age > 1 ? "s" : "") + " ago" : "last night"})` }); } }
    // a watch kept over a field tonight: its fire at the field's edge
    for (const [pid, wv] of Object.entries(wd.watch || {})) { const k = pidIx(pid); if (k < 0) continue; const p = edgePts(G, k, pid, ST)[0] || G.centre[k];
      if (wv.scare === "fire") items.push({ y: p[1], f: () => { P.put(p[0], p[1] - 1, "#f0a030"); P.put(p[0] + 1, p[1] - 2, "#f8d060"); P.put(p[0], p[1], "#6b4423"); P.put(p[0] + 1, p[1], "#6b4423"); } }); }
    // the groups on their way: at the edge of the field they mean to raid
    for (const [gid, g] of Object.entries(wd.groups || {})) { if (g.node !== nid || !(g.pos === "edge" || g.pos === "ready") || !g.target) continue;
      const k = pidIx(g.target); if (k < 0) continue; const R = rng(hstr(gid + d.day)), ep = edgePts(G, k, g.target, ST);
      for (let j = 0; j < Math.min(g.n, (WILD[g.kind] || {}).cap2 || 6); j++) { const p = ep[(R() * ep.length) | 0]; if (!p) break; const f = (R() * 2) | 0;
        items.push({ y: p[1], f: () => beastOf(P, p[0], p[1], g.kind, R, f) }); }
      const p0 = ep[0] || G.centre[k]; hot.push({ kind: "beasts", id: gid, x: p0[0] - 10, y: p0[1] - 10, w: 20, h: 14, label: `${g.kind}, about ${g.n}, at the edge of ${ST.parcels[g.target]?.name || g.target}` }); }
    // the village's own wild: its home area's count over the parcels that suit each kind, by their share of the area's ground
    for (const [kind, look] of Object.entries(WILD)) { const cnt = (wd.counts[kind] || [])[homeIx]; if (!cnt) continue;
      if ((KR[kind] || {}).count === "whole") continue;                                             // whole-counted kinds come as their group, above
      const row = (KR[kind] || {}).hab || {};
      for (let k = 0; k < N; k++) { const pid = G.pids[k], cov = ST.parcels[pid].cover, h = cov === "water" ? "water" : HAB_OF_COVER[cov], wt = look.water ? (h === "water" ? 1 : 0) : habWeight(row, h);
        if (wt <= 0.15 && !(kind === "rats" && cov === "built")) continue;
        const share = (+ST.parcels[pid].size || 1) * 0.02 / areaKm2, n = Math.min(look.cap2, Math.round(cnt * share / look.near)); if (n <= 0) continue;
        const R = rng(hstr(kind + "|" + pid + "|" + d.day));
        for (let j = 0; j < n; j++) { const p = pts(k, j, R); if (!p) break; const fl = look.flock || 1;
          for (let q = 0; q < fl; q++) { const x = p[0] + (q ? ((R() - 0.5) * 8) | 0 : 0), y = p[1] + (q ? ((R() - 0.5) * 5) | 0 : 0), f = (R() * 2) | 0; items.push({ y, f: () => beastOf(P, x, y, kind, R, f) }); } } } }
    return hot;
  }
  // the points of the wood beside a field (the engine's `_edge_of`: a forest or scrub parcel next to it), nearest the field; else the field's own rim
  function edgePts(G, k, pid, ST) {
    const adj = (ST.parcels[pid].adj || []).find((q) => ["forest", "scrub"].includes((ST.parcels[q] || {}).cover)), kk = adj != null ? G.pids.indexOf(adj) : -1;
    const [fx, fy] = G.centre[k], src = kk >= 0 ? G.area[kk] : G.area[k];
    return (src || []).map((p) => [p, Math.hypot(p[0] - fx, p[1] - fy)]).sort((a, b) => a[1] - b[1]).slice(0, 120).map((x) => x[0]);
  }
  // the night's raid, for the day as it happened: the group in the corn at night, or turned back at the edge
  function wildNight(P, V, d, nid, G, t) {
    const wd = d.wild; if (!wd || t < 1.02) return;
    for (const [gid, r] of Object.entries(wd.nights || {})) { const g = (wd.groups || {})[gid] || { kind: gid.split("@")[0], n: 4 }; if (gid.split("@")[1] !== nid) continue;
      const k = G.pids.indexOf(r.raid); if (k < 0) continue; const R = rng(hstr(gid + d.day + "night")), ep = edgePts(G, k, r.raid, V.static);
      const inField = (G.area[k] || []).filter((_, i) => i % 7 === 0);
      for (let j = 0; j < Math.min(g.n || 4, 6); j++) { const p = r.turned ? ep[(R() * ep.length) | 0] : inField[(R() * inField.length) | 0]; if (!p) break;
        beastOf(P, p[0], p[1], g.kind, R, ((t * 30) | 0) + j); } }
  }
  Object.assign(X, { WILD, beastOf, wildRegion, wildNode, wildNight });
})(C2X);
