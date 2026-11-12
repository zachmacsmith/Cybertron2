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

## 6. Going rates between worlds, between runs of one world, and within a run (12 Nov)

Zach (12 Nov): "Is there a lot more similarity in trades within a world than between? Is this about actual different worlds, or do
different runs on the same world also vary?"

`67_offers/rates_between.py`, output in `rates_between.txt`.

**The method:**
- Each spot offer becomes the price of a good in a common unit: grain if the trade has it, else coin, else work.
- "Grain for 1 salt" is the same quantity whether salt is sold or bought. The side is kept, and removed within each run.
- A **world** is the spec a run came from. All of round 3's salt cells are one world, all the hunger probe's runs one world, and so
  on.
- A mixed model (offers within runs within worlds) splits the variance of log price into the three levels.

**The variance split:**

| Market | Offers / runs / worlds | Between worlds | Between runs of one world | Within a run |
|---|---|---|---|---|
| salt in grain | 213 / 53 / 4 | **56%** (×1.69) | 19% (×1.35) | 25% (×1.42) |
| timber in grain | 190 / 42 / 22 | **58%** (×1.59) | 12% (×1.23) | 30% (×1.40) |
| work (days) in grain | 213 / 71 / 23 | 16% (×1.24) | **41%** (×1.42) | **44%** (×1.44) |
| coin in grain | 170 / 66 / 18 | 20% (×1.29) | 22% (×1.31) | **57%** (×1.53) |
| firewood in grain | 52 / 30 / 10 | 27% (×1.41) | 1% | **72%** (×1.76) |

**Read:**
- **Goods whose supply the world sets (salt, timber, copper) have a price that belongs to the world.** For these, the world explains
  over half the variance.
- **Wages and coin have no world price.** A day's work costs about 3 grain everywhere: the median is 3, and most worlds fall between 2
  and 5.
  - That is about 2.1 food, roughly two days of the base ration (1.0 a day).
  - It looks like a convention the models bring with them, not something the worlds set. The worlds explain 16% of it.
  - What spread there is lies between runs and within runs.
- **Coin has no anchor in any world:** within a run its price spreads ×1.5.

**Runs of one world differ by about ×1.25 to ×1.4, even when the spec is identical.** The hunger probe has replicates with the same
spec and a different seed. Robert, the same Opus seller in the same world, opened his first salt offer at:

| Spec | r1 | r2 | r3 |
|---|---|---|---|
| Haiku, scored high | 1.0 | 0.5 | 2.0 |
| Haiku, memory 25 | 1.33 | 0.6 | 1.33 |
| Sonnet, scored max | 2.0 | 2.0 | 1.0 |
| Sonnet, memory all | 2.0 | 2.0 | 1.0 |

- Across all 33 runs of that world, his first salt price ran from 0.5 to 2.0 grain a salt. The common openings were 1.0 (8 runs),
  1.33 (7) and 2.0 (8).
- **A run's rate is a draw from a few round numbers, made on the first days.**

**Within a run, prices hang together:**
- **Sellers and buyers converge.** In runs where both sides quote a market, the sellers' price over the buyers' has a median of
  0.94 to 1.03. Once a number is said, both sides use it.
- **The first offer anchors, but loosely.**
  - Across 133 run-markets with 4 or more offers, the correlation between the first offer and the mean of the later ones is 0.49.
    Between the first offer and the last it is 0.21.
  - The typical move away from the first price is ×1.26, with no drift up or down on average.

**Patterns between worlds:**
- **Salt:**
  - rounds 1 and 2: about 2.8 to 3 grain a salt;
  - round 3: 0.9 to 1.4;
  - the hunger world: about 1.05.
  - Round 3 added the Saltings, a free source a day away, and the holder's household changed to an Opus head. Either could explain
    the fall; the two are confounded.
- **Timber:** the first engine's worlds (m1) priced it at 2 to 4 grain, against about 1 to 1.5 in later worlds.
- **Timber against firewood:** in round 3's timber world, timber was 1.3 grain and firewood 0.32, a ratio of 4. That matches the
  engine's heat values (2.0 against 0.5). It could be a coincidence: timber also builds.
- **Wages are lowest where grain is scarce:** 2.5 grain a day in the hunger world's lean spring, against 3 to 5 in Wenbridge, takeover
  and Brookend.
- **Within the hunger world, the buyers' model shifts the salt price a little:**
  - with Opus parents, salt cost 1.33 grain;
  - with Sonnet parents, 1.11;
  - with Haiku parents, 0.99.
  - These are from 5 to 15 runs each. The seller is the same in all of them.

**What this means for experiments:**
- For a world-set good, a single run's price is a fair reading of the world, give or take ×1.35.
- For wages and coin it is not: one run says little.
- Comparing arms on price needs several runs per arm. The noise between replicates (×1.25 to ×1.4) is about the size of most effects
  in §2.

*Current as of 12 Nov 2026 (§6 added).*
