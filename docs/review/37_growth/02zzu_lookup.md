# 02zzu lookup: the food values checked against USDA FoodData Central

37.2, 20 Nov 2026. The check that putting the food values on one physical basis (D2-258) asks for before the data change: every
food good and animal of [02zzu_shared_units](02zzu_shared_units.md) (its table, [the JSON](02zzu_shared_units.json)), every good in
`cybertron2/engine/data.py` ITEMS with food above 0, and the wild layer's kinds (`cybertron2/wild/kinds.py` TAKEN and the colonies'
takes), read on `main` (`3b1e906c`), each against the closest food in USDA FoodData Central's **SR Legacy** release (April 2018).
The verdict follows the rule that a value within about 20% of its FoodData Central figure is kept (D2-259).

**Files:** the script [02zzu_lookup.py](02zzu_lookup.py) (`python3 -I 02zzu_lookup.py SR_CSV_DIR FOOD_DES.txt [CYB_ROOT]`), the
machine-readable result [02zzu_lookup.json](02zzu_lookup.json) (every SR row used, with its fdc_id, NDB number, kcal, refuse and
its role: match, proxy or check). Nothing else was changed; no engine state was touched.

**How each value is checked:**
- **Energy** is SR nutrient 1008 (number 208, kcal a 100 g), from the FDC CSV release. **Refuse** (the inedible share: shell,
  bone, stalks) is not in the FDC CSV files; it is SR28's `FOOD_DES` Refuse field, read from the USDA file as copied in
  github.com/alyssaq/usda-sqlite (`data/FOOD_DES.txt`; ars.usda.gov could not be reached from here). Every row used was
  cross-checked by its description against SR Legacy's `food.csv`: all match.
- **The food a unit** = kcal a 100 g × 10 × the edible share ÷ 2,500, for a unit of 1 kg as gathered or kept, with 02zzu's units,
  its weights within a mix (equal where it gave none) and its edible shares where SR gives none (SR records refuse 0 for foods it
  lists already prepared: blanched nettles, pitted wild plums, rose hips, hulled grain).
- **02zzu's design factors and rules are kept as they are**, applied to the checked physical value: the grain ladder (bread = the
  flour's energy less 2% in baking; grain and rye 0.7/1.3 of bread, meal and flour 1.0/1.3; D2-60, D4-107), beans at 0.53 of
  their physical value, raw acorns at 0.035 (tannin), tallow at 0, meat and fish units defined by energy (1,500 and 1,150 kcal),
  the kept goods by rule 5 (dried and smoked ×2, salt meat ×0.95), the raw values at the game's raw/cooked ratio. Those factors
  are 02zzu's proposals, not decisions; the check does not test them, only the food beneath them.
- **Animals:** the flesh from SR's raw meat or fish; the live weight and dressing share from 02zzu (its sources: Mitchell et al.
  for deer, Albarella for medieval cattle, Tesch for eels; estimates for the kinds 02zzu did not have); the edible share of the
  carcass from SR's carcass or ready-to-cook refuse where SR gives one (beef, veal, squab, wild duck, stewing hen, brook trout),
  else 02zzu's.
