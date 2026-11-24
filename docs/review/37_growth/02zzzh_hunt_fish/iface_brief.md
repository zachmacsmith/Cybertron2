# Brief: the interface from one registry (thread W-109)

You are a build subagent of session 37.2 on Cybertron 2. Work ONLY in the git worktree `/home/user/c2-iface` (branch
`w109-interface`, made from `main`). Never edit the main checkout. Do not push or merge. Commit on the branch in small commits, and
often; each message's last paragraph is exactly:

```
Agent: 37.2
Thread: W-109
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

No other trailer lines. No model calls, no live runs, no Hugging Face; bot runs only to test interfaces (D2-298).

## Why

The rebuilt prompt (stage 4, W-100) stopped rendering the acts from their table (`verbs.VERB`: 40 handlers, each with args, doc,
cost) and put eleven hand-written sentences in its place (`shapes.SHAPES`); every act not written into a sentence vanished or became
a word (try for a child, partner, meet, watch, write, erase, withdraw), the "ways" (`MODIFIERS`, 23: hunting range and parties,
building fine or grand, a pack ox) are rendered nowhere, techniques show their key name with the label stripped, and crafts
everyone knows show no inputs. Full list: `docs/review/37_growth/02zzzh_hunt_fish/prompt_compare.md`; the two prompts side by side
in `iface_ref/`; session bench's audit there too. The old prompt (`prompt.py` `verb_lines`, `MOD.lines`) read the table and was
complete, but showed everyone everything and carried world mechanics in its descriptions.

## The rules (binding)

- **D2-350:** every act and every technique a person can take is registered with required descriptions: its interface (what it
  does, how it is said, its arguments and every option, its cost) and what it needs, shown to each person at the detail their
  familiarity gives; one without them is a build error. Shapes organise: every act is listed under its shape on a line of its own,
  never folded into another act's sentence.
- **D5-2** (Zach, 24 Nov, recorded by session bench): "interface is not world": every act with what it does and its options, every
  technique of the person's with what it does; only the world (yields, seasons, ecology, where things are) left to memory and
  seeded lines.
- **D2-314:** the eleven shapes stay as the organisation (go, gather, set, tend, make, work, build, move, change, agree, force), each
  with its grammar line; the handlers stay underneath; old worlds keep the old prompt. **D2-263:** what each level of a craft shows.
  **D2-286:** no "what you could do today" list. **D2-341:** rules are not attendable.

## Build

1. **One registry, read by the renderer.** Every act (`verbs.VERB`), every technique (`data.TECHNIQUES`) and every way
   (`MODIFIERS`) carries required interface fields: its shape; one line of what it does in interface terms (what happens when you do
   it, not what the world yields); its arguments, each option with what it does; its cost in units; what it needs (a tool, a place,
   a fitting, materials, a partner, the same day); who is shown it (always; by stage; by holding a thing; by knowing it; by an
   office such as head); and its detail by familiarity (aware: its name and who does it; rough: what it does and what it needs;
   known or capable: inputs and batch, output, units, place, what a tool does to it, its ways). Keep the fields in the existing
   tables where they live, as data; add a loader check that raises for any entry missing a required field, so an undescribed act
   cannot be built.
2. **World out of the interface.** Audit the descriptions the old prompt used (`VERB[...]["doc"]`, the techniques' labels,
   `manual` and `note`) and split them: the interface stays in the registry; world facts (yields, firewood a kg, keeping times,
   seasons, what lives where) go to the seeded lines or stay as the engine's own; list each move in the report.
3. **The renderer.** Replace `shapes.lines` with a renderer that reads the registry: under each shape, each act and each of the
   person's techniques on its own line at their familiarity's detail, with its options and cost; the family acts (try, partner,
   care, watch, teach, learn) and the social ones (meet, come, write, erase, withdraw, join, admit, host, grant) listed like any other;
   the free reply fields as now. Keep `rules` as the only way to write a rule (the old `rule` act's kinds are stale beside D2-339:
   say so in `change` or retire the face). `look_up` back in the reply format. Crafts only known of kept apart from the doable ones.
   `go`'s four acts each on their own line.
4. **Who sees what, generally:** the visibility conditions from the registry (not ad hoc in the renderer): e.g. `set` whenever one
   knows a gear craft or holds gear, care whenever there is a child one may care for, try for a grown person of an age to, the
   head's acts for a head; a youth's and a child's lists by stage.
5. **Tests:** every handler in `VERB` and every option in its args and in `MODIFIERS` appears in the rendered prompt of some fixture
   person who can use it (a farmer head, a fisher, a youth, a parent, a lone newcomer), on Eelmouth and on session bench's World 0b
   founder Osric if its spec is reachable (else a fixture like him); the loader check; the render sizes per person reported (old
   about 7,200 words, rebuilt core about 2,000); an act refused for a missing argument the prompt does not show (sowing without
   "item", `farm.py:931`) is a test failure.
6. **Replay:** replay real replies from live run 1 (`/home/user/live1/live1_A_new`, `live1_B_new` turns.jsonl) through the
   shapes' parser against the new renderer, and report every reply that parses differently; nothing may be refused that was
   accepted before, unless the report says why.
7. **The suite** in six shards (`ls tests/test_cybertron2_*.py | split -n r/6`), all passing; a 4-day bot run of Eelmouth.

## Report

`docs/review/37_growth/02zzzh_hunt_fish/iface_report.md`, committed: the registry's fields and where each lives; every act and
technique that lacked a field and what was written; the world facts moved out; Osric's and Peter's prompts before and after (files
beside the report); the coverage test's table; the replay's differences; a "Not done, and why" section listing every designed item
left unbuilt; questions for Zach with the defaults you took.
