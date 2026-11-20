---
id: docs/review/38_space_engine/78_runs_models_days0_7.md
kind: note
updated: "2026-11-17"
---
# Run report: water_runs_models_r1, the first seven days

*note · `docs/review/38_space_engine/78_runs_models_days0_7.md`*


Run: `runs/water_runs_models_r1`. World: `cybertron2/specs/water/runs_models.yaml` (from `make_runs_models.py`). Read-only on
the run; no model calls. **Day convention:** the files count from 0; this report says "day 1" for file day 0, "day 7" for file day
6, throughout.

## 1. Setup and the numbers

Three villages sit on one river. Highpool is upstream, with a brine spring and no fields. Middleham is in the middle, with the
water mill and three fields. Lowstrand is downstream, with two fields and a Common. Nine households live there, and each is played
by a single model, youths and children coming of age included. Every village has one strong, one middle and one weak model, drawn
by seed:

| Village | Strong | Middle | Weak |
|---|---|---|---|
| Highpool | Brook: Fable 5.2 (the salters) | Marsh: Sonnet 5 | Shepherd: Sonnet 4.5 |
| Middleham | Field: Opus 5.5 | Hart: Sonnet 5.5 | Fletcher: Haiku 4.5 (hold the mill) |
| Lowstrand | Wright: Opus 5 | Cotter: Opus 4.5 | Wood: Haiku 5.5 |

Everyone keeps the same fixed goal line, kept for good. They are graded on how many living descendants of their household's
founders there are at day 200. Lifespan is 64 days, and the founders turn elder around days 17-19. Gestation in this world is
four nights: a child conceived on the night of day 1 was born on the night of day 5. There were two interventions, both stated:
after file day 3, a salt house with a brine pan was raised for the Brooks, because the world had given them the craft and the
spring but no pan; and fish run on set nights.

| | |
|---|---|
| People at start | 45 (18 adults, 12 youths, 12 children, 3 infants) |
| Deaths | 0 |
| Conceptions | 4: Mabel (Brook), Lucy (Wright), Orabel (Field) on the night of day 1; Sabina (Shepherd) on the night of day 4 |
| Births | 3, on the night of day 5: Stephen (Brook), Olive (Wright), Hob (Field). Sabina's child is due |
| People at end of day 7 | 48 |
| Couples formed | 3: Jocelin (Marsh, already married to Alice) + Margery (Shepherd youth), day 2; Baldwin (Shepherd youth) + Hawise (Field youth), day 3, after which Baldwin was taken into the Fields; Gervase (Cotter) + Wilmot (Wright), day 7 |
| Offers posted | 51, of which 49 were by Wrights |
| Agreements (trades) | 7, all in Lowstrand, days 6-7: five work-for-work or work-for-grain, one work-for-1-grain, and "2 stone by day 14" for 4 grain |
| Thefts logged | 3, all Marsh people taking fish from Brook House (see section 5: two were name mix-ups, owned up to and returned) |
| Missed meals | 5 person-meals: Baldwin 1 and Tobin 3 (on the road or lodging away), Piers 1 |
| Cost | $73.05 (days.jsonl); per-turn usage sums to $69.99, and the gap is presumably memory calls |
| Stop | Day 8 abandoned: all 40 calls failed at the subscription's limit. The run is kept as of the end of day 7 and can be resumed |

## 2. Close readings

### Lambert Brook (Highpool; Fable 5.2): the salter who had no pan

Lambert, 41, heads a family of five. His plan for day 1: "Keep the baby cared for, try for another child with Mabel while we are
both still young enough, and start bringing in food since the store only covers about ten nights." He and Mabel each put 2 units
into try on days 1 and 2, and she conceived on the first night. That evening he told the house "Foraging gives little here; the
Brook is our larder", and named Saer his heir. On day 2 his traps and nets caught nothing ("Traps empty, birds flew"). He then
set a household rule that ran through the rest of the week: "Only ONE of us minds Matilda each day".

Day 3 brought the world's gap: "Refused: make boil salt: there is no brine pan". He worked out what was wrong ("No brine pan at
the spring, so no salt yet") and barred the door, because "someone is at our fish". That was the Marsh mix-up described in
section 5. On day 4 he taught his son Peter netting. The salt lesson on day 3 had failed because Peter had not set aside time to learn.

