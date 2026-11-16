"""02zzm: the fish keeping check for brief 5 (OPEN Q-54, D2-211; 16 Nov). Run: python3 docs/review/37_growth/02zzm_fish_keeping_cal.py
                                                                                     Calibration check for fresh fish spoilage (OPEN Q-54): a run season at one village under brief 5's D2-210 caps.
Engine numbers (ecology-water 469d7f7): spoil in a store = base x house_spoil 0.3 x keep (bins 0.5); in the open x2 to 2.5;
smoke racks take one batch of up to 40 over 3 nights; salting 4 fish with 1 salt; a fish is 1 food fresh, smoked or salted.
Policy: each day the catch is lifted and stored; fresh fish are eaten first (the village's daily need), then one smokehouse batch
is loaded when the racks are free, then salt is used; the rest stays fresh and spoils overnight."""

RUN = {1: 1, 2: 1, 3: 1, 5: 1, 6: 1}           # five salmon nights in a window of 8 (the run thickest early and mid)
DAYS = 14


def season(cap, base, keep, salt, smokehouses=1, eat=12, open_share=0.0):
    fresh, racks, eaten, smoked, salted, spoiled, caught = 0.0, [], 0.0, 0.0, 0.0, 0.0, 0.0
    for d in range(1, DAYS + 1):
        c = cap * RUN.get(d, 0)
        caught += c
        fresh += c
        racks = [(n - 1, q) for n, q in racks]        # batches age a night
        for n, q in racks:
            if n == 0:
                smoked += q
        racks = [(n, q) for n, q in racks if n > 0]
        e = min(eat, fresh); eaten += e; fresh -= e
        while len(racks) < smokehouses and fresh > 0:
            q = min(40.0, fresh); racks.append((3, q)); fresh -= q
        s = min(salt * 4, fresh); salted += s; fresh -= s; salt -= s / 4
        rate = base * 0.3 * keep * (1 - open_share) + base * 2.25 * open_share
        lost = fresh * min(1.0, rate); spoiled += lost; fresh -= lost
    smoked += sum(q for _, q in racks)
    kept = smoked + salted
    return {"caught": round(caught), "eaten fresh": round(eaten), "kept (smoked+salted)": round(kept),
            "spoiled": round(spoiled), "spoiled %": round(100 * spoiled / caught) if caught else 0}


if __name__ == "__main__":
    print("A full weir (30 food a night), a village of 12, five salmon nights")
    for label, kw in [("house, bins; 1 smokehouse; no salt", dict(keep=0.5, salt=0)),
                      ("house, no bins; 1 smokehouse; no salt", dict(keep=1.0, salt=0)),
                      ("house, no bins; 1 smokehouse; 10 salt", dict(keep=1.0, salt=10)),
                      ("house, no bins; 2 smokehouses; no salt", dict(keep=1.0, salt=0, smokehouses=2)),
                      ("left in the open half the time; 1 smokehouse", dict(keep=1.0, salt=0, open_share=0.5))]:
        print(f"  {label}")
        for base in (0.30, 0.35, 0.40, 0.50):
            print(f"    base {base:.2f}: {season(30, base, **kw)}")
    print("One section (10 food a night), house without bins, no smokehouse (rack only), no salt")
    for base in (0.30, 0.35, 0.40, 0.50):
        print(f"    base {base:.2f}: {season(10, base, keep=1.0, salt=0, smokehouses=0)}")
