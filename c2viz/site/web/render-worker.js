// The renderer (c2pixel.js) on its own thread, so the page stays responsive while a world is drawn: the first picture of a
// run takes seconds while its places are laid out. Messages: {id, op: "load", key, urls} fetches a run (one viz.json, or a
// head and its days) and keeps it; {id, op: "draw", key, kind: "world" | "node" | "nodeAt", node, day, t} draws it and
// answers {id, bitmap, width, height, hotspots, phase}.
importScripts("c2pixel.js");
const runs = {};
const json = (u) => fetch(u).then((r) => { if (!r.ok) throw new Error(`${u}: ${r.status}`); return r.json(); });
self.onmessage = async ({ data: m }) => {
  try {
    if (m.op === "load") {
      if (!runs[m.key]) runs[m.key] = (async () => {
        if (m.urls.length === 1) return json(m.urls[0]);                 // a whole viz.json
        const [head, ...days] = await Promise.all(m.urls.map(json));   // a head and its days
        return { ...head, days };
      })();
      await runs[m.key];
      return self.postMessage({ id: m.id });
    }
    const V = await runs[m.key], cv = new OffscreenCanvas(1, 1);
    const out = m.kind === "world" ? C2Pixel.world(cv, V, m.day) : m.kind === "nodeAt" ? C2Pixel.nodeAt(cv, V, m.node, m.day, m.t) : C2Pixel.node(cv, V, m.node, m.day);
    const bitmap = cv.transferToImageBitmap();
    self.postMessage({ id: m.id, bitmap, width: out.width, height: out.height, phase: out.phase,
      hotspots: out.hotspots.map(({ kind, id, label, cx, cy, pop }) => ({ kind, id, label, cx, cy, pop })) }, [bitmap]);
  } catch (e) {
    self.postMessage({ id: m.id, error: String(e && e.message || e) });
  }
};
