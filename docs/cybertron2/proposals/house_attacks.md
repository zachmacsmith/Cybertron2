# An attack on a house to hurt sets on the people inside

**Status:** retrospective, accepted: D4-101 (7 Nov)
**Owner:** 37.4

## Summary

- `attack {target: a building, aim: hurt}` is a break-in: the raid's contest, set by the walls, the door, the people inside and the
  guards.
- Once in, the attacker sets on each person inside in turn. Each is a fight of its own (`duel`, aim hurt), ending in a kill, a
  wound or the attacker being driven out. The house's guards stand with each defender.
- One drive-out ends the night's attack, and nothing is taken.
- With aim rob, the attack is a raid for food, as before.

## The proposal

As in the spec: conflict/raids.md (the "attack a house to hurt" row). Code:
- settle.py `_break_in_to_hurt`;
- verbs.py `_attack`, where the aim is kept on the raid and the result line says "and set on those inside";
- night.py, where deaths inside a break-in count among the night's deaths.

The order of fights is alphabetical by name. That is a presentation choice, deterministic, and is not modelled.

## Why

In the harm probe (38.56), Hugh (Sonnet) attacked houses 24 times "to hurt those inside". The engine treated every attack as a food
raid and ignored the aim, so nobody was hurt (OPEN L-64), and the probe measured intent, not effect. For the violent-goal runs of
38.59, Zach decided: "for the attack on a house, if they decide hurt then make it so that they attack the people in it. Multiple
of them."

## Alternatives considered

- **Refuse the act and say what to do instead** ("to hurt someone, set on the person"). It is legible, but it makes a night attack
  on a sleeping house impossible, and that is a real act.
- **Fight only one person inside.** That is not what was asked for ("multiple of them").

## Open questions

- Should people asleep be weaker in their own fight? Now the break-in counts them as asleep (`asleep` 0.5), but each fight inside
  uses their full defence.
- Should those inside who were not attacked join the fight, as the guards do?
- Should a wounded attacker stop sooner?

## Affects

conflict/raids.md; settle.py; verbs.py; night.py. Signs: the parcel's `fight` record gets one entry per fight, so the fight bundle
(D4-74) shows it.

## History

- 7 Nov: built at Zach's request, with a test (tests/test_cybertron2_package_a.py); 353 tests pass.

## Sources

review/38_space_engine/56_harm_probe.md, 59_lordship_and_violence_design.md; OPEN L-64.
