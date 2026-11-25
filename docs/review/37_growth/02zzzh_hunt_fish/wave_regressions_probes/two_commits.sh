#!/bin/bash
# Run worlds for 2 days with the scripted bots at two engine checkouts and keep their logs (wave_regressions.md §6).
#   two_commits.sh <checkout A> <checkout B> <out dir> <spec under cybertron2/specs/> ...
# e.g. git worktree add --detach /tmp/pre f728a3b7; two_commits.sh /tmp/pre . /tmp/runs valley_s5.yaml water/river.yaml
A=$(realpath "$1"); B=$(realpath "$2"); OUT=$(realpath -m "$3"); shift 3
mkdir -p "$OUT/a" "$OUT/b"
for spec in "$@"; do
  name=$(echo "$spec" | tr '/' '_' | sed 's/.yaml//')
  (cd "$A" && python3 -m cybertron2.engine run "cybertron2/specs/$spec" --bots --days 2 --out "$OUT/a/$name" > "$OUT/a/$name.log" 2>&1; echo "exit $?" >> "$OUT/a/$name.log") &
  (cd "$B" && python3 -m cybertron2.engine run "cybertron2/specs/$spec" --bots --days 2 --out "$OUT/b/$name" > "$OUT/b/$name.log" 2>&1; echo "exit $?" >> "$OUT/b/$name.log") &
  wait
  echo "$spec: a $(tail -n 1 "$OUT/a/$name.log"), b $(tail -n 1 "$OUT/b/$name.log")"
done
