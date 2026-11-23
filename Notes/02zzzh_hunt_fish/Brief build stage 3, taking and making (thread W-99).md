---
id: docs/review/37_growth/02zzzh_hunt_fish/stage3_brief.md
kind: note
updated: "2026-11-23"
---
# Brief: build stage 3, taking and making (thread W-99)

*note · `docs/review/37_growth/02zzzh_hunt_fish/stage3_brief.md`*


You are a build subagent of session 37.2 on Cybertron 2. Build stage 3 of the wave: **keeping, stores and the household book**. Work ONLY in the git
worktree named in your prompt (branch `w85-s3-keeping`, made from `main` after stage 2 merged). Never edit the main checkout. Do not
push or merge. Commit on the branch in small commits; each message's last paragraph is exactly:

```
Agent: 37.2
Thread: [[W-99 Build stage 3, keeping, stores and the household book|W-99]]
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

No other trailer lines. No model calls, no live runs, no Hugging Face; bot runs only to test interfaces ([[D2-298 Bot runs test interfaces and basic functioning only|D2-298]]).

**Read first:** CLAUDE.md; docs/cybertron2/proposals/w73_design/README.md, basis.md, build_plan.md (stage 3), integration.md; the
specs **u4_processing.md, u5_stores.md, u6_book.md** in full, each opening with a "Decisions since" table that binds over its text
(u6 §5 was rewritten to [[D2-301 A person's own rules and standing fallback come before every…|D2-301]]: a person's own rules and fallback before every household chore; units left are rest);
stage1_report.md and stage2_report.md in docs/review/37_growth/02zzzh_hunt_fish/ (what is built, what was left to this stage);
37.4's docs/cybertron2/proposals/standing_rules.md and the spec's standing orders ([[D2-313 For this wave|D2-313]] gives 37.2 their files for this wave);
docs/cybertron2/guides/senses.md (for keeping's and vermin's signs); feature_packages.md §9.1 and §10.

**Build:**
1. **u4:** processing containers as one unit (`PROCESSES` rows, containers with `holds` in kg, lots, one night step replacing
   `keeping.night` and the rack code): the keeping smoke, the hard cure, salting at once in the salting tub, the hearth rack, the
   hot smoke as a day act; each depth a good (stage 1 added the goods); the smokehouse's capacity ([[D2-284 A smokehouse's capacity comes from the racks fitted, about 250 kg of…|D2-284]], [[D2-291 A set of smoke racks holds about 250 kg of fish on 1 space|D2-291]]) and work floor,
   its fire tended (one `tend` act on a placed thing, basis §6), fuel by the kg loaded; a done lot stays in its container (B8).
   **Tanning, liming and retting's tanning rows are out ([[D2-327 Tanning and leather are deferred from this wave until the rest is…|D2-327]]);** retting flax stays if u3's flax is built.
2. **u5:** stores as spaces and containers, each container's capacity in kg and the risks it removes ([[D2-272 A food's base rate of spoiling is its rate when well kept|D2-272]], [[D2-279 Stores, as answered|D2-279]]); the
   remaining store multipliers that slow food below its base removed (stage 1 left them); `alloc` deterministic; vermin by
   exposure and sudden illness as u5's first magnitude (B13); containers by kind and building (B14).
3. **u6:** one book per household and per person (`book.py`): go, keep, hold back, first, eat, move, tend, chore, drop, with
   `when` and `unless` on lasting states the household knows ([[D2-282 Standing rules support conditional actions conditioned on state…|D2-282]]); the spare-units phase after every plan, person by person,
   own rules and own standing fallback first, then the household's keeping chores, then the head's fallback chores ([[D2-301 A person's own rules and standing fallback come before every…|D2-301]],
   [[D2-296 Fallbacks are assignable by the household's standing rules|D2-296]]); no fallback at the start and nothing pushing for one; units left are rest ("You rested 2 units yesterday."); rules
   changed any time by a free act and in the evening talk ([[D2-319 Rules can be changed at any time by a free act and also in the…|D2-319]]); visibility: the rules block, what fired, what was missed,
   what waits; a chore may be any act a fallback may do, production included (B15).

Check every cited file:line before changing it; follow the spec's intent where the code has moved and note it. Run the test suite
before and after (with a timeout, in the background if long); fix what breaks; update only tests that pin numbers the decisions
replaced, listing each. Run the runs world with bots (`python3 -m cybertron2.engine run cybertron2/specs/nutrition/runs_high.yaml
--bots runs --days 40`): it must run, and a bot household must hang, salt, tend the fire and take down through a run, by rules.

**Report:** docs/review/37_growth/02zzzh_hunt_fish/stage3_report.md on the branch, as stage 1's: what was built by file, each
change with its test, numbers changed, tests updated and why, spec drift, what is not done and why, test results before and after,
and the gate check's results on the current worlds. End your reply with a short summary and the branch's commit list.
