---
id: D1-5
kind: decision
state: live
updated: "2026-11-20"
---

# D1-5 · Storage

*live · 24 Oct · spec: [[record - exchange|record/exchange]], [[record - journal|record/journal]]*

## The rule
one SQLite journal per run (WAL), JSON values, content-addressed compressed texts; Parquet for export, publishing and the site. Adopted with [[D1-4 proposalsrun_record.md is adopted as the spec area record|D1-4]]; Zach was told it is a judgment call (a directory of JSONL files, as cybertron 1, also works)

## Where it came from
Zach, 37.1 conversation; spec/record/journal.md


## Mentioned by
- [[The world keeps the land it runs on|The world keeps the land it runs on]]
- [[Proposal the run record and the run backend|Proposal: the run record and the run backend]]
- [[Export, publish, import|Export, publish, import]]
- [[The journal|The journal]]
- [[02zd cybertron2 as a response to cybertron 1|02zd: cybertron2 as a response to cybertron 1]]
- [[38.29 R1 of the run record built (the journal, and every physical…|38.29: R1 of the run record built (the journal, and every physical…]]
- [[38.34 R5 of the run record built (views, export, import, publish…|38.34: R5 of the run record built (views, export, import, publish…]]
