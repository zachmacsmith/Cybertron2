---
id: W-28
kind: thread
state: waiting
updated: "2026-11-20"
---

# The Cybertron 2 website (W-28)

*waiting · site (c2viz, session "Cybertron website") · touched 10 Nov (11 days ago)*

> **Next:** Zach sets up the Netlify site and the subdomain; `python -m c2viz.site.viewer_publish` after each publish (calling it from cybertron2/publish_hf.py is 37.4's to agree)

## What it is
The Cybertron 2 website: home, runs page, run explorer with each day's messages; viewer files on the Hub so it runs with no server (static on Netlify)

## Done so far, and what is left
built and pushed; viewer files for all 64 published runs uploaded (c2viz code_key ef4c0aa36282).

**Left:** Zach sets up the Netlify site and the subdomain; `python -m c2viz.site.viewer_publish` after each publish (calling it from cybertron2/publish_hf.py is 37.4's to agree)

## Where
- `main: c2viz/site/ (viewer_publish.py, static.py, server.py, run.html, web/), netlify.toml`
- `the Hub: `runs/<run>/viewer/`, `viewer/catalog.json``


## Mentioned by
- [[W-28b Build brief 4b written|Build brief 4b written (W-28b)]]
- [[Thread tracking a registry, hooks, checks and a commit schema|Thread tracking: a registry, hooks, checks and a commit schema]]
- *and 2 index or audit notes*
