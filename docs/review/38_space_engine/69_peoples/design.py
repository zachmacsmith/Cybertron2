"""Review 38.69: the five worlds of the peoples benchmark, as designed (not generated).

Each place is set by hand: its land (a bundle of engine covers), soil, the engine resources it holds, and what it is for. Each road is
set by hand with its length in whole days (the engine's roads are whole days: engine/roads.py; the generator puts a stopping place
on any road over a day and a half, so a road of 2 days is two one-day legs). Positions are sketched in days (x, y) and then fitted
in km so that each road's straight length matches its days (DAY_KM flat, HILL_KM over hills): the targets the generator's pins aim
at. The world builder realises these with the land generator (places pinned by position, land, soil and resources; roads pinned)
and is checked against this file."""
import math

LAND = {   # land type: (engine covers it is made of, colour on the map, the generator's vacant `land` word)
    "farmland": (["field", "meadow", "pasture", "scrub"], "#c9d98a", "open"),
    "rich vale": (["meadow", "pasture", "scrub", "water"], "#8fc45a", "open"),
    "forest": (["forest", "scrub", "meadow"], "#3f7a3a", "wood"),
    "old forest": (["forest"], "#2a5a2a", "wood"),
    "heath": (["heath", "scrub", "pasture"], "#c8a3c8", "waste"),
    "moor": (["moor", "heath", "pasture"], "#a68aa0", "waste"),
    "rock hills": (["rock", "heath", "pasture"], "#9a8f80", "rock"),
    "chalk down": (["rock", "pasture", "heath"], "#d8d2c0", "rock"),
    "fen": (["fen", "water", "meadow"], "#7fb3a8", "waste"),
    "lake": (["water", "meadow", "forest"], "#6aa3d6", "open"),
    "coast": (["saltmarsh", "water", "pasture"], "#9fc9d6", "waste"),
}
DAY_KM, HILL_KM = 18.0, 15.0       # a day's road in a straight line, on flat ground and over hills (the generator: 8 hours a day)


def P(name, x, y, land, soil="fair", res=(), kind="vacant", note="", value=0):
    """x, y: a sketch in days. kind: home:A (a people's starting village) or vacant (land no one holds). value: 0 ordinary, 1 good,
    2 high value (contested by design)."""
    return {"name": name, "sx": x, "sy": y, "land": land, "soil": soil, "res": list(res), "kind": kind, "note": note, "value": value}


def R(a, b, days, hill=False):
    return (a, b, int(days), bool(hill))


WORLDS = {}

# ---------------------------------------------------------------- 2 peoples
WORLDS["W1"] = {
    "title": "W1 Twin Hollows: two peoples, near, one prize between them",
    "peoples": ["A", "B"],
    "summary": "Small and mirror-symmetric. Two villages, each a day from a rich vale between them with the only mill site; the fen "
               "behind the vale is reached only through it. The only stone and copper are on one hill two days from both (or a day "
               "beyond each one's wood). Each has a wood and a heath of its own a day out.",
    "places": [
        P("Ashford", 0, 1, "farmland", "fair", ["wood", "grass"], "home:A"),
        P("Brockley", 2, 1, "farmland", "fair", ["wood", "grass"], "home:B"),
        P("Middlemead", 1, 1, "rich vale", "rich", ["grass", "fish", "mill site"], note="the best land and the only mill site", value=2),
        P("Lower Meads", 1, 0, "fen", "fair", ["fish", "grass"], note="hay and fish; its only way in is through Middlemead", value=1),
        P("Coppice Hill", 1, 2.2, "rock hills", "poor", ["seam", "quarry", "grass"], note="the only stone and copper", value=2),
        P("Ash Wood", -0.4, 2, "forest", "fair", ["wood", "game"]),
        P("Ash Heath", -0.8, 0.3, "heath", "poor", ["grass"]),
        P("Brock Wood", 2.4, 2, "forest", "fair", ["wood", "game"]),
        P("Brock Heath", 2.8, 0.3, "heath", "poor", ["grass"]),
    ],
    "roads": [R("Ashford", "Middlemead", 1), R("Brockley", "Middlemead", 1), R("Middlemead", "Lower Meads", 1),
              R("Ashford", "Coppice Hill", 2, True), R("Brockley", "Coppice Hill", 2, True), R("Ashford", "Ash Wood", 1),
              R("Ashford", "Ash Heath", 1), R("Brockley", "Brock Wood", 1), R("Brockley", "Brock Heath", 1),
              R("Ash Wood", "Coppice Hill", 1, True), R("Brock Wood", "Coppice Hill", 1, True)],
}

