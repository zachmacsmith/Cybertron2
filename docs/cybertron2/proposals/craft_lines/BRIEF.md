# Brief: each craft's lines by familiarity (W-205)

Zach (28 Nov): "Can you go and write all the different level of knowledge lines about all the crafts and techniques". You write
them for one part of the engine's 161 crafts (`cybertron2/engine/data.py` TECHNIQUES, after registration: import
`cybertron2.engine.data` and the rows from gear.py, process.py, stores.py and wild/methods.py are in it).

## What the prompt shows now, by level (D2-352, D2-356, D5-2)

- **aware**: the name and who does it, nothing more (`knowledge.craft_parts`, `iface.known_of`).
- **rough**: `- name args: DOES (a rough idea: its inputs; needs X; you could try: about half the time it works...)`.
- **capable**: `- name args: DOES (capable: inputs, units, gives, where; works about 3 times in 4...; needs; tools; HINT)`.
- **known**: as capable, with the skill word and the made thing's life; HINT shown.

DOES is the row's `does`, else its `label` ("making a harness"), which says nothing of what the thing is for. HINT is the row's
`hint`, shown at capable and known only. The numbers (inputs, batch, units, odds, life, where) are generated from the data
(`knowledge.craft_parts`, `iface.craft_line`): never repeat them in your lines.

D5-2 (Zach, 24 Nov): "You can't literally remove the action or its description or it practically doesn't exist. They need the
interface and its language. Concise doesn't mean idiotically short. It means don't explain the world when it can be memory.
Interface is not world." So a line says what doing the craft does and how it is done well; it does not state the world (yields,
how much a place gives, seasons, where things are).

## What you write, for each craft in your part

A JSON object keyed by the craft's exact TECHNIQUES key:

```json
"wicker trap": {
  "shown": true,
  "does": "make a wicker trap: set in running water, it catches fish and eels by night until it wears out",
  "does_is_new": true,
  "aware": "a basket trap for fish and eels",
  "rough": "...",
  "capable": "...",
  "known": "...",
  "grounded_in": ["cybertron2/engine/gear.py: ...", "data.py ITEMS['wicker trap']"],
  "doubts": ""
}
```

- **shown**: false for rows that are never a craft line (no shape: `shapes.shape_of(key)` is None, e.g. "for", "hidden: ...");
  give a one-line reason in `doubts` and leave the other fields empty.
- **does**: what doing it does, in the interface's voice (imperative, lower case, like the existing ones: "make a pack basket: you
  carry 15 kg more on the road"). For a **make** craft, say what the made thing is for and how it is used (from ITEMS' fields:
  `carry`, `tool`, `weapon`, `track`, `life`, `set`, and the handlers that read the item). For a gather, work or build craft, what
  it does to the land, the beasts, the building or the goods. If the row already has a `does`, copy it unchanged and set
  `does_is_new` false; if it is wrong against the code, say so in `doubts` and give a better one in `does` with `does_is_new` true.
- **aware** (at most 10 words): what someone who has only heard of it knows: what it is for, in plain words. This is a proposal
  beyond D2-352 (which shows aware as the name only); write it anyway.
- **rough** (at most 25 words): the one or two things a beginner must know to try it: what it is done with or on, and the
  commonest way it goes wrong in the engine (a refusal it would meet, a waste it would cause).
- **capable** (at most 30 words): working know-how: what makes it go better or worse as the engine computes it (tools, skill, wear,
  a crew, a fire, the state of the field or beast, what must be done first or after, what it spoils or protects).
- **known** (at most 30 words): the finer points: interactions with other crafts and states that only practice shows (what to do
  with the product next, how to keep it, when it is not worth doing), still grounded in the code.
- Each level adds to the one before; do not repeat what a lower level said.
- **grounded_in**: the file and function or data field each claim rests on. Every claim must be true of the engine as the code
  stands: read the handler (verbs.py HANDLERS and what it calls; gear.py, process.py, stores.py, farm/herd code, wild/methods.py),
  not just the row. Never invent an effect, a tool, a condition or a product. If you cannot find what a craft does, say so in
  `doubts` and keep the lines to what you can ground.
- **doubts**: anything uncertain, any fault or gap you notice in the engine (report it here only; change nothing).

## Style

Plain short English, British spelling, a village's words, second person only where natural. No numbers already generated, no
yields or seasons stated as facts of the world, no em dashes, no engine jargon (no "units" except where the interface already says
"unit"; no field names). Short clauses joined by commas, colons and semicolons, as the existing lines are.

## Rules

- Read and write only: do not edit any engine code, data or tests; do not commit or push.
- Write your part's JSON to `docs/cybertron2/proposals/craft_lines/part_<N>.json` (valid JSON, every key in your dump present).
- Your dump (each row, its shape and the items it uses or makes) was a scratch file `crafts_part<N>.json` made from TECHNIQUES
  and ITEMS at the time (not kept).
- When done, reply with: how many crafts written, how many `does` new, and the doubts worth Zach's attention (faults first).
