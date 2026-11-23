"""What an agent's code may see (D4-35, spec/core/architecture.md): `Here`, a view of the node the agent stands at with its own body
and hands, and `Mind`, what it knows. The verbs, knowledge views, perception and prompts are given these and nothing else; they have
no reference to the world (a test reads their source).

Here acts only through the chokepoint at its own node: `here.apply(primitive, ...)` is `w.apply(primitive, node, ...)`, so a
primitive that touches anything elsewhere fails as an engine fault.
"""
from __future__ import annotations

from cybertron2.engine.world import CONDITION, STAGES, Refused, show  # noqa: F401  (re-exported for the agent-facing modules)


class Here:
    def __init__(self, w, name, transit=False):
        self._w = w
        from cybertron2.engine import packs as PK
        PK.use(w)                                                               # the world's switched-on packs (D4-103)
        self.name = name
        self.node = w.at(name)
        if self.node is None and not transit:                                  # on the road: only for an urgent call (D2-81)
            raise Refused(f"{name} is on the road")
        self.place = self.node if self.node is not None else w.place_of(("person", name))   # a node, or the road one is on

    # ------------------------------------------------------------------ time and rules
    @property
    def day(self):
        return self._w.d

    @property
    def p(self):
        return self._w.p

    def calendar(self, day=None):
        return self._w.calendar(day)

    # ------------------------------------------------------------------ the weather where one is (D4-111)
    # Every weather query names its place; for one acting, the place is where they are (a node, or the road they are on). A call
    # about somewhere else names it (`at`).
    def cold(self, day=None, at=None):
        return self._w.cold(at or self.place, day)

    def weather(self, day=None, at=None) -> str:
        from cybertron2.engine import environment as EV
        return EV.weather(self._w, at or self.place, day)

    def wet(self, day=None, at=None) -> bool:
        from cybertron2.engine import environment as EV
        return EV.wet(self._w, at or self.place, day)

    def snow_lying(self, day=None, at=None) -> bool:
        from cybertron2.engine import environment as EV
        return EV.snow_lying(self._w, at or self.place, day)

    def since_heavy_rain(self, day=None, at=None):
        from cybertron2.engine import environment as EV
        return EV.since_heavy_rain(self._w, at or self.place, day)

    def weather_values(self, day=None, at=None) -> dict | None:
        """The physical weather here (temp, low, rain, wind, fog, storm) where the scheduler gives it, else None."""
        from cybertron2.engine import environment as EV
        return EV.values(self._w, at or self.place, day)

    def rng(self, *parts):
        return self._w.rng(*parts)

    def year_days(self) -> int:
        return self._w.year_days()

    @property
    def node_name(self):
        return self._w.s["nodes"][self.node]["name"]

    def road_to(self, x):
        """(node id, days, track) for a neighbouring place named x, or an unexplored way described as x, else None."""
        x = str(x or "").strip().lower().removeprefix("the ")
        for other, nm, days, track in self.roads():
            nm = nm.lower()
            if x and (x in (other.lower(), nm, nm.removeprefix("the "), nm.removeprefix("an ")) or (len(x) > 6 and x in nm)):
                return other, days, track
        return None

    def roads(self) -> list:
        """[(node id, name, days, track)] from here; a place one does not know is named by its way (D4-47)."""
        out = []
        from cybertron2.engine import layout as LY
        for rid, r in self._w.s["roads"].items():
            if self.node in (r["a"], r["b"]) and LY.way_known(self._w, self.name, rid, self.node):   # a hidden end: only if known (D2-90)
                other = r["b"] if r["a"] == self.node else r["a"]
                nm = self._w.s["nodes"][other]["name"] if self._w.knows_place(self.name, other) else r.get("way", "an unexplored way")
                out.append((other, nm, r["days"], r.get("track", False)))
        names = [x[1] for x in out]                                             # ways of the same name told apart by where they
        if len(set(names)) < len(names):                                        # lead (38.75: "the open road" three times)
            out = [(o, f"{nm} {self._heading(o)}" if names.count(nm) > 1 else nm, d, t) for o, nm, d, t in out]
            seen = {}
            for i, (o, nm, d, t) in enumerate(out):                             # still the same: numbered
                seen[nm] = seen.get(nm, 0) + 1
                if [x[1] for x in out].count(nm) > 1:
                    out[i] = (o, f"{nm} ({seen[nm]})", d, t)
        return sorted(out, key=lambda x: x[1])

    def _heading(self, other) -> str:
        """Which way a road leaves here, by the places' positions: 'to the north', 'to the south-east'; '' without positions."""
        a, b = (self._w.s["nodes"].get(self.node) or {}).get("xy"), (self._w.s["nodes"].get(other) or {}).get("xy")
        if not a or not b:
            return ""
        import math
        dx, dy = float(b[0]) - float(a[0]), float(b[1]) - float(a[1])
        if abs(dx) + abs(dy) < 1e-9:
            return ""
        ang = math.degrees(math.atan2(dx, dy)) % 360                            # 0 north (y up), 90 east
        return "to the " + ["north", "north-east", "east", "south-east", "south", "south-west", "west", "north-west"][int((ang + 22.5) // 45) % 8]

    # ------------------------------------------------------------------ me
    @property
    def me(self) -> dict:
        return self._w.s["people"][self.name]

    @property
    def hands(self) -> str:
        return self.me["hands"]

    def carried(self) -> dict:
        return dict(self._w.goods(self.hands))

    def wear(self, cid=None) -> dict:
        return dict(self._w.s["containers"][cid or self.hands]["wear"])

    def load(self) -> float:
        return self._w.load(self.name)

    def capacity(self, track=False, oxen=None) -> float:
        return self._w.capacity(self.name, track, oxen)

    def pack_ox(self, want=None):
        """A herd of one's household here with an ox one could lead as a pack ox (one must carry a harness), else None (D2-136)."""
        from cybertron2.engine import herds as HD
        return HD.pack_ox_for(self._w, self.name, want)

    def led(self) -> list:
        """The beasts one is leading, here with one (D2-136): [(id, name, oxen)]."""
        from cybertron2.engine import herds as HD
        return [(hid, self._w.s["herds"][hid]["name"], int(self._w.s["herds"][hid].get("oxen", 0))) for hid in HD.led_by(self._w, self.name)]

    def units(self) -> int:
        return self._w.units_for(self.name)

    def tired(self) -> int:
        """Units off today from yesterday's pushing on and walking (labour.py, D4-108)."""
        from cybertron2.engine import labour as LA
        return LA.tired_units(self._w, self.name)

    def yield_mult(self) -> float:
        return self._w.yield_mult(self.name)

    def best_tool(self, table):
        return self._w.best_tool(self.name, table)

    def weapon(self):
        return self._w.weapon(self.name)

    # ------------------------------------------------------------------ who and what is here
    def people(self, me=True) -> list:
        """Who is here: at the node, or on the road one's party and whoever one meets (D2-120)."""
        return [x for x in self._w.company(self.name) if me or x != self.name]

    def person(self, x):
        """A living person here, by name, else None."""
        x = str(x or "").strip().lower()
        return next((n for n in self.people() if n.lower() == x), None)

    def someone(self, x):
        """A living person anywhere, by name (for a give that cannot reach them: D2-111), else None."""
        x = str(x or "").strip().lower()
        return next((n for n in self._w.living() if n.lower() == x), None)

    def hands_of(self, x) -> str:
        if x not in self.people():
            raise Refused(f"{x} is not here")
        return self._w.s["people"][x]["hands"]

    def body(self, x) -> dict:
        """What can be seen of someone here: stage, hunger, wounds, what they carry."""
        if x not in self.people():
            raise Refused(f"{x} is not here")
        a = self._w.s["people"][x]
        from cybertron2.engine import life as LF
        return {"stage": a["stage"], "hunger": a["hunger"], "wounded": a["wounded"], "carried": dict(self._w.goods(a["hands"])),
                "sex": a.get("sex", ""), "with_child": LF.showing(self._w, x), "partner": a.get("partner"), "widowed_of": a.get("widowed_of"),
                "parents": list(a.get("parents") or []), "cared": dict(a.get("cared") or {}),
                "grows": LF.grows_in(self._w, x)}

    def kept_of(self, x) -> dict:
        """What a child here holds to keep for good, as its carers know it (D4-64): {lines: [(text, source)], room}."""
        if x not in self.people():
            raise Refused(f"{x} is not here")
        from cybertron2.engine import memory as MEM
        k = MEM.kept(self._w, x)
        return {"lines": [(l["text"], l["source"]) for l in k["lines"]],
                "room": max(0, int(MEM.kept_settings(self._w)["childhood"])
                            - sum(1 for l in k["lines"] if str(l.get("source", "")).startswith("from ")))}

    def children_on(self) -> bool:
        from cybertron2.engine import life as LF
        return LF.on(self._w)

    def life(self) -> dict:
        """The world's life settings, for the verbs: the cost dial, whether children come, the spans (D2-145, D2-153)."""
        from cybertron2.engine import life as LF
        inst = self._w.s["institutions"].get(self.household() or "", {})
        return {"on": LF.on(self._w), "dial": LF.dial(self._w), "gap": LF.in_gap(self._w, self.name), "succession": inst.get("succession"),
                "order": inst.get("order"), "heir": inst.get("heir"), "lifespan": LF.lifespan(self._w)}

    def person_stage(self, x) -> str:
        return self._w.s["people"][x]["stage"]

    def buildings(self) -> dict:
        return {bid: b for bid, b in self._w.s["buildings"].items() if b["node"] == self.node}

    def building(self, x):
        x = str(x or "").strip().lower().removeprefix("the ").removeprefix("my ").removeprefix("your ")
        for bid, b in self.buildings().items():
            nm = b["name"].lower()
            if x in (bid.lower(), nm, nm.removeprefix("the ")):
                return bid
        if any(x in (p["name"].lower(), p["name"].lower().removeprefix("the ")) for p in self.parcels().values()):
            return None                                                       # a place's own name is the place (u2 §6 bug 5)
        hh = {iid: h for iid, h in self._w.s["institutions"].items() if h["kind"] == "household"}
        for iid, h in hh.items():                                             # "the Fenns", "Fenns" or "Fenn's": that household's house
            hn = h["name"].lower().removeprefix("the ")                         # here; never the bare "Fenn" (u2 §6 bug 5)
            if x in (iid.lower() + "s", iid.lower() + "'s", h["name"].lower(), hn, hn + "'s", hn.removesuffix("s") + "'s",
                     iid.lower() + " house", hn.removesuffix("s") + " house"):
                hb = [bid for bid in self.buildings() if any(c["claimant"] == iid for c in self._w.claims_on(("building", bid)))]
                if hb:
                    return hb[0]
        return None

    def parcels(self) -> dict:
        return {pid: p for pid, p in self._w.s["parcels"].items() if p["node"] == self.node}

    def parcel(self, x):
        x = str(x or "").strip().lower()
        for pid, p in self.parcels().items():
            if x in (pid.lower(), p["name"].lower(), p["name"].lower().removeprefix("the ")):
                return pid
        return None

    def herds(self) -> dict:
        return {hid: h for hid, h in self._w.s["herds"].items() if h["node"] == self.node}

    # ------------------------------------------------------------------ settings, tags and names, age (D4-65 to D4-69)
    def meeting_today(self):
        """The meeting called for this morning at this place, if any (D4-77): {day, by, about, at}."""
        for rec in list(self.buildings().values()) + list(self.parcels().values()):
            m = rec.get("meeting")
            if m and int(m.get("day", -1)) == self.day:
                return m
        return None

    def setting(self, key):
        return (self._w.spec or {}).get(key)

    def levels_on(self) -> bool:
        """Shelter in levels in this world (brief 4 §3)."""
        from cybertron2.engine import buildings as BL
        return BL.levels_on(self._w)

    def place_name(self, nid) -> str:
        return self._w.s["nodes"][nid]["name"] if nid in self._w.s["nodes"] else str(nid)

    def tag_of(self, x):
        """The tag meant by a tag, a name one knows, or a herd here."""
        from cybertron2.engine import tags as TG
        t = TG.resolve(self._w, self.name, x)
        if t is None:
            hid = self.herd(x)
            t = self._w.s["herds"][hid].get("tag") if hid else None
        return t

    def tagged_here(self, tag) -> bool:
        """A group of beasts here, or a thing here one knows of, with this tag."""
        from cybertron2.engine import tags as TG, things as TH
        return TG.herd_by_tag(self._w, tag) in self.herds() or TG.thing_by_tag(self._w, tag) in TH.known_here(self._w, self.name, self.node)

    def give_name(self, tag, name) -> list:
        from cybertron2.engine import tags as TG
        return TG.give_name(self._w, self.name, tag, name)

    def age_line(self) -> str:
        from cybertron2.engine import life as LF
        return LF.age_line(self._w, self.name)

    def herd(self, x=None):
        hs = self.herds()
        from cybertron2.engine import farm as FM, tags as TG
        if TG.on(self._w):                                                     # a tag, or a name one knows (D4-68)
            t = TG.resolve(self._w, self.name, x)
            if t:
                return next((hid for hid, h in hs.items() if h.get("tag") == t), None)
            x = TG.strip(str(x or "")).strip().lower()
            hit = [hid for hid, h in hs.items() if not x or x in (hid.lower(), h["name"].lower(), TG.strip(h["name"]).lower(), h["kind"],
                                                                  "cattle", "the herd", "herd", str(h.get("base_name") or "").lower())
                   or TG.strip(h["name"]).lower().startswith(x)]
            return next((hid for hid in hit if FM.head(hs[hid]) > 0), hit[0] if hit else None)
        x = str(x or "").strip().lower()
        return next((hid for hid, h in hs.items() if not x or x in (hid.lower(), h["name"].lower(), h["kind"], "cattle", "the herd", "herd")), None)

    def fittings(self, kind) -> list:
        """Buildings here with this fitting that the agent can get into."""
        return [bid for bid, b in self.buildings().items() if not b.get("unfinished") and b["fittings"].get(kind)
                and self._w.can_enter(self.name, bid)]

    def stock(self, bid) -> dict:
        return dict(self._w.goods(self.buildings()[bid]["stock"]))

    def remains(self) -> dict:
        return {cid: c for cid, c in self._w.s["containers"].items() if c["kind"] == "remains" and c["node"] == self.node
                and any(q > 1e-9 for q in c["goods"].values())}

    def offers(self) -> dict:
        return {oid: o for oid, o in self._w.s["offers"].items() if o["node"] == self.place and o["open"]
                and (self.node is not None or o["by"] in self.people())}

    def offer(self, oid) -> dict:
        o = self._w.s["offers"][oid]
        if o["node"] != self.place:
            raise Refused(f"offer {oid} is not here")
        return o

    def contents(self, cid) -> dict:
        """What is in a container here (hands of someone here, a store here)."""
        if self._w.place_of(("container", cid)) != self.place:
            raise Refused("that is not here")
        return dict(self._w.goods(cid))

    def events(self) -> list:
        return [e for e in self._w.s["events"] if e["place"] == self.node]

    def acts_today(self) -> list:
        return [a for a in self._w.s["acts"] if a["day"] == self.day and a["node"] == self.node]

    # ------------------------------------------------------------------ rights here (D4-23)
    def rights(self, thing, who=None) -> set:
        return self._w.rights(who or self.name, thing)

    def may_grant(self, thing) -> bool:
        return self._w.may_grant(self.name, thing)

    def claims(self, thing) -> list:
        return self._w.claims_on(thing)

    def claim_records(self, thing) -> list:
        thing = tuple(thing)
        return [(cid, c) for cid, c in self._w.s["claims"].items() if tuple(c["thing"]) == thing
                and (c.get("until") is None or c["until"] >= self.day)]

    def takeable(self, who=None) -> list:
        return self._w.takeable(who or self.name, self.node)

    def may_take(self, cid, who=None) -> bool:
        return self._w.may_take(who or self.name, cid)

    def can_enter(self, bid, who=None) -> bool:
        return self._w.can_enter(who or self.name, bid)

    def homes_here(self, who=None) -> list:
        return [b for b in self._w.homes(who or self.name) if self._w.s["buildings"][b]["node"] == self.node]

    def dwellings_here(self, who=None) -> list:
        return [b for b in self._w.dwellings(who or self.name) if self._w.s["buildings"][b]["node"] == self.node]

    def household(self, who=None):
        return self._w.household_of(who or self.name)

    def institution(self, iid) -> dict:
        return self._w.s["institutions"][iid]

    def households(self) -> dict:
        return {iid: h for iid, h in self._w.s["institutions"].items() if h["kind"] == "household"}

    def head(self, iid):
        return self._w.head(iid)

    def party_container(self, party):
        """The container here that acting for a party fills or draws on (D2-37): a person's hands, or the stock of a building here
        its household holds."""
        if party in self.people():
            return self._w.s["people"][party]["hands"]
        for bid, b in self.buildings().items():
            if any(c["claimant"] == party and "withdrawal" in c["rights"] for c in self._w.claims_on(("building", bid))):
                return b["stock"]
        return None

    def layout(self) -> list:
        """How the village fits together, in words (D2-116): parcels with neighbours, side and height; where the roads leave."""
        from cybertron2.engine import layout as LY
        return LY.layout_lines(self._w, self.name)

    def overview(self) -> list:
        """What strikes one first here: 3 to 5 lines (D2-116)."""
        from cybertron2.engine import layout as LY
        return LY.overview(self._w, self.node)

    def landmarks_known(self, nid) -> list:
        """The landmarks one knows on the road from here to `nid` (world/roads.md)."""
        r = next((rid for rid, x in self._w.s["roads"].items() if {x["a"], x["b"]} == {self.node, nid}), None)
        lm = self._w.s["mind"][self.name].get("landmarks") or {}
        return [f"{v['words']} (crossed {v['crossed']} time{'s' if v['crossed'] != 1 else ''})" for v in lm.values() if v.get("road") == r]

    def weather_words(self, day=None, at=None) -> str:
        from cybertron2.engine import environment as EV
        return EV.words(self._w, at or self.place, day)

    def house_of(self, party):
        """A person's or a household's house here (where a give that cannot reach them is left at the door: D2-111)."""
        hh = self._w.s["institutions"].get(party)
        members = hh["members"] if hh else [party] if party in self._w.s["people"] else []
        for bid in self.buildings():
            if any(bid in self._w.homes(m) for m in members):
                return bid
        return None

    # ------------------------------------------------------------------ things at a spot (world/things_in_places.md)
    def things(self) -> dict:
        from cybertron2.engine import things as TH
        return TH.at_node(self._w, self.node)

    def house_things(self, bid) -> dict:
        """What hangs inside a house here or lies at its door, not hidden (racks, piles; empty ones too): {thing id: thing}. Its
        household knows them without a roll (brief 4c §6.4)."""
        return {cid: c for cid, c in self._w.s["containers"].items() if c.get("kind") == "pile" and c.get("node") == self.node
                and not c.get("hidden") and (c.get("in") == bid or c.get("door") == bid)}

    # the processing containers (u4; process.py) and the brine spring (brief 5 §4b; keeping.py)
    def lot_room(self, bid, proc) -> float:
        from cybertron2.engine import process as PROC
        return PROC.room(self._w, bid, proc)

    def smoke_fuel(self, bid) -> tuple:
        """(heat tonight's fire wants, heat there)."""
        from cybertron2.engine import process as PROC
        return PROC.fuel_tonight(self._w, bid), PROC.fuel_have(self._w, bid)

    def river_parcel(self, pid) -> bool:
        """Whether a parcel here is water on a river (brief 5 §3)."""
        from cybertron2.engine import wild as WL
        return bool(WL._river_parcel(self._w, pid))

    def run_here(self, pid) -> bool:
        """A run passes this place's water at that parcel today (Q-79 bug 1; W-97)."""
        from cybertron2.engine import wild as WL
        return WL.run_here(self._w, self.node, pid)

    def owns_set(self, c) -> bool:
        """A set thing one's own or one's household's (D2-305; W-97)."""
        from cybertron2.engine import things as TH
        return TH.owns_set(c, self.name, self._w)

    def own_set_at(self, tech, pid):
        """One's own (or household's) set thing of a technique standing at a parcel here, the newest (u2 §3; W-97)."""
        from cybertron2.engine import things as TH
        hits = [(int((c.get("set") or {}).get("set_day", 0)), cid) for cid, c in self._w.s["containers"].items()
                if c.get("kind") == "set" and c.get("parcel") == pid and not (c.get("set") or {}).get("weir")
                and (c.get("set") or {}).get("method") == tech and TH.owns_set(c, self.name, self._w) and TH.set_about(self._w, c)]
        return max(hits)[1] if hits else None

    # placed gear and the water's states (u1, u2; W-98): the reads the placed-gear acts make
    def sets(self) -> dict:
        """The set things standing here (not taken up or spent past `spent_days`): {thing id: thing}."""
        from cybertron2.engine import things as TH
        def live(sp):                                                          # spent and not yet looked at since: still there to
            return sp.get("state") != "up" and not (sp.get("state") == "spent" and int(sp.get("tended", -1)) >= int(sp.get("sprung", -1) or -1))
        return {cid: c for cid, c in self._w.s["containers"].items() if c.get("kind") == "set" and c.get("node") == self.node
                and TH.set_about(self._w, c) and live(c.get("set") or {})}             # be tended and found gone

    def gear_words(self) -> list:
        """One's own gear in hand and its state: ['6 wicker traps: 2 broken, wanting mending; the rest good for about 8 more nights set']."""
        from cybertron2.engine import gear as GE
        return GE.held_words(self._w, self.hands)

    def owns_thing(self, c) -> bool:
        """A thing lying somewhere one's own: put there by oneself or one's household (D2-305)."""
        by = c.get("by")
        if not by:
            return False
        hh = self._w.household_of(self.name)
        return by == self.name or (bool(hh) and self._w.household_of(by) == hh)

    def sound_held(self, item) -> int:
        """Whole pieces of a good in one's hands fit to use (gear worn past use is not; u3 §3.2)."""
        from cybertron2.engine import gear as GE
        return GE.sound_count(self._w.s["containers"][self.hands], item, self._w)

    def pieces(self, cid, item) -> list:
        from cybertron2.engine import gear as GE
        return GE.pieces(self._w.s["containers"][cid], item, self._w)

    def ice(self, pid) -> str:
        """The ice on a water or fen parcel here today: open, edges or over (u1 §4)."""
        from cybertron2.wild import water as WT
        return WT.ice(self._w, pid)

    def water_type(self, pid):
        from cybertron2.wild import water as WT
        return WT.water_type(self._w, pid)

    def pinch(self, pid) -> float:
        from cybertron2.wild import water as WT
        return WT.pinch(self._w, pid)

    def day_words(self, day) -> str:
        c = self._w.calendar(day)
        return f"{c['season']} day {c['day']}"

    def catch_words(self, c) -> str:
        from cybertron2.engine import things as TH
        return TH.catch_words(self._w, c)

    def plural(self, kind) -> str:
        from cybertron2.engine import things as TH
        return TH._plural(kind)

    def run_kinds(self, pid) -> list:
        """The kinds of a run passing this place's water at that parcel today (u2 §4.1's water axis)."""
        from cybertron2.engine import wild as WL
        return WL.run_kinds(self._w, self.node, pid)

    def flow_tonight(self) -> str:
        """The river's flow tonight at this place, from the catchment's rain (normal, high, spate, flood; normal without a river)."""
        from cybertron2.engine import wild as WL
        return WL.flow_tonight(self._w, self.node)

    def weir_water(self, pid) -> str:
        """A weir's water for its cost (D2-302): beck, lowland or large (wild.water_kind); lowland without the wild layer."""
        from cybertron2.engine import wild as WL
        try:
            return WL.water_kind(self._w, WL.model(self._w), pid) if WL.on(self._w) else "lowland"
        except Exception:                                                      # a world with no river network: as lowland
            return "lowland"

    def mind(self):
        from cybertron2.engine.here import Mind
        return Mind(self._w, self.name)

    def has_gap(self, b) -> bool:
        """Whether a building is a weir or a water mill with a gap (brief 5 §3, §3a)."""
        from cybertron2.engine import wild as WL
        return bool(WL.has_gap(self._w, b))

    def mill_water(self, b):
        """The water parcel a mill holds (brief 5 §3a)."""
        from cybertron2.engine import wild as WL
        return WL.mill_water(self._w, b)

    def mill_rate(self, b) -> float:
        """The water wheel's grinding rate by its gap (brief 5 §3a)."""
        from cybertron2.engine import wild as WL
        return WL.mill_rate(self._w, b)

    def near_spring(self, pid, kind="brine") -> bool:
        from cybertron2.engine import keeping as KP
        return KP.near_spring(self._w, pid, kind)


    def thing(self, cid) -> dict:
        c = self._w.s["containers"].get(cid)
        return c if c and c.get("node") == self.node else None

    def bodies(self) -> dict:
        from cybertron2.engine import things as TH
        return TH.bodies(self._w, self.node)

    def carcasses(self) -> dict:
        from cybertron2.engine import things as TH
        return TH.carcasses(self._w, self.node)

    def carcass_size(self, cid) -> str:
        from cybertron2.engine import things as TH
        return TH.carcass_size(self._w.s["containers"][cid])

    def grave_left(self, cid) -> int:
        """Units of digging a grave still wants, by the ground and the cold now (D2-96, D4-99)."""
        from cybertron2.engine import things as TH
        return TH.grave_left(self._w, cid)

    def graves(self) -> dict:
        """Graves here with no cairn yet (D4-99)."""
        from cybertron2.engine import things as TH
        return TH.graves(self._w, self.node)

    def spot_name(self, c) -> str:
        from cybertron2.engine import things as TH
        return TH.parcel_name(self._w, c)

    def bury_units(self, cid, cairn=False) -> int:
        from cybertron2.engine import things as TH
        return TH.bury_units(self._w, cid, cairn)

    def search_thing(self, where, item=None):
        from cybertron2.engine import things as TH
        return TH.search(self._w, self.name, where, item)

    def find_thing(self, where, item=None):
        from cybertron2.engine import things as TH
        return TH.find(self._w, self.name, where, item)

    def remember_thing(self, cid, how) -> None:
        from cybertron2.engine import things as TH
        TH.remember(self._w, self.name, cid, how)

    def look_thing(self, cid) -> None:
        """One looked a set thing over (brief 4c §4.3): what it held and the day, for the remembered line."""
        from cybertron2.engine import things as TH
        TH.look(self._w, self.name, cid)

    def set_line(self, c, r, daystr):
        """The remembered line of a set thing one knows (brief 4c §4.3), or None for the plain line."""
        from cybertron2.engine import things as TH
        return TH.set_line(self._w, self.name, c, r, daystr)

    def known_things(self) -> dict:
        from cybertron2.engine import things as TH
        return {cid: (r, self.thing(cid)) for cid, r in TH.known_here(self._w, self.name, self.node).items()}

    def living_in(self, bid) -> list:
        return [m for m in self._w.living() if bid in self._w.homes(m)]

    def household_name(self, bid):
        return _household_name(self._w, bid)

    def born_trades(self) -> set:
        return _born_trades(self._w, self.node)

    def agreements(self, who=None) -> dict:
        who = who or self.name
        hh = self._w.household_of(who)
        return {aid: a for aid, a in self._w.s["agreements"].items() if who in a["parties"] or hh in a["parties"]}

    def works_for(self, party) -> bool:
        """An open agreement in which I (or my household) owe work to this party (D2-36 to D2-38: the worker acts for the employer)."""
        def circle(x):                                                        # a person and their household, or a household and its members
            if x in self._w.s["people"]:
                return {x, self._w.household_of(x)}
            return {x} | set((self._w.s["institutions"].get(x) or {}).get("members", []))
        mine, theirs = circle(self.name), circle(party)
        return any(a["status"] == "open" and "work" in l and l["done"] < l["work"] and l["from"] in mine and l["to"] in theirs
                   for a in self.agreements().values() for l in a["legs"])

    # ------------------------------------------------------------------ acting, at this node only
    def apply(self, prim, **kw):
        return self._w.apply(prim, self.place, **kw)

    def event(self, kind, text, **kw):
        return self._w.event(self.place, kind, text, **kw)

    def record(self, verb, tech=None, for_=None, **extra):
        self._w.record(self.name, verb, tech, for_, self.place, **extra)

    def cause(self, verb, for_=None):
        return self._w.cause(actor=self.name, verb=verb, for_=for_, node=self.place)

    def new_offer(self, rec) -> str:
        return self.apply("offer", by=self.name, rec=rec)

    def new_agreement(self, rec) -> str:
        return self.apply("agree", node=self.place, rec=rec)

    def today(self) -> dict:
        return self._w.s["today"]


def _household_name(w, bid):
    hh = next((c["claimant"] for c in w.claims_on(("building", bid)) if c["claimant"] in w.s["institutions"]
               and "alienation" in c["rights"]), None)
    return w.s["institutions"][hh]["name"] if hh else None


def _born_trades(w, node) -> set:
    """The trades of the lines born at a node (D4-33: its repute), from those whose home is there."""
    from cybertron2.engine.data import TECHNIQUES
    out = set()
    for x, a in w.s["people"].items():
        hh = w.household_of(x)
        if not a["alive"] or not hh or a.get("born_line") != hh:
            continue
        if not any(w.s["buildings"][b]["node"] == node for b in w.homes(x)):
            continue
        out |= {t for t, r in w.s["know"].get(x, {}).items() if r["level"] == "known" and not TECHNIQUES[t].get("basic")}
    return out


class NodeView:
    """A read view of one node for seeding what people know of places (engine side only; agents never get one)."""

    def __init__(self, w, node):
        self._w, self.node = w, node

    def parcels(self):
        return {k: v for k, v in self._w.s["parcels"].items() if v["node"] == self.node}

    def buildings(self):
        return {k: v for k, v in self._w.s["buildings"].items() if v["node"] == self.node}

    def herds(self):
        return {k: v for k, v in self._w.s["herds"].items() if v["node"] == self.node}

    def household_name(self, bid):
        return _household_name(self._w, bid)

    def born_trades(self):
        return _born_trades(self._w, self.node)


class Mind:
    """What one person knows: its knowledge of crafts, its memory and beliefs, its notes, its kin and places as it knows them. It
    is the agent's own; reading it never reads the world."""

    def __init__(self, w, name):
        from cybertron2.engine import packs as PK
        self.packs = PK.use(w)                                             # the world's switched-on packs (D4-103)
        self.name = name
        self.know = w.s["know"].setdefault(name, {})
        self.store = w.s["mind"][name]
        self.person = w.s["people"][name]
        self._cal = w.calendar
        self.day = w.d
        self.p = w.p
        from cybertron2.engine import memory as MEM
        self.memory_mode = MEM.mode_for(w, name)                               # D4-61: rewrite, or append for weak models
        self.household = w.household_of(name)
        h = w.s["institutions"].get(self.household) if self.household else None
        self.household_name = h["name"] if h else None
        self.members = [m for m in (h["members"] if h else []) if m != name]   # one knows who belongs to one's household
        self.head = h["offices"].get("head") if h else None

    def calendar(self, day=None):
        return self._cal(self.day if day is None else day)

    @property
    def notes(self) -> dict:
        return self.person["notes"]

    def kin(self) -> dict:
        return self.store.get("kin", {})

    def places(self) -> dict:
        return self.store.get("places", {})

    def home_seen(self):
        return self.person.get("home_seen")
