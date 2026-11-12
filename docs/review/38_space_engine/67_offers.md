# 38.67: Offers across all cybertron2 runs: how they are priced, and what moves the price

Session 37.4, 12 Nov 2026. Zach (12 Nov): "investigate offers across all resources across all cybertron2 runs ... compare to scarcity
of the object currently, how many other people are offering for that or mentioning it, hunger / being low on food / starving".

Files in `67_offers/`:
- `offers_extract.py`: one row per offer, with that day's market;
- `offers.csv`: the rows;
- `offers_analyse.py`, with its output in `analysis.txt`;
- `offers_charts.py`, which draws `offers_price.png`.

## The data

- **1,896 offers from 157 runs**, taken from the runs folders of both repositories and the wild seed run. Bots are left out, which
  leaves 1,856 offers.
- **Each offer is read at the dawn of its day,** from `run.db`. The day comes from the "You offered (On)" result line. 93 runs have
  this state, with 970 single-item spot offers among them. The older runs (m1, w1 to w3, c1 to c7, the early b and v runs) keep only
  the final state. They are used for prices and roundness, not for the market.
- **What each offer's market records:**
  - **Scarcity:** how much of the item given, and of the item asked, the place holds per person there. This counts stores, the hands
    of the people there, and things lying there.
  - **The maker's own stock:** how much the maker's household holds of each item. That is the stores its claims let it withdraw from,
    plus its members' hands.
  - **The maker's hunger:** 0 if fed, -1 if hungry, -2 if starving, and meals missed in a row.
  - **The household's food,** in days per head.
  - **Competition:** the other offers open at the same place that give or ask for the same item.
  - **Mentions:** how often each item is named in that day's replies.
- **The price** is the quantity asked divided by the quantity given.
  - It is compared with the run's going rate: the mean log price of the same pair (item given → item asked) in the same run. This
    removes the differences between worlds.
  - "rel" above 0 means the maker asks more than the going rate.

**Limits:**
- 56% of the market sample is the salt probes (rounds 3 and hunger), and 18% is one person, the Fowler head Robert. Section 4 is
  repeated without the probes.
- Mentions also count the maker's own offer text, so they partly measure the maker's interest.
- Hunger is known only for the maker, not for the person who takes the offer.

## 1. Prices are round and anchored

- **99.5% of quantities are whole,** and 83% of price ratios have both terms at 4 or under.
- **The most common ratios:**
  - 1:1 (393 offers);
  - 2:1 (247);
  - 1:2 (228);
  - 3:1 (126);
  - 3:2 (113);
  - 2:3 (108).
- **The spread** is the factor that one standard deviation of log price stands for:

  | Pair | n | Median | Across runs | Within a run | Within one maker |
  |---|---|---|---|---|---|
  | work (days) → grain | 184 | 3 | ×1.74 | ×1.37 | ×1.14 |
  | coin → grain | 164 | 1.33 | ×1.78 | ×1.42 | ×1.21 |
  | salt → grain | 143 | 1 | ×1.68 | ×1.40 | ×1.33 |
  | timber → grain | 109 | 1.5 | ×1.75 | ×1.34 | ×1.16 |
  | grain → salt | 70 | 0.75 | ×1.87 | ×1.27 | ×1.09 |

  - **Prices are not random.** A maker who reposts an offer usually keeps or nudges the price, by ×1.1 to ×1.3.
  - **Across worlds the same pair varies by about ×1.7 to ×1.9.** No price carries over from one world to another: each run sets its
    own.
- **Bigger offers are cheaper per unit.** The coefficient on the log of the quantity given is -0.25.
- **How often reposts keep the same price:** Sonnet 61%, Haiku 46%, Opus 22%. Opus reprices; Sonnet repeats itself.

## 2. What moves the price

The regressions use log price, with a fixed effect for each run and pair. Standard errors are clustered by maker. All variables are
log(1 + x). The full tables are in `analysis.txt` §4 and §9.

