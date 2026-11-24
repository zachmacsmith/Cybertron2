"""W-109: the interface from one registry (D2-350, D2-351, D2-352, D2-353; D5-2 "interface is not world"). Interface tests
(D2-298): every act (verbs.VERB) and way (the modifier rows) reaches the rendered prompt of a fixture person who can use it, with
every argument and option; the loader check refuses an undescribed act, craft or way; what each familiarity shows; an argument an
act is refused without is shown as required; who is shown what, from the registry's conditions. Fixtures: session bench's World 0b
(Osric, a farmer head and a parent; Orabel; Jocelin, a fisher head who knows the weir; Alice, who dibbles; Hawise, a youth; Alice
again after leaving her household, a lone grown person) and Eelmouth (Peter, Nigel a youth, Nichola, Gunnild, Oliver)."""
import copy
import os
import re

import pytest

from cybertron2.engine import iface as IF, knowledge as KN, perceive as PC, prompt as PR, run as R, shapes as SH, verbs as V
from cybertron2.engine.data import MODIFIERS, TECHNIQUES
from cybertron2.engine.here import Here, Mind
from cybertron2.engine.world import World, load_spec

W0B = next(p for p in ("cybertron2/specs/mono/world0b_sonnet55.yaml", "tests/fixtures/world0b_sonnet55.yaml") if os.path.exists(p))
EEL = "cybertron2/specs/nutrition/eelmouth.yaml"
W0B_PEOPLE = ("Osric", "Orabel", "Jocelin", "Alice", "Hawise")
EEL_PEOPLE = ("Peter", "Nigel", "Nichola", "Gunnild", "Oliver")


def build(path):
    w = World(load_spec(path))
    w.s["day"] = 0
    w.s["events"] = []
    w.s["today"] = R.blank_today()
    R.dawn(w)
    PC.dawn(w)
    return w


@pytest.fixture(scope="module")
def w0b():
    return build(W0B)


@pytest.fixture(scope="module")
def eel():
    return build(EEL)


@pytest.fixture(scope="module")
def lone():
    w = build(W0B)
    r = V.do(Here(w, "Alice"), Mind(w, "Alice"), {"do": "leave_household"})
    assert not r.startswith("Refused"), r
    assert Here(w, "Alice").household() is None
    return w


@pytest.fixture(scope="module")
def cast(w0b, eel, lone):
    """[(label, world, name, system prompt)] for every fixture person."""
    out = [(f"w0b:{n}", w0b, n, PR.system_prompt(Here(w0b, n), Mind(w0b, n))) for n in W0B_PEOPLE]
    out += [(f"eel:{n}", eel, n, PR.system_prompt(Here(eel, n), Mind(eel, n))) for n in EEL_PEOPLE]
    out.append(("lone:Alice", lone, "Alice", PR.system_prompt(Here(lone, "Alice"), Mind(lone, "Alice"))))
    return out


def section(sp) -> str:
    return sp[sp.index("What you can do."):sp.index("Reply with JSON")]


def line_of(sp, name) -> str:
    return next((x for x in section(sp).splitlines() if x.startswith(f"- {name} {{") or x.startswith(f"- {name}:")), "")


def block(sp, shape) -> str:
    """The lines under a shape's grammar line, to its next."""
    out, on = [], False
    for x in section(sp).splitlines():
        if not x.startswith((" ", "-")):
            on = x.startswith(f"{shape} {{")
            continue
        if on:
            out.append(x)
    return "\n".join(out)


# ---------------------------------------------------------------------- the loader check
def test_the_loader_check_passes_and_refuses_an_undescribed_act_craft_or_way():
    IF.check()
    verbs = copy.deepcopy(V.VERB)
    verbs["watch"]["iface"][0].pop("does")
    with pytest.raises(IF.RegistryError, match="watch"):
        IF.check(verbs)
    verbs = copy.deepcopy(V.VERB)
    verbs["write"]["iface"][0].pop("cost")                                  # its cost is no number: the face must say it
    with pytest.raises(IF.RegistryError, match="write"):
        IF.check(verbs)
    verbs = copy.deepcopy(V.VERB)
    verbs["meet"].pop("iface")
    with pytest.raises(IF.RegistryError, match="meet"):
        IF.check(verbs)
    verbs = copy.deepcopy(V.VERB)
    verbs["grant"]["iface"][0]["args"][0].pop("req")
    with pytest.raises(IF.RegistryError, match="grant"):
        IF.check(verbs)
    techs = copy.deepcopy(TECHNIQUES)
    techs["snare"].pop("does")                                              # a set craft must say what doing it does
    with pytest.raises(IF.RegistryError, match="snare"):
        IF.check(None, techs)
    techs = copy.deepcopy(TECHNIQUES)
    techs["hunt with"].pop("takes")                                         # a way taking any value says what it takes
    with pytest.raises(IF.RegistryError, match="hunt with"):
        IF.check(None, techs)
    shapes = copy.deepcopy(SH.SHAPES)
    shapes["force"].pop("line")
    with pytest.raises(IF.RegistryError, match="force"):
        IF.check(None, None, shapes)


