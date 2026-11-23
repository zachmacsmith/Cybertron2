---
id: docs/cybertron2/proposals/acts_on_owned_things.md
kind: proposal
updated: "2026-11-23"
---
# Acts on held things take the thing as their target, and default to one's own

*proposal · discussion (21 Nov 2026). Nothing decided, nothing built. · `docs/cybertron2/proposals/acts_on_owned_things.md`*

> Every act on a thing someone holds (a set of snares or traps, a herd, a pile, a carcass, a plot, a store) names **the thing** as its target, by its tag or a name one knows ([[D4-68 Short tags, and names given|D4-68]]). With no target named, it touches **only one's own**: one of one's own there, it is that; several, it asks; none, it ref


**Status:** discussion (21 Nov 2026). Nothing decided, nothing built.
**Owner:** 37.2; the verbs and things core (`engine/things.py`, `verbs.py`, `tags.py`, the prompt) are 37.4's, named on any merge.
**Ask:** whether acts on owned things default to one's own ([[Q-80 Whether acts on owned things default to one's own|Q-80]]). **Thread:** fishing, hunting and their materials ([[W-73 Fishing, hunting and their materials developed together|W-73]]).

## Summary

Every act on a thing someone holds (a set of snares or traps, a herd, a pile, a carcass, a plot, a store) names **the thing** as its
target, by its tag or a name one knows ([[D4-68 Short tags, and names given|D4-68]]). With no target named, it touches **only one's own**: one of one's own there, it is
that; several, it asks; none, it refuses and says whose are there. Another's thing is acted on only when named, and the result says
it is not one's own. Theft stays possible, always as a choice.

## The proposal

1. **The target is the thing.** Each verb that acts on a held thing takes a `thing` (a tag such as T12 or H3, or a name the person
   knows), and its description in the prompt says so: "take from your snares (T12)", "slaughter a cow of H3", "lift your traps
   (T7)". A place still narrows where to look.
2. **One's own things are shown with their tags** where one is, in the person's view: "your snares on the Common (T12, set 2
   nights ago)", "your household's herd on the Leaze (H3: 4 cows, 1 ox)".
3. **No target named:**
   - exactly one of one's own (or one's household's, for household things) at the place: that one;
   - several: refused, listing their tags ("you have snares here at T12 and T15: say which");
   - none: refused, saying whose are there ("you have no snares on the Common; T14 there is Oliver's").
4. **Another's thing, named:** the act is done, and the result says it is not one's own and what that is ("You took 2 hares from
   Oliver's snares (T14), which are not yours to take from. Whether anyone saw, you will learn."), as stores already refuse ("not
   yours to use ... to take without the right is theft").
5. **What counts as one's own:** what one set or made (sets: `by`), one's household's (herds by their claims, stores, plots), a
   weir's traps for its crew (as `owns_set` now), what one has been given the use of (an agreement).

## Why

Found 21 Nov (OPEN [[Q-80 Whether acts on owned things default to one's own|Q-80]]):
- **Sets:** `things.find` picks the most recently known thing matching a place or set words ("the snares", "my traps"), with no
  preference for one's own; "my" is not read as ownership. A take "from my snares on the Common" can empty a neighbour's line
  (Peter, low arm, day 3: "Oliver emptied my snares on the Common: three hares gone").
- **Herds:** a slaughter goes through `work` with `at` and `item`; the code reads a herd by tag or name in `thing`
  (`farm._herd_on`), but `thing` is not among the arguments the prompt lists, and unnamed it falls back from one's own herd to the
  first herd on the parcel (`(own or hs)[0]`): a slaughter on a shared pasture can kill a neighbour's beast unchosen.
- **Set and lift:** a set act always lays new gear; lifting is a take by place, so agents meaning to lift set more (about 40% of
  trap acts, 02zzy2). With the thing as the target, "lift T7" cannot be mistaken for setting.

A choice made by the agent is a finding; a theft the engine made for them is a bug in the measurement.

## Alternatives considered

- **Keep place-based targeting, prefer one's own:** fixes most thefts, keeps the ambiguity between several of one's own and between
  setting and lifting.
- **Forbid acting on another's thing:** removes theft as a choice the world should hold.

## Open questions

1. A household's things: may any member act on them unnamed (proposed), or only the one who set them?
2. Several of one's own: refuse and ask (proposed), or take them all (a lift of every own set at a place, as the fishing design's
   lift proposes)?
3. Worlds without tags: a place-and-owner phrase ("Oliver's snares on the Common") as the target.

## Affects

`cybertron2/engine/things.py` (`find`), `verbs.py` (take, work, the args strings), `farm.py` (`_herd_on`), `tags.py`, `prompt.py`
(the view of one's own things with tags), the wild's set and lift (`engine/wild.py`; proposals/hunt_fish_materials.md §5).

## History

- 23 Nov 2026: accepted in part: [[D2-305 Acts on held things take the thing as their target, by tag or a known…|D2-305]] (Acts on held things take the thing as their target, by tag or a known name, said).
- 23 Nov 2026: accepted in part: [[D2-304 An unnamed act on several of one's own things at a place|D2-304]] (An unnamed act on several of one's own things at a place: an act that takes what).
- **21 Nov 2026:** drafted by 37.2 at Zach's request (21 Nov: "they seem perpetually confused about which snares to check and
  accidentally taking from each others snares (same as killing herds?), so maybe I should revise how the identity / target for
  these acts are selected? Requires an actual target and without it defaults to only their own? Meaning killing another's cattle or
  taking from their snares requires a choice?"; then "Does stuff like taking snares and killing cattle not take an explicit
  target?"; and "Yes" to adding the concrete proposal).

## Sources

`cybertron2/engine/things.py` (`find`, `owns_set`), `cybertron2/engine/farm.py` (`_herd_on`), `cybertron2/engine/verbs.py` (the
take and work args, the store's refusal), `cybertron2/engine/tags.py` ([[D4-68 Short tags, and names given|D4-68]]); docs/review/37_growth/02zzy2_fishing_methods_compared.md.
