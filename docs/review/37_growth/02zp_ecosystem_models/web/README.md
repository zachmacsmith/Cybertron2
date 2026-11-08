# 02zp web: food-web models (work in progress, 8 Nov)

Not yet written up. W (`web.py`, kinds0/1, rounds 1-3) is superseded: its food was a fixed slice, shortage was shared equally,
there were no reserves or hibernation, and each kind's intake was fitted to a target, which together made slow breeders die out
as an artefact. W2 (`web2.py`, `kinds2.py`) rebuilds it: food as standing stocks; intake from body mass (no per-kind fitting);
fine and coarse plant food by body size (Jarman-Bell); reserves, hibernation, breeding on condition; crowding by Damuth's law
(disease), predator interference, prey refuges; one anchor per food for calibration (`calib3.py`, `scale3.json`); an external
weather input (`weather_fn`) for 37.4's climate (D4-109). Round 4 (`round4.py`) is its evaluation.

`../generator_interim.patch` holds interim generator settings (flood_m, wetness, moisture, treeline_c, wet-ground rules) that were
tested but are patches; they are not applied, and are to be replaced by an absolute water balance, sea from elevation and labels
from the plant model.
