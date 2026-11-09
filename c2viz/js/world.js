// c2viz/js/world.js: the region's map for a day.
(function (X) {
  "use strict";
  const { D, PAL, Px, drawBuilding, drawTrees, geom, hstr, model, node, noise, weatherField, skyOver, wildRegion, paintLand, paintPath, paintRoad, peaks, person, personLabel, plan, regionPlan, rng, styleOf, verges, weatherOver } = X;
  // ---------------------------------------------------------------------------------------------------- the region
  // each place's ground plan at one scale for all places (so a big place looks big), in its own territory; its buildings at their
  // footprint, smaller, its people as small figures, roads between places from their ends, travellers at the middle of the stretch
  // they are on, landmarks on their stretches. Unexplored places are drawn as they are: the world exists before anyone finds it.
  function world(cv, V, day, opts = {}) {
    const M = model(V), d = D(V, day), ST = V.static, WL = ST.layout.world, nids = Object.keys(ST.nodes).sort();
    const RP = regionPlan(V), W = RP.W, H = RP.H, G = RP.G, pos = RP.pos, f = RP.f, R = rng(M.seed ^ 77), P = Px(cv, W, H, "#6ca63c"), out = { width: W, height: H, hotspots: [] };
    const toWorld = (n, x, y) => [pos[n][0] + (x - G[n].mid[0]) * f, pos[n][1] + (y - G[n].mid[1]) * f];
    const cellNode = RP.cellNode, cellPar = RP.cellPar, occ = new Uint8Array(W * H);
    const courses = RP.rivers.slice();
    nids.forEach((n, ni) => { for (const c of G[n].courses) courses.push({ pid: c.pid, pids: c.pids, n: ni, half: Math.max(1, c.half * f), line: c.line.map(([x, y]) => toWorld(n, x, y)) }); });
    const WF = d.places ? weatherFieldOf(V, RP, day, d) : null;                                  // the day's weather by place, blended
    const ctx = paintLand(P, V, day, W, H, nids, cellNode, cellPar, f, R, occ, { scale: "world", courses, relief: RP, snowAt: WF ? WF.snowAt : null });
    const n2 = noise(M.seed ^ 5), paint = paintRoad(P, occ, ctx.LV, W, H, ctx.face), roadPts = {};
    for (const [rid, r] of Object.entries(ST.roads)) {
      if (!RP.paths[rid]) continue;
      const pts = RP.paths[rid], a = pts[0], hid = Object.values(r.ends || {}).some((e) => e.hidden);
      paintPath(paint, pts, r.track ? 1 : 0, r.track ? PAL.road : PAL.lane, hid ? (x, y) => (Math.round(x) + Math.round(y)) % 3 : null);
      roadPts[rid] = pts;
      const mid = pts[pts.length >> 1] || a;
      out.hotspots.push({ kind: "road", id: rid, x: (mid[0] | 0) - 4, y: (mid[1] | 0) - 4, w: 8, h: 8, label: `${ST.nodes[r.a]?.name} — ${ST.nodes[r.b]?.name}: ${r.days} day${r.days > 1 ? "s" : ""}${r.track ? ", a cart track" : ""}${r.terrain ? ", " + r.terrain : ""}` });
      const ch = (d.roads[rid] || {}).challenges || {};
      (r.stretches || []).forEach((st, i, all) => (st.landmarks || []).forEach((lm, j) => {               // landmarks on their stretch
        const p = pts[Math.min(pts.length - 1, RP.sidx[rid][i] + j * 8)]; if (!p) return;
        const k = lm.kind || lm, x = p[0] | 0, y = p[1] | 0, c = ch[`${i + 1}:${k}`];
        if (k === "ford") { for (let a = -2; a <= 2; a++) { P.put(x + a, y, c ? "#4e94a8" : "#7cc0c8"); P.put(x + a, y + 1, c ? "#3e8498" : "#5aa2b4"); } }
        else if (k === "bridge") { for (let a = -2; a <= 2; a++) { P.put(x + a, y - 1, c ? "#6b4423" : "#8a5a2a"); P.put(x + a, y + 1, "#5aa2b4"); } P.put(x - 2, y, "#6b4423"); P.put(x + 2, y, "#6b4423"); if (c) P.put(x, y - 1, "#2a1a10"); }
        else if (k === "pass") { for (let a = -2; a <= 2; a++) P.put(x + a, y - 1 + Math.abs(a) - 2, "#9a9aa0"); P.put(x, y - 3, c ? "#ffffff" : "#b4b4ba"); }
        else if (k === "spring") { P.put(x + 2, y - 1, "#7cc0c8"); P.put(x + 3, y - 1, "#5aa2b4"); }
        else if (k === "fruit trees") { P.put(x + 2, y - 2, "#3a8a3e"); P.put(x + 3, y - 2, "#c8553d"); P.put(x + 2, y - 1, "#5a3a24"); }
        else { P.put(x + 2, y - 2, "#e8e8e0"); P.put(x + 2, y - 1, "#a8a29a"); P.put(x + 3, y - 1, "#c8c4bc"); }
        out.hotspots.push({ kind: "landmark", id: rid + ":" + i + ":" + j, x: x - 2, y: y - 3, w: 6, h: 6, label: `${k} on day ${i + 1} of the road${c ? ` (${c})` : ""}` }); }));
    }
    for (const n of nids) for (const e of geom(V, n).exits) for (const way of e.draw)                  // the village's own roads, as close up
      paintPath(paint, way.map(([x, y]) => toWorld(n, x, y)), 0, PAL.lane);
    verges(P, occ, ctx.LV, W, H, 0.18);
    const items = [];
    for (const n of nids) {
      const pl = plan(V, n, day); let tx = 0, ty = 0, tn = 0;
      const KW = 0.6;                                                                       // houses on the region's map: larger than its scale
      const hs = Object.entries(pl.buildings).map(([bid, p]) => { const [x, y] = toWorld(n, p.x + p.w / 2, p.y + p.h / 2), S = styleOf(bid, p.b, KW); return { x, y, x0: x, y0: y, w: S.w, h: S.h, b: p.b, bid }; });
      for (let it = 0; it < 60; it++) { for (const a of hs) for (const c of hs) { if (a === c) continue; const ox = (a.w + c.w) / 2 + 2 - Math.abs(a.x - c.x), oy = (a.h + c.h) / 2 + 2 - Math.abs(a.y - c.y);
          if (ox > 0 && oy > 0) { if (ox < oy) { const s_ = Math.sign(a.x - c.x || 1) * ox / 2; a.x += s_; c.x -= s_; } else { const s_ = Math.sign(a.y - c.y || 1) * oy / 2; a.y += s_; c.y -= s_; } } }
        for (const a of hs) { a.x += (a.x0 - a.x) * 0.02; a.y += (a.y0 - a.y) * 0.02; } }
      for (const q of hs) { const bx = Math.round(q.x - q.w / 2), by = Math.round(q.y - q.h / 2), w = q.w, h = q.h, x = q.x, y = q.y;
        items.push({ y: by + h, f: () => drawBuilding(P, bx, by, q.b, R, q.bid, KW) }); tx += x; ty += y; tn++;
        for (let yy = by + h - 3; yy < by + h + 3; yy++) for (let xx = bx - 2; xx < bx + w + 2; xx++) { const i = ctx.at(xx, yy); if (i >= 0 && ctx.LV[i] > 0 && occ[i] !== 3) P.put(xx, yy, ctx.snow ? PAL.snow[2] : PAL.ground[(xx + yy) & 1]); }
        for (let yy = by - 1; yy < by + h + 2; yy++) for (let xx = bx - 1; xx < bx + w + 1; xx++) { const i = ctx.at(xx, yy); if (i >= 0) occ[i] = 4; } }
      for (const h of pl.herds) for (const [x0, y0, role] of h.pts.slice(0, 10)) { const [x, y] = toWorld(n, x0, y0), col = role === "oxen" ? "#a0663a" : role === "bulls" ? "#4a3428" : "#f4efe6";
        items.push({ y, f: () => { P.put(x, y, col); P.put(x + 1, y, col); P.dark(x + 2, y, .3); } }); }
      for (const t of pl.things) { const [x, y] = toWorld(n, t.x, t.y); items.push({ y, f: () => t.t.kind === "remains" ? (P.put(x, y - 1, t.t.buried != null ? "#c8c4bc" : "#d8d2c4"), P.put(x, y, "#7a5a3a")) : P.put(x, y, "#c9b38a") }); }
      for (const q of pl.people) { const [x, y] = toWorld(n, q.x + 2, q.y); items.push({ y, f: () => person(P, x, y, q.name, { child: q.p.stage === "child" || q.p.stage === "infant", hungry: q.p.hunger <= -1 ? -q.p.hunger : 0 }) });
        out.hotspots.push({ kind: "person", id: q.name, x: (x | 0) - 2, y: (y | 0) - 6, w: 5, h: 7, label: personLabel(q, d, V), node: n }); }
      const pop = Object.values(d.people).filter((p) => p.alive && p.at === n).length, [cx, cy] = tn ? [tx / tn, ty / tn] : pos[n];
      out.hotspots.push({ kind: "node", id: n, x: (pos[n][0] - G[n].land * f * 0.7) | 0, y: (pos[n][1] - G[n].land * f * 0.6) | 0, w: G[n].land * f * 1.4, h: G[n].land * f * 1.2, cx, cy: Math.min(H - 12, cy + 6), label: ST.nodes[n].name, pop,
        unexplored: !!ST.nodes[n].unexplored, biome: M.nodes[n].biome, deaths: d.events.filter((e) => e.place === n && e.kind === "death").length });
    }
    drawTrees(P, ctx.trees, ctx, occ, W, H, R);
    peaks(P, RP, cellPar, occ, W, H, ctx.snow || ctx.season === "winter", 1);
    wildRegion(P, V, d, RP, items, (x, y) => occ[(y | 0) * W + (x | 0)] >= 3);                   // the wild layer's kinds (D2-199)
    items.sort((a, b) => a.y - b.y).forEach((it) => it.f());
    for (const [name, p] of Object.entries(d.people)) {                                             // travellers, at the middle of their stretch
      const t = p.transit; if (!t || !p.alive) continue; const r = ST.roads[t.road], pts = roadPts[t.road]; if (!r || !pts || !pts.length) continue;
      const q = pts[RP.sidx[t.road][Math.max(0, Math.min(RP.sidx[t.road].length - 1, t.pos - 1))] ?? 0], k = Object.keys(d.people).filter((m) => d.people[m].transit && d.people[m].transit.road === t.road && d.people[m].transit.pos === t.pos).indexOf(name);
      person(P, q[0] + k * 4, q[1] - 1, name, { tool: "carry" });
      out.hotspots.push({ kind: "person", id: name, x: (q[0] | 0) - 2 + k * 4, y: (q[1] | 0) - 7, w: 6, h: 8, label: `${name} on the road to ${ST.nodes[t.to]?.name || t.to}, day ${t.pos} of ${t.days}` });
    }
    // each place's own weather over its own ground (D4-111); a place's values where the weather scheduler gives them (D4-109)
    if (WF) { weatherField(P, W, H, WF.at, rng(hstr("weather|" + day)), true);
      skyOver(P, W, H, WF.at, rng(hstr("sky|" + day)), true, { avoid: (x, y) => nids.some((n) => Math.hypot(x - pos[n][0], y - pos[n][1]) < RP.rad(n) * 0.9),
        low: (x, y) => Math.max(0.3, 1.4 - 0.4 * (RP.level[(y | 0) * W + (x | 0)] || 1)) }); }
    else weatherOver(P, W, H, d.weather, rng(hstr("weather|" + day)), true);
    // storms still crossing the region (D4-110): on the scheduler's own plane of the places (km), laid onto this map by the
    // similarity that best fits its places to where the map has them (a presentation choice)
    const sky = d.sky, CL = ST.climate_layout;
    if (sky && CL && (sky.storms || []).length) { const fit = planeFit(CL, pos);
      if (fit) for (const st of sky.storms) { const [cx, cy] = fit.at(st.at), r = Math.max(14, st.radius * fit.s), nS = noise(hstr(st.id));
        for (let y = Math.max(0, cy - r | 0); y < Math.min(H, cy + r); y++) for (let x = Math.max(0, cx - r | 0); x < Math.min(W, cx + r); x++) {
          const dd = Math.hypot(x - cx, y - cy) / r * (0.85 + 0.3 * nS(x / 18, y / 18, 2)); if (dd > 1) continue;
          P.mix(x, y, "#1e2438", 0.45 * (1 - dd * dd)); if (nS(x / 3 + 5, y / 3, 1) > 0.86) P.mix(x, y, "#c8d0e0", 0.35); }
        out.hotspots.push({ kind: "storm", id: st.id, x: (cx - r) | 0, y: (cy - r) | 0, w: 2 * r, h: 2 * r, label: `a storm crossing the region (wind ${st.wind} m/s at its heart)` }); } }
    for (const h of out.hotspots) if (h.kind === "node") { const v = (d.places || {})[h.id]; if (!v) continue;      // the place's weather, on hover
      h.info = [v.weather, v.rain != null ? `${v.rain} mm` : null, v.wind != null ? `wind ${v.wind} m/s` : null, v.temp != null ? `${v.temp}\u00b0C, night ${v.low}\u00b0C` : null,
        v.frost ? "frost" : null, v.storm > 0.25 ? "a storm passing" : null, v.coming ? "a storm coming" : null].filter(Boolean).join(", ");
      if (v.coming) { const x = h.cx | 0, y = (h.cy | 0) - 16;                                                          // a dark sky to windward
        for (const [a, b] of [[0, 0], [1, 0], [2, 0], [3, 0], [-1, 1], [0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [0, -1], [1, -1], [2, -1]]) P.put(x + a, y + b, "#2a3048");
        P.put(x + 1, y + 3, "#c8dcf0"); P.put(x + 3, y + 3, "#c8dcf0"); } }
    out.season = ctx.season; out.scale = f;
    if (sky) out.phase = `${sky.type} weather${sky.era && sky.era !== "steady" ? ", a " + sky.era + " era" : ""}${sky.shock ? ", " + sky.shock : ""}`;   // the region's sky (D4-109)
    { let best = null, bp = -1; for (const h of out.hotspots) if (h.kind === "node" && h.pop > bp) { bp = h.pop; best = h; } if (best) out.focus = [best.cx, best.cy]; }
    P.flush();
    return out;
  }
  // the day's weather as a field over the region's map: each place's own (D4-111) weighted by nearness to it (a soft edge between
  // places, as the scheduler's own fields are alike between near places, D4-109), each weight taken against the nearest place's
  // distance so far ground keeps its nearest's and nothing jumps. A presentation of values the engine gives at places only, named as one (ENGINE.md §12)
  const FIELDS = new WeakMap();
  function weatherFieldOf(V, RP, day, d) {
    let c = FIELDS.get(V); if (!c) FIELDS.set(V, c = {}); if (c[day]) return c[day];
    const { W, H, pos, nids } = RP, N = W * H, k = nids.length, P0 = d.places || {};
    const near = nids.map((n, i) => Math.min(...nids.filter((m, j) => j !== i).map((m) => Math.hypot(pos[m][0] - pos[n][0], pos[m][1] - pos[n][1])), 1e9));
    const sig = Math.max(40, 0.45 * near.slice().sort((a, b) => a - b)[k >> 1]), labels = [];
    const vals = nids.map((n) => { const v = P0[n] || d, L = v.weather || "clear"; if (!labels.includes(L)) labels.push(L);
      return { L: labels.indexOf(L), rain: v.rain ?? (RAINYW.has(L) ? (L === "heavy rain" ? 12 : 4) : 0), wind: v.wind ?? (L === "gale" ? 18 : 4), storm: v.storm || 0,
        fog: L === "fog" ? 1 : 0, frost: v.frost ? 1 : 0, snow: v.snow ? 1 : 0 }; });
    const rain = new Float32Array(N), wind = new Float32Array(N), storm = new Float32Array(N), fog = new Float32Array(N), frost = new Float32Array(N), snow = new Float32Array(N), kind = new Uint8Array(N);
    const w = new Float32Array(k), vote = new Float32Array(labels.length);
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) { const i = y * W + x; let sw = 0;
      let dmin = 1e18; for (let j = 0; j < k; j++) { const p = pos[nids[j]]; w[j] = (x - p[0]) ** 2 + (y - p[1]) ** 2; if (w[j] < dmin) dmin = w[j]; }
      for (let j = 0; j < k; j++) { w[j] = Math.exp(-(w[j] - dmin) / (2 * sig * sig)); sw += w[j]; }      // against the nearest: continuous, never empty
      vote.fill(0); let r = 0, wi = 0, st = 0, fg = 0, fr = 0, sn = 0;
      for (let j = 0; j < k; j++) { const a = w[j] / sw, v = vals[j]; r += a * v.rain; wi += a * v.wind; st += a * v.storm; fg += a * v.fog; fr += a * v.frost; sn += a * v.snow; vote[v.L] += a; }
      let b = 0; for (let l = 1; l < labels.length; l++) if (vote[l] > vote[b]) b = l;
      rain[i] = r; wind[i] = wi; storm[i] = st; fog[i] = fg; frost[i] = fr; snow[i] = sn; kind[i] = b; }
    const nS = noise(hstr("snow|" + day));
    const F = { snowAt: (i) => snow[i] + (nS((i % W) / 14, ((i / W) | 0) / 14, 2) - 0.5) * 0.3 > 0.5,
      at: (x, y) => { const i = y * W + x; return { kind: labels[kind[i]], rain: rain[i], wind: wind[i], storm: storm[i], fog: fog[i], frost: frost[i] }; } };
    return (c[day] = F);
  }
  const RAINYW = new Set(["rain", "heavy rain", "snow"]);
  // the similarity (scale, rotation, maybe a mirror) that best lays one set of points onto another (least squares)
  function planeFit(src, dst) {
    const ks = Object.keys(src).filter((k) => dst[k]); if (ks.length < 2) return null;
    const best = [1, -1].map((m) => { const S = ks.map((k) => [src[k][0], m * src[k][1]]), D_ = ks.map((k) => dst[k]);
      const ms = [S.reduce((a, p) => a + p[0], 0) / S.length, S.reduce((a, p) => a + p[1], 0) / S.length], md = [D_.reduce((a, p) => a + p[0], 0) / D_.length, D_.reduce((a, p) => a + p[1], 0) / D_.length];
      let a = 0, b = 0, ss = 0; S.forEach((p, i) => { const x = p[0] - ms[0], y = p[1] - ms[1], u = D_[i][0] - md[0], v = D_[i][1] - md[1]; a += x * u + y * v; b += x * v - y * u; ss += x * x + y * y; });
      const c = a / (ss || 1), s_ = b / (ss || 1), f = (p) => { const x = p[0] - ms[0], y = m * p[1] - ms[1]; return [md[0] + c * x - s_ * y, md[1] + s_ * x + c * y]; };
      const err = ks.reduce((e, k, i) => { const q = f(src[k]); return e + (q[0] - dst[k][0]) ** 2 + (q[1] - dst[k][1]) ** 2; }, 0);
      return { at: f, s: Math.hypot(c, s_), err }; });
    return best[0].err <= best[1].err ? best[0] : best[1];
  }
  Object.assign(X, { world, planeFit });
})(C2X);
