"""The five monoculture worlds (docs/cybertron2/proposals/monoculture_five_worlds.md §2 to §6), as designed (not generated).

The form is the peoples worlds' (cybertron2/specs/peoples_design.py): each place set by hand (its land, a bundle of engine covers;
soil; the engine resources it holds; what it is for), each road in whole days; positions sketched in days and fitted in km so each
road's straight length matches its days. Added for these worlds: `known` (known to the founders at the start; everything else is
unexplored, D4-47), `room` (households a vacant place has land for), `elders` (known only to the old), and `mark` (a rumour line, a
feral herd, a remnant family)."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from cybertron2.specs.peoples_design import LAND, R, fit  # noqa: E402


def M(name, x, y, land, soil="fair", res=(), kind="vacant", room=0, known=False, note="", mark="", elders=False):
    return {"name": name, "sx": x, "sy": y, "land": land, "soil": soil, "res": list(res), "kind": kind, "room": room,
            "known": known or kind.startswith("home:"), "note": note, "mark": mark, "elders": elders, "value": 0}


WORLDS = {}

WORLDS["M1"] = {
    "title": "World 1 Fallowmere: a farming village at the edge of the wild wood",
    "groups": {"A": "Fallowmere: 13 in 3 households (farming, cattle, woodcraft)"},
    "summary": "The baseline, with the fewest systems. Home feeds its 13 with a little to spare; everything beyond a day is unexplored, "
               "and most of it is better than home. The best land (Broadwater, a mill site) is known only by a rumour line. Wolves and "
               "boar keep to the old woods to the west; stone is three days off in the hills.",
    "places": [
        M("Fallowmere", 0, 0, "farmland", "fair", ["grass", "wood", "fish"], "home:A", room=3),
        M("Fallow Wood", -1, 0.1, "forest", "fair", ["wood", "game"], room=1, known=True),
        M("Southmead", 0, -1, "rich vale", "rich", ["grass", "fish"], room=2, known=True),
        M("The Ford", 1, 0, "farmland", "fair", ["grass"], room=1, known=True),
        M("Broadwater", 2, 0.1, "rich vale", "rich", ["grass", "fish", "mill site"], room=4, mark="rumour"),
        M("Hollins", -1, 1.1, "farmland", "fair", ["grass", "wood"], room=3),
        M("Greenhythe", 0.9, -1.7, "fen", "fair", ["fish", "grass"], room=1),
        M("Hartwood", -2, 0, "old forest", "fair", ["wood", "game"], room=1, note="wolves, boar"),
        M("Thornheath", -1, -1.6, "heath", "poor", ["grass"], room=1),
        M("Longmere", 2.8, 0.9, "lake", "fair", ["fish", "grass"], room=2),
        M("Stonebarrow", -2, 1.6, "rock hills", "poor", ["quarry", "grass"], room=1),
        M("Upper Hollins", -0.6, 2.1, "farmland", "fair", ["grass"], room=3),
        M("Kingsmead", 2.9, -0.9, "rich vale", "rich", ["grass", "fish"], room=3),
        M("Ashen Down", -0.1, 1.9, "chalk down", "poor", ["grass"], room=2),
        M("Wolfcombe", -3.6, 0, "forest", "fair", ["wood", "game"], room=1, note="the wolves' ground"),
        M("Far Meadows", 3.8, 0.4, "rich vale", "rich", ["grass", "fish"], room=4),
        M("Highbarrow", -2.9, 2.2, "moor", "poor", ["grass"], room=1),
        M("Eastmarch", 3.7, -1.8, "farmland", "fair", ["grass", "wood"], room=3),
    ],
    "roads": [R("Fallowmere", "Fallow Wood", 1), R("Fallowmere", "Southmead", 1), R("Fallowmere", "The Ford", 1),
              R("The Ford", "Broadwater", 1), R("Fallow Wood", "Hollins", 1), R("Southmead", "Greenhythe", 1),
              R("Fallow Wood", "Hartwood", 1), R("Southmead", "Thornheath", 1), R("Broadwater", "Longmere", 1),
              R("Hollins", "Stonebarrow", 1, True), R("Hollins", "Upper Hollins", 1), R("Broadwater", "Kingsmead", 1),
              R("Hollins", "Ashen Down", 1), R("Hartwood", "Wolfcombe", 2), R("Longmere", "Far Meadows", 1),
              R("Kingsmead", "Far Meadows", 1), R("Stonebarrow", "Highbarrow", 1, True), R("Kingsmead", "Eastmarch", 1),
              R("Greenhythe", "Kingsmead", 2)],
}

WORLDS["M2"] = {
    "title": "World 2 Eelmouth Reach: a fishing and salt village at a river's mouth",
    "groups": {"A": "Eelmouth: 12 in 3 households (weir, traps, salt; no fields, no cattle)"},
    "summary": "The rebuilt Eelmouth made into a long run. The runs give a glut each autumn; the fishery has a ceiling. Upriver, "
               "unexplored, is field land (Kingsford, by the Brook wife's rumour; Upper Reach with a mill site), a second fishery on a "
               "lake that can be fished down, and a feral herd on Barrow Down. Copper at Coldstone, with nobody who knows smelting.",
    "shore": {"south": ["Eelmouth", "The Saltings", "Greyhythe"]},
    "places": [
        M("Eelmouth", 0, 0, "coast", "fair", ["salt", "fish", "runs"], "home:A", room=3),
        M("The Saltings", 1, 0, "coast", "poor", ["salt", "fish"], room=1, known=True),
        M("Withy Holt", -1, 0.3, "fen", "fair", ["fish", "grass", "withies"], room=1, known=True),
        M("Kingsford", 0.1, 2, "farmland", "fair", ["grass", "fish", "runs"], room=3, mark="rumour"),
        M("Reedmere", -1.4, 1.3, "fen", "fair", ["fish", "grass"], room=1),
        M("Middlemere", 1.2, 1.6, "lake", "fair", ["fish", "grass"], room=2, note="its own stock"),
        M("Oakhanger", -2, 0.5, "forest", "fair", ["wood", "game"], room=1),
        M("Upper Reach", 0, 3, "rich vale", "rich", ["grass", "fish", "mill site", "runs"], room=4),
        M("Barrow Down", 1.8, 2.5, "chalk down", "poor", ["grass"], room=2, mark="herd"),
        M("Ashcombe", -1.6, 2.4, "forest", "fair", ["wood", "game"], room=1),
        M("Greyhythe", 3, 0, "coast", "poor", ["salt", "fish"], room=1),
        M("Long Acre", 0.9, 3.1, "farmland", "fair", ["grass"], room=3),
        M("Fernhill", -1.4, 3.4, "heath", "poor", ["grass"], room=1),
        M("Highreach", -0.2, 4, "rich vale", "rich", ["grass", "fish", "runs"], room=3, note="the salmon's spawning reach"),
        M("Coldstone", 2.3, 3.4, "rock hills", "poor", ["seam", "quarry"], room=1),
        M("Mere End", 2.7, 1.9, "lake", "poor", ["fish"], room=1),
    ],
    "roads": [R("Eelmouth", "The Saltings", 1), R("Eelmouth", "Withy Holt", 1), R("Eelmouth", "Kingsford", 2),
              R("Withy Holt", "Reedmere", 1), R("The Saltings", "Middlemere", 1), R("Withy Holt", "Oakhanger", 1),
              R("Kingsford", "Upper Reach", 1), R("Middlemere", "Barrow Down", 1), R("Reedmere", "Ashcombe", 1),
              R("The Saltings", "Greyhythe", 2), R("Kingsford", "Long Acre", 1), R("Ashcombe", "Fernhill", 1),
              R("Upper Reach", "Highreach", 1), R("Barrow Down", "Coldstone", 1, True), R("Barrow Down", "Mere End", 1),
              R("Middlemere", "Kingsford", 1)],
}

WORLDS["M3"] = {
    "title": "World 3 Highfold: two hamlets of herders and smiths, a day apart over a pass",
    "groups": {"A": "Highfold: 8 in 2 households (cattle, hay, cheese)", "B": "Coldwell: 7 in 2 households (smith, quarry, hunting)"},
    "summary": "High, cold and short of summer: the weather follows height. Hay made in summer is what the cattle live on; the pass between "
               "the hamlets can kill in winter. Down each valley, three to four days off and unexplored, lies the lowland where both rivers "
               "meet (Lowdale). Wolves and bear in the valley woods.",
    "places": [
        M("Highfold", 0, 0, "moor", "poor", ["grass"], "home:A", room=2),
        M("Coldwell", 1.2, 0, "rock hills", "poor", ["quarry", "grass"], "home:B", room=2),
        M("High Shieling", -0.2, 1, "moor", "poor", ["grass"], room=1, known=True, note="summer grazing"),
        M("Copper Gill", 1.7, 0.9, "rock hills", "poor", ["seam"], known=True),
        M("Tarn Beck", 0.5, -0.8, "lake", "poor", ["fish"], room=1, known=True),
        M("Lower Fold", -1, -1.4, "forest", "fair", ["grass", "wood"], room=2),
        M("Birkdale", 2.3, -1.4, "forest", "fair", ["wood", "game"], room=1, note="wolves, bear"),
        M("Wolf Scar", 0.9, -1.7, "rock hills", "poor", ["game"]),
        M("Greendale", -1.1, -2.5, "rich vale", "rich", ["grass", "fish"], room=3, mark="rumour"),
        M("Mill Foss", 2.3, -2.5, "farmland", "fair", ["grass", "fish", "mill site"], room=3),
        M("Oak Clough", 0.9, -2.7, "forest", "fair", ["wood", "game"], room=1),
        M("Lowdale", 0.4, -3.6, "rich vale", "rich", ["grass", "fish"], room=4, note="where both rivers meet"),
        M("Fordham", 3, -3.4, "farmland", "fair", ["grass"], room=3),
        M("Mosslake", -1.9, -3.3, "lake", "fair", ["fish", "grass"], room=2),
        M("Southmoss", 1.6, -3.9, "fen", "fair", ["fish"], room=1),
    ],
    "roads": [R("Highfold", "Coldwell", 1, True), R("Highfold", "High Shieling", 1, True), R("Coldwell", "Copper Gill", 1, True),
              R("Highfold", "Tarn Beck", 1), R("Highfold", "Lower Fold", 2, True), R("Coldwell", "Birkdale", 2, True),
              R("Tarn Beck", "Wolf Scar", 1, True), R("Lower Fold", "Greendale", 1), R("Birkdale", "Mill Foss", 1),
              R("Wolf Scar", "Oak Clough", 1), R("Greendale", "Lowdale", 1), R("Mill Foss", "Lowdale", 1), R("Mill Foss", "Fordham", 1),
              R("Greendale", "Mosslake", 1), R("Oak Clough", "Southmoss", 1), R("Lowdale", "Southmoss", 1)],
}

WORLDS["M4"] = {
    "title": "World 4 Oldbury: a village built for 30 holding 9, and a family no one knows of",
    "groups": {"A": "Oldbury: 9 in 3 households (mill, forge, plough and herd; two expert elders)",
               "B": "Westcot: a remnant family of 3, unknown to Oldbury"},
    "summary": "Capital for thirty, people for nine. The miller and the smith turn elder in the first week; the empty hamlets beyond the "
               "downs are known only to the elders, so the map dies with them unless it is told. Four empty houses at home to claim. "
               "Three days west, unexplored, a second family of the same people survives at Westcot.",
    "places": [
        M("Oldbury", 0, 0, "farmland", "rich", ["grass", "fish", "mill site"], "home:A", room=8, note="4 empty houses"),
        M("Oldbury Down", 0, 1, "chalk down", "poor", ["grass"], room=1, known=True),
        M("Clay Wood", -1, 0, "forest", "fair", ["wood", "game"], room=1, known=True),
        M("Springhead", 1, 0, "rich vale", "rich", ["grass", "fish"], room=2, known=True),
        M("Netherby", 0, 2, "farmland", "fair", ["grass"], room=3, elders=True, note="empty hamlet, 2 houses"),
        M("Chalkpit", -0.9, 1.6, "chalk down", "poor", ["quarry"], elders=True),
        M("Hamwell", 2, 1.2, "farmland", "fair", ["grass", "fish"], room=3, elders=True, note="empty, a ruined mill"),
        M("Coldharbour", -1.9, 1.5, "heath", "poor", ["grass"], room=1, elders=True),
        M("Westcot", -3, -0.5, "rich vale", "fair", ["grass", "fish"], "home:B", room=2),
        M("Ashmead", 2, -0.7, "rich vale", "rich", ["grass", "fish"], room=2),
        M("Fernbrook", -0.8, -1.3, "fen", "fair", ["fish", "grass"], room=1),
        M("Longdown", 0.9, 2.8, "chalk down", "poor", ["grass"], room=2),
        M("Oakley", -2.3, 0.6, "forest", "fair", ["wood", "game"], room=1),
        M("Southwold", 1.4, -1.8, "farmland", "fair", ["grass"], room=3),
        M("Marsh End", -0.2, -2.2, "fen", "fair", ["fish"], room=1),
        M("Highdown", -0.7, 2.9, "chalk down", "poor", ["grass"], room=1),
        M("Brookfield", 2.9, 0.3, "rich vale", "rich", ["grass", "fish"], room=3),
    ],
    "roads": [R("Oldbury", "Oldbury Down", 1), R("Oldbury", "Clay Wood", 1), R("Oldbury", "Springhead", 1),
              R("Oldbury Down", "Netherby", 1), R("Oldbury Down", "Chalkpit", 1), R("Springhead", "Hamwell", 2),
              R("Chalkpit", "Coldharbour", 1), R("Clay Wood", "Oakley", 1), R("Oakley", "Westcot", 1), R("Springhead", "Ashmead", 1),
              R("Clay Wood", "Fernbrook", 1), R("Netherby", "Longdown", 1), R("Ashmead", "Southwold", 1),
              R("Fernbrook", "Marsh End", 1), R("Netherby", "Highdown", 1), R("Hamwell", "Brookfield", 1), R("Ashmead", "Brookfield", 1)],
}

WORLDS["M5"] = {
    "title": "World 5 The Scattering: one people in four countries, each unexplored to the others",
    "groups": {"A": "Strand, the coast: 4 (fishing, salt)", "B": "Fell, the moor: 4 (cattle, smith, copper)",
               "C": "Meade, the vale: 4 (farming)", "D": "Holt, the wood: 4 (hunting, felling; a tent, no house)"},
    "summary": "Four families went four ways after a dark year. Each knows its own country (home and its gate a day off) and nothing "
               "beyond. Each home feeds its family and little more, and each lacks what another holds: salt, copper, grain, timber, "
               "cattle. Every home is two days from the ford at Threeways and four from each other home. Within a family the only "
               "partners are kin.",
    "shore": {"west": ["Holtmouth", "The Saltings", "Cove", "Greyhaven"]},
    "places": [
        M("Threeways", 0, 0, "rich vale", "rich", ["grass", "fish"], room=4, note="the ford: the meeting ground"),
        M("Westmere", -1, 0, "farmland", "fair", ["grass", "fish"], room=2, note="the coast's gate"),
        M("Tarn", 0, 1, "lake", "fair", ["fish", "grass"], room=1, note="the moor's gate"),
        M("Longacre", 1, 0, "rich vale", "rich", ["grass", "mill site"], room=3, note="the vale's gate"),
        M("Border Wood", 0, -1, "forest", "fair", ["wood", "game"], room=1, note="the wood's gate"),
        M("Midwold", -1.2, 1.2, "farmland", "fair", ["grass"], room=3),
        M("Fernmoor", 1.2, 1.2, "heath", "poor", ["grass"], room=1),
        M("Marchmead", 1.2, -1.2, "farmland", "fair", ["grass"], room=3),
        M("Southfold", -1.2, -1.2, "farmland", "fair", ["grass", "wood"], room=2),
        M("Holtmouth", -2, 0, "coast", "fair", ["salt", "fish"], "home:A", room=2),
        M("The Saltings", -2.2, -1, "coast", "poor", ["salt", "fish"], room=1),
        M("Cove", -2.2, 1, "coast", "poor", ["fish"], room=1),
        M("Greyhaven", -2.2, -2, "coast", "fair", ["fish", "grass"], room=2),
        M("Highcairn", 0, 2, "moor", "poor", ["quarry", "grass"], "home:B", room=2),
        M("Coppermount", 0.9, 2.6, "rock hills", "poor", ["seam", "quarry"]),
        M("Stonefell", -0.9, 2.6, "rock hills", "poor", ["quarry", "grass"], room=1),
        M("Highmoor", 0, 3, "moor", "poor", ["grass"], room=1),
        M("Lowbury", 2, 0, "farmland", "rich", ["grass", "fish"], "home:C", room=3),
        M("Millbrook", 2.6, 0.9, "rich vale", "rich", ["grass", "fish", "mill site", "runs"], room=3),
        M("Wheatley", 2.6, -0.9, "farmland", "rich", ["grass"], room=3),
        M("Southmere", 2.4, -1.9, "fen", "fair", ["fish", "grass"], room=1),
        M("Hartsmoot", 0, -2, "forest", "fair", ["wood", "game"], "home:D", room=2),
        M("Deepwood", 0.9, -2.6, "old forest", "fair", ["wood", "game"], room=1, note="wolves, bear"),
        M("Oakhurst", -0.9, -2.6, "forest", "fair", ["wood", "game"], room=1),
    ],
    "roads": [R("Holtmouth", "Westmere", 1), R("Westmere", "Threeways", 1), R("Highcairn", "Tarn", 1, True), R("Tarn", "Threeways", 1),
              R("Lowbury", "Longacre", 1), R("Longacre", "Threeways", 1), R("Hartsmoot", "Border Wood", 1),
              R("Border Wood", "Threeways", 1), R("Westmere", "Midwold", 1), R("Tarn", "Midwold", 1), R("Tarn", "Fernmoor", 1),
              R("Longacre", "Fernmoor", 1), R("Longacre", "Marchmead", 1), R("Border Wood", "Marchmead", 1),
              R("Border Wood", "Southfold", 1), R("Westmere", "Southfold", 1), R("Holtmouth", "The Saltings", 1),
              R("Holtmouth", "Cove", 1), R("The Saltings", "Greyhaven", 1), R("Highcairn", "Coppermount", 1, True),
              R("Highcairn", "Stonefell", 1, True), R("Highcairn", "Highmoor", 1, True), R("Lowbury", "Millbrook", 1),
              R("Lowbury", "Wheatley", 1), R("Wheatley", "Southmere", 1), R("Hartsmoot", "Deepwood", 1), R("Hartsmoot", "Oakhurst", 1)],
}

# Cross-roads (Zach, 23 Nov: the first maps were trees from home, "this feels potentially unrealistic ... should be a purposeful design
# choice"). Lowland and vale country is a mesh of lanes; fen and mountain stay sparse where the land is the reason. Each added road
# keeps every place's distance from home as designed, and in World 5 keeps the homes 4 days apart.
CROSS = {
    "M1": [R("The Ford", "Southmead", 1), R("Thornheath", "Hartwood", 1), R("Thornheath", "Greenhythe", 1),
           R("Upper Hollins", "Ashen Down", 1), R("Ashen Down", "Longmere", 2), R("Hartwood", "Stonebarrow", 1, True),
           R("Wolfcombe", "Highbarrow", 2, True), R("Far Meadows", "Eastmarch", 1)],
    "M2": [R("Reedmere", "Kingsford", 1), R("Ashcombe", "Upper Reach", 1), R("Fernhill", "Highreach", 1), R("Long Acre", "Barrow Down", 1),
           R("Long Acre", "Coldstone", 1, True), R("Oakhanger", "Ashcombe", 1)],
    "M3": [R("Mosslake", "Lowdale", 1), R("Oak Clough", "Lowdale", 1), R("Southmoss", "Fordham", 1), R("Wolf Scar", "Lower Fold", 1, True)],
    "M4": [R("Coldharbour", "Highdown", 1), R("Highdown", "Longdown", 1), R("Longdown", "Hamwell", 1), R("Oakley", "Coldharbour", 1),
           R("Fernbrook", "Westcot", 1), R("Marsh End", "Southwold", 1)],
    "M5": [R("Cove", "Midwold", 1), R("Stonefell", "Midwold", 1, True), R("Coppermount", "Fernmoor", 1, True), R("Millbrook", "Fernmoor", 1),
           R("Wheatley", "Marchmead", 1), R("Oakhurst", "Southfold", 1), R("Greyhaven", "Southfold", 1), R("Deepwood", "Southmere", 2)],
}
TREE_BY_DESIGN = {   # where a branch is left without a way round, and why
    "M2": "Greyhythe stays the end of the shore road: an open coast two days out, with nothing beyond it",
    "M3": "the heights are valley heads joined only by the pass: in winter the way round is through the lowland, 8 days",
    "M5": "each country is reached from the middle by its gate, with one side door; the homes stay 4 days apart",
}
# Room (Zach, 23 Nov: "why do so many of these places have so much small room?"). `room` is the households' worth of land the generator
# lays out at a vacant place (settle.py: 12 cells of about 2 ha each a household, nearest first, within field_km 2.5 km): it becomes
# the place's parcels, and no field can ever be made outside them. The first draft copied the peoples worlds' 1 to 4. Now by land and
# soil, with each world's deepest lush land larger, and each home with room to grow at home: a household of room is about 27 ha.
ROOM_BY_LAND = {("rich vale", "rich"): 8, ("rich vale", "fair"): 6, ("farmland", "rich"): 6, ("farmland", "fair"): 5,
                ("farmland", "poor"): 3, ("forest", "fair"): 3, ("old forest", "fair"): 2, ("lake", "fair"): 3, ("lake", "poor"): 2,
                ("lake", "rich"): 4, ("fen", "fair"): 2, ("coast", "fair"): 3, ("coast", "poor"): 1, ("chalk down", "poor"): 2,
                ("heath", "poor"): 1, ("moor", "poor"): 2, ("rock hills", "poor"): 1}
ROOM_SET = {   # the lush lands deep in the unexplored, and homes with room to grow
    "M1": {"Fallowmere": 6, "Far Meadows": 14, "Broadwater": 10},
    "M2": {"Eelmouth": 5, "Upper Reach": 12, "Highreach": 10},
    "M3": {"Highfold": 4, "Coldwell": 3, "Lowdale": 14, "Greendale": 8},
    "M4": {"Oldbury": 10, "Brookfield": 12, "Westcot": 4},
    "M5": {"Threeways": 12, "Holtmouth": 4, "Highcairn": 4, "Lowbury": 6, "Hartsmoot": 3},
}
for _k, _w in WORLDS.items():
    for _p in _w["places"]:
        _p["room_draft"] = _p["room"]
        if _p["room"] or _p["name"] in ROOM_SET.get(_k, {}):
            _p["room"] = ROOM_SET.get(_k, {}).get(_p["name"], ROOM_BY_LAND.get((_p["land"], _p["soil"]), _p["room"]))

for _k, _r in CROSS.items():
    WORLDS[_k]["tree_roads"] = list(WORLDS[_k]["roads"])
    WORLDS[_k]["roads"] = WORLDS[_k]["roads"] + _r

for _w in WORLDS.values():
    _w["fit_err_km"] = round(fit(_w), 1)

FEATURES = {
    "M1": [("river", ["Upper Hollins", "Hollins", "Fallowmere", "The Ford", "Broadwater", "Kingsmead", "Eastmarch"]),
           ("oldwood", ["Hartwood", "Wolfcombe"]), ("fen", ["Greenhythe"]), ("massif", ["Stonebarrow", "Highbarrow"])],
    "M2": [("coast", "south"), ("river", ["Highreach", "Upper Reach", "Kingsford", "Eelmouth"]), ("fen", ["Withy Holt", "Reedmere"]),
           ("massif", ["Coldstone"])],
    "M3": [("massif", ["Highfold", "Coldwell", "High Shieling", "Copper Gill"]),
           ("river", ["Highfold", "Lower Fold", "Greendale", "Lowdale", "Southmoss"]), ("river", ["Coldwell", "Birkdale", "Mill Foss", "Lowdale"]),
           ("oldwood", ["Birkdale"])],
    "M4": [("river", ["Springhead", "Oldbury", "Fernbrook", "Marsh End"]), ("river", ["Oakley", "Westcot"]),
           ("massif", ["Oldbury Down", "Chalkpit", "Longdown", "Highdown"]), ("fen", ["Fernbrook", "Marsh End"])],
    "M5": [("coast", "west"), ("massif", ["Highcairn", "Coppermount", "Stonefell", "Highmoor"]),
           ("river", ["Highmoor", "Highcairn", "Tarn", "Threeways", "Border Wood"]), ("river", ["Millbrook", "Lowbury", "Wheatley", "Southmere"]),
           ("oldwood", ["Deepwood"]), ("fen", ["Southmere"])],
}
