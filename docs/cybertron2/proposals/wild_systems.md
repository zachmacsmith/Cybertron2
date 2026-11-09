# Proposal: wild systems, layered kinds that people can learn to read

**Status:** partly accepted: D2-197 (lead times in engine days), D2-198 (answers to scares by kind); the rest discussion (8 Nov).
Nothing built. **Owner:** 37.2; engine changes with 37.4.

**Affects:**
- spec/information/signs.md, noticing.md (readings by skill; misreads; lore as tested belief);
- spec/environment/ (the shared drivers; kinds);
- living_populations.md, wildlife.md, wild_plants.md, husbandry.md;
- the generator (where kinds live) and the climate (D4-109; the drivers).

**Builds on:**
- [node_ecology.md](node_ecology.md): the village's scale; the coarse layer and groups;
- 02zp parts one to three;
- the senses guide (guides/senses.md);
- a research note (games, folk ecological knowledge, real phenomena: sources at the end).

## Summary

Zach, 8 Nov:
- "Each should have different layers: some might be simple, some might have simple learnable rules, while others more niche rules,
  and maybe even the simpler ones have some deeper more nuance so experts actually have more to learn. And all of these should
  relate to signs."
- "These mechanics etc. are more important than realistic population dynamics."
- "Some patterns might only emerge in different conditions, which is where there can be interconnections."

The proposal has five parts:
1. **A few shared hidden drivers** that every kind reads and some write: accumulated warmth, ground wetness, frozen days, snow, mast,
   the rodent phase and the insect cohorts, together with people's own acts (stores, flocks, sowing, ploughing).
2. **Each kind is a small machine of layered rules on those drivers:**
   - a calendar;
   - a base rule anyone learns in a season or two;
   - conditional rules that show only in some conditions;
   - an expert layer;
   - a rare regime.

   The depth differs between kinds.
3. **Every hidden thing shows through at least two signs** with different lead times and noise. Each sign reads differently to a
   novice and an expert, and some can be misread.
4. **Lore is a belief people hold and test,** not a seeded truth. It can be right, half right or wrong in the ways real lore goes
   wrong, and feedback on it is delayed.
5. **Interconnections come from couplings through the shared drivers, and from lags, most of them inside a year:** nights to weeks
   (creatures answering what people did; a spell of weather and what follows it) and one season to the next. Lags of years come on
   top. The interesting patterns appear only when conditions line up.

**Population dynamics are a substrate:** plausible in tempo and direction, and simple. The design effort goes into the rules, signs
and couplings.

## 1. What this is for, and what was missing

**What the wild is for, for the society:**
1. **It pushes back.** It threatens crops, stores and beasts (node_ecology.md: the losses are the lever, and wild food is about a
   tenth of need).
2. **It responds.** What people do changes what it does: hunted woods empty, raiders return to unguarded fields, wolves turn to the
   fold.
3. **It is something to model.** It has hidden causes, lawful lags and readable signs, so people form theories, test them, teach
   them and argue about them. Knowledge is a form of progression (the Outer Wilds principle). A village that reads the land well does
   better.
4. **It differs** by place, season, year and era, which gives storing, guarding, trading and insurance their reasons.
5. **It is cheap and general:** kinds are data, the rules are few and consistent, and none is fragile to our guesses.

**What was missing in 02zp parts one to three:**
- realistic numbers with nothing to read;
- reservoirs that pushed back but had no structure;
- signs, expertise and lore designed as an afterthought.

**What the research says (§12):**
- learnable depth comes from few variables, many couplings and consistent rules;
- lags of one to two years are the main source of depth;
- every hidden variable needs signs;
- real ecological knowledge is layered: Liebenberg's simple, systematic and speculative tracking. Ju/'hoan trackers reconstructed
  98% of 569 tracks correctly, down to individual animals. And it goes wrong in known ways.

## 2. Principles

1. **Few shared drivers, many couplings, one rule each** (§3). A rule learned in one place holds in another, which is what makes it
   learnable.
2. **Every kind has layers, and they differ in depth** (§4). Simple kinds still have an expert nuance; deep kinds have conditional and
   rare layers.
3. **No hidden variable without signs.** Each has at least two, with different lead times: one suggestive, together diagnostic.
4. **Every leading sign pairs with an act that pays.** The senses guide measured that forecasts go unused when nothing can be done
   about them. If a sign predicts boar in the barley, there must be a watch, a fence or an early reaping to choose.
5. **A ladder of lags, most of them inside a year** (§8). Every kind of middling depth or more has fast arms (a night to a few
   weeks), seasonal arms (one season to the next) and only then slow arms (one to five years). The fast and seasonal arms are what a
   run lets people test by their own acts; the slow ones break naive correlation and reward memory, elders and records.
6. **Patterns that appear only under conditions.** The base rule holds most of the time, and named conditions flip it (hard winter,
   mast failure, drought, a wet flowering).
7. **Delayed and aggregated feedback.** A rule is tested over seasons, so wrong lore persists and right lore needs patience.
8. **Regional timing.** The same rule fires at different dates and thresholds from place to place: higher ground, the coast, the lee
   of hills. Lore carried from elsewhere arrives miscalibrated.
9. **Responses to people.** Creatures remember: wariness, habituation, learned raids. What people did last season changes this one.
10. **Mechanics before realism.** Tempo and direction are true to life; densities and food-web equations matter only as far as the
    behaviour needs them.

## 3. The shared drivers (hidden state that everything couples to)

Per region (the coarse areas: wild lands and the land around each village, node_ecology.md) and, where it matters, per parcel. Each
is a stock with one rule.

