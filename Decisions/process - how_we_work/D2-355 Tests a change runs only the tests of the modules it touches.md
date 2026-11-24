---
id: D2-355
kind: decision
state: live
updated: "2026-11-24"
---

# Tests: a change runs only the tests of the modules it touches (D2-355)

*live · 24 Nov · spec: [[process - how_we_work|process/how_we_work]]*

## The rule
**Tests: a change runs only the tests of the modules it touches (and a short bot smoke run where an interface changed); the full suite runs only when a whole stage merges or before a live run. Every brief says so.**

## Where it came from
conversation (24 Nov: "Yes write that up I've been asking you to stop running the full suite so often ... Only run relevant module tests.")


## Mentioned by
- [[The engine's architecture overhauled general mechanisms over typed…|The engine's architecture overhauled: general mechanisms over typed…]]
- [[A stable engine for comparative runs everything built so far tidied…|A stable engine for comparative runs: everything built so far tidied…]]
- [[How we work the process and its mechanisms|How we work: the process and its mechanisms]]
- [[Brief the interface from one registry (thread W-109)|Brief: the interface from one registry (thread W-109)]]
- [[W-109 the interface from one registry report (24 Nov 2026, session…|W-109: the interface from one registry: report (24 Nov 2026, session…]]
