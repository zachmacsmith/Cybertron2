import copy, json, pickle, numpy as np, kinds0, calibrate as C, rounds as R
CORE = ["red deer", "roe deer", "wild boar", "brown hare", "mountain hare", "voles and mice", "red grouse", "badger", "fox", "wolf",
        "beaver", "otter", "eel", "wildfowl", "rats"]
if __name__ == "__main__":
    kinds = {n: copy.deepcopy(kinds0.KINDS[n]) for n in CORE}
    fitted, hist = C.fit(kinds, iters=7, years=50)
    pickle.dump(fitted, open("kinds_r1.pkl", "wb"))
    print("fitted factors:", {n: round(fitted[n]["k"] / kinds[n]["k"], 2) for n in fitted if fitted[n]["migrant"] is None})
    res = R.evaluate(fitted, R.ALL, years=60)
    summ = R.summary(res, fitted)
    print(f"\n{'kind':16s} habitat-worlds persists rel(med) year-CV between-CV")
    for n, s in summ.items():
        f = lambda x, p=2: "  -  " if x is None else f"{x:.{p}f}"
        print(f"{n:16s} {s['worlds_with_habitat']:5d}  {f(s['persists'])}  {f(s['rel_median'])}  {f(s['year_cv'])}  {f(s['between_worlds_cv'])}")
    json.dump({"summary": summ, "res": {w: {k: v for k, v in r.items()} for w, r in res.items()}}, open("round1.json", "w"), default=float)
