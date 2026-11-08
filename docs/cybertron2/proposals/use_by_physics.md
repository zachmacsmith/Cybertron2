# Proposal: what is physically possible is possible; the consequences are social

**Status:** part 1 retrospective, accepted: D4-114 (8 Nov; built). Part 2 (the audit of claims) discussion. **Owner:** 37.4.
**Affects:** engine/farm.py, herds.py, verbs.py, lore.py, data FENCES; spec/world/holding.md, spec/core/processes.md;
economy/livestock.md (37.2's: OPEN Q-30).

## Summary

D4-23 already says the engine enforces only possession: claims are records, and using land against one is seen, never refused.
The Brookend run (p1) found places where the engine broke that, and others where its rules wasted the people's work:

1. **The ox the stones would not take.** The Crofts lent the Millers an ox, then gave it to them outright for days; the stones
   still refused it ("the ox on the Green is still yours, not one we may use"), because working beasts needed the `access` right.
   Hugh paid back the bread it had bought. Built: any beast at the place can be worked, whoever holds it; another's is seen.
2. **Fences on a season clock.** 137 acts (11% of all) went into three fences, none standing at the end: a wood fence lost a
   level a season (8 days) unless a quarter of its build went into mending each season, a fallen one was rebuilt from nothing,
   and one finished the day before a season turned lost a level at once. Built: by the year, safe in its first year, half kept.
3. **The lore named one window.** "Sow barley in spring" kept everyone from resowing after the summer harvest, though barley sown
   early in summer gives 0.85 of a full crop; nobody sowed in 32 days. Built: each crop's best and good halves of the seasons.

## Why (Zach, 8 Nov)

- "fix the ox lending, fences, lore and Green, then rerun"
- "I feel like the general default should be that anyone can use a thing if they physically could. Claims shouldn't be stopping
  people. Instead, it should be that socially it doesn't make sense. Claims should often not be enforced ... if it is physically
  possible it should be possible. The consequences are then social."
- On the fences: "137 fencing actions seems kind of insane?"

## The proposal (part 1, as built)

- farm.usable_herds: every herd here with the beasts needed, one's own or nobody's first; farm.beasts_note: an event naming
  whose beasts were worked, concerning their holders, and the words on the result (millstones, plough). A pack ox: any ox here
  (one's own first), seen if another's.
- FENCES wood: `mend` 0.25 a year (clocks: year), `kept` 0.5; herds._fences: the level falls at the year's turn, not in the
  fence's first year; farm._fence: a fallen fence restarts from half its build.
- lore.sowing_times: by halves of the seasons, best (within 5%) and well (3/4 of a full crop): "Barley does best sown in spring,
  and well early in summer or late in winter; rye does best sown late in autumn, and well in summer or early in autumn; beans do
  best sown early in summer, and well in spring; rye wants a winter; sown at other times, crops come up poor or not at all."
- Brookend (specs/make_plenty.py): the Green at size 4 (room to build), 48 days, children on.

## Part 2: the audit of claims (discussion, 8 Nov)

**How claims work now.** A claim is a record {thing, claimant, rights, grounds, since, until} (world.add_claim). Rights are any of
access, withdrawal, management, exclusion, alienation. `World.rights(name, thing)` is the union of the claims that name the person,
"anyone", or their household (a member gets access and withdrawal; the head everything the household holds). The spec (D4-23) and
the prompt both say the engine enforces only possession: "Anyone can use anything they can reach, but using what others hold is
seen and remembered." Most of the engine does that: sowing, reaping, grazing, felling and drawing from others' land go ahead with a
note and an event (verbs._against); claiming land another holds is allowed (a dispute); sleeping in another's house is allowed and
noted; taking from another's store goes ahead as a theft that may be seen (settle.settle_thefts).

**Where the engine still refuses for want of a right** (each against the principle unless marked keep):

| # | Act | Now | Under the principle |
|---|---|---|---|
| 1 | `move` goods between one's hands and a store one does not hold (verbs._store_here) | refused: "not yours to use (to take without the right is theft; to put, leave)" | as `take` and `give` already are: allowed; taking without the right is a theft, seen or not. Today `take` allows it and `move` does not, and `give` puts into any store one can enter while `move` cannot |
| 2 | Goods kept in another's store | the goods become the building's: nothing records whose they are, so the Thornes taking back their own grain from the Mill House was a "theft" (p1) | goods carry a keeper's mark (a lot kept for X), or a storage agreement leg gives withdrawal of those goods; taking one's own back is not theft, and the store's holder taking them is |
| 3 | Opening or barring a door (verbs._set) | only those with management (the head) | anyone at it can; seen. Who may is social (a member barring the head out is a quarrel) |
| 4 | A barred door (world.can_enter) | stops all without access; there is no way to force it | a barred door is a real barrier; add forcing it (work, noise, damage to the door), seen and heard. Access through a barred door stands for being let in |
| 5 | Talking in a building (run.py, say) | refused without access; only those with access hear | who hears is who is there (inside it, or at the place for the open air) |
| 6 | Acting `for` a household one is not of (verbs._give) | refused | keep as a clarity rule (acting for a party is a social role), but say it plainly: take it, then give it |
| 7 | Selling land one does not hold (agreements: alienation) | refused | allow; the buyer's claim records "bought from X", and whether anyone recognises it is social (a fraud is a dispute) |
| 8 | Letting others into a house (host, grant: exclusion) | refused without exclusion | keep: a grant is a record that means something only from one who may give it; physically letting someone in is opening the door (3) |
| 9 | Household offices: admitting, naming an heir, setting children's work (head only) | refused | keep for now: an institution's own rules bind its members (D4-23); flag for the institutions work |
| 10 | Night defaults: sleeping and eating where one has access and withdrawal | defaults, not blocks (`sleep` elsewhere is allowed) | keep: the automatic choice should be one's own; using another's is an act |

**Physical gaps the same audit found** (things the engine allows that are not physically possible):
- Beasts are at the node, not on a parcel, for working them: an ox grazing on the pasture can turn the millstones without being
  brought, and two people can work one ox on the same day.
- A store's goods are counted by the building, so who put what in is lost (2 above).

**Does the social side carry the weight?** Uses against a claim are events that concern the holders, reach their morning
"what concerned you", and become memories; agents decide what to do. Nothing more is enforced. Whether that is enough to make a
claim mean something is the experiment: in p1 nobody broke a claim on purpose; the conflicts came from the engine (the ox, the
stored grain).

**Proposed order:** 1 and 3 and 5 (small: they only stop refusing), then 2 (the storage design), then 4 (forcing a door), then 7.

## Alternatives considered

- **Lending as a grant the engine checks** (a use right passed with the ox): keeps the engine enforcing claims, against D4-23.
- **Fences: lower the mending share but keep the season clock:** the clock is the fault; with 8-day seasons any per-season rate
  is out of scale.
- **Lore: list all seasons with their yields:** too long for a kept line; the two grades carry what a family would pass on.

## Open questions

1. Other rates on a season or event clock that the short year puts out of scale (an audit with the year-length question).
2. Part 2 above.

## History

- 8 Nov: part 1 built at Zach's request after the p1 Brookend run (D4-114).
- 8 Nov: part 2, the audit of claims, written (discussion): ten places the engine refuses for want of a right, two physical gaps.

## Sources

runs/p1_brookend; spec/world/holding.md (D4-23); D2-130; D4-105.
