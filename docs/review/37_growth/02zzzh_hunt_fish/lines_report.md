# Report: the founders' seeded lines for every built livelihood (thread W-105)

Build subagent of session 37.2, 23 to 24 Nov 2026, on branch `w105-lines` (worktree `/home/user/c2-lines`), from the brief
`lines_brief.md` beside this file and the coordinator's addition (build_gaps.md G60 to G63, G66). Not pushed, not merged.

**What was built.** u9 §5.5's templates for every built livelihood in `cybertron2/engine/founders.py` (farmer FA1 to FA11, herder
HE1 to HE8, hunter HU1 to HU8, salter SA6 and SA7, smith SM1 to SM6, miller MI1 to MI5, builder BU1 to BU8, woodsman WO1 to WO5,
basket maker BA1 to BA5, cord and nets CO1 to CO5, trader TR1 to TR4, cottager CT1 to CT4, the fisher's FI13 and FI14), a neighbour
line for each of the thirteen built livelihoods, and (G60 to G62) HH2, HH4 and PE3. Every figure, season, keeping time and place is
read at world build from the engine's tables or the world's state (the docstring of each template names what it reads). The fowler
and the tanner are untouched (D2-318, D2-327).

In `cybertron2/engine/livelihoods.py`: the holdings that are not buildings (u11 §2.1) join `HOLDINGS`: **fields** (FA9), **an ox
team** (two oxen with a plough and two harness held by the household: FA7) and **a herd** (beasts beyond a plough team: HE7), found by
`holdings_of` and kept in the fill's report (only buildings record a `keeper`); `livelihood_line` names them ("and you keep the ox
team"). Specialisms that wait on a build are flagged `built: False` and never drawn (hunter: dressing the kill; woodsman: the coppice;
basket maker: the withy bed). The rows name u9's ids where it puts them (below). The basket maker's capable craft `pack basket` is the
engine's `pack`.

The keeper dispatch (G63): `founders.wanted` gives each keeper the line `keeper_line(kind, livelihoods)` returns, from the household's
rows' `keeper_lines`, else `HOLDINGS[kind]["keeper_line"]`, so a mill's keeper gets MI3, an oven's MI5, a forge's SM4, an ox team's
FA7, fields' FA9, a herd's HE7 (a withy bed's BA5 when a world can hold one). All ten keeper lines are in `KEEPER` (protected, source
"a holding"). `SOURCE` covers every prefix. The holdings line (HL) names fields, the ox team and the herd, and gives the mill, oven and
forge their fact clauses (u9 §5.6). `lore.seed` no longer seeds the sowing lore a second time to a filled founder (FA1 and FA2 carry
it).

**Wiring added to `ROWS`:** salter broad SA7; smith specialisms `mining_and_charcoal` (SM5) and `fittings` (SM6); builder capable
BU4; woodsman broad WO5, charcoal WO3, coppice (waiting) WO4; basket maker the withy bed (waiting) BA4, BA5; cord and nets
`flax_and_linen` (CO3, CO4); trader `the_road` (TR3), `the_market` (TR4); cottager capable CT4. The FI and SA wiring is as it was.

**Tests** (`tests/test_cybertron2_lines.py`, 29): a mixed fixture village (Wendle, with Thorpe a day off and the Holt beyond),
thirteen households, one for each built livelihood and the trader also as a second living, filled through `livelihoods.fill`, holding
fields and an ox team, a herd and a cellar, a mill, an oven, a forge, a weir, a smokehouse, a salt house and a saltmarsh; every built
template fires on it and its figures are checked against the data it reads; a bare village where every conditional line drops
(reported in `skipped`, never a stand-in); every id `wanted` can produce, on the fixture and on Eelmouth, has a template (G66); each
holding's keeper gets its keeper line, and no one else renders it; every founder fits the cap; Eelmouth's lines are unchanged.

## Corrected to the engine's truth

Where u9's words are false against the engine the line says what the engine does. Design words, then the engine's fact.

