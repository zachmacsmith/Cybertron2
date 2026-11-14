"""Brief 4c of the wild layer (proposals/hunt_calibration.md §3.1, §3.3, §5, §9): the take as a baseline times multipliers, hunting
worth learning (the pace, learning behind a better hunter, teaching over days), and the crew's kill bonus for the drive only."""
import math

from cybertron2.engine import knowledge as KN, settle as ST, wild as WL
from cybertron2.engine.data import SKILL, TECHNIQUES
from cybertron2.engine.here import Here, Mind
from cybertron2.wild.kinds import HUNT

from tests.test_cybertron2_wild import _hunters, _party_hunt, generated  # noqa: F401


# ---------------------------------------------------------------------------------------------------------------- §3.1 the chance
def test_the_chance_is_one_minus_e_to_the_baseline_times_the_multipliers():
    for tech in ("hunt the wild", "stalk", "drive"):
        base = float(TECHNIQUES[tech]["take_base"])
        assert math.isclose(WL.take_chance(tech, 1.0, 1.0, 0.0, 1.0), 1 - math.exp(-base))       # a bare-handed novice: at base
        p0 = WL.take_chance(tech, 1.0, 1.0, 0.5, 1.0)
        armed = WL.gear(tech, {"crude weapon": 1})
        assert armed > 1.0 and WL.gear(tech, {}) == 1.0                                             # gear as a multiplier, by item
        assert WL.take_chance(tech, 1.0, armed, 0.5, 1.0) > p0                                      # each multiplier raises it
        assert WL.take_chance(tech, 3.0, 1.0, 0.5, 1.0) > p0
        assert WL.take_chance(tech, 1.0, 1.0, 0.5, 1.35) > p0
        assert WL.take_chance(tech, 1.0, 1.0, 0.8, 1.0) < p0                                        # a beast quicker to flee: less
        top = WL.take_chance(tech, 8.0, armed, 0.0, 1.35)
        assert 0.95 < top < 1.0 or top > WL.take_chance(tech, 7.0, armed, 0.0, 1.35)               # no clip at 0.95: still rising
    assert WL.chance(20.0) < 1.0 and WL.chance(3.0) > 0.95                                          # never certain, never clipped


def test_the_crew_bonus_is_for_the_drive_only():
    flee, fam = 0.5, 1.0
    assert TECHNIQUES["drive"].get("crew")
    assert WL.take_chance("drive", 1.0, 1.0, flee, fam, n_out=3) > WL.take_chance("drive", 1.0, 1.0, flee, fam, n_out=1)
    x1 = float(TECHNIQUES["drive"]["take_base"]) * (1 - flee)
    assert math.isclose(WL.take_chance("drive", 1.0, 1.0, flee, fam, n_out=3), 1 - math.exp(-x1 * (1 + 2 * float(HUNT["crew"]))))
    for tech in ("hunt the wild", "stalk"):                                                         # a party's gain there is the carry,
        assert WL.take_chance(tech, 1.0, 1.0, flee, fam, n_out=3) == WL.take_chance(tech, 1.0, 1.0, flee, fam, n_out=1)   # the eyes


def test_no_wild_method_keeps_a_weapon_ceiling():
    for tech in ("hunt the wild", "stalk", "drive", "snare", "net", "trap in water", "den work"):
        assert "weapon" not in TECHNIQUES[tech] and isinstance(TECHNIQUES[tech].get("gear"), dict), tech


# ---------------------------------------------------------------------------------------------------------------- §3.3 the pace
def test_practice_raises_the_hunts_multiplier_from_one_toward_its_top():
    lo, hi = KN.curve("stalk")
    assert (lo, hi) == (1.0, 8.0) and not KN.hard("gather wild food")                          # gathering's curve unchanged
    assert KN.skill_of_practice("gather wild food", 30) == round(KN.curve("gather wild food")[0] + (KN.curve("gather wild food")[1]
                                                                 - KN.curve("gather wild food")[0]) * (1 - math.exp(-30 / SKILL["tau"])), 4)
    top = float(SKILL["top_hard"])
    xs = [KN.skill_of_practice("stalk", p) for p in (0, 10, 20, top / 2, top * 0.8, top, 2 * top)]
    assert xs[0] == 1.0 and all(b > a for a, b in zip(xs, xs[1:-1])) and xs[-2] == xs[-1] == 8.0
    assert 2.5 <= KN.skill_of_practice("stalk", top / 2) <= 3.5                                    # capable about half way
    for p in (5.0, 25.0, 40.0):
        assert math.isclose(KN.practice_of_skill("stalk", KN.skill_of_practice("stalk", p)), p, rel_tol=1e-3)


