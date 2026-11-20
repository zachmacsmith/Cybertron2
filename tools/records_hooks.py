"""Claude Code hooks for the records (D2-233, D2-235): the stop check and the commit check. Stdlib only.

stopcheck     (Stop hook) If the reply that is ending makes a promise or an offer ("I'll ...", "shall I ...", "left: ...") and no
              record changed during the turn, send it back once with the reason. Passes when a record (an item, WORK, OPEN or
              DECISIONS) was written or committed after the user's last message, after `records ack "why"`, or when the hook
              already sent this stop back once (stop_hook_active).
commit-check  (PreToolUse on Bash `git commit`) Refuse a commit whose message lacks the trailers (Agent, Thread; or a subject
              typed `upkeep`), names a thread that is not an item, or puts the trailers outside the last paragraph.
              `records commit` writes the trailers itself and is let through.
Both fail open: anything they cannot read lets the action go ahead.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import shlex
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
C2 = os.path.join(ROOT, "docs", "cybertron2")
RECORD_PATHS = [os.path.join(C2, "items"), os.path.join(C2, "WORK.md"), os.path.join(C2, "OPEN.md"),
                os.path.join(C2, "DECISIONS.md")]
ACK = os.path.join(ROOT, ".git", "records-ack")

PROMISE = re.compile(
    r"(?:\bI'll\b|\bI will\b|\bI'm going to\b|\bnext,? I\b|\bshall I\b|\bshould I\b|\bwant me to\b|\bwould you like me to\b|"
    r"\bI can (?:also )?(?:add|build|write|run|do|make|fix|check)\b|^\s*(?:\*\*)?(?:left|still to do|to do next|owed)(?:\*\*)?:|"
    r"\bI'd (?:then|next)\b|\bonce you(?:'ve| have)? (?:answered|said|confirmed)\b)", re.I | re.M)


def _read_tail(path, size=3_000_000):
    with open(path, "rb") as f:
        f.seek(0, 2)
        n = f.tell()
        f.seek(max(0, n - size))
        data = f.read().decode("utf-8", "replace")
    lines = data.split("\n")
    return lines[1:] if n > size else lines


def _is_user_prompt(e) -> bool:
    if e.get("type") != "user" or e.get("isMeta") or e.get("isSidechain"):
        return False
    c = (e.get("message") or {}).get("content")
    if isinstance(c, str):
        return not c.startswith("<") or c.startswith("<pasted")
    if isinstance(c, list):
        return any(isinstance(x, dict) and x.get("type") == "text" for x in c) and \
            not any(isinstance(x, dict) and x.get("type") == "tool_result" for x in c)
    return False


def _last_turn(transcript):
    events = []
    for line in _read_tail(transcript):
        try:
            events.append(json.loads(line))
        except ValueError:
            continue
    start = None
    for k in range(len(events) - 1, -1, -1):
        if _is_user_prompt(events[k]):
            start = k
            break
    if start is None:
        return None, ""
    ts = events[start].get("timestamp", "")
    text = []
    for e in events[start + 1:]:
        if e.get("type") == "assistant" and not e.get("isSidechain"):
            for x in (e.get("message") or {}).get("content") or []:
                if isinstance(x, dict) and x.get("type") == "text":
                    text.append(x.get("text", ""))
    return ts, "\n".join(text)


def _epoch(ts: str) -> float:
    try:
        return dt.datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return 0.0


def _recorded_since(t0: float) -> bool:
    for p in RECORD_PATHS:
        if os.path.isdir(p):
            for n in os.listdir(p):
                if os.path.getmtime(os.path.join(p, n)) > t0:
                    return True
        elif os.path.exists(p) and os.path.getmtime(p) > t0:
            return True
    try:
        if os.path.exists(ACK) and os.path.getmtime(ACK) > t0:
            return True
    except OSError:
        pass
    return False


def stopcheck() -> int:
    try:
        hook = json.load(sys.stdin)
    except ValueError:
        return 0
    if hook.get("stop_hook_active"):
        return 0
    tp = hook.get("transcript_path")
    if not tp or not os.path.exists(tp):
        return 0
    ts, text = _last_turn(tp)
    if not text:
        return 0
    hits = [m.group(0).strip() for m in PROMISE.finditer(text)]
    if not hits:
        return 0
    if _recorded_since(_epoch(ts)):
        return 0
    quotes = []
    for h in hits[:3]:
        i = text.find(h)
        quotes.append(text[max(0, i - 40): i + 90].replace("\n", " ").strip())
    reason = ("The stop check (D2-233): this reply makes a promise or an offer, and no record changed in this turn:\n- "
              + "\n- ".join(quotes)
              + "\nRecord it with one call: a thread's next step (records set W-n next=\"...\"), an offer or promise "
                "(records new O --title \"...\" --parent W-n default=\"do it\" default_on=YYYY-MM-DD), or a deferral "
                "(records new L ...). If it is already recorded, or is not a commitment, run: "
                "python3 tools/records.py ack \"<why>\". Then end the reply.")
    print(json.dumps({"decision": "block", "reason": reason}))
    return 0


def _message_of(cmd: str):
    """The commit message a `git commit` command carries, or None if it cannot be read (then the check lets it through)."""
    m = re.search(r"<<-?\s*'?(\w+)'?\s*\n(.*?)\n\1\b", cmd, re.S)
    if m and re.search(r"-F\s*-|--file[= ]-", cmd):
        return m.group(2)
    try:
        parts = shlex.split(cmd, posix=True)
    except ValueError:
        return None
    msgs = []
    for k, p in enumerate(parts):
        if p in ("-m", "--message") and k + 1 < len(parts):
            msgs.append(parts[k + 1])
        elif p.startswith("--message="):
            msgs.append(p.split("=", 1)[1])
    return "\n\n".join(msgs) if msgs else None


def _deny(reason):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                             "permissionDecisionReason": reason}}))
    return 0


def commit_check() -> int:
    try:
        hook = json.load(sys.stdin)
    except ValueError:
        return 0
    cmd = (hook.get("tool_input") or {}).get("command", "")
    if not re.search(r"\bgit\b[^|;&]*\bcommit\b", cmd) or "records.py commit" in cmd:
        return 0
    if not os.path.isdir(os.path.join(C2, "items")):
        return 0
    msg = _message_of(cmd)
    if msg is None:
        return 0
    paras = [p for p in re.split(r"\n\s*\n", msg.strip()) if p.strip()]
    subject = paras[0].split("\n")[0] if paras else ""
    last = paras[-1] if paras else ""
    tr = dict()
    for line in last.split("\n"):
        m = re.match(r"([A-Za-z-]+):\s*(.+)", line)
        if m:
            tr.setdefault(m.group(1), []).append(m.group(2))
    elsewhere = any(re.search(r"^(Agent|Thread):", p, re.M) for p in paras[:-1])
    upkeep = subject.startswith("upkeep")
    probs = []
    if elsewhere and "Agent" not in tr:
        probs.append("the Agent/Thread trailers are not in the last paragraph, so git will not read them: put them in one "
                     "block with the Co-Authored-By and Claude-Session lines, no blank line between")
    if "Agent" not in tr and not elsewhere:
        probs.append("no `Agent:` trailer")
    if "Thread" not in tr and not upkeep and not elsewhere:
        probs.append("no `Thread:` trailer (or type the subject `upkeep ...`)")
    items = os.path.join(C2, "items")
    for t in tr.get("Thread", []):
        for i in re.split(r"[,\s]+", t.strip()):
            if i and i != "upkeep" and not os.path.exists(os.path.join(items, f"{i}.md")):
                probs.append(f"Thread {i} is not an item (records new W ... first)")
    if probs:
        return _deny("The commit check (D2-235): " + "; ".join(probs)
                     + ". Easiest: python3 tools/records.py commit -m \"<subject>\" [--thread W-n] [paths], which writes "
                       "the trailers.")
    return 0


if __name__ == "__main__":
    sys.exit({"stopcheck": stopcheck, "commit-check": commit_check}[sys.argv[1]]())
