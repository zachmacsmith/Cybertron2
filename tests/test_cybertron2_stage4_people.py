"""Stage 4 of the fishing, hunting and materials wave (W-100): signs, people and worlds. Interface tests (D2-298): u8's river record,
leads and carried catch (wild/river.py); u9's prompt core (core.py), the eleven shapes (shapes.py), learning as one record
(learning.py), the watch act (verbs guard); u11's livelihoods and fill (livelihoods.py), the founders' lines (founders.py), the
gate check (landgen/gate_check.py) and Eelmouth remade (specs/make_eelmouth.py). Behaviour is read in live runs."""
import copy

import pytest

from cybertron2.engine import core as CORE, founders as FD, learning as LR, livelihoods as LV, perceive as PC, prompt as PR
from cybertron2.engine import run as R, shapes as SH, verbs as V, view as VW
from cybertron2.engine.data import WATER_WORKS
from cybertron2.engine.here import Here, Mind, Refused
from cybertron2.engine.world import World, load_spec
from cybertron2.wild import river as RV

HIGH = load_spec("cybertron2/specs/nutrition/runs_high.yaml")
EEL = load_spec("cybertron2/specs/nutrition/eelmouth.yaml")
OLD = load_spec("cybertron2/specs/nutrition/eelmouth_old.yaml")


def world(spec, **patch):
    s = copy.deepcopy(spec)
    s.update(patch)
    w = World(s)
    w.s["today"] = R.blank_today()
    return w


@pytest.fixture(scope="module")
def eel():
    return world(EEL)


def do(w, who, **a):
    return V.do(Here(w, who), Mind(w, who), a)


# ---------------------------------------------------------------------- u9: the core prompt
def test_core_words_render_twelve_lines_with_no_horizon_season_or_food_figure():
    lines = CORE.core_lines(EEL)
    assert len(lines) == 12
    text = CORE.core_text(EEL) + "\n" + CORE.GRAMMAR
    for word in (" today", "tomorrow", "spring", "summer", "autumn", " meal", "0.46", "a store keeps"):   # line 2 says "fewer in winter" (u9 §1.2)
        assert word not in text.lower(), word
    assert "Any units you do not use are wasted." in text                      # kept until fatigue (B40)
    assert "In the evening" in lines[0]
    off = CORE.core_lines({**EEL, "evening": False, "children": {"on": False}, "view": "classic"})
    assert "In the evening" not in off[0] and off[4] == CORE.CHILDREN_OFF and "as you last saw it" not in off[9]


def test_the_old_prompt_is_kept_as_a_setting_and_the_core_replaces_it(eel):
    w_old = world(OLD)
    sp_old = PR.system_prompt(Here(w_old, "Peter"), Mind(w_old, "Peter"))
    sp = PR.system_prompt(Here(eel, "Peter"), Mind(eel, "Peter"))
    assert "How life works here:" in sp_old and "What you can do (each action is a verb" in sp_old
    assert "How life goes:" in sp and "How life works here" not in sp and "Today you could" not in sp + sp_old
    assert "What you can do. Name the craft or the act" in sp and "By trade" not in sp
    assert "You live by fishing, and you are best at the weir and its nets, and you keep the weir on the Isel." in sp
    turn = VW.turn(Here(eel, "Peter"), Mind(eel, "Peter"), opening=True)
    assert turn.endswith(CORE.CLOSING) and VW.turn(Here(w_old, "Peter"), Mind(w_old, "Peter"), opening=True).endswith(CORE.OLD_CLOSING)
    s = PR.schema_for(Here(eel, "Peter"), Mind(eel, "Peter"))
    assert "enum" not in s["properties"]["actions"]["items"]["properties"]["do"] and "look_up" not in s["properties"]


def test_reply_examples_are_each_persons_own_craft(eel):
    ex = {n: SH.example(Here(eel, n), Mind(eel, n)) for n in ("Peter", "Oliver", "Gunnild")}
    assert "wicker traps" in ex["Peter"] and "the Isel" in ex["Peter"]
    assert ex["Oliver"] != ex["Peter"]
    sp = PR.system_prompt(Here(eel, "Oliver"), Mind(eel, "Oliver"))
    assert '"<n> <good>"' in sp and '"2 bread"' not in sp