| Driver | The sign rational pricing predicts | Across makers (n 649) | Within one maker over days (n 391) | Without the salt probes (n 235) |
|---|---|---|---|---|
| **Own stock of the good given** | − | **−0.32**, p < 0.001 | **−0.24**, p 0.02 | **−0.39**, p < 0.001 |
| **The household's food (days)** | + (less food, sells cheaper) | **+0.15**, p 0.004 | **+0.23**, p 0.005 | **+0.22**, p 0.02 |
| **The place's stock of the good asked** | + | **+0.22**, p < 0.001 | **+0.20**, p 0.001 | **+0.19**, p 0.02 |
| Others offering the good asked | + | +0.17, p 0.004 | +0.08, n.s. | n.s. |
| Others offering the same good (rivals) | − | −0.11, p 0.08 | −0.16, p 0.02 | n.s. |
| The place's stock of the good given | − | n.s. | n.s. | n.s. |
| Others asking for the good given (demand) | + | n.s. | n.s. | n.s. |
| Others asking for the same good | − | n.s. | n.s. | n.s. |
| Own stock of the good asked | + | n.s. (slightly −) | n.s. | n.s. |
| Hunger flag (beyond food days) | − | n.s. | n.s. | n.s. |
| Mentions | + | n.s. | +0.13 for the good given, p 0.01 | n.s. |
| Day of the run | ? | 0 | 0 | 0 |

**Read:**
- **Three drivers hold in every cut:**
  - **Less of the good in hand, a higher ask.** The coefficient of -0.3 means that halving one's stock raises the ask by about 20 to 25%.
  - **Less food at home, cheaper selling.** A household down to under 2 days of food sells about 9% below the going rate (Opus
    makers about 13%). One with 10 or more days asks about 4% above it (the chart's middle panel). This is the pattern Robert showed in the salt runs, now across
    all runs.
  - **More of the wanted good lying around the place, more of it asked.**
- **What makers do not price:**
  - other people's demand for what they sell;
  - how scarce their own good is in the village. Only their own stock counts.
  - Competition from rival sellers shows weakly, and it is not robust.
- **They are price-takers of their own situation, not readers of the market.**
- **By model,** the response to own stock and to food is mostly Opus's: −0.44 and +0.42, both p < 0.001. Haiku's and Sonnet's
  coefficients point the same way on own stock (about −0.17) but are not significant, and Sonnet shows no food effect at all.

## 3. Hunger

**Offers asking for food, by the maker's state:**

| State | n | rel | Share paying above the going rate | Taken |
|---|---|---|---|---|
| Fed, food in store | 296 | +0.04 | 36% | 26% |
| Fed, under 2 days of food | 59 | −0.02 | 37% | 12% |
| Hungry | 43 | −0.10 | 42% | 21% |
| Starving | 37 | −0.14 | 62% | 19% |

- **The starving pay about 13% more for food.** Yet they are taken no more often.
- **What the hungry offer,** by share of their offers:
  - they buy food: 67% of their offers, against 40% when fed;
  - they sell food: 7% (18% when fed);
  - they offer work for food: 9% (15% when fed). They turn to buying with goods, not labour.
- **Hungry makers selling food ask the going rate.** There are only 9 such offers.

## 4. Taking does not follow price

| Asking against the going rate | n | Taken |
|---|---|---|
| Much cheaper | 139 | 22% |
| Cheaper | 100 | 37% |
| At the rate | 154 | 42% |
| Dearer | 111 | 32% |
| Much dearer | 145 | 23% |

- **A logit of taking on rel is flat:** the coefficient is -0.06, p 0.77.
- **Offers far from the going rate are taken least, in either direction.** Cheap ones are mostly the hungry or the late, cutting
  prices after an offer went untaken, so cheapness marks a market with no buyer.
- **Whether an offer is taken depends on whether someone wants the good and holds the price, not on the terms.** This fits §2:
  neither side reads the market.

## 5. Credit

- **24 offers ask for grain now against more grain later.** The repayment is ×1.33 to ×2.0, median ×1.5.
- 22 are by Opus, 15 of them by Robert in the salt worlds. Haiku's Hugh made one.
- **Only 2 were taken.** Interest exists as a form of offer but not as a market.

## What this says

- **Rational on their own side, blind to the other side.**
  - Each maker prices from their own stock and their own food, in the direction a trader by need would.
  - Opus does this clearly; Haiku and Sonnet weakly or not at all.
  - Nobody prices from the village's scarcity of what they sell, or from how many others want it. Every prompt lists the offers open
    at the place (`prompt.py`, "Offers open here"), but makers do not price from them. Past trades and their rates are not shown.
- **Prices are focal.** Prices of 1:1, 2:1 and 1:2 make up half of all offers. A run settles its own rate in the first days, and
  later offers move from it in steps.
- **The hungry pay more and sell less food,** as they should. But the market does not reward a better price with more takers, so
  the price a hungry person pays is mostly lost.
- **For engine work:**
  - If prices that clear across a place are wanted, the open offers are not enough. Makers would need what last traded and at what
    rate, which no prompt shows now.
  - That is a question for senses (the guide) and for the prompt, not a mechanic. It is not proposed here.

*Current as of 12 Nov 2026.*
