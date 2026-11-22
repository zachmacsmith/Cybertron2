# Wave 2 calculations (estimates; inputs from wave1_physical_basis.md and the notes)
F7, F15 = 1/7, 1/15
U = {"spring": 6, "summer": 7, "autumn": 6, "winter": 5}
YEAR = 8 * sum(U.values())          # a person's world year: 192
print("person-year units", YEAR, "two adults", 2 * YEAR)

def cap(h, f=F7): return h * f / 2          # capital units from real hours
def day(h): return h / 2                     # day-clock units

# --- materials, real rates (day clock)
WILD_CUT = 1.5      # bundles a unit, winter (withies note est.)
SEASON = {"winter": 1.0, "autumn": 0.8, "spring": 0.5, "summer": 0.3}
BED_CUT = 4.0
WILD_CORD = 25.0    # units a kg (35-80 h)
FLAX_SPIN = 8.0     # units a kg (15-20 h), from 8 kg retted flax
# flax: 10 kg straw -> 8 retted -> 1 cord ; straw 3-5 t/ha ; plot ~0.1 ha
for t_ha in (3000, 4000, 5000):
    m2_per_kg = 10 / (t_ha / 10000)
    print(f"flax straw {t_ha} kg/ha: {m2_per_kg:.0f} m2 a kg of cord; a plot (0.1 ha) gives {t_ha*0.1/10:.0f} kg cord, {t_ha*0.1/10*FLAX_SPIN:.0f} units to spin")
# pulling 15-25 person-days of 10 h a ha (fibre note)
for kg in (1, 2, 3):
    area = kg * 10 / 4000 * 1e4  # m2 at 4 t/ha
    pull_h = (20 * 10) * area / 1e4
    print(f"cord {kg} kg: close {area:.0f} m2; pull {pull_h:.1f} h; sow+weed ~{area/1e4*40:.1f} h; ret lay+lift 2 units; spin {kg*FLAX_SPIN:.0f} units")

# --- gear table: (name, real hours each, batch at 1/7, materials)
gear = {
 "wicker trap": (6, 0.45, "withies"),
 "creel": (6, 0.25, "withies"),
 "gill net": (50, 1.0, "cord"),
 "fowling net": (60, 0.8, "cord"),
 "dip net": (3.5, 0.1, "cord"),
 "hand line": (1.5, 0.02, "cord"),
 "set line": (9, 0.3, "cord"),
 "fishing rod": (1.5, 0.1, "withies"),
 "hurdle": (3.0, 1.0, "withies"),
 "smoke racks (a set)": (8, 2.0, "withies"),
 "pack basket": (8, 0.4, "withies"),
 "frame": (9, 0.5, "leather"),
 "harness": (13, 1.5, "leather"),
 "shoes (a pair)": (4, 0.5, "leather"),
 "basket": (6, 0.3, "withies"),
 "sack": (4, 0.6, "cord"),
 "chest": (22, 4.0, "timber"),
 "keep box": (9, 1.0, "withies"),
}
print()
for k, (h, m, mat) in gear.items():
    print(f"{k:22s} real {h:5.1f} h  1/7 {cap(h):.2f}  1/15 {cap(h,F15):.2f}   {m} {mat}")

# --- wild willow supply vs village demand (Eelmouth-like: fen 3 units of size, two bank parcels)
K = {"fen": 60, "bank": 20}
supply = 3 * K["fen"] + 2 * K["bank"]
hh = 3
demand = {
 "traps (12 a household, 6 replaced a year)": hh * 6 * 0.45,
 "creels, rods, baskets, pack baskets": hh * (0.06 + 0.02 + 0.3 + 0.16),
 "smoke racks (a set a household, 5 years)": hh * 2 / 5,
 "wattle houses' upkeep (1 a level, ~1.5 a year)": hh * 1.5,
 "rebuilding wattle houses (35 each, 30 years)": hh * 35 / 30,
 "weir, 1 wattle first + 3 added (6 a section a year)": 4 * 6,
 "hurdles for folds or a bed fence (share)": 3,
}
tot = sum(demand.values())
print()
for k, v in demand.items(): print(f"  {k}: {v:.1f}")
print(f"village withies a year {tot:.0f}; wild supply (stools at full) {supply}; wild cutting units at winter rate {tot/WILD_CUT:.0f}; from a bed {tot/BED_CUT:.0f}; beds needed {tot/30:.1f}")
print(f"  a village with one bank parcel only: supply {K['bank']}")