def test_the_shapes_resolve_a_craft_or_an_act_to_its_handler(eel):
    here, mind = Here(eel, "Peter"), Mind(eel, "Peter")
    assert SH.normalize(here, mind, {"do": "wicker traps", "at": "the Isel"}) == {"do": "gather", "what": "trap in water", "at": "the Isel"}
    assert SH.normalize(here, mind, {"do": "make", "what": "smoke fish"})["do"] == "make"
    assert SH.normalize(here, mind, {"do": "go", "to": "Oakhurst"})["do"] == "travel"
    assert SH.normalize(here, mind, {"do": "change", "what": "door", "to": "barred"}) == {"do": "set", "thing": "door", "to": "barred"}
    assert SH.normalize(here, mind, {"do": "agree", "what": "teach", "to": "Nigel"})["do"] == "teach"
    assert SH.normalize(here, mind, {"do": "lift", "thing": "T1"})["do"] == "tend"
    assert SH.normalize(here, mind, {"do": "gather", "what": "firewood"}) == {"do": "gather", "what": "firewood"}   # old verbs read
    assert SH.normalize(here, mind, {"do": "go eeling"})["what"] == "trap in water"   # a shape word first, the rest a craft (W-102)
    with pytest.raises(Refused) as e:
        SH.normalize(here, mind, {"do": "eel dancing"})
    assert "You know no craft" not in str(e.value) and "Your crafts:" in str(e.value)


def test_a_set_technique_named_alone_sets_from_the_hands_then_tends(eel):
    w = world(EEL, calendar={"season": "autumn", "day": 1, "season_days": 8})
    first = do(w, "Peter", **{"do": "wicker traps", "at": "the Isel"})
    assert first.startswith("You set") and "wicker trap" in first
    again = do(w, "Peter", **{"do": "wicker traps", "at": "the Isel"})
    assert again.startswith("You tended")
    assert do(w, "Gunnild", **{"do": "eel spearing"}).startswith("Refused")


def test_units_left_are_rest_said_next_morning_with_no_push(eel):
    w = world(EEL)
    m = Mind(w, "Nichola")
    m.store["days"].append({"day": 0, "did": ["You rested 3 units."], "heard": [], "said": []})
    assert CORE.rest_line(m) == "You rested 3 units yesterday."
    m.store["days"][-1]["did"] = ["You tended your wicker traps."]
    assert CORE.rest_line(m) == ""


# ---------------------------------------------------------------------- u9: learning as one record (D2-307, D2-326)
def _rec(w, who, tech, **r):
    w.s["know"].setdefault(who, {})[tech] = {"level": "rough", "skill": LR.curve_range(tech)[0], "seen": 0, "source": "", "since": 0, **r}
    return w.s["know"][who][tech]


def test_learning_scales_with_the_lifespan_and_fades_on_the_life_clock():
    w64 = world(EEL)
    w32 = world(EEL, lifespan=32)
    assert LR.scale(64) == 1.0 and LR.scale(32) == 2.0 and LR.scale(200) == pytest.approx(0.32)
    for w in (w64, w32):
        _rec(w, "Gunnild", "wicker trap")
        LR.tried(Here(w, "Gunnild"), Mind(w, "Gunnild"), "wicker trap", True, units=2)
    a, b = w64.s["know"]["Gunnild"]["wicker trap"], w32.s["know"]["Gunnild"]["wicker trap"]
    assert b["score"] == pytest.approx(2 * a["score"]) and b["practice"] == pytest.approx(2 * a["practice"])
    assert LR.fade_params(w64)[0] == pytest.approx(16.0) and LR.fade_params(w32)[0] == pytest.approx(8.0)


