import json, sys
for r in sys.argv[1:]:
    m = json.load(open(r + "/measure.json"))
    print("==", r)
    for k in ('alive','people','deaths','households','food_end','missed_meals','first_missed','units','build_units_by','started','finished','unfinished','fields','refused'):
        print(" ", k, m[k])
