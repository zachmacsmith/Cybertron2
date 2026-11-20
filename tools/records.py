#!/usr/bin/env python3
"""The records: one file per item, views rendered from them, and the queries agents use (D2-232 to D2-239).

Items live in docs/cybertron2/items/<ID>.md: a flat front matter (key: value; lists as JSON arrays; strings JSON-quoted when
YAML would misread them), then the body. A migrated row's body is its table cell, verbatim. OPEN.md, WORK.md and DECISIONS.md
are views: their prose is kept in docs/cybertron2/items/_views/<NAME>.md with a marker where each table's rows go, and
`render` fills them. Documents (spec, proposals, session notes) are nodes too: their metadata is read from their front matter if
they have one, else derived (title from the first heading, summary from the proposals index or a "## Summary" section).

Agents' verbs (each one call; see .claude/skills/records/SKILL.md):
  show ID | ls ID | tree ID | area NAME | find WORDS | log ID | status [--owner O] | brief | digest | pack ID...
  new KIND --title T [--owner O] [--parent P] [--text X] [field=value ...]
  set ID field=value ...  |  link ID EDGE OTHER [--reason R]  |  close ID --by agent|zach|default|relayed [--note N]
  decide --rule R --area spec/AREA.md --quote Q [--closes Q-n ...] [--replaces D-n] [--parent W-n] [--proposal FILE]
  commit -m SUBJECT [--type T] [--thread W-n] [PATH ...]   (stages the records and PATHs, writes the trailers)
  render [--check] | check [--strict] | migrate | whoami [NAME]
Hooks: brief (SessionStart), commit-check (PreToolUse on git commit), stopcheck (Stop).
Stdlib only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
C2 = os.path.join(ROOT, "docs", "cybertron2")
ITEMS = os.path.join(C2, "items")
VIEWS = os.path.join(ITEMS, "_views")
GITDIR = os.path.join(ROOT, ".git")
PENDING = os.path.join(GITDIR, "records-pending.json")
WHOAMI = os.path.join(GITDIR, "records-agent")
TODAY = dt.date.today()

ID_RE = r"(?:D\d|H|W|Q|L|O|C)-\d+[a-z]?"
KINDS = {"W": "thread", "Q": "ask", "L": "deferred", "O": "offer", "C": "conflict", "D": "decision", "H": "decision"}
EDGES = ["parent", "waits_on", "blocks", "replaces", "decides", "relates"]
BY = ["zach", "agent", "default", "relayed"]
LIST_FIELDS = set(EDGES) | {"sources", "threads", "describes", "relates_why", "builds"}
OPEN_STATES = {"thread": {"queued", "active", "waiting", "paused"}, "ask": {"open"}, "deferred": {"open"}, "offer": {"open"},
               "conflict": {"open"}, "decision": set()}
TYPES = ["design", "decide", "build", "fix", "run", "record", "upkeep"]
MONTHS = {m: i for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}

# The tables of the three views: (view, marker, columns as fields, id prefix, which items, sort direction).
TABLES = [
    ("OPEN", "conflicts", ["id", "body", "where", "resolution", "owner"], "C", lambda it: it["kind"] == "conflict", 1),
    ("OPEN", "asks", ["id", "body", "where", "owner"], "Q", lambda it: it["kind"] == "ask", 1),
    ("OPEN", "deferred", ["id", "body", "decision", "designed_in", "waits_on_text", "owner"], "L",
     lambda it: it["kind"] == "deferred", 1),
    ("OPEN", "offers", ["id", "body", "default", "default_on", "owner"], "O", lambda it: it["kind"] == "offer", 1),
    ("DECISIONS", "decisions", ["id", "date", "body", "source", "replaces_text"], "D|H", lambda it: it["kind"] == "decision", 1),
    ("WORK", "in_progress", ["id", "body", "owner", "state", "started", "touched", "where", "notes"], "W",
     lambda it: it["kind"] == "thread" and table_of(it) == "in_progress", -1),
    ("WORK", "paused", ["id", "body", "owner", "state", "started", "touched", "where", "notes"], "W",
     lambda it: it["kind"] == "thread" and table_of(it) == "paused", -1),
    ("WORK", "done", ["id", "body", "owner", "done"], "W", lambda it: it["kind"] == "thread" and table_of(it) == "done", -1),
]
VIEW_FILES = {"OPEN": os.path.join(C2, "OPEN.md"), "WORK": os.path.join(C2, "WORK.md"),
              "DECISIONS": os.path.join(C2, "DECISIONS.md")}


# ---------------------------------------------------------------------- the item format
def _needs_quote(v: str) -> bool:
    return (v == "" or v[0] in "[{\"'&*!|>%@`#-?,:" or ": " in v or " #" in v or v.strip() != v
            or v.lower() in ("yes", "no", "true", "false", "null", "on", "off") or re.fullmatch(r"[\d.\-:]+", v) is not None)


def dump_value(v) -> str:
    if isinstance(v, list):
        return json.dumps(v, ensure_ascii=False)
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return str(int(v)) if float(v).is_integer() else str(v)
    v = str(v)
    return json.dumps(v, ensure_ascii=False) if _needs_quote(v) else v


def parse_value(s: str):
    s = s.strip()
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    if s.startswith("[") or s.startswith('"'):
        try:
            return json.loads(s)
        except ValueError:
            pass
    return s


def read_item(path) -> dict:
    with open(path, encoding="utf-8") as f:
        text = f.read()
    it = {"path": path}
    m = re.match(r"---\n(.*?)\n---\n?(.*)\Z", text, re.S)
    if not m:
        it["body"] = text
        return it
    for line in m.group(1).split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            it[k.strip()] = parse_value(v)
    it["body"] = m.group(2).rstrip("\n")
    return it


HEAD_ORDER = ["id", "kind", "title", "owner", "state", "by", "created", "seq"] + EDGES + ["revisit", "next", "branch"]


def write_item(it: dict):
    keys = [k for k in HEAD_ORDER if k in it] + sorted(k for k in it if k not in HEAD_ORDER and k not in ("path", "body"))
    lines = ["---"] + [f"{k}: {dump_value(it[k])}" for k in keys if it[k] not in (None, "", [])] + ["---", it.get("body", "")]
    path = it.get("path") or os.path.join(ITEMS, f"{it['id']}.md")
    it["path"] = path
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip("\n") + "\n")


def kind_of(i: str) -> str:
    return KINDS[re.match(r"[A-Z]+", i).group(0)[0] if not i.startswith("H") else "H"]


def load_items() -> dict:
    out = {}
    if not os.path.isdir(ITEMS):
        return out
    for n in sorted(os.listdir(ITEMS)):
        if n.endswith(".md") and not n.startswith("_"):
            it = read_item(os.path.join(ITEMS, n))
            if "id" in it:
                out[it["id"]] = it
    return out


def table_of(it) -> str:
    """A thread's WORK table: the one it was recorded in, unless its state has since moved it (set and close update it)."""
    return it.get("table") or ("paused" if it.get("state") == "paused" else "done" if is_closed(it) else "in_progress")


def is_closed(it) -> bool:
    k = it.get("kind")
    if k == "decision":
        return it.get("state") == "replaced"
    return it.get("state", "open") not in OPEN_STATES.get(k, {"open"})


def iso(s: str) -> str:
    m = re.match(r"\s*(\d{1,2}) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)", s or "")
    return f"2026-{MONTHS[m.group(2)]:02d}-{int(m.group(1)):02d}" if m else ""


def num(i: str):
    m = re.match(r"([A-Z]+\d?)-(\d+)([a-z]?)", i)
    return (m.group(1), int(m.group(2)), m.group(3)) if m else (i, 0, "")


def title_of(it) -> str:
    if it.get("title"):
        return str(it["title"])
    b = re.sub(r"~~", "", it.get("body", ""))
    b = re.sub(r"^\s*\*\*\((?:Closed|Answered|Resolved)[^*]*\)\*\*\s*", "", b)
    m = re.match(r"\s*\*\*(.+?)\*\*", b)
    t = m.group(1) if m else b
    t = re.sub(r"\s+", " ", t).strip().rstrip(":;,")
    return t if len(t) <= 110 else t[:107] + "..."


# ---------------------------------------------------------------------- git
def git(*a, check=False) -> str:
    r = subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit(r.stderr.strip())
    return r.stdout


_touch_cache: dict = {}


def last_touch(path) -> str:
    """The date of the last commit touching a path (or '' if none), from one pass over the history."""
    if not _touch_cache:
        _touch_cache["__loaded__"] = "1"
        day = ""
        for line in git("log", "--format=@%ad", "--date=short", "--name-only", "--since=2026-10-01").split("\n"):
            if line.startswith("@"):
                day = line[1:]
            elif line and line not in _touch_cache:
                _touch_cache[line] = day
    return _touch_cache.get(path, "")


def branches_ahead() -> list:
    out = []
    for b in git("for-each-ref", "--format=%(refname:short)", "refs/remotes/origin").split():
        if b in ("origin/main", "origin/HEAD", "origin"):
            continue
        n = git("rev-list", "--count", f"origin/main..{b}").strip()
        if n and int(n) > 0:
            out.append((b.replace("origin/", ""), int(n), git("log", "-1", "--format=%ad", "--date=short", b).strip()))
    return out


# ---------------------------------------------------------------------- documents as nodes
DOC_DIRS = [("spec", os.path.join(C2, "spec")), ("proposal", os.path.join(C2, "proposals")),
            ("note", os.path.join(ROOT, "docs", "review", "37_growth")),
            ("note", os.path.join(ROOT, "docs", "review", "38_space_engine"))]