# ---------------------------------------------------------------------- coverage
def test_every_handler_with_every_argument_and_option_reaches_someone_who_can_use_it(cast):
    allp = "\n".join(sp for *_, sp in cast)
    for v, d in V.VERB.items():
        for f in d["iface"]:
            if f.get("retired"):
                assert 'Standing rules are written in "rules"' in allp, v
                continue
            if f.get("via"):
                assert f"\n{f['shape']} {SH.SHAPES[f['shape']]['args']}: " in allp, (v, f["shape"])
                continue
            who = [(lab, w, n, sp) for lab, w, n, sp in cast if IF.allowed(Here(w, n), f["who"])]
            assert who, f"nobody in the fixtures may {v} ({f['who']})"
            lab, w, n, sp = who[0]
            line = IF.act_line(Here(w, n), Mind(w, n), v, f)
            assert line in sp, (v, lab)
            assert f'"do": "{f["word"]}"' in line
            for a in f["args"]:
                if a.get("who") and not IF.allowed(Here(w, n), a["who"]):
                    continue
                assert f'"{a["key"]}"' in line, (v, a["key"])
                for o in a["opts"]:
                    assert o in line, (v, a["key"], o)
        for key in re.findall(r'"([a-z ]+)"\??:', d["args"]):                  # the old registry's arguments, every one
            if v == "rule":
                continue
            assert f'"{key}"' in allp, (v, key)


def test_every_way_and_its_values_reach_someone_who_knows_it(cast):
    for m in sorted(MODIFIERS):
        d = TECHNIQUES[m]
        if d.get("shown_in"):
            continue
        knowers = [sp for lab, w, n, sp in cast if KN.level(Mind(w, n), m) in ("rough", "capable", "known")
                   or d.get("untaught") == "tryable"]
        assert knowers, m
        vals = [d["value"]] if d["value"] != "*" else (d.get("values") or [d["takes"]])
        hit = [sp for sp in knowers if f'"{d["key"]}"?: ' in section(sp) and all(x in section(sp) for x in vals)]
        assert hit, (m, d["key"], vals)


def test_every_craft_a_fixture_person_can_do_is_on_a_line_of_its_own(cast):
    for lab, w, n, sp in cast:
        here, mind = Here(w, n), Mind(w, n)
        for sh, xs in IF.familiar(here, mind).items():
            for t, lvl, uni in xs:
                if lvl == "aware":
                    continue
                assert line_of(sp, IF.craft_name(t)), (lab, t)


# ---------------------------------------------------------------------- familiarity (D2-352)
def test_an_aware_craft_shows_its_name_only_a_rough_one_its_minimum_interface_a_known_one_its_full_line(w0b, eel):
    sp = PR.system_prompt(Here(w0b, "Osric"), Mind(w0b, "Osric"))
    assert KN.level(Mind(w0b, "Osric"), "mine") == "aware"
    assert not line_of(sp, "mine") and "known of, not how" in sp and "mine (you have seen the Brooks at it all your life)" in sp
    assert KN.level(Mind(w0b, "Osric"), "milk") == "rough"
    milk = line_of(sp, "milk")
    assert "a rough idea" in milk and "you could try" in milk and " unit" not in milk           # no cost at rough
    plough = line_of(sp, "plough")
    assert "known, master" in plough and "1 unit" in plough and "on field" in plough            # the full line
    fell = line_of(sp, "fell")                                                                   # everyone's: in full
    assert "bare hands x0.25" in fell and "a copper tool x2" in fell and "2 units" in fell
    sp_n = PR.system_prompt(Here(eel, "Nigel"), Mind(eel, "Nigel"))
    assert KN.level(Mind(eel, "Nigel"), "weir") == "rough"
    weir = line_of(sp_n, "weir")
    assert '"with": one or more people here' in weir and "a rough idea" in weir                 # how it is said, what it must have
    rough_ways = [x for x in section(sp_n).splitlines() if x.startswith("  ways, with") and "weir" in x]
    assert not rough_ways                                                                        # the ways only from capable up