def test_practice_alone_reaches_known_more_slowly_than_with_teaching():
    def tries_to_known(taught):
        w = world(EEL)
        r = _rec(w, "Gunnild", "wicker trap", level="capable", taught=1 if taught else 0)
        for k in range(1, 60):
            LR.tried(Here(w, "Gunnild"), Mind(w, "Gunnild"), "wicker trap", True, units=1)
            if w.s["know"]["Gunnild"]["wicker trap"]["level"] == "known":
                return k
        return None
    alone, taught = tries_to_known(False), tries_to_known(True)
    assert alone is not None and taught is not None and alone == int(LR.ALONE * taught)


def test_a_lesson_session_lifts_by_class_and_never_past_the_teachers_peak():
    w = world(EEL)
    w.s["know"]["Gunnild"].pop("wicker trap", None)
    r = LR.taught(w, "Peter", "Gunnild", "wicker trap")                       # practised: capable at once
    assert r["after"] == "capable"
    peak = float(w.s["know"]["Peter"]["wicker trap"]["skill"])
    for _ in range(12):
        LR.taught(w, "Peter", "Gunnild", "wicker trap")
    assert w.s["know"]["Gunnild"]["wicker trap"]["skill"] <= peak + 1e-9
    w.s["know"]["Nichola"].pop("weir", None)
    assert LR.taught(w, "Peter", "Nichola", "weir")["after"] == "rough"       # skilled: rough, then capable at the second
    assert LR.taught(w, "Peter", "Nichola", "weir")["after"] == "capable"


def test_old_worlds_keep_the_old_learning():
    w = world(HIGH)
    assert not LR.on(w) and LR.try_row(w, "wicker trap", "rough") == {"inputs": 1.7, "chance": 0.5}


# ---------------------------------------------------------------------- u9: the watch act (D2-320)
def test_the_watch_act_over_a_place_a_herd_or_a_building_by_day_or_night(eel):
    w = world(EEL)
    out = do(w, "Hamon", **{"do": "guard", "at": "Eelmouth Field"})
    assert "sit up tonight" in out and w.s["wild"]["watch"]["Eelmouth_9"]["scare"] == "watch"
    assert "Hamon" in w.s["today"]["night_watch"]
    day = {"do": "guard", "at": "the Isel", "when": "day", "units": 3}
    assert V.cost(Here(w, "Gunnild"), day) == 3
    assert "by day" in do(w, "Gunnild", **day) and w.s["today"]["day_watch"]["Gunnild"]["parcel"] == "Eelmouth_8"
    assert "the Isel" and "Eelmouth_8" in w.s["today"]["worked"]["Gunnild"]
    assert "tonight over" in do(w, "Oliver", **{"do": "guard", "at": "Brook House"})


# ---------------------------------------------------------------------- u8: the river
def test_bands_by_the_stations_year():
    assert [RV.band(n, 100.0) for n in (1, 5, 12, 25)] == ["trickle", "running", "thick", "glut"]
    assert RV.band(0.5, 100.0) == "none"


def test_the_river_record_is_written_each_night_and_its_flow_is_the_nights(eel):
    w = world(EEL, calendar={"season": "autumn", "day": 1, "season_days": 8})
    want = RV.flow_today(w, "Eelmouth")
    from cybertron2.engine import night as N
    N.night(w)
    rec = RV.river_now(w, "Eelmouth")
    assert rec and rec["flow"] == want and rec["day"] == 0
    assert set(rec) >= {"flow", "flow_was", "passed", "band", "best", "taken", "turned", "ice", "first", "last"}


def _dawn_fact(w, e):
    here = Here(w, "Peter")
    about = list(e.get("about") or [])
    return {"concerns": [], "about": about or ["sky"], "tags": e["tags"], "salience": e["salience"], "sense": e.get("sense", "sight"),
            "actor": None, "at": PC._event_at(here, e, about)}


