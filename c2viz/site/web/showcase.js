// The home page's showcase: places from the runs, drawn live by the c2viz renderer (c2pixel.js, on its own thread: render.js)
// from each run's own days.
//   "places": one place from a run, three of its days played through (people walking to their work), then a fade to another run
//   "days":   one run's main place day after day to the end, the chart and its band of days building; then a swipe to the next run
//   "tiles":  the same, but four of the run's places side by side when it has four lived in (else one), moving together,
//             and a mark for how many more it has
const SEASON = { spring: "var(--spring)", summer: "var(--summer)", autumn: "var(--autumn)", winter: "var(--winter)" };
const TITLES = { wb2_wenbridge: "Wenbridge", d1_duo: "Duo", f1_frontier: "Frontier camps", c1_combe: "Combe" };
const MODELS = { wb2_wenbridge: "Opus 5.5 · Sonnet 5.5 · Haiku 5.5", d1_duo: "Opus 4.5 · Opus 4.7 · Sonnet 4.6 · Haiku 4.5",
  f1_frontier: "Opus 5.5 · Sonnet 5.5", c1_combe: "Opus 5.5 · Sonnet 5.5" };
import * as R from "./render.js";                         // the drawing is done on its own thread, so the page never stalls
const cache = {};
function run(key) {
  return cache[key] = cache[key] || Promise.all([R.load(key, [`data/full/${key}.json`]), fetch(`data/full/${key}.json`).then((r) => r.json())]).then(([, V]) => {
    V.key = key;
    V.series = V.days.map((d) => { const at = {}; let alive = 0;
      for (const p of Object.values(d.people)) if (p.alive) { alive++; if (p.at) at[p.at] = (at[p.at] || 0) + 1; }
      return { alive, at, season: (d.calendar || {}).season }; });
    return V;
  });
}
// the places with the most people over days d0..d1, most first
const busiest = (V, d0, d1) => { const tot = {}; for (let d = d0; d <= d1; d++) for (const k in V.series[d].at) tot[k] = (tot[k] || 0) + V.series[d].at[k];
  return Object.entries(tot).sort((a, b) => b[1] - a[1]).map(([k]) => k); };

const NS = "http://www.w3.org/2000/svg";
const el = (t, a, p) => { const e = document.createElementNS(NS, t); for (const k in a) e.setAttribute(k, a[k]); p && p.append(e); return e; };
// people alive by day, drawn up to day `upto` on an axis fixed to the whole run
function chart(svg, V, upto) {
  const s = V.series, n = s.length, max = Math.max(...s.map((d) => d.alive)), w = 420, h = 140, L = 24, B = 26;
  svg.setAttribute("viewBox", `0 0 ${w} ${h}`); svg.innerHTML = "";
  const X = (i) => L + (w - L - 6) * i / Math.max(1, n - 1), Y = (v) => 8 + (h - B - 14) * (1 - v / max);
  for (const v of [0, max]) { el("line", { x1: L, x2: w - 6, y1: Y(v), y2: Y(v), class: "grid" }, svg); el("text", { x: L - 6, y: Y(v) + 4, class: "tick", "text-anchor": "end" }, svg).textContent = v; }
  let d = `M${X(0)},${Y(s[0].alive)}`; for (let i = 1; i <= upto; i++) d += `H${X(i)}V${Y(s[i].alive)}`;
  el("path", { d, class: "line" }, svg);
  el("line", { x1: X(upto), x2: X(upto), y1: 6, y2: h - B + 2, class: "now" }, svg);
  el("circle", { cx: X(upto), cy: Y(s[upto].alive), r: 3.5, class: "dot" }, svg);
  // the days so far: each its season's colour, fainter as people die, with a red mark over a day someone died
  const bw = (w - L - 6) / n, s0 = s[0].alive;
  s.forEach((p, i) => {
    if (i > upto) return el("rect", { x: L + bw * i, y: h - B + 6, width: bw + 0.3, height: 7, fill: "#eee" }, svg);
    el("rect", { x: L + bw * i, y: h - B + 6, width: bw + 0.3, height: 7, fill: SEASON[p.season], opacity: 0.35 + 0.65 * p.alive / s0 }, svg);
    if (i && p.alive < s[i - 1].alive) el("rect", { x: L + bw * i + bw / 2 - 2, y: h - B + 0.5, width: 4, height: 4, class: "dot" }, svg);
  });
  el("text", { x: L, y: h - 2, class: "tick" }, svg).textContent = "day 1"; el("text", { x: w - 6, y: h - 2, class: "tick", "text-anchor": "end" }, svg).textContent = `day ${n}`;
}
const people = (hot) => hot.filter((h) => h.kind === "person").map((h) => { const [n, ...a] = h.label.split(" · "); return a.length ? `${n} <span>· ${a.join(" · ")}</span>` : n; });
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

