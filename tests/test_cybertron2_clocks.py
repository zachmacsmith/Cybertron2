"""Every rate in the data names its clock (D4-103)."""
import numbers

from cybertron2.engine import clocks as CK, data as D

RATE_NAMES = ("spoil", "r", "grow", "regrow", "rot", "shed", "births", "p", "cold", "rate", "fallow", "window", "nights", "gale",
              "grass_r", "stray", "in_milk_share", "dung", "survive", "abs", "share", "life", "wear", "starve_nights", "hungry_milk")


def _walk(o, path):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from _walk(v, path + [str(k)])
    elif isinstance(o, numbers.Number) and not isinstance(o, bool):
        yield ".".join(path)


def test_every_rate_names_its_clock():
    missing = []
    for t in ("ITEMS", "PHYSICS", "FORESTS", "CROPS", "DECAY", "RESOURCES", "TECHNIQUES"):
        for path in _walk(getattr(D, t), [t]):
            last = path.split(".")[-1]
            if last in RATE_NAMES and CK.clock_of(path) is None:
                missing.append(path)
    assert not missing, f"rates with no clock (engine/clocks.py RATES): {missing}"


def test_per_night():
    class W:
        def year_days(self):
            return 32
    assert CK.per_night(0.5, "day", W()) == 0.5 and abs(CK.per_night(32, "year", W()) - 1.0) < 1e-12