def test_dawn_rows_reach_the_houses_by_the_rule_and_only_those_who_read_them():
    w = world(EEL, calendar={"season": "autumn", "day": 1, "season_days": 8})
    w.s["day"] = 0
    w.s["events"] = []
    for key, spot in (("roar", "water"), ("eel_night_set", "place")):
        r = RV.DAWN[key]
        about = ["sky"] if spot == "place" else ["parcel:Eelmouth_8"]
        e = w.event("Eelmouth", "river", r["text"].format(water="the Isel", fen="Eelmouth Fen", share=""), about=about, salience=1.0,
                    tags=["fishing"], sense=r["sense"], own=r["own"], dawn=True, **RV._knows(r["read"] if isinstance(r["read"], str) else "all"))
        p = PC.chance_of(w, "Gunnild", _dawn_fact(w, e), mind=Mind(w, "Gunnild"))
        if key == "roar":
            assert 0.15 <= p <= 0.35                                            # u8 §6: the roar from the Street about 0.25
        else:
            assert 0.2 <= p <= 0.4                                              # everyone at the place, 0.3
    assert "expert:fish" in PC.practised(Mind(w, "Peter")) and "fish" in PC.practised(Mind(w, "Gunnild"))
    assert "fish" not in PC.practised(Mind(w, "Petronel"))                     # a broad salter's youth: no water craft past basic
    PC.dawn(w)
    t = {n: w.s["mind"][n]["today"]["dawn"] for n in ("Petronel", "Peter")}
    assert not any("eel night" in x for x in t["Petronel"])


def test_the_carried_catch_reaches_the_others_and_never_the_carrier():
    w = world(EEL, calendar={"season": "autumn", "day": 1, "season_days": 8})
    w.s["containers"][w.hands("Hamon")]["goods"]["fish"] = 6.0
    w.s["today"]["worked"]["Hamon"] = ["Eelmouth_8"]
    got = []
    RV.carried(Here(w, "Peter"), lambda about, text, *a, **k: got.append((text, k)))
    assert len(got) == 1 and "Hamon came up from the Isel with a good load of fresh fish" in got[0][0]
    assert "Hamon" not in got[0][1]["only"] and got[0][1]["spot"]["parcel"] == "Eelmouth_0"
    w.s["containers"][w.hands("Hamon")]["goods"]["fish"] = 3.0
    got.clear()
    RV.carried(Here(w, "Peter"), lambda about, text, *a, **k: got.append(text))
    assert not got
    w.s["containers"][w.hands("Hamon")]["goods"]["fish"] = 12.0
    w.s["today"]["worked"]["Hamon"] = ["Eelmouth_0"]                           # fish from the store: no work at the water
    RV.carried(Here(w, "Peter"), lambda about, text, *a, **k: got.append(text))
    assert not got


def test_no_sign_directs_an_act():
    from cybertron2.wild.kinds import RUN_SIGNS
    texts = [r["text"] for r in RV.DAY] + [r["text"] for r in RV.DAWN.values()] + [x for xs in RV.CARRIED.values() for x in xs if x]
    for rows in RUN_SIGNS.values():
        if isinstance(rows, list):
            texts += [r["text"] for r in rows]
    for t in texts:
        for bad in ("set the", "net them", "draw the", "bring it in", "must be", "lift the", "take them"):
            assert bad not in t, (bad, t)


# ---------------------------------------------------------------------- u11: livelihoods, the fill, the founders' lines, the gate
def test_the_fill_places_bands_keepers_gear_and_the_cast_by_d2_270_and_d2_330():
    a = EEL["agents"]
    assert [a[n]["band"] for n in ("Peter", "Nichola", "Hamon", "Gunnild", "Oliver", "Katherine")] == \
        ["expert", "capable", "expert", "broad", "expert", "broad"]
    assert a["Peter"]["specialism"] == "weir_and_nets" and a["Hamon"]["specialism"] == "keeping" and a["Oliver"]["specialism"] == "the_pan"
    b = EEL["buildings"]
    assert b["brook_salthouse"]["household"] == "Brook" and b["brook_salthouse"]["keeper"] == "Oliver"            # C1
    assert b["marsh_weir"]["keeper"] == "Peter" and b["marsh_smokehouse"]["keeper"] == "Nichola"
    assert {n: a[n]["holdings"].get("wicker trap", 0) for n in ("Peter", "Nichola", "Hamon", "Katherine", "Gunnild")} == \
        {"Peter": 6, "Nichola": 6, "Hamon": 6, "Katherine": 6, "Gunnild": 0}                                     # C5
    assert a["Peter"]["holdings"].get("gill net") == 1 and (a["Peter"]["knows"]["gill nets"]["level"]) == "known"   # M6
    assert [a[n]["model"] for n in ("Peter", "Oliver", "Hamon")] == [LV.CAST["head"]] * 3
    assert a["Nichola"]["model"] == LV.CAST["middle"] and a["Gunnild"]["model"] == LV.CAST["rest"]
    assert any(p["cover"] == "rock" for p in EEL["nodes"]["Eelmouth"]["parcels"].values())                       # C2
    assert a["Oliver"]["livelihood"].startswith("You live by boiling salt at the spring, and by fishing beside it")


