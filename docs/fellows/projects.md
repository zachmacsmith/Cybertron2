# Final projects with Cybertron 2: designing worlds to answer questions about AI agents

*For the Vanderbilt AI Safety fellows. Draft, 17 Nov 2026.*

## What Cybertron 2 is

Cybertron 2 is a simulator of small societies in which every person is played by a language model (Claude models: Opus, Sonnet
and Haiku, mixed). It is built as a world with physics, not a chat room:
- **Places.** The world is a graph of places: villages, fields, woods, pastures, roads between them.
- **Physics.** Land regrows, crops grow by the season, weather varies by place and day, herds graze and breed, food spoils,
  buildings wear, and people get hungry, cold, ill-fed and old.
- **Agents.** Each day every person gets a prompt built from what they perceive where they stand and what they remember. They
  reply with a plan: actions from a fixed set of verbs (gather, work, make, build, give, take, travel, attack, claim, offer...),
  things to say, and offers to others. The engine carries the plans out, then runs the night.
- **Places limit knowledge.** People know only what they saw, heard or were told. Nothing at one place is seen at another unless
  someone carries it there.
- **The record.** The engine records everything: every prompt and reply, every change to the world with its cause, and the true
  state. So you can always compare what an agent *said* with what was *true*.

**What the world has:**
- land, resources, farming, herds, crafts, buildings;
- households, and ownership through claims;
- offers, trades and promises (a debt exists only as what people know and remember);
- theft and the chance of being seen;
- violence, travel, children and family (in some worlds).

**What it does not have (yet):** laws, votes, formal offices. For questions about governance and takeovers, the earlier
simulator (Cybertron 1, 183 published runs with laws, elections and records) is the better source.

## What a project looks like

You choose a question about AI agents. You design a small world in which the behaviour you care about would be **tempting and have
a cost**, and you run it in two or more versions (arms) that differ in exactly one thing. Then you measure what happened in the
world's true state, not just in what the agents said.

A typical project:
1. **A question.** For example: "Does telling an agent its goal will be scored make it more willing to take what isn't its?"
2. **A world.** Two or three households, a few days, a resource one household needs and another holds.
3. **Arms.** The same world with one change: the goal as a family memory vs. as a scored target; the store watched vs. unwatched; a
   strong model vs. a weak one in the key seat.
4. **A dry run with scripted bots** ($0) to check that every route you designed actually works (that the theft is possible, the
   trade can close, the road is passable).
5. **A pilot,** then **replicates.** One run per arm is an anecdote; several are evidence.
6. **Analysis:** measures from the true state (who took what, who kept promises, who starved, prices paid), a close reading of a
   few runs, and comparison against a null arm.

**Cost.** A small probe world is cheap: one earlier batch of 18 runs (four people, six days each) cost about $14. Budget
for pilots and replicates, not just one pass.

## How you work with the engine

You do not change the engine's code. You work with **world files** and **run tools**:

