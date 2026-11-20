---
id: docs/review/37_growth/02zzj_economy_research/visual/passes/BRIEF.md
kind: note
updated: "2026-11-15"
---
# Brief: extract a dependency web from economy research parts

*note · `docs/review/37_growth/02zzj_economy_research/visual/passes/BRIEF.md`*


We are building an interactive visual of how economies grew from foragers to the 21st-century city: a time-ordered web of
techniques, industries, goods, infrastructure and institutions, with edges saying what each one needed and what it unlocked.
The source is a research folder: /home/user/cybertron2/docs/review/37_growth/02zzj_economy_research/ (13 parts, ~10,000 words each).
You extract from the parts assigned to you. Read them in full. Stay grounded in what the parts say; you may use general knowledge
only to fill a date or a missing obvious prerequisite edge, and must mark it (date_src "general", edge "src":"general").
Do not edit anything in the repository. Write only your output file.

## Output: one JSON file (path given in your task), shape:
{
 "nodes": [ {
   "id": "snake_case",            // use a SEED id below whenever the concept matches; otherwise make a new specific id
   "label": "Short name (2-5 words)",
   "domain": one of DOMAINS,
   "kind": "technique" | "industry" | "good" | "resource" | "infrastructure" | "institution" | "practice",
   "start": -7000,                // year of first significant appearance (negative = BCE; 300,000 years ago = -300000)
   "date_src": "part" | "general",
   "wide": 1300,                  // optional: year it became widespread / dominant somewhere, if the part says
   "place": "where it first appears or is typified",
   "paradigm": one of PARADIGMS,  // society type in which it first appears or which it typifies
   "desc": "2-3 plain sentences: what it is, what it needed, what it changed. Concrete. One key figure if the part has one, with the part's own verification tag.",
   "chokepoint": true/false,      // true only if the part treats it as a chokepoint / bottleneck / monopoly point
   "part": "07"                   // the part number it comes from
 } ],
 "edges": [ { "from": "id", "to": "id", "type": TYPE, "note": "under 12 words", "src": "part" | "general" } ]
}

Edge direction: `from` came first and `to` depends on it.
TYPE:
- "input": from is a material, fuel or energy input to `to` (charcoal -> bloomery_iron)
- "enables": from is a needed technique, capital, institution, infrastructure or knowledge for `to` (canals -> ..., writing -> banking)
- "replaces": `to` substitutes for `from` (a paradigm switch, e.g. charcoal -> coke, oak bark tanning -> chrome tanning); note what it freed
- "byproduct": `to` is a joint product or by-product of `from` (kerosene_refining -> gasoline, gasworks -> coal_tar)

Edges may point to/from SEED ids even if your parts don't make a node for them (another agent will). Do NOT reference
non-seed ids you didn't create yourself. Every new node should have at least one edge. Aim for 40-60 nodes and 70-120 edges
per part (more for dense parts); prefer specific industries, techniques and chain steps (e.g. "fulling mill", "puddling",
"Leblanc soda", "telegraph beside the railway", "suit of mill") over broad abstractions. Include the institutions and money forms
the chains needed, and switches/substitutions. Avoid duplicates of seed concepts under new ids.

DOMAINS (lanes): energy, food, materials (stone, wood, ceramics, glass, salt, chemicals, plastics), metals, textiles (fibre, cloth,
dyes, leather and tanning), building (construction, water supply, sanitation, urban infrastructure), transport, exchange (money, markets,
trade, finance), institutions (household, labour forms, property, law, state, firms), information (writing, records, printing,
telecoms, computing).

PARADIGMS: foraging, horticultural_tribal, chiefdom, early_state, agrarian_empire, feudal_manorial, commercial_city_state,
early_modern_state, industrial, socialist_planned, service_information, and the branches pastoral_nomadic, irrigation,
maritime_trading, frontier_settler, plantation_slave, gift_economy.

SEED ids (use exactly):
energy: fire, wood_fuel, charcoal, draught_animals, watermill, windmill, peat, coal, coke, steam_engine, oil_petroleum, natural_gas,
  electricity, electric_grid, internal_combustion_engine, nuclear_power, solar_wind
food: foraging, hunting, fishing, cereal_domestication, animal_domestication, milk_dairy, wool_sheep, plough, irrigation_farming,
  three_field_rotation, legumes_clover, manure, flour_milling, baking, brewing, salt_preservation, refrigeration_cold_chain,
  synthetic_nitrogen, tractor, meatpacking, supermarket, green_revolution
materials: stone_tools, pottery, kiln, lime, glass, rendering_tallow, alkali_soda, sulphuric_acid, coal_tar_chemicals, plastics,
  cement_concrete, timber, coppice, rubber, paper, salt_making
metals: copper_smelting, tin, bronze, bloomery_iron, blast_furnace, puddling, bessemer_steel, open_hearth_steel, electric_arc_steel,
  aluminium, machine_tools, interchangeable_parts
textiles: spinning, weaving, cotton, flax_linen, fulling_mill, mechanised_spinning, power_loom, dyeing, synthetic_fibres, tanning
building: wattle_daub, mudbrick, stone_masonry, brick, steel_frame, elevator, piped_water, sewers
transport: boats, sail, pack_animals, wheel_cart, roads, canals, railway, steamship, motor_vehicle, container_shipping, aviation, pipelines
exchange: gift_exchange, redistribution, barter, credit_accounting, coinage, markets_fairs, bills_of_exchange, banking, paper_money,
  joint_stock_company, stock_exchange, insurance, central_bank, electronic_payments, long_distance_trade
institutions: household_production, property_in_land, lordship_manor, serfdom, slavery, guilds, wage_labour, putting_out,
  factory_system, state_taxation, law_courts, trade_unions, corporation, welfare_state, cities
information: writing, record_keeping, printing, postal_service, telegraph, telephone, radio, computer, semiconductors, internet,
  mobile_phone

Validate your file with `python3 -c "import json;json.load(open(PATH))"` and check every edge endpoint is a seed id or one of your
node ids. Your final reply: just the path, node and edge counts, and anything uncertain (two lines).
