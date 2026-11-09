# Wild systems, wave 1 (02zp part six)

The general system of proposals/wild_systems.md §10, and wave 1 of §13 on it. Session notes, not the engine (§14).

| File | Holds |
|---|---|
| `rules.py` | the drivers from the engine's weather, and the general rules (Pulse, Group, Load, Run, Flock); no kind is named here |
| `village.py` | a village: land, stocks at risk, the ledger, signs and events |
| `kinds.py` | wave 1 as data: boar with the mast, red deer, hare, birds at the corn, rats and mice, eels, wildfowl; their signs (a reading per level), goods and acts |
| `sim.py` | villages from generated worlds (`../wild/prep.py` writes inputs.pkl), observers by level, costs of acts |
| `check.py` | no kind named in the rule code; where each kind lives |
| `baselines.py`, `survey.py` | scripted households (none, calendar, scripted expert) and the survey over all villages and eras |
| `llm_tests.py` | the targeted LLM tests T1 (boar and deer at the field), T2 (eels at the weir), T3 (birds and hares at the sowing) |
| `llm_runs/` | every call (prompt, reply, acts) and the results |
