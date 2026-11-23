---
id: docs/review/37_growth/02zzzh_hunt_fish/stage4_brief.md
kind: note
updated: "2026-11-23"
---
# Brief: build stage 4, taking and making (thread W-THREAD)

*note · `docs/review/37_growth/02zzzh_hunt_fish/stage4_brief.md`*


You are a build subagent of session 37.2 on Cybertron 2. Build stage 4 of the wave: **signs, people and worlds**, and the world for live run 1. Work ONLY in the git
worktree named in your prompt (branch `w85-s4-people`, made from `main` after stage 3 merged). Never edit the main checkout. Do not
push or merge. Commit on the branch in small commits; each message's last paragraph is exactly:

```
Agent: 37.2
Thread: W-THREAD
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

No other trailer lines. No model calls, no live runs, no Hugging Face; bot runs only to test interfaces ([[D2-298 Bot runs test interfaces and basic functioning only|D2-298]]).

**Read first:** CLAUDE.md; docs/cybertron2/proposals/w73_design/README.md, basis.md, build_plan.md (stage 4 and live run 1),
integration.md; the specs **u8_signs.md, u9_people.md, u11_worlds.md** in full, each opening with a "Decisions since" table that
binds over its text; stage1_report.md to stage3_report.md in docs/review/37_growth/02zzzh_hunt_fish/; docs/cybertron2/guides/senses.md
(every sign); docs/review/37_growth/02zzzj_steering/steering.md §2 and §4 (wording: no horizon word in intent lines, examples from
the person's own crafts); docs/scenario_design.md (the live-run world); feature_packages.md §9.1 and §10.

**Build:**
1. **u8:** the river's nightly record and the four leads (lore, the dawn cue, the run, the catch carried home), each sign grounded in
   state and checked against senses.md and its intended chance; signs for anyone at, passing or attending a full river, finer ones
   for any water craft from rough up ([[D2-325 Some river signs are for anyone|D2-325]]); the shallows' signs (stage 2); keeping's signs (stage 3).
2. **u9:** the core prompt and reply format as u9 §1 writes them (with [[D2-301 A person's own rules and standing fallback come before every…|D2-301]]: the morning line "You rested n units yesterday" only,
   no push for a fallback; "Any units you do not use are wasted" kept until fatigue, B40); the eleven act shapes ([[D2-314 The eleven act shapes are the verb list|D2-314]]) in
   `shapes.py` over the 38 handlers, each with its grammar line and the person's own techniques under it at their level ([[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]]),
   a technique named alone resolving by what stands; learning as one record ([[D2-307 Learning is scaled with the lifespan in every part|D2-307]], [[D2-326 Practice alone can bring a person to known in any craft|D2-326]]: practice alone can reach known, more
   slowly; teaching far faster); founders' seeded lines from templates with capital inside the 20-line budget, written with its
   livelihood ([[D2-311 Seeded memory of a household's capital is part of the founders'…|D2-311]]); the evening line on revisiting rules ([[D2-319 Rules can be changed at any time by a free act and also in the…|D2-319]]); the watch act, widening `guard` to a field, a herd or a
   building by day or night ([[D2-320 Crop protection stays as it is for now|D2-320]]). **Keep today's core prompt and 38-verb list as a world setting** (`prompt: old`, [[D2-331 Live run 1 has a comparison arm|D2-331]]) for
   live run 1's comparison arm, with no new seeded memories in that setting; the options list stays removed in both.
3. **u11:** livelihood rows, holdings, pin and fill, the gate check (people P1 to P21 with stage 2's making checks); **Eelmouth
   remade** ([[D2-316 A runs world means a water-only world|D2-316]] water-only; [[D2-330 The worlds' defaults as proposed|D2-330]]: the Salt House to the Brooks, a rock source in reach, no other village in reach, six traps
   seeded a capable setter and a net to the weir expert, a youth 0.8 food a night), as a world file under cybertron2/specs/, with
   its two live arms (main; `prompt: old` without the new seeded lines) and a bot null arm. Models by scenario_design: Opus at the
   poles (the weir keeper, the salter), Sonnet the middle, Haiku the bulk; the weekly stop at 0.99 ([[D2-334 Live run 1 and the overnight work stop if the weekly usage window…|D2-334]]).
   **From stage 2's gate check (stage2_report.md):** in the runs worlds no one can make a gill net (the weir expert's net cannot
   be remade), there is no stone within a day (M4), and nothing produces bone, so lines need a smith's copper hooks. The remade
   Eelmouth must pass M1 to M8: give a household the net-making craft with cord within reach, the rock source (C2), and seed hand
   lines with hooks where a livelihood fishes by line; list any making check that still warns and why.
   **From stage 3 (stage3_report.md):** there is no hut room kind yet, so a seeded smokehouse can take up to 4 sets: Eelmouth's
   smoke hut must be a wattle hut of 1 set ([[D2-284 A smokehouse's capacity comes from the racks fitted, about 250 kg of…|D2-284]], [[D2-291 A set of smoke racks holds about 250 kg of fish on 1 space|D2-291]]), a timber house by its room size. The book's `when` and `unless` read
   states by keywords; tie the run and river states to u8's record where u6 names them. The rules grammar adds about 105 words to
   every prompt: keep it inside the core's budget (u9 §2.5).
4. **Render and check, without model calls:** the gate check on remade Eelmouth (it must pass; list warnings); a bot dry run of 40
   days; every founder's rendered system prompt and first morning message, for both live arms, written to
   docs/review/37_growth/02zzzh_hunt_fish/live1_renders/ for 37.2 to read.

Check every cited file:line before changing it; follow the spec's intent where the code has moved and note it. Run the test suite
before and after (with a timeout, in the background if long); fix what breaks; update only tests that pin numbers the decisions
replaced, listing each. Run the runs world with bots (`python3 -m cybertron2.engine run cybertron2/specs/nutrition/runs_high.yaml
--bots runs --days 40`): it must run, and the remade Eelmouth must run with bots for 40 days.

**Report:** docs/review/37_growth/02zzzh_hunt_fish/stage4_report.md on the branch, as stage 1's: what was built by file, each
change with its test, numbers changed, tests updated and why, spec drift, what is not done and why, test results before and after,
and the gate check's results on the current worlds. End your reply with a short summary and the branch's commit list.