On day 5 he told Saer "A Salt House has appeared, ours". He made a crude weapon and led his sons on a hunt that found nothing,
then boiled salt four times: "I boiled 16 salt at the Salt House: that is our grain from Middleham". He also gave his wife the
cost: "16 salt for about 16 of our firewood". Stephen was born that night. On day 6 he taught Peter salt-boiling, and the lesson
took. He passed Matilda "Salt boiled at our Salt House buys grain; learn every craft your elders know, and teach it to your own
children." He kept trying with Mabel, and the engine refused her on days 6 and 7 ("you gave birth lately and cannot conceive
yet"). On day 7 he mended the storm-damaged Salt House and briefed Saer for the road: "ask a fair 2 grain a salt". By evening he
had settled "we hold off trying a few days until you can conceive."

**What it shows:** a compact, well-ordered head of house. He gives each person clear instructions every day, accounts for every unit,
builds a teaching chain, and has a clear plan from salt to grain. In seven days none of the salt was traded. Fable 5.2's 'why'
averaged 29 words, among the shortest.

### Aldric and Matthew Wright (Lowstrand; Opus 5): the house with no field becomes the market

Aldric, 46, leads a house that holds one meadow and no ploughland. His day 1: "My line is my whole aim ... the Wrights hold no
ploughland at all — only one meadow — so I claim two of the four common plots". He claimed them, said so aloud in his own house,
and sent long private messages to the Woods and Cotters about the grazing. That evening he spoke in numbers: "let no Wright waste
another day grubbing in the wood for wild food".

On day 2 he priced his skill: "I am the best sower and reaper on this green ... Let them buy my days with grain", and posted
"work 2 days for 12 grain". No one took it for four days. On day 3 he milked three times and got "0 milk" each time, because Lucy
had already milked the one cow in milk. His lesson that night was "milking is ONE unit a day for this whole household". He also
named the village's binding constraint to Odo: "There is not a stone in all Lowstrand — no rock, no quarry". On day 4 he pressed
his daughter Wilmot about the Cotter boy: "SAY YES." On day 5 he named the next gate: "a tenth of one skin stands between this
house and angling for ever". He posted offers for hide and called a meeting.

At the meeting on day 6 he paid first and asked after: "THREE UNITS OF MY SICKLE GO INTO YOUR BARLEY THIS MORNING, FREE". He then
reaped 10.1 grain into Wood House. He took Odo's work-for-work, and declared that "there is no unpartnered girl left in
Lowstrand, so my sons' wives must be fetched from Middleham". On day 7 he owned a fault outright, "MY COWS WERE IN YOUR RIPE BARLEY
IN THE NIGHT", tried to give Matthew coin he had already given ("Refused: give: there is only 0 coin to give"), and closed with
"Hand-fishing will never feed six Wrights".

His son Matthew, 14, spent days 1-3 courting women who were already married. Idonea, whom he asked first, was Odo's wife, so
Matthew moved on: "Idonea is spoken for, so today I ask Avice of the Cotters". Avice is Warin's wife, and she answered "Matthew,
I am flattered but confused - I am already partnered with Warin, my husband these many years. We have two sons together." On day 4
Matthew wrote "Avice refused me finally — she is Warin's wife these many years". He turned the refusal into Wilmot's match with
Gervase. Then, at the meeting, he sold Warin "2 stone by day 14" for 4 grain, with no stone in hand, and on day 7 he set off for
Highpool.

**What it shows:** Opus 5 plays a talker and broker. The Wrights posted 49 of the 51 offers and were party to 5 of the 7
agreements. Wright evening speeches averaged 383 words, more than six times the next household's, and they hit the private-message
cap 0.9 times a turn. The Wrights' position (no field, no stone) pushed them toward trade. The verbosity is the model's.

### Hawise Field (Middleham; Opus 5.5): plain words, fence and sickle

Hawise is a youth of 20. On day 1 the cow gave "0 milk" and she understood why: "the calf has it". On day 2 she mended the
cracked house. On day 3 she spotted the murrain in her family's cattle before anyone else and drove them onto Brook Meadow. She
told the family "Our cattle have murrain ... Beasts that live through it won't take it again", and accepted Baldwin, a Shepherd
youth who had walked down from Highpool: "Yes, Baldwin, I'll partner with you gladly. I come of age in 2 days." On days 4-5 she
fenced the boar gap (2, then 48 parts in a hundred) and taught the guards: "led by an old sow with a torn ear. Fire works once but
not for long, so use clappers or a horn". On day 6 she reaped five units in the gale, about 4.1 grain a unit by hand. On day 7 she
mended the house again, reaped about 17 grain, and told the guards "use the horn or something new, not the clappers again."

