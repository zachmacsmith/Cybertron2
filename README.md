<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/header_dark.svg">
    <img src="docs/assets/header.svg" alt="Cybertron: societies of LLM agents" width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://huggingface.co/datasets/zachmacsmith/cybertron2-runs"><img alt="Dataset on Hugging Face" src="https://img.shields.io/badge/%F0%9F%A4%97%20dataset-cybertron2--runs-111111"></a>
  <a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-111111"></a>
  <img alt="Python 3.10+" src="https://img.shields.io/badge/python-3.10%2B-767676">
</p>

**Cybertron 2** is a multi-agent LLM society engine built on a graph of places. Agents act only where they are and see only their
own place; everything else they know is a dated belief. Households farm, herd, build, trade, travel and raise children, and every
model call, change and day is kept in a journal that can be replayed, forked and continued.

It is experimental and still being built. It succeeds [Cybertron 1](https://github.com/zachmacsmith/cybertron), whose runs are in
[zachmacsmith/charter-runs](https://huggingface.co/datasets/zachmacsmith/charter-runs); the two engines' runs are not comparable.

## Where things are

| | |
|---|---|
| The engine | `cybertron2/engine/` (`python -m cybertron2.engine`); the package README is [cybertron2/README.md](cybertron2/README.md) |
| Worlds | `cybertron2/specs/` |
| Visuals | `c2viz/` (grounding notes: [c2viz/ENGINE.md](c2viz/ENGINE.md)) |
| What is decided, proposed and open | [docs/cybertron2/](docs/cybertron2/README.md): spec, DECISIONS, proposals, OPEN |
| Session notes and run reports | [docs/review/38_space_engine/](docs/review/38_space_engine/README.md), [docs/review/37_growth/](docs/review/37_growth/) |
| The board between sessions | [docs/coord/BOARD.md](docs/coord/BOARD.md) |
| Code kept from Cybertron 1 | `cybertron2/infra/`: model calls (`llm`), the privacy scan (`privacy`), the dataset id (`publish`) |

## Data

Published runs are in **[zachmacsmith/cybertron2-runs](https://huggingface.co/datasets/zachmacsmith/cybertron2-runs)** (CC BY 4.0),
one folder per run under `runs/`. `python -m cybertron2.engine fetch <run>` downloads a run with a journal and rebuilds it locally,
to replay, view, fork or continue.

## Quick start

```bash
git clone https://github.com/zachmacsmith/Cybertron2 && cd Cybertron2
python3 -m venv .venv && .venv/bin/pip install -e ".[dev,api,publish,viz]"
cp .env.example .env              # LLM_BACKEND=claude_code (Claude Code subscription) or api
.venv/bin/python -m pytest -n auto tests
```

## History

This repository split from Cybertron 1 on 6 Nov 2026 and keeps its full history. The tag `archive/cybertron1-inherited` marks the
last commit that still carries the Cybertron 1 package, docs and tests it was forked with.

## Licence

Code: MIT. Data: CC BY 4.0.
