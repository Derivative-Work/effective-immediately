#!/usr/bin/env bash
# Render the boardroom's shots from blender/boardroom.py and encode them. Lengths and votes come from the timing map
# (timing/board_cues.json). The probe is one still with alpha, composited after the grade.
# Usage: [SCALE=0.5] [SAMPLES=24] scripts/m3_boardroom.sh [shot ...]
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
if pgrep -f 'ComfyUI/[m]ain.py' >/dev/null; then echo "ComfyUI is running: refusing to render beside it"; exit 1; fi
SCALE=${SCALE:-0.5}; SAMPLES=${SAMPLES:-24}
OUT=renders/m3/boardroom; LOGS=log/render_logs; mkdir -p "$OUT" "$LOGS"
shots=("$@"); [ ${#shots[@]} -gt 0 ] || shots=(E08 E09 B1 B2 E11 E11c E17i E22 E22p E22s E22o E22b)

for shot in "${shots[@]}"; do
  extra=()
  case "$shot" in E11|E11c|B1|B2|E08|E09|E17i) extra=(--screen renders/m3/tx/screen_drop.png) ;; esac
  case "$shot" in E22|E22p|E22s|E22o|E22b) extra=(--screen renders/m3/tx/screen_recover.png) ;; esac
  rm -rf "${OUT:?}/$shot"
  t0=$(date +%s)
  blender -b --factory-startup --python blender/boardroom.py -- --shot "$shot" --out "$OUT/$shot" --scale "$SCALE" \
    --samples "$SAMPLES" "${extra[@]}" > "$LOGS/m3_boardroom_$shot.log" 2>&1
  ffmpeg -y -v error -framerate 24 -start_number 1 -i "$OUT/$shot/%04d.png" -c:v libx264 -crf 15 -pix_fmt yuv420p "$OUT/$shot.mp4"
  if [ "$shot" = E08 ]; then    # the narrator is generated footage, placed between the room and the board
    rm -rf "${OUT:?}/E08_matte"
    blender -b --factory-startup --python blender/boardroom.py -- --shot E08 --pass matte --out "$OUT/E08_matte" --scale "$SCALE" \
      --samples "$SAMPLES" > "$LOGS/m3_boardroom_E08_matte.log" 2>&1
    .venv/bin/python -I scripts/e08_comp.py
    ffmpeg -y -v error -framerate 24 -start_number 1 -i "$OUT/E08_comp/%04d.png" -c:v libx264 -crf 15 -pix_fmt yuv420p "$OUT/E08.mp4"
  fi
  echo "$shot: $(ls "$OUT/$shot" | wc -l) frames, $(( $(date +%s) - t0 )) s"
done

for shot in E22 E22p; do
  [[ " ${shots[*]} " == *" $shot "* ]] || continue
  rm -rf "${OUT:?}/${shot}_probe"
  blender -b --factory-startup --python blender/boardroom.py -- --shot "$shot" --pass probe --out "$OUT/${shot}_probe" --stills 1 \
    --scale 1 --samples 48 > "$LOGS/m3_boardroom_${shot}_probe.log" 2>&1
  cp -f "$OUT/${shot}_probe/0001.png" "remotion/public/gen/boardroom/${shot}_probe.png.new"
  mv -f "remotion/public/gen/boardroom/${shot}_probe.png.new" "remotion/public/gen/boardroom/${shot}_probe.png"
  echo "$shot probe done"
done
