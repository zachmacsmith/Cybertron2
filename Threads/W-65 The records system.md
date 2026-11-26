---
id: W-65
kind: thread
state: active
updated: "2026-11-20"
---

# The records system (W-65)

*active · 37.2 · touched 20 Nov (6 days ago)*

> **Next:** the header pass over the spec files and proposals; run threads labelled as such, with their branch ([[D2-238 Branches|D2-238]]); check the desk once opened, and after the 22 Nov refresh

## What it is
Tracking threads automatically (Zach, 20 Nov: "Go build it", after 02zzp): a structured thread registry (threads.yaml) WORK.md is generated from, a session-start brief and a stop check as Claude Code hooks, truth checks on every push to main, and a status page refreshed weekly

## Done so far, and what is left
built and on main 20 Nov (d2b130c to fdd1edb): tools/records.py and records_hooks.py; 627 rows moved into docs/cybertron2/items/ with every cell kept (duplicates renamed [[W-28b Build brief 4b written|W-28b]], [[W-34b Worlds for the population benchmark, the peoples variant|W-34b]], [[W-38b What went wrong building the peoples worlds, from properties to a…|W-38b]], [[W-39b Prototype of generation_redesign.md §4.3 and §4.5 for people|W-39b]], Q-24b); OPEN, WORK and DECISIONS rendered views that take in hand edits; the skill; the hooks in .claude/settings.json (session brief, commit check, stop check); the push workflow (checks, branches, hygiene, the Obsidian vault rebuilt on the branch vault after every push ([[D2-240 The Obsidian vault is a local folder Zach opens whenever he likes…|D2-240]])); the desk page (Data artifact MAn9WhTy6gGjpjcL3duoVm) with a weekly refresh (trig_016fSQnMbvyS2V8m9Mi4zh64, Sundays 19:17 UTC); tests/test_records.py.

**Left:** headers with summaries on the spec files and proposals ([[D2-234 Documents in the web|D2-234]]; derived until then); the desk unverified until opened, its refresh until 22 Nov; the hooks load only in sessions started in the repository (this one runs from /home/user)

## Where
- `tools/records.py`
- `tools/records_hooks.py`
- `docs/cybertron2/items/`
- `.claude/`
- `.github/workflows/records.yml`
- the desk page


## Linked
- under it: [[D2-240 The Obsidian vault is a local folder Zach opens whenever he likes…|The Obsidian vault is a local folder Zach opens whenever he likes… (D2-240)]] (live)
- under it: [[D2-253 Zach's decisions about the process and its mechanisms are kept…|Zach's decisions about the process and its mechanisms are kept… (D2-253)]] (live)
- under it: [[D2-254 Everything shown to Zach names each question, proposal, thread or…|Everything shown to Zach names each question, proposal, thread or… (D2-254)]] (live)
- under it: [[D2-285 The records brief is run by hand after each compaction for now, since…|The records brief is run by hand after each compaction for now, since… (D2-285)]] (live)
- under it: [[D2-300 Every item Zach defers or flags is tagged with the prospective…|Every item Zach defers or flags is tagged with the prospective… (D2-300)]] (live)
- under it: [[O-1 A first wiki generated from the spec as it stands, as a private page…|A first wiki generated from the spec as it stands, as a private page… (O-1)]] (open)
- under it: [[Q-65 Delete the 16 empty branches|Delete the 16 empty branches (Q-65)]] (closed)
- under it: [[Q-67 Confirm three rules the sessions follow without your own words behind…|Confirm three rules the sessions follow without your own words behind… (Q-67)]] (open)


## Mentioned by
- [[D2-240 The Obsidian vault is a local folder Zach opens whenever he likes…|The Obsidian vault is a local folder Zach opens whenever he likes… (D2-240)]]
- [[D2-253 Zach's decisions about the process and its mechanisms are kept…|Zach's decisions about the process and its mechanisms are kept… (D2-253)]]
- [[D2-254 Everything shown to Zach names each question, proposal, thread or…|Everything shown to Zach names each question, proposal, thread or… (D2-254)]]
- [[D2-285 The records brief is run by hand after each compaction for now, since…|The records brief is run by hand after each compaction for now, since… (D2-285)]]
- [[D2-300 Every item Zach defers or flags is tagged with the prospective…|Every item Zach defers or flags is tagged with the prospective… (D2-300)]]
- [[Q-65 Delete the 16 empty branches|Delete the 16 empty branches (Q-65)]]
- [[Q-67 Confirm three rules the sessions follow without your own words behind…|Confirm three rules the sessions follow without your own words behind… (Q-67)]]
- [[W-3 Records restructure|Records restructure (W-3)]]
- [[L-129 A wiki of the world's rules, generated from the development process…|A wiki of the world's rules, generated from the development process… (L-129)]]
- [[O-1 A first wiki generated from the spec as it stands, as a private page…|A first wiki generated from the spec as it stands, as a private page… (O-1)]]
- [[Records and workflow how the documents, the scripts and git carry…|Records and workflow: how the documents, the scripts and git carry…]]
- [[Thread tracking a registry, hooks, checks and a commit schema|Thread tracking: a registry, hooks, checks and a commit schema]]
- *and 2 index or audit notes*
