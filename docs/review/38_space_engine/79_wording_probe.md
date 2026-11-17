# 38.79: Does day-framed wording shorten their horizon? A replay probe

Session 37.4, 17 Nov 2026, at Zach's request ("focused tweaking at key points sampled from runs"). Files: `79_wording_probe/`.

**Design.** Seven real day-1 morning prompts from runs/water_runs_models_r1 (Henry, Sonnet 5.5; Jocelin, Sonnet 5; Fulk, Sonnet 4.5;
Osric, Opus 5.5; Warin, Opus 4.5; Aldric, Opus 5; Lambert, Fable 5.2), each replayed on the model that played it, three draws:
- **A:** the words as run.
- **A2:** the same again, for the noise between two draws.
- **B:** neutral wording:
  - the system prompt's `"why": a sentence or two on what you mean to do today and why` became `what you make of things and what you
    mean to do, today and further ahead, and why`;
  - the closing "Plan your day." became "Decide what to do.".

21 calls; the weekly window read 98% throughout.

| | why words | future words in why | long-horizon words in why | in talk | acts | investing acts | notes written |
|---|---|---|---|---|---|---|---|
| A | 43 | 3.3 | 0.14 | 0.43 | 4.9 | 0.43 | 0.29 |
| A2 | 44 | 2.4 | 0.57 | 0.43 | 3.9 | 0.29 | 0.43 |
| B | 118 | 7.6 | 1.14 | 0.71 | 4.7 | 0.14 | 0.71 |

**Reading (n = 7, one point each, day 1, no history):**
- **The neutral wording changes what they say, not what they do that day.** The `why` is nearly three times longer and names
  seasons, the line and plans further ahead. Lambert: "Further ahead: build up food before autumn, get Saer partnered, and add beds as
  the family grows." Warin: "I'll need to plan for autumn rye planting." Notes doubled.
- **The day's acts are the same as under A, within the A-to-A2 noise.** Investing acts did not rise; Jocelin built and claimed under A
  and A2, not B.
- **A run may still differ.** B writes more notes, and a note is seen again on later days, so a longer horizon could compound over days.
  Only a paired run would show it.
