---
id: docs/review/37_growth/02zzzh_hunt_fish/byproducts_and_substitutes.md
kind: note
updated: "2026-11-21"
---
# By-products, multistage chains, substitutes, and how the ladders meet (W-73)

*note · `docs/review/37_growth/02zzzh_hunt_fish/byproducts_and_substitutes.md`*


21 Nov 2026, 37.2 (subagent). Thread: fishing, hunting and their materials developed together ([[W-73 Fishing, hunting and their materials developed together|W-73]]), under the nutrition worlds
([[W-69 Nutrition worlds|W-69]]). Read-only: no code or data changed, nothing committed. It adds to the five notes in this folder and to the combined proposal
(`proposals/hunt_fish_materials.md`) and does not repeat them; where they already hold a figure, this note points to it.

Zach (21 Nov): "Also double check what we already looked into in terms of the other resources that could go into or come from
hunting / water etc. Also do any of these have multistage processes or different alternative substitutes for anything that have
different requirements but maybe are better or worse in different ways." And later the same day: "Do we only have many short
ladders, or do any ladders merge or replace other things? Are some high capital things much more efficient but push out others
etc? Do they differ in sustainability etc?"

**Parts:** 1, what we already looked into, and what became of it; 2, multistage chains and substitutes; 3, a recommendation for
the engine; 4, how the ladders merge, capture each other's flows, replace each other and differ in sustainability, with what the
engine already lets emerge.

**Marks.** **[firm]**: a published figure seen in this session's search results (a summary of the page, not the page itself).
**[recalled]**: a standard figure I know from the literature but did not see this session. **[estimate]**: my own reckoning, with
its working. **Fetching:** no page was fetched this session; every [firm] figure is as a search summary gave it, and the notes in
this folder found fetches refused by the proxy (fibre_and_cord.md, hunting_ladder.md). Check the [firm] figures against the page
before data.

**The engine's basis** ([[D2-258 The food values are put on one physical basis|D2-258]]): 1 food = 2,500 kcal; a unit of work = 2 hours; a person's engine year about 190 units (32 days).

---

## 0. In brief

