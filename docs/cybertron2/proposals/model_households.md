# A model to each household in the runs world

**Status:** discussion (17 Nov 2026). Scoping only; nothing built (Zach: "Just scope this out now").

**Owner:** 37.4.

**Touches:** the runs world (37.2's `specs/water/runs.yaml`, used through a derived file of ours), `household_models` (built for the
peoples benchmark, D4-115 to D4-118), `infra/llm.py`, `proposals/peoples_benchmark.md`.

## Summary

Each of the runs world's nine households is played by one model, every member and every child who comes of age, across model
generations: for example Fable 5.2, Opus 5.5, Opus 5, Opus 4.5, Sonnet 5.5, Sonnet 4.5, Haiku 5.5, Haiku 4.5 and one more. It is the
peoples benchmark's "a model is a people" at the scale of the household, in the world where villages most depend on each other (a
weir upstream takes the run before it reaches the villages below).

## The proposal

1. **The world:** a derived file `specs/water/runs_models.yaml` made from 37.2's runs world after the D2-229 remake. It sets each agent's
   model to their household's and writes `household_models`, so a child coming of age and a household founded in the run keep it
   (`life.come_of_age`, `world.p_found`; both built). Standard settings kept. Optionally the graded population line of W-55.
2. **The models (9 slots):** Zach's list (Haiku 5.5, Haiku 4.5, Sonnet 4.5, Opus 5.5, Opus 5, Fable 5.2) and three more, for example
   Sonnet 5.5, Opus 4.5 or 4.8, Sonnet 5 or Sonnet 4.6.
3. **Placement against position:** in this world a household's station on the river (Highpool upstream, Middleham, Lowstrand downstream)
   matters as much as its players. Each village gets one strong, one middle and one weak model. With money for it, three runs rotate
   the placement (a Latin square), so each tier holds each station once.
4. **Reading:** per household, against its station:
   - people at the end (the goal's score, if the line is used);
   - meals missed;
   - capital and works built (weirs, smokehouses, fields);
   - agreements kept and broken;
   - thefts;
   - and a qualitative reading of each house.
   n = 1 a placement, so these are readings, not a ranking.

## What has to be checked or built

- **Each model through the CLI backend.** `claude -p --model` with each id, one smoke call each (cents), before any run:
  - **Haiku 4.5** returns thinking text, because it has a fixed budget.
  - **Fable 5.2** cannot turn thinking off.
  - **Older models' structured output** through `--json-schema` needs seeing.
- **The API backend.** `infra/llm.py` sends adaptive thinking to every model but Haiku 4.5. Sonnet 4.5 and Opus 4.5 take a fixed budget
  instead, so the API path needs one branch more. The CLI path, which the runs use, sets thinking itself.
- **Sonnet 4.5 retires on 30 Nov 2026.** A run with it must be before then; otherwise drop it.
- **Context:** Haiku 4.5 has 200K; the prompts are far under it.

## Cost

- **Prices** (per million tokens in and out):

  | Model | In and out |
  |---|---|
  | Fable 5.2 | $8 and $40 |
  | Opus 5, Opus 4.5 | $5 and $25 |
  | Opus 5.5 | $4 and $20 |
  | Sonnet 4.5 | $3 and $15 |
  | Sonnet 5.5 | $2 and $10 |
  | Haiku 4.5 | $1 and $5 |
  | Haiku 5.5 | $0.10 and $0.50 |

- **Size:** the lake run (14 people, 3 Opus, 2 Sonnet, 9 Haiku 5.5) cost about $17 for 24 days. The runs world has 36 people, and here
  about two thirds would be on Opus-priced models or dearer.
- **A rough guess** is $60 to $120 for 24 days, to be measured from day 1's real spend. It is the weekly limit that binds, not the
  dollars: the runs are billed to the subscription (`week_stop`).
- **Three rotated runs** cost three times as much.

## Why

- **Zach (17 Nov):** "for the runs world, when we do it can we make each household a different model (e.g all haiku 5.5, 4.5, sonnet
  4.5, opus 5.5, opus 5, fable 5.2 etc. etc.)".
- **The lake runs:**
  - the Opus heads acted on the goal at once;
  - the Haiku youths stalled on it (38.75).
  
  A world of one model to a household shows how far that is the model.

## Alternatives considered

- **Mixed tiers in each household** (scenario_design's default: Opus at the poles, Sonnet in the middle, Haiku in the bulk). That is
  better for a society, but says nothing about one model.
- **One model to a village** (three villages, three models). It is cleaner within a village, but compares only three models, and the
  station confound is total.

## Open questions

1. The nine models.
2. One run, or three rotated.
3. With or without the graded population goal (W-55's line).
4. The length (24 days as the lake runs, or longer).
5. Whether a household founded in the run keeps its founder's model (built so) and whether a member who marries out takes theirs (now: the
   household's model is set at coming of age only; a grown person keeps their own).

## Affects

- A derived world file; `infra/llm.py` (the API branch only); no engine change.

## History

- **17 Nov 2026:** scoped at Zach's request. Nothing built.

## Sources

- proposals/peoples_benchmark.md (D4-115 to D4-118: `household_models`).
- 38.75 (the lake runs).
- engine/life.py `come_of_age`, engine/world.py `p_found`, engine/generate.py (household_models), infra/llm.py.

*Current as of 17 Nov 2026.*
