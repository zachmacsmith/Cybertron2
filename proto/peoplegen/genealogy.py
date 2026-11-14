"""The past built backward from a pinned present (generation_redesign.md §4.3), as decisions for the solver (§4.5).

Decisions, in the order they are made:
- found:<village>    the year the village was founded (pinned, or drawn: an older village for a bigger present);
- pairs:<household>  who in the household is married to whom (a matching of its adults);
- par:<person>       who a person's parents were, newest births first, so the build runs backward in time like a coalescent:
                     an existing couple (the present couple, an ancestral couple already made: siblings merge here, across
                     households and villages), a new couple in some village, one living person and a dead spouse, a couple at
                     the declared off-map node, or none (came from outside the record, for someone born before their village was
                     founded). Each new ancestor born within the span gets a par: decision of their own;
- age:<couple>       the age of a new couple's other spouse;
- wid:<person>       a dead spouse for a pinned widow or widower whom no living child gave one;
- death:<person>     when each ancestor who is not living now died;
- fill:<couple>      the couple's marriage year and the children not living now (died young, or left), from the fertility table.

Candidates are weighted by the forward model (demog.py): fertility at the mother's age, spacing after a birth, the chance each
parent is alive now (present) or dead now (absent), the marriage market by distance, and the number of couples a village had at
the time (its present households grown back to its founding), less those already made: the coalescent's merge rate."""
from __future__ import annotations

import math

from . import demog as D
from .keyed import order, u
from .solver import Trail, Var


EPS = 1e-12                                                     # a candidate the checks will reject, or nearly impossible


class P:
    __slots__ = ("id", "sex", "born", "bsrc", "kind", "hh", "village", "unions", "pc", "psrc", "died", "cause", "fate", "role",
                 "came", "age")

    def __init__(self, id, sex, born, bsrc, kind, hh=None, village=None, role=None):
        self.id, self.sex, self.born, self.bsrc, self.kind = id, sex, born, bsrc, kind
        self.hh, self.village, self.role = hh, village, role
        self.unions, self.pc, self.psrc, self.died, self.cause, self.fate, self.came = [], None, None, None, None, None, False
        self.age = None if born is None else -born


class C:
    __slots__ = ("id", "f", "m", "res", "kids", "src", "wed", "ghost")

    def __init__(self, id, f, m, res, src, ghost=None):
        self.id, self.f, self.m, self.res, self.src, self.ghost = id, f, m, res, src, ghost
        self.kids, self.wed = [], None


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


