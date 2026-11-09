# 02zza: a Fable 5.2 probe in run 6's world (9 Nov)

Zach (9 Nov) asked for a small test with one agent on Claude Fable 5.2 (`claude-fable-5-2`, just released) to see how it acts
differently. Run 6's world (`wild_probe6.json`, branch `ecology`, seed 7, spring, 8 days, 19 agents) with one change: Petronel,
head of the Carter household in Meadcombe (Opus 5.5 in run 6), played by Fable 5.2. Controls: run 6's Petronel (the same seat and
seed, Opus 5.5) and Ivy (head of the Holts, same village and run, Opus 5.5). Cost $10.81 for the run; run logs outside the
repository. The engine needed no change: the `claude_code` backend passes the model to the CLI, which accepts it.

| Petronel | Fable 5.2 (this run) | Opus 5.5 (run 6) |
|---|---|---|
| actions over 8 days (units used) | 38 (40 of 40) | 22 (40 of 41) |
| distinct acts | 15 | 9 |
| messages sent | 40 | 24 |
| refusals | 2 | 1 |
| stated reason, mean length | 152 characters | 188 |
| her calls' cost | $1.75 | $0.82 |
| seconds a call (median) | 8.8 | 10.8 |
| Carter store at the end | grain 19, dried meat 2.1, dung 15 | grain 0, dried meat 1.8 |

Ivy (Opus 5.5) acted much as in run 6 in both runs (firewood, milking, weeding), so the world played out alike; Ivy and Alys
died on day 6 in both runs (the life model and the seed, OPEN Q-35), which ends the within-run control there.

**What differed, at this seat:**
- **She ran her household by daily orders.** Every morning: "Husband, hoe East Field with me"; "Daughter, milk and herd our cows";
  each with a place and a reason. Run 6's Petronel negotiated with her husband as an equal ("Agreed, food first. So we don't hunt
  the same game ...") and asked who had done what ("Was that our calf you slaughtered?").
- **She bargained across households, and followed it up.** Day 2: asked the Holts to sell grain for coin or for her reaping at
  harvest, and posted a public offer (2 coin for 6 grain). Day 5: reaped Middle Field for the Holts and asked what share she would
  get; day 6: named a figure ("half of what I cut ... even 6 grain today"), and got 6; day 7: thanked Odo, counted her work (31
  grain cut over two days) and asked for the rest. Run 6's Petronel made no deal outside her household and leaned on hunting ("I'm
  a master hunter ... one long hunt far out").
- **She did more, smaller things and planned ahead:** slaughtering the calf herself when the store was empty, drying the meat,
  mending the house, gathering dung "for the fallow", asking the Holts to plough, telling her husband not to hoe where the crop
  stands. Her reasons were shorter and more concrete.
- **Both read the wild signs alike** (the hares on the open ground; snares refused at a wood, once each), and both households went
  hungry on day 3 or 4.

**What this does not show:** one seat in one run. Labour-for-grain deals between households are common in both runs (about 30
such messages in run 6 and 21 here, mostly by other agents), so Fable did not bring trading into the village; the difference is
how this seat behaved, and some of it follows from others' answers (Odo offered shares by work done to the Woods as well). The
Carter grain at the end comes partly from the Holts' share. Fable's calls cost about twice Opus 5.5's at this seat. A firmer test
puts Fable in two or three seats over several seeds, or swaps one seat in two runs with the same seed.

## History
- 9 Nov: run and written by 37.2 at Zach's request (WORK W-17).
