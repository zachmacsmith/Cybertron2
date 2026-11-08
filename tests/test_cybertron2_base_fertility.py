"""The land's base fertility (D4-112): every level the soil comes back toward is the table's times the parcel's base, so dung
raises poor ground by a share of what it can be; a world without `land` is as before."""
from cybertron2.capacity import rotation as RO
from cybertron2.engine import farm as FM
from cybertron2.engine.data import PHYSICS

F = PHYSICS["farming"]


def test_dung_cannot_make_poor_ground_rich():
    sand, plain = 0.3, 1.3
    s, p = sand, plain
    for _ in range(200):
        s, p = FM.manure_gain(F, s, base=sand), FM.manure_gain(F, p, base=plain)
    level = float(F["manure"][1])
    assert abs(s - level * sand) < 1e-3 and abs(p - level * plain) < 1e-3        # each to its own ceiling: the same share
    assert FM.manure_gain(F, 0.5) == FM.manure_gain(F, 0.5, base=1.0)             # base 1.0 is the old rule


def test_rest_and_crops_come_back_toward_the_base():
    f = 0.1
    for _ in range(400):
        f = FM.fallow_gain(F, f, 8, base=0.6)
    assert abs(f - 0.6) < 1e-3
    assert FM.soil_step(F, 0.9, "beans", base=1.0) == FM.soil_step(F, 0.9, "beans")


def test_the_parcels_base_and_the_capacity_model_scale_together():
    assert FM.base({}) == 1.0 and FM.base({"land": {"base_fertility": 0.4}}) == 0.4
    a = RO.best_year((0, 24), 32, _level(), base=1.0)
    b = RO.best_year((0, 24), 32, _level(), base=0.5)
    assert abs(b.fertility - 0.5 * a.fertility) < 1e-3                            # the soil rules are linear: the steady soil scales


def _level():
    from cybertron2.capacity.levels import LEVELS
    return LEVELS["worked"]
