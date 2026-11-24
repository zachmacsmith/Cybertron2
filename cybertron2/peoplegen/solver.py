"""A graph of keyed decisions, filled in order, repaired by conflict-directed backjumping, never rejected (generation_redesign.md
§4.5).

A problem gives decisions (vars) with a priority; for each, its candidates with the forward model's weights; and `apply`, which
either makes the choice (recording each change on a trail so it can be undone, and returning any new decisions the choice opens)
or says which earlier decisions it conflicts with. The solver:

- orders each decision's candidates by a keyed weighted draw (keyed.order), so the first candidate that fits is a draw from the
  forward model restricted to what fits, and the same seed and pins give the same world;
- puts the previous world's choice first, where it is still a candidate (a soft pin: stability under edits);
- on a decision with no candidate that fits, jumps back to the latest decision in its conflict set (not merely the last one made),
  undoing everything after it, and tries that decision's next candidate;
- refuses only when the conflict set holds nothing but pins, and then names them.
"""
from __future__ import annotations

import heapq
import time

from .keyed import order


class Var:
    __slots__ = ("id", "prio", "pin")

    def __init__(self, id, prio, pin=None):
        self.id, self.prio, self.pin = id, prio, pin

    def __lt__(self, o):
        return (self.prio, self.id) < (o.prio, o.id)


class Trail(list):
    """Every change to the state, as a function that undoes it."""

    def set(self, o, k, v):
        old = getattr(o, k)
        self.append(lambda: setattr(o, k, old))
        setattr(o, k, v)

    def push(self, lst, x):
        lst.append(x)
        self.append(lst.pop)

    def put(self, d, k, v):
        d[k] = v
        self.append(lambda: d.pop(k))

    def undo(self, mark):
        while len(self) > mark:
            self.pop()()


class Refusal(Exception):
    def __init__(self, var, pins, why):
        super().__init__(f"{var}: cannot be met; the pins in conflict: {sorted(pins)} ({why})")
        self.var, self.pins, self.why = var, sorted(pins), why


def is_pin(x):
    return x.startswith("pin:")


class Frame:
    __slots__ = ("var", "cands", "i", "mark", "agenda", "cs", "weights")

    def __init__(self, var, cands, mark, agenda, weights):
        self.var, self.cands, self.i, self.mark, self.agenda, self.cs, self.weights = var, cands, 0, mark, agenda, set(), weights


def solve(problem, seed, prev=None, max_steps=200000):
    """Fill every decision. Returns (assignment {var id: choice}, stats). The problem's state holds the world afterwards."""
    prev = prev or {}
    trail = problem.trail
    agenda = list(problem.initial())
    heapq.heapify(agenda)
    stack, assign = [], {}
    st = {"decisions": 0, "checks": 0, "rejected": 0, "backjumps": 0, "max_jump": 0, "undone": 0, "soft_kept": 0, "soft_moved": 0,
          "steps": 0, "shares": {}, "forced": {}}
    t0 = time.time()

    def open_frame(var):
        cw = problem.cands(var)
        if var.pin is not None:
            keys = [var.pin]
        else:
            keys = order(seed, var.id, cw)
            p = prev.get(var.id)
            if p is not None and p in keys:
                keys.remove(p)
                keys.insert(0, p)
        f = Frame(var, keys, len(trail), list(agenda), cw)
        stack.append(f)
        return f

    f = None
    while True:
        st["steps"] += 1
        if st["steps"] > max_steps:
            raise RuntimeError("step limit")
        if f is None:
            if not agenda:
                break
            f = open_frame(heapq.heappop(agenda))
        made = False
        while f.i < len(f.cands):
            c = f.cands[f.i]
            f.i += 1
            st["checks"] += 1
            conflict, new = problem.apply(f.var, c)
            if conflict is None:
                assign[f.var.id] = c
                for v in new or ():
                    heapq.heappush(agenda, v)
                made = True
                break
            st["rejected"] += 1
            f.cs |= conflict
        if made:
            st["decisions"] += 1
            f = None
            continue
        f.cs |= problem.blame(f.var)
        cs = f.cs - {f.var.id}                                   # no candidate fits: jump to the latest decision in conflict
        ids = [g.var.id for g in stack[:-1]]
        target = next((k for k in range(len(stack) - 2, -1, -1) if stack[k].var.id in cs and stack[k].var.pin is None), None)
        if target is None:
            pins = {x for x in cs if is_pin(x)} | {x for x in cs if x in ids and stack[ids.index(x)].var.pin is not None}
            if f.var.pin is not None:
                pins.add(f.var.id)
            raise Refusal(f.var.id, pins, "no candidate fits" if f.cands else "no candidates")
        st["backjumps"] += 1
        st["max_jump"] = max(st["max_jump"], len(stack) - 1 - target)
        for g in stack[target + 1:]:
            assign.pop(g.var.id, None)
        st["undone"] += len(stack) - 1 - target
        g = stack[target]
        del stack[target + 1:]
        trail.undo(g.mark)
        assign.pop(g.var.id, None)
        agenda[:] = g.agenda
        g.cs |= cs - {g.var.id}
        f = g
    for g in stack:                                              # how likely each choice was among its candidates
        if g.var.id in assign and g.weights:
            tot = sum(w for _, w in g.weights)
            cls = problem.klass(assign[g.var.id])
            share = sum(w for k, w in g.weights if problem.klass(k) == cls) / tot if tot > 0 else 1.0
            st["shares"][g.var.id] = share
            wk = dict(g.weights)
            ruled = sum(wk.get(k, 0) for k in g.cands[:g.i - 1]) / tot if tot > 0 else 0.0
            if ruled > 0:
                st["forced"][g.var.id] = round(ruled, 4)              # the model's weight the constraints ruled out before the choice
        p = prev.get(g.var.id)
        if p is not None:
            st["soft_kept" if p == assign.get(g.var.id) else "soft_moved"] += 1
    st["seconds"] = round(time.time() - t0, 3)
    return assign, st