WORLDS["W2"] = {
    "title": "W2 Over the Pass: two valleys, a short hard way and a long rich one",
    "peoples": ["A", "B"],
    "summary": "Medium and mirror-symmetric. Each people holds the head of its own valley, with a private backyard of wood, farmland "
               "and fen a day or two down-valley. The pass between the valleys, a day up from each head, has the copper and stone. "
               "Both valleys open onto a shared lowland three days south: the richest land, the mill site and the only salt. Going "
               "for metal brings early contact at the pass; expanding brings late contact on the plain.",
    "places": [
        P("Ashby Head", 1, 4, "farmland", "fair", ["wood", "grass"], "home:A"),
        P("Brook Head", 3, 4, "farmland", "fair", ["wood", "grass"], "home:B"),
        P("High Gap", 2, 4.4, "rock hills", "poor", ["seam", "quarry"], note="the pass: copper and stone", value=2),
        P("Ashby Wood", 0.2, 3.3, "forest", "fair", ["wood", "game"]),
        P("Ashdale", 1.1, 3, "farmland", "fair", ["grass"], note="A's backyard: good fields", value=1),
        P("Ash Fen", 0.5, 2.2, "fen", "fair", ["fish", "grass"]),
        P("Westmoor", 0, 4.5, "moor", "poor", ["grass"]),
        P("Brook Wood", 3.8, 3.3, "forest", "fair", ["wood", "game"]),
        P("Brookdale", 2.9, 3, "farmland", "fair", ["grass"], note="B's backyard: good fields", value=1),
        P("Brook Fen", 3.5, 2.2, "fen", "fair", ["fish", "grass"]),
        P("Eastmoor", 4, 4.5, "moor", "poor", ["grass"]),
        P("Two Waters", 2, 1, "rich vale", "rich", ["grass", "fish", "mill site"], note="where the valleys' rivers meet: the prize", value=2),
        P("Southmead", 1, 0.6, "rich vale", "rich", ["grass"], value=1),
        P("Eastmead", 3, 0.6, "rich vale", "rich", ["grass"], value=1),
        P("Salt Strand", 2, 0, "coast", "poor", ["salt", "fish"], note="the only salt", value=1),
    ],
    "roads": [R("Ashby Head", "High Gap", 1, True), R("Brook Head", "High Gap", 1, True),
              R("Ashby Head", "Ashby Wood", 1), R("Ashby Head", "Ashdale", 1), R("Ashby Head", "Westmoor", 1, True), R("Ashdale", "Ash Fen", 1),
              R("Ashby Wood", "Ash Fen", 1), R("Ash Fen", "Southmead", 2), R("Ashdale", "Two Waters", 2),
              R("Brook Head", "Brook Wood", 1), R("Brook Head", "Brookdale", 1), R("Brook Head", "Eastmoor", 1, True), R("Brookdale", "Brook Fen", 1),
              R("Brook Wood", "Brook Fen", 1), R("Brook Fen", "Eastmead", 2), R("Brookdale", "Two Waters", 2),
              R("Southmead", "Two Waters", 1), R("Eastmead", "Two Waters", 1), R("Two Waters", "Salt Strand", 1),
              R("Southmead", "Salt Strand", 1), R("Eastmead", "Salt Strand", 1)],
}

