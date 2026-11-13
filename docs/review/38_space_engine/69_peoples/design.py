"""Review 38.69: the five worlds of the peoples benchmark, as designed (not generated). Each place is set by hand: where it is (km, a
presentation and generation target), its land (engine covers), soil, the engine resources it holds, and what it is for. The world
builder will realise these with the land generator's pins and features and is checked against this file.

Land types are bundles of engine covers (data.COVERS); resources are engine RESOURCES keys or fittings: seam (copper ore), quarry
(stone), salt, fish, game, wood (timber), grass, mill site (a fall on a river where a water wheel can stand)."""

LAND = {   # land type: (engine covers it is made of, colour on the map)
    "farmland": (["field", "meadow", "pasture", "scrub"], "#c9d98a"),
    "rich vale": (["meadow", "pasture", "scrub", "water"], "#8fc45a"),
    "forest": (["forest", "scrub", "meadow"], "#3f7a3a"),
    "old forest": (["forest"], "#2a5a2a"),
    "heath": (["heath", "scrub", "pasture"], "#c8a3c8"),
    "moor": (["moor", "heath", "pasture"], "#a68aa0"),
    "rock hills": (["rock", "heath", "pasture"], "#9a8f80"),
    "chalk down": (["rock", "pasture", "heath"], "#d8d2c0"),
    "fen": (["fen", "water", "meadow"], "#7fb3a8"),
    "lake": (["water", "meadow", "forest"], "#6aa3d6"),
    "coast": (["saltmarsh", "water", "pasture"], "#9fc9d6"),
    "pass": (["rock", "heath"], "#b0a898"),
}
SOIL = {"rich": 1.3, "fair": 1.0, "poor": 0.7}          # the generator's soil words: rich 1.2 to 1.4, poor 0.6 to 0.8 (landgen.vocab)


def P(name, x, y, land, soil="fair", res=(), kind="vacant", note="", value=0):
    """kind: home:A (a people's starting village), vacant (land no one holds), stop (a stopping place on a long road).
    value: 0 ordinary, 1 good, 2 high value (contested by design)."""
    return {"name": name, "x": x, "y": y, "land": land, "soil": soil, "res": list(res), "kind": kind, "note": note, "value": value}


WORLDS = {}

# ---------------------------------------------------------------- 2 peoples
WORLDS["W1"] = {
    "title": "W1 Twin Hollows: two peoples, near, one prize between them",
    "size": (48, 40), "peoples": ["A", "B"],
    "summary": "Small and mirror-symmetric. Two villages half a day apart on either side of a rich vale with the only mill site; the "
               "only stone and copper on one hill a day from both; a fen with fish reached only through the vale. Each has a wood and "
               "a heath of its own.",
    "places": [
        P("Ashford", 12, 22, "farmland", "fair", ["wood", "grass"], "home:A", "A's village: fields for about twice its people as they stand"),
        P("Brockley", 36, 22, "farmland", "fair", ["wood", "grass"], "home:B", "B's village, the mirror of Ashford"),
        P("Middlemead", 24, 18, "rich vale", "rich", ["grass", "fish", "mill site"], note="the best land and the only mill site, half a day from each", value=2),
        P("Lower Meads", 24, 5, "fen", "fair", ["fish", "grass"], note="hay and fish; its only way in is through Middlemead", value=1),
        P("Coppice Hill", 24, 35, "rock hills", "poor", ["seam", "quarry", "grass"], note="the only stone and copper: a day from each village", value=2),
        P("Ash Wood", 4, 32, "forest", "fair", ["wood", "game"], note="A's side"),
        P("Ash Heath", 3, 12, "heath", "poor", ["grass"], note="A's side: rough grazing"),
        P("Brock Wood", 44, 32, "forest", "fair", ["wood", "game"], note="B's side"),
        P("Brock Heath", 45, 12, "heath", "poor", ["grass"], note="B's side: rough grazing"),
    ],
    "roads": [("Ashford", "Middlemead"), ("Brockley", "Middlemead"), ("Middlemead", "Lower Meads"), ("Ashford", "Coppice Hill"),
              ("Brockley", "Coppice Hill"), ("Ashford", "Ash Wood"), ("Ashford", "Ash Heath"), ("Brockley", "Brock Wood"),
              ("Brockley", "Brock Heath"), ("Ash Wood", "Coppice Hill"), ("Brock Wood", "Coppice Hill")],
    "hills": [("Ashford", "Coppice Hill"), ("Brockley", "Coppice Hill"), ("Ash Wood", "Coppice Hill"), ("Brock Wood", "Coppice Hill")],
}