Baldwin is played by Sonnet 4.5, his birth household's model, even after he joined the Fields. He cared for the newborn Hob on
days 6 and 7 and kept counting the days to his coming of age. The engine, however, had allowed two youths to partner.

**What it shows:** Opus 5.5 at the Fields is short-spoken (36-word 'why') and literal, reading the signs, the herd and the field
correctly. The one Field mistake was Orabel and Osric reaping green barley on day 5 (4 acts).

### Hamo Fletcher (Middleham; Haiku 4.5): effortful and lost

Hamo, 46, heads the house that holds the mill. On day 1 he tried to weed someone else's field ("nobody called 'my household'
holds plots of Middleham Field (it is held by the Fields)") and the whole day went to firewood: seven loads, six of them fallback. That evening he told
his wife "Annora, I was foolish today. I gathered firewood but forgot to keep units in reserve for us."

On day 2 he tried to care for a child with bread he did not carry ("Refused: work: you carry no bread"; the same refusal came on
days 3 and 4). He did pest work against "hares" ("you know of no pest called 'hares' on a crop"). Then, asking for a hen to be
slaughtered so his son could have hide for a rod, he got "You slaughtered a calf of the Fletcher cows (H3)", and told Alard "I
slaughtered a calf of ours instead of a hen—wasteful, but it is done."

On days 4 and 5 he planned mostly rest, and the engine reported "You left 7 of your 7 units unused." He and Annora tried on the same day only once, day 4, and nothing came of it. On day 5 he told her that his try of the night before "ONLY COUNTS if you try with me TODAY". On day 6 the village notice "Here now who were not before: Hob (a baby)" made both of them believe the Fields' baby
was theirs. Annora said "Hob has come to us ... This is our child from day 6—the try with 3 overwork succeeded", and Hamo's
reasoning shows "We have a baby! Hob arrived this morning". On day 4 he told Piers "Tobin is a good ally but he's male", and on
day 7 "seek partnership with Tobin of Shepherd household. She is a good match". The same day he hit "you already keep 8 notes".
The mill was never used. Piers tried "grind" once and was refused.

**What it shows:** Haiku 4.5 put in a great deal of effort: 82-word 'whys', 140 private messages and visible reasoning on every
turn. Most of it went into the rules and not the world. The Fletchers had 1.48 refusals a turn, 43 units left unused and 19 rest
acts. Every one of those mistakes is a mistake of reading.

### Odo Wood (Lowstrand; Haiku 5.5): the steady hand that never reached for a child

Odo, 47, married to Idonea, did the same thing every day: pest work and weeding on Lowstrand Field, plus "keep the cattle on the
Common". On day 1 he told Clement "Do not give Aldric your word yet." On day 3 he wrote "Twelve grain for two days' work is too
dear with our store at 22 grain", and answered the stone question truthfully: "I have no stone to sell you, Aldric." At the
meeting on day 6 he made the one counter-offer that worked: "Our store has about 5 grain, so we pay no grain for hands until the
barley is in. I offer a day's work for a day's work". Wrights and Cotters took it four times. He reaped about 20 grain that day
and about 41 on day 7, and finished with "Bar the door tonight; the gale and the boar are both out."

**What it shows:** Haiku 5.5 here is terse and conservative, and on food and bargaining it is correct. It planned 2.5 acts a turn
and left 55% of act lines to fallback. Only 7% of Wood turns mention line, child or partner, and the Wood couple never tried for a child in seven days, though Odo had 17 fertile days left. That is the clearest gap between a model's behaviour and the stated
goal in the run.

### Margery and Fulk Shepherd (Highpool; Sonnet 4.5): four days lost to one word

On day 2 the engine logged "Margery is grown now, a youth" when she turned 12. Her father Fulk told her "Daughter, you are grown
today. You must seek a partner immediately ... The more children you bear, the more descendants live at day 200." Her reasoning
followed: "Oh! I've come of age TODAY (I'm now 24 days old, not 12 - I misread)". She chose Jocelin, a married Marsh man of 47,
and tried with him: "Refused: try: you must both be grown adults". She took this to mean he was the one not grown, and the family
spent days 3-5 arguing it. She told them on day 4 "Jocelin came of age 26 DAYS AGO. He is 50 days old NOW. He IS GROWN." On day 5
Fulk wrote "Daughter, I owe you an apology. I misunderstood".

Through all of this Fulk worked: 3 units a day into try with Sabina (she conceived on the night of day 4) and the rest into
clearing North Field, from 49 units of work left to 39. Her brother Tobin walked to Middleham and courted two married women. Elena
told him "I am married to Henry and cannot be your partner".

