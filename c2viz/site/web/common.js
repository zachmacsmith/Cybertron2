// Shared data and small drawings for the Cybertron 2 design mockups. Every number here comes from the runs' own data
// (data/*.json, saved from the c2viz server): places and roads from each run's head, people and seasons from its days.
export const RUNS = [
  { key: "wb2_wenbridge", title: "Wenbridge", days: 30, people: 12, places: 3,
    models: ["Opus 5.5", "Sonnet 5.5", "Haiku 5.5"],
    line: "Twelve people in five households across a village, a wood and a hill. Three are alive at the end." },
  { key: "f1_frontier", title: "Frontier camps", days: 38, people: 10, places: 12,
    models: ["Opus 5.5", "Sonnet 5.5"],
    line: "Ten people spread over twelve places joined by a ring of one-day roads, most of them wild." },
  { key: "c3_combe_rich", title: "Combe, rich", days: 80, people: 3, places: 4,
    models: ["Opus 5.5", "Sonnet 5.5"],
    line: "Three people, four places and eighty days: the longest run, and nobody dies." },
  { key: "d1_duo", title: "Duo", days: 10, people: 14, places: 2,
    models: ["Opus 4.5", "Opus 4.7", "Sonnet 4.6", "Haiku 4.5"],
    line: "Two villages two days apart, four households of fourteen people." },
];

export async function load() {
  const j = (p) => fetch(p).then((r) => r.json());
  // all at once: the runs' days and every head in parallel
  const [days, ...heads] = await Promise.all([j("data/days.json"), ...RUNS.map((r) => j(`data/${r.key}.head.json`))]);
  RUNS.forEach((r, i) => { r.head = heads[i]; r.series = days[r.key]; });
  return RUNS;
}

const NS = "http://www.w3.org/2000/svg";
const el = (tag, attrs = {}, parent) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); parent && parent.append(e); return e; };

// the places and roads of a run as a graph, laid out where c2viz puts them on the world map
export function graph(svg, run, { day = 0, style = "ink", labels = true, pad = 70 } = {}) {
  const st = run.head.static, pos = st.layout.world, at = (run.series[day] || {}).at || {};
  const xs = Object.values(pos).map((p) => p[0]), ys = Object.values(pos).map((p) => p[1]);
  const x0 = Math.min(...xs) - pad, y0 = Math.min(...ys) - pad, w = Math.max(...xs) - x0 + pad, h = Math.max(...ys) - y0 + pad;
  svg.setAttribute("viewBox", `${x0} ${y0} ${w} ${Math.max(h, w * 0.35)}`);
  svg.innerHTML = "";
  const S = w / 400;                                             // one stroke width whatever the run's size
  for (const r of Object.values(st.roads)) {
    const [a, b] = [pos[r.a], pos[r.b]];
    el("line", { x1: a[0], y1: a[1], x2: b[0], y2: b[1], class: "edge", "stroke-width": S * (r.days > 1 ? 1.4 : 1),
      "stroke-dasharray": r.days > 1 ? `${S * 4} ${S * 3}` : "" }, svg);
    if (labels && style !== "pixel") el("text", { x: (a[0] + b[0]) / 2, y: (a[1] + b[1]) / 2 - S * 4, class: "elab", "font-size": S * 9, "text-anchor": "middle" }, svg).textContent = `${r.days}d`;
  }
  for (const [id, p] of Object.entries(pos)) {
    const n = at[id] || 0, settled = n > 0, name = st.nodes[id].name;
    if (style === "pixel") {
      const u = S * 2.4, g = el("g", { class: "pnode" + (settled ? " on" : ""), transform: `translate(${p[0]},${p[1]})` }, svg);
      if (settled) { // a 7 x 6 house: roof, walls, door
        const H = ["...R...", "..RRR..", ".RRRRR.", ".WWWWW.", ".WWDWW.", ".WWDWW."];
        H.forEach((row, y) => [...row].forEach((c, x) => { if (c !== ".") el("rect", { x: (x - 3.5) * u, y: (y - 5) * u, width: u, height: u, class: "px-" + c }, g); }));
      } else el("rect", { x: -u, y: -u, width: u * 2, height: u * 2, class: "px-W" }, g);
      if (labels) el("text", { y: u * 4.2, class: "nlab", "font-size": S * 10, "text-anchor": "middle" }, g).textContent = name + (n ? ` · ${n}` : "");
    } else {
      const rad = S * (3 + Math.sqrt(n) * 3.2);
      el("circle", { cx: p[0], cy: p[1], r: rad, class: "node" + (settled ? " on" : "") }, svg);
      if (labels) el("text", { x: p[0], y: p[1] - rad - S * 4, class: "nlab", "font-size": S * 10, "text-anchor": "middle" }, svg).textContent = name;
    }
  }
  return svg;
}