WORLDS["W2"] = {
    "title": "W2 Over the Pass: two valleys, a short hard way and a long rich one",
    "size": (84, 70), "peoples": ["A", "B"],
    "summary": "Medium and mirror-symmetric. Each people holds the head of its own valley, with a private backyard of wood, farmland "
               "and fen down-valley. The ridge between them has one pass, where the copper and stone are. Both valleys open onto a "
               "shared lowland two days south: the richest land, the mill site and the salt coast. Contact comes early at the pass "
               "if either goes for metal, and late on the plain if they expand.",
    "places": [
        P("Ashby Head", 24, 54, "farmland", "fair", ["wood", "grass"], "home:A"),
        P("Brook Head", 60, 54, "farmland", "fair", ["wood", "grass"], "home:B"),
        P("High Gap", 42, 58, "pass", "poor", ["seam", "quarry"], note="the pass: copper and stone, the short way between the valleys", value=2),
        P("Ashby Wood", 14, 44, "forest", "fair", ["wood", "game"]),
        P("Ashdale", 26, 36, "farmland", "fair", ["grass"], note="A's backyard: good fields", value=1),
        P("Ash Fen", 18, 24, "fen", "fair", ["fish", "grass"]),
        P("Westmoor", 6, 60, "moor", "poor", ["grass"], note="summer grazing"),
        P("Brook Wood", 70, 44, "forest", "fair", ["wood", "game"]),
        P("Brookdale", 58, 36, "farmland", "fair", ["grass"], note="B's backyard: good fields", value=1),
        P("Brook Fen", 66, 24, "fen", "fair", ["fish", "grass"]),
        P("Eastmoor", 78, 60, "moor", "poor", ["grass"], note="summer grazing"),
        P("Two Waters", 42, 14, "rich vale", "rich", ["grass", "fish", "mill site"], note="where the two valleys' rivers meet: the prize", value=2),
        P("Southmead", 30, 7, "rich vale", "rich", ["grass"], value=1),
        P("Eastmead", 54, 7, "rich vale", "rich", ["grass"], value=1),
        P("Salt Strand", 42, 1, "coast", "poor", ["salt", "fish"], note="the only salt", value=1),
        P("Ashdale Ford", 24, 18, "farmland", "fair", [], "stop"),
        P("Brookdale Ford", 60, 18, "farmland", "fair", [], "stop"),
    ],
    "roads": [("Ashby Head", "High Gap"), ("Brook Head", "High Gap"), ("Ashby Head", "Ashby Wood"), ("Ashby Head", "Ashdale"),
              ("Ashby Head", "Westmoor"), ("Ashdale", "Ash Fen"), ("Ashby Wood", "Ash Fen"), ("Ash Fen", "Ashdale Ford"), ("Ashdale", "Ashdale Ford"),
              ("Ashdale Ford", "Southmead"), ("Ashdale Ford", "Two Waters"),
              ("Brook Head", "Brook Wood"), ("Brook Head", "Brookdale"), ("Brook Head", "Eastmoor"), ("Brookdale", "Brook Fen"),
              ("Brook Wood", "Brook Fen"), ("Brook Fen", "Brookdale Ford"), ("Brookdale", "Brookdale Ford"), ("Brookdale Ford", "Eastmead"),
              ("Brookdale Ford", "Two Waters"), ("Southmead", "Two Waters"), ("Eastmead", "Two Waters"), ("Two Waters", "Salt Strand"),
              ("Southmead", "Salt Strand"), ("Eastmead", "Salt Strand")],
    "hills": [("Ashby Head", "High Gap"), ("Brook Head", "High Gap"), ("Ashby Head", "Westmoor"), ("Brook Head", "Eastmoor")],
}