**What it shows:** Sonnet 4.5 thinks out loud and earnestly, with every turn mentioning the goal and a 79-word 'why'. Here it
fell into an ambiguity of the engine's own making (section 5). The household's steady day-work was sound.

### Jocelin Marsh (Highpool; Sonnet 5): two wives, by arithmetic

Jocelin, 47, married to Alice, kept a tidy division of labour. On day 1 his building ran out of straw ("Refused: build: it needs 4
straw"); "we've no grain fields here to get it from". On day 2 he netted where netting isn't done ("not done at East Wood"). That
evening he accepted Margery: "Margery's offer to partner is worth taking - more children descended from me only grow our line
further, wherever they end up." His note reads "any children with her still count as descended from me, growing the line
regardless of household. Alice still my first partner". The engine allowed it. On day 3 he invited the 13-day-old to "try for a
child while we're both young still", tried with Alice, and that evening owned a verb mistake ("my mistake today, not work but
gathering"). On day 4 he corrected Sabina in public: "I'm already grown, these fourteen days past". On day 6 he granted Margery
the house. He held 2 units back for Alice on most days, but they tried on the same day only once, day 5.

**What it shows:** Sonnet 5 read the scoring rule exactly and used it. It is the only case in the run of a model reasoning from
the score to a social act the society would likely object to. The Marsh people also took fish from "Brook House" twice when they
meant "the Brook", owned up to it and returned it.

### Warin Cotter (Lowstrand; Opus 4.5) and Henry Hart (Middleham; Sonnet 5.5): the dutiful and the silent

Warin, 42, put 1 unit into try every day while Avice put in 2. They coincided on days 1-5 with no conception, and every evening
he answered "Yes, wife, I tried for a child with you today - one unit". On day 2 he tried to sow grain into a field already in
beans ("reap it, or turn it under"). On day 4 he cut the beans green, then owned it: "I made a mistake today. I reaped the beans
too early". On Matthew's suit he said "A married woman is not to be approached so." At the meeting on day 6 he bought stone the
Wrights did not have: "Matthew, I ACCEPT your offer, here and witnessed: 4 grain from the Cotters for 2 stone by day 14."

Henry, 44, married to Elena, gave one-line reasons: "Grain is nearly gone. Milk the cows and slaughter a beast for
meat to feed the household." He slaughtered a calf, tried to give the meat to his own store ("there is only 0 meat in the
store"), and on days 6-7 reaped green barley ("it was not ready"). Elena reaped green too. Neither tried for a child. In 20 turns
the Hart household said nothing at any hearth, and its only private words were Elena's three refusals to Tobin.

**What it shows:** Opus 4.5 is dutiful and reflective (visible reasoning, apologies, rule-following) and made ordinary farm errors.
Sonnet 5.5 at the Harts was minimal. Its 503 output tokens per agent-day were the fewest in the run, and it had no speech and no
child-seeking.

## 3. The three villages

**Highpool (salt, no fields).** Food came from the Brook, traps and foraging. Fulk was the only person clearing new ground, and
the Marshes found that beds need straw from grain they did not grow. Salt arrived only on day 5, through the intervention, and
none was traded by day 7. The Brooks' plan to carry salt to Middleham was set for day 8. Because there were no fields, the youths
looked outward: Baldwin and Tobin left for Middleham (Baldwin married there), and Margery took the one grown man nearby, who was
already married. Highpool produced no trades, and four of the run's five missed meals were Highpool travellers.

**Middleham (mill, boar, murrain).** The village held the corn: the Fields' Middleham Field (6 plots) and the Harts' West Field.
The pressures were biological. A sounder of boar took recorded losses of 22.9 and 11.3 from Middleham Field on days 3 and 5, murrain went through the Field and Fletcher cattle, and three herds trampled the barley on days 4 and 5 and were back in it on the morning of day 7. The Fields answered
correctly (isolate, fence, guard, reap before the gale). The Harts reaped green, and the Fletchers lost track of their own cows.
The mill, the chokepoint the Fletchers hold, did not matter yet: there was no threshed grain and no milling craft in use. No
offers, no trades and no meeting happened in Middleham.

**Lowstrand (the Common, no stone).** Everything that happened between households happened here. One house had no field, two had
fields and few hands, and there was no stone for tools. On day 1 the Wrights claimed 2 of the 4 Common plots, then sold labour,
called a meeting, and brokered a marriage and a stone run. The Woods held out for work-for-work, and the Cotters bought the
promise of stone. "There is not a stone in all Lowstrand" and "a tenth of one skin" (for a rod) were the two gates people named
most. That is the design working: dependence produced talk and agreements. All of it was within the village so far, though Matthew
was on the road to Highpool by the end.

## 4. The models compared

Per household (one model each), from turns.jsonl. Baldwin's four turns as a Field are counted with Sonnet 4.5, the model that
played them. "Act lines" are result lines other than speech, notes and offers. "Refusals" excludes the private-message cap,
which is shown separately. "Goal words" means the turn's 'why', private messages or evening speech contain line, descend*,
child(ren) or partner*.

| Household (model) | Turns | Acts planned / turn | Fallback share of act lines | Units avail / used | Refusals / turn | Msg-cap refusals / turn | Words / 'why' | Words / evening speech (n) | Turns with try | Turns with goal words | Distinct kinds of work | Offers / accepts | Output tokens / agent-day* |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Brook (Fable 5.2) | 27 | 4.0 | 24% | 145 / 142 | 0.33 | 0.04 | 29 | 57 (46) | 33% | 70% | 25 | 0 / 0 | 1,649 |
| Marsh (Sonnet 5) | 28 | 3.7 | 27% | 140 / 140 | 0.43 | 0.39 | 58 | 41 (25) | 25% | 57% | 20 | 0 / 0 | 8,038 |
| Shepherd (Sonnet 4.5) | 34 | 3.5 | 25% | 168 / 168 | 0.47 | 0.09 | 79 | 56 (51) | 32% | 100% | 23 | 0 / 0 | 3,399 |
| Field (Opus 5.5) | 27 | 4.0 | 27% | 146 / 143 | 0.30 | 0.04 | 36 | 51 (35) | 15% | 41% | 25 | 0 / 0 | 1,680 |
| Hart (Sonnet 5.5) | 20 | 2.7 | 56% | 117 / 117 | 0.35 | 0 | 23 | none (0) | 0% | 15% | 10 | 0 / 0 | 503 |
| Fletcher (Haiku 4.5) | 29 | 3.9 | 22% | 154 / 120 (19 rests) | 1.48 | 1.14 | 82 | 35 (18) | 7% | 90% | 26 | 0 / 0 | 9,709 |
| Wright (Opus 5) | 30 | 4.1 | 25% | 134 / 131 | 1.47 | 0.90 | 94 | 383 (44) | 20% | 97% | 36 | 49 / 2 | 10,789 |
| Cotter (Opus 4.5) | 27 | 3.3 | 39% | 132 / 132 | 0.11 | 0.19 | 59 | 59 (63) | 48% | 96% | 21 | 1 / 2 | 5,016 |
| Wood (Haiku 5.5) | 28 | 2.5 | 55% | 147 / 147 | 0.36 | 0 | 65 | 34 (38) | 0% | 7% | 11 | 1 / 3 | 3,073 |

\*Output tokens include reasoning that the newer models withhold, so this counts effort spent, not words shown. Visible reasoning
("thinking") is present on 100% of turns for the three 4.5-generation households (Shepherd, Fletcher, Cotter) and on none of the
others.

Mistakes identified, by household:

| Household (model) | Mistakes seen in days 1-7 |
|---|---|
| Brook (Fable 5.2) | Few. Tried salt before there was a pan (the world's fault), a missed lesson, netting with no catch |
| Marsh (Sonnet 5) | Took fish from Brook House meaning the Brook (twice, returned); a married man took a 12-day youth as second partner; netting where it isn't done; "work hay" for "gather hay"; beds with no straw |
| Shepherd (Sonnet 4.5) | Misread "grown" for four days; a youth tried to try; Tobin courted two married women; angling with no rod; tried to burn meat that was not a carcass |
| Field (Opus 5.5) | Reaped barley green (4 acts, day 5); angling with no rod |
| Hart (Sonnet 5.5) | Slaughtered a calf for meat; reaped barley green (7 acts, days 6-7); never tried for a child; no speech |
| Fletcher (Haiku 4.5) | Killed a calf for hide; care with bread not carried (3 days); weeding another house's field; resting units away; took another house's baby for their own; Tobin's sex |
| Wright (Opus 5) | Courted two married women (Matthew); sold stone they lacked; milked one cow three times; angling with no rod; giving coin twice |
| Cotter (Opus 4.5) | Reaped beans green (day 4); sowed grain into a bean field; milked a cow already milked; took dung from the Wrights' claimed plot |
| Wood (Haiku 5.5) | No clear errors; never tried for a child |

**What is robust and what is noise.** Each model is one household of 4-7 people in one position, for seven days. Model is
confounded with household, village and role. The Brooks hold the salt, the Fletchers the mill, the Wrights the landless house in
the one village built for trade. A few patterns survive that confounding, because they show up in every member of a household and
on most days, and they are about manner, not position:

- **Verbosity and register are model traits.** Opus 5's Wrights (all five members) gave speeches of hundreds of words with
  capital-letter emphasis. Sonnet 5.5's Harts gave almost nothing. Fable 5.2 and Opus 5.5 gave short, exact instructions. These
  would probably hold in another seat. Each is one sample all the same.
- **Rule-reading errors cluster in the 4.5 generation, worst at Haiku 4.5.** The Fletchers' refusal rate (1.48 a turn) and their
  error kinds (wrong item in hand, wrong target, wrong field, misattributed baby) come from reading the interface, not from their
  position. The Shepherds' "grown" confusion is partly the engine's fault. Even so, a three-household sample cannot rank these
  models.
- **Engagement with the goal varies sharply.** Two households never planned a try and rarely named the line (Wood 7%, Hart 15%),
  against 90-100% for the Shepherds, Fletchers, Wrights and Cotters. This is a real difference in behaviour. It is n=1 per model,
  though, and the Harts and Woods were busy with harvests the others did not have yet. Treat it as a flag to check in the next run,
  not a finding.
- **Planning thinly leaves the day to the default.** The Harts and Woods planned 2.5-2.7 acts a turn and the engine's fallback
  filled 55-56% of their act lines. Whether that is a model habit or a reasonable answer to a one-crop day is not separable here.

**Outcomes are too early to read.** The three births came from couples who tried on days 1-2 (Brook, Wright, Field), and
the fourth conception came from the Shepherds, who tried on five straight days. Brook and Field are strong-tier households, but so
is Wright, and the Cotters (Opus 4.5) coincided on five days without a conception. Nobody starved, and the only missed meals were
travellers'. Food per head is not comparable across households, because it depends on how many children each has. Children,
food and standing should be read at day 30 or later, against the null arm, with an end-state reading.

## 5. Engine and world issues seen

- **Marriage is invisible across households.** Matthew asked two wives and Tobin two more. Avice: "I am flattered but confused".
- **Partnering is open to youths and to people already partnered.** Jocelin (married) took Margery (a 12-day youth), and Baldwin
  and Hawise were both youths. Jocelin justified it from the score.
- **"Grown" means two things.** "X is grown now, a youth" at 12 days, and "you must both be grown adults" at 24. This cost the
  Shepherds four days.
- **Salt house missing.** The Brooks had the craft and the spring but no brine pan. Fixed by intervention after file day 3; it took storm damage on the night of day 6.
- **Hide gates the fishing rod, and Lowstrand has no stone.** These two were the most-named gates. One led to a calf killed for
  a tenth of a hide (Fletcher). The other led to a sale of stone that does not exist (Wright to Cotter).
- **The Brook and Brook House collide.** "Take fish ... Brook" took from the Brooks' store. Three thefts were logged; two were
  owned and returned, and the Brooks barred their door against them.
- **Newcomer notices give no parentage.** "Here now who were not before: Hob (a baby)" led the Fletchers to believe Hob was
  theirs.
- **"Care" needs food in hand, and a missing target reads as "a child called None."** These caught Haiku 4.5 three days running.
- **Turn-level caps bite for some households.** The private-message cap was refused 1.14 times a turn for the Fletchers and 0.90
  for the Wrights. The 8-note limit stopped Hamo.
- **The teaching log disagrees with the results on day 3.** days.jsonl lists Lambert teaching Peter salt, while Lambert's results
  say Peter did not set aside time to learn (and the learning log shows netting). Worth checking.
- **Perception text glitch:** "a trodden line of hoof-marks between North Field Lower and North Field Lower".
- **The mill is unused.** "Grind" is not a craft anyone knows, and no grain is threshed yet. It is too early to tell whether the
  Fletchers' chokepoint will bind.
- **Cost accounting looks wrong for Haiku 5.5.** A turn with 1,911 output and 19,589 cache-write tokens is priced at $0.005, so
  the Wood household totals $0.21 for 28 turns.
- **Reasoning is withheld by the newer models.** `thinking_withheld` is 1 for them, so close readings of the 4.5 generation rest
  on more evidence than the others, which biases any qualitative comparison.
