#!/usr/bin/env bash
# The memory plan in CLAUDE.md as a wrapper: refuse to start on a busy machine, start ComfyUI fresh, run each stage in
# turn with the models freed between stages, sample RAM, swap and VRAM every 2 s, interrupt the job if available RAM
# stays under 1 GB, then free the models and stop the server by its PID. Takes are resumable, so a stopped batch
# restarts with the same command.
# Usage: scripts/comfy_batch.sh <name> '<stage command>' ['<stage command>' ...]
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"
name=$1; shift
HOST=http://127.0.0.1:8188
LOGS=log/render_logs; mkdir -p "$LOGS"
MEM="$LOGS/${name}_mem.log"; STOP="$LOGS/${name}.lowmem"; rm -f "$STOP"

avail_mb() { awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo; }
if pgrep -f 'ComfyUI/[m]ain.py' >/dev/null; then echo "ComfyUI is already running: refusing to start"; exit 1; fi
if pgrep -x blender >/dev/null || pgrep -f 'remotion.*render' >/dev/null; then echo "A render is running: refusing to start"; exit 1; fi
if [ "$(avail_mb)" -lt 28000 ]; then echo "Only $(avail_mb) MB available: refusing to start"; exit 1; fi
gpu=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits)
if [ "$gpu" -gt 2000 ]; then echo "GPU has $gpu MiB in use: refusing to start"; exit 1; fi

~/ComfyUI/.venv/bin/python ~/ComfyUI/main.py --listen 127.0.0.1 --port 8188 > "$LOGS/${name}_comfy.log" 2>&1 &
SERVER=$!

(
  echo "time avail_mb swap_used_mb vram_mb" > "$MEM"
  low=0
  while kill -0 "$SERVER" 2>/dev/null; do
    a=$(avail_mb)
    s=$(awk '/SwapTotal/ {t=$2} /SwapFree/ {f=$2} END {print int((t-f)/1024)}' /proc/meminfo)
    v=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits)
    echo "$(date +%T) $a $s $v" >> "$MEM"
    if [ "$a" -lt 1000 ]; then low=$((low + 1)); else low=0; fi
    if [ "$low" -ge 3 ] && [ ! -e "$STOP" ]; then
      echo "$(date +%T) available RAM ${a} MB: interrupting" | tee "$STOP"
      curl -s -X POST "$HOST/interrupt" >/dev/null
    fi
    sleep 2
  done
) &
SAMPLER=$!

free_models() {
  curl -s -m 30 -X POST "$HOST/free" -H 'Content-Type: application/json' \
    -d '{"unload_models": true, "free_memory": true}' >/dev/null
  sleep 3
}
cleanup() {
  free_models
  kill "$SERVER" 2>/dev/null; wait "$SERVER" 2>/dev/null
  kill "$SAMPLER" 2>/dev/null; wait "$SAMPLER" 2>/dev/null
  awk 'NR>1 { if (min=="" || $2<min) min=$2; if ($3>swap) swap=$3; if ($4>vram) vram=$4 }
       END { printf "Memory: lowest available %.1f GB, peak swap %.1f GB, peak VRAM %.1f GB\n", min/1024, swap/1024, vram/1024 }' "$MEM"
  echo "After stop: $(avail_mb) MB available"
}
trap cleanup EXIT

for _ in $(seq 1 120); do curl -s -m 2 "$HOST/system_stats" >/dev/null && break; sleep 1; done
curl -s -m 2 "$HOST/system_stats" >/dev/null || { echo "ComfyUI did not start (see $LOGS/${name}_comfy.log)"; exit 1; }

status=0
for stage in "$@"; do
  echo "=== $(date +%T) $stage"
  bash -c "$stage"; status=$?
  if [ "$status" -ne 0 ] || [ -e "$STOP" ]; then echo "Stopped at this stage (exit $status)"; status=1; break; fi
  free_models
done
exit "$status"
