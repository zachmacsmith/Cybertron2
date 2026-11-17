"""The home page's featured maps, drawn once and saved with the site: each run's world on one day, by the c2viz renderer in a
headless browser, as web/img/<run>-world.webp (at most 640 pixels wide: a card shows it at about 260), with where it put each place (and the roads) in web/img/worldpos.json.

    python3 c2viz/site/card_images.py pw1_opus_sonnet_r1 wild_region_s7 wb2_wenbridge water_lake_r2 [--day 4]

The runs come from their viewer files on the Hub (c2viz/site/viewer_publish.py). Drawing a world the first time takes the
renderer seconds, so the page shows these saved pictures rather than drawing them for each visitor. Needs Playwright (Chromium).
"""
from __future__ import annotations

import argparse
import base64
import json
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from static import bundle  # noqa: E402  (the renderer, as the site serves it)

HF = "https://huggingface.co/datasets/zachmacsmith/cybertron2-runs/resolve/main"
IMG = HERE / "web" / "img"


def get(url: str):
    with urllib.request.urlopen(url) as r:
        return json.load(r)


def save(png: bytes, path: Path, width: int) -> None:
    """A drawn world as WebP (about a quarter of the PNG), no wider than `width`; worldpos.json keeps the drawing's own pixels."""
    import io
    from PIL import Image
    im = Image.open(io.BytesIO(png)).convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(path, "WEBP", quality=88, method=6)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("runs", nargs="+")
    ap.add_argument("--day", type=int, default=4, help="the day drawn, from 0 (default 4: day 5, the people settled in)")
    ap.add_argument("--base", default=HF, help="where the viewer files are")
    ap.add_argument("--width", type=int, default=640, help="the saved picture's largest width (the hero's: 1200)")
    a = ap.parse_args(argv)
    from playwright.sync_api import sync_playwright
    pos_file = IMG / "worldpos.json"
    pos = json.loads(pos_file.read_text()) if pos_file.exists() else {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content("<canvas id=cv></canvas>")
        page.add_script_tag(content=bundle())
        for key in a.runs:
            base = f"{a.base}/runs/{key}/viewer"
            index = get(f"{base}/index.json")
            day = min(a.day, index["days"] - 1)
            with ThreadPoolExecutor(8) as ex:                               # the days up to it: a world may read its past
                head, *days = ex.map(get, [f"{base}/head.json"] + [f"{base}/day/{d}.json" for d in range(day + 1)])
            out = page.evaluate("""([head, days, day]) => {
                const V = { ...head, days }, cv = document.getElementById("cv"), r = C2Pixel.world(cv, V, day);
                return { png: cv.toDataURL("image/png"), w: cv.width, h: cv.height,
                         nodes: r.hotspots.filter((h) => h.kind === "node").map((h) => ({ id: h.id, cx: h.cx, cy: h.cy, label: h.label, pop: h.pop || 0 })) };
            }""", [head, days, day])
            save(base64.b64decode(out["png"].split(",", 1)[1]), IMG / f"{key}-world.webp", a.width)
            pos[key] = {"w": out["w"], "h": out["h"], "day": day, "nodes": out["nodes"],
                        "roads": [{"a": r["a"], "b": r["b"], "days": r["days"]} for r in (head["static"].get("roads") or {}).values()]}
            print(f"  {key}: day {day + 1}, {out['w']}x{out['h']}, {len(out['nodes'])} places", flush=True)
        browser.close()
    pos_file.write_text(json.dumps(pos, separators=(",", ":")))


if __name__ == "__main__":
    main()