- **The verdict (D2-259)** compares the game's value now with the checked value: keep within 20%, change beyond it, "borderline"
  within 3 points of the line. For the animals it is the food a head (the engine's goods × the game's value a unit); since meat
  and fish change their value a unit, the goods a head change with them in any case (the column "goods a head on the checked
  unit"). The brief's flag (a move over 10% against 02zzu) is the column ">10%".

## The changes (beyond 20%, D2-259)

**Goods (26 of 37):**

| Good | Now | Proposed (food a unit) | Now against checked |
|---|---|---|---|
| meat; drying meat; smoking meat | 1.5 (raw 0.8) | 0.6 (raw 0.32) | 2.5 times |
| dried meat; smoked meat | 3.0 | 1.2 | 2.5 times |
| salt meat | 1.4 (raw 0.6) | 0.57 (raw 0.24) | 2.46 times |
| fish; salt fish; drying fish; smoking fish | 1.0 (raw 0.6) | 0.46 (raw 0.28) | 2.17 times |
| dried fish; smoked fish | 2.0 | 0.92 | 2.17 times |
| milk | 0.5 | 0.256 | +95% |
| cheese | 2.5 | 1.61 | +55% |
| greens | 0.6 | 0.098 | 6.1 times |
| roots (on SR proxies) | 0.8 (raw 0.4) | 0.263 (raw 0.13) | 3.0 times |
| mushrooms | 0.6 (raw 0.3) | 0.107 (raw 0.053) | 5.6 times |
| watercress | 0.4 | 0.041 | 9.9 times |
| samphire (on an SR proxy) | 0.5 (raw 0.4) | 0.061 (raw 0.049) | 8.2 times |
| berries | 0.8 | 0.167 | 4.8 times |
| hedge fruit | 0.6 (raw 0.3) | 0.33 (raw 0.165) | +82% |
| hazel nuts | 1.6 | 1.03 | +55% |
| acorns (raw, with 02zzu's tannin factor 0.035) | 0.1 | 0.034 | 3.0 times; the factor is a design choice, not a food figure |
| wild food (the legacy autumn mix) | 1.0 | 0.41 | 2.4 times |
| green grain, green rye (no FDC figure) | 0.15 | 0.24 on 02zzu's estimate | -38%: not an FDC check |

**Animals (15 of 16 engine kinds; food a head, and the goods a head that give it on the checked unit):**

| Kind | Engine goods | Food a head now | Checked food a head | Goods a head on the checked unit |
|---|---|---|---|---|
| red deer | 20 meat | 30 | 19.8 | 32.9 meat |
| roe deer | 4.5 meat | 6.75 | 4.9 | 8.1 meat |
| wild boar | 15 meat | 22.5 | 17.3 | 28.8 meat |
| brown hare (wild rabbit proxy) | 0.7 meat | 1.05 | 0.75 | 1.25 meat |
| woodpigeon (squab proxy) | 0.1 meat | 0.15 | 0.092 | 0.15 meat |
| wildfowl | 0.3 meat | 0.45 | 0.33 | 0.56 meat |
| eel | 0.2 fish | 0.2 | 0.265 | 0.58 fish |
| salmon | 2.0 fish | 2.0 | 1.41 | 3.06 fish |
| lamprey (eel proxy) | 0.3 meat | 0.45 | 0.088 | 0.19 fish |
| cow | 40 meat | 60 | 102 | 170 meat |
| ox, bull | 50 meat | 75 | 141 | 235 meat |
| young | 10 meat | 15 | 29 | 48 meat |
| young heron, from the nest (squab proxy) | 0.3 meat | 0.45 | 0.22 | 0.37 meat |
| young rook, from the nest (squab proxy) | 0.12 meat | 0.18 | 0.065 | 0.11 meat |

The brown bear is kept on food a head (60 now against 72.5 checked, -17%, borderline), but with meat at 0.6 a unit its goods must
rise from 40 to 121 meat to keep it.

**Kept (within 20%):** grain, rye, meal, flour and bread (all within 1% on the ladder); beans (-20%, borderline, with 02zzu's 0.53
factor; D2-53's "less food"); green beans (-12%); beech nuts (-15%); acorn meal (-18%, borderline: 02zzu's 1.48 is not needed);
tallow (0, design); the egg (+19%, borderline) **only if** the egg unit becomes 1 kg: the game's egg weighs 0.1, so a unit as
weighed now is 0.05 food against 0.6 (12 times). The laying rate's `EGG_FOOD` (0.02 an egg, `engine/wild.py`) is 0.025 for a 50 g
egg (-20%, borderline change) and 0.023 for a 45 g one (keep).

## What moved more than 10% against 02zzu

| Value | 02zzu | Checked | Move | Why |
|---|---|---|---|---|
| green beans | 0.216 | 0.341 | +58% | SR's young broad beans in the pod (88 kcal, 3% refuse) are eaten whole; 02zzu took 90 kcal with 0.4 lost. Shelled seeds (11088, 72 kcal, pods about 0.35 seed) would give about 0.10 |
| hedge fruit | 0.21 | 0.33 | +57% | SR's crab apple is 76 (8% refuse), wild plum 91, wild rose hips 162; 02zzu's mid was 75 a 100 g at 0.7 eaten. Without the hips it is 0.27 (+27%) |
| wild boar (a head) | 22.7 | 17.3 | -24% | SR's wild boar is 122 kcal; 02zzu raised it to 160 for autumn fat (an estimate SR does not support) |
| samphire | 0.075 | 0.061 | -19% | purslane proxy (20 kcal, 24% refuse) against 02zzu's estimate 22 at 0.85 |
| acorns (raw) | 0.041 | 0.034 | -18% | SR's shell share is 38% (02zzu 25%) |
| acorn meal | 1.48 | 1.22 | -17% | the same shell share through 02zzu's rule (3 acorns make 2 meal, 15% lost in leaching) |
| greens | 0.112 | 0.098 | -12% | sorrel's genus (dock) is 22 kcal with 30% stalks; ramsons have no SR row |
| cow, ox (a head) | 91, 126 | 102, 141 | +12% | SR's carcass refuse is 20% bone (02zzu 30%); the flesh is SR's grass-fed beef (198, against 02zzu's 200). With 02zzu's 0.70 the cow is 90 (-1%): the move is the edible share alone, and a modern select carcass is meatier than a medieval cow's, so 02zzu's 0.70 may be the better figure |

Everything else is within 10% of 02zzu: the grain ladder 3% lower (whole-grain flour 340 at 0.97 extraction), beans 3% higher
(split peas are 364, not 341), mushrooms -7%, watercress +10% (8% refuse, 02zzu 15%), hazel nuts -5% (59% shell), beech nuts +2%,
the eel, salmon, deer, hare and bear unchanged (02zzu's kcal were SR's), the pigeon -7%, wildfowl +6%, the lamprey -8%, the
young beast -5%.

**02zzu's citations that were wrong** (its values were mostly right): beech nuts cited 12014, which is pumpkin seed kernels (the
beechnut row is NDB 12077, fdc 170161); wild boar 17165, which is roasted venison (the boar is 17158, fdc 175297); the hare's
rabbit 17178, roasted domestic rabbit (wild raw is 17180, fdc 174347); the woodpigeon 05153, pheasant (squab meat is 05161, fdc
171079); wildfowl 05141, domestic duck meat (wild duck is 05144 and 05145, fdc 174468 and 174469); rose hips 09136, no such row
(35203, fdc 168998); split peas 341 (SR has 364).

## No SR Legacy match

| Good or kind | What SR lacks | What is used here (marked in the JSON) |
|---|---|---|
| samphire | Salicornia | proxy: purslane raw (11427, fdc 169274), 20 kcal, 24% refuse. No Salicornia composition table was looked up here (the other sources found are not reachable from this environment); 02zzu's estimate was 15 to 30 kcal |
| roots | pignut (Conopodium), silverweed (Potentilla anserina) | proxies: parsnip, burdock, salsify, arrowhead (72 to 99 kcal, 13 to 25% refuse) |
| lamprey | any lamprey | proxy: eel raw (184 kcal); 02zzu estimated 200 |
| brown hare | hare | wild rabbit raw (114) |
| woodpigeon; young herons and rooks | wild pigeon, heron, rook | squab meat only (142, 35% refuse of the dressed bird); live weights of the young birds are estimates |
| green grain, green rye | immature cereal | none: 02zzu's estimate (40 to 90 kcal) stands, and the verdict is not an FDC check |
| greens | ramsons | left out of the mix (nettles and dock only) |
| mushrooms | ceps (Boletus) | left out (chanterelle and white mushroom) |
| hedge fruit | sloes, haws | sloes by wild plum (pitted, 02zzu's stone share 0.3); haws left out |
| berries | bilberry, wild strawberry | cultivated blueberry and strawberry |
| all whole fish but brook trout | the edible share of a whole fish | 02zzu's (FAO yields): eel 0.72, salmon 0.62 |
| deer, boar, bear, hare | the carcass's edible share | 02zzu's (0.70 to 0.75) |

## Three things the check turns up besides the values

1. **What a unit of fish is.** 02zzu's fish unit is 1,150 kcal, about 1 kg gutted and headed. SR's brook trout (fdc 175181) gives
   53% refuse for a whole fish, so a kilogram as caught is 0.21 food, under half the unit. Where the engine counts a fish stock in
   kilograms (`K`, OPEN L-75), the stock's food falls by that again unless the unit is read as gutted weight.
2. **The kept goods' rules** (dried and smoked ×2) are not testable in SR: its smoked fish are modern hot-smoked and not dried
   (whitefish 108 against 134 raw, kippered herring 217 against 158), its dried beef is 57% water (153), its salt cod is hard
   dried (290 against 82 fresh, ×3.5). They neither confirm nor refute "half the weight".
3. **The egg unit** (above) and **the killed hen**: the engine kills hens (raids) and gives no meat for one; a stewing hen of
   1.2 kg (SR 05123, 258 kcal, 30% bone) is about 0.6 food.

## The tables

kcal/100 g is SR's for each row used; "Refuse (edible)" is SR's refuse and the edible share used (with its source when not SR).
"Checked a unit" is the value on the basis at 2,500 kcal, after 02zzu's factor or rule. "vs 02zzu" is checked over 02zzu less 1;
"Game now vs checked" is the game's value over checked less 1.

### Goods

| Good | Game now | 02zzu | USDA SR Legacy (fdc_id: description) | kcal/100 g | Refuse (edible) | Checked a unit | vs 02zzu | >10% | Game now vs checked | D2-259 |
|---|---|---|---|---|---|---|---|---|---|---|
| grain | 0.7 (raw 0.2) | 0.717 | 170283: Barley, hulled; 168890: Wheat, hard red winter; 169705: Oats | 354; 327; 389 | 0% (0.92, 02zzu); 0% (0.92, 02zzu); 0% (0.92, 02zzu) | **0.696** (raw 0.199) | -3% |  | +1% | keep |
| rye | 0.7 (raw 0.2) | 0.717 | 168884: Rye grain | 338 | 0% (1, whole) | **0.696** (raw 0.199) | -3% |  | +1% | keep |
| beans | 0.6 (raw 0) | 0.723 | 175205: Broadbeans (fava beans), mature seeds, raw; 172428: Peas, green, split, mature seeds, raw | 341; 364 | 0% (1, whole); 0% (1, whole) | **0.747** (raw 0) | +3% |  | -20% | keep (borderline) |
| meal | 1 (raw 0.5) | 1.02 | 168893: Wheat flour, whole-grain; 169739: Barley flour or meal | 340; 345 | 0% (1, whole); 0% (1, whole) | **0.995** (raw 0.497) | -3% |  | +1% | keep |
| flour | 1 (raw 0.5) | 1.02 | 168893: Wheat flour, whole-grain | 340 | 0% (0.97, 02zzu) | **0.995** (raw 0.497) | -3% |  | +1% | keep |
| bread | 1.3 | 1.33 | checked against: 172688: Bread, whole-wheat, commercially prepared | 252 | - | **1.29** | -3% |  | +1% | keep |
| green grain | 0.15 | 0.24 | none (rule or estimate) | - | - | **0.24** | +0% |  | -38% | no FDC figure: change on 02zzu's estimate |
| green rye | 0.15 | 0.24 | none (rule or estimate) | - | - | **0.24** | +0% |  | -38% | no FDC figure: change on 02zzu's estimate |
| green beans | 0.3 | 0.216 | 168574: Beans, fava, in pod, raw | 88 | 3% (0.97) | **0.341** | +58% | yes | -12% | keep |
| meat | 1.5 (raw 0.8) | 0.6 | checked against: 173855: Game meat, deer, raw; 175297: Game meat, boar, wild, raw; 174347: Game meat, rabbit, wild, raw; 173845: Game meat, bear, raw; 168608: Beef, grass-fed, ground, raw; 173815: Veal, composite of trimmed retail cuts, separabl | 120; 122; 114; 161; 198; 144 | - | **0.6** (raw 0.32) | +0% |  | +150% | change to 0.6 |
| fish | 1 (raw 0.6) | 0.46 | checked against: 175154: Fish, trout, rainbow, wild, raw; 173680: Fish, pike, northern, raw; 173678: Fish, perch, mixed species, raw; 171952: Fish, carp, raw; 174193: Fish, eel, mixed species, raw; 173686: Fish, salmon, Atlantic, wild, raw | 119; 88; 91; 127; 184; 142 | - | **0.46** (raw 0.276) | +0% |  | +117% | change to 0.46 |
| dried meat | 3 | 1.2 | checked against: 170604: Beef, cured, dried; 167536: Snacks, beef jerky, chopped and formed | 153; 410 | - | **1.2** | +0% |  | +150% | change to 1.2 |
| smoked meat | 3 | 1.2 | none (rule or estimate) | - | - | **1.2** | +0% |  | +150% | change to 1.2 |
| drying meat | 1.5 (raw 0.8) | 0.6 | none (rule or estimate) | - | - | **0.6** (raw 0.32) | +0% |  | +150% | change to 0.6 |
| smoking meat | 1.5 (raw 0.8) | 0.6 | none (rule or estimate) | - | - | **0.6** (raw 0.32) | +0% |  | +150% | change to 0.6 |
| salt meat | 1.4 (raw 0.6) | 0.57 | checked against: 170199: Beef, cured, corned beef, brisket, raw | 198 | - | **0.57** (raw 0.244) | +0% |  | +146% | change to 0.57 |
| salt fish | 1 (raw 0.6) | 0.46 | checked against: 174190: Fish, cod, Atlantic, dried and salted | 290 | - | **0.46** (raw 0.276) | +0% |  | +117% | change to 0.46 |
| drying fish | 1 (raw 0.6) | 0.46 | none (rule or estimate) | - | - | **0.46** (raw 0.276) | +0% |  | +117% | change to 0.46 |
| smoking fish | 1 (raw 0.6) | 0.46 | none (rule or estimate) | - | - | **0.46** (raw 0.276) | +0% |  | +117% | change to 0.46 |
| dried fish | 2 | 0.92 | checked against: 174190: Fish, cod, Atlantic, dried and salted | 290 | - | **0.92** | +0% |  | +117% | change to 0.92 |
| smoked fish | 2 | 0.92 | checked against: 173712: Fish, whitefish, mixed species, smoked; 173668: Fish, herring, Atlantic, kippered | 108; 217 | - | **0.92** | +0% |  | +117% | change to 0.92 |
| milk | 0.5 | 0.256 | 171266: Milk, producer, fluid, 3.7% milkfat | 64 | 0% (1, whole) | **0.256** | +0% |  | +95% | change to 0.256 |
| cheese | 2.5 | 1.6 | 173414: Cheese, cheddar | 403 | 0% (1, whole) | **1.61** | +1% |  | +55% | change to 1.61 |
| egg | 0.6 (raw 0.5) | 0.503 | 171287: Egg, whole, raw, fresh | 143 | 12% (0.88) | **0.503** (raw 0.419) | +0% |  | +19% | keep (borderline) |
| greens | 0.6 | 0.112 | 169819: Stinging Nettles, blanched (Northern Plains Indians); 170076: Dock, raw | 42; 22 | 0% (0.8, 02zzu); 30% (0.7) | **0.098** | -12% | yes | +512% | change to 0.098 |
| roots | 0.8 (raw 0.4) | 0.256 | 170417: Parsnips, raw (proxy); 169974: Burdock root, raw (proxy); 169277: Salsify, (vegetable oyster), raw (proxy); 169203: Arrowhead, raw (proxy) | 75; 72; 82; 99 | 15% (0.85); 25% (0.75); 13% (0.87); 25% (0.75) | **0.263** (raw 0.132) | +3% |  | +204% | change (on an SR proxy) to 0.263 |
| mushrooms | 0.6 (raw 0.3) | 0.115 | 168422: Mushrooms, Chanterelle, raw; 169251: Mushrooms, white, raw | 32; 22 | 0% (1); 3% (0.97) | **0.107** (raw 0.0533) | -7% |  | +462% | change to 0.107 |
| watercress | 0.4 | 0.037 | 170068: Watercress, raw | 11 | 8% (0.92) | **0.0405** | +10% |  | +888% | change to 0.041 |
| samphire | 0.5 (raw 0.4) | 0.075 | 169274: Purslane, raw (proxy) | 20 | 24% (0.76) | **0.0608** (raw 0.0486) | -19% | yes | +722% | change (on an SR proxy) to 0.061 |
| berries | 0.8 | 0.171 | 173946: Blackberries, raw; 171711: Blueberries, raw; 167762: Strawberries, raw | 43; 57; 32 | 4% (0.96); 5% (0.95); 6% (0.94) | **0.167** | -2% |  | +378% | change to 0.167 |
| hedge fruit | 0.6 (raw 0.3) | 0.21 | 171721: Crabapples, raw; 169820: Plums, wild (Northern Plains Indians) (proxy); 168998: Rose Hips, wild (Northern Plains Indians) | 76; 91; 162 | 8% (0.92); 0% (0.7, 02zzu); 0% (0.7, 02zzu) | **0.329** (raw 0.165) | +57% | yes | +82% | change to 0.329 |
| hazel nuts | 1.6 | 1.08 | 170581: Nuts, hazelnuts or filberts | 628 | 59% (0.41) | **1.03** | -5% |  | +55% | change to 1.03 |
| beech nuts | 1.2 | 1.38 | 170161: Nuts, beechnuts, dried | 576 | 39% (0.61) | **1.41** | +2% |  | -15% | keep |
| acorns | 0.1 | 0.041 | 170157: Nuts, acorns, raw | 387 | 38% (0.62) | **0.0336** | -18% | yes | +198% | change to 0.034 |
| acorn meal | 1 (raw 0.3) | 1.48 | 170157: Nuts, acorns, raw | 387 | 38% (0.62) | **1.22** (raw 0.367) | -17% | yes | -18% | keep (borderline) |
| wild food | 1 | 0.414 | none (rule or estimate) | - | - | **0.411** | -1% |  | +144% | change to 0.411 |
| tallow | 0 | 0 | 171400: Fat, beef tallow | 902 | 0% (1, whole) | **0** |  |  | +0% | keep |

The meat and fish units are defined by energy, so their value is exact; the SR rows check the kcal a kg behind them (meat 114 to 198,
mean 143: a unit is 0.76 kg of beef to 1.3 kg of rabbit; fish 88 to 184, mean 125: 0.63 kg of eel to 1.3 kg of pike).

### Animals

| Kind | Engine goods a head | Game food a head now | 02zzu | Flesh: USDA SR Legacy | kcal/100 g (02zzu) | Live kg | Dressing | Edible of carcass (source) | Checked food a head | Goods a head on the checked unit | vs 02zzu | >10% | Now vs checked | D2-259 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| red deer | 20 meat | 30 | 19.764 | 173855: Game meat, deer, raw | 120 (120) | 90 | 0.57 | 0.75 (02zzu) | **19.764** | 32.94 meat | +0% |  | +52% | change |
| roe deer | 4.5 meat | 6.75 | 4.88 | 173855: Game meat, deer, raw | 120 (120) | 22 | 0.6 | 0.72 (02zzu) | **4.88** | 8.13 meat | -0% |  | +38% | change |
| wild boar | 15 meat | 22.5 | 22.669 | 175297: Game meat, boar, wild, raw | 122 (160) | 70 | 0.68 | 0.7 (02zzu) | **17.285** | 28.81 meat | -24% | yes | +30% | change |
| brown hare | 0.7 meat | 1.05 | 0.75 | 174347: Game meat, rabbit, wild, raw (proxy) | 114 (114) | 3.5 | 0.6 | 0.75 (02zzu) | **0.75** | 1.25 meat | +0% |  | +40% | change (on an SR proxy) |
| woodpigeon | 0.1 meat | 0.15 | 0.099 | 171079: Squab, (pigeon), meat only, raw (proxy) | 142 (142) | 0.5 | 0.5 | 0.65 (SR (squab meat only: 23% bone, 12% skin of the dressed bird)) | **0.092** | 0.15 meat | -7% |  | +62% | change (on an SR proxy) |
| wildfowl | 0.3 meat | 0.45 | 0.314 | 174468: Duck, wild, meat and skin, raw | 211 (170) | 1.1 | 0.6 | 0.6 (SR (wild duck meat and skin: 38% bone, 2% loss)) | **0.334** | 0.56 meat | +6% |  | +35% | change |
| brown bear | 40 meat | 60 | 72.45 | 173845: Game meat, bear, raw | 161 (161) | 250 | 0.6 | 0.7 (02zzu) | **72.45** | 120.75 meat | -0% |  | -17% | keep (borderline) |
| eel | 0.2 fish | 0.2 | 0.265 | 174193: Fish, eel, mixed species, raw | 184 (184) | 0.5 | 1 | 0.72 (02zzu) | **0.265** | 0.58 fish | -0% |  | -24% | change |
| salmon | 2 fish | 2 | 1.41 | 173686: Fish, salmon, Atlantic, wild, raw | 142 (142) | 4 | 1 | 0.62 (02zzu) | **1.41** | 3.06 fish | -0% |  | +42% | change |
| lamprey | 0.3 meat | 0.45 | 0.096 | 174193: Fish, eel, mixed species, raw (proxy) | 184 (200) | 0.15 | 1 | 0.8 (02zzu) | **0.088** | 0.19 fish | -8% |  | +410% | change (on an SR proxy) |
| cow | 40 meat | 60 | 91.2 | 168608: Beef, grass-fed, ground, raw | 198 (200) | 300 | 0.5 | 0.8 (SR carcass refuse 20% bone (13002, a modern select carcass)) | **102.168** | 170.28 meat | +12% | yes | -41% | change |
| ox | 50 meat | 75 | 126.08 | 168608: Beef, grass-fed, ground, raw | 198 (200) | 400 | 0.52 | 0.8 (SR carcass refuse 20% (13002)) | **141.293** | 235.49 meat | +12% | yes | -47% | change |
| bull | 50 meat | 75 | - | 168608: Beef, grass-fed, ground, raw | 198 | 400 | 0.52 | 0.8 (SR carcass refuse 20% (13002)) | **141.293** | 235.49 meat |  |  | -47% | change |
| young | 10 meat | 15 | 30.6 | 173815: Veal, composite of trimmed retail cuts, separable lean and fat, raw | 144 (150) | 120 | 0.55 | 0.69 (SR veal composite refuse 31% bone) | **28.996** | 48.33 meat | -5% |  | -48% | change |
| heron (young, from the nest) | 0.3 meat | 0.45 | - | 171079: Squab, (pigeon), meat only, raw (proxy) | 142 | 1.2 | 0.5 | 0.65 (SR squab refuse (proxy)) | **0.222** | 0.37 meat |  |  | +103% | change (on an SR proxy) |
| rook (young, from the nest) | 0.12 meat | 0.18 | - | 171079: Squab, (pigeon), meat only, raw (proxy) | 142 | 0.35 | 0.5 | 0.65 (SR squab refuse (proxy)) | **0.065** | 0.11 meat |  |  | +179% | change (on an SR proxy) |
| hen (a kept hen killed) | - | - | - | 172400: Chicken, stewing, meat and skin, raw | 258 | 1.2 | 0.7 | 0.7 (SR stewing hen refuse 30% bone) | **0.607** | - |  |  |  | reference (no engine good a head) |
| rabbit | - | - | - | 174347: Game meat, rabbit, wild, raw | 114 | 1.5 | 0.5 | 0.75 (02zzu) | **0.257** | - |  |  |  | reference (no engine good a head) |
| trout (a kg whole, as caught) | 1 fish | 1 | - | 175181: Fish, trout, brook, raw, New York State | 110 | 1 | 1 | 0.47 (SR brook trout refuse 53% (skin, head, viscera, bones)) | **0.207** | 0.45 fish |  |  | +384% | reference (depends on what a fish unit is) |

The hen, the rabbit and a kilogram of whole trout are reference rows: the engine has no good a head for them.

Read: the verdicts and figures here are measured from the USDA tables; the proxies, the live weights not from 02zzu, and the
choice between a modern carcass refuse and 02zzu's are judgements, named in each row.

## Applied (20 Nov)

37.2, 20 Nov 2026, W-64, branch `w64-food-values` (on main `b4076951`, with the food-source switches). The data change of D2-258
under D2-259's rule. Every departure from a checked value is written beside the data with its factor and reason. The model's
re-run is [02zzu_applied.py](02zzu_applied.py).

### The values changed

- **Goods** (`engine/data.py` ITEMS): the 26 of the change table above, as proposed:
  - meat, drying and smoking meat 0.6 (raw 0.32); dried and smoked meat 1.2; salt meat 0.57 (raw 0.24);
  - fish and its kept forms 0.46 (raw 0.28); dried and smoked fish 0.92;
  - milk 0.256; cheese 1.61;
  - greens 0.098; roots 0.263 (raw 0.13); mushrooms 0.107 (raw 0.053); watercress 0.041; samphire 0.061 (raw 0.049);
  - berries 0.167; hedge fruit 0.33 (raw 0.165); hazel nuts 1.03; raw acorns 0.034; the legacy wild food 0.41;
  - green grain and green rye 0.24.
- **Kept** with a comment saying so: the grain ladder, beans, green beans, beech nuts, acorn meal, tallow (0) and the egg.
- **Kills** (`wild/kinds.py` TAKEN, colonies), goods a head:
  - meat: red deer 33, roe 8.1, boar 29, hare 1.25, woodpigeon 0.15, wildfowl 0.56, bear 121;
  - fish: eel 0.58, salmon 3.06, lamprey 0.19 (it was meat);
  - from the nests: young heron 0.37 meat, young rook 0.11.
- **Slaughter** (`TECHNIQUES.slaughter`): cow 150 meat, ox and bull 210, young 48, on 02zzu's medieval carcass share (0.70).
  USDA's modern carcass (20% bone) would give 12% more, which is within D2-259's 20%.
- **Carrion:** a unit of meat is 3 kg of carrion (`THINGS.carcass_kg`, was 5), so a red deer's 33 units are about its 90 kg.
  The pull of the dead is measured against a red deer's 33 (`CARCASS_PULL.ref`, was 20).
- **The egg (a choice):** the egg good is a kilogram of eggs (weight 1, was 0.1), and hens lay `wild.EGG_KG` (0.045 kg) an egg.
  This is the smaller change: the good's food stays at 0.6, which the check keeps (+19%), and one line of the laying changes. The
  other way, an egg a unit, would have changed the good's food, raw value and weight as well. A hen's spring day is now 0.135
  food (was 0.1). Laying is still on the old clock (L-138).

### The levers

Each lever is named beside the data with its factor:

| Lever | Where | Factor | Why |
|---|---|---|---|
| resident fish stocks | `make_peoples.RESIDENT_FISH`, `make_water_worlds.RESIDENT_FISH`, the fishing probe | x 2.2 (K 8 -> 17.6 a unit of size; the sea 26.4; the probe's 10 -> 22, run 40 -> 88) | the stock is counted in fish units, whose food fell to 0.46. Not checked against a real standing biomass (a unit of size has no hectares) |
| the lake's stock | `make_water_worlds.LAKE_FISH` | 7,500 -> 16,500 a km² | the old 7,500 was 150 kg of **whole** fish a hectare at 2 kg a unit. On the gutted unit (about 0.53 of the whole fish) that is about 8,000, within 7% of 7,500, so the base is kept and the lever applied. 16,500 is about 330 kg whole a hectare, the top of a real lake's 50 to 300 |
| the eel run | `RUNS.eel.year` 0.2 -> 0.6, the eel's `b` 1.0 -> 3.0 (KINDS) | runs x 4.2 to 5 | measured below. At `year` 0.6 alone the history emptied the stock to a fifth, and the runs fell. `b` stands for the elvers that come up from the sea. The standing eel stock is now about 1.5 times what it was |
| the salmon run | `RUNS.salmon`: `spawn: river` (wild/runs.py `Net.spawns`), `cap_km` 1.5 -> 6, `seed_km` 1 -> 6 | spawning along the whole big river, by its km | Middleham now sees salmon. The runs are 12 to 40 times the old at the lower stations, at a real river's low to middle (part 6) |
| the lamprey run | `RUNS.lamprey` `cap_km` 3 -> 9, `seed_km` 2 -> 6 | x 3 | |
| the gear's holds | `WATER_WORKS`, in kg of the catch's goods (`wild.held_kg`, `_kg_of`) | a wattle section 10 food -> 100 kg, a timber section 7 -> 70 kg, a set trap 3 food -> 10 kg (`SETS` heads 6 -> 20) | real gear's kg (D2-258). A fish unit weighs 1 kg in the game: 0.86 kg of whole eel, 1.3 kg of whole salmon |
| gathering's kg a unit | `plants.PLANTS[k].kg` (`wild.forage`) | greens, watercress and samphire x 5; berries and mushrooms x 3.3 | real picking rates: greens about 3 kg an hour (2 to 4), soft fruit and mushrooms about 2 (1 to 3). Nuts, acorns, hedge fruit and roots keep the base |
| the plant niche's floor | `plants.niche` | 0.3 -> 0.03 | sized by food, the cheap leaves fell under the old floor, and a parcel's plants lost up to a third of their food (02zzu choice 11) |
| the legacy hunt | `TECHNIQUES.hunt` range | [2, 6] -> [5, 15] | a kill's food is kept on the new meat unit (02zzu part 5). The game stocks are not scaled (Q-71) |
| the wild's capacity | `engine/capacity.WILD` | 10 -> 4 food a year a unit of wood | the legacy forage and game on the new values. The generator sizes fields by what the woods leave |

**Larders** re-sized in the makers so their days of food are unchanged:
- the Croft house's dried meat in the food probe: 10 -> 25;
- the frontier's and the wild bands' dried meat x 2.5, Gormhold 40 -> 100;
- Croft House's cheese at Brookend: 10 -> 15.5;
- Highpool's smoked fish: 3 -> 6.5 a person;
- the runs world's late-summer store (`RUNS_STORE`): dried meat 10, roots 18.5, acorns 17.6, berries 19.2 (20.6 food a house, as before);
- Weirford's salt fish in the wild region: 12 -> 26.

The nutrition runs' larder is made from food shares and follows by itself. The generator's own house stocks are grain and beans,
which did not change.

**Committed worlds that would change if regenerated** (none was regenerated):
- `fishing/water.yaml`, `fishing/dry.yaml`;
- `goal_probe/food_*.yaml`;
- `frontier_camps.yaml`, `wild_bands.yaml`;
- `plenty/brookend.yaml`;
- `peoples/w1.yaml`, `peoples/w4.yaml`;
- `water/river.yaml`, `lake.yaml`, `lake_goal.yaml`, `runs.yaml`, `runs_models.yaml`;
- `nutrition/runs_*.yaml`;
- the wild region;
- every generated world, through `capacity.WILD`.

The hand-made worlds whose larders are meat, wild food or cheese lose that food as they stand. Two examples:
- `valley_s5.yaml`: Fenn House's meat and wild food, 10.7 food -> 4.3;
- the 30 specs with a legacy `game` stock (Q-71).

The runs and the plants are not stored in the specs: they are seeded or sized when a world is built, so a committed world gets them
without being regenerated.

### Food a unit of work by method, before and after

"Before" is 02zzu's measured rate on the old values. "02zzu" is its prediction (for gathering, with its rate fix). "Applied" is the
measured rate times the engine's data now against the old values, at the same kg a unit, with the gathering's `kg` applied by
kind. Real is the real range of part 1 on the basis (2,500 kcal, 2 h).

| Method | Before | 02zzu | Applied | Real | Verdict |
|---|---|---|---|---|---|
| farming, unbroken ground, crude reap | 1.77 | 1.81 | 1.77 | 1.6-3.6 | in range |
| farming, hoe-broken | 1.37 | 1.40 | 1.37 | 1.2-2.4 | in range |
| farming, plough-broken | 2.35 | 2.41 | 2.35 | 3.2-5.6 | pays, a little under the real |
| farming, plough and copper reap | 2.80 | 2.87 | 2.80 | 3.6-6.0 | pays, a little under |
| milking (3 cows a unit) | 2.4 | 1.23 (4.6 with its rate fix) | 1.23 | 6.4-11 | far under: the rate fix was not applied (Q-72) |
| gathering, autumn | 1.07-1.72 | 0.55-0.88 | 0.64-1.03 | 0.8-2.4 | in range (mushrooms and berries at their kg) |
| gathering, spring and summer | 0.28-0.77 | 0.16-0.43 | 0.17-0.48 | 0.24-1.1 | in range |
| gathering, winter | 0.19-0.43 | 0.08-0.17 | 0.09-0.19 | 0.12-0.64 | never pays, as in life |
| leaching acorns (the gain) | 1.7 | 2.84 | 1.90 | 0.8-1.4 | rich: acorn meal kept at 1.0, not 02zzu's 1.48 |
| hunting, novice armed, near | 0.2-0.3 | 0.14-0.22 | 0.14-0.21 | 0.08-0.32 | never pays, as in life |
| hunting, capable armed, near | 0.7 | 0.51 | 0.50 | 0.4-1.2 | in range |
| hunting, master armed, near | 2.5 | 1.87 | 1.74 | 1.2-3.2 | in range, under the ploughman (Q-70 e); the boar at SR's 122 kcal |
| snares, lifted (hares) | 0.9 | 0.64 | 0.64 | 0.4-1.2 | in range |
| netting fowl (2 units) | 0.11-0.70 | 0.08-0.49 | 0.08-0.52 | 0.24-2.2 | pays at the top |
| fishing by hand (full stock) | 0.6 | 0.28 | 0.28 | 0.16-0.72 | feeds the fisher |
| angling | 1.5 | 0.69 | 0.69 | 0.24-1.4 | in range |
| eel trap, resident, a night | 0.02-0.08 | 0.01-0.04 | 0.01-0.04 | 0.16-1.2 | far under (measured before 4c; the eel stock is now x 1.5 and the trap's hold x 3) |
| legacy hunt (full stock, armed) | 1.05 | - | 1.05 | 0.4-1.2 | in range (the kill x 2.5) |
| legacy forage (full stock) | 1.2 | - | 0.49 | 0.24-2.4 | in range |
| the mills and ovens (the gain) | 0.9, 9.6, 30; 3, 10 | +2% | unchanged | none | a design gain |

**The weir, a year, on the run pulses recorded with no one acting** (36 nights, `02zzu_shared_units.py runs` on each code; one
wattle section; 02zzu's work):

| Station | Eels a year, before -> after | Salmon a year | Lampreys a year | Weir food a year, before -> after | Food a unit | Nights its hold binds | 02zzu's real-run mid |
|---|---|---|---|---|---|---|---|
| Highpool (runs) | 36 -> 181 | 0.5 -> 46 | 0 | 2.5 -> 34 | 0.09 -> 1.24 | 0 of 10 | 2.8 |
| Middleham (runs) | 101 -> 473 | 0.5 -> 99 | 0 | 6.4 -> 80 | 0.22 -> 2.81 | 0 of 11 | 3.9 |
| Lowstrand (runs) | 474 -> 2,124 | 21 -> 848 | 26 -> 77 | 44.5 -> 278 | 1.29 -> 8.09 | 3 of 17 (a peak night offers 333 kg) | 4.2 |
| Saltwell (river) | 73 -> 338 | 10 -> 124 | 10 -> 32 | 11.5 -> 80 | 0.38 -> 2.64 | 0 of 13 | 3.0 |
| Millham (river) | 278 -> 1,164 | 31 -> 387 | 35 -> 106 | 39.8 -> 216 | 1.27 -> 6.89 | 2 of 14 (152 kg) | 4.3 |

(The "before" eel counts are on main as it stands, lower than 02zzu's runs-models checkout: 36 against 74 at Highpool.) The weir
now pays at every station, as part 6 found for a real river. At the two lowest stations it is above 02zzu's mid (6.9 and 8.1
against 4.2 and 4.3), because the hold D2-258 chose (100 kg on a peak night) is above part 6's 30 kg. That is 216 to 278 food a
year for one section, against D2-210's 60 to 70, and inside the real 4 to 48 a unit of a run night. The run nights are not yet
concentrated (37.4's part).

### What binds the keeping of a catch (no mechanics built)

A peak night at Lowstrand offers 333 kg and the section takes its 100. What follows the catch:
- **Fresh fish spoils at 0.30 a night** (in a house's store, twice meat's rate there). A night's 100 kg left fresh is about 50 kg
  after two nights. **Binds.**
- **Gutting:** no step. The fish unit is gutted weight and arrives gutted, so gutting costs no work. **Does not bind (a gap).**
- **Salt:** `salt fish` takes 1 salt to 4 fish, the real 1 kg to 4 or 5. It takes a unit of work for 4 kg (2 kg an hour), so 100 kg
  is 25 salt and 25 units. A saltmarsh pan gives 1 salt a unit (in summer). Boiling salt gives 4 a unit for 4 firewood. **Binds
  hard:** the salting rate is several times under a real one with gutting (Q-73).
- **Racks and smokehouses:** a smokehouse's racks take a batch of 40 for 3 nights, about 13 kg a night of capacity each. It is
  tended daily and burns 1 firewood a night. A hearth's rack takes 8 for 3 nights. **Binds:** a peak night needs about 8
  smokehouses' nights.
- **Fuel:** 1 firewood a smokehouse night and 1 a salt boiled. **Binds lightly,** behind the racks and the salting work.
- **Nets:** no fish net exists. The `net` method is fowling, and D2-258's "nets when built" waits on the gear ladder
  (water_and_preservation.md: a seine needs flax or hemp, L-13). **A gap.**

### Tests

- The full suite at 4c8def4d: TESTS_RESULT.
- 18 tests failed at first. All 18 pass on the code before the change.
- Their fixes, each with a comment in the test:
  - **The old value, re-pinned in units:** 12 tests;
  - **the 4c ecology digest re-pinned:** it is the old digest again with `data.py`, `kinds.py` and `wild.py` put back at 44d10eb7;
  - **the red deer test now uses a party of four:** a party of three cannot carry a 33-meat deer at 10 each (02zzu choice 12);
  - **the hosting test tops up valley_s5's larder** to its old days of food.
- **Three resume tests** (`test_cybertron2_branch.py`) failed because people now starve in valley_s5 by day 3 (7 of 17 dead by
  day 5, against 2 before). That exposed a real bug: the night record kept live references to the day's offers. When an offerer
  died later, the straight run rewrote the earlier days' records, and a run resumed from a day's end did not. The record now keeps
  a copy (`engine/run.py`).

### The bot runs (32 days, `--bots`, before b4076951 and after 4c8def4d)

BOTS_TABLE

### Gaps found

- **The legacy game and forage stocks** are counted in their goods' units and were not scaled. Legacy woods hold 0.4 of their old
  food (Q-71). `valley_s5.yaml` starves sooner on its meat and wild food.
- **Milking** at the real milk value is 1.2 a unit, against a real 6.4 to 11 (Q-72). The cheese is still 6 milk (02zzu proposed
  10).
- **Keeping:** the salting rate (Q-73), gutting with no work, and no fish nets.
- **The hens** are on the old clock (L-138), and a killed hen gives no meat (0.6 food on SR).
- **The weir at the lowest stations** is 3 to 4 times D2-210's year (the 100 kg hold). Concentrating the run nights (37.4) will
  change it.
- **`make_wild_tests.EEL_GOOD`** is still "meat" (stale since D2-216, before this change).
- **`tools/records.py`** cannot run `whoami` or keep its pending file in a git worktree (`.git` is a file there).

*Current as of 20 Nov 2026.*
