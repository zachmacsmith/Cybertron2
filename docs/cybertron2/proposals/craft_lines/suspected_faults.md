# Suspected engine faults found while writing the craft lines (W-205, 28 Nov)

Found by the five drafters while grounding each line in the code; collated by session bench. **Not sent to anyone** (D5-11): each
waits on Zach's word that it is a bug before it goes to the engine's owners. Each row's evidence (file and function) is in
`craft_lines.json` under that craft's `doubts` and `grounded_in`. Two were confirmed by a probe run (marked); the rest are read
from the code.

## A. What the prompt tells people is untrue

| # | Suspected fault | Where | Crafts affected |
|---|---|---|---|
| A1 | The rough line promises "about half the time it works, and it takes more", and the capable line "works about 3 times in 4 ... a third more materials", for every craft; only making and fittings roll a failure. Gathering (`verbs._technique`) and field work roll none and take nothing extra; rooms, monuments and the weir only take more materials | `knowledge.craft_parts`, `iface.craft_line` | all gather and work crafts; rooms, monuments, weir |
| A2 | Every build's rough line reads "a rough idea: no materials": the costs are in ROOMS, FITTINGS and MONUMENTS, not the row's inputs | `knowledge.craft_parts` | every build |
| A3 | A fitting at capable still fails 1 in 4 and spoils its materials, but the blueprint branch of the line says no odds | `iface.craft_line`, `verbs._fitting` | fittings |
| A4 | The anvil needs a hearth, never shown: FITTINGS' `needs` is not carried into the row, so a smith learns it from the refusal | `iface._needs_words` | anvil (and any fitting with needs) |
| A5 | Ditch, terrace and wall say "needs others with you", but one person who knows how can do it alone | crew rows | ditch, terrace, wall |
| A6 | mend gear's line says "a tenth of its materials a piece"; a set line takes 15 hooks, half its making, and a hand line 1 hook and no cord | `gear.LIVES` mend | mend gear |
| A7 | Hot-smoked meat's manual says it keeps "about a week", but it spoils barely slower than fresh meat (0.247 against 0.283 a night) | process rows | hot smoke meat |
| A8 | Hoeing reports "0 of a plot ... turning up 0 stone": small amounts rounded to nothing in the message (probe) | the hoe result line | hoe |

## B. An act or item that does less than it should

| # | Suspected fault | Where |
|---|---|---|
| B1 | **Manuring never uses up the dung**: it checks dung is to hand but never takes it (probe: 5 dung before and after, the field's fertility raised) | work handler, `farm.act` |
| B2 | Hunting weapons never wear: every wild method has `wear: 0.3`, nothing applies it; a crude weapon wears only in fights | `wild.take`, `wild.hunt`, `verbs._technique` |
| B3 | The dip net never wears: fishing at the edge checks one is held, never wears it, so mending it restores nothing | wild edge fishing |
| B4 | Making never wears the tool in hand (`_make` calls no wear); smelting's `trade: smelter` is checked nowhere | `verbs._make` |
| B5 | Nothing gives bone: no beast's goods, no craft's output; bone hooks only from a world's starting bone | ITEMS, wild kinds |
| B6 | Hurdles do nothing: no fence, fold or fitting takes them | hurdle |
| B7 | The keep box does nothing, though its hint promises fish kept alive in the water; a catch always goes to the hands | keep box |
| B8 | Tallow lights: the only use is picking slugs at dusk, not work at night in general | `wild.guard` |
| B9 | Burning the stubble does not check the field is harvested (runs over a standing crop and harms nothing); and a field keeps one guard, so a later one-day slug picking replaces the stubble's longer protection | burn the stubble, field guards |
| B10 | An open gate does not let wild raiders in: the night raid reads the fence's level, not its gate (herds do respect the gate) | night raids |
| B11 | Finishing a clearing silently deletes a crop sown on that turf | clear |
| B12 | Select seed: the mark does nothing (only its own refusal reads it); and every go counts as failed practice, so the gain (sooner-ripening sowings, at known) takes twice the goes | select seed |
| B13 | Several works count each act as failed practice: clear, clear for building, ditch, terrace, the four mending crafts, dig a strip (slows learning ditch and terrace) | learning |
| B14 | Work on a whole wall is allowed as mending until its yearly quarter is in, and changes nothing | wall |
| B15 | Breaking a dam where there is none is not refused: the work is spent and counted as practice | den work |
| B16 | Salting can never fail and takes no extra salt at any level | salting |

## C. Words that do not reach what they say

| # | Suspected fault | Where |
|---|---|---|
| C1 | Guard-the-field aliases naming a scare ("watch the field with a horn", "set the dog on them") carry no scare, so the first to hand is used: the fire, burning the wood | guard aliases |
| C2 | Pest-work aliases ("pick slugs", "top the beans", "kill the grubs") act on the worst pest present, not the one named; "grubs" means the ladybirds, the helpers; `needs.on_crop` read nowhere | pest work |
| C3 | "cairn" alone resolves to the monument, not the burial cairn: a monument cairn by a grave does not cover the body | cairn, bury |
| C4 | The brine pan's alias "salt pan" is the key of the saltmarsh gather craft | brine pan, salt pan |
| C5 | Hints read by nothing: den work's "spades and a dog help" (only a crude weapon counts), fish by hand's "with a spear" (only a dip net, on a run), the woodshed's "kept dry" (no store reads rain) | rows' hints |
| C6 | Net is marked untaught "tryable", but `_technique` refuses anyone without a rough idea (the field is read only for ways) | net |
| C7 | The set line's `does` says "baited hooks" (no bait in the engine); the snare's says "for a few nights" (snares stand until taken up and thin as they tear) | existing does |
| C8 | Slaughter's argument says "else the young first", but with neither beast nor herd named the act is refused | slaughter |
| C9 | Weeding a ripe crop is not refused; the engine's own "ripe: past weeding" refusal is never reached for a field | weed |

## D. Data and docs that disagree (small)

- The plough's life is 60 in ITEMS ("60 plots") but 18 in gear.TOOL_LIVES, which is what wears it; at known a tent or a plough shows
  no life (gear.life_words reads LIVES only).
- buildings.py's docstring says "bins 60 food, a cellar 40 food"; the stores give 300 kg and 30 kg a space.
- The granary's `does` leaves out oats; the fire ring's says "burns timber" (it burns firewood, timber or charcoal, in that order).
- A camp: 99 free floor in `_fitting`, so beds beyond its four; a comment says a lean-to keeps 10 weight, SPACE camp_store is 30; in
  a levels world it costs 1 timber and has no fixed life, but its line shows the blueprint's 3 timber and "1 units".
- The owl hole's owl never leaves once nested; the vault needs no stone building and guards fire only.
- The fishing rod beats the hand line on every count (withies only, x1.5, longer life); the hand line's only gain is mending.
- Old hunt: weapon and skill scale a kill's size, not its chance (the lines say so).

## Design points, not faults

- Bins fill before a granary floor (rats reach bins less), so a granary only takes grain once the bins are full.
- A creel's carry does not add to a pack basket's (the better counts); on a hunt only a pack basket or a led ox counts.
- Coin has no use but changing hands; a day at the salt pans in a season that gives nothing costs the unit and a failed try.
