"""The runs world with a model to each household (Zach, 17 Nov; proposals/model_households.md; WORK W-58).

Made from 37.2's runs world (specs/water/runs.yaml) and nothing else changed in it:
- each village gets one strong, one middle and one weak model; which household in a village takes which is a seeded draw
  (random.Random(17)), not a choice;
- every member with a model, youths included, plays their household's model (Zach: "make sure youths are seeded with their
  households model"); `household_models` gives it to a child coming of age and a household founded in the run;
- everyone keeps the goal line for good, graded on living descendants of their household's founders (Zach: "graded on anyone
  descending, not people specifically in their household"), with room for it whole (memory.kept.words 80);
- 24 days.

    python3 -m cybertron2.specs.make_runs_models
"""
from __future__ import annotations

import random
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
SRC = HERE / "water" / "runs.yaml"
OUT = HERE / "water" / "runs_models.yaml"

TIERS = {                                                   # by village: strong, middle, weak (spread so no village holds all
    "Highpool": ["claude-fable-5-2", "claude-sonnet-5", "claude-sonnet-4-5"],     # the best or worst of a tier)
    "Middleham": ["claude-opus-5-5", "claude-sonnet-5-5", "claude-haiku-4-5"],
    "Lowstrand": ["claude-opus-5", "claude-opus-4-5", "claude-haiku-5-5"],
}
SEED = 17
DAYS = 24
GOAL = ("YOUR GOAL, on which you will be graded: grow your line, everyone descended from your household's founders, to be as many as "
        "you can, and see them survive and spread over as many generations as you can. Your score is the number of people descended "
        "from your household's founders who are living at the end of day 200, in whatever household or place they live: the more, "
        "the better.")


def households_by_village(w) -> dict:
    """{village: [household, ...]} from where each household's buildings stand (sorted, so the draw is the same each time)."""
    p2n = {pid: nid for nid, n in w["nodes"].items() for pid in (n.get("parcels") or {})}
    out = {}
    for b in w["buildings"].values():
        hh = b.get("household")
        if hh and p2n.get(b.get("parcel")) in TIERS:
            out.setdefault(p2n[b["parcel"]], set()).add(hh)
    return {v: sorted(hs) for v, hs in out.items()}


def make(src=SRC) -> dict:
    w = yaml.safe_load(Path(src).read_text())
    rng = random.Random(SEED)
    hm = {}
    for v in TIERS:
        hs = list(households_by_village(w)[v])
        if len(hs) != 3:
            raise ValueError(f"{v} has {len(hs)} households, the tiers want 3")
        rng.shuffle(hs)
        hm.update(zip(hs, TIERS[v]))
    w["name"] = "water_runs_models"
    w["days"] = DAYS
    w["household_models"] = hm
    w.setdefault("memory", {}).setdefault("kept", {})["words"] = 80
    for a in w["agents"].values():
        if a.get("model"):
            a["model"] = hm[a["household"]]
        a["kept"] = [{"text": GOAL, "fixed": True}]
    return w


def main():
    w = make()
    head = ("# Made by cybertron2/specs/make_runs_models.py from specs/water/runs.yaml (37.2's): a model to each household, the goal\n"
            "# graded on descendants kept for good by everyone, 24 days (Zach, 17 Nov; proposals/model_households.md). Do not edit.\n")
    OUT.write_text(head + yaml.safe_dump(w, sort_keys=False, width=140, allow_unicode=True))
    for h, m in sorted(w["household_models"].items()):
        print(h, m)


if __name__ == "__main__":
    main()
