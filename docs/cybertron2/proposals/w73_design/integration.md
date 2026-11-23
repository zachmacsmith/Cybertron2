# The integration review (23 Nov 2026)

**By:** 37.2, reading the eleven specs against each other, basis.md and the decisions to D2-303, by their text (the interfaces
between units, the shared records and words, the code each changes), not their authors' summaries.

## Fixed in this review

| # | What | Where it was | Fix |
|---|---|---|---|
| 1 | The fallback's order: u6 ran the household's keeping chores before a person's own fallback, against Zach's D2-301 | u6 §5; u9 §1.5's morning line nudged people to set a fallback ("units ... go unused") | u6 §5 rewritten person by person: own rules and own fallback first, then the household's chores; u6 §6 and u9's line say units left are rest, with no push |
| 2 | `tend` used two ways: going back to set gear (u2, u9, D2-294) and tending a container's fire (u4's `tend the smoke`, u6's `tend` rule) | u2, u4, u6, u9 | one act on any placed thing that runs over nights (basis §6, default; questions B41) |
| 3 | The gear piece record: u2 `{life, torn}`, u3 `{life, rot, of, barked}` | u2 §2, u3 §3 | one record with all five (basis §6; questions B42) |
| 4 | No spec held stage 1's code, though every spec deferred to "U0": the goods resize, fuel a night, the keeping curve's rates, the clock conversions, the floor and batches, the misleading faults | u1, u3, u4, u5, u7, u9, u11 | u0_basis.md written |
| 5 | `capital_units` called two ways (u3 `(hours, w)`, u7 `(row, w, n)`); `batch_of` defined nowhere | u3 code table, u7 §1 | u7's signature; `batch_of(row, w)` in u0 §4 |
| 6 | Tanning's nights: u4 had lime 3 and tanning 16 to 24; u10, which owns them, lime 2, light 16, heavy 32 | u4 §2 | u4 aligned to u10 |
| 7 | The weir's cost from an unsourced hours model | u7 §3 | D2-302's numbers; the model kept as replaced reasoning |
| 8 | Trap and weir holds called "units" on the basis sheet | basis §4 | kg, as the code holds them (data.py:365) |

## Checked and consistent

- The cured goods' names across u3, u4, u5, u6, u9, u11 (smoked, hot-smoked, hard-cured, salt and dried fish and meat).
- Ice states (`open`, `edges`, `over`) between u1 and u8; a run's bands between u8 and u6's states (what the household has seen).
- Seeded gear (u11: six traps a capable setter) against one set laying up to 6 (u2, D2-264).
- The lore lines' numbers against the data (u9 FI4's spate and flood wrecks against `methods.py`'s 0.5 and 0.85; keeping figures
  said from the curve, not "half gone").
- The stages: u7's 1, 2 to 4, 5a to 5c sit inside the README's order; u3's floor and batches and u11's gate check in stage 1 and 4.

## Open from the review (in questions.md)

- A12: the wild's rates still on the day clock (u0 §7), D2-273 against D2-297.
- B41, B42: the two defaults above.

## Still to do

- **The hand-off to 37.4:** most code changes land in 37.4's files (verbs, clocks, prompt, view, night, buildings, the standing
  rules). One board post when Zach has answered questions.md's section A, listing each change by file with its spec (D2-239).
- **The staged build plan in detail:** each stage's changes, tests and the live runs that read it, once section A is answered.
- What this review did not do: re-derive every number in the specs, or check every file:line they cite against the code. The build
  checks each line as it changes it.
