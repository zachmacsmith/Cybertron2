// c2viz/js/land.js: painting the land from a day's record: ground by level and character, terraces, each parcel by its cover and stocks, fields by crop stage and shares, fences, weather, trees.
(function (X) {
  "use strict";
  const { BIOMES, CROP_PAL, D, PAL, STAGE_PAL, STOPS, TREES, fieldAngle, hstr, model, noise, rng, tree } = X;
  // snow lying on the wild land by its year's mean temperature (a generated world's, °C) and the season: on cold high ground in
  // winter, only the coldest tops in spring and autumn, none in summer short of permanent snow (a presentation rule, ENGINE.md §12)
  const snowLies = (t, season) => season === "winter" ? t < 6 : season === "summer" ? t < -4 : t < 2;
  // paint the land from the day's record (c2viz/model.py): each parcel by its cover that day and its stocks (S/K), crops by the
  // engine's stage and their sown and reaped shares, works, fences, clearing; snow when it lies. `cellNode` and `cellPar` give, per
  // pixel, the place (an index into nids) and the parcel (an index into that place's parcels, -1 the wild); `sc` is pixels per
  // close-up pixel (1 close up, smaller on the region's map)
  function paintLand(P, V, day, W, H, nids, cellNode, cellPar, sc, R, occ, opts) {
    const M = model(V), d = D(V, day), season = (d.calendar || {}).season || "summer", snow = d.places ? nids.some((n) => (d.places[n] || {}).snow) : !!d.snow, sdays = V.meta.season_days || 6;
    const n2 = noise(M.seed ^ 2), n3 = noise(M.seed ^ 3), small = sc < 0.5, RL = opts.relief || null, cday = (d.calendar || {}).day || 1;
    const flowering = (season === "summer" && cday > sdays / 2) || (season === "autumn" && cday <= sdays / 2);   // heather: late summer
    const snowAt = opts.snowAt || (() => snow);                                            // where snow lies (the region: by place, D4-111)
    const LV = new Int8Array(W * H), at = (x, y) => (x < 0 || y < 0 || x >= W || y >= H) ? -1 : (y | 0) * W + (x | 0);
    const parcelOf = (i) => { const n = cellNode[i]; if (n < 0 || cellPar[i] < 0) return null; return M.nodes[nids[n]].pids[cellPar[i]]; };
    const cov = (pid) => (d.parcels[pid] || {}).cover || V.static.parcels[pid].cover;
    const area = {}; for (let i = 0; i < W * H; i++) { const p = parcelOf(i); if (p) (area[p] = area[p] || []).push([i % W, (i / W) | 0]); }
    // rivers: water along each course, in its own chain, other water, and the wild; reeds on the banks
    const wet = new Uint8Array(W * H);
    for (const c of opts.courses || []) {
      const reed = small ? 0.6 : 1.8, rr = c.half + reed, e = Math.ceil(rr);
      for (const [lx, ly] of c.line) for (let dy = -e; dy <= e; dy++) for (let dx = -e; dx <= e; dx++) {
        const x = Math.round(lx + dx), y = Math.round(ly + dy), i = at(x, y); if (i < 0 || (c.n != null && cellNode[i] !== c.n)) continue;
        const p = parcelOf(i); if (p && !(c.pids || [c.pid]).includes(p) && STOPS.has(cov(p))) continue;
        const dd = Math.hypot(x - lx, y - ly); if (dd <= c.half) wet[i] = 1; else if (dd <= rr && !wet[i]) wet[i] = 2;
      }
    }
    for (let i = 0; i < W * H; i++) {
      const p = parcelOf(i);
      if (!p) { LV[i] = wet[i] === 1 ? 0 : RL ? RL.level[i] : 1; continue; }
      const P0 = V.static.parcels[p], N = M.nodes[P0.node];
      LV[i] = cov(p) === "water" ? (N.river[N.pids.indexOf(p)] ? (wet[i] === 1 ? 0 : RL ? RL.level[i] : 1) : 0) : wet[i] === 1 ? 0 : RL ? RL.level[i] : Math.max(1, Math.min(3, P0.height ?? 1));
    }
    const lv = (x, y) => { const i = at(x, y); return i < 0 ? -1 : LV[i]; };
    const grassOf = (n, l, v) => { const B = BIOMES[n >= 0 ? M.nodes[nids[n]].biome : "meadow"]; return B.grass[Math.max(0, Math.min(2, l - 1))][v > 0.62 ? 1 : v < 0.36 ? 2 : 0]; };
    // ground
    for (let i = 0; i < W * H; i++) {
      const x = i % W, y = (i / W) | 0, p = parcelOf(i), c = p ? cov(p) : "wild", v = n3(x / 3, y / 3, 2), l = LV[i], n = cellNode[i];
      let col;
      if (l === 0) { let shore = false; for (const [a, b] of [[2, 0], [-2, 0], [0, 2], [0, -2], [1, 1], [-1, -1]]) if (lv(x + a, y + b) > 0) shore = true;
        col = shore ? (n3(x / 2, y / 2, 1) > 0.6 ? PAL.water.foam : PAL.water.shore) : (n3(x / 6, y / 3, 2) > 0.6 ? PAL.water.deep2 : PAL.water.deep); }
      else if (c === "rock") col = PAL.rock[v > 0.7 ? 1 : v < 0.3 ? 2 : 0];
      else col = grassOf(n, l, v);
      if (wet[i] === 2 && l > 0) col = n3(x * 1.5, y * 1.5, 1) > 0.45 ? PAL.reed : col;
      P.put(x, y, col);
      if (!p && l > 0 && RL) {                                                                       // the region's wild land by its kind
        const k = RL.kind[i], moor = n >= 0 && M.nodes[nids[n]].biome === "moor";
        if (k === 2) { P.put(x, y, v > 0.66 ? "#aaa59a" : v < 0.33 ? "#8a857a" : "#9a958a"); if (n3(x * 1.7, y * 1.7, 1) > 0.82) P.put(x, y, "#c4c0b4"); }
        else if (k === 1) { P.mix(x, y, moor ? "#8a7068" : "#8e9a58", moor ? 0.45 : 0.4); if (n3(x * 1.5, y * 1.5, 1) > 0.9) P.put(x, y, "#b8b4aa"); }
        else if (k === 4) { P.put(x, y, RL.tint[i]); if (v > 0.62) P.light(x, y, .07); else if (v < 0.36) P.dark(x, y, .08);   // heath and moor
          const hv = n3(x * 1.3 + 4, y * 1.3, 1); if (hv > 0.78) P.put(x, y, flowering ? "#8a5a7a" : "#6e5a48"); else if (hv < 0.12) P.put(x, y, "#6e7a3a"); }
        else if (k === 3) { P.put(x, y, RL.tint[i]); P.mix(x, y, "#6a8a5a", 0.45); const pv = n3(x / 12 + 3, y / 12, 2); if (pv > 0.7) P.put(x, y, pv > 0.76 ? "#4e7e94" : "#5a8aa0"); else if (pv > 0.64 && n3(x * 2, y * 2, 1) > 0.5) P.put(x, y, PAL.reed); }
        else { P.put(x, y, RL.tint[i]); if (v > 0.62) P.light(x, y, .06); else if (v < 0.36) P.dark(x, y, .06);
          const tg = [null, ["#8cc04c", "#9cd05a", "#7cb042"], ["#7cb444", "#8cc452", "#6ca43a"], ["#6ca63c", "#7cb64a", "#5c9632"], ["#8a9a52", "#9aaa5e", "#7a8a48"]][Math.min(4, l)];
          if (tg) { P.put(x, y, tg[v > 0.62 ? 1 : v < 0.36 ? 2 : 0]); P.mix(x, y, RL.tint[i], RL.tintW ?? 0.3); } if (moor && !RL.ground) P.mix(x, y, flowering ? "#8a6a7a" : "#7e6e52", 0.3);
          if (n3(x / 5 + 1, y / 5, 2) > 0.7) P.dark(x, y, 0.06); }
      }
      else if (!p && l > 0) { P.dark(x, y, 0.13 + 0.06 * (n2(x / 20, y / 20) > .5)); if (!small && n3(x * 1.9, y * 1.9, 1) > 0.8) P.dark(x, y, .16); }
      else if (p && l > 0) { if (c === "meadow") P.light(x, y, .07); else if (c === "pasture") P.light(x, y, .03);
        else if (c === "built") { P.mix(x, y, PAL.ground[0], 0.16); if (n2(x / 6 + 3, y / 6, 2) > 0.62) P.mix(x, y, PAL.ground[(x + y) & 1], 0.55); } }
    }
    if (RL) for (let y = 1; y < H - 1; y++) for (let x = 1; x < W - 1; x++) {                              // the relief's light from the north-west
      const i = y * W + x; if (LV[i] <= 0) continue; const s = (RL.E[i - W - 1] - RL.E[i + W + 1]) * 3;
      if (s > 0) P.light(x, y, Math.min(0.2, s)); else P.dark(x, y, Math.min(0.32, -s));
      const sn = RL.snowy ? RL.snowy(i, season) : RL.kind[i] === 2 && (season === "winter" || (season !== "summer" && RL.E[i] > 0.93));
      if (sn && cellPar[i] < 0) P.mix(x, y, PAL.snow[0], RL.snowy ? 0.7 : RL.E[i] > 0.93 ? 0.85 : 0.6);
    }
    // terraces from height (a word in the engine; drawn as a step down to the south)
    const face = new Uint8Array(W * H), fh = RL ? 4 : 3;
    if (!small) for (let y = 0; y < H - 1; y++) for (let x = 0; x < W; x++) {
      const l = LV[y * W + x]; if (l <= 1) continue;
      if (lv(x, y + 1) < l && lv(x, y + 1) > 0) { P.put(x, y, snowAt(y * W + x) ? PAL.snow[0] : PAL.rim); for (let k = 1; k <= fh; k++) { if (lv(x, y + k) >= l || y + k >= H) break; P.put(x, y + k, PAL.face[Math.min(3, k - 1 + (x % 3 === 0 ? 1 : 0))]); face[(y + k) * W + x] = 1; } }
      else if (RL && ((lv(x + 1, y) < l && lv(x + 1, y) > 0) || (lv(x - 1, y) < l && lv(x - 1, y) > 0))) P.put(x, y, "#5a9030");
    }
    const trees = [], marks = [];
    const border = (x, y, p) => { for (const [a, b] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) { const j = at(x + a, y + b); if (j < 0 || parcelOf(j) !== p) return true; } return false; };
    const wildNext = (x, y) => { for (const [a, b] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) { const j = at(x + a, y + b); if (j >= 0 && cellPar[j] < 0 && LV[j] > 0) return true; } return false; };
    for (const [pid, pts] of Object.entries(area)) {
      const dp = d.parcels[pid] || {}, res = dp.res || {}, c = cov(pid), P0 = V.static.parcels[pid], N = M.nodes[P0.node], B = BIOMES[N.biome], pR = rng(hstr(pid + "|" + (opts.scale || "")));
      const land = pts.filter(([x, y]) => LV[y * W + x] > 0);
      if (!small && ["meadow", "pasture", "built"].includes(c)) for (const [x, y] of land) if (wildNext(x, y)) P.dark(x, y, .14);
      if (c === "field") paintField(P, V, d, pid, dp, land, sc, small, border, n3, pR, trees, marks, sdays, day);
      else if (c === "pasture" || c === "meadow") {
        const g = res.grass ?? 1, flowers = c === "meadow" && (season === "summer" || season === "spring") && g > 0.5;
        for (const [x, y] of land) { const v = n3(x * 1.3, y * 1.3, 1);
          if (flowers && v > 0.84 && !small) P.put(x, y, PAL.flowers[(hstr(x + "," + y) >>> 3) % 4]);
          else if (v > 0.8 && !small) P.dark(x, y, .12);
          if (g < 0.6 && n3(x / 3 + 5, y / 3) < 0.75 - g) P.mix(x, y, "#b8a868", 0.6 * (0.6 - g) / 0.6 + 0.15); }
        if (!small && dp.dung > 5) for (const [x, y] of land) if (pR() < Math.min(0.02, dp.dung / 4000)) { P.put(x, y, "#6b4a2a"); P.put(x + 1, y, "#5a3a20"); }
      } else if (c === "forest" || c === "scrub") {
        // standing trees in proportion to the wood's stock (S/K); where it was felled, stumps; fallen wood by the dead stock;
        // scrub's bushes by its young growth
        const wood = res.wood ?? (c === "forest" ? 0.8 : 0), was = dp.was === "forest" || c === "forest", step = small ? 2 : 3, nz = small ? 3 : 7;
        for (const [x, y] of land) if (x % step === 0 && y % step === 0) { const tx = x + pR() * (step - 1), ty = y + pR() * (step - 1), v = n2(tx / nz, ty / nz);
          if (v < wood) trees.push([tx, ty, small ? 1 : (pR() < 0.6 ? 2 : 3), B.trees[(pR() * B.trees.length) | 0]]);
          else if (!small && was && v < Math.max(wood, 0.85) && pR() < 0.5) { P.put(tx, ty, "#8a6a42"); P.put(tx + 1, ty, "#6b4423"); P.dark(tx, ty + 1, .25); } }
        if (!small) { const dead = res.dead ?? 0, young = res.young ?? (c === "scrub" ? 0.5 : 0);
          for (const [x, y] of land) { const r = pR();
            if (r < 0.006 * dead) { P.put(x, y, "#7a5a3a"); P.put(x + 1, y, "#6b4a2a"); P.put(x + 2, y, "#7a5a3a"); }
            else if (r < 0.006 * dead + (c === "scrub" ? 0.05 : 0.01) * (0.2 + young) && n2(x / 9 + 3, y / 9, 2) > 0.4) {
              for (const [a, b] of [[0, 0], [1, 0], [-1, 0], [0, -1], [1, -1]]) P.put(x + a, y + b, (a + b) < 0 ? "#6c8a40" : PAL.bush[(a + 1) & 1]); P.dark(x + 2, y, .3); P.dark(x, y + 1, .3); } } }
        else if (c === "scrub") for (const [x, y] of land) if (pR() < 0.1) P.put(x, y, PAL.bush[0]);
        for (const [x, y] of land) if (!small && c === "forest" && n3(x * 1.1, y * 1.1, 1) > 0.8) P.dark(x, y, .15);
      } else if (c === "rock") {
        const st = small ? 3 : 6;
        for (const [x, y] of land) { if (x % st || y % st || pR() > 0.45) continue; const bx = x + (pR() * 3 | 0), by = y + (pR() * 3 | 0);
          if (small) { P.put(bx, by, "#e8e8e0"); P.dark(bx + 1, by, .3); continue; }
          const bw = 3 + (pR() * 3 | 0), bh = 2 + (pR() * 2 | 0);
          for (let yy = 0; yy < bh; yy++) for (let xx = 0; xx < bw; xx++) P.put(bx + xx, by + yy, yy === 0 ? "#e8e8e0" : xx === bw - 1 || yy === bh - 1 ? "#9a9a92" : "#c8c8c0");
          for (let xx = 1; xx <= bw; xx++) P.dark(bx + xx, by + bh, .3); }
        if (res.seam != null) for (const [x, y] of land) if (n2(x / 3, y / 3) > 0.92 - 0.25 * res.seam) P.put(x, y, PAL.copper);
      } else if (c === "water" && !N.river[N.pids.indexOf(pid)]) {
        for (const [x, y] of pts) if (n3(x / 2 + 3, y, 1) > 0.97) P.put(x, y, PAL.water.foam);
      }
      if (dp.clearing && !small) for (const [x, y] of land) if (n2(x / 5 + 11, y / 5) < dp.clearing) { P.mix(x, y, PAL.soil[(x + y) & 1], 0.6); if (pR() < 0.01) { P.put(x, y, "#8a6a42"); P.put(x + 1, y, "#6b4423"); } }
      if (dp.fence && dp.fence.built && !small && dp.fence.level > 0) {                              // a fence or a wall round it, by its level
        const col = dp.fence.kind === "stone" ? PAL.fenceStone : PAL.fenceWood; let k = 0, gate = null;
        for (const [x, y] of pts) if (border(x, y, pid)) { k++; if (!gate) gate = [x, y]; if (dp.fence.level === 1 && k % 4 === 0) continue;
          if (gate && Math.abs(x - gate[0]) + Math.abs(y - gate[1]) < 3) { if (dp.fence.gate === "open") continue; P.put(x, y, "#a0703a"); continue; }
          P.put(x, y, col[(x + y) & 1]); }
      }
      if (snow) for (const [x, y] of land) if (snowAt(y * W + x)) P.mix(x, y, PAL.snow[(x + y) % 3 === 0 ? 1 : 0], n3(x / 4 + 7, y / 4) > 0.3 ? 0.82 : 0.55);
    }
    if (snow) for (let i = 0; i < W * H; i++) if (cellPar[i] < 0 && LV[i] > 0 && snowAt(i)) { const x = i % W, y = (i / W) | 0; P.mix(x, y, PAL.snow[(x + y) % 3 === 0 ? 1 : 0], n3(x / 4 + 7, y / 4) > 0.3 ? 0.8 : 0.5); }
    // the wild country's trees, by each place's character
    const wildStep = small ? 2 : 4;
    for (let gy = 0; gy < H; gy += wildStep) for (let gx = 0; gx < W; gx += wildStep) {
      const x = gx + R() * (wildStep - 1), y = gy + R() * (wildStep - 1), i = at(x, y); if (i < 0 || cellPar[i] >= 0 || LV[i] <= 0 || wet[i]) continue;
      const n = cellNode[i], B = BIOMES[n >= 0 ? M.nodes[nids[n]].biome : "meadow"], z = 26 * Math.max(0.4, Math.min(1, sc * 2)), wild = small || B === BIOMES.woodland ? B.wild : B.wild * 0.6;
      if (RL) { const k = RL.kind[i], fo = RL.F[i];
        if (k === 2 || (k === 3 && R() > 0.08)) continue;
        if (!RL.wood[i] && R() > 0.0015) continue;
        trees.push([x, y, R() < 0.6 ? 2 : 3, RL.tree && RL.tree[i] ? TREES[RL.tree[i]] : LV[i] >= 4 || k === 1 ? "pine" : k === 3 ? "willow" : B.trees[(R() * B.trees.length) | 0] || "oak"]); continue; }
      if (n2(x / z, y / z, 3) < 1 - wild) { if (!small && B === BIOMES.moor && flowering && R() < 0.15) { P.put(x, y, "#8a5a7a"); P.put(x + 1, y, "#9a6a8a"); } continue; }
      trees.push([x, y, small ? 1 : (R() < 0.6 ? 2 : 3), B.trees[(R() * B.trees.length) | 0] || "oak"]);
    }
    return { LV, area, trees, marks, season, snow, lv, at, parcelOf, wet, face };
  }
  // a field: strips along its length; the sown share in the crop's colours by stage, the reaped share as stubble with stooks, the
  // rest dug or lying fallow; ditches or terraces for the works done; hoof-marks where a herd trampled it lately
  function paintField(P, V, d, pid, dp, land, sc, small, border, n3, pR, trees, marks, sdays, day) {
    const ang = fieldAngle(pid), ux = Math.cos(ang), uy = Math.sin(ang), sw = small ? Math.max(1.5, 7 * sc) : 7 + (hstr(pid) >>> 9) % 3;
    let u0 = 1e9, u1 = -1e9; for (const [x, y] of land) { const u = x * ux + y * uy; u0 = Math.min(u0, u); u1 = Math.max(u1, u); }
    const n = Math.max(1, Math.ceil((u1 - u0) / sw)), crop = dp.crop, sownN = crop ? Math.round((crop.sown ?? 1) * n) : 0, reapN = crop ? Math.round((crop.reaped || 0) * sownN) : 0;
    const brokenN = Math.round((dp.broken || 0) * n), stubble = !crop && dp.last_crop && dp.last_crop !== "fallow" && dp.fallow_since != null && day - dp.fallow_since <= sdays;
    const pal = crop ? (STAGE_PAL[crop.stage] || (CROP_PAL[crop.family] || CROP_PAL.grain)[crop.stage] || CROP_PAL.grain.green) : null;
    for (const [x, y] of land) {
      if (border(x, y, pid)) { if (n3(x / 2 + 9, y / 2) < 0.75) P.put(x, y, PAL.hedge); if (!small && pR() < 0.02) trees.push([x, y, 1.5, "oak"]); continue; }
      const u = x * ux + y * uy - u0, s = Math.min(n - 1, Math.floor(u / sw)), v = -x * uy + y * ux;
      if (!small && u - s * sw < 1) { P.put(x, y, PAL.balk); continue; }                                     // the balk between strips
      let c;
      if (crop && s < reapN) { c = PAL.stubble[Math.floor(v / 2) & 1]; if (!small && (Math.floor(v) % 6 === 0) && Math.floor(u - s * sw) === 3) marks.push(["stook", x, y]); }
      else if (crop && s < sownN) { c = pal[Math.floor(v / (small ? 1 : 2)) & 1];
        if (!small && crop.stage === "new" && (x * 7 + y * 3) % 5) c = PAL.soil[Math.floor(v / 2) & 1];
        if (!small && (crop.stage === "high" || crop.stage === "ripe") && Math.floor(v) % 3 === 0 && (x + y) % 2 === 0) c = null, P.put(x, y, pal[0]), P.dark(x, y, .14);
        if (!small && crop.weeds && n3(x * 2.1, y * 2.1, 1) > 0.88) c = "#6a9a3a"; }
      else if (s < (crop ? sownN : 0) + brokenN) c = PAL.soil[Math.floor(v / 2) & 1];
      else if (stubble) c = PAL.stubble[Math.floor(v / 2) & 1];
      else { c = n3(x / 2 + 5, y / 2, 1) > 0.5 ? "#9cb860" : "#a8a070"; }                                     // lying fallow: rough grass
      if (c) P.put(x, y, c);
      const sh = ((hstr(pid + s) % 5) - 2) * 0.03; if (sh > 0) P.dark(x, y, sh); else if (sh < 0) P.light(x, y, -sh);
    }
    if (crop && crop.trampled != null && crop.trampled <= 3 && !small) for (const [x, y] of land) if (pR() < 0.01) { P.dark(x, y, .35); P.dark(x + 1, y + 1, .3); }
    const wk = dp.works;
    if (wk && wk.done > 0 && !small) {                                                                      // ditches on wet ground, terraces on hill ground
      const k = Math.round(wk.done * n);
      for (const [x, y] of land) { const u = x * ux + y * uy - u0, s = Math.floor(u / sw);
        if (s >= k) continue;
        if (wk.ground === "wet" && Math.abs(u - s * sw - sw / 2) < 0.6) P.put(x, y, "#5a8aa0");
        if (wk.ground === "hill" && u - s * sw < 1.2) P.put(x, y, "#b8b0a0"); }
    }
  }
  // the day's weather over everything drawn (environment.weather): a place's own close up; on the region's map, the commonest
  // weather over what is drawn: per pixel, `at(x, y)` gives {kind, rain, wind, frost, storm, fog} (the engine's label, environment.
  // weather, and with the weather scheduler its values, climate.env: rain in mm, wind in m/s); one place close up gives the same
  // everywhere, the region's map a field blended between its places. Rain falls as dense as it is and slanted by the wind, snow
  // drifts, a gale streaks, fog lies, rime on a frost morning, a passing storm darkens. How it is drawn is a presentation choice
  // (ENGINE.md §12)
  const RAINY = new Set(["rain", "heavy rain"]);
  function weatherField(P, W, H, at, R, small, seed = 0) {
    const nz = noise(77 + seed);
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) { const v = at(x, y); if (!v) continue;
      if (v.storm > 0.05) P.mix(x, y, "#2a3048", 0.15 * Math.min(1, Math.max(0, (v.storm - 0.05) / 0.6)));   // a storm passing: a little dim
      if (v.frost > 0 && v.kind !== "snow" && nz(x / 4 + 3, y / 4, 2) > 1 - 0.45 * v.frost) P.mix(x, y, "#e8eef4", 0.28);   // rime, as thick as the frost's share
      if (v.fog > 0) P.mix(x, y, "#e8ecf0", 0.1 * Math.min(1, v.fog));                                // a fog's haze; its banks are drawn
      const wet = v.rain != null ? Math.min(0.16, 0.13 * v.rain / 7) : RAINY.has(v.kind) ? Math.min(0.16, 0.04 + 0.05 * heavyOf(v)) : 0;   // by the mm where given:
      if (wet > 0.005) P.dark(x, y, wet);                                                                  // no edge where the label flips
    }
    const n = (W * H) / 25;                                                                      // candidates, kept by each spot's own density
    for (let k = 0; k < n; k++) { const x = (R() * W) | 0, y = (R() * H) | 0, v = at(x, y); if (!v || !v.kind || v.kind === "clear" || v.kind === "fog") continue;
      const wind = v.wind ?? (v.kind === "gale" ? 18 : 4), dens = v.kind === "snow" ? 25 / 40 * Math.min(1.5, heavyOf(v)) : v.kind === "gale" ? 25 / 90 * Math.max(1, wind / 17) : 25 / 70 * heavyOf(v);
      if (R() > dens) continue;
      const slant = Math.max(0, Math.min(3, Math.round(wind / 6)));                                   // the wind leans the rain
      if (v.kind === "snow") { P.put(x, y, "#ffffff"); if (slant > 1) P.mix(x + 1, y, "#ffffff", 0.4); continue; }
      if (v.kind === "gale") { for (let j = 0; j < 4; j++) P.mix(x + j, y, "#ffffff", 0.35); continue; }
      const L_ = small ? 2 : 3; for (let j = 0; j < L_; j++) P.mix(x - j * (1 + slant) / 2, y + j, "#c8dcf0", 0.4); }
  }
  // ---------------------------------------------------------------------------------------------------- clouds
  // The weather drawn as things in the sky (a presentation choice, ENGINE.md §14): fair-weather puffs on a clear day, grey clouds
  // for rain and snow (darker for heavy rain), towering dark storm clouds with rain shafts and now and then lightning where a storm
  // passes, low flat fog banks in the low ground, torn scraps in a gale. Each cloud casts its shadow on the land below.
  const CLOUD = { fair: ["#f4f6fa", "#ffffff", "#c8d0dc"], rain: ["#a8b0bc", "#c4cad4", "#848c9a"], heavy: ["#8a92a0", "#a4acb8", "#6a7282"],
    storm: ["#4c5266", "#6e7488", "#2e3244"], snow: ["#d4d8e0", "#eef0f4", "#aeb4c0"] };
  function cloud(P, cx, cy, w, h, style, R, alpha) {
    const C = CLOUD[style], n = Math.max(3, Math.ceil(w * 0.75 / (h * 0.55)) + 1 + ((R() * 2) | 0)), puffs = [];   // enough puffs to touch
    for (let k = 0; k < n; k++) puffs.push([cx + (k / (n - 1) - 0.5) * w * 0.75 + (R() - 0.5) * w * 0.1, cy - R() * h * 0.25, h * (0.45 + 0.35 * R()) * (k === 0 || k === n - 1 ? 0.75 : 1)]);
    if (style === "storm") {                                                                        // a storm cloud towers, to a flat anvil
      for (let k = 0; k < 3; k++) puffs.push([cx + (R() - 0.5) * w * 0.25, cy - h * (0.55 + 0.35 * k), h * (0.5 - 0.06 * k)]);
    }
    const lean = (R() - 0.3) * 0.3, anvil = style === "storm" ? [cx + w * lean, cy - h * (1.4 + R() * 0.25), w * (0.5 + R() * 0.2), h * (0.22 + R() * 0.12)] : null;   // a flat top, spread downwind
    const ns = noise((R() * 1e6) | 0), base0 = cy + h * 0.32, base = (x) => base0 + (ns(x / 7, 3) - 0.5) * h * 0.3;   // an underside, not ruled
    for (let y = Math.floor(cy - h * 2.2); y <= base0 + h * 0.2; y++) for (let x = Math.floor(cx - w * 0.8); x <= cx + w * 0.8; x++) {
      if (y > base(x)) continue;
      const jr = 0.88 + 0.24 * ns(x / 5, y / 5);                                                     // ragged edges
      let inside = false, top = 1e9; for (const [px, py, r0] of puffs) { const r = r0 * jr, dd = (x - px) ** 2 + (y - py) ** 2; if (dd <= r * r) { inside = true; top = Math.min(top, py - Math.sqrt(Math.max(0, r * r - (x - px) ** 2))); } }
      if (anvil) { const e = ((x - anvil[0]) / anvil[2]) ** 2 + ((y - anvil[1]) / anvil[3]) ** 2; if (e <= 1) { inside = true; top = Math.min(top, anvil[1] - anvil[3] * Math.sqrt(Math.max(0, 1 - ((x - anvil[0]) / anvil[2]) ** 2))); } }
      if (!inside) continue;
      const c = y >= base(x) - 1 ? C[2] : y - top < 2 ? C[1] : C[0];
      P.mix(x, y, c, alpha);
    }
  }
  function shadow(P, cx, cy, w, h, t) { for (let y = Math.floor(cy - h * 0.4); y <= cy + h * 0.4; y++) for (let x = Math.floor(cx - w * 0.55); x <= cx + w * 0.55; x++)
    if (((x - cx) / (w * 0.55)) ** 2 + ((y - cy) / (h * 0.4)) ** 2 <= 1) P.dark(x, y, t); }
  function fogBank(P, cx, cy, w, h, R, nz) { for (let y = Math.floor(cy - h); y <= cy + h; y++) for (let x = Math.floor(cx - w); x <= cx + w; x++) {
    const e = ((x - cx) / w) ** 2 + ((y - cy) / h) ** 2; if (e > 1) continue; P.mix(x, y, "#eef1f4", (1 - e) * (0.45 + 0.35 * nz(x / 9, y / 5, 2))); } }
  function bolt(P, x, y, L, R) { for (let k = 0; k < L; k++) { P.put(x, y, k % 3 ? "#fff8c0" : "#ffffff"); y++; if (R() < 0.4) x += R() < 0.5 ? -1 : 1; } }
  // the sky over the land: at points on a grid, the weather there (`at`) decides what is in the sky; `opts.avoid(x, y)` keeps
  // clouds off what must stay seen (the region's villages), `opts.low(x, y)` is how low the ground lies (fog settles there)
  function skyOver(P, W, H, at, R, small, opts = {}) {
    const step = small ? 120 : 90, k = small ? 2.2 : 1.9, nz = noise(91 + (opts.seed || 0)), cov = noise(173 + (opts.seed || 0)), items = [];
    for (let gy = -step / 2; gy < H + step; gy += step) for (let gx = -step / 2; gx < W + step; gx += step) {
      const x = gx + (R() - 0.5) * step * 0.8, y = gy + (R() - 0.5) * step * 0.8, v = at(Math.max(0, Math.min(W - 1, x | 0)), Math.max(0, Math.min(H - 1, y | 0))); if (!v) continue;
      if (opts.avoid && opts.avoid(x, y)) continue;
      const storm = v.storm || 0, kind = v.kind || "clear", c = (cov(x / (step * 2.5), y / (step * 2.5), 2) - 0.5) * 1.1;   // clouds come in systems
      const p = (q) => R() < Math.max(0, Math.min(1, q + c));
      if (storm > 0.3) { if (p(0.2)) items.push({ t: "heavy", x, y, w: (36 + R() * 20) * k, h: (12 + R() * 5) * k, shaft: 2 }); }   // between the cells
      else if (kind === "fog" || (v.fog || 0) > 0.5) { for (let b = 0; b < 3; b++) if (p(0.55 * Math.max(0.4, opts.low ? opts.low(x, y) : 1)))
        items.push({ t: "fog", x: x + (R() - 0.5) * step * 0.6, y: y + (R() - 0.5) * step * 0.5, w: (30 + R() * 26) * k, h: (5 + R() * 3) * k }); }
      else if (kind === "heavy rain") { if (p(0.55)) items.push({ t: "heavy", x, y, w: (40 + R() * 22) * k, h: (13 + R() * 5) * k, shaft: 2 }); }
      else if (kind === "rain") { if (p(0.3 + 0.2 * Math.min(1, (v.rain || 3) / 8))) items.push({ t: "rain", x, y, w: (34 + R() * 20) * k, h: (11 + R() * 4) * k, shaft: 1 }); }
      else if (kind === "snow") { if (p(0.4)) items.push({ t: "snow", x, y, w: (34 + R() * 20) * k, h: (11 + R() * 4) * k }); }
      else if (kind === "gale") { for (let b = 0; b < 2; b++) if (p(0.25)) items.push({ t: "rain", x: x + (R() - 0.5) * step * 0.6, y: y + (R() - 0.5) * step * 0.6, w: (14 + R() * 10) * k, h: (5 + R() * 2) * k }); }
      else if (kind === "clear") { if (p(0.18)) items.push({ t: "fair", x, y, w: (16 + R() * 14) * k, h: (7 + R() * 4) * k }); }
    }
    const cell = step * 2.2;                                                                      // storm cells: a few to a storm
    for (let gy = -cell / 2; gy < H + cell; gy += cell) for (let gx = -cell / 2; gx < W + cell; gx += cell) {
      const x = gx + (R() - 0.5) * cell * 0.7, y = gy + (R() - 0.5) * cell * 0.7, v = at(Math.max(0, Math.min(W - 1, x | 0)), Math.max(0, Math.min(H - 1, y | 0)));
      if (!v || (v.storm || 0) < 0.3 || (opts.avoid && opts.avoid(x, y)) || R() > Math.min(0.85, 0.15 + v.storm * 0.6)) continue;
      items.push({ t: "storm", x, y, w: (46 + R() * 30) * k, h: (17 + R() * 9) * k, bolt: R() < 0.5 }); }
    for (const c of items) if (c.t !== "fog") shadow(P, c.x + c.w * 0.25, c.y + c.h * 1.4, c.w, c.h, c.t === "storm" ? 0.22 : c.t === "fair" ? 0.1 : 0.14);   // shadows first
    for (const c of items) if (c.t === "fog") fogBank(P, c.x, c.y, c.w, c.h, R, nz);
    items.sort((a, b) => a.y - b.y);
    for (const c of items) { if (c.t === "fog") continue;
      if (c.shaft || c.t === "storm") { const n = (c.t === "storm" ? 0.9 : 0.35 * c.shaft) * c.w; for (let j = 0; j < n; j++) {     // rain falling from it
        const sx = c.x + (R() - 0.5) * c.w * 0.8, sy = c.y + c.h * 0.4 + R() * c.h * 1.8; for (let q = 0; q < 3; q++) P.mix(sx - q * 0.5, sy + q, "#c8dcf0", 0.5); } }
      if (c.bolt) bolt(P, (c.x + (R() - 0.5) * c.w * 0.4) | 0, (c.y + c.h * 0.35) | 0, (c.h * 1.4) | 0, R);
      cloud(P, c.x, c.y, c.w, c.h, c.t, R, opts.alpha ?? 0.9); }
  }
  // how much falls: the rain's mm (12 a heavy day) where the scheduler gives it, else the label's
  const heavyOf = (v) => v.rain != null ? Math.max(0.15, Math.min(1.8, v.rain / 7)) : v.kind === "heavy rain" ? 1.6 : 1;
  // one place's weather everywhere (close up)
  function weatherOver(P, W, H, kind, R, small, o = {}) {
    const v = { kind, rain: o.rain, wind: o.wind, frost: o.frost ? 1 : 0, storm: o.storm || 0, fog: kind === "fog" ? 1 : 0 };
    weatherField(P, W, H, o.mask ? (x, y) => (o.mask(x, y) ? v : null) : () => v, R, small, o.seed || 0);
  }

  function drawTrees(P, trees, ctx, occ, W, H, R) {
    trees.sort((a, b) => a[1] - b[1]);
    for (const [x, y, r, kind] of trees) {
      const i = ctx.at(x, y); if (i < 0 || occ[i] || ctx.LV[i] <= 0) continue;
      let ok = true; for (let k = -1; k <= 1; k++) { const j = ctx.at(x + k, y + 2); if (j >= 0 && (occ[j] >= 3 || ctx.LV[j] <= 0)) ok = false; }
      if (ok) tree(P, x, y, r, R, kind, ctx.season);
    }
  }
  Object.assign(X, { snowLies, paintLand, paintField, weatherField, weatherOver, skyOver, cloud, drawTrees });
})(C2X);