class Build:
    def __init__(self, spec: dict, seed: int):
        self.seed = seed
        self.span = int(spec.get("span", 100))
        self.V = {v: d["at"] for v, d in spec["villages"].items()}
        self.off = spec.get("off")
        self.hard = set(spec["hard_years"]) if spec.get("hard_years") is not None else D.hard_years(seed, self.span)
        self.pin_found = (spec.get("pins") or {}).get("found") or {}
        self.trail = Trail()
        self.P, self.C, self.F = {}, {}, {}
        self.hh = {}
        self.H = {}                                               # present households per village
        for h in spec["households"]:
            ms = []
            for k, m in enumerate(h["members"]):
                i = m.get("id") or f"{h['id']}.{k}"
                self.P[i] = P(i, m["sex"], -int(m["age"]), f"pin:age:{i}", "present", h["id"], h["village"], m.get("role"))
                ms.append(i)
            self.hh[h["id"]] = {"village": h["village"], "members": ms}
            self.H[h["village"]] = self.H.get(h["village"], 0) + 1
        self.heads = {}
        for h, d in self.hh.items():
            r = [i for i in d["members"] if self.P[i].role == "head"]
            self.heads[h] = r[0] if r else None
        self.couples_by_res = {}

    # ------------------------------------------------------------------ helpers
    def dv(self, a, b):
        at = lambda v: self.off["at"] if v == "OFF" else self.V[v]
        return dist(at(a), at(b))

    def K(self, v, b):
        """Fertile couples in village v in year b: its present households grown back to two at its founding (calibrate)."""
        F = self.F.get(v)
        if F is None or b < F:
            return 0.0
        H = max(2, self.H.get(v, 2))
        t = (b - F) / max(1, -F)
        return D.KFRAC * 2 * (H / 2) ** t

    def kids_of_mother(self, m):
        return [k for c in self.P[m].unions for k in self.C[c].kids if self.C[c].m == m]

    def adult_village(self, x):
        p = self.P[x]
        if p.kind == "present":
            return p.village
        for c in p.unions:
            return self.C[c].res
        return None

    def married(self, x):
        return bool(self.P[x].unions)

    def anc(self, x, depth=2):
        """{ancestor: decisions on the way} for x and its ancestors within depth generations (x itself at depth 0)."""
        out = {x: set()}
        front = [(x, set())]
        for _ in range(depth):
            nxt = []
            for y, via in front:
                p = self.P[y]
                if p.pc is None:
                    continue
                c = self.C[p.pc]
                for q in (c.f, c.m):
                    vq = via | {p.psrc}
                    out.setdefault(q, set()).update(vq)
                    nxt.append((q, vq))
            front = nxt
        return out

    def desc(self, x, depth=2):
        out, front = {x}, [x]
        for _ in range(depth):
            front = [k for y in front for c in self.P[y].unions for k in self.C[c].kids]
            out.update(front)
        return out

    def incest(self, x):
        """Spouses who share an ancestor within two generations (or one is the other's), among x's couples and its descendants'."""
        for y in sorted(self.desc(x)):
            for cid in self.P[y].unions:
                c = self.C[cid]
                a, b = self.anc(c.f), self.anc(c.m)
                common = set(a) & set(b)
                if common:
                    z = sorted(common)[0]
                    return a[z] | b[z] | {c.src}
        return None

    def alive_now(self, q, b):
        """The chance parent q, alive at the birth in year b, is in the state the present says: alive if living now, dead if not."""
        p = self.P[q]
        if p.kind == "off":
            return 1.0
        if p.born is None:
            return 1.0
        s = D.survive(b - p.born, -p.born)
        return s if p.kind == "present" else 1 - s

    def res_w(self, x, r):
        """The marriage market and residence: where x's parents lived, given where x lives as an adult."""
        p = self.P[x]
        v = self.adult_village(x)
        if p.kind == "present" and p.age < 16:
            return 1.0 if r == v else 0.0
        if v is None or r == v:
            return 1.0
        k = math.exp(-self.dv(r, v) / D.LAMBDA)
        if p.sex == "f" and self.married(x):
            return D.OUT * k
        return D.MOVE * k

    def spacing(self, m, b):
        ks = [self.P[k].born for k in self.kids_of_mother(m)]
        if not ks:
            return 1.0
        d = min(abs(b - y) for y in ks)
        return 0.0 if d < 1 else 0.3 if d == 1 else 1.0

    def klass(self, cand):
        if cand[0] in ("new",):
            return cand[:2]
        if cand[0] in ("off", "age", "death", "fill", "year"):
            return cand[:1]
        return cand

    # ------------------------------------------------------------------ decisions
    def initial(self):
        vs = [Var(f"found:{v}", (0, v), pin=("year", self.pin_found[v]) if v in self.pin_found else None) for v in sorted(self.V)]
        vs += [Var(f"pairs:{h}", (1, h)) for h in sorted(self.hh)]
        vs += [Var(f"par:{i}", (2, -p.born, i, 0)) for i, p in sorted(self.P.items()) if p.born >= -self.span]
        vs += [Var(f"wid:{i}", (2.9, i)) for i, p in sorted(self.P.items()) if p.role == "widowed"]
        return vs

    # a pinned widow or widower with no dead spouse yet (none was needed to explain living children): one is made
    def c_wid(self, x):
        return [(("wid",), 1.0)]

    def a_wid(self, var, x, cand):
        q = self.P[x]
        if any(self.C[c].ghost == x for c in q.unions):
            return None, []
        t = self.trail
        gh = P(f"{x}~", "m" if q.sex == "f" else "f", None, var.id, "ghost")
        fa, mo = (gh, q) if q.sex == "f" else (q, gh)
        c = C(f"pg:{x}", fa.id, mo.id, q.village, var.id, ghost=x)
        t.put(self.P, gh.id, gh)
        t.put(self.C, c.id, c)
        t.push(q.unions, c.id)
        t.push(gh.unions, c.id)
        t.push(self.couples_by_res.setdefault(q.village, []), c.id)
        return None, [Var(f"age:{c.id}", (2.95, x)), Var(f"death:{gh.id}", (3, gh.id)), Var(f"fill:{c.id}", (5, c.id))]

    def cands(self, var):
        kind, key = var.id.split(":", 1)
        return getattr(self, "c_" + kind)(key)

    def blame(self, var):
        """The decisions a decision reads: where its conflict set goes when it has no candidate at all."""
        kind, key = var.id.split(":", 1)
        if kind == "par":
            p = self.P[key]
            pins = set()
            if p.role:
                pins = {f"pin:role:{key}"} | ({f"pin:age:{self.heads[p.hh]}", f"pin:role:{self.heads[p.hh]}"} if self.heads.get(p.hh) else set())
            if p.kind == "present" and p.age < 16:                 # a child is born where it lives, to a couple paired at home
                return {p.bsrc, f"pairs:{p.hh}"} | pins | ({f"found:{p.village}"} if p.born < self.F.get(p.village, -999) else set())
            av = self.adult_village(key)
            return {p.bsrc} | pins | {f"found:{v}" for v in self.V if p.born < self.F.get(v, -999)} | ({f"found:{av}"} if av in self.V else set())
        if kind == "age":
            c = self.C[key]
            return {c.src} | {self.P[k].psrc for k in c.kids}
        if kind == "death":
            return {self.P[k].psrc for c in self.P[key].unions for k in self.C[c].kids} | self.bounds(key)[2]
        return set()

    def apply(self, var, cand):
        kind, key = var.id.split(":", 1)
        return getattr(self, "a_" + kind)(var, key, cand)

    # found
    def c_found(self, v):
        H = max(2, self.H.get(v, 2))
        est = -min(self.span, max(10, math.log(H / 2) / 0.02))
        return [(("year", y), math.exp(-((y - est) ** 2) / (2 * 15 ** 2))) for y in range(-self.span, -4)]

    def a_found(self, var, v, cand):
        minors = [p for p in self.P.values() if p.kind == "present" and p.village == v and p.age < 16]
        old = min(minors, key=lambda p: p.born) if minors else None
        if old and cand[1] > old.born:                              # the village was there when its children were born
            return {old.bsrc}, None
        self.trail.put(self.F, v, cand[1])
        return None, []

    # pairs
    def c_pairs(self, h):
        ad = sorted([i for i in self.hh[h]["members"] if self.P[i].age >= 16], key=lambda i: (self.P[i].born, i))
        out = []

        def rec(rest, pairs, w):
            if not rest:
                out.append((("pairs", tuple(pairs)), w))
                return
            a, rest2 = rest[0], rest[1:]
            pa = self.P[a]
            single = 1.0 - 0.85 * D.married_share(pa.age, pa.sex) if pa.age < 60 else 0.5     # never married, or widowed
            rec(rest2, pairs, w * max(single, 0.05))
            for b in rest2:
                pb = self.P[b]
                if pb.sex == pa.sex:
                    continue
                m, f = (a, b) if pa.sex == "m" else (b, a)
                gap = self.P[m].age - self.P[f].age
                if -5 <= gap <= 25:                                 # a couple explains the children they could have borne
                    n = sum(1 for k in self.hh[h]["members"] if self.P[k].age < 16 and 16 <= self.P[f].age - self.P[k].age <= 45)
                    rec([r for r in rest2 if r != b], pairs + [(m, f)], w * D.gap_w(gap) * 3 * (1 + 4 * n))

        rec(ad, [], 1.0)
        return out

    def a_pairs(self, var, h, cand):
        pairs = cand[1]
        head = self.heads[h]
        for i in self.hh[h]["members"]:
            r = self.P[i].role
            inpair = any(i in pr for pr in pairs)
            if r == "spouse" and not (head and any(set(pr) == {i, head} for pr in pairs)):
                return {f"pin:role:{i}", f"pin:role:{head}"}, None
            if r in ("widowed", "single") and inpair:
                return {f"pin:role:{i}"}, None
        for m, f in pairs:
            c = C(f"cp:{m}+{f}", m, f, self.hh[h]["village"], var.id)
            self.trail.put(self.C, c.id, c)
            self.trail.push(self.P[m].unions, c.id)
            self.trail.push(self.P[f].unions, c.id)
        return None, [Var(f"fill:cp:{m}+{f}", (5, f"cp:{m}+{f}")) for m, f in pairs]

    # par
    def c_par(self, x):
        p = self.P[x]
        b = p.born
        out = []
        v = self.adult_village(x)
        minor = p.kind == "present" and p.age < 16
        for cid, c in self.C.items():                            # every couple whose ages are known is a candidate: those that
            if x in (c.f, c.m) or c.m is None:                   # cannot be are rejected by check_child, which says why (so the
                continue                                         # conflict set is complete), and weigh next to nothing
            m, f = self.P[c.m], self.P[c.f]
            if m.born is None or f.born is None:
                continue
            am, af = b - m.born, b - f.born
            r = c.res
            w = D.fert(am) * self.spacing(c.m, b) * self.alive_now(c.m, b) * self.alive_now(c.f, b) * (1.0 if 16 <= af <= 72 else 0)
            if r == "OFF":
                w *= self.off_w(x)
            else:
                w *= self.res_w(x, r)
                if b < self.F.get(r, -999):
                    w *= 0.15
            w *= self.co(x, [q for q in (c.f, c.m) if self.P[q].kind == "present"])
            out.append((("c", cid), max(w, EPS)))
        for r in sorted(self.V):
            k = self.K(r, b)
            if k <= 0:
                continue
            n = sum(1 for c in self.couples_by_res.get(r, ()) if self.P[self.C[c].m].born is not None
                    and 16 <= b - self.P[self.C[c].m].born <= 45)
            crowd = max(k - n, D.FLOOR)
            rw = self.res_w(x, r)
            if rw <= 0:
                continue
            foster = D.FOSTER if minor else 1.0                    # a child whose parents are both dead is raised by others
            for am in range(16, 46):
                dead = (1 - D.survive(am, am - b)) * (1 - D.survive(am + 3, am + 3 - b))
                out.append((("new", r, am), crowd * D.g(am) * rw * dead * foster))
        if self.off and not minor:
            for am in range(16, 46):
                out.append((("off", am), D.OFF_RATE * D.g(am) * self.off_w(x)))
        for q, pq in sorted(self.P.items()):
            if pq.kind != "present" or q == x or any(self.C[c].ghost == q for c in pq.unions):
                continue
            a = b - pq.born
            if not ((15 <= a <= 47) if pq.sex == "f" else (16 <= a <= 65)):
                continue
            r = pq.village
            w = (D.fert(a) if pq.sex == "f" else D.FBAR) * D.survive(a, pq.age) * (0.15 if pq.unions else 0.6)
            w *= (self.spacing(q, b) if pq.sex == "f" else 1.0) * self.res_w(x, r) * self.co(x, [q])
            ga = a - D.GAP[0] if pq.sex == "m" else a + D.GAP[0]          # the dead spouse's age then, about
            w *= 1 - D.survive(ga, ga - b)                                 # and dead now
            out.append((("with", q), max(w, EPS)))
        if v in self.F and b < self.F[v] and not minor:
            out.append((("came",), D.CAME_RATE * D.FBAR))
        return self.by_role(x, out)

    def by_role(self, x, out):
        """Candidates a role pin rules out are not offered (a pin is never revisited, so there is nothing to blame)."""
        p = self.P[x]
        head = self.heads.get(p.hh) if p.kind == "present" else None
        mem = lambda k: ((self.C[k[1]].f, self.C[k[1]].m) if k[0] == "c" else (k[1],) if k[0] == "with" else ())
        if p.role == "child" and head:
            out = [(k, w) for k, w in out if head in mem(k)]
        if p.role == "lodger":
            out = [(k, w) for k, w in out if not any(self.P[q].kind == "present" and self.P[q].hh == p.hh for q in mem(k))]
        if head == x:
            want = [i for i in self.hh[p.hh]["members"] if self.P[i].role == "parent"]
            if want:
                out = [(k, w) for k, w in out if all(q in mem(k) for q in want)]
        return out

    def co(self, x, livers):
        """Living in one household is evidence of kin: a child lives with a living parent; a grown son or an unmarried daughter
        living with an elder is mostly that elder's child (forward model: 9 in 10); a wife mostly lives with her husband's."""
        p = self.P[x]
        if p.kind != "present" or not livers:
            return 1.0
        same = any(self.P[q].hh == p.hh for q in livers)
        if p.age < 16:
            return 1.0 if same else 0.03
        if p.sex == "f" and self.married(x):
            return 1.0
        return D.CO if same else 1.0

    def off_w(self, x):
        p = self.P[x]
        if not self.off:
            return 0.0
        v = self.adult_village(x)
        k = math.exp(-self.dv("OFF", v) / D.LAMBDA) if v else 1.0
        return k if p.sex == "f" and self.married(x) else 0.3 * k

    def a_par(self, var, x, cand):
        p = self.P[x]
        b = p.born
        t = self.trail
        mark = len(t)
        new = []
        kind = cand[0]
        if kind == "came":
            if p.role == "child":
                return {f"pin:role:{x}"}, None
            t.set(p, "came", True)
            return None, []
        if kind == "c":
            c = self.C[cand[1]]
        elif kind in ("new", "off"):
            r = cand[1] if kind == "new" else "OFF"
            am = cand[-1]
            kk = "anc" if kind == "new" else "off"
            mo = P(f"{x}^m", "f", b - am, var.id, kk)
            fa = P(f"{x}^f", "m", None, var.id, kk)
            c = C(f"pc:{x}", fa.id, mo.id, r, var.id)
            for o in (mo, fa):
                t.put(self.P, o.id, o)
            t.put(self.C, c.id, c)
            t.push(mo.unions, c.id)
            t.push(fa.unions, c.id)
            t.push(self.couples_by_res.setdefault(r, []), c.id)
            new.append(Var(f"age:{c.id}", (2, -b, x, 1)))
            if kind == "new":
                if mo.born >= -self.span:
                    new.append(Var(f"par:{mo.id}", (2, -mo.born, mo.id, 0)))
                new += [Var(f"death:{mo.id}", (3, mo.id)), Var(f"death:{fa.id}", (3, fa.id)), Var(f"fill:{c.id}", (5, c.id))]
        elif kind == "with":
            q = self.P[cand[1]]
            gh = P(f"{q.id}~", "m" if q.sex == "f" else "f", None, var.id, "ghost")
            fa, mo = (gh, q) if q.sex == "f" else (q, gh)
            c = C(f"pg:{q.id}", fa.id, mo.id, q.village, var.id, ghost=q.id)
            t.put(self.P, gh.id, gh)
            t.put(self.C, c.id, c)
            t.push(q.unions, c.id)
            t.push(gh.unions, c.id)
            t.push(self.couples_by_res.setdefault(q.village, []), c.id)
            new += [Var(f"age:{c.id}", (2, -b, x, 1)), Var(f"death:{gh.id}", (3, gh.id)), Var(f"fill:{c.id}", (5, c.id))]
        else:
            raise ValueError(cand)
        conflict = self.check_child(x, c, var)
        if conflict is None:
            t.set(p, "pc", c.id)
            t.set(p, "psrc", var.id)
            t.push(c.kids, x)
            conflict = self.incest(x) or self.interleave(c)
        if conflict is not None:
            t.undo(mark)
            return conflict, None
        return None, new

    def check_child(self, x, c, var):
        """x as a child of couple c: the role pins, the mother's age and spacing, the father's age, both alive and in place."""
        p = self.P[x]
        b = p.born
        h = p.hh
        if p.role == "child" and self.heads.get(h) not in (c.f, c.m):
            return {f"pin:role:{x}"}                             # no choice of how c was made would put the head in it
        if p.role == "lodger" and any(self.P[q].kind == "present" and self.P[q].hh == h for q in (c.f, c.m)):
            return {f"pin:role:{x}"}
        head = self.heads.get(h)
        if head == x:
            want = [i for i in self.hh[h]["members"] if self.P[i].role == "parent"]
            if want and not all(w in (c.f, c.m) for w in want):
                return {f"pin:role:{w}" for w in want}
        m, f = self.P[c.m], self.P[c.f]
        if m.born is not None:
            am = b - m.born
            if not 15 <= am <= 47:                               # the ages are pins or age: decisions; who made the couple
                return {p.bsrc, m.bsrc}                          # cannot change them, so it is not blamed
            for k in self.kids_of_mother(c.m):
                if abs(self.P[k].born - b) < 1:
                    return {p.bsrc, self.P[k].bsrc, self.P[k].psrc}
        if f.born is not None and not 16 <= b - f.born <= 72:
            return {p.bsrc, f.bsrc}
        if p.kind == "present" and p.age < 16 and c.res != p.village:
            return {p.bsrc} | ({c.src} if c.id.startswith("pc:") else set())   # only a new couple's place was chosen
        for q in (m, f):
            if q.died is not None and q.died < b - (1 if q is f else 0):
                return {p.bsrc, f"death:{q.id}"}
        return None

    def interleave(self, c):
        """A living person's dead spouse came first: all that union's children before any of the living union's."""
        for q in (c.f, c.m):
            us = self.P[q].unions
            gh = [u_ for u_ in us if self.C[u_].ghost == q]
            li = [u_ for u_ in us if self.C[u_].ghost != q]
            if gh and li:
                g_k, l_k = self.C[gh[0]].kids, [k for u_ in li for k in self.C[u_].kids]
                if g_k and l_k and max(self.P[k].born for k in g_k) >= min(self.P[k].born for k in l_k):
                    a = max(g_k, key=lambda k: self.P[k].born)
                    z = min(l_k, key=lambda k: self.P[k].born)
                    return {self.P[a].psrc, self.P[z].psrc, self.P[a].bsrc, self.P[z].bsrc}
        return None

    # age of the other spouse
    def c_age(self, cid):
        c = self.C[cid]
        m, f = self.P[c.m], self.P[c.f]
        known = m if m.born is not None else f
        k0 = min(self.P[k].born for k in c.kids) if c.kids else known.born + 24     # childless: about the wedding
        out = []
        if f.born is None:                                         # the father's age, given the mother's
            for gap in range(-3, 21):
                fb = m.born - gap
                w = D.gap_w(gap) * (self.alive_now(c.f, k0) if f.kind == "present" else 1 - D.survive(k0 - fb, -fb) if f.kind != "off" else 1)
                out.append((("age", fb), w))
        else:                                                      # a dead mother's age, given the living father's
            for gap in range(-3, 21):
                mb = f.born + gap
                am = k0 - mb
                if 16 <= am <= 45:
                    out.append((("age", mb), D.gap_w(gap) * D.g(am) * (1 - D.survive(am, -mb))))
        return out

    def a_age(self, var, cid, cand):
        c = self.C[cid]
        m, f = self.P[c.m], self.P[c.f]
        o = f if f.born is None else m
        yb = cand[1]
        for k in c.kids:
            a = self.P[k].born - yb
            if not ((15 <= a <= 47) if o is m else (16 <= a <= 72)):
                return {self.P[k].psrc, self.P[k].bsrc}, None
        t = self.trail
        t.set(o, "born", yb)
        t.set(o, "bsrc", var.id)
        t.set(o, "age", -yb)
        new = []
        if o.kind in ("anc", "ghost") and yb >= -self.span:
            new.append(Var(f"par:{o.id}", (2, -yb, o.id, 0)))
        return None, new

    # deaths
    def bounds(self, q):
        p = self.P[q]
        lo = p.born + (16 if p.unions else 0)                    # a spouse lived to marry, and the other was of age
        for cid in p.unions:
            o = self.P[self.C[cid].m if self.C[cid].f == q else self.C[cid].f]
            if o.born is not None:
                lo = max(lo, o.born + 15)
            c = self.C[cid]
            for k in c.kids:
                lo = max(lo, self.P[k].born - (1 if c.f == q else 0))
        hi, why = -1, set()
        for cid in p.unions:
            c = self.C[cid]
            if c.ghost:
                other = self.P[c.ghost]
                li = [k for u_ in other.unions if self.C[u_].ghost != other.id for k in self.C[u_].kids]
                if li:
                    z = min(li, key=lambda k: self.P[k].born)
                    hi = min(hi, self.P[z].born - 1)
                    why |= {self.P[z].psrc}
        return lo, hi, why

    def c_death(self, q):
        p = self.P[q]
        lo, hi, _ = self.bounds(q)
        s0 = D.S(lo - p.born)
        return [(("death", y), D.death_w(y - p.born, y, self.hard) / max(s0, 1e-12)) for y in range(lo, hi + 1)]

    def a_death(self, var, q, cand):
        p = self.P[q]
        lo, hi, why = self.bounds(q)
        y = cand[1]
        if not lo <= y <= hi:
            kids = [k for c in p.unions for k in self.C[c].kids]
            return why | {self.P[k].psrc for k in kids}, None
        a = y - p.born
        childbed = p.sex == "f" and any(self.P[k].born == y for k in self.kids_of_mother(q))
        self.trail.set(p, "died", y)
        self.trail.set(p, "cause", D.cause(a, y, self.hard, childbed))
        return None, []

    # the children not living now, and the marriage
    def c_fill(self, cid):
        return [(("fill", self.fill_plan(cid)), 1.0)]

    def fill_plan(self, cid):
        c = self.C[cid]
        m, f = self.P[c.m], self.P[c.f]
        K = sorted(self.P[k].born for k in c.kids)
        if c.res == "OFF" or m.born is None or f.born is None:
            return ()
        first = K[0] if K else None
        lo = max(m.born + 15, f.born + 16)
        if not c.ghost:                                          # a living union comes after a dead spouse's death
            for q in (c.f, c.m):
                for u_ in self.P[q].unions:
                    g_ = self.C[u_]
                    if g_.ghost == q:
                        dead = self.P[g_.m if g_.f == q else g_.f].died
                        if dead is not None:
                            lo = max(lo, dead)
        hi = (first - 1) if first is not None else min(0, m.born + 40)
        hi = min([hi] + [q.died for q in (m, f) if q.died is not None])  # married while both were alive
        ws = [(y, D.first_marriage(y - m.born) * D.married_share(y - m.born) + 1e-6) for y in range(lo, max(lo, hi) + 1)]
        wed = order(self.seed, ("wed", cid), ws)[0] if ws else lo
        end = min(0 if m.died is None else m.died, 0 if f.died is None else f.died + 1, m.born + 47)
        others = [self.P[k].born for q in (c.f, c.m) for u_ in self.P[q].unions if u_ != cid for k in self.C[u_].kids]
        if c.ghost:                                              # a dead spouse's union ends before the living one's children
            later = [y for y in others if y > (first if first is not None else wed)]
            if later:
                end = min(end, min(later) - 1)
        K = sorted({self.P[k].born for k in self.kids_of_mother(c.m)})   # the mother's children by any union block their years
        out = [("wed", wed)]
        last = None
        for y in range(wed + 1, end + 1):
            if y in K:
                last = y
                continue
            gapb = 99 if last is None else y - last
            ahead = min([k - y for k in K if k > y] or [99])
            sp = (0 if min(gapb, ahead) < 1 else 0.3 if min(gapb, ahead) == 1 else 1)
            a_now = -y
            q_dead = 1 - D.S(a_now)
            q_left = 0.25 if self.off and a_now >= 18 else 0.0
            gone = q_dead + (1 - q_dead) * q_left
            if u(self.seed, "fill", cid, y) < D.fert(y - m.born) * sp * gone:
                sex = "m" if u(self.seed, "fsex", cid, y) < .5 else "f"
                if u(self.seed, "ffate", cid, y) < q_dead / gone:
                    ds = [(z, D.death_w(z - y, z, self.hard)) for z in range(y, 0)]
                    z = order(self.seed, ("fdie", cid, y), ds)[0]
                    out.append(("died", y, sex, z))
                else:
                    z = y + 16 + int(u(self.seed, "fleft", cid, y) * min(14, max(1, -y - 16)))
                    out.append(("left", y, sex, min(z, -1)))
                last = y
        return tuple(out)

    def a_fill(self, var, cid, cand):
        c = self.C[cid]
        t = self.trail
        for e in cand[1]:
            if e[0] == "wed":
                t.set(c, "wed", e[1])
                continue
            fate, y, sex, z = e
            k = P(f"{cid}~{y}", sex, y, var.id, "fill")
            t.put(self.P, k.id, k)
            t.set(k, "pc", cid)
            t.set(k, "psrc", var.id)
            t.push(c.kids, k.id)
            if fate == "died":
                t.set(k, "died", z)
                t.set(k, "cause", D.cause(z - y, z, self.hard))
            else:
                t.set(k, "fate", ("left", z))
        return None, []

    # ------------------------------------------------------------------ the result
    def export(self) -> dict:
        """The common form stats.py reads (as forward.truth gives it)."""
        out = {}
        for i, p in self.P.items():
            c = self.C.get(p.pc) if p.pc else None
            bi = "before" if p.born is not None and p.born < -self.span and not c else ("came" if p.came else (c.res if c else None))
            out[i] = {"sex": p.sex, "born": p.born, "died": p.died, "left": p.fate[1] if p.fate else None,
                      "father": c.f if c else None, "mother": c.m if c else None, "present": p.kind == "present",
                      "village": p.village, "hh": p.hh, "born_in": bi, "kind": p.kind}
        unions = [{"f": c.f, "m": c.m, "res": c.res, "wed": c.wed} for c in self.C.values()]
        return {"P": out, "unions": unions, "founded": dict(self.F), "span": self.span}
