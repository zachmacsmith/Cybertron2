---
name: records
description: Record and query cybertron2's design records (threads, asks, offers, deferrals, decisions, documents) with tools/records.py. Use whenever Zach decides something, work starts, pauses or finishes, something is left open or promised, before any status answer ("what is in progress", "is X done"), before designing in an area, when handing work to another agent or subagent, and to commit.
---

# The records (D2-232 to D2-239)

Every record is a node. Small nodes are **items**, one file each in `docs/cybertron2/items/`:

| Prefix | Kind | Example |
|---|---|---|
| W | thread (work) | W-65 |
| Q | ask | Q-63 |
| O | offer or promise | O-1 |
| L | deferred | L-129 |
| C | conflict | C-11 |
| D2, D4, D1, H | decision | D2-239 |

Large nodes are **documents**: spec files, proposals and session notes, where they already are.

OPEN.md, WORK.md and DECISIONS.md are **views rendered from the items**. Never edit them by hand: their prose lives in
`docs/cybertron2/items/_views/`, and `records render` writes them.

Run everything from the repository root: `python3 tools/records.py <verb>`. Each event is **one call**. Record only what outlives the
turn. A question you answered in the turn, an explanation, or a fix that is committed needs nothing more.

## Which call for which event

| Event | Call |
|---|---|
| Work starts | `new W --title "..." [--parent W-n]`, then `set W-n state=active next="..."` |
| The next step changes, or the work is set aside | `set W-n next="..."`; `set W-n state=paused notes="done ...; left ..."` |
| Work finishes | `close W-n --by agent --note "what it passed"`. It refuses while open children remain: move each (`set X parent=W-m`), close it, or `set X revisit="why"` |
| You promise or offer something ("I'll ...", "shall I ...") | `new O --title "..." --parent W-n default="do it" default_on=YYYY-MM-DD` |
| A question for Zach | `new Q --title "..." --parent W-n recommend="..." default="..." default_on=YYYY-MM-DD` |
| Zach flags something for later | `new L --title "..." --parent W-n waits_on_text="..."` |
| Zach decides (his own words only) | `decide --rule "the rule, stated as a rule" --area economy/production --quote "his words" --closes Q-n [--replaces D2-k] [--parent W-n] [--proposal proposals/x.md]` |
| Something resolved that Zach did not settle | `close Q-n --by agent --note "why"`, or `--by default` or `--by relayed`. These are provisional. Never `--by zach` without `--answer "his words"` |
| Link two nodes | `link X waits_on Y`; `link X relates Y --reason "why"`. Edges: parent, waits_on, blocks, replaces, decides, relates |
| Commit | `commit -m "<what>" [--thread W-n] [--type build] [--builds D2-k W-n] [paths...]`. It stages the records and the paths and writes the type, subject and trailers. Typed `git commit` must carry `Agent:` and `Thread:` in the last paragraph (the hook checks) |

## Reading

| Call | Shows |
|---|---|
| `status [--owner 37.2]` | the live threads with their next steps, asks, provisional closes, branches no thread names. **Every status answer comes from here, not from memory.** |
| `show <id or path>` | the node in full (a document: its summary, outline, decided lines and open questions), its links one line each, what mentions it, and a "links newer" flag |
| `ls <id> [--all]` | everything linked, one line each |
| `tree W-n` | the thread's sub-threads and items |
| `area <spec area>` | every decision in it, and the open items |
| `find <words>` | search |
| `log <id>` | recent commits on the node and its direct links |
| `digest` | Zach's asks, the most waited-on first. At most about 8, one choice each, with a recommendation and a default |
| `pack <ids...>` | the context to hand to another agent, a new thread or a subagent. Paste its output into their prompt |
| `brief` | runs at session start and after each compaction. Read it before working |

## Rules

- **Name things for Zach by description first** (D2-254): "the nutrition worlds' livelihoods and levels (Q-66)", never a bare
  id. When you create an item, give it a `title` that says accurately what it asks or does, in plain words.
- **A process decision** goes to `--area process/how_we_work` (D2-253).
- **Decisions only on Zach's own statement,** quoted. A "sure" to your recommendation is "default taken" (`--by default`), not a
  decision.
- **Every new ask, offer and deferral has a parent thread.** Every code change has a thread (D2-237).
- **Before designing in an area,** run `area <name>` and `show` its documents.
- **A promise left in a reply with no record is sent back** by the stop check. Record it, or run `ack "why"` if it is already
  recorded or is not a promise.
- **Set your session once:** `whoami 37.2`.