| Line | u9's words | The engine | Where |
|---|---|---|---|
| FA3 | sown from the best ears "it bears better" | chosen seed ripens sooner (15%), no more yield | `data.py:568` (`select seed`, D2-65), PHYSICS `seed_selection` 0.85 |
| FA4 | "a hard frost takes what is still growing"; "sow nothing into frozen ground" | each frosty night takes a third of a tender crop; seed lying in cold ground is lost a little each night | `data.py:958-959` (`frost_loss` 0.3, `lie_loss` 0.08); `farm.py:100` |
| FA6 | a copper tool "does about twice the work" | reaps half as much again, fells twice; the plough breaks ground four times as fast as a hoe | `data.py:577`, `:512`, `:554`, `:557` |
| FA7 | "the byre in a frost" | no frost harm to beasts; they eat hay when the grass is gone, a fifth less in stalls | `farm.py:1465` (`_herds`), `data.py:340` (stalls fodder 0.8) |
| FA10 | grain "ground to meal" feeds half as far again; bread further | meal is the hand mill's (porridge only); the mill gives flour (1.0 against boiled grain's 0.7) | `data.py` ITEMS flour, meal, bread |
| FA11 | "a night's watch"; beasts trample "by night" | a watch by day or night (D2-320); herds are drawn to a ripe crop at any time | kinds NEAR_PEOPLE woodpigeon (`kinds.py:169`); HERDS draw, trample |
| HE1 | "Hay is cut in summer, and only then"; cattle "starve within days" | most in summer, half in spring, a third in autumn, none in winter; a beast dies after 4 hungry nights | `data.py:581`, `:965` |
| HE2 | strays "wander back to the common" | most walk home at dusk; on the road a beast may die or be lost | HERDS dusk, road |
| HE3 | wolves "in late winter and early spring; bring the beasts in at dusk and bar the byre" | all winter and the first days of spring; a byre does not keep wolves off, a fence round the ground or a watch turns them | `kinds.py:155`; `wild.py:1984-1995` |
| HE4 | a beast with the murrain "must be kept off shared grass" | it goes worst where herds share grass, and comes from the deer | `kinds.py:775` |
| HE8 | a bundle of hay a night "in winter" | when there is no grass (grass first, then fodder), a fifth less in stalls | `farm.py:1465` |
| HU1 | snares in "pasture, meadow, heath and field edges"; a hare taken "before it spoils" | pasture, meadow, heath, field and scrub; an untended catch breaks free (1 in 3) or is taken by a fox or crows (1 in 4) | `methods.py:61`; `wild.py:921` |
| HU3 | "Deer are fattest in autumn"; "in spring the hinds have calves" | no seasonal fat in the state (dropped); the hinds calve early in summer; the rut is autumn's | `kinds.py:306`, `:311` |
| HU4 | "dried or salted it keeps far longer" | dried meat more than a year (salted dropped to keep 40 words) | `data.py:143` |
| HU6 | the wood "holds {game} in autumn" | holds game (no seasonal reading of a wood's game) | parcel `state.game` |
| HU7 | snares from cord "or a thong of rawhide that rots on a wet night"; it "moves when the run goes cold" | cord only, about 200 a kilo; a set snare lost or torn one night in six; a run snared hard goes cold | `gear.py:80`, `:107` |
| SA7 | "in winter they give little" | none in winter (40% spring, 20% autumn) | `data.py:723` |
| SM1 | "Charcoal burns hotter than timber" | at the anvil a sack smelts as much as six loads of timber (hearths burn by mass) | `data.py:746`, `:764` |
| SM2 | a copper tool "about twice a crude one's work" | half as much again, twice at felling; it lasts four times as long | `data.py:577`, `:512`; ITEMS life 40, 10 |
| SM3 | "tries alone get one only so far, and the rest is taught" | practice alone reaches known, taking twice as many tries (D2-326) | `learning.py:40` (`ALONE` 2.0) |
| SM4 | "an anvil, a hearth and bellows" | an anvil and bellows on its hearth | `data.py:327` (anvil needs hearth) |
| SM5 | "{ore_in} of ore" | 3 units of 3 kg: 9 kilos; mining wants a tool | `data.py:764`, `:544` |
| SM6 | "{farmer}'s plough share" | the plough (its making takes copper); the mill wheel added (its materials take copper) | `data.py:748`, `:335` |
| NB-SM | "want charcoal and grain" | want charcoal (the row's needs) | ROWS smith depends |
| MI1 | "flour keeps as grain does" | flour about a season, grain more than a year, bread a night or two | `data.py:138-143` |
| MI2 | "idle in spring" | dropped (no state says so); the harvest season is read: summer | `farm.season_run` |
| MI5 | "{oven_batch} loaves" | 100 kilos of flour into bread (bread by weight) | `data.py:705` |
| BU1 | "Wattle cracks on cold nights" | every house wears with the weather, wattle fastest, worst in frost, wind and snow | `data.py:923` (wear minor, weather) |
| BU4 | "and it stands longer; a room thrown up wears faster" | dropped: no build quality in the engine; the speed is D2-324's work x skill (built) | `verbs.py:273` |
| BU8 | stone walls "want their footings on dry ground" | dropped (no footings; damp is a store's spoiling by the house's level); added: an oven stands only in a stone house | `stores.py:286`; `data.py:323` |
| WO1 | "the dead wood once gathered is gone" | it comes back slowly as the trees shed it | `forests.py:64` |
| WO2 | "the smith and the salter want it, and little else does" | the salter's pan burns firewood; a hearth burns charcoal too, a sack as long as four bundles | `data.py:728`, `:910` |
| WO5 | the buyer "takes firewood and charcoal for grain" | the price dropped (no line states one); names the holding's fuel | ROWS; `boil salt`, `smelt` |
| CO1 | nettles "in late summer" | most in summer and autumn, three quarters in spring, a quarter in winter | `data.py:539` |
| CO2 | "A close of flax gives the cord a whole fishing village needs" | flax as a strip up to a quarter of a plot, tiring the ground as barley does | CROPS flax (strip 0.25, takes 0.15) |
| CO4 | "dressed and spun in winter, when other work is thin" | under a roof, any season; retted a night in water or three on the grass | `process.py:49`; `data.py:751` |
| CO5, NB-CO | nets needed "every few years"; "fishers and fowlers" | a net rots in about 16 nights in the water (barking waits on tanning, D2-329); fowlers deferred | `gear.py:100` |
| TR1 | "after {season}" | dropped (no seasonal surplus in the state) | |
| TR3 | "{landmark} is a place to stop the night" | a landmark on the road (landmarks are not shelters) | world `roads` |
| TR4 | "grain and fish are scarce everywhere by late winter" | dropped; the sources of salt, ore and stone are read from the world | parcel states |
| CT1, CT3 | "a cottage and a garden"; "a cow or a pig ... and a garden of beans" | no garden lot in the engine; the common's grass and wild food | |
| CT2 | "a day's work earns a meal or more" | dropped: a price | |
| NB-HE | "milk in summer and oxen to lend" | milk (calves come all year, `farm._herds`); oxen only if held | `farm.py:1465` |
| NB-FA, NB-CT | "the big field"; "they spin in winter" | the household's own field; dropped (not a fact of the household) | |
| FI12 | rendered for anyone asked | reads its keeper, as FI17 and SA4 do | `founders.py` FI12 |
| BS2 | 41 words with both its fields and wolves clauses | drops "through winter" only then (Eelmouth's text unchanged) | |

## Dropped for want of a built thing

Each template is written and returns None until the engine has what it reads; its condition checks the engine, so the line fires
once the thing is built.

| Line | Waits on | What the engine lacks |
|---|---|---|
| FI13 | bone | nothing gives bone (no technique's gives, no kill's goods) |
| FI14 | dressing the catch, bait | no technique dresses fish or baits with offal |
| HU8 | dressing the kill (u3) | no `dress the kill` technique; its specialism is flagged waiting |
| BU5 | seasoning (W-76) | no seasoned timber |
| WO3 | the burn as a process | charcoal is one act, not a process |
| WO4 | the coppice (W-76) | no coppice kind or cycle; its specialism waits |
| BA2 | hurdles' uses | hurdles are made and rot but nothing folds beasts or fences with them |
| BA4, BA5 | the withy bed (U7, stage 5; G18) | no bed work, no record; its specialism waits |
| CO3 | retting's fouling (U10; G79) | retting fouls no water |
| PE3 (often) | history dated in world years | the generator dates hard winters from its tree's years, so several can fall in one world year (runs_high: days -6, -4, -3, -2); PE3 then drops |

The cellar is not made a holding (its keeper line would be HE5, a dairy line, and the gate's P2 would refuse it); HE5 reads the
household's cellar directly. The gate check (`landgen/gate_check.py`) still sees building holdings only: fields, the ox team and the
herd pass its P1 and P2 by.

## Lines as rendered on the fixture

### Farmer (u9 §5.5.2)

| Id | On the fixture (who) | Reads | Condition |
|---|---|---|---|
| FA1 | "Barley does best sown in spring, and well early in summer or late in winter; sown at other times it comes up poor or not at all." (Ralph) | lore.sowing_times (farm.season_run) | [fields in the village] |
| FA2 | "Rye does best sown late in autumn, and well in summer or early in autumn, and wants a winter in the ground; beans do best sown early in summer, and well in spring." (Ralph) | lore.sowing_times; CROPS needs_winter | [fields in the village] |
| FA3 | "A plot wants about 16 kilos of seed; seed chosen from the best ears of a ripe crop ripens sooner. Seed eaten in a hungry spring is next year's harvest gone." (Ralph) | PHYSICS farming plot_seed; select seed, seed_selection |  |
| FA4 | "Rye wants a winter in the ground and bears poor without one; barley and beans are tender: each frosty night takes a third of what is growing. Seed sown in cold ground lies, and is lost a little each night." (Emma) | CROPS hardy, needs_winter; farming frost_loss, lie_loss |  |
| FA5 | "Ripe corn will not wait: left standing more than 2 days it sheds and rots, a quarter each night, and ears reaped too soon give only green grain, fit for fodder." (Ralph) | farming window, rot; CROPS grain green |  |
| FA6 | "A crude tool reaps and fells; a copper one from the smith reaps half as much again and fells twice as much. Oxen and a plough break the ground four times as fast as a hoe." (Agnes) | reap, fell tools; plough, hoe plots |  |
| FA7 | "Our oxen plough a plot in 4 units where a hoe takes 16; they eat hay when the grass is gone, a fifth less in stalls, and the plough and harness wear with use." (Agnes) | plough, hoe plots; FITTINGS stalls fodder | [keeps an ox team] (protected) |
| FA8 | "Barley and rye sown year on year tires the ground; beans give it back. A field rested, or dunged, bears better." (Ralph) | CROPS takes, restores |  |
| FA9 | "The Long Field stands in barley, beans last year, its soil rich; the Infield lies empty, rested last year, its soil tired." (Ralph) | the fields' state.crop, last_crop, fertility (farm.soil_word) | [keeps fields] (protected) |
| FA10 | "Grain ground to flour feeds about half as far again as boiled grain, and bread further; Wendle Mill grinds for those who bring it grain." (Ralph) | ITEMS food (flour, grain, bread); mills by road days | [a mill within a day] |
| FA11 | "Woodpigeons come down on the sowing in spring and again in autumn; clappers or a watch keep them off. Beasts through an open gate are drawn to a ripe crop and trample it." (Walter) | kinds.NEAR_PEOPLE woodpigeon seasons |  |

### Herder (§5.5.3)

| Id | On the fixture (who) | Reads | Condition |
|---|---|---|---|
| HE1 | "Hay is cut most in summer, half as much in spring, a third as much in autumn, none in winter; beasts on bare winter grass without it begin to die after about 4 hungry nights." (Robert) | hay by_season; cattle starve_nights |  |
| HE2 | "Cattle stray through an open gate, and most walk home at dusk; a beast that strays onto the road may die there or be lost." (Robert) | cattle stray; HERDS dusk, road |  |
| HE3 | "The wolves come to the herds all winter and into the first days of spring; a fence round the beasts' ground, or a watch over them by night, turns most." (Cecily) | NEAR_PEOPLE wolf herd seasons; wild fence/watch turning | [wolves in the region] |
| HE4 | "Pasture and meadow feed beasts best, fen half as well, heath and moor less; the murrain goes worst where herds share the grass, and comes from the deer." (Robert) | cattle grazing; DISEASES murrain |  |
| HE5 | "Milk will not keep past the day it is drawn; 20 kilos of it with a little salt make about 3 of cheese in a cellar, and cheese keeps two seasons." (Mabel) | cheese inputs, gives; cheese keeping | [a cellar in the household] |
| HE6 | "Without the plough oxen, 2 to a yoke, there is no ploughing, and without the bull no calves; meat from them is eaten once." (Robert) | plough animals; breeding in farm._herds | [holds oxen or a bull] |
| HE7 | "Our herd is 4 cows, a bull and a calf, kept on the Common; 2 of the cows are in milk." (Robert) | the herd record | [keeps a herd] (protected) |
| HE8 | "A beast eats about a bundle of hay a night when there is no grass, a fifth less in stalls: our 6 beasts want about 48 bundles for the 8 nights of winter." (Geoffrey) | a head's fodder a night; ITEMS hay fodder; stalls fodder; season_days | [holds a herd] |

### Hunter and trapper (§5.5.4)

| Id | On the fixture (who) | Reads | Condition |
|---|---|---|---|
| HU1 | "Snares go on the runs in pasture, meadow, heath, field and scrub, never in the wood; a hare snared in the night is best taken at first light, before it breaks free or a fox or the crows take it." (Godfrey) | snare covers; wild.SNARE_NIGHT |  |
| HU2 | "Game near home grows wary when it is hunted hard; fresh ground a day or two out gives far more, but one carries home only about 10 kilos." (Godfrey) | carry foot |  |
| HU3 | "In autumn the stags roar at dusk in the rut, bold and careless and easier to come on; early in summer the hinds drop their calves." (Ivo) | kinds.WHEN red deer rut, calving | [red deer in the region] |
| HU4 | "A kill left lying draws the wolf and, in a hungry spring, the bear: dress it and carry it in the same day. Fresh meat goes off in a night or two; dried it keeps more than a year." (Ivo) | carcass targets; meat, dried meat keeping | the wolf/bear clause [wolves; bears] |
| HU5 | "Stalking is slow work in wood and heath, downwind and close; a drive wants beaters and spears and is dangerous; one alone with a weapon takes what comes." (Godfrey) | stalk, drive, hunt the wild rows |  |
| HU6 | "The Holt, a day off, holds game; a camp there saves the walk home each night." (Godfrey) | other places' forest parcels with game | [a wood with game within 2 days] |
| HU7 | "Snares are twisted from a little cord, about 200 to a kilo; a set snare is lost or torn about one night in six, and a run snared hard goes cold." (Avice) | gear.RECIPES snares cord; LIVES snare torn |  |

### Salter, the missing rows (§5.5.6)

| Id | On the fixture (who) | Reads | Condition |
|---|---|---|---|
| SA6 | "Salt is heavy only in bulk: one carries about 10 kilos a day's walk on foot, 25 with a pack basket; Thorpe, a day off, has meat and hide and no salt." (Katherine) | carry foot; pack carry; reach; ROWS gives | [a village within 2 days with no salter] |
| SA7 | "The pans on Salt Marsh make salt in the sun: most in summer, about 4 in 10 as much in spring, a fifth as much in autumn, none in winter." (Oliver) | salt pan by_season | [holds saltmarsh] |

### Smith and miner (§5.5.7)

| Id | On the fixture (who) | Reads | Condition |
|---|---|---|---|
| SM1 | "Five loads of timber burnt slow in the wood make one sack of charcoal; at the anvil a sack of it smelts as much as six loads of timber." (Simon) | charcoal inputs; smelt fuel |  |
| SM2 | "A copper tool does half as much again as a crude one, twice as much at felling, and lasts four times as long; the plough, the salter's pan and the fishers' hooks all want copper." (Isabel) | tools; ITEMS life; plough, pan, hooks' copper |  |
| SM3 | "Smithing is skilled work: tries alone get one there in time, but take twice as many as with a teacher at the anvil." (Simon) | learning.cls; learning.ALONE |  |
| SM4 | "Our forge at the Forge has an anvil and bellows on its hearth; it burns charcoal by the sack, and holds 3 sacks now." (Simon) | the forge's fittings and stock | [keeps a forge] (protected) |
| SM5 | "Ore is dug where the rock shows it, at the Scar, and wants a tool; 9 kilos of ore and a sack of charcoal smelt to a kilo of copper at the anvil." (Alice) | seam parcels; smelt inputs; ITEMS weights | [a seam within 2 days] |
| SM6 | "The Brooks' pan, the Hobbs' plough, the Millers' mill wheel and the fishers' hooks are copper work: those who need them come to us." (Martin) | neighbours' holdings | [a household within a day wanting copper work] |

### Miller and baker (§5.5.8)

| Id | On the fixture (who) | Reads | Condition |
|---|---|---|---|
| MI1 | "Grain ground to flour feeds about half as far again as boiled grain, and bread further still; flour keeps about a season, grain more than a year, and bread goes off in a night or two." (William) | ITEMS food; flour, grain, bread keeping |  |
| MI2 | "The farm houses bring grain after the harvest, in summer; the mill is busiest then." (Roger) | harvest season (farm.season_run) |  |
| MI3 | "Our mill grinds up to 200 kilos of grain at a turn; the leat silts and wants clearing once a year, the stones dressing after about 2000 kilos ground. Both are sound as it stands." (William) | water mill grain; FITTINGS wear (wheel years, stones life); the building's worn | [keeps a mill] (protected) |
| MI4 | "Shut, the hatches hold the river: the wheel turns full, and half the fish going up are held below. Drawn, they let the fish by, and the wheel turns at half." (William) | WATER_WORKS mill stop, open_rate | [keeps a water mill on a run river] |
| MI5 | "Our oven bakes up to 100 kilos of flour into bread at a firing, with 3 bundles of firewood, and wants relining with stone after about 10 firings." (Matilda) | oven bread inputs; FITTINGS oven wear; reline oven inputs | [keeps an oven] (protected) |

### Builder (§5.5.9)

| Id | On the fixture (who) | Reads | Condition |
|---|---|---|---|
| BU1 | "Every house wears with the weather, wattle fastest, and worst in frost, wind and snow; unmended it falls to ruin. Mending wants timber, or stone for a stone house: keep some back from the fire." (John) | PHYSICS wear minor, weather; buildings.repair_need |  |
| BU2 | "Felling with a tool gives far more than gathering dead wood by hand; a crude tool wants only a little wood and stone." (John) | fell, firewood; crude tool inputs |  |
| BU3 | "A full store takes no more, and what will not go in lies at the door; at Wright House the bins hold about 300 kilos." (Thomas) | stores.SPACES, stores._cap | [the house has a store] |
| BU4 | "One who knows the work raises a room in about half the days one new to it takes." (Thomas) | D2-324 build work x skill; class_range |  |
| BU6 | "The mill's wheel, the plough and the handcart are a wright's work; the Carters, the Hobbs and the Millers need them." (John) | trades of water wheel, plough, handcart; neighbours' holdings | [a household within a day with a wheel, plough or cart] |
| BU7 | "Stone lies only where the rock shows, at the Scar; quarrying wants a tool." (Margaret) | rock parcels with quarry; quarry tools | [rock with a quarry within 2 days] |
| BU8 | "A hearth wants 20 stones and an oven 60, and an oven stands only in a stone house; stone walls wear about a tenth as fast as wattle." (Margaret) | FITTINGS hearth, oven stone, oven structure; wear minor |  |

### Woodsman (§5.5.10)

| Id | On the fixture (who) | Reads | Condition |
|---|---|---|---|
| WO1 | "Young growth cut in the Hanger comes again in a few years; dead wood once gathered comes back only slowly, as the old trees shed it." (Henry) | FORESTS kinds regrow; shed | [a wood in the village] |
| WO2 | "Five loads of timber burnt slow in the wood make a sack of charcoal; the smith wants it at the anvil, and a hearth burns a sack as long as four bundles of firewood." (Henry) | charcoal inputs; ITEMS heat |  |
| WO5 | "The Brooks here want firewood for the pan." (Henry) | neighbours' salt house / forge; boil salt, smelt fuel | [a salt house or forge within 2 days] |

### Basket maker (§5.5.11)

| Id | On the fixture (who) | Reads | Condition |
|---|---|---|---|
| BA1 | "Willow rods cut in winter, when the sap is down, give the most: about 8 in 10 as much in autumn, half as much in spring, a third as much in summer, and summer cutting harms the stools." (Adam) | cut withies by_season; WILLOW summer_harm |  |
| BA3 | "A creel carries the catch on the back, 5 kilos more than the hands; a pack basket carries about 25 kilos where hands carry 10." (Adam) | creel, pack carry; carry foot |  |

### Cord and nets (§5.5.12)

| Id | On the fixture (who) | Reads | Condition |
|---|---|---|---|
| CO1 | "Nettle and bast twisted into cord give most in summer and autumn, three quarters as much in spring, a quarter as much in winter; it is slow work, a kilo in about 4 days." (Richard) | twist cord base, by_season; PHYSICS units summer |  |
| CO2 | "Flax is sown in a strip of a field, up to a quarter of a plot, and pulled by the root; it tires the ground as barley does, and gives the fibre for cord." (Nicholas) | CROPS flax strip, takes | [fields in the village] |
| CO4 | "Pulled flax is retted a night in still water or 3 on the grass, then dressed and spun under a roof; about 8 kilos of retted flax make a kilo of cord." (Richard) | PROCESSES retting nights; dress and spin |  |
| CO5 | "A gill net wants a kilo of cord and many evenings' knotting; in the water it rots in about 16 nights, so the fishers want nets again and again." (Sarah) | gill nets cord; LIVES gill net rot |  |

### Trader (§5.5.14)

| Id | On the fixture (who) | Reads | Condition |
|---|---|---|---|
| TR1 | "Thorpe, a day off, has meat and hide, and lacks salt." (Richard) | reach; ROWS depends | [a village with households within 2 days] |
| TR2 | "A pack ox carries about 100 kilos where one on foot carries 10, but wants grazing on the way; a handcart carries about 125 on a road with a track, and is no use off one." (Bartholomew) | HERDS pack_ox; ITEMS handcart |  |
| TR3 | "The road to Thorpe is a day, the track along the river, with a ford on it." (Gilbert) | world roads | [a road from home] |
| TR4 | "Some goods are made in few places and wanted in all: salt, copper ore and stone only at Wendle." (Lucy) | parcels with brine/saltmarsh, seam, quarry | [a salt, ore or stone source in the world] |

### Cottager (§5.5.15)

| Id | On the fixture (who) | Reads | Condition |
|---|---|---|---|
| CT1 | "We hold a cottage and no field; we live by work for others, for food or coin, and by what Thorpe Common and the wild give." (Wat) | held fields; the common | [holds no field] |
| CT2 | "Hands are wanted at the busy times: the Haywards at haymaking in summer and the Hobbs at reaping in summer." (Wat) | neighbours' harvest, hay, eel seasons | [a neighbour with a busy season: fields, a herd, water, a mill] |
| CT3 | "What Thorpe Common gives, grass for a beast and wild food at its edges, sees us through when the work fails." (Maud) | the common | [an unheld pasture in the village] |
| CT4 | "In winter, when the days are short and work is thin, we spin and make baskets for those who will take them." (Maud) | dress and spin; gear basket; PHYSICS units |  |

### Head, people and holdings lines (G60 to G62; §5.3, §5.4, §5.6)

| Id | On the fixture (who) | Reads | Condition |
|---|---|---|---|
| HH2 | "Next year's 6 plots want about 96 kilos of seed. A rule can keep it back from the pot, and say what may be eaten first instead." (Ralph) | held fields' plots; plot_seed | [holds fields] |
| HH4 | "Grain on a floor or in sacks draws mice; in bins or on a granary floor fewer, and a cat or a barn owl keeps them down. The bins at Marsh House hold about 300 kilos." (Peter) | stores SPACES/CONTAINERS vermin; STORE_STOPS; _cap |  |
| PE3 | "I have seen 2 hard winters, the last of them last winter: the frost came early and the stores ran out." (Osbert) | history kind winter; born; season_days | [an elder; hard winters in their life, one a world year] |

### Neighbour lines

| Id | On the fixture |
|---|---|
| NB-basket maker | "The Willows cut the willow; they make traps, creels and baskets for those who need them." |
| NB-builder | "The Wrights build: a frame, a wheel or a hearth is their work." |
| NB-cord and nets | "The Ropers twist cord and knot nets; the fishers get their nets from them." |
| NB-cottager | "The Cotters work for whoever needs hands." |
| NB-farmer | "The Hobbs sow and reap the Long Field; they have grain after harvest and want hands at reaping." |
| NB-fisher | "The Marshs live by the Wend: they know when the eels run, and dry and salt the catch; in late autumn they have fish to spare." |
| NB-herder | "The Haywards keep their cattle on the Common; they have milk." |
| NB-hunter | "The Hunts hunt Thorpe Wood; they bring home meat and hides." |
| NB-miller | "The Millers keep Wendle Mill; bring them grain after harvest and they grind it." |
| NB-salter | "The Brooks boil salt at the spring; they want firewood for the pan." |
| NB-smith | "The Smiths work copper at their forge; they make tools and hooks, and want charcoal." |
| NB-trader | "Gilbert of the Carters carries between Wendle and Thorpe; ask them for what is not made here." |
| NB-woodsman | "The Woods work the wood; they have charcoal, timber and firewood." |

## The cap on the fixture (u9 §5.2; D2-308, D2-340)

Every founder fits 20 lines and 800 words with no line over 40 words; no set is over the cap after the last step (no gate refusal).
Two defaults were needed for that (questions 1 and 2 below): before them the farmer head (Ralph, expert in seed and harvest, keeper
of the fields) held 22 lines after the whole drop order, because his oxen-only plough team was also counted as a herd (HE7, now
fixed: question 3) and HH2 repeats FA3's seed figure.

| Founder | Household | Stage | Band (specialism) | Wanted | Seeded | Words | Drop steps taken |
|---|---|---|---|---|---|---|---|
| Katherine | Brook | adult | expert (carrying) | 30 | 18 | 582 | neighbours beyond one |
| Oliver | Brook | adult, head | expert (the_pan) | 43 | 20 | 627 | neighbours beyond one, HH5, HH4, HH8, broad lines of a second living beyond its first, BS9, BS7, BS6 |
| Osbert | Brook | elder | expert (salting) | 32 | 19 | 614 | neighbours beyond one |
| Petronel | Brook | youth | broad | 9 | 8 | 260 | none |
| Bartholomew | Carter | adult | capable | 27 | 13 | 400 | neighbours beyond one |
| Gilbert | Carter | adult, head | expert (the_road) | 36 | 20 | 620 | neighbours beyond one, HH5, HH4 |
| Lucy | Carter | adult | expert (the_market) | 28 | 15 | 455 | neighbours beyond one |
| Maud | Cotter | adult | capable | 30 | 17 | 506 | neighbours beyond one |
| Wat | Cotter | adult, head | broad | 36 | 20 | 624 | neighbours beyond one, HH5, HH4 |
| Cecily | Hayward | adult | capable | 28 | 15 | 470 | neighbours beyond one |
| Geoffrey | Hayward | adult | expert (hay_and_winter) | 27 | 14 | 445 | neighbours beyond one |
| Mabel | Hayward | adult | expert (dairy) | 29 | 17 | 532 | neighbours beyond one |
| Robert | Hayward | adult, head | expert (stock) | 39 | 20 | 627 | neighbours beyond one, HH5, HH4, HH8, BS9, BS7 |
| Agnes | Hobb | adult | expert (ploughman) | 32 | 20 | 662 | neighbours beyond one |
| Alan | Hobb | adult | broad | 27 | 14 | 464 | neighbours beyond one |
| Emma | Hobb | adult | capable | 29 | 16 | 535 | neighbours beyond one |
| Hugh | Hobb | youth | broad | 9 | 8 | 282 | none |
| Joan | Hobb | child | - | 2 | 2 | 64 | none |
| Ralph | Hobb | adult, head | expert (seed_and_harvest) | 41 | 20 | 636 | neighbours beyond one, HH5, HH4, HH8, capable lines a specialism repeats, BS9, BS7, BS6, the last neighbour line, BS8, when HH10 is held |
| Walter | Hobb | adult | expert (hedge_and_field) | 28 | 15 | 497 | neighbours beyond one |
| Avice | Hunt | adult | expert (snares) | 29 | 16 | 516 | neighbours beyond one |
| Godfrey | Hunt | adult, head | expert (stalking) | 38 | 20 | 627 | neighbours beyond one, HH5, HH4, HH8, BS9 |
| Ivo | Hunt | adult | capable | 29 | 15 | 489 | neighbours beyond one |
| Hawise | Marsh | adult | broad | 27 | 14 | 489 | neighbours beyond one |
| Nichola | Marsh | adult | expert (keeping) | 34 | 20 | 678 | neighbours beyond one, capable lines a specialism repeats, BS9 |
| Nigel | Marsh | youth | broad | 9 | 8 | 298 | none |
| Peter | Marsh | adult, head | expert (weir_and_nets) | 41 | 20 | 692 | neighbours beyond one, HH5, HH4, HH8, BS9, BS7, BS6, the last neighbour line, BS8, when HH10 is held |
| Matilda | Miller | adult | expert (the_oven) | 28 | 16 | 528 | neighbours beyond one |
| Roger | Miller | adult | capable | 27 | 13 | 426 | neighbours beyond one |
| William | Miller | adult, head | expert (the_mill) | 37 | 20 | 670 | neighbours beyond one, HH5, HH4, HH8, BS9 |
| Nicholas | Roper | adult | capable | 28 | 13 | 415 | neighbours beyond one |
| Richard | Roper | adult, head | expert (flax_and_linen) | 38 | 20 | 632 | neighbours beyond one, HH5, HH4, HH8 |
| Sarah | Roper | adult | expert (nets) | 28 | 15 | 488 | neighbours beyond one |
| Alice | Smith | adult | expert (mining_and_charcoal) | 28 | 16 | 498 | neighbours beyond one |
| Isabel | Smith | adult | capable | 27 | 14 | 434 | neighbours beyond one |
| Martin | Smith | adult | expert (fittings) | 26 | 13 | 400 | neighbours beyond one |
| Simon | Smith | adult, head | expert (smelting) | 37 | 20 | 631 | neighbours beyond one, HH5, HH4, HH8 |
| Adam | Willow | adult, head | expert (traps_and_creels) | 37 | 20 | 655 | neighbours beyond one, HH5, HH4 |
| Beatrice | Willow | adult | capable | 29 | 15 | 488 | neighbours beyond one |
| Edith | Wood | adult | capable | 29 | 16 | 493 | neighbours beyond one |
| Henry | Wood | adult, head | expert (charcoal) | 38 | 20 | 623 | neighbours beyond one, HH5, HH4, HH8 |
| John | Wright | adult, head | expert (wright) | 38 | 20 | 634 | neighbours beyond one, HH5, HH4, HH8 |
| Margaret | Wright | adult | expert (mason) | 30 | 17 | 525 | neighbours beyond one |
| Thomas | Wright | adult | capable | 29 | 14 | 437 | neighbours beyond one |

By role: heads reach 20 lines, taking the steps to HH8 or BS9 (with twelve neighbour households they drop eleven NB lines first); the
fisher and farmer heads with a protected keeper line and HH10 reach the last steps (BS6, the last neighbour line, BS8 when HH10 is
held). Experts who are not heads hold 13 to 20; capable members 13 to 17; broad adults 14; youths 8; a child 2.

## Eelmouth

Regenerating before the change was byte-identical. After it, `eelmouth.yaml`, `eelmouth_old.yaml`, `eelmouth_small.yaml` and
`eelmouth_small_old.yaml` are **byte-identical**: no seeded line changes for any person. FI13 and FI14 (the hand, rod and dressing
expert's) wait on bone and dressing, and no one in Eelmouth holds that specialism; the new NB lines are for livelihoods Eelmouth does
not have; SA7 drops (the Brooks hold a fen, not a saltmarsh); HH2 drops (no fields); HH4 renders for the three heads and is dropped
at its step after HH5, which each of them reaches, so their sets are as before. Only the two fill reports changed
(`eelmouth.report.json`, `eelmouth_old.report.json`): HH2 and SA7 now listed as skipped, HH4's step listed. A 4-day bot run of
Eelmouth (`--bots runs`) runs clean and its days are identical to the same run from `main` (Basilia, an infant, dies on day 1 in both).

## The suite
In six shards (`ls tests/test_cybertron2_*.py | split -n r/6`), after merging `main` into the branch: **858 passed, 2 skipped, 0
failed** (shards of 90, 146, 148, 169 with the 2 skips, 159 and 146), the 29 new tests among them. No model calls; the bot run
above is the only run.

## Questions for Zach (each with the default taken)

1. **Where the stores line (HH4) goes in the drop order.** u9 §5.2's order has no place for it; added to every head now that U5 is
   built, it pushes the heads at the cap over it. Default taken: HH4 drops right after HH5 (both describe what the store and the book
   already show). Recommendation: keep it; the alternative is to protect it and drop more base lines.
2. **FA3 when HH2 is held.** A farmer head expert in seed and harvest held 21 lines after the whole order. Default taken: step 5
   ("lines a more specific line repeats") also drops FA3 when HH2 is held (HH2 states the house's own plots' seed). Ralph ends at
   exactly 20 with every step taken: one more line for such a head (a second living, a marriage's lines) is a gate refusal.
   Recommendation: for heads with a protected keeper line, let BS1 or BS4 go before refusing.
3. **A herd of oxen alone is the ox team, not a herd.** Default taken: the herd holding needs cows, a bull or young; an oxen-only herd
   held with a plough and harness is only the ox team (FA7).
4. **The trader as a second living only ever gets TR1.** u11 says the trader is always a second living, and a second living's hands
   get only its `second` lines, so TR2 to TR4 (and NB-trader, keyed on the core living) reach no one unless a world makes the trader a
   core living, as the fixture's Carters are. Default taken: as built. Recommendation: the capable second hand gets the second
   living's capable line too, for rows marked "always second".
5. **Step 6 drops a second living's lines for anyone**, not only when a deeper band is held in the core (u9 §5.2's words): Katherine
   in Eelmouth, broad in both, loses them. Default taken: kept as built, so Eelmouth stays as it is. Recommendation: tighten it with
   the next Eelmouth remake.
6. **"In the region" reads the world file's `wild.kinds`.** Eelmouth's file names no kinds, so BS2's wolves clause, HE3, HU3 and HU4's
   wolf and bear never fire there although the wild pack may place wolves at run time. Default taken: as `_wolves` already reads.
   Recommendation: read the wild pack's placement at world build.
7. **The sowing lore for a filled founder.** `lore.seed` now leaves a filled founder's sowing lore to FA1 and FA2 (else a farmer held
   it twice); a filled founder of another livelihood who holds a field no longer gets it. Default taken: so.
8. **New specialisms in the rows**: the smith's `mining_and_charcoal` and `fittings`, cord and nets' `flax_and_linen`, the trader's
   `the_road` and `the_market` (u11 §1.2 names them); three waiting ones flagged `built: False`. Default taken: added, as u11 names
   them; a world with two experts may now draw them.
9. **PE3's facts.** Default taken: PE3 renders only when the elder's hard winters fall one to a world year; the generator's dating
   (tree years as days) usually breaks that, so PE3 mostly drops. Recommendation: date the generated hard winters in world winters
   (G62's follow-up, in `generate.simulate`).
10. **The gate check and the new holdings.** P1 and P2 check building holdings only, so a field, an ox team or a herd with no able hand
    or no keeper line is not refused. Default: unchanged (outside the brief); a follow-up row.