WORLDS["W3"] = {
    "title": "W3 The Long Frontier: two neighbours on the coast, a wide country inland",
    "size": (124, 86), "peoples": ["A", "B"],
    "summary": "Large and asymmetric (positions rotated between models). The peoples start a day apart on a settled coastal strip: A "
               "has the salt and fish, B the stone. A ford between them is the way inland. The interior is a frontier in rings of "
               "distance: woods, meadows, a lake and moors within two days; a rich vale with a mill site and a deep forest at three; "
               "the only copper at four; and beyond, a great rich basin and a second coast. There is room to grow without meeting, "
               "and long supply lines if they do not.",
    "places": [
        P("Ashmouth", 8, 58, "coast", "fair", ["salt", "fish", "grass"], "home:A", "A: salt and fish, fair fields"),
        P("Barrowby", 10, 28, "chalk down", "fair", ["quarry", "grass"], "home:B", "B: stone, fair fields"),
        P("Ashholt", 18, 70, "forest", "fair", ["wood", "game"]),
        P("Barrow Down", 20, 16, "chalk down", "poor", ["quarry", "grass"]),
        P("Midford", 16, 43, "rich vale", "rich", ["grass", "fish"], note="the ford between them and the way inland", value=2),
        P("Greenhurst", 34, 54, "forest", "fair", ["wood", "game"]),
        P("Longmead", 36, 36, "rich vale", "rich", ["grass", "fish"], value=1),
        P("Hartmoor", 32, 74, "moor", "poor", ["grass"]),
        P("Wickfen", 34, 14, "fen", "fair", ["fish", "grass"]),
        P("Deepwood", 56, 62, "old forest", "fair", ["wood", "game"], note="the great timber", value=1),
        P("Mirewater", 54, 44, "lake", "fair", ["fish", "wood"]),
        P("Hallow Vale", 58, 26, "rich vale", "rich", ["grass", "mill site"], note="rich land and a mill site, three days in", value=2),
        P("Highfold", 62, 78, "moor", "poor", ["grass"], note="upland grazing"),
        P("Coppermount", 82, 56, "rock hills", "poor", ["seam", "quarry", "grass"], note="the only copper, four days in", value=2),
        P("Riverbend", 84, 34, "rich vale", "rich", ["grass", "fish"], value=1),
        P("Far Heath", 80, 76, "heath", "poor", ["grass"]),
        P("Eastfen", 86, 10, "fen", "fair", ["fish", "grass"]),
        P("Sunvale", 106, 40, "rich vale", "rich", ["grass", "fish", "mill site"], note="the great basin: the most land, farthest out", value=2),
        P("Stonegate", 104, 64, "rock hills", "poor", ["quarry", "grass"]),
        P("Far Strand", 118, 18, "coast", "poor", ["salt", "fish"], note="the second salt", value=1),
        P("Greenhurst Stop", 44, 48, "heath", "poor", [], "stop"),
        P("Hallow Stop", 72, 42, "heath", "poor", [], "stop"),
        P("Sunvale Stop", 96, 48, "heath", "poor", [], "stop"),
    ],
    "roads": [("Ashmouth", "Midford"), ("Barrowby", "Midford"), ("Ashmouth", "Ashholt"), ("Barrowby", "Barrow Down"),
              ("Midford", "Greenhurst"), ("Midford", "Longmead"), ("Ashholt", "Hartmoor"), ("Ashholt", "Greenhurst"), ("Barrow Down", "Wickfen"),
              ("Longmead", "Wickfen"), ("Greenhurst", "Greenhurst Stop"), ("Greenhurst Stop", "Mirewater"), ("Greenhurst Stop", "Deepwood"),
              ("Longmead", "Mirewater"), ("Longmead", "Hallow Vale"), ("Hartmoor", "Highfold"), ("Deepwood", "Highfold"),
              ("Mirewater", "Hallow Stop"), ("Hallow Vale", "Hallow Stop"), ("Hallow Stop", "Coppermount"), ("Hallow Stop", "Riverbend"),
              ("Deepwood", "Coppermount"), ("Highfold", "Far Heath"), ("Far Heath", "Coppermount"), ("Hallow Vale", "Eastfen"),
              ("Riverbend", "Eastfen"), ("Riverbend", "Sunvale Stop"), ("Coppermount", "Sunvale Stop"), ("Sunvale Stop", "Sunvale"),
              ("Coppermount", "Stonegate"), ("Sunvale", "Stonegate"), ("Sunvale", "Far Strand"), ("Eastfen", "Far Strand")],
    "hills": [("Deepwood", "Coppermount"), ("Hallow Stop", "Coppermount"), ("Far Heath", "Coppermount"), ("Coppermount", "Stonegate"),
              ("Hartmoor", "Highfold"), ("Deepwood", "Highfold")],
}

