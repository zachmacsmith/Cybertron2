#!/usr/bin/env bash
# World 0's live runs (W-202): run one arm, then keep it at once by publishing it to the dataset (as live run 1, D2-332).
#   run_arm.sh <world yaml> <out name> <days> [--bots ...]
# Outputs go to /home/user/mono1/<out name>; a line per start, end and publish in /home/user/mono1/log.txt.
set -u
WORLD="$1"; NAME="$2"; DAYS="$3"; shift 3
REPO=/home/user/Cybertron2
OUT=/home/user/mono1/$NAME
mkdir -p /home/user/mono1
export LLM_BACKEND=claude_code CYBERTRON2_WEEK_STOP=0.9 HF_HUB_DISABLE_XET=1
cd "$REPO" || exit 2
echo "$(date -u +%FT%TZ) start $NAME ($WORLD, $DAYS days, $*)" >> /home/user/mono1/log.txt
python3 -m cybertron2.engine run "$WORLD" --days "$DAYS" --out "$OUT" "$@" > "$OUT.log" 2>&1
RC=$?
echo "$(date -u +%FT%TZ) end $NAME rc=$RC $(tail -1 "$OUT.log")" >> /home/user/mono1/log.txt
python3 -m cybertron2.engine publish "$OUT" --push --staging "/home/user/mono1/staging_$NAME" >> "$OUT.log" 2>&1
echo "$(date -u +%FT%TZ) published $NAME rc=$? $(tail -1 "$OUT.log")" >> /home/user/mono1/log.txt