WORLDS["W3"] = {
    "title": "W3 The Long Frontier: two neighbours on the coast, a wide country inland",
    "peoples": ["A", "B"],
    "summary": "Large and asymmetric (positions rotated between models). The peoples start two days apart on a coastal strip, each a "
               "day from the ford between them: A has the salt and fish, B the stone. The ford is the way inland. The interior is a "
               "frontier in rings: woods, meadows, a lake and moors within two days of the ford; a rich vale with a mill site and a "
               "deep forest at three; the only copper at four; a great rich basin and a second coast at six. Room to grow without "
               "meeting, and long supply lines.",
    "places": [
        P("Ashmouth", 0, 2, "coast", "fair", ["salt", "fish", "grass"], "home:A", "A: salt and fish, fair fields"),
        P("Barrowby", 0, 0, "chalk down", "fair", ["quarry", "grass"], "home:B", "B: stone, fair fields"),
        P("Midford", 0.6, 1, "rich vale", "rich", ["grass", "fish"], note="the ford between them and the way inland", value=2),
        P("Ashholt", 0.9, 2.9, "forest", "fair", ["wood", "game"]),
        P("Barrow Down", 0.9, -0.8, "chalk down", "poor", ["quarry", "grass"]),
        P("Greenhurst", 1.6, 1.9, "forest", "fair", ["wood", "game"]),
        P("Longmead", 1.6, 0.4, "rich vale", "rich", ["grass", "fish"], value=1),
        P("Hartmoor", 1.8, 3.6, "moor", "poor", ["grass"]),
        P("Wickfen", 1.9, -0.6, "fen", "fair", ["fish", "grass"]),
        P("Mirewater", 2.6, 1.2, "lake", "fair", ["fish", "wood"]),
        P("Deepwood", 3.4, 2.6, "old forest", "fair", ["wood", "game"], note="the great timber", value=1),
        P("Hallow Vale", 3.5, 0, "rich vale", "rich", ["grass", "mill site"], note="rich land and a mill site, three days in", value=2),
        P("Highfold", 2.9, 3.8, "moor", "poor", ["grass"]),
        P("Coppermount", 4.4, 2.3, "rock hills", "poor", ["seam", "quarry", "grass"], note="the only copper", value=2),
        P("Riverbend", 4.5, 0.4, "rich vale", "rich", ["grass", "fish"], value=1),
        P("Far Heath", 3.9, 3.6, "heath", "poor", ["grass"]),
        P("Eastfen", 4.3, -0.7, "fen", "fair", ["fish", "grass"]),
        P("Sunvale", 6.4, 1.2, "rich vale", "rich", ["grass", "fish", "mill site"], note="the great basin, farthest out", value=2),
        P("Stonegate", 5.2, 2.8, "rock hills", "poor", ["quarry", "grass"]),
        P("Far Strand", 6.6, 0, "coast", "poor", ["salt", "fish"], note="the second salt", value=1),
    ],
    "roads": [R("Ashmouth", "Midford", 1), R("Barrowby", "Midford", 1), R("Ashmouth", "Ashholt", 1), R("Barrowby", "Barrow Down", 1),
              R("Midford", "Greenhurst", 1), R("Midford", "Longmead", 1), R("Ashholt", "Hartmoor", 1), R("Ashholt", "Greenhurst", 1),
              R("Barrow Down", "Wickfen", 1), R("Longmead", "Wickfen", 1), R("Greenhurst", "Mirewater", 1), R("Longmead", "Mirewater", 1),
              R("Greenhurst", "Deepwood", 2), R("Longmead", "Hallow Vale", 2), R("Hartmoor", "Highfold", 1, True), R("Deepwood", "Highfold", 1, True),
              R("Mirewater", "Coppermount", 2, True), R("Deepwood", "Coppermount", 1, True), R("Highfold", "Far Heath", 1), R("Far Heath", "Coppermount", 1, True),
              R("Hallow Vale", "Riverbend", 1), R("Hallow Vale", "Eastfen", 1), R("Riverbend", "Eastfen", 1), R("Riverbend", "Sunvale", 2),
              R("Coppermount", "Sunvale", 2), R("Coppermount", "Stonegate", 1, True), R("Sunvale", "Stonegate", 1), R("Sunvale", "Far Strand", 1),
              R("Eastfen", "Far Strand", 2)],
}