def test_hunting_practice_lifts_the_multiplier_and_a_youth_learns_twice_as_fast(generated):  # noqa: F811
    w, _, wood = _hunters(generated, n=2, knows=("hunt the wild",))
    for n in ("H0", "H1"):
        w.s["know"][n]["hunt the wild"]["skill"] = 1.0
    w.s["people"]["H1"]["stage"] = "youth"
    for n in ("H0", "H1"):
        KN.tried(Here(w, n), Mind(w, n), "hunt the wild", True, units=10)
    adult, youth = (float(w.s["know"][n]["hunt the wild"]["skill"]) for n in ("H0", "H1"))
    assert adult > 1.0
    assert math.isclose(KN.practice_of_skill("hunt the wild", youth), 2 * KN.practice_of_skill("hunt the wild", adult), rel_tol=1e-3)


def test_the_hunts_pace_scales_with_the_lifespan(generated):  # noqa: F811
    w, _, wood = _hunters(generated, n=1, knows=("hunt the wild",))
    w.s["know"]["H0"]["hunt the wild"]["skill"] = 1.0
    w.spec["lifespan"] = 64                                                                      # twice the default: half the pace
    KN.tried(Here(w, "H0"), Mind(w, "H0"), "hunt the wild", True, units=10)
    assert math.isclose(KN.practice_of_skill("hunt the wild", w.s["know"]["H0"]["hunt the wild"]["skill"]), 5.0, rel_tol=1e-3)


def test_a_hunt_is_practised_by_how_it_went(generated):  # noqa: F811
    w, _, wood = _hunters(generated, n=1, knows=("hunt the wild",))
    w.s["know"]["H0"]["hunt the wild"]["skill"] = 1.0
    ms = [WL.member(Here(w, "H0"), Mind(w, "H0"), Here(w, "H0").hands, 1.0, 2.0)]
    WL.practise(ms, "hunt the wild", {"kills": {"H0": 0}, "t": {"H0": 2.0}})
    miss = KN.practice_of_skill("hunt the wild", w.s["know"]["H0"]["hunt the wild"]["skill"])
    WL.practise(ms, "hunt the wild", {"kills": {"H0": 1}, "t": {"H0": 2.0}})
    both = KN.practice_of_skill("hunt the wild", w.s["know"]["H0"]["hunt the wild"]["skill"])
    assert math.isclose(miss, 2.0, rel_tol=1e-3) and math.isclose(both - miss, 2.0 * float(SKILL["kill_hard"]), rel_tol=1e-3)


def test_behind_a_master_a_novice_learns_about_twice_as_fast_as_alone(generated):  # noqa: F811
    w, _, wood = _hunters(generated, n=3, knows=("hunt the wild",))
    w.s["know"]["H0"]["hunt the wild"]["skill"] = 8.0                                          # the master leads
    for n in ("H1", "H2"):
        w.s["know"][n]["hunt the wild"]["skill"] = 1.0
    party = [WL.member(Here(w, n), Mind(w, n), Here(w, n).hands, KN.skill(Mind(w, n), "hunt the wild"), 2.0) for n in ("H0", "H1")]
    alone = [WL.member(Here(w, "H2"), Mind(w, "H2"), Here(w, "H2").hands, 1.0, 2.0)]
    for _ in range(5):                                                                           # the same trips: no kill on any
        WL.practise(party, "hunt the wild", {"kills": {"H0": 0, "H1": 0}, "t": {"H0": 2.0, "H1": 2.0}})
        WL.practise(alone, "hunt the wild", {"kills": {"H2": 0}, "t": {"H2": 2.0}})
    pr = lambda n: KN.practice_of_skill("hunt the wild", w.s["know"][n]["hunt the wild"]["skill"])   # noqa: E731
    assert 1.7 <= pr("H1") / pr("H2") <= float(SKILL["lead_hard"]) + 1e-9


