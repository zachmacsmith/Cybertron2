// The page's side of render-worker.js: load(key, urls) and draw(key, kind, node, day, t) as promises, and paint(canvas, frame)
// to put a drawn frame on a canvas. Up to four workers, and each run always drawn by the same one (which keeps what it laid out
// for it): a run being made ready in the background, which takes seconds, never holds up the run that is playing.
const N = Math.max(1, Math.min(4, navigator.hardwareConcurrency || 2));
const workers = Array.from({ length: N }, () => new Worker("render-worker.js"));
let next = 0;
const waiting = new Map();
for (const w of workers) w.onmessage = ({ data }) => { const p = waiting.get(data.id); waiting.delete(data.id); data.error ? p.ko(new Error(data.error)) : p.ok(data); };
const ask = (w, m) => new Promise((ok, ko) => { const id = ++next; waiting.set(id, { ok, ko }); w.postMessage({ ...m, id }); });
const owners = new Map(); let turn = 0;                      // runs handed out to the workers in turn, and kept with them
const owner = (key) => { if (!owners.has(key)) owners.set(key, workers[turn++ % N]); return owners.get(key); };

const loading = new Map();
export const load = (key, urls) => { if (!loading.has(key)) loading.set(key, ask(owner(key), { op: "load", key, urls })); return loading.get(key); };
export const draw = (key, kind, node, day, t) => ask(owner(key), { op: "draw", key, kind, node, day, t });
export function paint(cv, f) {
  if (cv.width !== f.width || cv.height !== f.height) { cv.width = f.width; cv.height = f.height; }
  cv.getContext("2d").drawImage(f.bitmap, 0, 0); f.bitmap.close();
}