1. **We had looked at almost all of it before, and built little of it.** Of about 50 resources from the hunt, the fowl and the
   water discussed since 23 Oct, the engine has 17 as goods (meat, offal, hide, tallow, tallow light, antler, horn, beaver pelt,
   castoreum, fish and its kept forms, salt, brine, egg, watercress, samphire, charcoal). Almost everything else sits in two benched
   packages: **the hunting and resources build ([[L-111 The hunting and resources build, a soon follow-up|L-111]])** and **wildlife pack K8, crafts and wild goods ([[L-121 Wildlife pack K8 crafts and wild goods|L-121]])**, with the fen and
   boats in **brief 5's fen and boats half ([[L-125 Brief 5's fen and boats half (pack K4's rest)|L-125]])** and the coast in **pack K9 ([[L-122 Wildlife pack K9 coast and cliff|L-122]])**. Three things were raised once and never
   recorded anywhere: **fish oil** (economy_web.md §2.11 "fish oil (light, P)"; Zach, 14 Nov: "seems potentially valid"), **eel
   skin for thongs** and **fish glue** (Zach, 14 Nov: "somewhat TOO niche or irrelevant ... maybe later"). Neither the deferral nor
   the "valid" was written into OPEN.md; the [[W-73 Fishing, hunting and their materials developed together|W-73]] proposal does not mention fish oil at all.
2. **Every chain that matters has a short, worse path beside the long, better one.** Rawhide beside bark-tanned leather (a day
   against a year); fresh, dried and smoked fish beside salt and barrels; wild cord beside flax; a hand-dug fat render beside the
   chandler; sun salt beside boiled salt. The short path is what a household does alone; the long path needs a fitting, a season
   and usually another group.
3. **The substitutes differ by what they need, more than by how well they work.** Cord from nettle needs only labour, from flax
   needs land and water, from the kill needs a carcass and rots in water. A trap of withies needs a willow bank, of net needs cord,
   of stone needs a crew and a shore. Fuel for salt and smoke is wood where there is wood and peat where there is bog. That is where
   villages would specialise and trade.
4. **The ladders do merge, and the big works do push others out.** Cord, withies, the smokehouse, salt, boats and dogs each serve
   several livelihoods. The weir, the mill dam, the decoy, small-mesh nets, the warren, the park and the dovecote each took a share
   of a flow others also lived on, and each brought a law: Magna Carta's fish-weir clause (1215), the gap and close time of 1285,
   London's burning of fine-mesh nets (1329, 1343, 1349), the weekly "Saturday's slop" in Scots cruives, the 1534 close time for
   moulting duck. The switch from fresh-water to sea fish in England around AD 1000 is real in the bones (Barrett and others 2004).
5. **The engine already lets several of these emerge.** Salmon and lamprey return from the spawners that got through (a
   Beverton-Holt return in `wild/runs.py`), so a weir's take and a shut mill race lower next year's run; the eels pass the upper
   village's gear first and the salmon the lower's; resident fish are one stock per water body shared by every method; the game's
   wariness carries one hunter's pressure onto the next. What it cannot yet do: fouling of the water, gear that selects by size,
   close times and mesh rules that bind, disturbance around a decoy, kept stocks (park, warren, pond).
6. **Recommendation:** model as choices only the substitutes that change who depends on whom: cord by three paths (wild, flax,
   the kill's thong for land snares only), trap and net from withies or cord, fuel for smoke and salt (wood or peat), keeping
   (built: recalibrate), the hook and spear from bone or the smith, butchering and gutting with two layers of skill, offal as bait,
   and later the barrel (withy hoops) and two boats. Fold fish oil into the coast (K9), glue and sinew into the bow, rushlights into
   evening work ([[L-102 Acting at different times of the day, as one general system|L-102]]). Details in §3.

---

## 1. What we already looked into (the records)

Sources read: proposals economy_web.md (all stages), economy_later.md, wildlife.md (§6 goods, §11 candidates), water_and_preservation.md,
river_and_water.md (brief 5), hunt_calibration.md (brief 4c), husbandry.md, tools.md, recipes.md, environment_systems.md,
livelihood_archetypes.md; review notes 02zu, 02zv (the content ledger), 02zs, 02zr, 02zzh (14 Nov, the economy's layers) and
02zzj 01, 02, 03, 10; `tools/records.py find` for each material word and `show` for [[L-111 The hunting and resources build, a soon follow-up|L-111]], [[L-13 Economy options kept out of the first worlds|L-13]], [[L-117 Wildlife pack K3 forays, methods and knowing|L-117]], [[L-121 Wildlife pack K8 crafts and wild goods|L-121]], [[L-125 Brief 5's fen and boats half (pack K4's rest)|L-125]] and the items
they point to; the engine's ITEMS (`engine/data.py`) for what exists.

**The 14 Nov conversation.** The transcript of this session holds the 14 Nov exchange only in a compaction summary, which cuts
Zach's message off. What survives: at 21:59 he asked "What are all the different fishing tool chains etc. different ladders kinda
like other things. What is a weir and how does this fit amongst other potential types of tools? And what resources would they
require? ... What dependencies would make sense to require for the different fishing things?"; the answer (not kept) listed
by-products including eel skin and fish glue; at 22:12 he replied: "Ok some of these things might be somewhat TOO niche or
irrelevant like eel skin for thongs and fish glue? Like maybe later idk. Fish oil seems potentially valid. I guess would gutting
fish be like the butchering meat equivalent, that turns it into all the different things. Also I feel like butchering for both
fish and other meats should have layers of skill, whereby default they can get some of the [cut off in the summary]". The written
outcome of that conversation is 02zzh (14 Nov) §3.7 ("gutting with skill (P) ... fish oil for lamps (P)") and §3.11 ("oil lamp (P:
fish or linseed oil)"), then economy_web.md §2.4 ("butchering and gutting ... skill decides how much meat, whether the hide is
whole, and what by-products are kept") and §2.11 ("fish oil (light, P)"). Eel skin and fish glue were dropped without a record.

**Status words.** *built*: on main as a good or act. *decided*: a D-number says it, not built. *benched*: a deferred item names it
(id). *proposed*: in a proposal in discussion. *dropped*: Zach set it aside, not recorded as a deferral. *never followed up*: raised
in a note or proposal, in no item and no later plan.

### 1a. From the kill

| Resource | Comes from | Goes into | Where discussed | Status | Zach's words |
|---|---|---|---|---|---|
| meat | kills, slaughter, young taken | eating; dried, smoked, salt meat | everywhere | built ([[D2-258 The food values are put on one physical basis|D2-258]] values) | |
| offal | every kill: 0.25 of its meat, left with the carcass | nothing now; proposed: dogs, ferrets, hawks, bait, food | economy_web §2.4; 02zzh §3.7 ("bait of offal"); 02zu Part D; 02zzj/03 §6.1 | built as waste; uses never followed up (not in the [[W-73 Fishing, hunting and their materials developed together|W-73]] proposal) | |
| hide (one good for every skin) | slaughter, wild kills | bedroll, tent, harness, pack, anvil, rod | wildlife.md §6; economy_web §2.5 | built | |
| rawhide thong | a hide cut in a spiral | lashing, heavy snares | fibre_and_cord §1; hunting_ladder §1.7 | proposed (rawhide for gear, [[W-73 Fishing, hunting and their materials developed together|W-73]] §2) | |
| leather (bark-tanned) | hide, oak bark, lime, months in pits | harness, packs, bellows, coracles | economy_web §2.5 (stage 1); husbandry §2; 02zzj/03 §6.2; 02zv rank 257 | benched: [[L-111 The hunting and resources build, a soon follow-up|L-111]], [[L-121 Wildlife pack K8 crafts and wild goods|L-121]]; the [[W-73 Fishing, hunting and their materials developed together|W-73]] proposal leaves tanning for later | |
| tawed or dressed skin, fur | skins with alum and salt, or brains and smoke | clothing, gloves, bags | hunting_ladder §1.7; 02zzj/03 §6.2; wildlife.md §6 ("trade and prestige only") | benched: [[L-121 Wildlife pack K8 crafts and wild goods|L-121]]; clothing parked ([[D2-10 Clothing is parked|D2-10]]) | |
| pelt, fur by quality | fox, otter, wolf, beaver, marten, stoat | warmth, trade | wildlife.md §6; 02zs §2; 02zv ranks 88, 259 | built only as "beaver pelt" (no use); every other pelt is "hide"; benched [[L-121 Wildlife pack K8 crafts and wild goods|L-121]] | |
| castoreum | beaver, at the lodge | medicine, trade | wildlife.md §6; 02zv rank 268 | built as a good with no use; its use waits on illness ([[L-121 Wildlife pack K8 crafts and wild goods|L-121]]) | |
| tallow | slaughter only (4 a cow) | tallow lights (x1.3 at night work) | 02zzg; hunt_calibration History; 02zzj/03 §6.3 | built; real uses benched: tallow's real uses ([[L-107 Tallow's real uses|L-107]]); from wild kills proposed ([[W-73 Fishing, hunting and their materials developed together|W-73]] §2) | 13 Nov, on tallow as food: "really worth more than meat feels kinda crazy" (so dropped as food) |
| fat, lard (boar, bear) | wild pigs and bears | food (rich), tallow | wildlife.md §6; KINDS uses "pork, fat" | never followed up; the kill gives none | |
| marrow and bone grease | cracked, boiled bones | food in a lean season | hunting_ladder §1.7 | never followed up | |
| bone | every carcass | hooks, gorges, needles, net gauges, glue, bone meal | economy_web §2.4; 02zs §2; 02zv ranks 264, 275 | benched: [[L-111 The hunting and resources build, a soon follow-up|L-111]], [[L-121 Wildlife pack K8 crafts and wild goods|L-121]]; proposed as one good with antler ([[W-73 Fishing, hunting and their materials developed together|W-73]] §2) | |
| antler | cast in spring (a 0.15 find), or a kill | a horn to blow; proposed: points, picks, handles, combs | wildlife.md §6 ("(none yet)"); 02zv rank 263 | built as a find; from the kill benched ([[L-111 The hunting and resources build, a soon follow-up|L-111]]); proposed with bone ([[W-73 Fishing, hunting and their materials developed together|W-73]] §2) | |
| horn (the material) | cattle, sheep | lantern panes, spoons, handles | 02zs §2; 02zu light row; 02zv rank 263 (horn lantern in K2 rank 6) | the engine's "horn" is a horn to blow made from antler; the material is benched ([[L-121 Wildlife pack K8 crafts and wild goods|L-121]]) | |
| sinew, gut | deer, cattle, sheep | bowstrings, thread, snares | 02zs §2; 02zv rank 265; fibre_and_cord §1 ("poor in water") | benched: [[L-121 Wildlife pack K8 crafts and wild goods|L-121]]; the [[W-73 Fishing, hunting and their materials developed together|W-73]] proposal leaves them out until the bow | |
| glue (hide, bone, fish) | scraps, hooves, bone; fish skins and swim bladders | the bow and arrow, joinery | 02zs §2; 02zv rank 266; withies_wood_materials §1.7 | benched: [[L-121 Wildlife pack K8 crafts and wild goods|L-121]]; fish glue dropped | 14 Nov: "TOO niche or irrelevant like ... fish glue? Like maybe later idk" |
| feathers, down | fowl, geese, swans, poultry | fletching, bedding, quills | wildlife.md §6; 02zs §2; 02zv ranks 174, 260 | benched: [[L-121 Wildlife pack K8 crafts and wild goods|L-121]]; the proposal leaves them until the bow | |
| quills, parchment, wax seals | goose feathers, limed hides, beeswax | documents | wildlife.md §11 ("writing is made from wild things"); husbandry §2 | documents decided ([[D2-24 The first-world goods include copper, salt, documents, hides and…|D2-24]]), parchment not built (recipes.md); benched [[L-121 Wildlife pack K8 crafts and wild goods|L-121]] | |
| eggs, young | heronries, rookeries, nests | food | wildlife.md; hunting_ladder §1.6 | built (gather young; egg as a hen's good); widening to wild eggs proposed ([[W-73 Fishing, hunting and their materials developed together|W-73]] §4) | |
| dung, bone meal | carcasses, flocks, dovecotes | fields | 02zs §2; 02zzj/02 | benched: [[L-121 Wildlife pack K8 crafts and wild goods|L-121]] (dung and bone meal); cattle dung built | |

### 1b. From the water and the wet ground

| Resource | Comes from | Goes into | Where discussed | Status | Zach's words |
|---|---|---|---|---|---|
| fish (eel, salmon, lamprey, the resident stock) | runs, lakes, reaches | eating; salt, dried, smoked fish | brief 5; [[D2-209 Brief 5 (river and water) is built|D2-209]] to [[D2-218 Set traps in high water|D2-218]], [[D2-229 One fish stock per water body|D2-229]], [[D2-258 The food values are put on one physical basis|D2-258]] | built | |
| gutting with skill | any catch | fish ready to keep; offal, roe, livers | economy_web §2.4; 02zzh §3.7; [[Q-73 Whether salting fish and meat stays at 4 kg a unit of work|Q-73]]'s notes (gutting folded into the salting rate) | proposed; open as the proposal's question 9, with the salting rate ([[Q-73 Whether salting fish and meat stays at 4 kg a unit of work|Q-73]]) | 14 Nov: "would gutting fish be like the butchering meat equivalent ... butchering for both fish and other meats should have layers of skill" |
| fish oil | livers and fat of fish (cod, eel), seals | lamps, currying leather, oil tanning | economy_web §2.11; 02zzh §3.7, §3.11; 02zu light row ("seal and fish oil"); 02zzj/03 §6.2 | proposed in two notes, then never followed up: in no item, not in the [[W-73 Fishing, hunting and their materials developed together|W-73]] proposal | 14 Nov: "Fish oil seems potentially valid" |
| eel skin | eels | thongs, flail bindings | the 14 Nov answer only | dropped | 14 Nov: "TOO niche or irrelevant ... maybe later idk" |
| salt, brine | saltmarsh pans by sun; a brine spring boiled with firewood | salting, cheese | [[D2-56 Recipe changes from the chain analysis|D2-56]]; brief 5 §4b; water_and_preservation §5 | built; open: salt's fuel ([[L-110 Salt's fuel, to recalibrate|L-110]]), "salt pan" names two things ([[L-128 'salt pan' names two things|L-128]]), the salting rate ([[Q-73 Whether salting fish and meat stays at 4 kg a unit of work|Q-73]]), keeping capital in the runs world ([[Q-76 Whether the runs world's medium arm needs more keeping capital|Q-76]]), stores perhaps too strong against preserving ([[L-137 Stores may be too strong against preserving|L-137]]) | 16 Nov on salt's fuel: "for now but flag as revisit for calibration"; 20 Nov: "stores are currently too overpowered rn potentially compared to salt etc." |
| sea salt boiled, sleeching | seawater, salt-caked sand | salt | 02zzj/01 §2.7 | never followed up (coast later, [[L-122 Wildlife pack K9 coast and cliff|L-122]]) | |
| stockfish (wind-dried) | cold windy coasts | food that keeps for years | water_and_preservation §7 ("a coastal speciality") | never followed up | |
| samphire, watercress | saltmarsh, wet ground | food | wild_plants | built (plant foods) | |
| crayfish | the shallows | food | [[L-125 Brief 5's fen and boats half (pack K4's rest)|L-125]] ("crayfish and retting downstream"); 02zv rank 246; fishing_ladder | benched [[L-125 Brief 5's fen and boats half (pack K4's rest)|L-125]]; the shallows stock proposed ([[W-73 Fishing, hunting and their materials developed together|W-73]] §4) | 16 Nov: "wouldn't they be like crayfish vs actual fish etc." |
| pearl mussel | upstream of salmon rivers | trade | 02zr; 02zv ranks 180, 243 | benched [[L-125 Brief 5's fen and boats half (pack K4's rest)|L-125]] | |
| shellfish, seals, seabirds, a stranded whale | the coast | food, oil, skins | wildlife.md §11; [[L-122 Wildlife pack K9 coast and cliff|L-122]] | benched: pack K9, coast and cliff ([[L-122 Wildlife pack K9 coast and cliff|L-122]]) | |
| medicinal leech | fen water | healing | 02zv rank 244 | benched: pack K10 ([[L-123 Wildlife pack K10 illness and the hidden|L-123]]) | |
| seaweed | the shore | (fields, kelp ash) | not found in the records | never raised for this world | |
| reeds | fen, reedbed | thatch, screens | water_and_preservation §5; wildlife.md §11; husbandry (thatcher); river_and_water §5 (left out) | benched with the fen ([[L-125 Brief 5's fen and boats half (pack K4's rest)|L-125]]); the proposal leaves them out | |
| rushes | wet pasture | rushlights, mats, fish frails | wildlife.md §11; 02zs §3 (light); withies_wood_materials §1.5 | never followed up (the built "tallow light" is "a rush or rag dipped in tallow" but rushes are no good) | |
| sedge | fen | thatch ridges, oven fuel | withies_wood_materials §1.5 | the proposal leaves it out | |
| peat, turf | wet moor, fen | fuel | water_and_preservation §5; economy_web §2.7 (stage 4); husbandry (turbary); 02zzj/01 §3.7; [[L-20 The catalogue's later kinds|L-20]] (peat fires) | never built; planned for economy_web stage 4 | |
| flax, hemp | a field or close; retted in water | cord, nets, linen | economy_later (fibre, [[L-13 Economy options kept out of the first worlds|L-13]]); economy_web §2.9 and stage 4; husbandry; 02zzj/03 §5.3 | benched ([[L-13 Economy options kept out of the first worlds|L-13]]); flax proposed as a crop ([[W-73 Fishing, hunting and their materials developed together|W-73]] §2); hemp not | |
| withies, willow | wild willow on wet ground; a withy bed | traps, wattle, hurdles, baskets | wildlife.md §11; economy_web §2.6; husbandry; [[D2-209 Brief 5 (river and water) is built|D2-209]]'s answer 7 | benched [[L-111 The hunting and resources build, a soon follow-up|L-111]]; proposed as a good with the withy bed ([[W-73 Fishing, hunting and their materials developed together|W-73]] §2) | 16 Nov: "This will be for the hunting and resources build which should be flagged as a soon follow up" |
| fowl: feathers, down | wildfowl, swans | bedding, fletching | as 1a | benched [[L-121 Wildlife pack K8 crafts and wild goods|L-121]] | |

### 1c. From the wood and the heath, for the hunt and the water

| Resource | Comes from | Goes into | Where discussed | Status | Zach's words |
|---|---|---|---|---|---|
| poles | young growth, coppice | stakes, shafts, weir, racks | economy_web §2.6 | proposed: folded into timber ([[W-73 Fishing, hunting and their materials developed together|W-73]] §2); "cut poles" today gives firewood | |
| bark (oak) | coppice in spring | tanning, barking nets | economy_web §2.5, §2.6; fibre_and_cord §4 | benched [[L-111 The hunting and resources build, a soon follow-up|L-111]]; the proposal leaves it out | |
| bast, nettle, cord | lime, willow; nettle stems | snares, lines, nets, rope | economy_web §2.9; [[L-117 Wildlife pack K3 forays, methods and knowing|L-117]] (K3: cord); [[Q-57 Fishing, from the lake run|Q-57]] (b) ("cord and hair are not resources yet", closed into [[W-67 Extending the wildlife economy|W-67]]) | benched [[L-111 The hunting and resources build, a soon follow-up|L-111]], [[L-117 Wildlife pack K3 forays, methods and knowing|L-117]]; proposed as one good ([[W-73 Fishing, hunting and their materials developed together|W-73]] §2) | |
| horsehair | horses' tails | rod lines, bird nooses | [[Q-57 Fishing, from the lake run|Q-57]] (b); fibre_and_cord §1 | proposed and closed into [[W-67 Extending the wildlife economy|W-67]]; the proposal leaves it out | |
| bracken, heather, gorse | heath, moor | bedding, thatch, oven fuel | wildlife.md §11; 02zv rank 233 (K5) | gorse folded into firewood ([[W-73 Fishing, hunting and their materials developed together|W-73]] §2); the rest never followed up | |
| oak galls, ink | oaks | documents | wildlife.md §11 ("with documents") | never followed up | |
| honey, wax | wild bees | food; seals, candles | wildlife.md (wave 2, [[D2-192 The first wild kinds come in four waves|D2-192]]); 02zv rank 262; [[L-119 Wildlife pack K6 keeping|L-119]] (the apiary) | decided as a wave-2 kind, not built; wax benched [[L-121 Wildlife pack K8 crafts and wild goods|L-121]] | |
| pitch, tar | pine roots, birch bark | boats, tarred nets and lines | economy_later ("boats: timber, pitch"); withies_wood_materials §1.7 | benched with boats ([[L-13 Economy options kept out of the first worlds|L-13]], [[L-125 Brief 5's fen and boats half (pack K4's rest)|L-125]]); the proposal waits for boats | |
| bird lime | holly bark, fermented | limed twigs for small birds | hunting_ladder §1.6; withies_wood_materials §1.7 | the proposal: "unless fowling needs it" | |
| lime (quick) | limestone, burned | tanning, mortar, fields, parchment | economy_web (L); 02zzh tranche 4; 02zzj/03 | never built; planned later | |
| charcoal | timber, a woodsman | smelting, a hearth | [[D2-56 Recipe changes from the chain analysis|D2-56]] | built | |
| resin, dye | | | not found in the records | never raised | |

### 1d. Gear and keeping that these feed

| Thing | Status |
|---|---|
| traps as a good (1 timber, 0.25 hide, 20 nights) | decided ([[D2-23 The tool set|D2-23]], recipes.md), never built; the free sets took their place |
| nets | benched: options kept out of the first worlds ([[L-13 Economy options kept out of the first worlds|L-13]]: "fibre is deferred"); a `net` method exists without cord |
| boats (punt, coracle, logboat) | benched: [[L-13 Economy options kept out of the first worlds|L-13]], travel by water ([[L-38 Travel by water|L-38]]), transport ([[L-53 Transport and traders, built out|L-53]]), the fen and boats half ([[L-125 Brief 5's fen and boats half (pack K4's rest)|L-125]]) |
| metal-jawed traps, hide armour | economy_later; never followed up |
| hooks of bone or copper, the spear, the bow | economy_web §2.10, §2.11, stage 2 and 4; [[L-111 The hunting and resources build, a soon follow-up|L-111]]; [[L-117 Wildlife pack K3 forays, methods and knowing|L-117]] (K3) |
| dogs, ferrets, the warren, purse nets, the fishpond, the dovecote, hawks, tame decoys | decided in part (hounds in wave 2, [[D2-196 Hounds in wave 2, with the wolves|D2-196]]); benched: pack K6, keeping ([[L-119 Wildlife pack K6 keeping|L-119]]) |
| the decoy pond and its quiet zone | benched [[L-125 Brief 5's fen and boats half (pack K4's rest)|L-125]] (it needs a trained dog) |
| barrels | economy_web stage 3 ("barrels as a store fitting") and 02zzx §5; never built: brief 5 left them out |
| baskets, fish frails | 02zu containers row; never followed up |

