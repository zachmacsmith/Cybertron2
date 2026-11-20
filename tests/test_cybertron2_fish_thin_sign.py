"""Sign 9 of the signs pass (17 Nov): a water's resident fish thinning or plenty is read from its stock (one per water body, D2-229)."""
from types import SimpleNamespace

from cybertron2.engine import signs as SG


def _rows(r):
    x = SimpleNamespace(r=lambda key: r if key == "fish" else None, nm="the Mere", season="summer", snow=False)
    out = []
    for row in SG.WILD:
        try:
            ok = row["when"](x)
        except (AttributeError, KeyError, TypeError):
            continue
        if ok and "fish" in (row.get("land") or ("",))[0]:
            out.append((row["land"][1], row["text"](x), row.get("knack")))
    return out


def test_thin_fish_is_seen_and_read_by_anglers():
    got = _rows(0.2)
    assert ("thin", "the water at the Mere is quiet: few fish rising", None) in got
    assert any(k == "angle" and s == "thin" for s, _, k in got)


def test_plenty_and_middling():
    assert [s for s, _, _ in _rows(0.9)] == ["good"]
    assert _rows(0.5) == []