// people alive, day by day, as a thin line (or a stepped one), with the seasons as a band beneath
const SEASON = { spring: "var(--spring)", summer: "var(--summer)", autumn: "var(--autumn)", winter: "var(--winter)" };
export function chart(svg, run, { w = 600, h = 120, steps = false, band = 8, axis = true } = {}) {
  const s = run.series, n = s.length, max = Math.max(...s.map((d) => d.alive)), L = axis ? 26 : 2, B = band + (axis ? 16 : 4);
  svg.setAttribute("viewBox", `0 0 ${w} ${h}`); svg.innerHTML = "";
  const X = (i) => L + (w - L - 4) * i / Math.max(1, n - 1), Y = (v) => 6 + (h - B - 10) * (1 - v / max);
  if (axis) for (const v of [0, max]) {
    el("line", { x1: L, x2: w - 4, y1: Y(v), y2: Y(v), class: "grid" }, svg);
    el("text", { x: L - 6, y: Y(v) + 4, class: "tick", "text-anchor": "end" }, svg).textContent = v;
  }
  let d = "";
  s.forEach((p, i) => { d += i ? (steps ? `H${X(i)}V${Y(p.alive)}` : `L${X(i)},${Y(p.alive)}`) : `M${X(0)},${Y(p.alive)}`; });
  el("path", { d, class: "line" }, svg);
  const bw = (w - L - 4) / n;
  s.forEach((p, i) => el("rect", { x: L + bw * i, y: h - B + 4, width: bw + 0.3, height: band, fill: SEASON[p.season] || "#ccc" }, svg));
  if (axis) { el("text", { x: L, y: h - 1, class: "tick" }, svg).textContent = "day 1"; el("text", { x: w - 4, y: h - 1, class: "tick", "text-anchor": "end" }, svg).textContent = `day ${n}`; }
  return svg;
}

// one cell a day: the season's colour, fading as people die; a death is a mark above the cell
export function ledger(host, run) {
  const s = run.series, max = s[0].alive;
  host.innerHTML = s.map((p, i) => {
    const died = i > 0 && p.alive < s[i - 1].alive;
    return `<i style="background:${SEASON[p.season]};opacity:${0.35 + 0.65 * p.alive / max}" class="${died ? "death" : ""}" title="Day ${i + 1}: ${p.alive} alive, ${p.season}"></i>`;
  }).join("");
}

// the graph of places drawn over the world map, each node where the renderer put the place (img/worldpos.json)
let WP = null;
export async function overlay(svg, run, { labels = true } = {}) {
  WP = WP || fetch("img/worldpos.json").then((r) => r.json());                   // one fetch, shared by every map
  const P = (await WP)[run.key], pos = Object.fromEntries(P.nodes.map((n) => [n.id, [n.cx, n.cy]])), at = (run.series[P.day] || {}).at || {};
  svg.setAttribute("viewBox", `0 0 ${P.w} ${P.h}`); svg.setAttribute("preserveAspectRatio", "xMidYMid slice"); svg.innerHTML = "";
  const S = P.w / 500;
  for (const r of Object.values(run.head.static.roads)) {
    const [a, b] = [pos[r.a], pos[r.b]]; if (!a || !b) continue;
    for (const [cls, wd] of [["case", 4], ["edge", 1.6]])
      el("line", { x1: a[0], y1: a[1], x2: b[0], y2: b[1], class: cls, "stroke-width": S * wd, "stroke-dasharray": r.days > 1 && cls === "edge" ? `${S * 5} ${S * 4}` : "" }, svg);
    if (labels) el("text", { x: (a[0] + b[0]) / 2, y: (a[1] + b[1]) / 2 - S * 6, class: "elab", "font-size": S * 11, "text-anchor": "middle" }, svg).textContent = `${r.days} day${r.days > 1 ? "s" : ""}`;
  }
  for (const [id, p] of Object.entries(pos)) {
    const n = at[id] || 0, rad = S * (4 + Math.sqrt(n) * 4);
    el("circle", { cx: p[0], cy: p[1], r: rad, class: "node" + (n ? " on" : "") }, svg);
    if (labels) el("text", { x: p[0], y: p[1] - rad - S * 5, class: "nlab", "font-size": S * 13, "text-anchor": "middle" }, svg).textContent = run.head.static.nodes[id].name + (n ? ` · ${n}` : "");
  }
}

export const fmt = (r) => `${r.places} place${r.places === 1 ? "" : "s"} · ${r.people} people · ${r.days} days`;