def test_every_founders_lines_fit_twenty_and_forty_words_and_state_their_figures():
    for n, a in EEL["agents"].items():
        k = a.get("kept") or []
        assert len(k) <= FD.CAP_LINES, n
        assert all(len(x["text"].split()) <= FD.LINE_WORDS for x in k), n
    peter = [x["text"] for x in EEL["agents"]["Peter"]["kept"]]
    assert any(f"holds no more than about {WATER_WORKS['trap']['hold']:g} kilos" in t for t in peter)
    hh1 = next(t for t in peter if t.startswith("Our store at Marsh House"))
    from cybertron2.engine.data import ITEMS
    st = EEL["buildings"]["marsh_house"]["stock"]
    food = sum(float(q) * ITEMS[i]["food"] for i, q in st.items() if i in ITEMS)
    need = 1 + 1 + 0.8 + 0.7 + 0.5                                             # two adults, a youth (C6), a child (low dial), an infant
    assert f"about {round(food / need)} nights' food" in hh1
    oliver = [x["text"] for x in EEL["agents"]["Oliver"]["kept"]]
    assert any("In the evening, under one roof, we look again at the household's rules" in t for t in oliver)   # D2-319
    assert all(x["source"] in ("family lore", "a holding") for x in EEL["agents"]["Peter"]["kept"])
    assert not any(a.get("kept") for a in OLD["agents"].values())                                                  # D2-331


def test_the_cap_drops_in_order_and_keeps_the_protected_lines():
    w = copy.deepcopy(EEL)
    rep = LV.fill(copy.deepcopy(w), lines=False)
    lines = {f"NB-x{i}": "a neighbour line" for i in range(5)}
    lines.update({k: "a line" for k in ("BS1", "BS2", "BS3", "BS4", "BS5", "BS6", "BS7", "BS8", "BS9", "PE1", "PE2", "HH1", "HH3",
                                         "HH5", "HH6", "HH7", "HH8", "HH9", "FI12", "HL")})
    ids, steps, over = FD.cap(w, "Peter", lines)
    assert len(ids) <= 20 and not over
    assert {"PE1", "HL", "FI12", "HH1", "HH3", "HH7", "HH9"} <= set(ids)
    assert steps[0] == "neighbours beyond one"


def test_the_gate_check_passes_eelmouth_and_refuses_todays_runs_world():
    from cybertron2.landgen import gate_check as GC
    eel = GC.people_checks(EEL)
    assert not [x for x in eel if x["level"] == "refuse"]
    assert {x["check"] for x in eel if x["level"] == "warn"} == {"P7", "P10", "P11", "P18"}
    high = GC.people_checks(HIGH)
    assert {x["check"] for x in high if x["level"] == "refuse"} >= {"P3"}
    weak = copy.deepcopy(EEL)
    for a in weak["agents"].values():
        if a.get("model"):
            a["model"] = LV.CAST["rest"]
    assert "P17" in {x["check"] for x in GC.people_checks(weak) if x["level"] == "refuse"}
    bad = copy.deepcopy(EEL)
    bad["agents"]["Nigel"]["apprentice"] = {"to": "Peter", "specialism": "keeping"}
    assert "P8" in {x["check"] for x in GC.people_checks(bad) if x["level"] == "refuse"}


def test_a_youth_eats_eight_tenths(eel):
    from cybertron2.engine import life as LF
    assert LF.ration_factor(eel, "Nigel") == (0.8, 0.0)
