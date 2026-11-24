"""Keyed draws (D2-70): every random choice is a hash of the world's seed and the decision's own key, so the same key gives the
same draw whatever else changed, and a decision's candidates keep their relative order when other candidates come or go."""
from __future__ import annotations

import hashlib
import math


def u(*key) -> float:
    """A uniform draw in (0, 1) fixed by the key."""
    h = hashlib.blake2b("\x1f".join(map(str, key)).encode(), digest_size=8).digest()
    return (int.from_bytes(h, "big") + 0.5) / 2.0 ** 64


def order(seed, var_id, cands):
    """Candidates [(key, weight)] in a keyed weighted order (Efraimidis and Spirakis): each candidate's score is log(u) / w, and
    the highest comes first. The first is a draw with probability proportional to weight; the whole order is a weighted draw
    without replacement. Candidates of weight 0 are left out (the model says they cannot happen)."""
    scored = [(math.log(u(seed, var_id, repr(k))) / w, k) for k, w in cands if w > 0]
    scored.sort(key=lambda t: (-t[0], repr(t[1])))
    return [k for _, k in scored]


def pick(seed, key, cands):
    """One keyed weighted draw from [(value, weight)]; None if nothing has weight."""
    o = order(seed, key, cands)
    return o[0] if o else None
