"""Round 3: the refined list, after rounds 1 and 2 (02zp §W).

Cut, and why:
- aurochs, bison, wild horse: die out even in wildwood (slow breeders losing grass to red deer); out of the era anyway.
- fallow deer: fails and cuts red deer to a third (the same food); introduced; a park animal for husbandry, not the web.
- great bustard: never finds open enough ground at this scale.
- brown bear: cannot hold a population at real numbers; a legendary individual (D2-195), not a density.
- wildcat, buzzard: redundant with fox and owls on the same voles; they push each other about and add nothing people use.
- pine marten, water vole: fragile (a +-25% change kills them in 1 run in 6); kept as stocks (a fine fur in old wood cores; a
  sign of clean water), not web members.
Changed:
- heron, golden eagle: capped by territory (too many at real intakes);
- black grouse: the moor's edge only (heath with birch and scrub, above 150 m);
- one small-predator guild kept: stoat and polecat (ermine; the polecat is the ferret's wild form);
- coast: sea fish near the shore feed seabirds, seals and sea eagles (round 2 had no sea food).
"""
import copy
from web import K
import kinds0

KEEP = ["red deer", "roe deer", "wild boar", "brown hare", "mountain hare", "voles and mice", "red grouse", "badger", "fox", "wolf",
        "beaver", "otter", "eel", "wildfowl", "rats",
        "crane", "grey heron", "grey geese", "sea eagle", "golden eagle", "black grouse", "raven", "elk", "lynx", "capercaillie",
        "red squirrel", "stoat and polecat", "owls", "rabbit", "woodpigeon", "seabirds", "seal", "salmon"]
KINDS = {n: copy.deepcopy(kinds0.KINDS[n]) for n in KEEP}
KINDS["grey heron"]["cap"] = 0.8
KINDS["golden eagle"]["cap"] = 0.01
KINDS["black grouse"]["hab"] = {"heath": 0.6, "shrub": 0.5}
KINDS["black grouse"]["limits"] = {"h": (150, 3000)}
KINDS["seabirds"]["diet"] = {"seafish": 4, "fish": 1}
KINDS["seal"]["diet"] = {"seafish": 4, "fish": 1, "salmon": 1}
KINDS["sea eagle"]["diet"] = {"fish": 2, "seafish": 2, "wildfowl": 2, "carrion": 1, "seabirds": 1, "eel": 1}
KINDS["otter"]["diet"] = {"fish": 4, "seafish": 1, "wildfowl": 0.5, "eel": 2}
KINDS["salmon"]["k"] = 0.0
KINDS["rabbit"]["notes"] = "introduced (Norman), warrens: a pack, off unless a world turns it on"

KINDS["black grouse"]["cap"] = 12
KINDS["woodpigeon"]["cap"] = 120
KINDS["golden eagle"]["cap"] = 0.008
PACK = {"rabbit": KINDS.pop("rabbit")}                  # introduced: on only in worlds that turn the pack on (tested in B)
