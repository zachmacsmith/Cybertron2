"""Build the website's files for published runs and put them on the Hub, beside each run's journal.

    python -m c2viz.site.viewer_publish                 # every published run whose viewer files are missing or out of date
    python -m c2viz.site.viewer_publish --only p1_brookend --force
    python -m c2viz.site.viewer_publish --no-upload --out /tmp/viewer   # build only, to look at
    python -m c2viz.site.viewer_publish --local         # build from runs already on this machine, no network ...
    python -m c2viz.site.viewer_publish --upload-only   # ... and upload that build later

The journal (run.db, published as `<folder>/<run>/journal/`) is the record of a run: every model call and change, enough to
replay, fork or continue it. The website needs each day as it was (who was where, every parcel and building), which only replaying
the engine gives; so that is done once here, from the journal, by the same code the site's server uses (c2viz.model.RunModel), and
saved as plain JSON the browser reads directly:

    <folder>/<run>/viewer/index.json     what was built, from which revision of the journal, by which c2viz code (code_key)
    <folder>/<run>/viewer/head.json      the world: places, parcels, roads, every building it ever had
    <folder>/<run>/viewer/day/<d>.json   day d (from 0), with `words`: what people said that day (each reply's say and tell)
    <folder>/<run>/viewer/thumb.jpg      the runs page's small map of day 1, when one has been drawn (by the site, in a browser)
    viewer/catalog.json                  every run with viewer files: its summary and its days in brief (the runs page's list)

These files are derived: when c2viz's code changes (a new code_key), run this again and they are rebuilt from the journals, with
no run played again. Nothing here reads or changes the engine.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from pathlib import Path

from c2viz.site.server import Builder, Catalog, code_key, day_talk


def dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, separators=(",", ":"), default=str))


def published_index(repo: str, folder: str, name: str, sha: str) -> dict | None:
    """The viewer files' index as published at this revision, if there is one."""
    from huggingface_hub import hf_hub_download
    try:
        return json.loads(Path(hf_hub_download(repo_id=repo, filename=f"{folder}/{name}/viewer/index.json", repo_type="dataset", revision=sha)).read_text())
    except Exception:                                                       # noqa: BLE001 (not built yet)
        return None


def local_runs(cache: Path) -> dict:
    """The published runs already fetched and imported on this machine (the site's cache), newest import of each: no network."""
    out = {}
    for db in sorted((cache / "hub").glob("*/*/run/run.db"), key=lambda f: f.stat().st_mtime):
        run, name = db.parent, db.parent.parent.name
        if not imported_ok(run):
            continue
        meta = {}
        for fn in ("run.json", "manifest.json"):
            f = run.parent / fn
            if f.exists():
                meta[fn] = json.loads(f.read_text())
        spec = (meta.get("run.json") or {}).get("spec") or {}
        out["hub:" + name] = {"id": "hub:" + name, "name": name, "path": run, "revision": None, "title": spec.get("name") or name,
                              "planned_days": spec.get("days"), "seed": spec.get("seed"), "people": len(spec.get("agents") or {}),
                              "places": len(spec.get("nodes") or {}), "generated": bool((spec.get("generated") or {}).get("by")),
                              "models": sorted({a.get("model") for a in (spec.get("agents") or {}).values() if a.get("model")})}
        sha = run.parent.parent.name                                         # the revision it was fetched at (its first 12 characters)
        out["hub:" + name]["revision"] = sha
    return out


def imported_ok(run: Path) -> bool:
    from c2viz.site.server import imported
    return imported(run)