def test_only_what_one_is_familiar_with_is_shown(w0b):
    here, mind = Here(w0b, "Osric"), Mind(w0b, "Osric")
    sp = PR.system_prompt(here, mind)
    for t, d in TECHNIQUES.items():
        if SH.shape_of(t) is None or KN.level(mind, t) is not None or SH._universal(t, "adult"):
            continue
        known_of = " ".join(x.split("taught): ", 1)[1] for x in section(sp).splitlines() if "known of, not how" in x)
        mine = [x for x in block(sp, SH.shape_of(t)).splitlines() if x.startswith((f"- {IF.craft_name(t)} {{", f"- {IF.craft_name(t)}:"))]
        assert not mine and not re.search(rf"(^|; ){re.escape(IF.craft_name(t))} \(", known_of), t


# ---------------------------------------------------------------------- an argument refused without is shown as required
def test_an_act_refused_for_a_missing_argument_shows_it_as_required(w0b):
    here, mind = Here(w0b, "Osric"), Mind(w0b, "Osric")
    sp = PR.system_prompt(here, mind)
    tried = [V.do(Here(w0b, "Osric"), Mind(w0b, "Osric"), {"do": "sow", "at": p["name"]}) for p in here.parcels().values()
             if p["cover"] in TECHNIQUES["sow"]["at"]["covers"]]
    assert any(r.startswith("Refused") and "say which seed" in r for r in tried), tried
    assert '- sow {"item": the seed to sow' in sp                            # required: no "?"
    for case, needs in (({"do": "meet"}, '"at"'), ({"do": "write"}, '"at"'), ({"do": "erase", "at": "Field House"}, '"line"'),
                        ({"do": "travel"}, '"to"'), ({"do": "name"}, '"heir"')):
        r = V.do(Here(w0b, "Osric"), Mind(w0b, "Osric"), case)
        assert r.startswith("Refused"), (case, r)
        word = next(f["word"] for f in V.VERB[case["do"]]["iface"] if f.get("word"))
        line = next(x for x in section(sp).splitlines() if x.startswith(f'- {word} {{"do": "{word}"'))
        assert needs in line, (case, line)
    for t, d in TECHNIQUES.items():                                           # every required argument shown without "?"
        for a in d.get("args") or []:
            ln = line_of(sp, IF.craft_name(t))
            if a["req"] and ln:
                assert f'"{a["key"]}":' in ln, (t, a["key"])
    for v, d in V.VERB.items():
        for f in d["iface"]:
            if f.get("word") and IF.allowed(here, f["who"]):
                ln = IF.act_line(here, mind, v, f)
                for a in f["args"]:
                    if a["req"]:
                        assert f'"{a["key"]}":' in ln, (v, a["key"])


# ---------------------------------------------------------------------- who is shown what (the registry's conditions)
def test_who_sees_what_by_stage_office_household_and_world(cast, w0b):
    sp = {lab: s for lab, *_, s in cast}
    acts = lambda lab: {x.split(" {")[0][2:] for x in section(sp[lab]).splitlines() if x.startswith("- ") and ' {"do": ' in x}  # noqa: E731
    osric, orabel, hawise, lone_ = acts("w0b:Osric"), acts("w0b:Orabel"), acts("w0b:Hawise"), acts("lone:Alice")
    assert {"order", "admit"} <= osric and not {"order", "admit"} & orabel            # the head's acts for a head
    assert {"try", "partner", "attack", "found", "host"} <= orabel
    assert not {"try", "partner", "attack", "found", "host", "part"} & hawise and "guard" in hawise   # a youth's list by stage
    assert "found" in lone_ and "join" in lone_ and "leave household" not in lone_                   # no household
    assert '"heir"' not in section(sp["lone:Alice"]) and '"heir"' in section(sp["w0b:Orabel"])
    assert line_of(sp["w0b:Osric"], "care") and line_of(sp["w0b:Hawise"], "care")      # a world with children
    for lab in sp:
        assert "\n- tend " in section(sp[lab]) or not IF.allowed(Here(*next((w, n) for l2, w, n, _ in cast if l2 == lab)), ["sets"])
    eel_has_herds = V.when_holds(Here(next(w for l2, w, *_ in cast if l2 == "eel:Peter"), "Peter"), "herds")
    assert ("- drive {" in section(sp["eel:Peter"])) == eel_has_herds
    assert "- drive {" in section(sp["w0b:Osric"])                                     # cattle at Middleham


