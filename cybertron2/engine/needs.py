"""What a person needs a night (D4-103; proposals/process_model.md part 5): one pure function per need, the night calls it, any
analysis calls the same.

`food(p, c)`: the night's food need and the cold's fall, from the PHYSICS tables (ration, shelter, shelter_cold, heat ring_cold,
camping, camping_fire) and the person's night `c`:
  state        housed | damaged | unsheltered | no_fuel | the floor state (beds.floor)
  cold         a cold night
  structure    the sleeping building's structure (camp, wattle, ...), or None
  warm, hearth, fire     the building's warmth (0..1), whether it has a hearth, whether its fire is lit
  gear         camp | bedroll | tent | out | None (sleeping out with what one has)
  open_fire, fire_gone   warmed by a fire in the open; that fire went out in the night
  fed_on_road  the share of a meal a good place on the road gave, or None
  mult, extra  the ration's multiplier and addition (an infant, a child, a pregnancy: life.ration_factor)
  care_fed     what the largest care gave a child, or None
Clocks: every value here is a night's (the day clock).
"""
from __future__ import annotations


def food(p, c) -> tuple:
    hp = p["heat"]
    state, cold = c["state"], c["cold"]
    need = float(p["ration"]) * float((p["shelter_cold"] if cold else p["shelter"]).get(state, 1.0))
    if cold and state == "housed" and c.get("structure") != "camp" and c.get("warm", 1.0) < 1.0:   # partly warmed (D2-159)
        ww = c.get("warm", 1.0)
        if not c.get("hearth"):
            need = float(p["ration"]) * float(hp["ring_cold"])
        else:
            need = float(p["ration"]) * (ww + float(p["shelter_cold"]["no_fuel"]) * (1 - ww))
    fall = 1.0
    gear = c.get("gear")
    if gear:
        out_ = p["camping"][gear]
        need = float(p["ration"]) * float(out_[1] if cold else out_[0])
        fall = float(out_[2])
        gone = c.get("fire_gone", False)                                     # the fire went out in the night (D4-83)
        if cold and c.get("open_fire") and gear != "camp" and not gone:      # a fire in the open warms (D2-159)
            need, fall = float(p["ration"]) * float(p["camping_fire"].get(gear, out_[1])), 0.0
        if gear == "camp" and cold and c.get("structure") is not None and (not c.get("fire") or gone):
            need, fall = float(p["ration"]) * float(p["camping"]["out"][1]), 0.0
    if state == "unsheltered" and c.get("fed_on_road") is not None:          # fed on the way at a good place (D2-109)
        need = min(need, float(p["ration"]) * float(c["fed_on_road"]))
    need = need * c.get("mult", 1.0) + c.get("extra", 0.0)                   # an infant, a child, a pregnancy (D2-141, D2-145)
    if c.get("care_fed") is not None:                                        # it eats all the largest care gave it (D4-64)
        need = max(need, c["care_fed"])
    return need, fall
