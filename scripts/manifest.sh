#!/usr/bin/env bash
# Regenerate MANIFEST.sha256 for every large file (git-ignored): audio, generated assets, renders, the edit and rejected large files under archive/.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
dirs=(audio timing assets/gen renders edit archive review)
existing=()
for d in "${dirs[@]}"; do [ -d "$d" ] && existing+=("$d"); done
# Frame sequences are never archived: they regenerate from the logged commands (plates, overlays, frames, guides and previews).
find "${existing[@]}" -type f -not -regex '.*/\(plates[^/]*\|overlay[^/]*\|frames[^/]*\|guides\|preview\)/.*' -print0 \
  | while IFS= read -r -d '' f; do if git check-ignore -q "$f"; then printf '%s\0' "$f"; fi; done \
  | sort -z | xargs -0 -r sha256sum > MANIFEST.sha256
echo "$(wc -l < MANIFEST.sha256) files in MANIFEST.sha256"
