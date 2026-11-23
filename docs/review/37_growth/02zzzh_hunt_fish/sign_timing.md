# When signs and outcomes reach people (a survey of the engine, 23 Nov 2026)

Session 37.2, at Zach's question: attending "shouldn't tell them the next morning, it should be the evening"; "signs seen during the
day should be received by the evening as well to be discussed". Read from `engine/run.py` (the day's order, about lines 900 to
1120), `engine/perceive.py` (`dawn`, `evening`), `engine/prompt.py` (`saw_lines`), `engine/evening.py` (the hearth prompt), and
checked against live run 1's own prompts (live1_A_new, Gunnild's evening of day 0).

| What | Worked out | Seen | Where |
|---|---|---|---|
| Dawn signs (sky, the river at dawn, the run's dawn cue, herons) | `perceive.dawn`, at dawn, at one's node | that morning, before planning | "This morning" |
| The day's sights (what stood out where one worked; the run in the reach; others at work) | `perceive.evening(..., phase day)`, once after the day's work, each by where they worked | that evening at the hearth (D4-82) | "What you saw today" |
| One's attend target | with the day's sights | that evening | "You paid close attention to ..." |
| In passing (where others spent the day) | with the day's sights | that evening | "In passing" |
| One's own acts' results | as each act is done | that evening | "What you did" |
| Talk (morning, the evening hearth) | as said | the same day | the talk |
| The night (spoilage, storms, breaks, vermin, a theft settled, arrivals at nightfall) | after the evening, a second `perceive.evening` pass that skips what was already shown | the next morning | "Since last evening" |
| One's own house and stores | daily, known without a roll (`house_known`) | the next morning | "Since your last morning" |

**The correction:** the attend target is already shown at that evening's hearth, not the next morning (37.2 told Zach otherwise,
wrongly).

**Two timing gaps found:**
1. **Day signs arrive only after the day's work.** Something seen at the water at mid-morning cannot change that day's acts; only
   dawn signs can. Noticing in parts of the day belongs with timed acts (W-94).
2. **Outcomes settled after the evening:** teaching (`ST.settle_teaching`), partnerships, joins and thefts are settled in the
   `settle` step, after the evening talk, so a lesson's success cannot be talked over that evening (live1_A_new: Peter's "You taught
   Nigel making a gill net" came after his evening lines telling Nigel it had not happened). Moving the teaching and partnership
   settlements before the evening would fix it; thefts stay after it, as night events.