# ---------------------------------------------------------------- 3 peoples
_ang = lambda deg, r: (r * math.cos(math.radians(deg)), r * math.sin(math.radians(deg)))
WORLDS["W4"] = {
    "title": "W4 The Ring Basin: three peoples at three gates to one rich basin",
    "peoples": ["A", "B", "C"],
    "summary": "Near-symmetric. A fertile basin inside a ring of hills, entered by three gaps; each people starts a day outside one gap, "
               "with a backyard of its own a day out (A the great wood, B the quarry, C the upland grazing). Inside, a day past each "
               "gap, a rich mead; a day further, the mere at the centre with the mill site. The only copper is in the gorge where "
               "the basin drains, two days from B and C and five from A.",
    "places": [
        P("Ashgate", *_ang(90, 3), "farmland", "fair", ["wood", "grass"], "home:A"),
        P("Brackwell", *_ang(210, 3), "farmland", "fair", ["grass"], "home:B"),
        P("Colton", *_ang(330, 3), "farmland", "fair", ["grass"], "home:C"),
        P("North Gap", *_ang(90, 2), "rock hills", "poor", ["grass"], note="a gate into the basin"),
        P("West Gap", *_ang(210, 2), "rock hills", "poor", ["grass"], note="a gate into the basin"),
        P("East Gap", *_ang(330, 2), "rock hills", "poor", ["grass"], note="a gate into the basin"),
        P("Northmead", *_ang(90, 1), "rich vale", "rich", ["grass"], value=1),
        P("Westmead", *_ang(210, 1), "rich vale", "rich", ["grass"], value=1),
        P("Eastmead", *_ang(330, 1), "rich vale", "rich", ["grass"], value=1),
        P("The Mere", 0, 0, "lake", "rich", ["fish", "grass", "mill site"], note="the centre: fish and the mill site", value=2),
        P("The Gorge", *_ang(270, 2), "rock hills", "poor", ["seam", "quarry"], note="the only copper, where the basin drains", value=2),
        P("Ashwood", *_ang(120, 3.2), "old forest", "fair", ["wood", "game"], note="A's: the great wood"),
        P("Ash Moor", *_ang(60, 3.2), "moor", "poor", ["grass"]),
        P("Brack Quarry", *_ang(180, 3.2), "chalk down", "poor", ["quarry", "grass"], note="B's: stone"),
        P("Brack Wood", *_ang(240, 3.0), "forest", "fair", ["wood", "game"]),
        P("Colton Fell", *_ang(0, 3.2), "moor", "poor", ["grass"], note="C's: upland grazing"),
        P("Colton Wood", *_ang(300, 3.0), "forest", "fair", ["wood", "game"]),
    ],
    "roads": [R("Ashgate", "North Gap", 1, True), R("North Gap", "Northmead", 1), R("Northmead", "The Mere", 1),
              R("Brackwell", "West Gap", 1, True), R("West Gap", "Westmead", 1), R("Westmead", "The Mere", 1),
              R("Colton", "East Gap", 1, True), R("East Gap", "Eastmead", 1), R("Eastmead", "The Mere", 1),
              R("The Mere", "The Gorge", 2), R("Brack Wood", "The Gorge", 1, True), R("Colton Wood", "The Gorge", 1, True),
              R("Ashgate", "Ashwood", 1), R("Ashgate", "Ash Moor", 1), R("Brackwell", "Brack Quarry", 1), R("Brackwell", "Brack Wood", 1),
              R("Colton", "Colton Fell", 1), R("Colton", "Colton Wood", 1), R("Ashwood", "Brack Quarry", 2, True),
              R("Ash Moor", "Colton Fell", 2, True)],
}