_docs_cache = None


def load_docs() -> dict:
    global _docs_cache
    if _docs_cache is not None:
        return _docs_cache
    index = {}
    pr = os.path.join(C2, "proposals", "README.md")
    if os.path.exists(pr):
        for line in open(pr, encoding="utf-8"):
            m = re.match(r"\| \[([^\]]+\.md)\]\([^)]*\) \| (.*?) \| (.*?) \| (.*?) \|", line)
            if m:
                index[m.group(1)] = (m.group(2), m.group(3), m.group(4))
    docs = {}
    for kind, d in DOC_DIRS:
        for dirpath, _, files in os.walk(d):
            for n in files:
                if not n.endswith(".md") or n == "README.md":
                    continue
                p = os.path.join(dirpath, n)
                rp = os.path.relpath(p, ROOT)
                text = open(p, encoding="utf-8").read()
                it = read_item(p) if text.startswith("---\n") else {"body": text}
                body = it["body"]
                h = re.search(r"^# (.+)$", body, re.M)
                doc = {"id": rp, "kind": it.get("kind", kind), "path": p, "body": body,
                       "title": it.get("title") or (h.group(1).strip() if h else n)}
                if it.get("summary"):
                    doc["summary"] = it["summary"]
                elif kind == "proposal" and n in index:
                    doc["summary"], doc["owner"], doc["state"] = index[n]
                else:
                    s = re.search(r"^## Summary\n+(.+?)(?:\n\n|\Z)", body, re.M | re.S)
                    doc["summary"] = re.sub(r"\s+", " ", s.group(1)).strip()[:300] if s else ""
                if kind == "proposal" and "state" not in doc:
                    st = re.search(r"^\*\*Status:\*\*\s*(.+)$", body, re.M)
                    doc["state"] = st.group(1).strip()[:80] if st else ""
                if kind == "spec":
                    doc["area"] = os.path.relpath(p, os.path.join(C2, "spec"))[:-3]
                for k in ("threads", "describes", "reviewed", "area", "owner"):
                    if it.get(k):
                        doc[k] = it[k]
                docs[rp] = doc
    _docs_cache = docs
    return docs


# ---------------------------------------------------------------------- the web
class Web:
    def __init__(self):
        self.items = load_items()
        self.docs = load_docs()
        self.mentions: dict = {}  # id -> set of node ids whose text mentions it
        for nid, n in list(self.items.items()) + list(self.docs.items()):
            for m in set(re.findall(r"\b(" + ID_RE + r")\b", n.get("body", "") + " " + json.dumps(
                    {k: v for k, v in n.items() if k not in ("body", "path")}, ensure_ascii=False))):
                if m != nid:
                    self.mentions.setdefault(m, set()).add(nid)
        self.children: dict = {}
        for i, it in self.items.items():
            for p in as_list(it.get("parent")):
                self.children.setdefault(p, []).append(i)

    def node(self, i):
        return self.items.get(i) or self.docs.get(i) or self.docs.get(_doc_key(i, self.docs))

    def line(self, i, edge="") -> str:
        n = self.node(i)
        if not n:
            return f"  {edge:<10}{i}  (not found)"
        st = n.get("state", "")
        by = f" by {n['by']}" if n.get("by") and n.get("by") != "zach" and is_closed(n) else ""
        rev = "  revisit" if n.get("revisit") else ""
        return f"  {edge:<10}{i}  {n.get('kind', '')} {st}{by}  \"{title_of(n)}\"{rev}  [{updated(n)}]"

    def area_of(self, i) -> list:
        """The spec files that cite a decision (its area), or the area field."""
        n = self.node(i) or {}
        if n.get("area"):
            return as_list(n["area"])
        return sorted(self.docs[x]["area"] for x in self.mentions.get(i, ()) if x in self.docs and self.docs[x].get("area"))


def _doc_key(i, docs):
    for k in docs:
        if k.endswith("/" + i) or k.endswith("/" + i + ".md") or os.path.basename(k) == i:
            return k
    return None


def as_list(v) -> list:
    if v in (None, ""):
        return []
    return v if isinstance(v, list) else [x.strip() for x in str(v).split(",") if x.strip()]


def updated(n) -> str:
    return last_touch(os.path.relpath(n["path"], ROOT)) if n.get("path") else ""


