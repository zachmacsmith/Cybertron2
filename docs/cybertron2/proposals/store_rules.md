# Stores in the book of standing rules: where goods go, where they are kept, what is taken first, what is moved

**Status:** accepted in part: D2-274 (22 Nov 2026). Labour rates provisional; the rest open below.
**Owner:** 37.2 for this part; the standing rules as a whole are 37.4's (proposals/standing_rules.md, OPEN W-37), named on any merge.
**Related:** stores (D2-272; hunt_fish_materials.md §7.4), acts on owned things (Q-80), fallbacks as a standing setting (L-142),
households as shared rule books (L-151), travel in the rules (L-152). The design: docs/review/37_growth/02zzzh_hunt_fish/store_management.md.

## Summary

One book of standing rules per household (set by its head) and per person, for eating and for stores alike (D2-274). It says four
everyday things: where incoming goods go; where things are kept and what is held back; what is taken or eaten first; what is moved,
and by whom. The engine applies a few obvious defaults only where the book says nothing. Labour is charged only where moving is real.
Agents see their rules and what the rules did.

## The proposal

- **Precedence:** an act in a turn, then the person's own rule, then the household's, then the engine's default; going against a
  household rule is recorded and noticed. A person may override their own defaults (D2-274).
- **The grammar:** a rule is one record, set by a free `rule` act in the agent's own sentence and shown back as the engine reads it:
  the rule (go, keep, hold back, first, eat, move, drop); the goods (an item, a kind, everything); where (a building, a room or
  storey, a container by tag or kind, hands; and from, for moves); and qty, before, who, by, unless (someone is starving, winter, it
  is full). The most specific rule wins, then the person's over the household's, then the newer. A rule that cannot be followed falls
  back to the defaults and says so. A rule naming a place no longer held lapses.
- **Read at five moments:** goods arrive (go); a store's goods change (keep, hold back); drawing for eating, making, giving, paying
  (first, hold back); the night's meal (eat: order, rations, who first, guests); a person's spare units (move chores).
- **The defaults:** goods come home to where one lives; inside a building each good goes to the best container or space with room;
  when full, the household's next store at the place, then the door, with a line saying so; drawing: hands, home, other household
  stores, door piles, food needing no fire first, then the most perishable, full rations, guests fed by the host; nothing held back,
  and the evening says so; **a store built for a kind writes its own droppable rule** (a granary for grain, a woodshed for fuel, a
  byre for fodder) (D2-274); **no default for putting carried goods away at night**: people set their own (D2-274); never between
  households by rule; a locked chest is outside every rule but its key holders'.
- **Labour (provisional, D2-274):** free within a building (rooms, storeys, cellar, containers), on arrival to any household store at
  the place, and drawing for a meal or an act; between buildings about 1 unit per 800 kg per parcel step (a quarter on the same
  parcel), a handcart three times a trip, a pack ox six; move chores done from spare units only (D2-274), never from a plan.
- **Visibility (D2-274):** each person sees their current rules, how to change them, what they can set, and each time something is
  moved or drawn by a rule; chores a rule would have done but no one did are shown. By default a line per store; by attending to it,
  each container's fill, state and life, last night's spoilage and vermin losses with their signs, what is held back, the locked
  chests, the rules in force and what they did. Facts, never advice.
- **A fault the design fixes:** work done for a household goes to its first-claimed building (`here.party_container`), so a granary
  built later never receives a harvest (pw1: 10 grain in the Reed Granary while 96 lay outside the house door).

## Seeded knowledge (D2-279)

The system prompt gives the rules' grammar and nothing more; how to manage a household (where to keep what, what to hold back, what
to eat first in a hungry spring) is seeded as starting memories, chiefly for the head, who may pass them to the heir. The locked chest
is deferred (L-156).

## Open questions

1. A cap on rules (about 12 a household and 6 a person proposed), or none?
2. May any member change the household's rules, and do rules pass to a household a member founds (with L-151)?
3. The labour rates, once timber and goods are in kilograms.
4. Travel in the same book (L-152): what one eats and does on the road, when to push on or turn back.

## History

- 23 Nov 2026: accepted in part: D2-339 (The household book's grammar: five kinds and drop. set (name; people, goods or p).
- 23 Nov 2026: accepted in part: D2-338 (The household book has named sets as a primitive: a household (or a person) name).
- 23 Nov 2026: accepted in part: D2-337 (Standing rules are written in a stated grammar the prompt gives in full (each ki).
- 23 Nov 2026: accepted in part: D2-319 (Rules can be changed at any time by a free act and also in the evening talk unde).
- 22 Nov 2026: accepted in part: D2-301 (A person's own rules and standing fallback come before every household chore, ke).
- 22 Nov 2026: accepted in part: D2-296 (Fallbacks are assignable by the household's standing rules: the head divides the).
- 22 Nov 2026: accepted in part: D2-282 (Standing rules support conditional actions conditioned on state changes: a rule ).
- **22 Nov 2026:** written by 37.2 as the proposal for D2-274 (Zach's answers: "1. yes. 2. yes. 3. I don't think default ... 4. sounds
  ok for now but don't mark as final 5. chores from spare sure, idk about the cap. There should be visibility into chores that usually
  would happen but no-one did ..."), from store_management.md, under D2-277.
- **22 Nov 2026:** seeded knowledge added (D2-279); the locked chest deferred.

## Sources

docs/review/37_growth/02zzzh_hunt_fish/store_management.md, storage.md; proposals/standing_rules.md (37.4's).