# --- fisher household, a world year in steady state (two adults, 384 units), wild and flax paths
def year(path):
    cut = WILD_CUT * 0.9 if path == "wild" else BED_CUT    # wild: mostly winter, a little autumn
    cordu = WILD_CORD if path == "wild" else FLAX_SPIN + 2.0  # flax: spin + a share of growing (sow, pull, ret ~2 a kg for 1-2 kg)
    rows = {}
    w = 6 * 0.45 + 0.06 + 0.02 + 0.3 + 0.16 + 0.4 + 1.5   # traps, creel, rod, baskets, pack basket, racks share, house upkeep
    rows["withies cut"] = w / cut
    rows["traps made (6)"] = 1 + 2      # one act of a line at the floor... 6 for 3 units
    rows["net: half a net of netting"] = 3.5 / 2
    rows["net: mend and bark"] = 0.5 + 0.5
    cord = 0.5 + 0.04 + 0.02
    rows["cord (net, lines)"] = cord * cordu
    rows["lines, rod (made)"] = 1
    rows["creel, pack basket, baskets (made)"] = 0.2 + 0.4 + 0.5
    rows["racks (a set in 5 years)"] = 0.2
    rows["house upkeep, rethatch, rebuild share"] = 3.9
    return rows
for p in ("wild", "flax"):
    r = year(p); t = sum(r.values())
    print(f"\n{p}: " + "; ".join(f"{k} {v:.1f}" for k, v in r.items()))
    print(f"  making and mending {t:.1f} units = {100*t/384:.1f}% of 384 (part 1 §5.1: {'32 (8%)' if p=='wild' else '20 (5%)'})")

# --- from scratch, first year: 12 traps, a gill net, creel, rod and 2 lines, pack basket, a set of racks
first = {"withies": 12*0.45 + 0.25 + 0.1 + 0.4 + 2.0, "cord": 1.0 + 0.04}
mk = 6 + 3.5 + 0.5 + 0.2 + 0.4 + 1 + 1   # traps 2 lines (3+3), net, creel, rod+lines, pack basket(1), racks(1)
print(f"\nfirst year: withies {first['withies']:.1f} bundles, cord {first['cord']:.2f} kg, making {mk:.1f} units")
for p, cu in (("wild", WILD_CORD), ("flax", FLAX_SPIN)):
    cut_summer = first["withies"] / (WILD_CUT * SEASON["summer"])
    cut_winter = first["withies"] / WILD_CUT
    print(f"  {p}: cord {first['cord']*cu:.0f} units; withies wild in winter {cut_winter:.1f}, in summer {cut_summer:.1f}")

# --- tanner's year
print()
for hides in (10, 20, 30):
    bark = 2 * hides
    peel = bark / 1.5
    handle = 1.5 * hides
    pits = 3
    print(f"tanner {hides} hide units: bark {bark} bundles ({bark*10} kg), peeling {peel:.0f} units, handling {handle:.0f}, pits ~{pits}; "
          f"total {peel+handle+3:.0f} units = {100*(peel+handle+3)/192:.0f}% of one person; leather {3*hides} kg")
# peeling window
for nights in (3, 6):
    print(f"peeling window {nights} nights: one peeler at 6 units a day gives {nights*6*1.5:.0f} bundles, enough for {nights*6*1.5/2:.0f} hide units")
# leather demand of a village of 12: shoes
for life_days in (90, 180):
    wd = life_days / 11.4
    pairs = 12 * 32 / wd
    print(f"shoes lasting {life_days} real days of wear = {wd:.1f} world days: a village of 12 wears {pairs:.0f} pairs a world year, {pairs*0.5:.0f} kg leather = {pairs*0.5/3:.1f} hide units")
