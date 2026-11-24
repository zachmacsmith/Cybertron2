---
id: docs/review/37_growth/02zzzh_hunt_fish/iface_ref/prompt_audit.md
kind: note
updated: "2026-11-24"
---
# What the rebuilt prompt no longer shows (24 Nov 2026, session bench, W-202)

*note · `docs/review/37_growth/02zzzh_hunt_fish/iface_ref/prompt_audit.md`*


Zach (24 Nov): "Were there other important things that were tucked away behind shared verbs that aren't really obvious now? …
Check if there are other important things that ended up tucked away."

Method: one founder's system prompt (Osric, World 0b, day 0) rendered under the rebuilt core (`prompt: core`, the eleven act shapes,
[[D2-314 The eleven act shapes are the verb list|D2-314]]) and under the old prompt (`prompt: old`, the 38 verbs), both saved beside this file (`prompt_osric_new.txt`, 2,016 words;
`prompt_osric_old.txt`, 7,174 words). Every engine handler (`verbs.VERBS`, 40) and every option the old prompt offered was looked for
in the new action lines; use is counted from World 0b's four arms (Sonnet 5.5, Haiku 5.5, Haiku 4.5, Sonnet 4.5; days 3 to 18).
All of these still work if an agent writes them ([[D2-314 The eleven act shapes are the verb list|D2-314]]: "the 38 handlers stay underneath"); what changed is whether the agent is
told they exist.

## 1. Acts named nowhere, or only in passing

| Act | Old prompt | New prompt | Used in World 0b |
|---|---|---|---|
| try for a child | its own line | the last phrase of `agree`; "with" optional | 7 tries, almost all Sonnet 5.5 |
| partner | its own line | "partnering", inside `agree` | 0 |
| care for a child (feed it, pass on a line) | under `work`, with food | not in the action list; the morning message only, when caring | 32 to 40 a run for three arms; 0 for Sonnet 5.5 |
| watch (a day beside someone, learning) | its own line | not named (the core says knowledge comes "by watching") | 0 |
| meet (call a gathering) | its own line | not named; `go` mentions "come to a meeting called here" | 0 |
| write, erase (lines on a building) | own lines | not named | 0 |
| rest | its own line | not named | 0 |
| withdraw (an offer) | its own line | not named | 0 |

## 2. Options of an act that are gone from the prompt

| Option | Old prompt | New prompt |
|---|---|---|
| hunting **range**: near, the wood around (about 2.5 km, 1 unit), far (a long day, 3 units) | listed | not shown; fresh ground farther out gives far more game (seeded line HU2) |
| hunting **party**: "alone", "only" (whom to take), "with" (join another's party) | listed | not shown: cooperative hunts are invisible |
| hunting "looking for" one kind | listed | not shown |
| leading a **pack ox** (on a hunt, on the road) | listed | not shown |
| building **fine** or **grand** (seen from next door; materials x1.5 or x4) | listed | not shown |
| an **upper storey**; a room added to a building costs a quarter less | listed | not shown |
| **burial** methods (a cairn, shallow) and burying the dead at all | listed | `cairn` only among builds |
| what each technique **does** ("snare: catches by night for a few nights: come back…", "drive: dangerous alone") | a phrase each | names only, with level, units and covers (by design: what each level is shown, [[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]]) |

## 3. Reading

- The eleven shapes are a regrouping of the same 38 handlers, which buys a prompt about a quarter as long. The cost has fallen on
  the acts of **family and passing on** (try, partner, care, watch, teach and learn) and on **social and status** acts (meet, write,
  fine and grand building, party hunts). Work acts keep their visibility, each technique listed with the person's skill.
- In a benchmark scored on living descendants, with knowledge meant to cross generations, those are the levers. Sonnet 5.5 never
  cared for a child; no arm watched anyone, called a meeting, partnered, hunted far, or hunted in a party.
- The descriptions of techniques (row 8) may be deliberate ([[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]]: what each level is shown); the rest reads as the shapes'
  wording leaving them out rather than a decision to hide them.

## 4. Proposed (not decided; Q-216, amends [[D2-314 The eleven act shapes are the verb list|D2-314]]; 37.2's code)

Keep the shapes' grammar. Give the acts of family and passing on their own visible lines again (try, partner, care, watch), name
`meet`, `write` and `rest` in the shapes they belong to, and show each act's options (range and party for hunting; fine, grand and
storey for building; pack ox; burial), at the same weight as the work acts and no more.