WORLDS["W5"] = {
    "title": "W5 Three Countries: lowland, upland and woodland coast, each one people's",
    "peoples": ["A", "B", "C"],
    "summary": "Complementary (positions rotated). Each people starts in a country that has what the others lack: the lowland (A) "
               "rich soil and two mill sites but no stone and little wood; the upland (B) copper, stone and grazing but poor, cold "
               "fields; the woodland coast (C) timber, game, salt and fish but little ploughland. Each home is two days from a ford "
               "market at Threeways and four from each other home.",
    "places": [
        P("Lowbury", 0, 1, "farmland", "rich", ["grass", "fish"], "home:A", "A: rich fields; no stone, little wood"),
        P("Millbrook", -0.6, 1.8, "rich vale", "rich", ["grass", "fish", "mill site"], value=1),
        P("Wheatley", 0.7, 0.2, "farmland", "rich", ["grass"], value=1),
        P("Southmere", -0.3, 0, "fen", "fair", ["fish", "grass"]),
        P("Longacre", 1, 1.6, "rich vale", "rich", ["grass", "mill site"], value=1),
        P("Highcairn", 2.6, 4.2, "moor", "poor", ["quarry", "grass"], "home:B", "B: stone and grazing; poor, cold fields"),
        P("Coppermount", 3.3, 4.9, "rock hills", "poor", ["seam", "quarry"], note="the copper", value=2),
        P("Stonefell", 2.0, 4.9, "rock hills", "poor", ["quarry", "grass"]),
        P("Highmoor", 3.5, 3.7, "moor", "poor", ["grass"]),
        P("Tarn", 2.2, 3.3, "lake", "poor", ["fish", "grass"]),
        P("Holtmouth", 4, 0.6, "coast", "fair", ["salt", "fish", "wood"], "home:C", "C: timber, game, salt, fish; little ploughland"),
        P("Deepwood", 3.2, 1.3, "old forest", "fair", ["wood", "game"], value=1),
        P("Saltings", 4.8, 0, "coast", "poor", ["salt", "fish"]),
        P("Oakhurst", 4.6, 1.6, "forest", "fair", ["wood", "game"]),
        P("Cove", 3.2, -0.1, "coast", "poor", ["fish"]),
        P("Threeways", 2.1, 1.8, "rich vale", "rich", ["grass", "fish"], note="the ford where the countries' roads meet", value=2),
        P("Border Wood", 1.8, 2.6, "forest", "fair", ["wood", "game"]),
        P("Marchmead", 2.0, 0.6, "farmland", "fair", ["grass"]),
    ],
    "roads": [R("Lowbury", "Millbrook", 1), R("Lowbury", "Wheatley", 1), R("Lowbury", "Southmere", 1), R("Wheatley", "Southmere", 1),
              R("Lowbury", "Longacre", 1), R("Millbrook", "Longacre", 1), R("Longacre", "Threeways", 1),
              R("Highcairn", "Coppermount", 1, True), R("Highcairn", "Stonefell", 1, True), R("Highcairn", "Highmoor", 1, True),
              R("Highcairn", "Tarn", 1), R("Tarn", "Border Wood", 1), R("Stonefell", "Border Wood", 2, True), R("Border Wood", "Threeways", 1),
              R("Highmoor", "Oakhurst", 2, True), R("Longacre", "Border Wood", 1),
              R("Holtmouth", "Deepwood", 1), R("Holtmouth", "Saltings", 1), R("Holtmouth", "Oakhurst", 1), R("Holtmouth", "Cove", 1),
              R("Deepwood", "Threeways", 1), R("Cove", "Marchmead", 1), R("Marchmead", "Threeways", 1), R("Wheatley", "Marchmead", 1)],
}