def test_the_section_lists_each_act_on_its_own_line_with_look_up_back_and_no_options_list(cast):
    for lab, w, n, sp in cast:
        s = section(sp)
        for word in ("sleep", "fire", "meet", "come", "go"):                           # go's acts each on its own line
            assert f'\n- {word} {{"do": "{word}"' in s, (lab, word)
        assert "Today you could" not in sp and "you could do today" not in sp            # D2-286
        assert '"look_up": [crafts]' in sp
        assert "a standing rule (rule)" not in s and "- rule " not in s                  # rules only in "rules" (D2-339)
        assert "known of, not how" not in s or s.index("known of, not how") > s.index("\n- ")


def test_the_build_shapes_upgrade_face_is_read_from_the_registry(w0b):
    here, mind = Here(w0b, "Osric"), Mind(w0b, "Osric")
    a = SH.normalize(here, mind, {"do": "build", "what": "upgrade", "at": "Field House", "to": "timber"})
    assert a == {"do": "build", "what": "upgrade", "at": "Field House", "to": "timber"}
    assert '- upgrade {"do": "build", "what": upgrade, "at": a building here' in PR.system_prompt(here, mind)


# ---------------------------------------------------------------------- the wave's regressions (wave_regressions.md 2, 3, 10, 11)
def test_the_gear_line_reaches_the_beliefs_view_from_the_one_source():
    from cybertron2.engine import gear as GE, view as VW
    eel = build(EEL)
    c = eel.s["containers"][eel.hands("Peter")]
    for _ in range(400):                                                       # wear pieces down to broken (wave_regressions probe)
        GE.wear(eel, c, "wicker trap", 1.0)
        if "broken" in " ".join(Here(eel, "Peter").gear_words()):
            break
    here, mind = Here(eel, "Peter"), Mind(eel, "Peter")
    line = here.gear_line()
    assert line.startswith("Of your gear: ") and "wicker trap" in line, line
    assert line in VW.turn(here, mind, opening=True)
    assert line in VW.turn(Here(eel, "Peter"), Mind(eel, "Peter"), opening=False)
    assert line in PR.turn_prompt(Here(eel, "Peter"), Mind(eel, "Peter"), True)


def test_craft_lines_keep_their_working_hint_and_where_they_came_from():
    milk = KN.craft_line("milk", "rough", {"source": "from your upbringing"})
    assert milk.startswith("milking (a cow in milk) (") and "from your upbringing" in milk
    assert KN.craft_line("drive", "known", {}).startswith(KN.doing("drive"))
    assert "Brook" in KN.craft_line("stalk", "capable", {"source": "taught by Hamon Brook"})
    old = build("cybertron2/specs/nutrition/eelmouth_old.yaml")
    sp = PR.system_prompt(Here(old, "Peter"), Mind(old, "Peter"))
    assert "(from your upbringing; a rough idea" in sp


def test_waiting_today_is_shown_each_morning_in_a_beliefs_world(eel, monkeypatch):
    from cybertron2.engine import view as VW
    from cybertron2.engine.here import Here as H
    monkeypatch.setattr(H, "book_waiting_lines", lambda self: ["Waiting today: tend the Smokehouse (rule 1)."])
    VW.turn(Here(eel, "Nichola"), Mind(eel, "Nichola"), opening=True)
    m = eel.s["mind"]["Nichola"]
    m["view"] = m.pop("view_next")                                             # the morning's snapshot made current (perceive.py)
    later = VW.turn(Here(eel, "Nichola"), Mind(eel, "Nichola"), opening=False)
    assert "Waiting today: tend the Smokehouse (rule 1)." in later


def test_the_old_prompt_shows_one_grammar_for_rules():
    old = build("cybertron2/specs/nutrition/eelmouth_old.yaml")
    sp = PR.system_prompt(Here(old, "Peter"), Mind(old, "Peter"))
    assert '"rules": [...]' in sp or "Standing rules go in" in sp
    assert "\n- rule {" not in sp and "hold back | first | eat | move | tend | chore | drop" not in sp


