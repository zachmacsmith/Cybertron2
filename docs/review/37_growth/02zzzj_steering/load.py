"""Load the replies of past runs from their published journals (Hugging Face dataset zachmacsmith/cybertron2-runs, read only).

Each row: run, key, kind (decision, evening, talk, ...), agent, day, model, parsed reply, and the system text, message and schema
by their blob sha (read lazily). The journals are read from the local copies named in ROOTS (the dataset's own files, unchanged).
"""
import json, os, zlib, functools
import pandas as pd

SCR = "/tmp/claude-0/-home-user/7e098288-bcf5-5d91-98fd-74db17ae2c32/scratchpad"
ROOTS = [f"{SCR}/eval/data/runs", f"{SCR}/w84/hf/runs"]
# the runs read, all with `view: beliefs` but pw1 (the old prompt, with the options list), and their export dates
RUNS = {"water_runs_models_r1": "20 Nov", "water_lake_r2": "17 Nov", "water_lake_r1": "16 Nov", "pw1_opus_sonnet_r1": "13 Nov",
        "e2_labour": "8 Nov", "p1_brookend": "8 Nov", "orwell": "7 Nov", "takeover": "7 Nov", "f1_frontier": "4 Nov",
        "wb2_wenbridge": "4 Nov", "c3_combe_rich": "4 Nov", "violent_opus": "7 Nov"}


def path(run):
    for r in ROOTS:
        p = f"{r}/{run}/journal"
        if os.path.exists(f"{p}/requests.parquet") and os.path.exists(f"{p}/blobs.parquet"):
            return p
    return None


@functools.lru_cache(maxsize=None)
def blobs(run):
    b = pd.read_parquet(f"{path(run)}/blobs.parquet")
    return dict(zip(b.sha, b.z))


def blob(run, sha):
    z = blobs(run).get(sha)
    return None if z is None else zlib.decompress(z).decode()


@functools.lru_cache(maxsize=None)
def rows(run):
    p = path(run)
    q = pd.read_parquet(f"{p}/requests.parquet")
    r = pd.read_parquet(f"{p}/responses.parquet")
    q = q.sort_values("attempt").drop_duplicates("key", keep="last")
    d = q.merge(r[["key", "parsed", "usage"]], on="key", how="left")
    out = []
    for x in d.itertuples():
        try:
            rep = json.loads(x.parsed) if isinstance(x.parsed, str) else (x.parsed or {})
        except Exception:
            rep = {}
        day = int(x.key.split(".")[0][1:]) if x.key.startswith("d") and x.key.split(".")[0][1:].isdigit() else None
        out.append({"run": run, "key": x.key, "kind": x.kind, "agent": x.agent, "day": day,
                    "model": (x.responder or "").split(":", 1)[-1], "reply": rep if isinstance(rep, dict) else {},
                    "system_sha": x.system_sha, "message_sha": x.message_sha, "schema_sha": x.schema_sha,
                    "conversation": x.conversation, "idx": x.idx})
    return out


def available():
    return [r for r in RUNS if path(r)]
