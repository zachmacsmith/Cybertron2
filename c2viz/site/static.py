"""The Cybertron 2 site as static files, for a host with no server (Netlify).

    python3 c2viz/site/static.py OUT                       # the site, reading the runs' viewer files from the Hub
    python3 c2viz/site/static.py OUT --data VIEWER_BUILD   # ... or from a local build of them (viewer_publish.py --local), copied in

The pages are the server's own (web/ and run.html) plus the renderer (c2pixel.js). Without a server behind them, the runs page and
the run explorer read the viewer files published beside each run's journal (c2viz/site/viewer_publish.py). Standard library only,
so a host's build step needs nothing installed.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
WEB, JS = HERE / "web", HERE.parent / "js"


def bundle() -> str:
    """c2pixel.js, as the server makes it (c2viz.build.bundle), without importing the engine's model."""
    names = [n.strip() for n in (JS / "MANIFEST").read_text().split() if n.strip()]
    return "var C2X = {};\n" + "\n".join((JS / f"{n}.js").read_text() for n in names)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("out", nargs="?", default="_site")
    ap.add_argument("--data", help="a local build of the viewer files to serve with the site instead of the Hub's")
    a = ap.parse_args(argv)
    out = Path(a.out)
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(WEB, out, ignore=shutil.ignore_patterns(".DS_Store"))
    shutil.copy(HERE / "run.html", out / "run.html")
    (out / "c2pixel.js").write_text(bundle())
    if a.data:                                                              # served from the site itself, under hub/
        shutil.copytree(a.data, out / "hub")
        for page in ("runs.html", "run.html"):
            f = out / page
            f.write_text(f.read_text().replace("<head>", '<head>\n<script>self.C2_DATA = "hub";</script>', 1))
    print(f"static site in {out}")


if __name__ == "__main__":
    main()