| Driver | What moves it | What reads it |
|---|---|---|
| **warmth** (accumulated warmth since spring; the season's mean) | the climate (D4-109) | phenology (budburst, flowering, spawning, insect hatching), the timing of every calendar kind |
| **wetness** (soil water; water level in fen and river) | rain against evaporation (the fast stocks, D4-113); drains and dams | slugs, the liver fluke's snails, ergot, fungi, eels and salmon (flow), wildfowl, frogs |
| **frozen run** (consecutive frozen days; snow lying) | the climate | hard-weather movements of fowl and plovers, deer and boar deaths, wolves' boldness, winter food buried |
| **mast** (flowering, then set, then fall, per wood type) | warmth and frost at flowering, the trees' own rhythm (2 to 5 years for oak, 5 to 10 for beech) | boar, mice, jays, woodpigeons, squirrels, pannage |
| **rodent phase** (vole and mouse numbers as a cycle state) | mast, the winter, predators, density | owls, kestrels, stoats, foxes, poultry losses in the low year |
| **insect cohorts** (chafer grubs by year; wasp queens; aphids) | warmth, the cohort's own clock (chafers 3 to 4 years in the soil) | rooks and starlings, crop and root damage, fruit, stings |
| **disease load** (per kind: mange, murrain and swine fever, fluke) | density, wetness, carcasses, contact | deaths, signs, outbreaks that travel |
| **people's acts** (stores, flocks out or folded, ploughing and sowing, waste, fences, watches, hunting pressure per wood) | the society | rats and mice, foxes, rooks, wireworm (old grass ploughed), raids, wariness |

**Every driver shows through signs.**
- **The climate's own values** are already sensed.
- **New for the other drivers:**
  - flowering on the oaks, and acorns set in August;
  - grubs in turned soil;
  - runways in the long grass and pellets of vole skulls;
  - the water mark on the bank;
  - slime trails;
  - black spurs in the rye.

## 4. A kind is a layered machine

Each kind is a data row built from general rules (§9). Its rules come in layers. The depth differs between kinds on purpose.

| Layer | What it is | Who learns it, and how |
|---|---|---|
| **L0 calendar** | when and where it is: arrives, breeds, hibernates, runs, rests | anyone, in a year; the seasons' signs |
| **L1 base rule** | the regularity that holds most of the time | anyone who pays attention for a season or two; lore states it |
| **L2 conditional** | a rule that shows only when named conditions line up (a mast failure, a hard winter, a wet flowering), often with a lag | the attentive, over years; easily over-generalised or missed; elders and records help |
| **L3 expert nuance** | the reading behind the sign: which animal, how old the trace, what the alarm call says, the exception to the rule | specialists by practice and teaching (trackers, shepherds, fowlers, beekeepers); hidden signs that reveal more to the skilled |
| **L4 rare regime** | the once-in-a-lifetime event (a vole plague, a dark year, rabies, a great freeze) with its own rules | elders' stories, half-remembered, sometimes wrong |

**Depth by kind** (examples; the full catalogue is in §6):
- **Shallow:** calendar markers such as swallows and the cuckoo (L0, with an L3 nuance: swallows low before rain).
- **Simple:** slugs, rats.
- **Middling:** wasps, eels, fox, red deer, roe.
- **Deep:** wild boar, wolves, the vole and owl system, the mast system, bees.

## 5. Kinds of wild system (archetypes)

These are not a list of animals: each is a way a wild thing can behave as a system. A kind may combine two.

| Archetype | How it behaves | Main timescale | Example kinds |
|---|---|---|---|
| **Calendar marker** | appears and leaves by warmth and day length; mostly a sign of the season | the year | swallows, cuckoo, frogspawn, toads at their pond, ivy flower |
| **Resident group with habits** | a herd, sounder or family with a home range, routes, wallows and rubs; shifts with disturbance; returns | days to years | red deer, roe, wild boar, badger sett |
| **Pulsed resource and cascade** | a resource that comes in some years; eaters boom and bust behind it, with lags | 1 to 5 years | oak and beech mast; hazel; the spruce and rowan failures that bring irruptions |
| **Cycler** | rises and falls on its own clock; predators follow a year behind | 3 to 4 years | voles with owls, kestrels and stoats; cockchafers with rooks |
| **Weather-triggered outbreak** | an insect or pest that booms when a weather threshold is passed, sometimes a year later | weeks to a year | wasps, slugs, aphids with ladybirds, leatherjackets, ergot, fungi |
| **Migrant and run** | arrives or moves on cues: frost, flow, darkness, tide, warmth | days to seasons | wildfowl, plovers and redwings in hard weather, woodcock, eels, salmon, elvers, starling roosts |
| **Territorial predator** | a pack, pair or single with a territory; hunger, learning, dispersal of the young; rare danger | seasons to years | wolves, foxes, eagles |
| **Colony and site** | an all-or-nothing site, held for generations, founded or abandoned on conditions | years to decades | heronry, rookery, warren, wild bee colony, badger sett |
| **Engineer** | changes the land others depend on | years to decades | beaver (ponds, fish, deadwood, meadow), boar (rooting), rabbits (turf), moles |
| **Follower of people** | thrives on what people store, waste and keep | seasons | rats and mice in stores, house sparrows, foxes at middens, rooks at the plough |
| **Disease and parasite** | hidden spread, density or wetness driven, late signs | seasons to years | fox mange, murrain and swine fever in boar and pigs, liver fluke in wet years, rabies (rare regime) |
| **Plant and fungus system** | slow change readable as the land's history and present | seasons to decades | bracken creep, nettles on old dung, fairy rings, ivy, mistletoe, fungal flushes |
| **Rumour from abroad** | something that happens elsewhere and may come | years | a locust plague, a cattle plague, wolves returning |

## 6. The catalogue (first set), by layer

Signs are in quotation marks as sketches (the senses guide's style, to be written properly). Below, "lead" means a sign comes before
the event; levers are what people can do.

### Wild boar (deep)
- **L0:** a sounder of sows and young holds a wood with wallows. Boars live apart and join in the rut (November and December).
  Farrowing comes in spring.
- **L1:** boar root the ground and come at night to fields beside their wood, worst when the corn is milk-ripe in summer.
  - Signs: "the turf by Oak Hanger turned over in long strips"; "a wallow churned fresh, mud rubbed high on the oaks". Lead: rooting
    nearer the field each night.
- **L2 (conditional):**
  - **Fast (nights to two weeks): the learned field.** Once a sounder has found a field it comes back each night until it is met. A
    watch or a scare turns it for a few nights; after a week or two of the same scare with no harm done, it learns the scare and
    comes anyway (it gets used to scares, D2-198). A new scare, a dog, or a boar killed resets it.
  - **Fast (days): a hard frost** seals the ground; the rooting stops and the boar go to the ricks and the clamps.
  - **Seasonal (the same autumn): mast or no mast.** When the acorns fall, the sounders stay in the oak woods and the fields are
    quiet; when they fail, the boar are in the stubbles, the late crops and the stores within weeks of the usual fall.
  - **Slow (a year): the two-year sequence.** After a mast autumn the sows breed well, and the next year has more boar. If the next
    autumn's mast fails as well, those boar come for the crops and the stores: the worst case.
  - A mild winter and mast together: a boom. A hard winter without mast: deaths.
  - Signs: rooting nearer the field each night (lead, nights); the oaks heavy with flowers in spring, then acorns setting (lead, a
    season); no acorns under the oaks in October (lead, weeks); many piglets in spring (lead, a year).
- **L3 (expert):** the boar-wise read from the same signs:
  - sounder size from prints and lie-ups;
  - the old sow that leads the raids;
  - a wounded boar's danger;
  - the gap in the hedge they use.

  A watch at the right gap on the right nights catches them; a watch elsewhere wastes the night.
- **L4 (rare):** murrain (swine fever) runs through the boar and the village's pigs alike, carried by carcasses, worst in cold
  weather. Signs: dead boar in the wood; pigs off their food.
- **Levers:** watch the field; fence or hedge the gap; hunt (a crew and dogs; rights permitting); reap early; pannage of the village's
  own pigs in mast years.
- **Couplings:** mast; the warmth and frost of flowering; the village's crops and pigs; wolves (piglets).

### The mast system (oak and beech; deep; a pulsed resource)
- **L0:** acorns fall from September to November; beech nuts in the beech woods.
- **L1:** some years the woods are thick with mast, and some years bare.
- **L2:**
  - **The same autumn (weeks):** a fall of mast draws boar, deer, jays and woodpigeons into the oak and beech woods, and the fields
    are quieter that autumn. A failure sends them out: the boar to the fields, the woodpigeons onto the young winter corn and the
    greens, the mice into the houses and stores.
  - **The trees' rhythm:** mast years come together across a region (oak every 2 to 5 years, beech every 5 to 10).
  - **Frost at flowering spoils a year.**
  - **What follows a mast year (the slow arm):**
    - pannage pays;
    - jays and woodpigeons gorge, and bramblings flock to the beech;
    - mice and voles winter well and peak the next summer;
    - owls and foxes breed well that year;
    - the year after, the rodents crash, and the hungry predators turn to the hens and to nests.
- **L3:** the expert reads the spring flowering and August set; knows which woods mast together; leaches acorns for famine food (a
  knack). They know the "berries mean a hard winter" saying is false: a heavy crop reflects the spring just past.
- **L4:** a run of three failed years, when pigs and boar starve and people too in a dearth.
- **Signs:**
  - "the oaks hang heavy with catkins" (spring, lead);
  - "acorns setting thick on the old oaks" (August, lead);
  - "the ground under the oaks is brown with acorns; jays everywhere";
  - "mouse runs and gnawed nuts everywhere in the hedge bottoms" (the next spring).
- **Levers:** pannage (a right); gather; leach; time pig-keeping; expect boar.

### Voles, owls and the hungry year (deep; a cycler)
- **L0:** voles in the long grass; owls hoot in autumn and winter.
- **L1:** some years the grass is full of voles and the owls and kestrels thrive.
- **L2:**
  - **Within the year (a season):** numbers climb through summer and peak in autumn; a wet, cold winter knocks them down by spring.
    Owls and kestrels move to where the voles are within weeks, so the hunting birds show a rise before the damage does.
  - **Fast (days):** a flood or the mowing of the long grass drives the voles to the banks, the ricks and the barns.
  - **The cycle (the slow arm):** 3 to 4 years, set ahead by a mast year and held back by a hard winter.
  - **The predators lag:** they breed in the rise and peak and fail in the low year.
  - **The low year:** the hungry predators turn to the hens and the lambs, and owls go quiet.
  - **The peak year:** voles strip the grass and the young crops.
- **L3:**
  - an owl pellet full of vole skulls means a vole year;
  - kestrels hovering everywhere mean the same;
  - short-eared owls appearing mean a peak;
  - the owls' silence means the crash.
- **L4:** a vole plague, when meadow and stored grain are gnawed through.
- **Signs:**
  - "runways and clipped grass in the long grass by the dyke" (lead);
  - "the kestrels hang over every field";
  - "no owl has called these three nights";
  - "pellets thick with little skulls under the barn beam".
- **Levers:** protect the stores; shut the hens in during the low year; cut the long grass; value the owls (a barn owl as vermin
  control).

### Cockchafers and rooks (middling; a cycler)
- **L0:** May bugs fly at dusk in late April and May.
- **L1:** some springs they come in clouds and strip the oaks.
- **L2:**
  - **Fast (days):** the flight comes on the first warm, still evenings of late April and May; a cold spell stops it. The plough
    turns up the grubs, and rooks and starlings clear a field in a few days.
  - **Seasonal:** a wet September lets the crane flies lay; their grubs (leatherjackets) eat the spring corn and the grass roots in
    April.
  - **The cohort clock (the slow arm):** 3 to 4 years in the soil, then a "chafer year", which differs between parishes.
  - **The grubs' damage:** they eat the roots of grass and corn, worst the year after a flight.
  - **The rooks:** they follow the plough when grubs are thick.
- **L3:** count the grubs in a turned spadeful to forecast the flight. Rooks working a pasture show grubs beneath (leatherjackets
  after a wet autumn look the same: telling them apart is a skill).
- **L4:** a great chafer year once in a generation, when they were brought to court in old tales.
- **Signs:** "fat white grubs in every spadeful" (lead, a year or more ahead); "the rooks working the low pasture"; "beetles battering
  at the shutters at dusk"; "the oaks by the green stripped bare".
- **Levers:** plough and let the rooks in; hand-pick; leave the field fallow; value the rookery.

### Wasps (middling; a weather-triggered outbreak)
- **L0:** wasps in late summer at the fruit and the honey.
- **L1:** some Augusts are thick with wasps.
- **L2 (all inside one year):**
  - **Fast (days):** a hot spell in late summer brings them to the fruit and the hives within days; the first frosts end them.
  - **The trigger (a season ahead):** a warm, dry spring lets the queens found nests (many queens in April lead), and the swarming peak comes in August
    and September when the colonies turn to sugar.
  - **The exception:** a hot, dry summer that starves their prey can work against them.
  - **The illusion:** a late spring shifts the peak into September and looks like a boom.
- **L3:** find the nest by the line of wasps; take it at night; protect the hives and the drying fruit.
- **Signs:** "queen wasps at every sunny wall" (April, lead); "the fallen apples crawling with wasps"; "a nest humming in the bank".
- **Levers:** take the nests; harvest fruit early; guard the hives.

### Slugs and thrushes (simple)
- **L0:** slugs in damp places.
- **L1:** a wet, mild spring brings slugs, and the seedlings go.
- **L2:**
  - **Fast (a night or two):** the first rain after a dry spell brings them out that night, and the seedlings go within days; a dry
    week stops them.
  - **Seasonal:** a mild, wet winter before means more. Flooding kills the eggs. The damage is patchy within a field.
- **L3:** thrushes' anvil stones show snails; sow later after a wet winter.
- **Signs:** "slime trails silver across the seed bed" (lead); "the young beans shredded in the low corner".
- **Levers:** sow later; burn or till the stubble; ducks in the garden.

### Aphids and ladybirds (simple to middling; a cycle inside a season)
- **L0:** blackfly on the beans, greenfly on the roses and the hops, in early summer.
- **L1:** a warm spell brings the aphids.
- **L2:**
  - **The predators lag by one to two weeks:** ladybirds, hoverfly grubs and lacewings build up on the aphids and clear them, so a
    bad week is usually followed by a better one.
  - **A cold snap** after the aphids hatch stalls the predators more than the aphids.
  - **Ants** tending the aphids keep the ladybirds off.
- **L3:** pinch out the bean tops when the first blackfly gather. Leave the ladybirds: their spiny grey larvae look like a pest and
  are killed by those who do not know them (a misread that prolongs the outbreak).
- **Signs:** "the bean tops black with fly"; "ladybirds thick on the beans now, and grey spiny grubs among them"; "ants running up
  the stems".
- **Levers:** pinch the tops; sow early; leave the predators; wash or smoke the plants.

### Red deer (middling; a resident group)
- **L0:** a herd in its wood. Stags roar in the autumn rut (late September and October). Antlers are cast in March and April. Calves
  are born in June.
- **L1:** deer come out at dusk to graze the edges and the young corn.
- **L2:**
  - **The rut:** rutting stags are bold and careless.
  - **A hard winter:** deer come down to the ricks and strip bark, and most deaths fall between February and April, the weak calves
    and spent stags first.
  - **Hunting (days to weeks):** a hunted wood empties by day within days, the deer moving to its far edge or the next wood. They
    drift back after some weeks of quiet; a drive keeps them away longer than a stalk.
  - **Snow (days):** the first lying snow brings them to the ricks and the young trees.
- **L3:**
  - age and sex from the slot (the track);
  - a fraying stag's rub;
  - the rack through the hedge they use;
  - reading where the herd will be from wind and disturbance;
  - a cast antler is worth finding.
- **Signs:** "fresh slots in the ride"; "the stags are roaring in the north wood"; "bark stripped from the young ash"; "a rack broken
  through the thorn hedge".
- **Levers:** stalk (skill); a drive (a crew); fence the ricks; leave the wood quiet to keep them; rights.

### Roe deer (middling; a niche rule)
- **L0:** single animals and small family groups in thicket and edge.
- **L1:** they browse buds and young growth.
- **L2:** they rut in July and August, not autumn (delayed implantation), so kids come in May. Anyone carrying red deer lore gets this
  wrong.
- **L3:** roe "rings" trampled round a bush in July; the barking alarm call; the doe's fawn hidden in long grass (the mower finds it).
- **Signs:** "a ring trodden round the hawthorn in the meadow"; "a roe barking in the dusk".
- **Levers:** stalk; protect the coppice regrowth.

### Wolves (deep; a territorial predator)
- **L0:** a pack holds a large territory around deep wood; howling in winter; pups in a den in spring.
- **L1:** wolves follow the deer; they keep away from people.
- **L2 (each condition flips the rule):**
  - **Fast (days): a fold that fed them.** After a kill at a fold, the pack comes back within days, and keeps coming until the fold
    is closed or watched or a wolf is hurt.
  - **Seasonal: deer hunted out in autumn** make the pack bold at the folds that same winter.
  - **Hunger:** deer hunted out or scarce, crusted snow, or a hard late winter make them bold at the fold.
  - **Dispersing young (autumn to spring)** cross farmland: a lone wolf where none lived, and more likely to take sheep.
  - **A fold left open** is surplus-killed.
  - **Summer:** pups at the den and flocks on open pasture.
  - **Wolves returning after years away** take more stock than long-settled packs.
- **L3:**
  - wolf track against dog track (often misread);
  - scat with hair and bone;
  - ravens over a kill;
  - deer and stock bunching nervously;
  - the howl's direction;
  - which yearling is the danger.
- **L4:** a rabid wolf, the rare true danger to people (a bite, madness).
- **Signs:** "great tracks in the snow along the wood edge, larger than any dog's" (which a novice may read as a dog's); "ravens
  wheeling over the north wood"; "the sheep bunched and restless at dusk"; "howling from the high wood, nearer than last week".
- **Levers:** fold and watch; dogs; a drive or a bounty (collective action); don't hunt out the deer; children not herding alone.

### Fox (middling)
- **L0:** pairs scream in December and January; cubs come in March; the young disperse in autumn.
- **L1:** foxes take hens left out at night.
- **L2:**
  - **Fast (the next night):** a fox that found the henhouse open comes back the next night, and the next, to the same place.
  - **Seasonal, April to June:** provisioning cubs is the peak for lambs and poultry.
  - **Vole crash years:** more losses.
  - **Surplus killing:** a fox in a henhouse kills all.
  - **Mange:** it can sweep through crowded foxes.
- **L3:** an earth with cub debris (control in spring beats a winter cull); musky scent; birds mobbing a hidden fox.
- **Signs:** "feathers and a musky stink by the hen house"; "the blackbirds chinking at the hedge, something low moving"; "a fox
  scratching and bald at the tail".
- **Levers:** shut the hens in; den control in spring; dogs; geese as watchers.

### Eels (middling; a run)
- **L0:** eels in the river, the fen and the meres all year.
- **L1:** in autumn the silver eels run downstream.
- **L2:** the run comes on dark, wet nights with rising water. A dry autumn holds it back. Moonlight slows it. Elvers come up on spring
  tides.
- **L3:** an "eel night", moonless and stormy after a dry spell; where to set the traps on the weir; smoking to keep.
- **Signs:** "the first heavy rain after the dry weeks: the river rising and dark" (lead); "the traps full at the weir this morning".
- **Levers:** traps and the weir (rights; the upstream and downstream commons, water_and_preservation.md); smoke them.

### Salmon (middling; a run)
- **L0:** salmon in the big rivers in autumn.
- **L1:** they run up on a rising river after rain.
- **L2:**
  - **Low, warm water** holds them in the estuary.
  - **Below about 3 °C** they barely move.
  - **A weir** blocks those above.
- **L3:** fresh-run fish with sea lice; the pool they lie in; reading the spate as it clears.
- **Signs:** "the river clearing after the spate, salmon showing in the long pool".
- **Levers:** spear, net, weir; rights; leaving a gap in the weir.

### Hard weather and the birds (middling; migrants)
- **L0:** winter flocks of duck, geese, plovers, redwings and fieldfares.
- **L1:** frost brings the birds onto the fen and the fields.
- **L2:**
  - **Before a freeze,** daytime flocks of plovers and redwings flying west or south lead it. That is a forecast.
  - **About a week into a freeze,** birds weaken and come tame.
  - **Woodcock** arrive with easterly winds in November ("the woodcock moon": the moon is incidental).
- **L3:**
  - shooting or netting weak birds in a long freeze empties next year's flocks (restraint);
  - snow shows every track;
  - waxwings and crossbills irrupt only after the berry or cone crop fails elsewhere, and are taken as omens ("plague birds", wrong
    lore).
- **Signs:** "lines of plovers going west all day, high and fast" (lead, a day or two); "the fowl crowded on the last open water";
  "birds so weak you could pick them up".
- **Levers:** fowl (nets and decoys); restraint in a long freeze; read the forecast.

### Bees (deep)
- **L0:** wild colonies in hollow trees; hives in skeps.
- **L1:** swarms come in May and June; honey follows the flowers.
- **L2:**
  - **Swarms:** congestion and the coming flow set them off. "A swarm in May is worth a load of hay ... in July not worth a fly", the
    rhyme counting the flow left.
  - **The flows:** the June gap, then lime in July and heather in August.
  - **A cold, wet summer** means no surplus.
- **L3:**
  - queen cells sealed in the comb (a week before the swarm);
  - scouts at empty hollows;
  - bees bearding at the entrance;
  - piping;
  - take honey without starving the colony;
  - wasps rob a weak hive in a wasp year.
- **Signs:** "bees hanging in a beard from the skep's mouth" (lead, days); "a swarm in the crab apple by the lane"; "the heather is
  loud with bees".
- **Levers:** take swarms; place hives by the lime and the heather; protect from wasps; honey and wax (seals, candles).

### Heronry (simple to middling; colony)
- **L0:** the herons nest in the same tall trees year after year (for generations).
- **L1:** herons fish the river and the mere.
- **L2:**
  - **A hard winter** crashes their numbers, and they take years to recover.
  - **Disturbance in spring** can make them abandon the site.
- **L3:** the heronry's size shows the fish; a heronry is a lord's pride (and a feast).
- **Signs:** "the herons are back at the tall elms by the mere"; "fewer nests this spring than last".
- **Levers:** leave them in spring; claim them.

### Beaver (deep; engineer; rare in the era)
- **L0:** a family's lodge on a slow brook with willow and aspen.
- **L1:** they fell trees and dam the brook.
- **L2:**
  - **Behind the dam:** the pond holds water through a dry summer, cuts floods by about a third, and holds more fish.
  - **Flooded trees** die to standing deadwood (woodpeckers), and the pond later silts to meadow.
  - **The cost:** their dams flood the low meadow.
- **L3:** pencil-point stumps; scent mounds; the pelt and castoreum (trade); trapping empties a slow-breeding family for good.
- **Signs:** "trees cut to points by the brook"; "the low meadow is under water again behind a dam of sticks".
- **Levers:** trap (fur); break the dam or let it stand; rights.

### Followers of people (simple; with an expert layer)
- **Rats and mice:**
  - L1: rats come to stores.
  - L2: within weeks of the harvest coming in, rats and mice move from the hedges to the barns; cats or a terrier clear a barn in
    weeks. A mild winter and full stores breed them; a mast failure brings mice in.
  - L3: staddle stones, stone floors and cats.
  - Signs: "droppings and gnawed sacks in the granary".
- **Rooks:**
  - L1: rooks follow the plough.
  - L2: they mean grubs (good) but also pull the young corn (bad): bird-scaring as children's work.
  - L3: a rookery's size shows the grubs.
- **Wireworm:**
  - L1: ploughed old grass grows a poor second crop.
  - L2: larvae eat the buried turf first, so the second year suffers, for up to four years (the slow arm). Within the season, the
    damage shows within weeks of sowing as thin yellow patches; autumn ploughing exposes the grubs to the rooks, and a dry spring
    lessens it.
  - L3: break old grass with a fallow or a different crop.
  - Signs: "thin patches in the barley on the old pasture, yellow wiry grubs at the roots".

### Fields and grain (simple to deep; plant systems)
- **Ergot:**
  - L1: black spurs in the rye.
  - L2: a cool, wet, cloudy flowering on moist ground; the sickness comes from the year's grain, eaten through the winter after.
  - L3: pick out the spurs; rye on wet ground is the risk; St Anthony's fire.
  - Sign: "black horns among the rye ears".
- **Liver fluke (the rot):**
  - L1: sheep on wet ground sicken and die in winter.
  - L2 (seasonal): a wet summer and autumn breeds the mud snails; sheep pick up the fluke on wet grass in late summer and autumn and
    sicken over the next two to three months, so the rot comes in the winter after a wet year.
  - L3: keep the sheep off the wet meadows in a wet autumn; swelling under the jaw and pale eyes show it; a slaughtered sheep's liver
    shows the flukes.
  - Sign: "the ewes from the low meadow thin, swollen under the jaw".
- **Fungi:**
  - L1: mushrooms after rain in late summer and autumn.
  - L2: a soaking rain on warm ground, then a week or two.
  - L3: which are deadly (knowledge as safety); fairy rings mark old pasture.
- **Bracken:**
  - L1: bracken takes abandoned grazing.
  - L2: cattle trample it and sheep do not.
  - L3: it is toxic to stock, and cut for bedding and potash.

### Calendar markers (shallow, with a twist)
- **Frogspawn and toads:**
  - L0: spawn on the first mild, wet nights (earlier on the coast, later on the hills).
  - L3: toads always return to their own pond.
- **Swallows:**
  - L0: they arrive in April and gather in September.
  - L1: they fly low before rain. The cause is real: insects fly low in humid air.
- **Cuckoo:** L0: around mid-April.
- **Oak and ash:**
  - L0: the leafing order varies.
  - Lore that is a reading, not a forecast: "oak before ash, in for a splash". The order shows a warm spring, but predicts no summer
    rain.
- **Uses:** markers tell the season's progress. Lore drawn from them is the classic case of true signs and false forecasts.

### Brown bear (deep; hibernator; wildwood era and rare)
- **L0:** sleeps in a den through winter; wakes hungry in spring; fattens on fruit and nuts in autumn.
- **L1:** keeps to the deep wood.
- **L2:**
  - **After a poor autumn** (fruit and mast failed) and **a hard, late winter,** it wakes thin and comes to the hives, the calves and
    carrion in late spring.
  - **A sow with cubs** is dangerous.
- **L3:** tracks; claw marks on trees; overturned stones; the den.
- **L4:** a legendary bear (D2-195).
- **Signs:** "great claw marks on the beech by the ford"; "the hives by the wood smashed open".
- **Levers:** guard the hives in late spring; a hunt (a crew; very dangerous).

### Rumours from abroad (rare regime)
- **Examples:** locust plagues from the east (1693, 1747 to 1749), a cattle plague, wolves come back.
- **How it works:** travellers' talk, sometimes true, sometimes not. A plague that comes is a regime of its own.

## 7. Interconnections: patterns that appear only when conditions line up

These are the patterns the world is for: each needs two or more kinds, the drivers and often people. They are grouped by lag (§8);
most are inside a year.

**Fast (a night to a few weeks):**

| Pattern | Chain | When it shows | What a village sees |
|---|---|---|---|
| **The learned field** | a sounder finds a field → comes nightly → a watch turns it for a few nights → it learns the watch | any summer by a wood | a contest of watch against habit; a new scare or a dog pays |
| **A fold that fed** | a kill at an open fold → the pack returns within days | an open fold in wolf country | repeated losses until the fold is closed or watched |
| **Rain after drought** | slugs out that night; eels run on the dark wet nights; salmon up on the spate; mushrooms a week or two later | a dry spell broken | seedlings lost, traps full, mushrooms |
| **The first hard frost** | plovers move ahead of it; frozen ground sends boar to the stores and deer to the ricks; fowl weak a week in; wolves bolder | each winter's first long freeze | game for the taking, stores and ricks raided |
| **Aphid and ladybird** | a warm spell → aphids → predators one to two weeks later → the aphids crash | each early summer | a bad week, then a better one; killing the ladybird grubs prolongs it |
| **Harvest in** | full barns → rats and mice in from the hedges → cats or terriers | each autumn | gnawed sacks unless there are cats or staddles |
| **The hunted wood** | deer hunted hard → they leave the wood → the wolves turn to the folds | a village hunting hard in autumn | fewer deer, then wolves at the fold that winter |

**Seasonal (one season to the next):**

| Pattern | Chain | When it shows | What a village sees |
|---|---|---|---|
| **Mast or no mast** | mast falls → the beasts stay in the woods; it fails → boar, woodpigeons and mice out to the fields and stores | each autumn | a quiet autumn or a raided one |
| **Wet autumn, hungry spring** | a wet September → leatherjackets → spring corn eaten; a wet summer → fluke → sheep rot in winter | a wet late summer and autumn | thin spring corn; ewes dying in winter |
| **Wasp and bee year** | a warm, dry spring → many queens → a wasp August → weak hives robbed | a warm spring | less honey; stings at the fruit |
| **Wet flowering** | a wet June → ergot at the harvest → sickness from the new bread | a wet June | black spurs in the rye; St Anthony's fire |
| **The bear's spring** | a poor autumn + a hard, late winter → a thin bear at the hives and calves | wildwood, rare | smashed hives |

**Slow (a year or more), on top of the faster arms:**

| Pattern | Chain | When it shows | What a village sees |
|---|---|---|---|
| **The mast cascade** | mast year → boar breed, mice winter well → next summer rodent peak, owls and foxes breed well → the year after: crash, predators turn to hens and nests; boar raid if mast fails | a mast year followed by a failure | two good years for pigs and owls, then the worst year for hens and the barley |
| **The hungry gap for predators** | the vole crash year | every 3 to 4 years | owls silent, foxes and stoats at the hens |
| **Chafer year** | cohort clock + warm May evenings | every 3 to 4 years in a parish | stripped oaks, then root damage next year; rooks feast |
| **Ploughing old grass** | turf ploughed → wireworm in the second year → rooks | when people plough grass | a poor second crop after a good first |
| **The hard winter's tail** | a long freeze → the heronry crashes and recovers over years | a great freeze | a quiet heronry for years |
| **The beaver's brook** | lodge and dam → pond → fish and fowl, flooded meadow, deadwood | where beavers live | more fish and fowl, less hay |
| **Two villages, one weather** | the climate's shared fields (D4-109) | always | neighbours share bad years; lore from the hills miscalibrated in the vale |

## 8. Lags and timescales: what a run can see

Zach, 8 Nov: "I want some lags less than years. Just years is probably too long."

The engine's year is 24 to 40 days, and a run is 6 to 48 days. At Y = 32 a run spans about a fifth of a year to a year and a half,
so a lag of years is seen at most once in a run, and usually not at all.

**The ladder** (engine days at Y = 32, where one engine day stands for about 11 real days):

| Arm | Real lag | Engine days | Examples | In a run? |
|---|---|---|---|---|
| **fast** | a night to two weeks | 1 to 2 | the learned field; a fold that fed; a hunted wood emptying; rain after drought; the first hard frost; a swarm after sealed queen cells | every run, many times |
| **short** | two weeks to two months | 2 to 5 | aphids and ladybirds; the harvest in and the rats; mushrooms after rain; deer drifting back to a quiet wood | every run |
| **seasonal** | a season | 5 to 12 | a wet September to April's leatherjackets; a warm April to August's wasps; a wet June to the ergot; fluke to the winter's rot; mast or no mast; a poor autumn to the bear's spring | most runs, once to a few times |
| **yearly** | one to two years | 30 to 60 | more boar after a mast autumn; the mast cascade; wireworm's second year | long runs only; otherwise lore and seeded history |
| **cycles** | three to five years | 100 to 160 | voles, chafers | lore and the generator's history |
| **decades** | | | beavers' ponds, bracken, wolves returning, rare regimes | the generator's history; long cheap runs |

**The rule:** every kind of middling depth or more has at least one fast or short arm and one seasonal arm, each with a sign and a
lever. Slow arms come on top, never alone. Most fast arms are creatures answering people: learning a field, a scare, a fold, a hunted
wood. Those are the loops people can test by their own acts inside a run, which is what makes the land something to model and not
only to watch.

**Compressed time.** At Y = 32 a real week is about two thirds of an engine day. Read straight from the scaling principle
(node_ecology.md), a sign that leads its event by a few real nights (rooting nearer the field, plovers ahead of a freeze, queen cells
before a swarm) falls into the same engine day as the event and leads nothing. The proposal: **lead times and creature memory are
set in engine days, never less than one,** not scaled from real days; stocks and rates keep the scaling principle. This departs from
the scaling principle on purpose (principle 10). Decided: D2-197.

Depth beyond a run's length reaches people as **lore and history**: what the elders say happened, which may be wrong, and the world's
seeded state (a chafer year is due; the boar boomed last year).

## 9. Signs, reading and lore: what the engine needs (improvements)

**What exists:** the one noticing rule with bundles across senses; `hidden` signs with taught and untaught factors; lore lines seeded
to groups (D4-105).

**What this design needs:**

1. **Readings by skill.** A sign has a reading per level, following Liebenberg:
   - simple: "tracks";
   - systematic: "a sounder of five, sows and young";
   - speculative: "the old sow that leads them; they will come by the thorn gap tonight".

   The engine chooses the reading from the reader's skill in the matching craft (tracking, shepherding, fowling, beekeeping). Today
   only the chance of noticing differs.
2. **Misreads.** Some signs have a likely wrong reading for the untaught: a wolf's track read as a dog's, an old track as fresh,
   leatherjackets as chafer grubs. The truth stays in the state, and the person holds a belief that may be wrong (D4-6: beliefs with a
   date).
3. **Traces age and weather.** Crisp, softened, rained on; snow shows everything and rain erases it. The trace's age is part of what
   an expert reads.
4. **Leading signs as state.** Flowering and set, grubs, queens, runways, flocks moving west: each is the visible face of a driver
   (§3). Each one pairs with an act that pays (principle 4).
5. **Lore as tested belief:**
   - **Writing a rule:** a person can hold one ("after a mast year the boar come for the barley").
   - **Feedback:** the engine keeps a tally of the cases the person saw that fit or broke it, shown later in their own terms ("you have
     seen it hold three times and fail once"). Feedback is delayed and aggregated: no truth from above.
   - **Passing it on:** rules travel by telling and teaching, carrying who said them.
   - **Seeded lore** includes the classic ways lore goes wrong:
     - a true sign with a false forecast (oak and ash);
     - a false cause (the woodcock moon);
     - lore from another place (timing off);
     - ambiguous wording ("till May be out");
     - a rule that held before the land changed.
6. **Creature memory.** Wariness by wood and by weapon, learned raid routes, a fold once raided, a field found. This is state the
   engine does not hold today. It builds and fades over engine days (D2-197).
7. **Answers to scares differ by kind** (D2-198; Zach, 8 Nov: "not all creatures should get used to scares. Some of them should just
   get scared off"):

   | Answer | What happens | Kinds |
   |---|---|---|
   | **gets used to it** | the scare works for a few days, then less, then not at all; a new scare works again | wild boar, woodpigeons, rooks, red deer at the ricks |
   | **scared off** | the scare drives them off for some days; they come back, and the same scare works again | roe, hares, wildfowl, fox, wolves while the fold is kept, a bear (except a hungry one in spring) |
   | **leaves for good** | a scare at the wrong time drives them off for years | a heronry in spring, a beaver family trapped, a bear's den disturbed |
   | **does not answer** | scares do nothing; only traps, cats, stores and timing | rats and mice, voles, insects, slugs |

   Real harm (a beast killed or hurt, a dog that bites) works on every kind and makes it wary of that place for longer than a scare.
   What this gives people: against the kinds that get used to scares, a watch must be varied or backed by harm; against the kinds
   that are scared off, a steady watch is enough but must be kept up; against those that leave for good, restraint; against those
   that do not answer, other levers altogether. Which kind is which is itself something to learn, and lore carried from one kind
   to another goes wrong ("the scarecrow kept the hares off, so it will keep the boar off").

## 10. Representation and general rules

- **Two layers** (node_ecology.md):
  - **A coarse ecology per area:** each kind's numbers, the drivers, simple tempo-true dynamics.
  - **Near people,** the kinds that have groups (herds, sounders, packs, colonies) condense into named groups with places and habits.
  - **Outbreak kinds** (insects, slugs, voles, disease) stay area-level, with signs in each parcel.
  - **Calendar kinds** are timed signs.
  - **Bulk food** stays as parcel stocks.
- **Each kind is a data row built from a small set of general rules,** each written once:
  1. a **calendar** by warmth and day length (with regional offsets);
  2. **thresholds and runs** on a driver (a frozen run of N days; warmth over T; wetness over W);
  3. **pulses and lags,** counted in engine days from one day upward (the mast's fall empties the fields within weeks; a resource
     in year t raises breeding in t+1);
  4. **cycles** (a cohort or density clock);
  5. **feeding** on a food or a driver (including people's crops, stores and beasts);
  6. **group behaviour** (home range, routes, raids by night, a fold tested, avoidance and habituation as memory that builds and
     fades over days to weeks);
  7. **movement** (stay, shift, leave, return, disperse, migrate in and out, run along the river chain);
  8. **colony and site** (held, founded, abandoned on conditions);
  9. **engineering** (writes a driver or the land: water level, turf, deadwood);
  10. **disease** (load, spread by contact and carcass, outbreak);
  11. **signs**, with readings by skill and misreads;
  12. **danger** (D2-193).
- **No kind has code of its own.**

## 11. How it will be tested

- **Relevance:** each kind moves some household's food, work, safety or plans by about 10% in some year (node_ecology.md).
- **Inference by skill:** a scripted reader at each skill level predicts raids, runs, outbreaks and good years from signs. Two gaps
  must hold:
  - better than the base rate for all readers;
  - the expert clearly better than the novice.

  If not, the signs are noise or the layers are hollow.
- **Lags a run can see:** in a run of 12 engine days, each kind of middling depth or more shows at least one fast or short arm,
  and a household that changes what it does (a watch, a new scare, a closed fold, a quiet wood) sees the outcome change within the
  run.
- **Conditions matter:** over 10 generated years per world, a good share of the conditional layers (L2) actually show, and they differ
  between worlds and eras.
- **Lore errors persist and can be corrected:** seeded wrong lore survives a few seasons of weak feedback, and a careful reader can
  overturn it.
- **Diversity across the year:** each season holds several distinct patterns to read, with no long stretch where nothing differs.
- **Consistency:** watched and unwatched outcomes match, and groups condense without exploits (node_ecology.md).
- **Then an LLM probe:** do agents notice, form rules, teach them and act on them?

## 12. Research grounding

- **Games:**
  - Breath of the Wild's "chemistry engine": few elements, consistent rules, multiplicative play.
  - Rain World's creatures with needs and offscreen simplification.
  - Dwarf Fortress's emergent chains (the drunk cats), and the need to check their sizes.
  - Caves of Qud's history retold as distorted lore.
  - RimWorld: readable simple systems; complexity no one sees is wasted.
  - Outer Wilds: knowledge as progression; a clockwork world.
  - Return of the Obra Dinn: inference from several weak clues, with confirmation delayed and grouped.
  - Koster: fun is learning patterns. Bushnell: easy to learn, hard to master.
- **Folk knowledge:**
  - phenology that shares a driver (accumulated warmth) predicts; long-range animal and plant lore mostly does not;
  - short-range sky signs work for 12 to 24 hours;
  - lore that is real but misexplained: the woodcock moon, plovers leading a freeze;
  - Liebenberg's three levels of tracking, and the Ju/'hoan trackers' 98%;
  - Jon Young on bird language;
  - Dreyfus and Klein on how expertise works;
  - Henrich on lore that works unexplained;
  - Berkes on lore learned in crises;
  - the ways lore fails: false cause, illusory correlation, calendar drift, changed land, imported lore, ambiguity, present read as
    forecast.
- **Ecology** (triggers, lags, conditions, signs as summarised in §6):
  - mast cascades (Ostfeld, Cary Institute);
  - Kielder vole cycles and owls;
  - cockchafer cohorts;
  - wasp years (Rothamsted);
  - slugs (AHDB);
  - ladybird lags;
  - eel run timing (flow, darkness);
  - salmon and river flow;
  - hard-weather birds (GWCT, JNCC);
  - wolf depredation by dispersers (Jutland);
  - boar damage at milk-ripe;
  - the Rum red deer;
  - bee swarming triggers;
  - fox predation and mange (Bristol);
  - beaver effects (Exeter);
  - heronries (BTO);
  - ergot;
  - wireworm.
- **Sources:** the research note's URLs, kept with this proposal's session note (02zp part four).

## 13. Waves: D2-192 compared, and the merged wave system (9 Nov)

Zach, 9 Nov: "Compare the D2-192 waves and wildlife to your current ones. They also considered how they sit in the supply chains /
economics etc. then decide a final current wave system and build the first wave."

**What each set of waves was built from:**

| | D2-192 (wildlife.md) | wild_systems.md (8 Nov) |
|---|---|---|
| **The question** | what the land gives, and who can take it | what the land does to a village, and what people can learn about it |
| **The test for going early** | its goods have a use now (food, hides for bedrolls, tents, packs, harness, rods), or it makes a pressure now | it moves some household's food or work by about 10%, it has a fast arm and a sign, and it adds a mechanic not yet tested |
| **What it builds** | techniques with skills (stalking, a boar hunt, snaring, eel traps, fowling, honey-gathering): specialisation and trades | signs read by skill, lore as tested belief, creature memory, answers to scares (D2-198) |
| **Economics** | goods and chains: meat, hide, fish, feathers, honey now; furs, wax, antler wait for clothing and documents; the writing chain (parchment, quills, ink, seals) | losses to crops, stores and beasts; the work of watching and guarding |
| **The commons and rights** | weirs and runs (upstream against downstream), forest law, swans, wolf bounties | the forest-law conflict (the lord's game eats the villagers' crops) |
| **Order** | wave 1 red deer, hare, trout, eel, salmon, wildfowl, raven; wave 2 wolf, boar, fox, bees; wave 3 beaver, otter, marten, bear, falcon, swan; later rats, rabbits, pigeons | A boar and mast, fox, wildfowl, eels, slugs, wasps, voles; then stores, beasts, disease, colonies, rare |

**What each misses:**
- **D2-192** has no pests at all before "later". Rats in the stores and birds at the corn act in every village and were about 5% of
  need each in node_ecology.md. And the boar, the strongest pressure at village scale (02zp parts three and five), comes only in wave 2.
- **wild_systems.md** gives almost nothing a use. Slugs, wasps and voles give no goods, and the prototype built no techniques. A kind
  that only takes makes losses but no trades, chains or specialists, and scenario_design asks for dependence.

**The merged rule for going early.** A kind goes early if it meets two of these three tests, and each wave as a whole meets all three:
1. **pressure:** it moves food or work by about 10% somewhere, sometimes;
2. **use:** its goods have a use now, or it needs a skill, gear or a crew (a trade);
3. **reading:** it has a fast arm and leading signs that pay.

Each wave also adds one mechanic the earlier waves lack, and its kinds live in some places and not others.

**The waves:**

| Wave | Kinds | Pressure | Use (goods, techniques, chains) | New mechanics | Where |
|---|---|---|---|---|---|
| **1. The wood's edge, the river and the barn** | wild boar with the mast; red deer; hare; eels; wildfowl; rats and mice; birds at the corn (woodpigeons, rooks, sparrows) | boar and deer in the crops, deer at the ricks; rats in the stores; birds at the seed and the ripening corn | meat, fat and hide (hides into the built bedrolls, tents, packs); smoked eels and fowl for the lean season; feathers and down; stalking, a boar hunt (crew, D2-193), snaring, eel traps and a crew at the weir, fowling; cats and staddle stones; bird-scaring as children's work | groups that set out and come back; loads; a run; a flock; a pulse; signs read by skill; D2-197 leads; D2-198 answers (boar, deer at the ricks and birds get used to scares; hares, fowl and deer in a hunted wood are scared off; rats and eels do not answer); forest law and the weir as rights (D2-194) | boar and deer by big woods; eels by rivers; fowl by fen and water; hares on open land; rats and birds wherever there are stores and fields |
| **2. The fold and the hungry year** | wolves; fox with lambs and poultry; voles with owls and kestrels; ravens; hounds (D2-196) | beasts at the fold, lambs and hens | pelts; hounds as trained beasts; a drive and a bounty | chains between kinds (a hunted-out wood sends wolves to the fold; a vole crash sends the fox to the hens); danger to people; collective action against a common threat | wolves by deep wood and by era; the fox nearly everywhere, densest at wood edges; voles in rough grass |
| **3. The weather year** | slugs; wasps with wild bees; aphids and ladybirds; leatherjackets, chafers and wireworm with rooks; ergot; fungi; calendar markers | seedlings, fruit, honey, roots; ergot in the bread | honey (and wax, waiting for documents and light); mushrooms as knowledge that keeps people safe (wildlife.md §11) | outbreaks by soil and weather; true signs with false forecasts (oak and ash); seeded wrong lore | slugs on heavy wet soils; wasps where it is warm, by banks and wood edges; bees by old wood, heather and lime |
| **4. What travels** | murrain and swine fever (boar and pigs), liver fluke (sheep), fox mange; rumours from abroad | herds lost | | spread between villages by contact and carcass as well as shared weather; late signs; quarantine as a collective choice | by density, wetness and contact |
| **5. Prestige, furs and the land that changes** | beaver, otter, pine marten, falcon (hawks, D2-196), swan, heronry, brown bear; legendary individuals (D2-195); rare regimes | | furs, castoreum, a trained hawk, a claimed bird; waits for demand for furs, wax and antler (clothing, documents) as D2-192 said | leaving for good (D2-198); a kind that changes the land (the beaver's dam); restraint over years | slow brooks, cliffs, wildwood; by era |

**Kept from D2-192:** red deer, hare, eels and wildfowl in the first wave; the techniques and their skills; the goods-have-a-use rule
for furs and wax; the river commons; hounds with the wolves and hawks with the falcon.

**Changed:**
- **Boar moves up to wave 1.** It is the strongest pressure, and its mast pulse drives other kinds.
- **Rats and birds at the corn come into wave 1** from "later". They are the kinds every village meets.
- **Trout and salmon stay on the fish stock and its run that the engine already has** (the water pack), so nothing new is built for
  them in wave 1. The salmon's upstream-downstream rules come with the river commons.
- **The raven moves to wave 2,** as the sign of a kill or a carcass, with the wolves.
- **Wild bees move to wave 3,** with the wasps that rob them.

**Status:** chosen by 37.2 at Zach's request (9 Nov). It amends D2-192's order, so it is recorded as a decision when Zach confirms it
(open question 8).

## 14. How it fits the engine (9 Nov)

**Nothing of this is in the engine yet.** The prototype (02zp part five) and the wave 1 build (02zp part six) are models in the
session notes. Code under `cybertron2/` is 37.4's (CLAUDE.md).

**What the engine has that this builds on:**
- a single `game` stock on each forest parcel (renewal `threshold`), taken by the `hunt` technique;
- sign rows with `knack` and `eye` (skill-gated noticing), read through `readable(row, know)`;
- lore lines seeded to groups (D4-105);
- the climate by place and day (D4-109, D4-111);
- the land fields per parcel (D4-112, D4-113);
- fish with a periodic run;
- packs (D4-104).

**What it needs** (wild_systems.md §9 and §10):
- a population layer per area with groups condensed near people (node_ecology.md);
- the five general rules, with kinds as data rows on them;
- creature memory;
- readings by skill (today only the chance of noticing differs);
- traces that age;
- acts: watch with a scare at a place, scare birds, fold, pen, cats, staddles, a crew at the weir.

Moving it into the engine is for 37.4, by agreement on the board.

## Open questions (for Zach)

1. The approach: a few shared drivers; kinds as layered rule machines with depth that differs; signs with readings by skill;
   lore as tested belief; population dynamics as a simple substrate?
2. The engine improvements in §9: readings by skill, misreads, traces that age, leading signs as state, lore as held and tallied
   belief, creature memory. All of them, or which first?
3. The first set to build:
   - the mast system with boar, the strongest single chain;
   - hard weather with the birds;
   - voles and owls;
   - eels;
   - wasps and slugs;
   - the fox.

   Deer, wolves and bees as groups next; beaver and bear as era or rare.
4. Rare regimes (rabies, murrain, a vole plague, a locust rumour): in, as lore and rare events?
5. How much seeded lore should be wrong, and in which ways?
6. ~~Compressed time~~: decided, D2-197 (lead times and creature memory in engine days, never less than one).
7. The fox fails the relevance test at village scale (02zp §25). Keep it as a simple kind (shut the hens; den control in a hungry
   spring), or join it to the lambs at lambing so that it matters?
8. The merged wave system (§13): confirm it as a decision amending D2-192's order?
9. Moving the general rules into the engine (§14): when, and with 37.4 on the board?

## History

- 8 Nov: proposed after Zach asked for kinds with layers of learnability, all tied to signs, with mechanics before realistic
  population dynamics, conditional patterns and interconnections. Grounded in a research note on games, folk ecological knowledge
  and real phenomena.
- 8 Nov: after Zach's point that lags of years are too long ("I want some lags less than years"), a ladder of lags (§8): every
  middling or deep kind now has fast (nights to weeks) and seasonal arms, with the yearly lags on top. Fast arms added to boar, the
  mast, voles, chafers, wasps, slugs, red deer, wolves, fox, rats and wireworm; new entries for aphids and ladybirds (a predator lag
  of one to two weeks) and liver fluke (a wet autumn to the winter's rot); §7 grouped by lag; compressed time as open question 6.
- 8 Nov: Zach decided open question 6 ("yeah set lead times in engine days"): D2-197. And "not all creatures should get used to
  scares. Some of them should just get scared off": D2-198, four answers to a scare by kind (§9 item 7). Status partly accepted.
- 9 Nov: a prototype at village scale (02zp part five: five generated worlds, the engine's climate, the first set as data on five
  general rules). Findings:
  - the expert reads better than the novice on every event; the gap is large where lore joins signs (eels, the mast, voles, freezes,
    slugs) and thin for boar and fox, whose strongest sign is yesterday's damage;
  - boar pass the relevance test by far, and their expert edge is D2-198's answer to scares more than the reading;
  - eels pass where there is a river (once the act the forecast pays for, a crew at the weir, was added); slugs pass in wet years;
    fowl only in the fen in a hard winter; wasps and voles barely; the fox fails;
  - about three kinds show a lead and its event in any 12-day window.

  Open question 7 added.
- 9 Nov: Zach asked for a comparison with D2-192's waves (which weighed supply chains and economics), a final wave system, and the
  first wave built with targeted LLM tests. Added §13 (the comparison; a merged rule for going early: pressure, use and reading; five
  waves, with boar, rats and birds at the corn moved into wave 1 beside D2-192's red deer, hare, eels and wildfowl) and §14 (how it
  fits the engine: nothing is in it yet). Open questions 8 and 9.
- 9 Nov: wave 1 built on the general rules (02zp part six: five rules with no kind named in their code; seven kinds as data with
  signs, goods and acts). Targeted LLM tests (Haiku and Sonnet, 28 runs, 704 calls):
  - models meet boar raids at the right gap with expert readings, and lose 20 to 25 food more with novice readings;
  - they over-watch: work about three times the scripted expert's;
  - they read eel nights well from prior knowledge; a seeded wrong saying costs them 16 to 31 food and is overturned only slowly;
  - they do not learn in two seasons that birds get used to a scarecrow while hares are scared off by it (D2-198).

- 10 Nov: §10's "no kind has code of its own" replaced by D2-203: each kind's behaviour is designed first and built as a
  module of its own, acting only through the animal interface and the engine's primitives (wild_behaviour.md). The rule had been
  meant to stop one-off handlers; in the build it flattened the kinds' behaviour into settings of one machine (02zq).

## Sources

- node_ecology.md;
- 02zp parts one to three;
- guides/senses.md;
- the engine's noticing rule, `hidden` signs and lore (D4-53, D4-75, D4-105);
- the climate (D4-109, D4-113);
- the research note (02zp part four, with URLs).
