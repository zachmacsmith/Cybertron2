#!/usr/bin/env bash
# Live run 1 (D2-335): run one arm, then at once keep it and publish it (D2-332).
#   run_arm.sh <code dir> <world yaml> <out name> <days> [--bots runs]
# The code dir is the engine to run (the rebuilt main, or the pre-rebuild worktree). Outputs go to /home/user/live1/<out name>.
set -u
CODE="$1"; WORLD="$2"; NAME="$3"; DAYS="$4"; shift 4
OUT=/home/user/live1/$NAME
MAIN=/home/user/cybertron2
export LLM_BACKEND=claude_code CYBERTRON2_WEEK_STOP=0.99 HF_HUB_DISABLE_XET=1
cd "$CODE" || exit 2
echo "$(date -u +%FT%TZ) start $NAME ($WORLD, $DAYS days, $*)" >> /home/user/live1/log.txt
python3 -m cybertron2.engine run "$WORLD" --days "$DAYS" --out "$OUT" "$@" > "$OUT.log" 2>&1
RC=$?
echo "$(date -u +%FT%TZ) end $NAME rc=$RC $(tail -1 "$OUT.log")" >> /home/user/live1/log.txt
# keep: publish from the rebuilt main's code (the dataset's format), staging kept beside the run
cd "$MAIN" && python3 -m cybertron2.engine publish "$OUT" --push --staging "/home/user/live1/staging_$NAME" >> "$OUT.log" 2>&1
echo "$(date -u +%FT%TZ) published $NAME rc=$? $(tail -1 "$OUT.log")" >> /home/user/live1/log.txt