# ---------------------------------------------------------------------- a technique's fields apart (D2-356)
def test_a_techniques_name_needs_hints_and_world_are_fields_rendered_together(w0b, eel):
    for t, d in TECHNIQUES.items():
        assert "(" not in d["label"], t                                       # the name only
    techs = copy.deepcopy(TECHNIQUES)
    techs["milk"]["label"] = "milking (a cow in milk)"
    with pytest.raises(IF.RegistryError, match="milk"):
        IF.check(None, techs)
    assert KN.label("milk") == "milking" and KN.titled("milk") == "milking (a cow in milk)"
    assert KN.titled("forage") == "foraging (greens, roots, berries, nuts)" and KN.titled("forage", world=False) == "foraging"
    assert KN.named("den work", "aware") == "digging out a den or trapping at a lodge"             # by level, never the world
    assert KN.named("milk", "rough") == "milking (a cow in milk)" and KN.named("den work", "rough") == KN.label("den work")
    assert KN.named("den work", "known").endswith("(spades and a dog help)")
    sp = PR.system_prompt(Here(w0b, "Osric"), Mind(w0b, "Osric"))
    milk = line_of(sp, "milk")                                                # rough: what it needs, no hint
    assert "needs a cow in milk" in milk
    assert "spades and a dog help" in line_of(sp, "den work")                 # known: its hint
    for t, d in TECHNIQUES.items():                                           # the world's words never in the interface (D5-2)
        if d.get("world"):
            assert d["world"] not in section(sp), t
    old = build("cybertron2/specs/nutrition/eelmouth_old.yaml")               # the old prompt keeps them, from the fields
    sp_old = PR.system_prompt(Here(old, "Peter"), Mind(old, "Peter"))
    assert "making a gill net (netting twine, with sinkers) (known" in sp_old
    from cybertron2.engine import knowledge as K2
    card = K2.card(Here(w0b, "Osric"), Mind(w0b, "Osric"), "mine")            # a card in the interface: aware, the name only
    assert card.startswith(f"{KN.label('mine')}: you know of it")
    from cybertron2.engine import prompt as P2
    assert "smoke racks (hurdles over a smouldering fire)" in P2._craft_note("smoke fish")      # a fitting's name and what it is
    assert P2.craft_note_words("cairn").startswith("3 units of work")


# ---------------------------------------------------------------------- World 0b's refusals (session bench, L-189)
def _did(w, name, act):
    return V.do(Here(w, name), Mind(w, name), dict(act))


def test_sleep_with_no_building_named_is_sleep_at_home_and_home_is_ones_house():
    w = build(W0B)
    home = Here(w, "Osric").buildings()[Here(w, "Osric").homes_here()[0]]["name"]
    for act in ({"do": "sleep"}, {"do": "go", "what": "sleep"}, {"do": "sleep", "at": "home"}, {"do": "sleep", "at": "my house"}):
        r = _did(w, "Osric", act)
        assert r.startswith(f"You mean to sleep at {home}"), (act, r)
    assert "None" not in _did(build(W0B), "Alice", {"do": "sleep", "at": None})
    line = IF.act_line(Here(w, "Osric"), Mind(w, "Osric"), "sleep", V.VERB["sleep"]["iface"][0])
    assert '"at"?: a building here (else your home here)' in line


def test_goods_moved_to_my_hands_or_me_go_to_the_hands_never_racks():
    for to in ("my hands", "me", "hands", "inventory", "myself"):
        w = build(W0B)
        here = Here(w, "Osric")
        store = here.buildings()[here.homes_here()[0]]["name"]
        before = here.carried().get("grain", 0.0)
        r = _did(w, "Osric", {"do": "move", "item": "grain", "qty": 1, "from": store, "to": to})
        assert r.startswith("You took 1 grain"), (to, r)
        assert Here(w, "Osric").carried().get("grain", 0.0) == pytest.approx(before + 1)
        assert "racks" not in r and "no building called" not in r


def test_foraged_greens_and_mushrooms_are_stored_as_wild_food():
    w = build(W0B)
    here = Here(w, "Osric")
    for g, q in (("greens", 2.0), ("mushrooms", 1.5)):
        w.apply("create", here.node, dst=here.hands, item=g, qty=q, why="test")
    r = _did(w, "Osric", {"do": "move", "item": "wild food", "to": "store"})
    assert "2 greens" in r and "1.5 mushrooms" in r, r
    assert Here(w, "Osric").carried().get("greens", 0.0) == 0 and Here(w, "Osric").carried().get("mushrooms", 0.0) == 0
    w.apply("create", here.node, dst=here.hands, item="greens", qty=1.0, why="test")
    assert V.item_of("greens") == "greens"                                    # a good of the world is itself, never "wild food"
    assert _did(w, "Osric", {"do": "move", "item": "greens", "to": "store"}).startswith("You put 1 greens")