export async function showcase(root, mode, opts = {}) {
  // until the first run is drawn: hopping pixels in the stage, and placeholder lines where its numbers will be
  root.innerHTML = `<div class="sc-stage"><div class="sc-loading"><div class="px3"><i></i><i></i><i></i></div><span>Loading a run</span></div></div>
    <div class="sc-panel"><div class="sc-in">
      <div class="k sc-where">Loading…</div><h3 class="sc-title"><span class="sk" style="width:60%"></span></h3><div class="meta sc-models"><span class="sk" style="width:40%"></span></div>
      <div class="sc-nums"><div><b><span class="sk" style="width:1.4em"></span></b><span>here</span></div><div><b><span class="sk" style="width:1.4em"></span></b><span>alive</span></div><div><b><span class="sk" style="width:1.4em"></span></b><span>places</span></div></div>
      <svg class="sc-chart"></svg>
      <div class="sc-who"></div><a class="sc-open" href="#">Open this run →</a></div></div>`;
  const stage = root.querySelector(".sc-stage"), Q = (s) => root.querySelector(s);
  // a scene is a layer of up to four tiles; a new one fades (or swipes) in over the last
  const layer = (V, nodes, extra, how) => {
    const L = document.createElement("div"); L.className = `sc-layer n${nodes.length}`;
    L.innerHTML = nodes.map((n) => `<figure><canvas></canvas><figcaption>${V.static.nodes[n].name}<b></b></figcaption></figure>`).join("")
      + (extra > 0 ? `<span class="sc-more">+${extra} more place${extra > 1 ? "s" : ""}</span>` : "") + `<span class="sc-clock"></span>`;
    stage.querySelector(".sc-loading")?.remove();
    stage.append(L); L.classList.add(how);
    void L.offsetWidth; setTimeout(() => { L.classList.add("in"); for (const o of stage.querySelectorAll(".sc-layer:not(.out):not(.away):not(.away-r)")) if (o !== L) { o.classList.add("in"); o.classList.add(how === "swipe" ? "away" : how === "back" ? "away-r" : "out"); setTimeout(() => o.remove(), 900); } }, 20);
    return { L, canvases: [...L.querySelectorAll("canvas")], counts: [...L.querySelectorAll("figcaption b")], clock: L.querySelector(".sc-clock") };
  };
  const panel = (V, nodes, d, hot, phase) => {
    const s = V.series[d], st = V.static, here = nodes.reduce((a, n) => a + (s.at[n] || 0), 0);
    Q(".sc-where").textContent = `${nodes.length === 1 ? st.nodes[nodes[0]].name + " · " : ""}day ${d + 1} of ${V.days.length} · ${s.season}${phase ? " · " + phase : ""}`;
    Q(".sc-title").textContent = TITLES[V.key]; Q(".sc-models").textContent = MODELS[V.key];
    Q(".sc-open").href = `run.html?id=${encodeURIComponent("hub:" + V.key)}&day=${d + 1}`;     // the explorer, at this day
    Q(".sc-nums").innerHTML = `<div><b>${here}</b><span>${nodes.length === 1 ? "here" : "in these places"}</span></div><div><b>${s.alive}</b><span>alive, of ${V.series[0].alive}</span></div>
      <div><b>${Object.keys(st.nodes).length}</b><span>places</span></div>`;
    chart(Q(".sc-chart"), V, d);
    const w = hot.names || people(hot); Q(".sc-who").innerHTML = w.length ? `<div class="k">Here now</div><p>${w.slice(0, 5).join(", ")}${w.length > 5 ? ` and ${w.length - 5} more` : ""}</p>` : "";
  };

  if (mode === "places") {
    // [run, first day, place (the one-place version)]: picked where people are at work
    const SCENES = [["wb2_wenbridge", 3, "wenbridge"], ["f1_frontier", 4, "gormhold"], ["d1_duo", 2, "wynford"], ["c1_combe", 12, "combe"], ["wb2_wenbridge", 20, "wenbridge"]];
    const DAY_MS = 7000, DAYS = 3;
    for (let i = 0; ; i = (i + 1) % SCENES.length) {
      const [key, d0, one] = SCENES[i], V = await run(key), d1 = Math.min(V.days.length - 1, d0 + DAYS - 1);
      const nodes = [one];
      await Promise.all(nodes.map((n) => R.draw(key, "nodeAt", n, d0, -0.1)));     // the slow first picture, before the fade
      const S = layer(V, nodes, Object.keys(V.static.nodes).length - nodes.length, "fade");
      for (let d = d0; d <= d1; d++) {
        const t0 = performance.now();
        for (let t = -0.1; t <= 1.15; t = -0.1 + 1.25 * (performance.now() - t0) / DAY_MS) {
          const fr = await Promise.all(nodes.map((n) => R.draw(key, "nodeAt", n, d, t)));
          let hot = []; const phase = fr[0].phase;
          fr.forEach((f, k) => { R.paint(S.canvases[k], f); hot = hot.concat(f.hotspots); S.counts[k].textContent = V.series[d].at[nodes[k]] ? ` · ${V.series[d].at[nodes[k]]}` : ""; });
          panel(V, nodes, d, hot, phase); S.clock.textContent = `day ${d + 1} · ${phase}`;
          await wait(60);
        }
      }
    }
  }

  // "days" and "tiles": a run day after day, the chart building; at the end, a swipe to the next run. "days" shows the run's
  // busiest place, "tiles" four of its busiest (or one), moving together, with a mark for how many more it has. The arrows
  // (opts.prev, opts.next) slide to the run before or after, which starts again from its first day.
  // a run's first picture takes the renderer seconds (it lays out the whole world first), so the run after the one playing
  // is made ready while it plays, and the showcase opens on a quick one
  const ORDER = ["wb2_wenbridge", "f1_frontier", "d1_duo", "c1_combe"], DAY_MS = 900;
  const ready = {};
  const prepare = (key) => ready[key] = ready[key] || run(key).then(async (V) => {
    const busy = busiest(V, 0, V.days.length - 1), nodes = busy.slice(0, mode === "tiles" && busy.length >= 4 ? 4 : 1);   // four tiles or one
    return { V, nodes, first: await Promise.all(nodes.map((n) => R.draw(key, "node", n, 0))) };
  });
  let at = 0, turn = 0;                                     // a new turn stops the run that was playing
  const play = async (i, how) => {
    const me = ++turn, live = () => me === turn;
    const P = await prepare(ORDER[i]); if (!live()) return;
    const { V, nodes } = P; let fr = P.first; delete ready[ORDER[i]];          // its first picture is used once; drawn again next time
    prepare(ORDER[(i + 1) % ORDER.length]); prepare(ORDER[(i - 1 + ORDER.length) % ORDER.length]);   // the runs either side, for the arrows
    const S = layer(V, nodes, mode === "tiles" ? Object.keys(V.static.nodes).length - nodes.length : 0, how);
    for (let d = 0; d < V.days.length && live(); d++) {
      const t0 = performance.now();
      if (d) fr = await Promise.all(nodes.map((n) => R.draw(V.key, "node", n, d)));
      if (!live()) return;
      fr.forEach((f, k) => { R.paint(S.canvases[k], f); S.counts[k].textContent = V.series[d].at[nodes[k]] ? ` · ${V.series[d].at[nodes[k]]}` : ""; });
      // just the names of those at these places that day, so the panel keeps still from day to day
      const names = Object.entries(V.days[d].people).filter(([, p]) => p.alive && nodes.includes(p.at)).map(([n]) => n);
      panel(V, nodes, d, { names }, ""); S.clock.textContent = `day ${d + 1}`;
      await wait(Math.max(0, (d ? DAY_MS : DAY_MS + 600) - (performance.now() - t0)));   // the drawing counts toward the day's time
    }
    if (!live()) return;
    await wait(2200);
    if (live()) { at = (i + 1) % ORDER.length; play(at, "swipe"); }
  };
  const go = (step) => { at = (at + step + ORDER.length) % ORDER.length; play(at, step > 0 ? "swipe" : "back"); };
  opts.prev && opts.prev.addEventListener("click", () => go(-1));
  opts.next && opts.next.addEventListener("click", () => go(1));
  play(0, "fade");
}