def fit(w, iters=4000, lr=0.02):
    """Positions in km from the sketch, so each road's straight length is its days x DAY_KM (HILL_KM over hills), and places not
    joined stay at least a day's road apart (so the generator does not find a shorter way). Returns the largest road error, km."""
    import numpy as np
    names = [p["name"] for p in w["places"]]
    ix = {n: i for i, n in enumerate(names)}
    X = np.array([[p["sx"] * DAY_KM, p["sy"] * DAY_KM] for p in w["places"]], float)
    want = {}
    for a, b, d, hill in w["roads"]:
        want[(ix[a], ix[b])] = d * (HILL_KM if hill else DAY_KM)
    joined = set(want) | {(j, i) for i, j in want}
    for _ in range(iters):
        G = np.zeros_like(X)
        for (i, j), L in want.items():
            v = X[i] - X[j]; d = np.linalg.norm(v) + 1e-9
            g = (d - L) / L * v / d
            G[i] += g; G[j] -= g
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                if (i, j) in joined:
                    continue
                v = X[i] - X[j]; d = np.linalg.norm(v) + 1e-9
                if d < 0.95 * DAY_KM:
                    g = (d - 0.95 * DAY_KM) / DAY_KM * v / d
                    G[i] += g; G[j] -= g
        X -= lr * DAY_KM * G
    X -= X.min(0)
    X += 8.0                                                               # a margin in km round the places
    for p, (x, y) in zip(w["places"], X):
        p["x"], p["y"] = round(float(x), 1), round(float(y), 1)
    w["size_km"] = round(float(X.max() + 8.0), 0)
    errs = [abs(np.linalg.norm(X[i] - X[j]) - L) for (i, j), L in want.items()]
    return max(errs)


for _w in WORLDS.values():
    _w["fit_err_km"] = round(fit(_w), 1)

# The land's large shapes, by the places they run through (drawn on the maps; given to the generator as its features): ridges and
# massifs (hill country), rivers (from source to mouth), coasts (the sea's side), basins, old woods.
FEATURES = {
    "W1": [("massif", ["Coppice Hill"]), ("river", ["Coppice Hill", "Middlemead", "Lower Meads"])],
    "W2": [("ridge", ["High Gap", "Two Waters"], {"gap_at": "High Gap", "stop_short": 0.45}), ("massif", ["Westmoor"]), ("massif", ["Eastmoor"]),
           ("river", ["Ashby Head", "Ashdale", "Two Waters"]), ("river", ["Brook Head", "Brookdale", "Two Waters"]),
           ("river", ["Two Waters", "Salt Strand"]), ("coast", "south")],
    "W3": [("coast", "west"), ("river", ["Mirewater", "Longmead", "Midford"]), ("massif", ["Coppermount", "Stonegate"]),
           ("massif", ["Highfold"]), ("fen", ["Wickfen"]), ("fen", ["Eastfen"]), ("oldwood", ["Deepwood"]),
           ("river", ["Riverbend", "Sunvale", "Far Strand"]), ("basin", ["Sunvale"])],
    "W4": [("ring", ["North Gap", "West Gap", "East Gap", "The Gorge"]), ("basin", ["The Mere"]), ("river", ["The Mere", "The Gorge"]),
           ("oldwood", ["Ashwood"])],
    "W5": [("massif", ["Highcairn", "Coppermount", "Stonefell", "Highmoor"]), ("river", ["Tarn", "Border Wood", "Threeways", "Marchmead", "Cove"]),
           ("river", ["Millbrook", "Longacre", "Threeways"]), ("coast", "south"), ("oldwood", ["Deepwood"]), ("fen", ["Southmere"])],
}