# ---------------------------------------------------------------------- migration and the views
def split_cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def migrate():
    """Read OPEN, WORK and DECISIONS into items, and their prose into templates. Run once, at the cut-over."""
    os.makedirs(VIEWS, exist_ok=True)
    seen = set()
    made = []
    for view, path in VIEW_FILES.items():
        text = open(path, encoding="utf-8").read()
        lines = text.split("\n")
        tmpl, seq = [], {}
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("| ") and i + 1 < len(lines) and re.match(r"\|[-| ]+\|$", lines[i + 1]):
                header = split_cells(line)
                j = i + 2
                rows = []
                while j < len(lines) and lines[j].startswith("|"):
                    rows.append(lines[j])
                    j += 1
                first = split_cells(rows[0])[0] if rows else ""
                table = _which_table(view, header, first, tmpl)
                if table is None:
                    tmpl.extend(lines[i:j])
                    i = j
                    continue
                tmpl.extend([line, lines[i + 1], f"<!-- records:{table[1]} -->"])
                cols = table[2]
                n_rows = len(rows)
                for k, r in enumerate(rows):
                    c = split_cells(r)
                    raw = c[0]
                    closed = raw.startswith("~~")
                    rid = raw.strip("~ ")
                    if rid in seen:
                        rid = rid + "b"
                    seen.add(rid)
                    it = {"id": rid, "kind": kind_of(rid), "path": os.path.join(ITEMS, f"{rid}.md")}
                    for f, v in zip(cols[1:], c[1:]):
                        it[f] = v
                    if len(c) > len(cols):
                        it["extra_cells"] = c[len(cols):]
                    # the cell's order in its table, so the view renders back exactly
                    it["seq"] = (n_rows - k) if table[5] < 0 else k + 1
                    it["table"] = table[1]
                    if closed:
                        it["struck"] = "yes"
                    if it["kind"] == "thread":
                        if table[1] == "done":
                            it["state"] = "done"
                    elif it["kind"] == "decision":
                        it["state"] = "replaced" if re.search(r"replaced by", it.get("body", ""), re.I) else "live"
                        it["created"] = iso(it.get("date", ""))
                    else:
                        it["state"] = "closed" if closed else "open"
                    if rid.endswith("b"):
                        it["duplicate_of"] = rid[:-1]
                    write_item(it)
                    made.append(rid)
                i = j
                continue
            tmpl.append(line)
            i += 1
        with open(os.path.join(VIEWS, f"{view}.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(tmpl))
    print(f"migrated {len(made)} rows into {os.path.relpath(ITEMS, ROOT)}/")


def _which_table(view, header, first, tmpl):
    heads = [l for l in tmpl if l.startswith("## ")]
    sect = heads[-1] if heads else ""
    for t in TABLES:
        if t[0] != view:
            continue
        if not re.match(r"~*(" + t[3] + r")\d*-", first or "X-"):
            if not (first == "" and t[1] == "offers"):
                continue
        if t[1] == "in_progress" and "In progress" not in sect:
            continue
        if t[1] == "paused" and "Paused" not in sect:
            continue
        if t[1] == "done" and "Done" not in sect:
            continue
        if len(header) != len(t[2]):
            continue
        return t
    return None


def render_view(view, items) -> str:
    tmpl = open(os.path.join(VIEWS, f"{view}.md"), encoding="utf-8").read()
    for t in TABLES:
        if t[0] != view:
            continue
        marker = f"<!-- records:{t[1]} -->"
        if marker not in tmpl:
            continue
        rows = [it for it in items.values() if t[4](it)]
        rows.sort(key=lambda it: (float(it.get("seq", 0) or 0), num(it["id"])), reverse=t[5] < 0)
        out = []
        for it in rows:
            rid = it["id"]
            if it.get("struck") or (is_closed(it) and it["kind"] in ("ask", "deferred", "conflict", "offer")):
                rid = f"~~{rid}~~"
            cells = [rid] + [str(it.get(f, "")).replace("\n", " ").replace("|", "/") for f in t[2][1:]]
            cells += [str(x) for x in as_list(it.get("extra_cells"))] if isinstance(it.get("extra_cells"), list) else []
            out.append("|" + "|".join(f" {c} " if c != "" else " " for c in cells) + "|")
        tmpl = tmpl.replace(marker + "\n", "\n".join(out) + ("\n" if out else ""))
        tmpl = tmpl.replace(marker, "\n".join(out))
    return tmpl


def view_rows(view):
    """The table rows of a view as it stands: [(table name, cells)], with the same table detection as the migration."""
    path = VIEW_FILES[view]
    if not os.path.exists(path):
        return []
    lines = open(path, encoding="utf-8").read().split("\n")
    out, heads, i = [], [], 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("## "):
            heads.append(line)
        if line.startswith("| ") and i + 1 < len(lines) and re.match(r"\|[-| ]+\|$", lines[i + 1]):
            header = split_cells(line)
            j = i + 2
            rows = []
            while j < len(lines) and lines[j].startswith("|"):
                rows.append(lines[j])
                j += 1
            first = split_cells(rows[0])[0] if rows else ""
            tb = _which_table(view, header, first, heads)
            if tb:
                out += [(tb, split_cells(r)) for r in rows]
            i = j
            continue
        i += 1
    return out


def sync_from_views() -> list:
    """Take in hand edits to the views (D2-232: the views are rendered, but a session that edits one by hand must not lose
    its edit): a row that differs from what its item renders updates the item; a row with a new id becomes an item."""
    items = load_items()
    changed = []
    for view in VIEW_FILES:
        if not os.path.exists(os.path.join(VIEWS, f"{view}.md")):
            continue
        rendered = {}
        for line in render_view(view, items).split("\n"):
            if line.startswith("|"):
                c = split_cells(line)
                rendered[c[0].strip("~ ")] = c
        for tb, c in view_rows(view):
            rid = c[0].strip("~ ")
            if not re.fullmatch(ID_RE, rid) or rendered.get(rid) == c:
                continue
            it = items.get(rid) or {"id": rid, "kind": kind_of(rid), "path": os.path.join(ITEMS, f"{rid}.md"),
                                     "created": str(TODAY), "table": tb[1],
                                     "seq": max([float(x.get("seq", 0) or 0) for x in items.values()] + [0]) + 1}
            for f, v in zip(tb[2][1:], c[1:]):
                it[f] = v
            if len(c) > len(tb[2]):
                it["extra_cells"] = c[len(tb[2]):]
            elif "extra_cells" in it:
                del it["extra_cells"]
            struck = c[0].startswith("~~")
            if it["kind"] == "thread":
                if it.get("table") != tb[1]:
                    it["table"] = tb[1]
                    it["seq"] = max([float(x.get("seq", 0) or 0) for x in items.values() if x["kind"] == "thread"] + [0]) + 1
                if tb[1] == "done":
                    it["state"] = it.get("state") if is_closed(it) else "done"
            elif it["kind"] != "decision":
                if struck and not is_closed(it):
                    it["state"], it["by"] = "closed", it.get("by") or "agent"
                elif not struck and is_closed(it):
                    it["state"] = "open"
                it["struck"] = "yes" if struck else ""
            write_item(it)
            items[rid] = it
            changed.append(rid)
    if changed:
        print(f"took in hand edits to the views: {', '.join(changed)}", file=sys.stderr)
    return changed


def render(check=False, sync=False) -> int:
    """Write the views from the items. `sync` first takes in hand edits; the writing verbs sync at their start instead,
    before they change an item, so that their own change is never mistaken for an edit to the view."""
    if sync and not check:
        sync_from_views()
    items = load_items()
    bad = 0
    for view, path in VIEW_FILES.items():
        if not os.path.exists(os.path.join(VIEWS, f"{view}.md")):
            continue
        new = render_view(view, items)
        old = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
        if new != old:
            if check:
                print(f"{os.path.relpath(path, ROOT)} is out of step with the items (run: python3 tools/records.py render)")
                bad += 1
            else:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new)
    return bad


# ---------------------------------------------------------------------- pending events and trailers
def pending() -> dict:
    try:
        return json.load(open(PENDING))
    except (OSError, ValueError):
        return {"opens": [], "closes": [], "decides": [], "threads": [], "builds": []}


def note(kind, *ids):
    p = pending()
    for i in ids:
        if i not in p.setdefault(kind, []):
            p[kind].append(i)
    try:
        json.dump(p, open(PENDING, "w"))
    except OSError:
        pass


def agent_name() -> str:
    try:
        return open(WHOAMI).read().strip()
    except OSError:
        return os.environ.get("RECORDS_AGENT", "")


def next_id(prefix) -> str:
    git("fetch", "-q", "origin", "main")
    used = set(load_items())
    for line in git("ls-tree", "--name-only", "origin/main", "docs/cybertron2/items/").split():
        used.add(os.path.basename(line)[:-3])
    for path in VIEW_FILES.values():
        if os.path.exists(path):
            used |= set(re.findall(r"\b(" + re.escape(prefix) + r"-\d+)", open(path, encoding="utf-8").read()))
    n = max([num(u)[1] for u in used if num(u)[0] == prefix] + [0]) + 1
    return f"{prefix}-{n}"


# ---------------------------------------------------------------------- the verbs: reading
def cmd_show(web, i, full=True):
    n = web.node(i)
    if not n:
        print(f"{i}: not found")
        return 1
    nid = n["id"]
    head = f"{nid}  {n.get('kind', '')}  {n.get('state', '')}"
    if n.get("by"):
        head += f" (by {n['by']})"
    print(f"{head}  {n.get('owner', '')}  updated {updated(n)}")
    print(f"  \"{title_of(n)}\"")
    for k in ("next", "revisit", "branch", "where", "waits_on_text", "default", "default_on", "decision", "designed_in",
              "resolution", "source", "replaces_text", "started", "touched", "notes", "done", "summary"):
        if n.get(k):
            v = str(n[k])
            print(f"  {k}: {v if len(v) < 400 else v[:397] + '...'}")
    if n.get("kind") in ("spec", "proposal", "note"):
        heads = re.findall(r"^(##+ .+)$", n["body"], re.M)
        if heads:
            print("  outline: " + " | ".join(h.lstrip("# ") for h in heads[:24]) + (" ..." if len(heads) > 24 else ""))
        dec = re.search(r"^## Decided\n(.*?)(?=^## |\Z)", n["body"], re.M | re.S)
        if dec:
            print("  decided:\n" + "\n".join("    " + l for l in dec.group(1).strip().split("\n")))
        oq = re.search(r"^## Open questions\n(.*?)(?=^## |\Z)", n["body"], re.M | re.S)
        if oq and oq.group(1).strip():
            print("  open questions:\n" + "\n".join("    " + l for l in oq.group(1).strip().split("\n")[:30]))
    elif full and n.get("body") and n["body"].strip() not in (title_of(n), f"**{title_of(n)}**"):
        b = n["body"]
        print("  " + (b if len(b) < 2500 else b[:2500] + " ... (open the file for the rest)").replace("\n", "\n  "))
    newer = []
    me = updated(n)
    for e in EDGES:
        for o in as_list(n.get(e)):
            print(web.line(o, e))
            on = web.node(o)
            if on and me and updated(on) > me:
                newer.append(o)
    kids = web.children.get(nid, [])
    _list(web, "child", kids)
    if n.get("kind") == "decision":
        a = web.area_of(nid)
        if a:
            print(f"  area      {', '.join(a)}")
    ments = sorted(web.mentions.get(nid, set()) - set(kids))
    docs = [m for m in ments if m in web.docs]
    its = [m for m in ments if m in web.items]
    _list(web, "doc", docs, limit=10)
    if its:
        shown = its[:12]
        print(f"  mentioned by {len(its)}: " + ", ".join(shown) + (f" and {len(its) - 12} more (ls {nid} --all)" if len(its) > 12 else ""))
    if newer:
        print(f"  ! {len(newer)} links newer than this: {', '.join(newer)}")
    return 0


def _list(web, edge, ids, limit=15, allrows=False):
    ids = list(ids)
    for o in (ids if allrows else ids[:limit]):
        print(web.line(o, edge))
    if not allrows and len(ids) > limit:
        print(f"  ... and {len(ids) - limit} more")


def cmd_ls(web, i, allrows=False):
    n = web.node(i)
    if not n:
        print(f"{i}: not found")
        return 1
    nid = n["id"]
    print(web.line(nid, "self").strip())
    for e in EDGES:
        _list(web, e, as_list(n.get(e)), allrows=allrows)
    _list(web, "child", web.children.get(nid, []), allrows=allrows)
    _list(web, "mention", sorted(web.mentions.get(nid, set())), allrows=allrows)
    return 0


def cmd_tree(web, i, depth=0, seen=None):
    seen = seen or set()
    if i in seen:
        return
    seen.add(i)
    print("  " * depth + web.line(i).strip())
    for c in sorted(web.children.get(i, []), key=num):
        cmd_tree(web, c, depth + 1, seen)
    for d in sorted(x for x in web.mentions.get(i, ()) if x in web.docs and i in as_list(web.docs[x].get("threads"))):
        print("  " * (depth + 1) + web.line(d, "doc").strip())


def cmd_area(web, name):
    docs = [d for d in web.docs.values() if d.get("area") and (d["area"] == name or d["area"].startswith(name + "/")
                                                                or name in d["area"])]
    if not docs:
        print(f"no spec area matches {name!r}; areas: " + ", ".join(sorted({d['area'].split('/')[0] for d in web.docs.values() if d.get('area')})))
        return 1
    for d in sorted(docs, key=lambda d: d["area"]):
        print(f"{d['area']}  ({d['id']}, updated {updated(d)})  \"{d['title']}\"")
        cited = sorted(set(re.findall(r"\b(" + ID_RE + r")\b", d["body"])), key=num)
        decs = [c for c in cited if c in web.items and web.items[c]["kind"] == "decision"]
        for c in decs:
            it = web.items[c]
            flag = "  REPLACED" if is_closed(it) else ""
            print(f"  {c}{flag}: {title_of(it)}")
        opens = [c for c in cited if c in web.items and web.items[c]["kind"] != "decision" and not is_closed(web.items[c])]
        for c in opens:
            print(web.line(c, "open"))
    return 0


def cmd_find(web, words):
    ws = [w.lower() for w in words]
    hits = []
    for nid, n in list(web.items.items()) + list(web.docs.items()):
        hay = (title_of(n) + " " + n.get("summary", "") + " " + n.get("body", "")).lower()
        if all(w in hay for w in ws):
            score = sum(3 for w in ws if w in title_of(n).lower()) + (0 if is_closed(n) else 1)
            hits.append((score, nid))
    hits.sort(key=lambda x: (-x[0], num(x[1])))
    for _, nid in hits[:25]:
        print(web.line(nid).strip())
    if len(hits) > 25:
        print(f"... and {len(hits) - 25} more")
    return 0


def cmd_log(web, i, limit=12):
    n = web.node(i)
    if not n:
        print(f"{i}: not found")
        return 1
    nid = n["id"]
    related = [nid] + [o for e in EDGES for o in as_list(n.get(e))] + web.children.get(nid, [])
    pat = "|".join(re.escape(x) for x in related)
    out = git("log", "--all", f"-{limit * 4}", "-E", f"--grep=\\b({pat})\\b", "--format=%ad %h %s", "--date=short")
    lines = out.strip().split("\n")[:limit]
    print("\n".join(l[:160] for l in lines if l))
    return 0


def cmd_status(web, owner=None):
    live = [it for it in web.items.values() if it["kind"] == "thread" and not is_closed(it)
            and (not owner or owner in it.get("owner", ""))]
    by_owner: dict = {}
    for it in live:
        by_owner.setdefault(it.get("owner", "?"), []).append(it)
    for o, its in sorted(by_owner.items()):
        act = [x for x in its if x.get("state") == "active"]
        print(f"{o}: {len(its)} live ({len(act)} active)" + ("  ! over the soft limit of 6 active: revisit" if len(act) > 6 else ""))
        for it in sorted(its, key=lambda x: (x.get("state") != "active", num(x["id"]))):
            nxt = it.get("next") or _left(it.get("notes", ""))
            print(f"  {it['id']} {it.get('state', '')} [{it.get('touched', '')}] {title_of(it)[:80]}")
            if nxt:
                print(f"      next: {nxt[:150]}")
    asks = [it for it in web.items.values() if it["kind"] == "ask" and not is_closed(it)
            and (not owner or "Zach" in it.get("owner", ""))]
    print(f"\nasks open: {len(asks)} (digest: python3 tools/records.py digest)")
    prov = [it for it in web.items.values() if is_closed(it) and it.get("by") in ("agent", "default", "relayed")]
    if prov:
        print(f"provisional resolutions to confirm: {len(prov)}: " + ", ".join(it["id"] for it in prov[:15]))
    rev = [it for it in web.items.values() if it.get("revisit")]
    if rev:
        print(f"marked revisit: {len(rev)}: " + ", ".join(it["id"] for it in rev[:15]))
    named = " ".join(json.dumps(it, ensure_ascii=False) for it in web.items.values())
    br = [b for b in branches_ahead() if b[0] not in named]
    if br:
        print("branches ahead of main that no thread names: " + ", ".join(f"{b} (+{n}, {d})" for b, n, d in br))
    return 0


def _left(notes: str) -> str:
    m = re.search(r"Left[^:]*:\s*(.+)", notes)
    return m.group(1) if m else ""


def cmd_brief(web):
    me = agent_name()
    if not web.items:
        return 0
    print(f"# The records, {TODAY} (you: {me or 'unset: run python3 tools/records.py whoami <37.2|37.4|...>'})")
    print("Status answers come from `records status`, not memory; record each event with one call and commit with "
          "`records commit` (skill: .claude/skills/records). A promise or offer in a reply needs a record (stop check).")
    live = [it for it in web.items.values() if it["kind"] == "thread" and not is_closed(it)]
    mine = [it for it in live if me and it.get("owner", "").startswith(me)]
    for st in ("active", "waiting"):
        rows = [it for it in mine if it.get("state", "").startswith(st)]
        if rows:
            print(f"\n{st} ({len(rows)}):" + ("  ! over the soft limit of 6: revisit" if st == "active" and len(rows) > 6 else ""))
        for it in sorted(rows, key=lambda x: num(x["id"])):
            nxt = it.get("next") or _left(it.get("notes", ""))
            print(f"  {it['id']} [{it.get('touched', '')}] {title_of(it)[:70]}" + (f"\n      next: {nxt[:140]}" if nxt else ""))
    for st in ("queued", "paused"):
        rows = [it for it in mine if it.get("state", "").startswith(st)]
        if rows:
            print(f"{st}: " + ", ".join(f"{it['id']} [{it.get('touched', '')}]" for it in sorted(rows, key=lambda x: num(x["id"]))))
    others: dict = {}
    for it in live:
        if it not in mine:
            others[it.get("owner", "?").split(" ")[0]] = others.get(it.get("owner", "?").split(" ")[0], 0) + 1
    if others:
        print("other owners' live threads: " + ", ".join(f"{o} {n}" for o, n in sorted(others.items())))
    asks = [it for it in web.items.values() if it["kind"] == "ask" and not is_closed(it)]
    print(f"asks open: {len(asks)}; Zach's digest: records digest")
    prov = [it["id"] for it in web.items.values() if is_closed(it) and it.get("by") in ("agent", "default", "relayed")]
    if prov:
        print(f"provisional resolutions for Zach to confirm: {', '.join(prov[:12])}")
    rev = [it["id"] for it in web.items.values() if it.get("revisit")]
    if rev:
        print(f"marked revisit: {', '.join(rev[:12])}")
    stale = [it for it in web.items.values() if it["kind"] == "offer" and not is_closed(it)
             and it.get("default_on") and str(it["default_on"]) <= str(TODAY)]
    if stale:
        print("offers past their default date: " + ", ".join(f"{it['id']} ({it.get('default', '')})" for it in stale))
    return 0


def cmd_digest(web, limit=8):
    asks = [it for it in web.items.values() if it["kind"] == "ask" and not is_closed(it) and "Zach" in it.get("owner", "")]
    waiting = {i: sum(1 for x in web.items.values() if i in as_list(x.get("waits_on"))) for i in (a["id"] for a in asks)}
    asks.sort(key=lambda a: (-waiting[a["id"]], -num(a["id"])[1]))
    print(f"# Asks for Zach: {len(asks)} open; the {min(limit, len(asks))} most waited on\n")
    for k, a in enumerate(asks[:limit], 1):
        print(f"{k}. {a['id']}: {title_of(a)}")
        for f in ("recommend", "default", "default_on"):
            if a.get(f):
                print(f"   {f}: {a[f]}")
        if waiting[a["id"]]:
            print(f"   waited on by {waiting[a['id']]}")
    return 0


def cmd_pack(web, ids):
    """The context to hand over: each node in full, its links one line each, the files to read, the open asks under it."""
    print(f"# Context pack: {', '.join(ids)} ({TODAY})\n")
    print("Read first: CLAUDE.md; .claude/skills/records/SKILL.md (how to record). Then the nodes below.\n")
    files = set()
    for i in ids:
        print("-" * 72)
        cmd_show(web, i)
        n = web.node(i) or {}
        for d in web.mentions.get(n.get("id", i), ()):
            if d in web.docs:
                files.add(d)
        for c in web.children.get(n.get("id", i), []):
            if not is_closed(web.items[c]):
                print(web.line(c, "open"))
    if files:
        print("\nDocuments that mention these (open as needed):")
        for f in sorted(files)[:30]:
            print(f"  {f}: {web.docs[f]['title']}")
    return 0


# ---------------------------------------------------------------------- the verbs: writing
def _kv(pairs) -> dict:
    out = {}
    for p in pairs:
        if "=" not in p:
            raise SystemExit(f"expected field=value, got {p!r}")
        k, v = p.split("=", 1)
        out[k] = as_list(v) if k in LIST_FIELDS else v
    return out


def cmd_new(kind_letter, title, owner, parent, text, extra) -> str:
    prefix = kind_letter.upper()
    if prefix not in ("W", "Q", "L", "O", "C"):
        raise SystemExit("new: kind is W, Q, L, O or C (decisions: use `decide`)")
    i = next_id(prefix)
    it = {"id": i, "kind": KINDS[prefix], "title": title, "owner": owner or agent_name(), "created": str(TODAY),
          "body": f"**{title}**" + (f": {text}" if text else "")}
    it["state"] = "queued" if prefix == "W" else "open"
    if prefix == "W":
        it.update({"started": TODAY.strftime("%-d %b"), "touched": TODAY.strftime("%-d %b"), "table": "in_progress",
                   "where": "", "notes": "started"})
    else:
        it["table"] = {"Q": "asks", "L": "deferred", "O": "offers", "C": "conflicts"}[prefix]
    if parent:
        it["parent"] = as_list(parent)
    it.update(_kv(extra))
    items = load_items()
    it["seq"] = max([float(x.get("seq", 0) or 0) for x in items.values() if x["kind"] == it["kind"]] + [0]) + 1
    if it["kind"] == "thread" and not it.get("parent"):
        pass
    elif not it.get("parent"):
        print(f"warning: {i} has no parent thread (set one: records set {i} parent=W-n)", file=sys.stderr)
    write_item(it)
    note("opens", i)
    render()
    print(i)
    return i


def cmd_set(i, pairs):
    items = load_items()
    if i not in items:
        raise SystemExit(f"{i}: not found")
    it = items[i]
    kv = _kv(pairs)
    if kv.get("by") == "zach" and not kv.get("answer") and not it.get("answer"):
        raise SystemExit("by=zach needs Zach's own words: add answer=\"...\" (D2-236)")
    it.update(kv)
    if it["kind"] == "thread":
        it["touched"] = TODAY.strftime("%-d %b")
        if kv.get("state"):
            new = "paused" if kv["state"] == "paused" else "done" if is_closed(it) else "in_progress"
            if new != it.get("table"):
                it["table"] = new
                it["seq"] = max([float(x.get("seq", 0) or 0) for x in items.values() if x["kind"] == "thread"] + [0]) + 1
    write_item(it)
    th = [i] if it["kind"] == "thread" else as_list(it.get("parent"))
    note("threads", *th)
    render()
    return 0


def cmd_link(i, edge, other, reason):
    items = load_items()
    if i not in items:
        raise SystemExit(f"{i}: not found")
    if edge not in EDGES:
        raise SystemExit(f"edge is one of {EDGES}")
    if edge == "relates" and not reason:
        raise SystemExit("relates needs --reason (D2-234)")
    it = items[i]
    it[edge] = sorted(set(as_list(it.get(edge)) + [other]), key=num)
    if reason:
        it["relates_why"] = as_list(it.get("relates_why")) + [f"{other}: {reason}"]
    write_item(it)
    render()
    return 0


def cmd_close(i, by, note_text, state=None, answer=None):
    items = load_items()
    if i not in items:
        raise SystemExit(f"{i}: not found")
    if by not in BY:
        raise SystemExit(f"--by is one of {BY} (D2-236)")
    it = items[i]
    if by == "zach" and not (answer or it.get("answer")):
        raise SystemExit("--by zach needs --answer with Zach's own words (D2-236)")
    if it["kind"] == "thread":
        kids = [c for c, x in items.items() if i in as_list(x.get("parent")) and not is_closed(x) and not x.get("revisit")]
        if kids:
            raise SystemExit(f"{i} has open children: {', '.join(kids)}. Move each (set X parent=W-n), close it, "
                             f"or mark it (set X revisit=\"reason\") first (D2-236)")
        it["state"] = state or "done"
        it["done"] = f"{state or 'done'} {TODAY.strftime('%-d %b')}" + (f": {note_text}" if note_text else "")
        it["table"] = "done"
        it["seq"] = max([float(x.get("seq", 0) or 0) for x in items.values() if x["kind"] == "thread"] + [0]) + 1
    else:
        it["state"] = state or "closed"
        if note_text:
            it["body"] = f"**(Closed {TODAY.strftime('%-d %b')}: {note_text}.)** " + it.get("body", "")
    it["by"] = by
    if answer:
        it["answer"] = answer
    write_item(it)
    note("closes", i)
    render()
    return 0


def cmd_decide(rule, area, quote, closes, replaces, parent, proposal, series=None):
    series = series or {"37.2": "D2", "37.4": "D4", "37.1": "D1"}.get(agent_name(), "")
    if not series:
        raise SystemExit("decide: set your session first (records whoami 37.2) so the decision takes your series")
    if not quote:
        raise SystemExit("decide needs --quote: Zach's own words (D2-236; README rule 2)")
    items = load_items()
    i = next_id(series)
    body = f"**{rule}**"
    it = {"id": i, "kind": "decision", "state": "live", "by": "zach", "created": str(TODAY), "owner": agent_name(),
          "date": TODAY.strftime("%-d %b"), "body": body, "source": f"conversation ({TODAY.strftime('%-d %b')}: \"{quote}\")",
          "replaces_text": replaces or "", "area": area or "",
          "seq": max([float(x.get("seq", 0) or 0) for x in items.values() if x["kind"] == "decision"] + [0]) + 1}
    if closes:
        it["decides"] = closes
    if replaces:
        it["replaces"] = as_list(replaces)
    if parent:
        it["parent"] = as_list(parent)
    write_item(it)
    for q in closes or []:
        if q in items and not is_closed(items[q]):
            cmd_close(q, "zach", i, answer=quote)
    for r in as_list(replaces):
        if r in items:
            ri = items[r]
            ri["state"] = "replaced"
            ri["body"] = ri.get("body", "") + f" (replaced by {i})"
            write_item(ri)
    if area:
        sp = area if area.endswith(".md") else os.path.join("docs/cybertron2/spec", area + ".md")
        sp = os.path.join(ROOT, sp) if not os.path.isabs(sp) else sp
        if os.path.exists(sp):
            _spec_line(sp, i, rule, as_list(replaces))
        else:
            print(f"warning: no spec file {os.path.relpath(sp, ROOT)}; the decision has no spec line yet", file=sys.stderr)
    if proposal:
        _history(proposal, f"accepted in part: {i} ({rule[:80]})")
    note("decides", i)
    if parent:
        note("threads", *as_list(parent))
    render()
    print(i)
    return i


def _spec_line(path, did, rule, replaces):
    t = open(path, encoding="utf-8").read()
    line = f"- {did}: {rule}"
    m = re.search(r"^## Decided\n", t, re.M)
    if m:
        end = re.search(r"^## ", t[m.end():], re.M)
        pos = m.end() + (end.start() if end else len(t) - m.end())
        block = t[m.end():pos].rstrip("\n")
        t = t[:m.end()] + block + ("\n" if block else "\n") + line + "\n\n" + t[pos:].lstrip("\n")
    else:
        t = t.rstrip("\n") + f"\n\n## Decided\n\n{line}\n"
    for r in replaces:
        t = re.sub(r"^(- .*\b" + re.escape(r) + r"\b.*)$", r"\1 **(replaced by " + did + r": rewrite this line)**", t, flags=re.M)
    open(path, "w", encoding="utf-8").write(t)
    note("paths", os.path.relpath(path, ROOT))


def _history(proposal, text):
    p = proposal if os.path.isabs(proposal) else os.path.join(ROOT, proposal)
    if not os.path.exists(p):
        p = os.path.join(C2, "proposals", os.path.basename(proposal))
    t = open(p, encoding="utf-8").read()
    entry = f"- {TODAY.day} {TODAY.strftime('%b %Y')}: {text}."
    t = re.sub(r"^## History\n\n", "## History\n\n" + entry + "\n", t, count=1, flags=re.M)
    open(p, "w", encoding="utf-8").write(t)
    note("paths", os.path.relpath(p, ROOT))


def infer_type(paths) -> str:
    code = [p for p in paths if p.startswith(("cybertron2/", "c2viz/", "tests/", "tools/", ".claude/", ".github/"))]
    if any(p.startswith(("cybertron2/specs/", "specs/")) for p in paths) or code:
        return "build"
    if pending().get("decides"):
        return "decide"
    if paths and all(p.startswith("docs/cybertron2/items/") or p in [os.path.relpath(v, ROOT) for v in VIEW_FILES.values()]
                     for p in paths):
        return "record"
    return "design"


def trailers(agent, threads, p) -> list:
    out = [f"Agent: {agent}"]
    for t in threads:
        out.append(f"Thread: {t}")
    for key, name in (("opens", "Opens"), ("closes", "Closes"), ("decides", "Decides"), ("builds", "Builds")):
        if p.get(key):
            out.append(f"{name}: {', '.join(p[key])}")
    return out


ATTRIBUTION = os.environ.get("RECORDS_ATTRIBUTION", "")


def cmd_commit(msg, typ, thread, paths, body, builds):
    p = pending()
    if builds:
        p["builds"] = sorted(set(p.get("builds", []) + as_list(builds)), key=num)
    render()
    git("add", "--", os.path.relpath(ITEMS, ROOT), *[os.path.relpath(v, ROOT) for v in VIEW_FILES.values()], *paths,
        *p.get("paths", []))
    staged = [l for l in git("diff", "--cached", "--name-only").split("\n") if l]
    if not staged:
        raise SystemExit("nothing staged")
    typ = typ or infer_type(staged)
    threads = as_list(thread) or p.get("threads", []) or []
    if not threads and typ != "upkeep":
        raise SystemExit("commit: name a thread (--thread W-n), or --type upkeep (D2-235)")
    main = threads[0] if threads else ""
    typed = re.match(r"(" + "|".join(TYPES) + r") (" + ID_RE + r"|[\w./-]+):", msg)
    subject = msg if typed else f"{typ} {main}: {msg}".replace(" : ", ": ")
    agent = agent_name() or "unknown"
    att = ATTRIBUTION or _attribution()
    text = subject + ("\n\n" + body if body else "") + "\n\n" + "\n".join(trailers(agent, threads, p) + att)
    r = subprocess.run(["git", "commit", "-q", "-F", "-"], cwd=ROOT, input=text, text=True, capture_output=True)
    if r.returncode:
        raise SystemExit(r.stderr + r.stdout)
    try:
        os.remove(PENDING)
    except OSError:
        pass
    print(git("log", "--oneline", "-1").strip())
    return 0


def _attribution() -> list:
    """The attribution lines of the last commit by this agent, so the trailers sit in one block with them."""
    out = git("log", "-1", "--format=%(trailers:key=Co-Authored-By)%(trailers:key=Claude-Session)").strip()
    return [l for l in out.split("\n") if l]


# ---------------------------------------------------------------------- checks
def check(strict=False) -> int:
    items = load_items()
    hard, soft = [], []
    hard += [f"view: {x}" for x in _render_diff()]
    ids = {}
    for it in items.values():
        ids.setdefault(os.path.basename(it["path"])[:-3], []).append(it["id"])
    hard += [f"{f}.md holds id {v}" for f, v in ids.items() if v != [f]]
    for it in items.values():
        for e in EDGES:
            for o in as_list(it.get(e)):
                if o not in items and not os.path.exists(os.path.join(ROOT, o)):
                    hard.append(f"{it['id']}: {e} names {o}, which is not an item")
        if it.get("by") and it["by"] not in BY:
            hard.append(f"{it['id']}: by is {it['by']!r} (one of {BY})")
        if it.get("created", "") >= "2026-11-20" and it["kind"] in ("ask", "deferred", "offer") and not it.get("parent"):
            soft.append(f"{it['id']}: an orphan (no parent thread)")
        if it["kind"] == "decision" and it.get("created", "") >= "2026-11-20" and not it.get("area") \
                and "[no spec]" not in it.get("body", ""):
            soft.append(f"{it['id']}: a decision with no area")
    for f in hard:
        print("ERROR " + f)
    for f in soft:
        print("note  " + f)
    print(f"{len(items)} items; {len(hard)} errors, {len(soft)} notes")
    return 1 if hard or (strict and soft) else 0


def _render_diff():
    items = load_items()
    out = []
    for view, path in VIEW_FILES.items():
        if os.path.exists(os.path.join(VIEWS, f"{view}.md")) and render_view(view, items) != open(path, encoding="utf-8").read():
            out.append(f"{os.path.relpath(path, ROOT)} differs from its items (records render)")
    return out


# ---------------------------------------------------------------------- the push check of commits, branches, the vault
def check_commits(rng) -> int:
    """Each commit in a range (the push) against D2-235: trailers present and readable; ids it names exist in its tree.
    Reports, never fails: a direct push to main cannot be refused (D2-235)."""
    out = git("log", "--no-merges", "--format=%H%x1f%s%x1f%(trailers:key=Agent,valueonly,separator=%x2c)%x1f"
              "%(trailers:key=Thread,valueonly,separator=%x2c)%x1f%(trailers:key=Opens,valueonly,separator=%x2c)%x1e", rng)
    probs = []
    n = 0
    for rec in out.split("\x1e"):
        rec = rec.strip()
        if not rec:
            continue
        n += 1
        h, subj, agent, thread, opens = (rec.split("\x1f") + [""] * 5)[:5]
        tag = f"{h[:7]} {subj[:70]}"
        if not git("ls-tree", "--name-only", h, "docs/cybertron2/items/").strip():
            continue  # before the records existed
        if not agent.strip():
            probs.append(f"{tag}: no Agent trailer git can read")
        if not thread.strip() and not subj.startswith("upkeep"):
            probs.append(f"{tag}: no Thread trailer")
        tree = set(os.path.basename(x)[:-3] for x in git("ls-tree", "--name-only", h, "docs/cybertron2/items/").split())
        for i in as_list(thread) + as_list(opens):
            if re.fullmatch(ID_RE, i) and i not in tree:
                probs.append(f"{tag}: names {i}, not an item in that commit")
        if not re.match(r"(" + "|".join(TYPES) + r")\b", subj):
            probs.append(f"{tag}: the subject does not start with a type ({', '.join(TYPES)})")
    print(f"{n} commits checked; {len(probs)} problems")
    for p in probs:
        print("- " + p)
    return 0


def cmd_branches(web) -> int:
    """Branches against main (D2-238): ahead with their thread, or empty (fully merged) and so clutter."""
    named = " ".join(json.dumps(it, ensure_ascii=False) for it in web.items.values())
    ahead, empty = [], []
    for b in git("for-each-ref", "--format=%(refname:short)", "refs/remotes/origin").split():
        if b in ("origin/main", "origin/HEAD", "origin"):
            continue
        name = b.replace("origin/", "")
        n = int(git("rev-list", "--count", f"origin/main..{b}").strip() or 0)
        d = git("log", "-1", "--format=%ad", "--date=short", b).strip()
        (ahead if n else empty).append((name, n, d))
    print(f"ahead of main ({len(ahead)}):")
    for name, n, d in sorted(ahead, key=lambda x: x[2], reverse=True):
        th = sorted({i for i, it in web.items.items() if name in json.dumps(it, ensure_ascii=False)}, key=num)[:4]
        print(f"  {name:<28} +{n:<4} {d}  " + (", ".join(th) if th else "NO THREAD names it"))
    print(f"empty (all on main), can be deleted ({len(empty)}): " + ", ".join(f"{n} ({d})" for n, _, d in sorted(empty)))
    return 0


def _slug(s: str) -> str:
    s = re.sub(r"[\\/:*?\"<>|#^\[\]`]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s[:80].rstrip(" .")


def _cut(s: str, n: int) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) <= n:
        return s
    c = s[:n].rsplit(" ", 1)[0].rstrip(",;:(")
    return c + "…"


def short_title(n) -> str:
    """A readable title: the bold lead of a row, else its first clause, cut at a word."""
    t = title_of(n).rstrip(".")
    if len(t) > 60:
        m = re.match(r"(.{12,}?)(?::\s| \(|; | - )", t)
        if m:
            t = m.group(1)
    return _cut(t, 70)


def _body_md(n) -> str:
    """A table cell as prose: the bold lead it repeats dropped, numbered parts as a list, 'Left:' and 'done:' on lines."""
    b = n.get("body", "") or ""
    b = re.sub(r"^\*\*\(Closed[^*]*\)\*\*\s*", "", b)
    lead = title_of(n)
    b = re.sub(r"^\*\*" + re.escape(lead) + r"\*\*\s*:?\s*", "", b) if lead else b
    parts = re.split(r"\s*\((\d{1,2})\)\s+", b)
    if len(parts) >= 5:
        out = [parts[0].rstrip(" :;")] if parts[0].strip() else []
        for k in range(1, len(parts) - 1, 2):
            out.append(f"{parts[k]}. " + parts[k + 1].strip().rstrip(";"))
        b = "\n".join(out)
    b = re.sub(r"[.;]\s+(Left(?:, in order)?:|left:|Done so far:|done:|Next:)", r".\n\n**\1**", b)
    return b.strip()


def cmd_vault(web, out) -> int:
    """A derived Obsidian vault (D2-240): readable notes by kind, linked, the live apart from the archive. Never edited."""
    import shutil
    out = os.path.abspath(out)
    keep = (".git", ".obsidian", ".gitignore")
    if os.path.exists(out) and [n for n in os.listdir(out) if n not in keep] \
            and not os.path.exists(os.path.join(out, ".records-vault")):
        raise SystemExit(f"{out} exists and is not a vault this tool made; choose another folder")
    # Regenerate in place (D2-240): the notes are replaced, but a git checkout (.git) and Obsidian's own settings
    # (.obsidian, kept local by .gitignore) stay, so a clone of the vault branch can be pulled into.
    os.makedirs(out, exist_ok=True)
    for n in os.listdir(out):
        if n in keep:
            continue
        p = os.path.join(out, n)
        shutil.rmtree(p) if os.path.isdir(p) and not os.path.islink(p) else os.remove(p)
    folder = {"thread": "Threads", "ask": "Asks", "offer": "Offers", "deferred": "Later", "conflict": "Conflicts",
              "decision": "Decisions", "spec": "Spec", "proposal": "Proposals", "note": "Notes"}
    # Documents that mention very many ids are indexes or audits: they are kept, but not listed as "mentioned by".
    index_docs = {d for d, doc in web.docs.items()
                  if len(set(re.findall(r"\b(" + ID_RE + r")\b", doc.get("body", "")))) > 60}
    names, short = {}, {}
    for nid, n in web.items.items():
        short[nid] = short_title(n)
        sub = folder[n["kind"]]
        if n["kind"] == "decision":
            a = (web.area_of(nid) or [""])[0]
            sub = os.path.join("Archive", "Decisions replaced") if is_closed(n) else \
                os.path.join(sub, _slug(a.replace("/", " - ")) if a else "Process and other")
        elif is_closed(n):
            sub = os.path.join("Archive", sub)
        names[nid] = os.path.join(sub, _slug(f"{nid} {short[nid]}"))
    for nid, d in web.docs.items():
        short[nid] = _cut(d["title"], 70)
        sub = folder[d["kind"]]
        if d["kind"] == "spec":
            sub = os.path.join(sub, os.path.dirname(d["area"]))
        elif d["kind"] == "note":
            sub = os.path.join(sub, os.path.basename(os.path.dirname(nid)))
        names[nid] = os.path.join(sub, _slug(short[nid]))
    areas = sorted({d["area"] for d in web.docs.values() if d.get("area")})
    area_page = {a: os.path.join("Areas", f"{a.replace('/', ' - ')}") for a in areas}

    def link(i, full=False):
        if i not in names:
            return i
        label = (f"{i} · {short[i]}" if full else i) if not i.endswith(".md") else short[i]
        return f"[[{os.path.basename(names[i])}|{label}]]"

    def alink(a):
        return f"[[{os.path.basename(area_page[a])}|{a}]]" if a in area_page else a

    def linkify(text):
        return re.sub(r"\b(" + ID_RE + r")\b", lambda m: link(m.group(1)), text)

    def write(rel, text):
        p = os.path.join(out, rel + ".md")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(text)

    def ago(d):
        try:
            k = (TODAY - dt.date.fromisoformat(iso(d) or d)).days
            return "today" if k == 0 else f"{k} day{'s' if k != 1 else ''} ago"
        except ValueError:
            return d

    def mentions(nid):
        ms = [m for m in web.mentions.get(nid, set()) if m not in index_docs]
        order = {"decision": 0, "ask": 1, "thread": 2, "deferred": 3, "offer": 4, "conflict": 5}
        ms.sort(key=lambda m: (m.endswith(".md"), order.get((web.node(m) or {}).get("kind"), 9), num(m)))
        hidden = len([m for m in web.mentions.get(nid, set()) if m in index_docs])
        if not ms and not hidden:
            return ""
        lines = [f"- {link(m, True)}" for m in ms[:40]]
        if len(ms) > 40:
            lines.append(f"- … and {len(ms) - 40} more")
        if hidden:
            lines.append(f"- *and {hidden} index or audit notes*")
        return "\n## Mentioned by\n" + "\n".join(lines) + "\n"

    def links_block(n):
        rows = [f"- {e.replace('_', ' ')}: {link(o, True)}" for e in EDGES for o in as_list(n.get(e))]
        kids = sorted(web.children.get(n["id"], []), key=num)
        rows += [f"- under it: {link(k, True)} ({web.items[k].get('state', '')})" for k in kids]
        return ("\n## Linked\n" + "\n".join(rows) + "\n") if rows else ""

    def head(n):
        fm = {"id": n["id"], "kind": n.get("kind"), "state": n.get("state", ""), "updated": updated(n)}
        return "---\n" + "\n".join(f"{k}: {dump_value(v)}" for k, v in fm.items() if v) + "\n---\n"

    for nid, n in web.items.items():
        k = n["kind"]
        st = n.get("state", "")
        if n.get("by") and is_closed(n):
            st += f", by {n['by']}" + (" (provisional)" if n["by"] != "zach" else "")
        lines = [head(n), f"# {nid} · {short[nid]}\n"]
        if k == "thread":
            lines.append(f"*{st} · {n.get('owner', '')} · touched {n.get('touched', '')} ({ago(n.get('touched', ''))})*\n")
            nxt = n.get("next") or _left(n.get("notes", ""))
            if nxt:
                lines.append(f"> **Next:** {linkify(nxt)}\n")
            if len(title_of(n)) > len(short[nid]) + 3:
                lines.append("## What it is\n" + linkify(_body_md(n) or title_of(n)) + "\n")
            if n.get("notes") or n.get("done"):
                lines.append("## Done so far, and what is left\n" + linkify(_body_md({"body": n.get("done") or n.get("notes", "")})) + "\n")
            if n.get("where"):
                lines.append("## Where\n" + "\n".join(f"- `{w.strip()}`" if "/" in w or "." in w else f"- {w.strip()}"
                                                     for w in re.split(r";\s*", n["where"]) if w.strip()) + "\n")
        elif k == "decision":
            a = web.area_of(nid)
            lines.append(f"*{st} · {n.get('date', '')}" + (f" · spec: {', '.join(alink(x) for x in a)}" if a else "") + "*\n")
            lines.append("## The rule\n" + linkify(_body_md(n)) + "\n")
            if n.get("source"):
                lines.append("## Where it came from\n" + linkify(n["source"]) + "\n")
            if n.get("replaces_text"):
                lines.append("## What it replaced\n" + linkify(n["replaces_text"]) + "\n")
        else:
            lines.append(f"*{st} · {n.get('owner', '')}*\n")
            lines.append("## " + {"ask": "The question", "deferred": "Later", "offer": "The offer", "conflict": "The conflict"}
                         .get(k, "Text") + "\n" + linkify(_body_md(n)) + "\n")
            for f, label in (("recommend", "Recommended"), ("default", "Default"), ("default_on", "Default applies on"),
                             ("answer", "Zach's answer"), ("decision", "Decided"), ("designed_in", "Designed in"),
                             ("waits_on_text", "Waits on"), ("resolution", "Proposed resolution"), ("where", "Where"),
                             ("revisit", "Revisit")):
                if n.get(f):
                    lines.append(f"**{label}:** {linkify(str(n[f]))}\n")
        lines.append(links_block(n))
        lines.append(mentions(nid))
        write(names[nid], "\n".join(x for x in lines if x))
    for nid, d in web.docs.items():
        intro = [f"---\nid: {dump_value(nid)}\nkind: {d['kind']}\nupdated: {dump_value(updated(d))}\n---\n"]
        meta = [f"*{d['kind']}" + (f" · {d['state']}" if d.get("state") else "") + f" · `{nid}`" +
                (f" · area {alink(d['area'])}" if d.get("area") else "") + "*"]
        if d.get("summary"):
            meta.append(f"\n> {linkify(d['summary'])}")
        body = re.sub(r"^# .+\n", "", d["body"], count=1)
        write(names[nid], intro[0] + f"# {d['title']}\n\n" + "\n".join(meta) + "\n\n" + linkify(body) + mentions(nid))
    # area pages
    for a in areas:
        d = next(x for x in web.docs.values() if x.get("area") == a)
        cited = sorted(set(re.findall(r"\b(" + ID_RE + r")\b", d["body"])), key=num)
        decs = [c for c in cited if c in web.items and web.items[c]["kind"] == "decision"]
        live = [c for c in decs if not is_closed(web.items[c])]
        lines = [f"# {a}\n", f"*{d['title']}* · the spec: {link(d['id'])}\n"]
        if d.get("summary"):
            lines.append(f"> {d['summary']}\n")
        lines.append(f"## Decided ({len(live)})")
        for c in live:
            lines.append(f"- **{link(c)}** {short[c]}")
        gone = [c for c in decs if c not in live]
        if gone:
            lines.append(f"\n*Replaced: {', '.join(link(c) for c in gone)}*")
        opens = [c for c in cited if c in web.items and web.items[c]["kind"] != "decision" and not is_closed(web.items[c])]
        if opens:
            lines.append("\n## Open here")
            lines += [f"- {link(c, True)} ({web.items[c].get('state', '')})" for c in opens]
        write(area_page[a], "\n".join(lines) + "\n")
    # the start page and its indexes
    live = [it for it in web.items.values() if it["kind"] == "thread" and not is_closed(it)]
    owner = lambda it: it.get("owner", "?").split(" ")[0]
    asks = [it for it in web.items.values() if it["kind"] == "ask" and not is_closed(it)]
    mine = [a for a in asks if "Zach" in a.get("owner", "")]
    waits = {}
    for x in web.items.values():
        for w in as_list(x.get("waits_on")):
            waits[w] = waits.get(w, 0) + 1
    mine.sort(key=lambda a: (-waits.get(a["id"], 0), -num(a["id"])[1]))
    home = ["# Cybertron 2\n", f"*The records, rebuilt from main after every push (last {TODAY}). Read only: ask a session to "
            "change anything.*\n", f"## Waiting on you ({len(mine)})"]
    home += [f"- {link(a['id'], True)}" for a in mine[:12]]
    if len(mine) > 12:
        home.append(f"- … all of them: [[All asks]]")
    att = [it for it in web.items.values() if (is_closed(it) and it.get("by") in ("agent", "default", "relayed"))
           or it.get("revisit")]
    if att:
        home.append("\n## To confirm or revisit")
        home += [f"- {link(it['id'], True)}: " + (f"closed by {it['by']}" if is_closed(it) else f"revisit: {it['revisit']}")
                 for it in att[:12]]
    for stname, label in (("active", "Active"), ("waiting", "Waiting")):
        rows = [it for it in live if it.get("state", "").startswith(stname)]
        home.append(f"\n## {label} threads ({len(rows)})")
        for o in sorted({owner(it) for it in rows}):
            home.append(f"\n**{o}**")
            for it in sorted((x for x in rows if owner(x) == o), key=lambda x: num(x["id"])):
                nxt = it.get("next") or _left(it.get("notes", ""))
                home.append(f"- {link(it['id'], True)}" + (f"  \n  next: {_cut(nxt, 110)}" if nxt else ""))
    rest = [it for it in live if not it.get("state", "").startswith(("active", "waiting"))]
    if rest:
        home.append(f"\n## Queued and paused ({len(rest)})")
        home.append(", ".join(f"{link(it['id'])} {short[it['id']]}" for it in sorted(rest, key=lambda x: num(x["id"]))))
    recent = sorted((it for it in web.items.values() if it["kind"] == "decision" and it.get("created", "") >= str(TODAY - dt.timedelta(days=7))),
                    key=lambda x: (x.get("created", ""), num(x["id"])[1]), reverse=True)
    if recent:
        home.append(f"\n## Decided this week ({len(recent)})")
        home += [f"- {link(it['id'], True)}" for it in recent[:15]]
    home.append("\n## The world, by area")
    tops = {}
    for a in areas:
        tops.setdefault(a.split("/")[0], []).append(a)
    for top, sub in sorted(tops.items()):
        home.append(f"- **{top}**: " + ", ".join(f"[[{os.path.basename(area_page[a])}|{a.split('/', 1)[-1]}]]" for a in sub))
    home.append("\n## Everything\n[[All threads]] · [[All asks]] · [[All deferred]] · [[All offers]]")
    write("Home", "\n".join(home) + "\n")
    for title, kind in (("All threads", "thread"), ("All asks", "ask"), ("All deferred", "deferred"), ("All offers", "offer")):
        its = sorted((it for it in web.items.values() if it["kind"] == kind), key=lambda x: (is_closed(x), -num(x["id"])[1]))
        lines = [f"# {title}\n", "## Open"] + [f"- {link(it['id'], True)} ({it.get('state', '')})" for it in its if not is_closed(it)]
        closed = [it for it in its if is_closed(it)]
        if closed:
            lines += [f"\n## Closed ({len(closed)})"] + [f"- {link(it['id'], True)}" for it in closed]
        write(title, "\n".join(lines) + "\n")
    open(os.path.join(out, ".records-vault"), "w").write("made by tools/records.py vault; rebuilt after every push to main\n")
    if not os.path.exists(os.path.join(out, ".gitignore")):
        open(os.path.join(out, ".gitignore"), "w").write(".obsidian/\n.trash/\n")
    app = os.path.join(out, ".obsidian", "app.json")
    if not os.path.exists(app):
        os.makedirs(os.path.dirname(app), exist_ok=True)
        json.dump({"defaultViewMode": "preview", "propertiesInDocument": "hidden"}, open(app, "w"))
    print(f"vault written: {out} ({len(names)} notes; open the folder in Obsidian and start from Home)")
    return 0


def cmd_export(web, out) -> int:
    """The desk's data (D2-239): Zach's asks, the live threads, what needs his attention, the branches, recent decisions."""
    os.makedirs(out, exist_ok=True)
    def age(d):
        try:
            return (TODAY - dt.date.fromisoformat(iso(d) or d)).days
        except ValueError:
            return None
    waiting = {}
    for x in web.items.values():
        for w in as_list(x.get("waits_on")):
            waiting[w] = waiting.get(w, 0) + 1
    asks = [{"id": a["id"], "ask": title_of(a), "owner": a.get("owner", ""), "waited_on_by": waiting.get(a["id"], 0),
             "recommend": a.get("recommend", ""), "default": a.get("default", ""), "default_on": a.get("default_on", "")}
            for a in web.items.values() if a["kind"] == "ask" and not is_closed(a) and "Zach" in a.get("owner", "")]
    asks.sort(key=lambda r: (-r["waited_on_by"], -num(r["id"])[1]))
    threads = []
    for it in web.items.values():
        if it["kind"] == "thread" and not is_closed(it):
            threads.append({"id": it["id"], "owner": it.get("owner", "").split(" ")[0], "state": it.get("state", ""),
                            "touched": it.get("touched", ""), "days_since": age(it.get("touched", "")),
                            "work": title_of(it), "next": (it.get("next") or _left(it.get("notes", "")))[:240]})
    order = {"active": 0, "waiting": 1, "queued": 2, "paused": 3}
    threads.sort(key=lambda r: (r["owner"], order.get(r["state"].split(" ")[0], 9), -num(r["id"])[1]))
    attention = []
    for it in web.items.values():
        if is_closed(it) and it.get("by") in ("agent", "default", "relayed"):
            attention.append({"id": it["id"], "what": title_of(it), "why": f"closed by {it['by']}: confirm or reopen"})
        if it.get("revisit"):
            attention.append({"id": it["id"], "what": title_of(it), "why": f"revisit: {it['revisit']}"})
        if it["kind"] == "offer" and not is_closed(it) and it.get("default_on") and str(it["default_on"]) <= str(TODAY):
            attention.append({"id": it["id"], "what": title_of(it), "why": f"past its default ({it.get('default', '')})"})
    for o in sorted({r["owner"] for r in threads}):
        n = sum(1 for r in threads if r["owner"] == o and r["state"] == "active")
        if n > 6:
            attention.append({"id": o, "what": f"{n} active threads", "why": "over the soft limit of 6: revisit (D2-239)"})
    named = " ".join(json.dumps(it, ensure_ascii=False) for it in web.items.values())
    branches = []
    for name, n, d in branches_ahead():
        th = sorted({i for i, it in web.items.items() if it["kind"] == "thread" and name in json.dumps(it, ensure_ascii=False)},
                    key=num)
        branches.append({"branch": name, "ahead": n, "last": d, "threads": ", ".join(th[:4]) or "none"})
    branches.sort(key=lambda r: r["last"], reverse=True)
    recent = []
    for it in web.items.values():
        if it["kind"] == "decision" and it.get("created") and age(it["created"]) is not None and age(it["created"]) <= 14:
            recent.append({"id": it["id"], "date": it["created"], "decision": title_of(it),
                           "area": ", ".join(web.area_of(it["id"])) or ("process" if "[no spec]" in it.get("body", "") else ""),
                           "state": it.get("state", "")})
    recent.sort(key=lambda r: (r["date"], num(r["id"])[1]), reverse=True)
    for name, rows in (("asks", asks), ("threads", threads), ("attention", attention), ("branches", branches),
                       ("decisions", recent)):
        json.dump(rows, open(os.path.join(out, f"{name}.json"), "w"), ensure_ascii=False, indent=0)
    print(f"exported to {out}: {len(asks)} asks, {len(threads)} threads, {len(attention)} for attention, "
          f"{len(branches)} branches, {len(recent)} recent decisions")
    return 0


# ---------------------------------------------------------------------- main
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("show", "ls", "tree", "log"):
        s = sub.add_parser(name)
        s.add_argument("id")
        s.add_argument("--all", action="store_true")
    sub.add_parser("area").add_argument("name")
    sub.add_parser("find").add_argument("words", nargs="+")
    sub.add_parser("status").add_argument("--owner")
    sub.add_parser("brief")
    sub.add_parser("digest").add_argument("--limit", type=int, default=8)
    sub.add_parser("pack").add_argument("ids", nargs="+")
    s = sub.add_parser("new")
    s.add_argument("kind")
    s.add_argument("--title", required=True)
    s.add_argument("--owner")
    s.add_argument("--parent")
    s.add_argument("--text")
    s.add_argument("fields", nargs="*")
    s = sub.add_parser("set")
    s.add_argument("id")
    s.add_argument("fields", nargs="+")
    s = sub.add_parser("link")
    s.add_argument("id")
    s.add_argument("edge")
    s.add_argument("other")
    s.add_argument("--reason")
    s = sub.add_parser("close")
    s.add_argument("id")
    s.add_argument("--by", required=True)
    s.add_argument("--note")
    s.add_argument("--state")
    s.add_argument("--answer")
    s = sub.add_parser("decide")
    s.add_argument("--rule", required=True)
    s.add_argument("--area")
    s.add_argument("--quote", required=True)
    s.add_argument("--closes", nargs="*")
    s.add_argument("--replaces")
    s.add_argument("--parent")
    s.add_argument("--proposal")
    s.add_argument("--series")
    s = sub.add_parser("commit")
    s.add_argument("-m", required=True)
    s.add_argument("--type", choices=TYPES)
    s.add_argument("--thread")
    s.add_argument("--body")
    s.add_argument("--builds", help="comma-separated ids the code implements, e.g. D2-229,W-48")
    s.add_argument("paths", nargs="*")
    sub.add_parser("render").add_argument("--check", action="store_true")
    sub.add_parser("check").add_argument("--strict", action="store_true")
    sub.add_parser("migrate")
    sub.add_parser("whoami").add_argument("name", nargs="?")
    sub.add_parser("ack").add_argument("why")
    sub.add_parser("check-commits").add_argument("range")
    sub.add_parser("branches")
    sub.add_parser("vault").add_argument("out")
    sub.add_parser("export").add_argument("out")
    for h in ("stopcheck", "commit-check"):
        sub.add_parser(h)
    a = ap.parse_args(argv)
    c = a.cmd
    if c in ("new", "set", "link", "close", "decide", "commit"):
        sync_from_views()
    if c == "migrate":
        migrate()
        return render()
    if c == "render":
        return render(check=a.check, sync=True)
    if c == "check":
        return check(a.strict)
    if c == "whoami":
        if a.name:
            open(WHOAMI, "w").write(a.name)
        print(agent_name())
        return 0
    if c == "new":
        cmd_new(a.kind, a.title, a.owner, a.parent, a.text, a.fields)
        return 0
    if c == "set":
        return cmd_set(a.id, a.fields)
    if c == "link":
        return cmd_link(a.id, a.edge, a.other, a.reason)
    if c == "close":
        return cmd_close(a.id, a.by, a.note, a.state, a.answer)
    if c == "decide":
        cmd_decide(a.rule, a.area, a.quote, a.closes, a.replaces, a.parent, a.proposal, a.series)
        return 0
    if c == "commit":
        return cmd_commit(a.m, a.type, a.thread, a.paths, a.body, a.builds)
    if c == "check-commits":
        return check_commits(a.range)
    if c == "ack":
        open(os.path.join(GITDIR, "records-ack"), "w").write(f"{dt.datetime.now(dt.timezone.utc).isoformat()} {a.why}\n")
        print("acknowledged: the stop check passes for this turn")
        return 0
    if c == "stopcheck":
        from records_hooks import stopcheck
        return stopcheck()
    if c == "commit-check":
        from records_hooks import commit_check
        return commit_check()
    web = Web()
    if c == "show":
        return cmd_show(web, a.id)
    if c == "ls":
        return cmd_ls(web, a.id, a.all)
    if c == "tree":
        cmd_tree(web, a.id)
        return 0
    if c == "log":
        return cmd_log(web, a.id)
    if c == "area":
        return cmd_area(web, a.name)
    if c == "find":
        return cmd_find(web, a.words)
    if c == "status":
        return cmd_status(web, a.owner)
    if c == "brief":
        return cmd_brief(web)
    if c == "digest":
        return cmd_digest(web, a.limit)
    if c == "pack":
        return cmd_pack(web, a.ids)
    if c == "branches":
        return cmd_branches(web)
    if c == "export":
        return cmd_export(web, a.out)
    if c == "vault":
        return cmd_vault(web, a.out)
    return 1


if __name__ == "__main__":
    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    sys.exit(main())
