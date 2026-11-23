# Brief: build stage 2, taking and making (thread W-98)

You are a build subagent of session 37.2 on Cybertron 2. Build stage 2 of the wave: **taking and making**. Work ONLY in the git
worktree named in your prompt (branch `w85-s2-taking`, made from `main` after stage 1 merged). Never edit the main checkout. Do not
push or merge. Commit on the branch in small commits; each message's last paragraph is exactly:

```
Agent: 37.2
Thread: W-98
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

No other trailer lines. No model calls, no live runs, no Hugging Face; bot runs only to test interfaces (D2-298).

**Read first:** CLAUDE.md; docs/cybertron2/proposals/w73_design/README.md, basis.md, build_plan.md (stage 2), integration.md; the
specs **u1_water.md, u2_taking.md, u3_making.md** in full, each opening with a "Decisions since" table that binds over its text;
docs/review/37_growth/02zzzh_hunt_fish/stage1_report.md (what stage 1 built and left: gear as goods, fault 12, gear lives not yet
applied, the bridging `cut withies`, `set {what}`); docs/cybertron2/guides/senses.md (for the shallows' signs);
docs/cybertron2/proposals/feature_packages.md §9.1 and §10 (seams; new code in its own units).

**Build:**
1. **u1:** the shallows as one stock per parcel by water type (D2-317), with their own signs for their own creatures, checked
   against senses.md; the water-only runs world (D2-316): small resident and shallows stocks always present, no switch that removes
   them; ice states as u1 designs them (to be revisited with the environment, L-161); hand fishing in a run by u1's factors.
   **Fowling is out of this wave (D2-318):** no fowling net, no fowling method changes.
2. **u2:** gear as goods (the wicker trap, snares, the gill net, the set line) and **set from the hands** (fault 12): set lays held
   gear, refused with none in hand and naming one's gear standing; **tend** takes the catch from all one's own of that technique at
   the place, re-sets what was sprung, `up` brings gear home (D2-294, D2-304); a consuming act on several of one's own needs a
   named target (D2-304); the set record with its household, pieces and state; household things every member's own (D2-305);
   theft of another's set named (stage 1's wording kept); every taking act's result wording as u2 gives it.
3. **u3:** every made thing of the wave in real kg (basis units) with its batch and the 1-unit floor (stage 1's `batch_of`,
   `act_units`); two lives a piece (uses and rot, one record with u2's placed gear: basis §6 "A piece of gear"), mending (half the
   uses for a tenth of the materials, never rot); lives in nights at 1/11.4 for set gear (D2-310) and **nets about 16 nights**
   until barking returns (D2-329); what a person is shown at each knowledge level (D2-263: inputs with amounts and batch at known
   and capable, inputs as the card has them at rough); the flax strip (questions B35, default: up to a quarter of a plot) and what farm.py
   needs; the willow stock replacing stage 1's bridging `cut withies`; the making gate check (M1 to M8) as a function, run on the
   current worlds and its results listed. **Leather, tanning, bark and barking are out (D2-327).** Materials stay at real hours
   (D2-312).

Check every cited file:line before changing it; follow the spec's intent where the code has moved and note it. Run the test suite
before and after (with a timeout, in the background if long); fix what breaks; update only tests that pin numbers the decisions
replaced, listing each. Run the runs world with bots (`python3 -m cybertron2.engine run cybertron2/specs/nutrition/runs_high.yaml
--bots runs --days 40`): it must run, and a bot fisher must set, tend, wear and remake gear through a run.

**Report:** docs/review/37_growth/02zzzh_hunt_fish/stage2_report.md on the branch, as stage 1's: what was built by file, each
change with its test, numbers changed, tests updated and why, spec drift, what is not done and why, test results before and after,
and the gate check's results on the current worlds. End your reply with a short summary and the branch's commit list.