**What this shows.** The materials were not missed: they were benched in packages that waited on uses (clothing, documents, the bow,
illness, the coast, boats). The design rule that benched them (wildlife.md §6: "a kind earns its place ... only if what it gives has
a use now") still holds, and [[W-73 Fishing, hunting and their materials developed together|W-73]]'s job is to give the first of them a use. Three items need recording: fish oil (no item), eel
skin and fish glue (Zach's "maybe later", no item), and offal's uses (no item, though the engine makes offal at every kill).

---

## 2. Multistage chains and substitutes

### 2a. Multistage chains

Each row is one stage; "short path" says whether a household can stop there with a worse product. Times on the engine's basis: a
unit of work is 2 hours, a night is a night.

**Hides and skins**

| Stage | What it is | Time and work | Capital | Gives, and its trade-off |
|---|---|---|---|---|
| 1. skinned, scraped | fleshed with a scraper or knife | a deer 1 to 2 hours [estimate] | a knife | raw hide: rots in days unless dried or salted (the engine's DECAY abs on hides) |
| 2. rawhide | stretched and dried, or salted | days to dry, an hour's work [estimate] | a frame or pegs; salt to keep it | **short path**: stiff, strong dry, stretches and rots wet; lashing, heavy snares, drum heads, the rod's grip; a cow hide gives tens to hundreds of metres of thong (fibre_and_cord §1) |
| 3a. brain-dressed and smoked | brains worked in, the skin stretched soft, then smoked | brain soak 2 to 8 hours, softening hours a hide; a practised worker softens about 4 deer hides a day [firm, a practitioner quoted in *The Furrow*]; one deer's brain tans its own hide [firm, Richter and Dettloff 2002] | none but fire | soft buckskin: clothes, bags; smoked so it dries soft after a wetting; no bark, no pit, no trade |
| 3b. tawed | soaked in alum and salt, with egg yolk and flour | 2 to 4 weeks [firm, ethnographic summary] | alum (traded), a vat | white soft leather: gloves, purses, fur; **not stable in water** unless greased [firm, conservation literature] |
| 3c. bark-tanned | limed to unhair, then months in pits of oak-bark liquor, then curried with fat or fish oil | light skins several weeks to months, heavy hides 11 to 18 months, sometimes two years (02zzj/03 §6.2) [firm]; bark several times the hide's weight [recalled] | tan pits by water, a coppice's bark (spring only), lime, credit for a year's stock | heavy leather: harness, soles, buckets, bellows; durable and water-resistant; ties the tanner to oak and water, and fouls the water below |

The short path (rawhide) does nearly everything the hunt and the water need: snares, lashings, the rod's grip, a coracle's skin
(a hide stretched on willow, greased). Leather is for harness, shoes and bellows: the farm and the forge more than the hunt.

**Fish**

| Stage | Time and work | Capital | Keeps | Trade-off and who did it |
|---|---|---|---|---|
| alive in the trap, the weir's crib, a keep box or a stew | none until lifted | the trap; a stew pond, a corf (a floating box) | days to weeks (built: alive in a trap or weir until lifted, [[D2-211 Fresh fish keep as meat in hand, and alive in a trap or a weir until…|D2-211]]) | fresh fish at Lent for a lord; corves held eels off shore until the catch reached harbour [firm, later practice]; medieval eels were mainly traded salted, smoked or dried, not alive [firm, BBC History summary] |
| fresh, gutted | herring 2,400 to 3,600 an hour a skilled gutter; cod 240 an hour (02zzx §3) | a knife | a day or two (built: 0.30 a night) | everyone; gutting is fast for a trade, slow for a novice |
| dried at a hearth or on a rack | 3 nights (built) | a hearth rack | weeks (built) | the household floor |
| smoked: hot (70 to 80 °C, hours) or cold (28 to 32 °C) [firm, Wikipedia on smoked fish] | bloaters 4 to 16 hours of cold smoke; red herring heavily salted up to 24 hours, then heavy smoke up to 2 days and light smoke up to 6 weeks [firm, secondary]; a Yarmouth maker today does reds about twelve weeks [firm] | a smokehouse, fuel, tending | kippers days; red herring months, about as long as white salt herring [firm] | the hard red herring is salt and smoke together: the long path; the engine's smokehouse is the mild 3-night cure |
| salted: dry salt or pickle in barrels | crews about 110 to 165 kg an hour a person all steps (02zzx §3); barrels settle in about 10 days and are filled up | salt at 1 to 3 or 4 by weight; barrels (32 gallons; a last of 12 barrels held about 10,000 to 13,200 herring [firm, Albion summary]) | a year or more | the medieval trade in herring and eels; the bind is salt, barrels and hands (02zzx §5) |
| wind-dried: stockfish | 2 to 3 months on racks from February or March, finished indoors by May or June [firm, Lofoten]; about five-sixths of the weight goes [firm, Norwegian heritage summary] | racks, a cold dry windy spring, lean fish (cod) | years | no salt, no fuel; only where the weather does it (the north, the coast); the stockfish trade from Lofoten fed medieval Europe |

The short path is fresh or hearth-dried. Each longer path buys months of keeping with a different scarce thing: smoke with fuel and
a building, salt with salt and barrels, wind with a climate. That is why the 1-to-4 salt ratio and the fuel budget (brief 5 §4c)
matter more than the catch.

**Fat, oil and light**

| Stage | Work | Capital | Gives | Trade-off |
|---|---|---|---|---|
| suet or fat cut out | part of butchering | a knife | raw fat | spoils like meat |
| rendered at the hearth | an hour or two a beast's fat [estimate] | a pot | tallow (beef, mutton), lard (pig, boar), dripping | keeps; candles, rushlights, grease, soap; deer are lean, boar and bear fat (hunting_ladder §1.7) |
| rushlight: a peeled rush dipped in fat | quick; Gilbert White, 1775: about 1,600 rushes to the pound [firm, though one source says 1,000]; a 28.5-inch rush burned 57 minutes; a poor family got about 5.5 hours of light for a farthing [firm, secondary] | rushes from wet ground; kitchen fat | the cheapest light | needs rushes and fat, both by-products; White's point was that it beat a halfpenny candle many times over |
| dipped tallow candle | a chandler's dipping, a wick of cord | a trade in towns; tallow | a brighter, smokier light | tallow was dear before about 1350 and fell after [firm, secondary]; wax was for the church and the rich (Sapoznik 2019, wax in England c.1300 to 1555) |
| fish oil | livers left to rot in barrels and the oil skimmed through the season, heat to get the last [firm, Science History Institute, Wikipedia]; 250 to 400 cod gave a barrel of livers, two barrels of livers a barrel of oil (1883) [firm] | barrels, a coast with cod or seals | lamp oil ("train oil"), currying and oil-tanning leather (02zzj/03 §6.2) | a sea product: fat sea fish and their livers, seals, whales. Fresh-water fish are mostly lean; the eel is the exception at about 12% fat raw [recalled, USDA], but no inland trade in eel oil was found |

**Bone, antler and horn**

| Stage | Work | Gives | Trade-off |
|---|---|---|---|
| raw, from the carcass | part of butchering | bone, antler | a gorge (a pointed bone sliver on a line) is minutes' work [estimate] |
| boiled and cleaned | a pot over hours [estimate] | grease (food), glue stock, clean bone | the same pot makes glue from scraps (5 to 10% of their weight, withies_wood_materials §1.7) |
| soaked and worked | antler soaked days to weeks; a barbed point hours with flint, an hour or two with metal (withies_wood_materials §1.8) | points, hooks, net needles, gauges, handles, combs | a bone hook is a home product; an iron hook is the smith's (§2b) |
| horn soaked, heated, pressed | the horner's trade (02zzj/03) | lantern panes, spoons | from cattle and sheep, not the hunt |

**Flax** is in fibre_and_cord §2 (pull, ripple, ret 1 to 2 weeks in water or 3 to 6 on grass, break, scutch, hackle, spin, ply;
about 4 to 7 hours a kg to fibre and 15 to 20 hours a kg to coarse cord, three times cheaper than wild cord). The short path is
wild nettle or bast twisted by hand.

**Salt**

| Path | Needs | Fuel | Season | Trade-off |
|---|---|---|---|---|
| sun pans on a saltmarsh (built) | a saltmarsh, pans, raking | none | summer only (built: by season) | free heat, but weather-bound and seasonal |
| boiled brine from a spring (built) | a spring, a lead or iron pan, the salter | Droitwich brine near saturated: four tons of brine to one of salt (17th c.) (02zzj/01 §2.7) [firm]; the engine 1 firewood a salt ([[L-110 Salt's fuel, to recalibrate|L-110]]) | all year | ties the spring to the woods; Droitwich took cartloads of wood as rent |
| boiled seawater | the shore, a pan | seawater is about 3.5% salt: about seven times the brine and nine times the water boiled off for the same salt (02zzj/01) [calc] | all year | so dear in fuel that coastal makers concentrated the brine first |
| sleeching (muldefang in Lincolnshire) | salt-caked sand from the spring-tide line washed in a trench to a strong brine, then boiled; filtration beds lined with lime mortar; lead boiling tanks; peat ash at Fenland sites [firm, Historic England; Lincolnshire HER] | labour to carry and wash sand, then much less fuel | summer for the sand | turns labour into saved fuel; Domesday counts eleven salterns at Wainfleet and twenty more nearby [firm] |

### 2b. Substitutes with different requirements

**Cord** (fibre_and_cord §1 holds the figures; this is the trade-off view)

| Option | Needs | Better at | Worse at | Who used it |
|---|---|---|---|---|
| nettle | rich ground, labour (35 to 80 hours a kg twisted) | strong, fine, free | slow; late summer | everyone before flax; Bronze Age nettle cloth |
| lime or willow bast | young lime or willow, spring stripping, weeks of retting in still water | coarse, good wet, plentiful near woods | weak (hemp about three times bast's breaking load) | Mesolithic nets (Antrea, willow bast); Russian bast rope to the 19th c. |
| flax | good manured land, a retting pond, a hackle from the smith | cheap by weight once grown; fine twine for gill nets | takes grain land, fouls the water | Neolithic lake villages for fine nets; every medieval village with a close |
| hemp | a heavily manured hemp-yard by the house | the strongest; rope, nets, sail | as flax, more manure | eastern England from about AD 800; rope walks |
| sinew | a carcass's back strap and leg tendons | very strong dry; bowstrings, sewing | stretches and fails wet: not for fishing | hunters, the steppe |
| gut | intestines | bowstrings, strings | poor wet | strings; Viking fishing lines of sheep, cow or walrus gut [firm, World History Encyclopedia summary] (a counter-example: gut lines did fish at sea) |
| horsehair | horses' tails | fine rod lines, bird nooses, good in water | needs horses; short lengths | anglers until silkworm gut (17th to 18th c.); Berners, 1496 [recalled] |
| rawhide thong | any hide | heavy snares, lashing, quick | stretches wet, rots | everywhere, for land gear |

**Light**

| Option | Needs | Good for | Bad for |
|---|---|---|---|
| the hearth's glow | a fire | free | no task work |
| rushlight | rushes (wet ground) and any fat | cheapest per hour | dim, an hour a rush |
| tallow candle | tallow, a wick of cord, a chandler or a mould | brighter, carried | smoky, dear before 1350 |
| fish or seal oil lamp (the cruisie of the Scottish coast [recalled]) | a coast, fish livers or seal blubber, a lamp | a steady light from waste | coastal; smells |
| beeswax candle | bees (wild or kept) | clean, bright, prestige; church and seals | dear; a church and lord's light |

**Glue**

| Option | Needs | Good for | Bad for |
|---|---|---|---|
| hide glue | hide scraps, hooves, a pot, about 6 hours a batch; 5 to 10% of the scrap's weight | the strongest common glue; bows, fletching, joinery | weakens with heat and wet |
| bone glue | bones boiled | as hide, weaker | |
| fish glue (isinglass from swim bladders; glue from skins) | sturgeon or other bladders, fish skins | fine work; manuscript painting and illumination in the Middle Ages [firm, secondary] | small quantities; a town or coast good |
| birch tar | birch bark dry-distilled: 1 to 10 g a 100 g of bark by method | waterproof hafting of points | hours of tending for grams |

**Preserving** (built: dry, smoke, salt, alive in a trap; this is the trade-off view)

| Option | Needs | Keeps | Good for | Bad for |
|---|---|---|---|---|
| alive in a trap, a weir's crib, a corf, a stew | water, the gear or a pond | days (traps) to months (a stew) | fresh fish when wanted; no work | space; theft and otters (built: otters rob unwatched traps) |
| hearth-drying | a hearth | weeks | anyone | small batches (built: 8) |
| smoking | a smokehouse, fuel, daily tending | months | a village's capital; meat and fish | fuel; fire risk (built: 2% a night for wattle) |
| salting | salt, barrels or tubs, hands | a year or more | the long trade | salt is a chokepoint; barrels a craft |
| wind-drying (stockfish) | a cold, dry, windy spring; lean fish | years | no salt, no fuel | only the right climate |
| freezing | a frost | while it lasts | winter kills keep (the engine's DECAY `frozen` 0.2 already slows rot) | a thaw ends it |
| fermenting (rakfisk, surströmming, buried fish) | a pit or a barrel, little salt | months | where salt was scarce | Nordic, not English practice [recalled]; out of period here |

**Fuel for smoking and boiling salt**

| Option | Needs | Heat | Good for | Bad for |
|---|---|---|---|---|
| firewood, brushwood | a wood | 0.5 a unit (built) | anywhere with wood | bulky; competes with the hearth (brief 5 §4c) |
| timber | felling | 2 (built) | dense | competes with building |
| charcoal | 5 timber, a woodsman | 6 (built) | light to carry far; smelting | wastes about 60% of the wood's energy; no smoke for smoking |
| peat | a bog, cut in spring, dried 2 to 8 weeks before stacking [firm, Irish practice]; about two weeks for a family to cut its own plot [firm, a recollection]; air-dry 12 to 15 MJ a kg (02zzj/01) | about half of dry wood's 18 to 19 MJ a kg [recalled] | where wood is gone: the Fens' salterns burned it (peat ash at Pinchbeck) | a summer's work ahead; it hardly regrows |
| gorse, furze | heath, cut every few years | quick hot flame | bread ovens, kilns | not a slow fire |
| reeds, sedge, straw, dung | fen, fields, byres | low | where nothing else | quick, smoky |

**Traps**

| Option | Needs | Life | Good for | Bad for |
|---|---|---|---|---|
| wicker trap (grig, hive, putcher) | 2 to 3 kg of willow rods, 4 to 8 hours | about 2 years with repair (withies_wood_materials §1.2) | eels and salmon; anyone with willow | spates wreck it (built) |
| net fyke (a bag net on hoops with wings) | cord (about 0.2 to 0.5 kg for a small one [estimate]), withy hoops, a netter | a season untreated, more if barked | lighter, folds; wings lead fish in | rots; needs cord and a netter |
| stone or wattle fish garth, a tidal weir | a crew, stakes and wattle or stone, a shore or a river | decades for the frame, seasons for the wattle | the whole run, unattended | a held site; blocks others (§4) |
| deadfall, pit | stones, timber | as long as it stands | furbearers, wolves | indiscriminate; dangerous |
| snare of cord, hair or thong | 3 to 4 g of cord a noose | a few settings | hares, rabbits, birds | chewed, stolen |

Both wicker and nets were used side by side into the 20th century in Dorset and the Fens [firm, *Shooting Times* summary]; FAO
says wooden eel baskets were later replaced by netting or plastic ones [firm]. No dated medieval switch from wicker to fyke was found.

**Boats** (later; [[L-38 Travel by water|L-38]], [[L-125 Brief 5's fen and boats half (pack K4's rest)|L-125]])

| Option | Needs | Good for | Bad for |
|---|---|---|---|
| logboat | one large oak (felling a 1.1 m oak with bronze axes is about two man-days [firm, Soton logboat repairs paper]), hollowing by axe and fire, a crew | lasts decades; carries a load; ferries | a great tree; heavy, river-bound; no total build time found |
| coracle | a willow and hazel frame, one hide (its size set by one ox's hide [firm, *Mother Earth News* summary]), grease or pitch | one person carries it; salmon netting in pairs on the Teifi [firm]; cheap | short life, one person, still water or a steady river |
| plank boat | boards (a saw pit), nails or rivets (the smith), a boatwright, pitch | the open water, loads, the sea | the dearest: a carpenter and a smith |

**Points and hooks**

| Option | Needs | Good for | Bad for |
|---|---|---|---|
| thorn, wood gorge | a hedge, minutes | free | weak, small fish |
| bone or antler (gorge, hook, leister prong) | the kill, hours of work | a home product; Mesolithic to Neolithic Scandinavia [firm, EXARC 2020] | brittle; barbs hard to cut |
| copper or iron (hook, spear head) | the smith, ore and charcoal | durable, sharp, barbed; Viking iron hooks 800 to 1000 "easy and cheap to produce" [firm, secondary] | a dependence on the smith |

**Containers for salting and keeping**

| Option | Needs | Good for | Bad for |
|---|---|---|---|
| barrel, cask | a cooper, cleft oak staves, hoops of hazel or willow withies [recalled] | salt fish and meat in pickle, carried and stacked; a herring barrel about 113 kg of fish (02zzx §3) | a craft; dear |
| crock, pot | clay, a kiln (deferred) | potted meat, butter | breaks; heavy (02j: "pottery jars never win") |
| basket, frail | withies or rushes | carrying fish, drying | no pickle |
| pit, clamp | digging | roots, fermented fish | damp |

**Bait**

| Option | Needs | Good for |
|---|---|---|
| worms, grubs | digging, free | the rod and set lines for eels and trout |
| offal, guts | the kill or the gutting (built: offal rots at the carcass) | eel traps, set lines, crayfish; draws otters and crows as it does now |
| small fish | the shallows | pike, eels |

**Rabbits** (out of the engine until the warren: no rabbit kind; [[L-119 Wildlife pack K6 keeping|L-119]])

| Option | Needs | Good for | Bad for |
|---|---|---|---|
| ferrets with purse nets over the holes | ferrets kept and fed, purse nets of cord | taking rabbits from burrows by day; the warrener's main method [firm, secondary] | ferrets eat every day; nets |
| long nets at night with a lurcher | a long net (much cord), a dog | many at once on open ground [firm, secondary] | a dog to keep; poaching's method |
| dogs alone (coursing) | a fast dog | hares on open ground | few at a time |
| snares | cord or hair | a cheap line overnight | slow; stolen |

---

## 3. A recommendation for the engine

The test (02zzh §6; economy_web §1): a substitute or stage earns a place only if it **creates a decision** (a cheaper, worse way and a
dearer, better way), or **ties a chain to different land, skills or capital** so that villages specialise and trade (scenario_design
§1: leverage and dependence, several interlocking chokepoints). It must fit [[D2-204 People answer the wild by general methods, not a technique per kind|D2-204]] (general methods: gear and recipes vary, not a
technique per kind), real values within about 20% where they touch food ([[D2-259 The food values are anchored on real values|D2-259]]), and Zach's shallow ladders ("having 4 ladder
rungs is a terrible idea"; "possible to do things with less layers, that have less beneficial outputs").

### 3a. Model as real choices

| Choice | How, in the engine's seams | Why it is a choice | Phase |
|---|---|---|---|
| **1. Cord by three paths** | one good, `cord`, from three recipes: twist from wild nettle or bast (slow, seasonal), dress and spin flax (cheap, needs land and the retting water), cut thong from a hide (fast; usable only for land gear: snare lines and lashing take cord or hide as alternatives, nets and lines take cord) | labour against land against the kill; the flax village sells cord, the hunter has thong | 3 (the proposal's §2) |
| **2. Traps and nets of withies or cord** | one `trap` good from withies (wicker) or from cord and withies (a net fyke); one `net` good; the set's hold and life from the gear (engine_audit seam 5) | the willow village against the cord village, the same method | 3 |
| **3. Butchering and gutting in two layers of skill** | one general `dress` work at a carcass or a catch (as `bury` and `burn`). Anyone: meat (a novice loses 10 to 20%) and the hide. Capable or trained: also tallow from fat beasts, bone and antler, and the hide whole (a cut hide makes worse gear). Fish: gutting fast and folded into salting until [[Q-73 Whether salting fish and meat stays at 4 kg a unit of work|Q-73]] settles; offal from both | Zach's 14 Nov "layers of skill, whereby default they can get some of the ..." read as two layers, not four; it makes the skilled butcher worth having | 3 |
| **4. Hooks and spear points from bone or the smith** | gear multipliers on the rod and the spear by material (bone, copper), as weapons already carry `weapon` 2.0; a bone hook from the kill at home, a copper one from the smith | the home product against the smith's: a dependence on the forge, the shape scenario_design wants | 3 or 4 |
| **5. Offal as bait** | an optional input to set lines, traps and the rod that multiplies the take (about x1.5 for eels [estimate; calibrate]); offal keeps drawing otters and crows (built) | it gives a good the engine already makes a use, at no new good; baited traps draw robbers | 4 |
| **6. Fuel for smoke and salt: wood or peat** | peat as a gather on wet moor and fen (cut, then dried over nights as a batch, like hearth drying), heat about half of firewood's by weight [calibrate]; gorse folded into firewood (proposal) | a fen or moor village can smoke and boil without a wood; the Fens' salterns burned peat | 4 or with the fen ([[L-125 Brief 5's fen and boats half (pack K4's rest)|L-125]]) |
| **7. Keeping: built, recalibrated** | the four ways exist (alive, dried, smoked, salted) and frost already slows rot; settle the salting rate ([[Q-73 Whether salting fish and meat stays at 4 kg a unit of work|Q-73]]) and stores against preserving ([[L-137 Stores may be too strong against preserving|L-137]]) | already the right shape: each long way costs a different scarce thing | 2 (calibration) |
| **8. The barrel (later, with [[Q-73 Whether salting fish and meat stays at 4 kg a unit of work|Q-73]])** | a store fitting that holds salt fish and meat, made by a cooper from timber and **withy hoops** | if salting gets ten times faster, the container binds, as it did (02zzx §5); and withies gain a second buyer | 6 |
| **9. Two boats (later, with [[L-125 Brief 5's fen and boats half (pack K4's rest)|L-125]])** | one `boat` good with two recipes: a coracle (withies, one hide, grease; one person) and a logboat (one great oak, a crew; lasts) | the willow-and-hide village against the oak-and-crew village; both open the mere's middle | 6 |
| **10. Hide: rawhide now, leather as a threshold later** | rawhide is the built `hide`; tanning later as a batch in tan pits over many nights, with bark and water | time capital and a tanner who needs hunters, herders and the oak wood (economy_web §2.5) | 6 |

### 3b. Merge

- **Bone and antler** into one good (as the proposal); horn the material stays with the herds.
- **Brain-dressing and tawing** into one later "dressed skin", or leave both out: the hunt's gear needs only rawhide.
- **Rushlight into the tallow light**: the built light already reads "a rush or rag dipped in tallow"; a rushes input matters only
  when evening work makes light a need ([[L-102 Acting at different times of the day, as one general system|L-102]]).
- **Fish oil into the coast** (pack K9, [[L-122 Wildlife pack K9 coast and cliff|L-122]]): cod livers, seals and stranded whales give the oil; inland, the fat eel is the only
  fresh-water source and no trade in it was found. Record it under K9 with Zach's "seems potentially valid". If an inland use is
  wanted, let gutting eels give a little tallow-equivalent fat at the capable layer, named as a lever.
- **Sleeching and sea-water boiling** into one coastal salt-making recipe when the coast comes; the two inland ways are built.
- **Gut and horsehair** into cord as recipes only if horses and sheep are common in a world; otherwise leave out.

### 3c. Leave out (for now), and record

- **Eel skin, fish glue, isinglass**: Zach's "maybe later"; add a deferred row so it is not lost.
- **Sinew, glue, feathers** until the bow (the bow is the only deep chain: hunting_ladder §2.2).
- **Bird lime**: tiny food; only if a world's fowling needs a no-cord path for small birds.
- **Fermenting, crocks, pits**: out of period or never winning (02j).
- **Rabbits, ferrets, purse and long nets, the warren**: with keeping ([[L-119 Wildlife pack K6 keeping|L-119]]).
- **Stockfish**: with the coast and a cold climate.

### 3d. How it fits the proposal's phases

Phase 2 (the compressed year) and the salting rate first, since both scale every keeping choice. Phase 3 takes choices 1 to 3 (cord
by three paths, gear of withies or cord, dressing with two layers) and the bone hook of choice 4. Phase 4 adds bait and peat with
the methods. Phase 6 (later) holds the barrel, the boats, tanning and the coast's oil. The goods count stays small: cord, withies,
flax, bone, peat; offal and hide gain uses rather than new goods.

---

## 4. Do the ladders merge, push each other out, replace each other, and differ in sustainability?

Short answer: yes to all four. The ladders are short, but they share their inputs and their water, and the high-capital works on a
shared flow took from everyone else, which is why every one of them has a law.

### 4a. Ladders that merge through shared inputs or shared capital

| Shared thing | Serves | The real case |
|---|---|---|
| **cord** | snares (hunting), fowling nets, fish nets and lines, bowstrings, well ropes, barrel slings | fibre_and_cord §7; one hemp-yard or flax close served all of a village's gear |
| **withies** | eel traps and putchers (fishing), the weir's wattle, sheep hurdles and folds (herding), wattle walls (building), smoke-rack hurdles (keeping), baskets, barrel hoops, coracle frames | the Severn putcher weirs renewed their willow cones about every two years on elm frames lasting 20 years (withies_wood_materials §1.2); a hazel acre made about 300 hurdles a cut (§1.3) |
| **the mill dam** | grinding and the eel fishery | eel bucks were built on Thames mill and lock structures [firm, Wikipedia "Eel buck"]; built in the engine: a trap in a shut mill race takes half an eel run |
| **boats** | salmon netting (coracles in pairs), fowling (the moult drive), ferries, carrying | the Teifi coracle men netted salmon in pairs [firm]; the 1678 and 1720 moult drives used boats and beaters (hunting_ladder §1.6) |
| **dogs** | the hunt, the decoy (the decoyman's dog draws duck up the pipe), herding, the watch | hunting_ladder §1.6; [[D2-196 Hounds in wave 2, with the wolves|D2-196]] |
| **the smokehouse and salt** | fish, meat, cheese, salted hides | built for fish and meat; salt for cheese built |
| **the knife and the carcass** | food, gear (thong, bone hooks), light (tallow), bait (offal) | economy_web §2.4 |

### 4b. High-capital methods that are far more efficient but take a shared flow

| Method | How much better | Whom it pushed out | The law or the fight |
|---|---|---|---|
| **the fish weir** across a river | a share of the whole run, unattended (brief 5: 30% a first section) | boats, and every fisher below | Magna Carta c. 33 (1215) ordered kydells (fish weirs) removed from the Thames, the Medway and all England except the sea coast, after Richard I's 1197 and John's 1199 charters had failed; it served London's navigation first [firm, Magna Carta Project]. At Stirling in 1365 townsmen "violently and unjustly attacked and demolished the weirs and fisheries" of Cambuskenneth Abbey [firm, Arcadia] |
| **the gap and the close time** | (the remedy) | | Westminster II (1285, 13 Edw. I c. 47) set a close season for salmon, required a gap in weirs on the Eden, Esk and Derwent, and barred taking young salmon at mill dams from mid-April to St John's Day; confirmed and extended to the Thames in 1389 (13 Ric. II c. 19), which also barred fry nets [firm, secondary; check the statute text] |
| **the cruive** (a Scots fixed salmon trap) | the run, held | the proprietors above | "Saturday's slop": no salmon to be taken from evensong on Saturday to sunrise on Monday; a 1684 Court of Session case ordered it kept in all of a man's cruives, citing an Act of 1581 [firm, BAILII summary]; the modern weekly close time is 42 to 60 hours [firm, legislation.gov.uk] |
| **the mill dam** | grinding power | the salmon, and so every salmon fisher above and below | a 2016 Radboud study argues mills, not overfishing, began the collapse of salmon stocks: dams blocked spawning runs and destroyed gravel beds, an effect lasting centuries [firm, phys.org summary]; as mill dams spread, southern English and northern French stocks dwindled and buyers turned to Scottish rivers [firm, Arcadia] |
| **fine-mesh nets** (kidels) | "catching every fish, even the smallest" | the next year's fishers | London: in 1329 twelve nets with half-inch meshes (the rule one and a half inches) were burned at the Cross in Cheapside and the men jailed; in 1343 four of eight nets failed the two-inch rule and were burned; in 1349 five more, with three bushels of small fish [firm, Memorials of London] |
| **the duck decoy** (17th c.) | about 2,700 duck a season at Ashby, 3,100 a decoy near Wainfleet (hunting_ladder §1.6) | every other fowler near it | silence at the pond; "shooting within a considerable radius is, of course, strictly prohibited", and damages were awarded against people who put the birds up [firm, a 19th-c. text via the Essex Field Club]. The decoy's quiet zone is an externality on the neighbours' guns |
| **the warren** | about 4,500 rabbits culled on about 930 ha at Lakenheath in 1384-5, 78% to market [firm, but garbled in the summary]; more than 20,000 a year sold at 4d in the 1520s [firm]; a 13th-c. rabbit 3.5d plus a penny for the skin [firm, *Country Life*] | the commoners' grazing and crops nearby | Wiltshire farmers' complaints of rabbits on their farms and woods ended the 17th-c. trade there (Bettey) [firm]; the 1389-90 statute barred the poor from dogs, ferrets, nets and "other engines" (hunting_ladder §2.5) |
| **the deer park** | about 570 food a km² a year against 50 to 120 wild (hunting_ladder §2.2) | commoners' hunting and the forest's deer (the deer leap drew forest deer in, not out: 02zr) | forest law, licences to empark |
| **the dovecote** | about 2 food a unit (hunting_ladder §1.6) | the peasants' grain | a lord's right; the grievance of 1789 (02zzj/02) |
| **the fishpond** | Laperrière-sur-Saône in Burgundy took 11,000 full-grown carp, 31,000 young and 400 pike from one pond in 1345 [firm, secondary] | fresh fish became a lord's and a monastery's good; pike a mark of rank (a 2021 study of 11 English sites) [firm] | upkeep: draining, cleaning, restocking, walls against poachers [firm, Sheffield Cistercian pages] |

### 4c. Methods that replaced others, and why

| From | To | When | Why |
|---|---|---|---|
| fresh-water fish | sea fish (herring, cod) | within a few decades of AD 1000 in England, seen in 127 bone assemblages (Barrett, Locker and Roberts 2004) [firm] | rising demand from towns and falling fresh-water stocks, not more sea fish (the North Sea was probably poorer then) [firm, York press release]; later work adds long-range trade in dried cod [firm]. The evidence holds |
| bone and antler hooks | iron hooks | Iron Age to Viking age in the north; iron hooks 800 to 1000 in Norway [firm] | iron hooks "easy and cheap to produce" and made to last [firm]: a lower cost a hook once there is a smith |
| open fowling, nets at flight, the moult drive | the duck decoy | 1620s onward (Sir William Woodhouse under James I is said to have built the first [firm, secondary]) | a steady 1,000 to 3,000 birds a season for one man and a dog against a yearly pulse that emptied the breeding stock; then drainage ended both |
| wicker traps | net fykes, then plastic | no dated medieval switch found; side by side into the 20th c. | net is lighter and folds; wicker needs no cord |
| sun salt | boiled salt, then rock salt | | all-year supply and higher output; the fuel then bound salt to the woods |
| bark tanning | chrome tanning | 1858 onward | days instead of months; leather left the woods (02zzj/03 §6.4) |
| rushlights and tallow | wax for the rich, then oil and paraffin | | brightness and cost |
| salmon of the southern rivers | Scottish salmon | late Middle Ages | the southern runs declined under mills [firm, Arcadia] |

The pattern: a replacement wins when it lowers the cost per catch once a new capital exists (iron, the decoy, chrome), or when the old
stock fails (fresh-water fish, southern salmon). The old way usually goes on beside the new for a long time at a smaller scale, as
the quern did beside the mill (02zzj/01).

### 4d. Harms across ladders

| Cause | Harm | Case |
|---|---|---|
| retting flax and hemp in water | oxygen gone, dead fish, beasts' water fouled | an Act of Henry VIII forbade putting hemp or flax in rivers where beasts were watered, allowing pits [firm, local history; the chapter not found; 24 Hen. VIII c. 4 (1532) the likeliest]; the Severn Act of 1678 (fibre_and_cord §2) |
| flax and hemp | grain land and manure | fibre against food (02zzj/01 §2.9) |
| tanning, glue-boiling | the water below; towns zoned them downstream and downwind | 02zzj/03 §6.1 |
| mill dams | salmon runs blocked, gravel destroyed | Radboud 2016 [firm] |
| warrens, dovecotes | rabbits and pigeons on neighbours' crops | Bettey; 1789 grievance |
| deer and beasts in the coppice | the withy and pole regrowth dies | 02zzj/03; the engine's own sign |
| draining a wet meadow | pasture up, eels and fowl down | environment_systems §3 |

### 4e. Sustainability

| Method or rule | How it treats the stock |
|---|---|
| the rod and hook | selective: a hook of a size takes fish of a size; one at a time |
| mesh minimums | London's 1.5 to 2 inches (1329, 1343) let small fish through: selective by rule |
| fry nets, fine kidels | indiscriminate: banned in 1389 |
| the weir with its gap shut | takes a share of everything passing; the gap (1285) and the weekly slop let spawners through: escapement by rule |
| the close season | salmon from 1285; moulting wildfowl and their eggs from 1534 ("to avoide distruction of wilde fowle", hunting_ladder §1.6) |
| the moult drive | 3,000 to 4,000 birds at one drive: it empties the breeding stock |
| the decoy | takes migrants from beyond the region in winter: locally sustainable, as long as the flyway holds |
| the withy bed, the coppice | managed: a bed lives about 30 years if cut each winter and kept from beasts; wild willow cut too often or grazed fails (withies_wood_materials §1.1) |
| the park, the warren, the pond | sustainable by design: a kept stock culled to its increase; the cost is the pale, the keeper and the law |

### 4f. What the engine already lets emerge, and what it lacks

Read from the code on main (21 Nov): `cybertron2/wild/runs.py`, `wild/gear.py`, `engine/wild.py` (`_runs_night`, `_dam_stops`),
`wild/kinds.py` (RUNS, the eel's row), `wild/ecology.py` (migrants, wariness), `engine/waters.py` ([[D2-229 One fish stock per water body|D2-229]]).

| Real effect | In the engine? | How (file) |
|---|---|---|
| **escapement sets next year's salmon** | **yes** | an up-run returns from the spawners that reached their stretch a year before, Beverton-Holt (`r` 2.0 a spawner, at most `cap_km` 6 a km of river; `runs.advance`), so every salmon a weir or a net takes below is fewer next year. The signs "the run was thin this year ... about {share} of last year's" exist (RUN_SIGNS thin, good) |
| **a mill dam blocks the run** | **yes, in part** | a shut mill gap holds `stop` 0.5 of an up-run as it arrives; held fish go back to the sea and never spawn (`_dam_stops`, `runs.advance`). Gravel destroyed for centuries: no |
| **eel escapement** | no, and rightly | the eel's stock is made up by `b` 3.0 standing for elvers from the sea (kinds.py), not by the silver eels that got away; the real eel is one ocean-spawning stock, so local escapement does not set local recruitment |
| **upstream first for eels, downstream first for salmon** | **yes** | `gear.py`: between parcels a down-run passes the gear upstream first, an up-run downstream first; between villages the pulses move stretch by stretch with a lag, so the upper village takes the eels first and the lower the salmon first |
| **gear sharing a run** | **yes** | weirs, the race trap and set traps at one stretch share what passes, each capped by its hold (`gear.share_run`) |
| **the gap** | yes, as an act | open or shut by a person (a share x `open` 0.1 open); no weekly or seasonal custom; nothing makes a person keep it |
| **close times, mesh rules, the slop** | no | agreements exist, but nothing checks a take against one; a close time can only be a habit people choose |
| **resident fish shared by every method** | **yes** | one stock per lake or reach, fished from every parcel on it ([[D2-229 One fish stock per water body|D2-229]]; `waters.py`); a heavy method thins everyone's catch. The shallows as their own stock: proposed ([[W-73 Fishing, hunting and their materials developed together|W-73]] §4) |
| **one hunter's pressure on another's** | **yes** | the wild methods draw one population; learned wariness and short-lived pressure raise flight for everyone after a kill (`ecology.py`) |
| **over-taking the winter fowl** | yes, roughly | next winter's flocks scale with how many left last spring (`back` 0.3 to 1.2; `ecology.py`); for a real flyway this is stronger than life |
| **the decoy's quiet zone** | no | no disturbance a method leaves on a place for others; needs a new rule (a method's `disturbs` on a parcel for a night) |
| **gear that selects by size** | no | each kind is one size; a net's mesh and a hook's size cannot spare the young; needs age or size classes or a share spared by the gear |
| **retting, tanning and glue fouling the water** | no | environment_systems lists fouling as a flow along `down`, not built; needs a water state read by the fish kinds |
| **kept stocks (park, warren, pond, dovecote)** | no | pack K6 and core C8 ([[L-119 Wildlife pack K6 keeping|L-119]], [[L-126 The wildlife's core mechanisms not built|L-126]]) |
| **rabbits or pigeons of a lord on the crops** | partly | wild raiders on fields exist (the woodpigeon raids); kept rabbits or doves are not kinds |
| **flax against grain** | will emerge | once flax is a crop on the farming verbs, it competes for plots and manure with no new rule |
| **a shared work's rent or toll** | no rule | left to agreements (economy_web question 3) |

So: the capture of a run by position and by a weir, the mill's block on salmon, the shared resident stock and the shared game are
already emergent; what is needed for the rest are three general rules, not per-kind code: **fouling** carried down the water,
**disturbance** a method leaves on a place, and **sparing** by gear (a share of the young or the small let through), with close
times and mesh rules as customs people can agree and break. Each belongs to a later phase; none is needed for [[W-73 Fishing, hunting and their materials developed together|W-73]]'s phases 1 to 4.

---

## 5. Records to add (for 37.2, not done here)

- A deferred row: **fish oil** with the coast (K9, [[L-122 Wildlife pack K9 coast and cliff|L-122]]), with Zach's "seems potentially valid" (14 Nov).
- A deferred row: **eel skin, fish glue** with K8 ([[L-121 Wildlife pack K8 crafts and wild goods|L-121]]), with Zach's "maybe later" (14 Nov).
- A deferred row or a line in the proposal: **offal's uses** (bait, dog food) and **peat** as fuel.
- In the proposal's open questions: the two layers of skill in dressing (§3a, choice 3), cord's three paths, and §4f's three
  general rules (fouling, disturbance, sparing) as later work.

---

## Sources

**In the repository:** the proposals and notes named in §1; this folder's five notes; 02zzx_salting_rates.md; the code files named in
§4f.

**On the web (search summaries; no page fetched):**
- Fish and the AD 1000 shift: [Barrett, Locker and Roberts 2004, White Rose eprint](https://eprints.whiterose.ac.uk/1317/1/barrettjh1.pdf); [York press release 2004](https://www.york.ac.uk/news-and-events/news/2004/fishing/); [Medievalists.net summary](https://www.medievalists.net/2009/12/the-origins-of-intensive-marine-fishing-in-medieval-europe-the-english-evidence/).
- Weirs and law: [Magna Carta Project, clause 33](https://magnacarta.cmp.uea.ac.uk/read/magna_carta_1215/Clause_33); [Canal & River Trust, early fisheries law](https://canalrivertrust.org.uk/enjoy-the-waterways/fishing/related-articles/the-fisheries-and-angling-team/the-early-history-of-salmon-and-freshwater-fisheries-law); [Arcadia, rioting townsmen destroy an abbey's salmon weir](https://www.environmentandsociety.org/arcadia/rioting-townsmen-destroy-abbeys-salmon-weir-medieval-scotland); [BAILII, Saturday's Slop, 1684](https://mansfield.bailii.org/scot/cases/ScotCS/1684/Mor3314286-021.html); [Legal Genealogist, Saturday's stop](https://legalgenealogist.com/?p=18956); [Salmon and Freshwater Fisheries (Consolidation) (Scotland) Act 2003, close times](https://www.legislation.gov.uk/asp/2003/15/part/1/crossheading/close-times-for-salmon?view=plain); [Memorials of London, 1329](https://prod.british-history.ac.uk/node/49302); [Memorials, 1343](https://prod.british-history.ac.uk/node/49314); [Memorials, 1349](https://www.british-history.ac.uk/node/49320); [Eel buck](https://en.wikipedia.org/wiki/Eel_buck).
- Mills and salmon: [phys.org, medieval water power initiated the collapse of salmon stocks (2016)](https://phys.org/news/2016-07-medieval-power-collapse-salmon-stocks.html).
- Fowling: [Essex Field Club archive text on decoys](https://essexfieldclub.org.uk/archivetext.php/s/054/o/0053); [Duck decoy (structure)](https://en.wikipedia.org/wiki/Duck_decoy_(structure)).
- Warrens: [Breckland Society, Lakenheath warren](https://brecsoc.org.uk/?p=187); [Country Life via PressReader, the Normans' rabbit conquest](https://www.pressreader.com/uk/country-life/20220413/282140704913093); [Bettey, rabbits in Wiltshire, Antiquaries Journal](https://resolve.cambridge.org/core/journals/antiquaries-journal/article/abs/production-of-rabbits-in-wiltshire-during-the-seventeenth-century/ED022FEA9298E7027BF8F9DD25D22161); [Medievalists.net, the rabbit and the medieval East Anglian economy](https://www.medievalists.net/2012/06/the-rabbit-and-the-medieval-east-anglian-economy/); [English Heritage, Thetford Warren Lodge](https://www.english-heritage.org.uk/visit/places/thetford-warren-lodge/history/rabbits-warreners); [Rabbiting](https://en.wikipedia.com/wiki/Rabbiting).
- Fishponds: [Sheffield, Cistercian water](https://cistercians.shef.ac.uk/cistercian_life/environment/water/water3.php); [Archaeological and Anthropological Sciences 2021, pike and status](https://link.springer.com/article/10.1007/s12520-021-01373-6); [Archaeofauna, Laperrière-sur-Saône](https://revistas-new.uam.es/archaeofauna/article/download/8412/8783/18193).
- Eels: [History Hit, eels in medieval England](https://www.historyhit.com/paid-in-fish-strange-uses-for-eels-in-medieval-england/); [Shooting Times, eel traps](https://www.pressreader.com/uk/shooting-times-country-magazine/20200520/282218012981723); [FAO, fish traps](https://www.fao.org/4/aa043b/AA043B06.htm); [Corf](https://www.wikipedia.org/wiki/Corf); [Tides and Tales, eel boxes](https://tidesandtales.ie/echoes-of-medieval-fishing-in-waterford/).
- Keeping fish: [Stockfish](https://www.wikipedia.org/wiki/Stockfish); [Norwegian intangible heritage, stockfish](https://www.immateriellkulturarv.no/en/bidrag/the-cultural-and-culinary-traditions-of-stockfish/); [Nofima, end-drying stockfish](https://nofima.com/publication/1578556/); [Cooksinfo, red herrings](https://www.cooksinfo.com/red-herrings); [Kipper](https://en.wikipedia.org/wiki/Kipper); [NOAA leaflet 196](https://fisherybulletin.nmfs.noaa.gov/sites/default/files/legacy-pdfs/leaflet196.pdf); [Albion, the English fishing industry: Great Yarmouth](https://cambridge.org/core/journals/albion/article/english-fishing-industry-in-the-sixteenth-century-the-case-of-great-yarmouth/463E8A679AD605AFC36F8EA977F04520).
- Oil and light: [Cod liver oil](https://EN.wikipedia.com/wiki/Cod_liver_oil); [Science History Institute, the man with a fish on his back](https://www.sciencehistory.org/distillations/the-man-with-a-fish-on-his-back); [Rushlight](https://en.wikipedia.org/wiki/Rushlight); [Modern Reenactor, rushlights](https://modernreenactor.blogspot.com/2022/01/darkness-visible-rushlight-background.html); [Sapoznik 2019, wax in England](https://ideas.repec.org/a/bla/ehsrev/v72y2019i4p1152-1174.html).
- Hides and glue: [Richter and Dettloff 2002](https://www.uwlax.edu/globalassets/offices-services/urc/jur-online/pdf/2002/richter_and_dettloff.pdf); [The Furrow, December 2025](https://www.deere.com/en/publications/the-furrow/2025/december-2025/hiding-place); [Outdoor Life, brain tanning](https://www.outdoorlife.com/blogs/survivalist/2011/11/survival-skills-brain-tanning-hides/); [Alum leather, CAMEO](https://cameo.mfa.org/wiki/Alum_leather); [ethnographic note on processing skin](https://vmek.oszk.hu/02700/02790/html/97.html); [Williamsburg leatherworker](https://pascalbonenfant.com/18c/crafts/leatherworker.html); [Animal glue, CAMEO](https://cameo.mfa.org/wiki/Animal_glue); [Bone glue](https://www.wikiwand.com/en/articles/Bone_glue).
- Salt: [Historic England, pre-industrial salterns](https://cms.historicengland.org.uk/images-books/publications/iha-preindustrial-salterns/heag225-pre-industrial-salterns); [Lincolnshire HER, Spalding saltern](https://heritage-explorer.lincolnshire.gov.uk/Monument/MLI84750); [Wainfleet report](https://archaeologydataservice.ac.uk/catalogue/adsdata/arch-1045-1/dissemination/pdf/1145_StMichaelsLane_Wainfleet.pdf).
- Peat: [RTÉ Brainstorm, turf cutting](https://www.rte.ie/brainstorm/2022/0426/1206028-bogs-turf-cutting-culture-climate-change-ireland); [Ask About Ireland, cutting turf](https://askaboutireland.ie/learning-zone/primary-students/looking-at-places/offaly/aspects-of-offaly/cutting-turf).
- Retting law: [Haxey Walkers, linen and hemp in the Isle](https://www.haxeywalkers.co.uk/linen-and-hemp-in-the-isle/); [24 Hen. 8](https://www.wikiwand.com/en/articles/24_Hen._8).
- Boats: [Southampton, logboat repairs](https://eprints.soton.ac.uk/447234/1/Logboat_Repairs_.pdf); [EXARC, Prometheus logboat](https://exarc.net/ark:/88735/10176); [Coracle](https://www.Wikipedia.com/wiki/Coracle); [Mother Earth News, how to build a coracle](https://www.motherearthnews.com/diy/how-to-build-a-coracle-zmaz03amzgoe/); [Royal Museums Greenwich, Teifi coracle](https://www.rmg.co.uk/collections/objects/rmgc-object-11470).
- Hooks: [The Viking World, iron fishhook](https://scalar.usc.edu/works/viking-world/iron-fishhook); [World History Encyclopedia, Viking iron fishing hooks](https://www.worldhistory.org/image/9704); [EXARC 2020, bone fishhooks](https://doaj.org/article/61fdf7b3d4354ab293f54fd3dece7965).
- Fish garths and weirs: [Yorkshire Dialect Dictionary, fish-garth](https://yorkshiredictionary.york.ac.uk/words/fish-garth); [Nayling 1999, medieval fish weirs](https://archaeologydataservice.ac.uk/catalogue/adsdata/arch-2776-1/dissemination/pdf/VOL_10_1999/Nayling_1999_Medieval_and_Later_Fish_Weirs.pdf).

**Recalled, not checked this session:** eel fat about 12% raw (USDA); peat's heat about half of dry wood's by weight; barrel hoops of
hazel or willow; the cruisie lamp burning fish oil; Berners (1496) on horsehair lines; fermented fish as Nordic practice.

## History

- **21 Nov 2026:** written by 37.2 (subagent) at Zach's two asks of 21 Nov (what we had looked into and the substitutes; whether
  the ladders merge, push out and replace each other, and their sustainability).
