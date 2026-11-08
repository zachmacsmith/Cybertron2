# 02zp models: ecosystems on generated land

Supporting code for [02zp_ecosystems_deep_dive.md](../02zp_ecosystems_deep_dive.md). Standalone numpy models: they read the terrain
generator's land and the engine's pure functions (renewal rules, the capacity model), and change nothing under `cybertron2/`.

Run from this folder, with the repository on the path (the scripts insert `/home/user/cybertron2`; change it if your checkout is
elsewhere):

```
python3 dump.py                      # land for every configuration, seeds 1-3, into lands/ (about 4 s a world; not committed)
python3 m1_report.py                 # M1: plant kinds by conditions against the generator's labels -> m1_results.json
python3 calib_m2.py; python3 fit_m2.py   # M2: succession against real timescales -> m2_calib.json
python3 run_m3.py; python3 m3_sens.py    # M3: deer, boar, hares, wolves and the wood -> m3_*.json
python3 m3b_inrun.py                 # M3b: a village's game over a run under three renewal rules -> m3b.json
python3 run_m4.py                    # M4: the wild year by season for every village -> m4_results.json
python3 run_m5.py                    # M5: goods, specialties and dependence between villages -> m5_results.json
python3 engine_flows.py; python3 m6_periodic.py   # M6: the engine's own flows; the periodic rule as a seasonal wild year
python3 m7_drain.py                  # M7: draining a fen, heath management lapsing, a village abandoned -> m7_results.json
python3 probe/make_wild_year_probe.py # the LLM probe's two arms (not run: needs Zach's approval and an API key)
```

| File | What |
|---|---|
| land.py, dump.py | generator land without people or writer (physical.build, settle.choose_sites, ecology.settled) |
| niche.py | M1: Ellenberg-scale conditions, 40 plant kinds, soft dominance per layer, labels read back |
| test_niche.py, diag.py, m1_report.py | M1 tests and report |
| succession.py, calib_m2.py, fit_m2.py | M2: the yearly succession step and its calibration |
| populations.py, run_m3.py, m3_sens.py, m3b_inrun.py | M3: populations on 1 km patches; in-run game |
| seasonal.py, run_m4.py | M4: wild food by kind and season, from real yields |
| trade.py, run_m5.py | M5: goods and dependence |
| engine_flows.py, m6_periodic.py | M6: the engine's renewal rules under steady takes |
| m7_drain.py | M7: interactions through the economy |
| probe/ | the wild-year probe: maker, the two arms, their capacity reports |