# ---------------------------------------------------------------- 3 peoples
WORLDS["W4"] = {
    "title": "W4 The Ring Basin: three peoples at three gates to one rich basin",
    "size": (84, 84), "peoples": ["A", "B", "C"],
    "summary": "Medium, near-symmetric. A fertile basin inside a ring of hills, entered by three gaps; each people starts outside one "
               "gap with a backyard of its own (each backyard leans one way: A the great wood, B the quarry, C the upland grazing). "
               "Inside: three rich meads, each nearest one gap, and the mere at the centre with the mill site on its outflow. The only "
               "copper is in the gorge where the basin drains out, between B and C and farthest from A.",
    "places": [
        P("Ashgate", 42, 78, "farmland", "fair", ["wood", "grass"], "home:A"),
        P("Brackwell", 10, 22, "farmland", "fair", ["grass"], "home:B"),
        P("Colton", 74, 22, "farmland", "fair", ["grass"], "home:C"),
        P("North Gap", 42, 62, "pass", "poor", [], "stop", "a gate into the basin"),
        P("West Gap", 22, 32, "pass", "poor", [], "stop", "a gate into the basin"),
        P("East Gap", 62, 32, "pass", "poor", [], "stop", "a gate into the basin"),
        P("Northmead", 42, 52, "rich vale", "rich", ["grass"], value=1),
        P("Westmead", 32, 38, "rich vale", "rich", ["grass"], value=1),
        P("Eastmead", 52, 38, "rich vale", "rich", ["grass"], value=1),
        P("The Mere", 42, 42, "lake", "rich", ["fish", "grass", "mill site"], note="the centre: fish and the mill site", value=2),
        P("The Gorge", 42, 16, "rock hills", "poor", ["seam", "quarry"], note="the only copper, where the basin drains out", value=2),
        P("Ashwood", 26, 80, "old forest", "fair", ["wood", "game"], note="A's: the great wood"),
        P("Ash Moor", 60, 82, "moor", "poor", ["grass"]),
        P("Brack Quarry", 4, 38, "chalk down", "poor", ["quarry", "grass"], note="B's: stone"),
        P("Brack Wood", 16, 8, "forest", "fair", ["wood", "game"]),
        P("Colton Fell", 82, 38, "moor", "poor", ["grass"], note="C's: upland grazing"),
        P("Colton Wood", 68, 8, "forest", "fair", ["wood", "game"]),
    ],
    "roads": [("Ashgate", "North Gap"), ("North Gap", "Northmead"), ("Northmead", "The Mere"), ("Brackwell", "West Gap"),
              ("West Gap", "Westmead"), ("Westmead", "The Mere"), ("Colton", "East Gap"), ("East Gap", "Eastmead"), ("Eastmead", "The Mere"),
              ("The Mere", "The Gorge"), ("Brack Wood", "The Gorge"), ("Colton Wood", "The Gorge"), ("Ashgate", "Ashwood"), ("Ashgate", "Ash Moor"),
              ("Brackwell", "Brack Quarry"), ("Brackwell", "Brack Wood"), ("Colton", "Colton Fell"), ("Colton", "Colton Wood"),
              ("Ashwood", "Brack Quarry"), ("Ash Moor", "Colton Fell")],
    "hills": [("Ashgate", "North Gap"), ("Brackwell", "West Gap"), ("Colton", "East Gap"), ("Ashwood", "Brack Quarry"), ("Ash Moor", "Colton Fell")],
}