def build_run(r: dict, path: Path, cache: Path, folder: str, out: Path) -> tuple[dict, list]:
    """One run's viewer files, written under `out` at their path in the dataset; and its days in brief, from the days built."""
    from c2viz.model import RunModel
    dest = out / folder / r["name"] / "viewer"
    if dest.exists():
        shutil.rmtree(dest)
    RM = RunModel(path)
    head = RM.head()
    head["meta"]["days"] = len(RM.days)
    dump(dest / "head.json", head)
    strip, alive0 = [], None
    for d in RM.days:
        day = RM.day(d)
        day["words"] = day_talk(path, d)
        dump(dest / "day" / f"{d}.json", day)
        alive = sum(1 for p in (day.get("people") or {}).values() if p.get("alive", True))
        strip.append({"alive": alive, "season": (day.get("calendar") or {}).get("season"), "died": max(0, (alive0 if alive0 is not None else alive) - alive)})
        alive0 = alive
    thumbs = Builder(r["id"], path, cache).dir                              # a map the site has already drawn, if any
    for n in ("thumb.jpg", "thumb.json"):
        if (thumbs / n).exists():
            shutil.copy(thumbs / n, dest / n)
    index = {"run": r["name"], "journal_revision": r["revision"], "code_key": code_key(), "built": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
             "days": len(RM.days), "thumb": (dest / "thumb.jpg").exists()}
    dump(dest / "index.json", index)
    return index, strip


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--repo", default=None, help="the dataset of published runs (default: the project's)")
    ap.add_argument("--folder", default=None, help="the folder in the dataset that holds the runs (default: the engine's)")
    ap.add_argument("--only", nargs="*", help="these runs only (their names)")
    ap.add_argument("--force", action="store_true", help="rebuild even when the published files are up to date")
    ap.add_argument("--out", default=None, help="where to build (default: a folder in the cache)")
    ap.add_argument("--no-upload", action="store_true", help="build only")
    ap.add_argument("--local", action="store_true", help="build from the runs already imported on this machine, with no network; then upload with --upload-only")
    ap.add_argument("--upload-only", action="store_true", help="upload what an earlier build left in --out, building nothing")
    ap.add_argument("--cache", default=str(Path.home() / ".cache" / "c2viz-site"))
    a = ap.parse_args(argv)
    from c2viz import touch as E
    repo, folder, cache = a.repo or E.default_repo(), a.folder or E.published_folder(), Path(a.cache)
    out = Path(a.out or cache / "viewer-publish")
    if a.upload_only:
        return upload(repo, folder, out, "viewer files (c2viz " + code_key() + ")")
    if out.exists():
        shutil.rmtree(out)
    if a.local:                                                             # only what is on this machine already
        cat, runs = None, local_runs(cache)
    else:
        cat = Catalog([], repo, folder, "main", True, cache)
        runs = cat.hub_list()
        if cat.hub_error:
            sys.exit(f"could not list the published runs: {cat.hub_error}")
    key = code_key()
    built, catalog = [], {}
    if not a.local:                                                         # the published list: kept for the runs not rebuilt now
        from huggingface_hub import hf_hub_download
        try:
            old = json.loads(Path(hf_hub_download(repo_id=repo, filename="viewer/catalog.json", repo_type="dataset", revision=cat.sha)).read_text())
            catalog = {x["name"]: x for x in old.get("runs", []) if "hub:" + x["name"] in runs}
        except Exception:                                                   # noqa: BLE001 (none yet)
            pass
    for rid, r in sorted(runs.items()):
        if a.only and r["name"] not in a.only:
            continue
        if not a.local and not a.force:
            old = published_index(repo, folder, r["name"], cat.sha)
            if old and old.get("code_key") == key:
                print(f"  {r['name']}: up to date", flush=True)
                continue
        t = time.time()
        try:
            path = r["path"] if a.local else cat.path_of(rid)               # the journal, fetched and imported (cached)
            idx, strip = build_run(r, path, cache, folder, out)
        except Exception as e:                                              # noqa: BLE001 (one run's failure does not stop the rest)
            print(f"  {r['name']}: FAILED {type(e).__name__}: {e}", flush=True)
            continue
        built.append(r["name"])
        print(f"  {r['name']}: {idx['days']} days in {time.time() - t:.0f}s", flush=True)
        catalog[r["name"]] = ({k: r.get(k) for k in ("name", "title", "planned_days", "seed", "people", "places", "generated", "models")}
                              | {"id": rid, "days": idx["days"], "thumb": idx["thumb"], "strip": strip})
    if built or not a.only:
        dump(out / "viewer" / "catalog.json", {"repo": repo, "folder": folder, "code_key": key, "built": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                                               "runs": sorted(catalog.values(), key=lambda x: x["name"])})
    print(f"built {len(built)} run(s) in {out}", flush=True)
    if a.no_upload or a.local or not built:
        return
    upload(repo, folder, out, f"viewer files for {len(built)} run(s) (c2viz {key})")


def upload(repo: str, folder: str, out: Path, message: str) -> None:
    """Every viewer file under `out` to the dataset, in one commit."""
    from huggingface_hub import HfApi
    HfApi().upload_folder(repo_id=repo, repo_type="dataset", folder_path=str(out), allow_patterns=[f"{folder}/*/viewer/**", "viewer/**"],
                          commit_message=message)
    print(f"uploaded to {repo}", flush=True)

if __name__ == "__main__":
    main()