def test_a_rules_for_my_household_or_the_households_name_is_read():
    from cybertron2.engine import book as BK
    w = build(W0B)
    for f, whose in (("my household", "the household"), ("the Fields", "the household"), ("me", "yours"), ("myself", "yours")):
        r = BK.apply_rules(Here(w, "Osric"), [{"rule": "keep", "goods": "grain", "in": "Field House", "at least": 5, "for": f}])
        assert r and f"({whose})" in r[0], (f, r)


def test_bury_is_the_craft_of_burying_the_dead_and_every_face_names_an_act(w0b):
    a = SH.normalize(Here(w0b, "Osric"), Mind(w0b, "Osric"), {"do": "bury", "at": "the body"})
    assert a["do"] == "work" and a["what"] == "bury"
    for sh, row in SH.SHAPES.items():
        for f, v in (row.get("faces") or {}).items():
            assert v in V.VERB or v in V.ALIASES, (sh, f, v)
    shapes = copy.deepcopy(SH.SHAPES)
    shapes["move"]["faces"]["inter"] = "inter"                                # a face naming no act cannot be built
    with pytest.raises(IF.RegistryError, match="inter"):
        IF.check(None, None, shapes)
    w = build(W0B)                                                            # with goods named, burying is hiding them
    here = Here(w, "Osric")
    w.apply("create", here.node, dst=here.hands, item="mushrooms", qty=1.0, why="test")
    r = _did(w, "Osric", {"do": "bury", "item": "mushrooms", "qty": 1, "at": here.parcels()[next(iter(here.parcels()))]["name"]})
    assert "hidden" in r or "buried" in r or "bury" in r.lower(), r
    assert not r.startswith("Refused"), r
    sp = PR.system_prompt(Here(w0b, "Osric"), Mind(w0b, "Osric"))
    assert line_of(sp, "bury").startswith('- bury {"at": the body}')


def test_say_and_other_reply_fields_put_among_the_actions_are_read_as_those_fields():
    reply = {"actions": [{"do": "say", "to": "everyone", "message": "the barley is in"}, {"do": "gather", "what": "firewood"},
                         {"do": "tell", "to": "Orabel", "text": "come home early"}, {"do": "look up", "what": "mine"},
                         {"do": "drop", "item": "coin", "qty": 1}]}
    out, notes = SH.reply_fields(reply)
    assert out["say"] == [{"to": "everyone", "text": "the barley is in"}]
    assert out["tell"] == [{"to": "Orabel", "text": "come home early"}] and out["look_up"] == ["mine"]
    assert out["actions"] == [{"do": "gather", "what": "firewood"}, {"do": "drop", "item": "coin", "qty": 1}]   # an alias stays
    assert len(notes) == 3 and all('not in "actions"' in x for x in notes)


def test_a_lesson_or_an_act_without_its_fields_is_told_them_from_the_registry(w0b):
    with pytest.raises(Exception) as e:
        SH.normalize(Here(w0b, "Osric"), Mind(w0b, "Osric"), {"do": "agree", "with": "Orabel", "what": "fishing"})
    assert '{"do": "teach", "to": a person here, "what": a craft you know}' in str(e.value)
    assert '{"do": "learn", "from": a person here, "what": the craft}' in str(e.value)
    w = build(W0B)
    assert _did(w, "Osric", {"do": "teach", "to": "Drew"}) == 'Refused: teach: say a craft you know in "what"'
    assert _did(w, "Osric", {"do": "watch"}) == 'Refused: watch: say a person here in "person"'
    assert "None" not in _did(w, "Osric", {"do": "learn", "from": "Orabel"})


def test_live_run_ones_lessons_and_offers_under_agree_are_read(w0b):
    """Replies of live run 1 refused before (the replay, iface_report.md): a lesson written in "agreement" or "name", an offer
    accepted under agree."""
    here, mind = Here(w0b, "Osric"), Mind(w0b, "Osric")
    a = SH.normalize(here, mind, {"do": "agree", "with": "Orabel", "agreement": "learn the plough from Orabel, 2 units"})
    assert (a["do"], a["from"], a["what"]) == ("learn", "Orabel", "plough")
    assert SH.normalize(here, mind, {"do": "agree", "with": "Orabel", "name": "learn milking"})["what"] == "milk"
    assert SH.normalize(here, mind, {"do": "agree", "offer": "O1", "for": "my household"})["do"] == "accept"
