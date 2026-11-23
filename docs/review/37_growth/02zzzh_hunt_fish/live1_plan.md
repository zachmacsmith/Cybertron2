# Live run 1: the plan (D2-333, D2-334, D2-335)

Session 37.2, 23 Nov 2026. Zach: "not just do one big run ... have some that are either longer and smaller or if at all larger
then shorter. Design sets of smaller runs with null runs comparing to how things were before the rebuild. We don't need any findings
with statistical significance but aiming for qualitative holistic sense of if the new things have changed things if so how and if it
is for the better."

## The worlds

- **Eelmouth, rebuilt** (`specs/nutrition/eelmouth.yaml`, stage 4): water-only (D2-316), three households: the Marshes hold the weir
  (Peter, Opus; Nichola, Sonnet; Nigel, Haiku), the Brooks the salt house and the fen (Oliver, Opus; Katherine and Petronel,
  Haiku), the Shepherds fish by traps and keep (Hamon, Opus; Gunnild, Haiku); four children; the new core prompt, the eleven act
  shapes, founders' seeded lines with their capital (D2-311), learning as one record, the household book.
- **Eelmouth small** (`eelmouth_small.yaml`): the same without the Shepherds: two households, the weir against the salt; six play.
- **The comparison with the old prompt** (`eelmouth_old.yaml`, `eelmouth_small_old.yaml`): the rebuilt engine and world, today's old
  core prompt and 38-verb list, no new seeded lines.
- **Before the rebuild** (`pre_full.yaml`, `pre_small.yaml`): the engine at f728a3b7 (main before stage 1 merged) on the runs world as
  it then was (runs_high: the same people and households, the old world: the Salt House with the Marshes, no rock, no seeded gear),
  the cast's models set as in the rebuilt Eelmouth (Katherine Haiku), the weekly stop 0.99.

## The sets

The eel run reaches the weir on day 6, peaks on days 10 and 11 and ends about day 17 (a 26-day bot run of the rebuilt Eelmouth).
A world year is 32 days; the next autumn begins about day 37.

| Set | Shape | Arms with models | Free arms | Length | Asks |
|---|---|---|---|---|---|
| **A: larger and shorter** | full Eelmouth, 8 play | A-new (rebuilt), A-old (rebuilt, old prompt), A-pre (before the rebuild) | bots on the rebuilt and the pre-rebuild worlds | 18 days: summer's end, the whole eel run, the start of winter | Do they learn of the run in time and fish it? Set and tend right? What happens to the glut? Do rules, chores and evening talk appear? |
| **B: smaller and longer** | Eelmouth small, 6 play | B-new, B-pre | bots on both | 40 days: the run, the winter, the spring gap, the next autumn's first nights | Do they keep the glut through the winter? Is anything traded between the weir and the salt? Is knowledge passed on? Who holds what at the end? |

About 900 person-days with models (A 432, B 480). They run two or three at a time, A first; each stops at 99% of the weekly window
(D2-334); the window is read before and after each.

## How it is read

Not for significance (D2-335): one seed each, read as a whole. For each arm, a short qualitative reading of the end state (who is
alive, fed, holding what; what was built, kept, traded, taught), and of the days around the run; against the bot arms (what the world
gives with no decisions) and the arms before the rebuild and with the old prompt (what the rebuild changed). The question is
whether the new systems changed things, how, and whether for the better.

## Keeping them

Every arm is copied out of the container the moment it ends and published to the Hugging Face dataset at once (D2-332); the world
files and this plan are in the repository.