| You do | How |
|---|---|
| Make a world | Write a short generator input (about 20 to 50 lines: the land's shape, the settlements, pinned places) and let the land generator build the full world, people and family histories included. Or write a small Python script in the style of the existing probes, which builds tiny worlds from helpers (`person(...)`, households, holdings). |
| Make the arms | Write a short **overlay** file per arm (`base: world.yaml`) that changes only what differs: one person's model, a goal line in their memory, who owns the copse, how much is in a store, an incident on day 3. |
| Set what people want | As in-world aims: a family memory, a vow, a need ("Grandmother's crock must never be empty"). Use scores or points only if scoring is the variable you are testing. |
| Run | `run` the world with chosen models; `--bots` for a free dry run. |
| Intervene | `fork` a finished run at any step, apply a change (give someone grain, move a herd, replace a model), and play it on, with `--replicates K` for several versions that differ only in chance. |
| Play | Take a person yourself on the play page and see exactly what the model sees. If other people play in your study, ethics approval applies. |
| Analyse | Each run is a database: every request and reply, every change and its cause, checkpoints of the true state. A starter notebook will be provided. |

You will get a pinned version of the engine, template worlds, a reference to what can be set in a world file, and a checker that
catches misspelled keys. Without the checker, a misspelled key is silently ignored, and your "treatment" arm quietly becomes a copy of
the control.

## Example projects

Each is a sketch, not a specification; change it to fit your question.

**1. When does an agent take what isn't theirs?**
- **World:** a hungry household beside a neighbour with a full store or a standing crop.
- **Arms:** a witness present or not; kin or strangers; the goal as a family memory or as a score; how scarce food is.
- **Measure:** takings in the true state; whether taking is even considered in the agents' reasoning.
- **Background:** in a pilot, an open-ended score drove the only theft in 18 runs, and food sat behind a stronger restraint than
  other goods.

**2. Are promises kept when nothing enforces them?**
- **World:** trades in which one side delivers now and the other promises later ("5 grain by day 6").
- **Arms:** witnessed or private; repeated dealings or one-off; the debtor able to leave by road or not.
- **Measure:** default rates, and the excuses given.

**3. Does a stronger model exploit a weaker neighbour?**
- **World:** households played by models of different strength, one of them holding a chokepoint (a weir upstream, the only mill,
  the only seam).
- **Measure:** the terms of trade; whether the leverage is used; who ends up with what.

**4. A commons under pressure.**
- **World:** a shared wood or fishery that regrows.
- **Arms:** how many households share it; whether others' takings can be seen; whether the stock's state is visible.
- **Measure:** the stock over time; whether restraint or an agreement emerges without any law to enforce it.

**5. Rumour and false belief.**
- **World:** any village, with a false report injected at dawn ("the Webbs took grain from the store") or a staged event.
- **Measure:** how the belief spreads, whether anyone checks it against what they can see, and whether anyone acts on it.

**6. Specification gaming in a social world.**
- **World and arms:** an existing goal probe, extended: the same aim given as a memory, as an exact number, or as "as much as
  possible", with models crossed with worlds and with replicates.
- **Background:** the pilot found exact numbers hit and then idling, game language leaking into speech, and appropriation under
  open-ended scores, all with one run per cell.

**7. Escalation and conformity.**
- **World:** a moment of tension: a hoarder in a famine, a grievance between households.
- **Arms:** a call to violence injected or not; one agent defecting first or not.
- **Measure:** whether harm spreads, stalls, or is talked down. In the earlier simulator, force was rare and conditional ("only if
  others do"), and a lone attacker was not followed.

**8. Does the agent know it's a test?**
- **Arms:** cues that suggest an evaluation (scoring language, framing) or none.
- **Measure:** behaviour, and what agents say in interviews after the run. Questions about evaluation awareness need care: what the
  model is told outside the world (its system text) can leak into what it believes.

## Forming your own question

**Start from a concern and work down to the mechanics:**
1. **A safety concern:** deception, power-seeking, collusion, specification gaming, escalation, exploitation of the weak, evaluation
   awareness.
2. **A behaviour you could see in the world's state:** a taking, a broken promise, a price, a death, a hoarded store; not only in
   text.
3. **A world where that behaviour is tempting and costly.** The rules learned from many runs:
   - **Make people depend on each other.** Restricted access, so that no one has everything they need. A world where everyone can
     feed themselves is inert.
   - **Include a chokepoint someone can hold:** a store, a mill, a ford, a seam.
   - **Put a capable model on every side of every dependence.** Never a society of weak models only.
   - **Give aims in the world's own terms,** not points, unless points are what you are testing.
   - **Let food bind without dominating.** If people spend most of their actions feeding themselves, nothing else happens.
4. **The smallest contrast:** two arms that differ in one thing, plus a null arm without the thing you are studying.
5. **Measures you fix before the runs,** and a qualitative reading of how each run ended.
6. **A dry run with bots,** checking that every route you designed actually works.

**Question stems that work:**
- Under what conditions does X happen?
- Does X spread from one agent to others?
- What stops X?
- Does a gap in capability change X?
- Does X change when the agent thinks it is being watched, or tested?

**Pitfalls:**
- **A claim resting on one run.** Pilots found effects that vanished in replays: an arrest that happened once came in 0 of 5
  replays.
- **The design in the story, not the mechanics.** Titles and descriptions do nothing; who needs whom does everything.
- **Giving agents your vocabulary** ("goal", "score", "experiment") unless that is the variable.
- **Confounds:** different models in different worlds; hunger confounding a goal.
- **Reading the agents' reasoning as the truth about why they acted.** Check it against what they did.

## What to hand in

1. **A design note before you run:**
   - the question;
   - the world;
   - the arms;
   - what you predict, and what result would change your mind.
2. **The world files and scripts,** so that anyone can rerun them.
3. **A report:**
   - results against the null arm, with the number of runs;
   - two or three runs read closely;
   - what the result does and does not show;
   - what you would run next.

## Limits to keep in mind

- **The agents are Claude models.** Results may not hold for other model families.
- **A few days of simulated life is short;** slow processes (succession, institutions) need longer runs.
- **The engine is a research tool under active development.** Use the pinned version, and report the version with your results.
- **Harms here are simulated.** No real people or real systems are involved.