def test_a_party_hunt_practises_each_member_once_when_it_is_settled(generated):  # noqa: F811
    w, _, wood = _hunters(generated, n=2, knows=("hunt the wild",))
    w.s["know"]["H0"]["hunt the wild"]["skill"] = 8.0
    w.s["know"]["H1"]["hunt the wild"]["skill"] = 1.0
    for n in ("H0", "H1"):
        w.s["containers"][w.s["people"][n]["hands"]]["goods"]["crude weapon"] = 1
    _party_hunt(w, ["H0", "H1"], {"do": "gather", "what": "hunt the wild", "at": wood})
    p = KN.practice_of_skill("hunt the wild", w.s["know"]["H1"]["hunt the wild"]["skill"])
    t = float(TECHNIQUES["hunt the wild"]["units"])
    lead = min(float(SKILL["lead_hard"]), 1 + 7.0 / 8.0)
    assert math.isclose(p, t * lead, rel_tol=1e-3) or math.isclose(p, t * lead * float(SKILL["kill_hard"]), rel_tol=1e-3), p


# ---------------------------------------------------------------------------------------------------------------- §3.3 teaching
def _teach_day(w, teacher, learner, tech):
    from cybertron2.engine import run as R
    w.s["today"] = R.blank_today()
    w.s["today"]["teach"].append({"by": teacher, "to": learner, "tech": tech})
    w.s["today"]["learn"].append({"by": learner, "from": teacher, "tech": tech})
    return ST.settle_teaching(w, w.s["today"])


def test_ten_days_teaching_bring_a_youth_near_the_teacher_with_no_level_cap(generated):  # noqa: F811
    w, _, wood = _hunters(generated, n=3, knows=("stalk",))
    w.s["know"]["H0"]["stalk"]["skill"] = 8.0
    w.s["people"]["H1"]["stage"] = "youth"
    for n in ("H1", "H2"):
        w.s["know"][n].pop("stalk", None)
    first = None
    for d in range(10):
        out = _teach_day(w, "H0", "H1", "stalk")
        _teach_day(w, "H0", "H2", "stalk")
        if d == 0:
            first = float(w.s["know"]["H1"]["stalk"]["skill"])
        assert not any("nothing more" in x for x in out.get("H1", [])), out                        # no refusal after the first day
    youth, adult = (float(w.s["know"][n]["stalk"]["skill"]) for n in ("H1", "H2"))
    lo = KN.curve("stalk")[0]
    assert first < 4.0                                                                           # a day gives a share, not a jump
    assert youth >= 8.0 - 0.1 * (8.0 - lo)                                                       # near the teacher: 97% of the gap
    assert lo + 0.7 * (8.0 - lo) <= adult < youth                                                # an adult about 80%
    assert w.s["know"]["H1"]["stalk"]["level"] == "known" and w.s["know"]["H2"]["stalk"]["level"] == "capable"


def test_teaching_is_refused_only_when_nothing_is_left_to_give(generated):  # noqa: F811
    w, _, wood = _hunters(generated, n=2, knows=("stalk",))
    w.s["know"]["H0"]["stalk"]["skill"] = 3.0
    w.s["know"]["H1"]["stalk"] = dict(w.s["know"]["H0"]["stalk"], level="capable", skill=3.0)
    out = _teach_day(w, "H0", "H1", "stalk")
    assert any("nothing more" in x for x in out["H1"])


# ---------------------------------------------------------------------------------------------------------------- the rule code
def test_no_kind_or_method_is_named_in_the_take_rule():
    import inspect
    src = (inspect.getsource(WL.take_chance) + inspect.getsource(WL.gear) + inspect.getsource(WL.practise)).lower()
    import re
    assert not [k for k in ("deer", "hare", "boar", "pigeon", "drive", "stalk", "hunt the wild", "crude weapon")
                if re.search(r"\b" + k + r"s?\b", src)]