WORLDS["W5"] = {
    "title": "W5 Three Countries: lowland, upland and woodland coast, each one people's",
    "size": (124, 104), "peoples": ["A", "B", "C"],
    "summary": "Large and complementary (positions rotated). Each people starts in a country that has what the others lack and lacks "
               "what they have: the lowland (A) rich soil and two mill sites but no stone and little wood; the upland (B) copper, "
               "stone and grazing but poor, cold fields; the woodland coast (C) timber, game, salt and fish but little ploughland. "
               "Growth past the home village needs the others' goods or their land. A ford market at Threeways joins the three, two "
               "days from each.",
    "places": [
        # the lowland (A)
        P("Lowbury", 24, 34, "farmland", "rich", ["grass", "fish"], "home:A", "A: rich fields; no stone, little wood"),
        P("Millbrook", 14, 50, "rich vale", "rich", ["grass", "fish", "mill site"], value=1),
        P("Wheatley", 36, 20, "farmland", "rich", ["grass"], value=1),
        P("Southmere", 20, 10, "fen", "fair", ["fish", "grass"]),
        P("Longacre", 40, 44, "rich vale", "rich", ["grass", "mill site"], value=1),
        # the upland (B)
        P("Highcairn", 88, 84, "moor", "poor", ["quarry", "grass"], "home:B", "B: stone and grazing; poor, cold fields"),
        P("Coppermount", 104, 94, "rock hills", "poor", ["seam", "quarry"], note="the copper", value=2),
        P("Stonefell", 70, 94, "rock hills", "poor", ["quarry", "grass"]),
        P("Highmoor", 102, 70, "moor", "poor", ["grass"]),
        P("Tarn", 74, 74, "lake", "poor", ["fish", "grass"]),
        # the woodland coast (C)
        P("Holtmouth", 98, 24, "coast", "fair", ["salt", "fish", "wood"], "home:C", "C: timber, game, salt, fish; little ploughland"),
        P("Deepwood", 82, 36, "old forest", "fair", ["wood", "game"], value=1),
        P("Saltings", 116, 10, "coast", "poor", ["salt", "fish"]),
        P("Oakhurst", 110, 44, "forest", "fair", ["wood", "game"]),
        P("Cove", 78, 8, "coast", "poor", ["fish"]),
        # the middle
        P("Threeways", 62, 52, "rich vale", "rich", ["grass", "fish"], note="the ford where the three countries' roads meet", value=2),
        P("Border Wood", 58, 70, "forest", "fair", ["wood", "game"]),
        P("Marchmead", 56, 30, "farmland", "fair", ["grass"]),
        P("Lowbury Stop", 42, 34, "farmland", "fair", [], "stop"),
        P("Highcairn Stop", 76, 64, "moor", "poor", [], "stop"),
        P("Holtmouth Stop", 80, 44, "forest", "fair", [], "stop"),
    ],
    "roads": [("Lowbury", "Millbrook"), ("Lowbury", "Wheatley"), ("Lowbury", "Southmere"), ("Wheatley", "Southmere"), ("Lowbury", "Lowbury Stop"),
              ("Lowbury Stop", "Longacre"), ("Lowbury Stop", "Threeways"), ("Millbrook", "Longacre"), ("Wheatley", "Marchmead"),
              ("Highcairn", "Coppermount"), ("Highcairn", "Stonefell"), ("Highcairn", "Highmoor"), ("Highcairn", "Tarn"), ("Highcairn", "Highcairn Stop"),
              ("Highcairn Stop", "Threeways"), ("Tarn", "Border Wood"), ("Stonefell", "Border Wood"), ("Highmoor", "Oakhurst"),
              ("Holtmouth", "Deepwood"), ("Holtmouth", "Saltings"), ("Holtmouth", "Oakhurst"), ("Holtmouth", "Cove"), ("Holtmouth", "Holtmouth Stop"),
              ("Holtmouth Stop", "Threeways"), ("Deepwood", "Holtmouth Stop"), ("Cove", "Marchmead"), ("Marchmead", "Threeways"),
              ("Border Wood", "Threeways"), ("Longacre", "Border Wood")],
    "hills": [("Highcairn", "Coppermount"), ("Highcairn", "Stonefell"), ("Highcairn", "Highmoor"), ("Highcairn", "Highcairn Stop"),
              ("Highcairn Stop", "Threeways"), ("Highmoor", "Oakhurst"), ("Stonefell", "Border Wood")],
}

KMH = 17.0 / 8.0           # about a day's road (8 hours) for 17 km in a straight line (landgen: spacing_km 17, road_day_hours 8)


def hours(w, a, b):
    pa = next(p for p in w["places"] if p["name"] == a)
    pb = next(p for p in w["places"] if p["name"] == b)
    d = ((pa["x"] - pb["x"]) ** 2 + (pa["y"] - pb["y"]) ** 2) ** 0.5
    return d / KMH * (1.5 if (a, b) in w["hills"] or (b, a) in w["hills"] else 1.0)

# The land's large shapes, drawn on the maps and given to the generator as features: ridges (with their passes), rivers, coasts.
FEATURES = {
    "W1": [("river", [(24, 40), (24, 18), (24, 0)]), ("ridge", [(14, 38), (34, 38)])],
    "W2": [("ridge", [(42, 70), (42, 30)]), ("ridge", [(0, 66), (84, 66)]),
           ("river", [(24, 62), (26, 36), (24, 18), (42, 14)]), ("river", [(60, 62), (58, 36), (60, 18), (42, 14)]),
           ("river", [(42, 14), (42, -2)]), ("coast", [(0, -2), (84, -2)])],
    "W3": [("coast", [(2, 86), (2, 0)]), ("river", [(70, 70), (54, 44), (36, 36), (16, 43), (2, 43)]),
           ("ridge", [(74, 84), (92, 40)]), ("river", [(110, 70), (106, 40), (86, 10)]), ("coast", [(124, 30), (124, 0)])],
    "W4": [("ridge", "ring"), ("river", [(42, 52), (42, 42), (42, 16), (42, 0)])],
    "W5": [("ridge", [(60, 104), (66, 76), (100, 60), (124, 60)]), ("river", [(14, 60), (24, 34), (40, 44), (62, 52), (62, 104)]),
           ("coast", [(70, 0), (124, 0), (124, 30)]), ("river", [(100, 60), (98, 24)])],
}
