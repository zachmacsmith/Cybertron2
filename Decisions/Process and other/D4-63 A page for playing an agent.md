---
id: D4-63
kind: decision
state: live
updated: "2026-11-20"
---

# A page for playing an agent (D4-63)

*live · 31 Oct*

## The rule
**A page for playing an agent:** `serve` shows a person exactly what the model would be shown, and a form built from the request's reply schema and the verb registry (a verb from a list with only its own arguments, lists where the schema closes them, free text typed); the reply is the same JSON, checked against the schema; `serve RUN --new WORLD --as NAME` starts a run with that person played

## Where it came from
conversation ("show me the verbs I can choose and then I just type the things that are fully freeform"); proposals/play_page.md (retrospective)

## What it replaced
R3's bare page, where the whole reply was typed as JSON


## Mentioned by
- [[A page for playing an agent|A page for playing an agent]]
- [[Proposal the verbs, and what each agent is shown|Proposal: the verbs, and what each agent is shown]]
