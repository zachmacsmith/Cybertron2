"""Review 38.70: Twin Hollows run 1 (runs/pw1_opus_sonnet_r1): each people's living numbers by day, from the dawn checkpoints.
A person counts for the people of their household's model (agents: their model; children: their household's)."""
import json, sqlite3, zlib, csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
RUN = "/home/user/cybertron2/runs/pw1_opus_sonnet_r1/run.db"
con = sqlite3.connect(f"file:{RUN}?mode=ro", uri=True)
model_of = {"Hale": "Opus (Ashford)", "Reed": "Opus (Ashford)", "Marsh": "Sonnet (Brockley)", "Wynn": "Sonnet (Brockley)"}
rows = []
for d in range(0, 101):
    r = con.execute("select z from checkpoints where step=? order by attempt desc limit 1", (f"d{d}.dawn",)).fetchone()
    if not r:
        continue
    w = json.loads(zlib.decompress(r[0]))["world"]
    hh = {m: h for h, i in w["institutions"].items() for m in i.get("members", [])}
    c = {"Opus (Ashford)": [0, 0], "Sonnet (Brockley)": [0, 0]}
    for n, p in w["people"].items():
        if not p.get("alive"):
            continue
        k = model_of.get(hh.get(n))
        if not k:
            k = "Opus (Ashford)" if "opus" in str(p.get("model")) else "Sonnet (Brockley)"
        c[k][0] += 1
        c[k][1] += p.get("stage") in ("youth", "adult")
    rows.append({"day": d, **{f"{k} alive": v[0] for k, v in c.items()}, **{f"{k} youth+adult": v[1] for k, v in c.items()}})
with open("population.csv", "w", newline="") as f:
    wr = csv.DictWriter(f, fieldnames=list(rows[0])); wr.writeheader(); wr.writerows(rows)
fig, ax = plt.subplots(figsize=(10, 5))
for k, col in (("Opus (Ashford)", "#d1495b"), ("Sonnet (Brockley)", "#2a78d6")):
    ax.plot([r["day"] for r in rows], [r[f"{k} alive"] for r in rows], color=col, lw=2.2, label=f"{k}: alive")
    ax.plot([r["day"] for r in rows], [r[f"{k} youth+adult"] for r in rows], color=col, lw=1.2, ls="--", label=f"{k}: youths and adults")
ax.axvspan(36, 50, color="#bbb", alpha=0.25, lw=0)
ax.text(43, 1, "winter famine", ha="center", fontsize=8, color="#555")
ax.set_xlabel("day"); ax.set_ylabel("people"); ax.set_ylim(0, None)
ax.set_title("Twin Hollows, run 1: each people's numbers (Opus against Sonnet, the rival aim)", loc="left", fontsize=11)
ax.legend(frameon=False, fontsize=8); ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig("population.png", dpi=140)
print(rows[0], rows[-1], max(rows, key=lambda r: r["Opus (Ashford) alive"]))
