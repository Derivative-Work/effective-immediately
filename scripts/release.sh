#!/usr/bin/env bash
# The v1.0 release (human interventions 29: "create the release in line with the other songs"), the way the series'
# earlier videos made theirs: the upload files with their captions and thumbnail, the human's Logic project, and the
# production archive git doesn't hold, in tars under GitHub's 2 GiB per-asset limit. Staged in release/ (git-ignored;
# the videos and the Logic project hard-linked), then a GitHub release of this repository with docs/release_notes.md.
#
#   effective_immediately_1080p.mp4             the main video, the YouTube upload file (deliverables/)
#   effective_immediately_short_<name>.mp4      the four Shorts, 1080x1920 (deliverables/), and their .en.srt captions
#   effective_immediately.en.srt                the main video's captions (deliverables/)
#   effective_immediately_thumbnail.jpg         the thumbnail on YouTube (deliverables/thumbnails/, option A)
#   effective-immediately.logicx.zip            the human's Logic Pro project for the master, as the human supplied it
#                (audio/logic/): Suno's twelve stems (generation 2) and Logic's own plugins, no loops, samples or
#                software instruments. Space Designer's impulse response is Logic's own and isn't included
#   inputs-suno.tar    Suno's audio, none of which can be regenerated: audio/track and audio/source (generation 1, the
#                      take and its stems as downloaded; audio/stems is that zip unpacked), audio/candidates
#                      (generation 2, the take used, and its stems) and audio/credits (the credits music, a Suno cover)
#   inputs-master.tar  the human's masters from the Logic project (audio/master: both versions and the bounced stems)
#                      and audio/postfilter (the post-filtered masters and credits music; the post-filter model is
#                      private). Split from inputs-suno.tar because together they pass 2 GiB
#   takes.tar          every generated still and clip, used or not (assets/gen: FLUX.2 stills, LTX-2.3 clips)
#   SHA256SUMS         for every file above; the files inside the tars are in MANIFEST.sha256
# Left out: the human's full-page release screenshots (assets/captures/releases/, they show the browser) and the crops;
# the market data (Databento's terms: not redistributed; scripts/fetch_databento.py fetches it with your own key) and
# Alpaca's, which isn't used, with the archived renders drawn from either (archive/); the people kit library
# (assets/figures/, from All Systems Operational); audio/working (scripts/master_audio.py rebuilds it); renders,
# frames, animatics and review copies, which regenerate from the logged commands; and the Claude Code session transcript.
#
# Usage: scripts/release.sh [--create]   (stages release/; --create also creates the release v1.0 with gh)
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
TAG=v1.0
R=release
P=effective_immediately
SHORTS=(chorus bridge reinstated plaque)  # METADATA.md's order
LOGIC=effective-immediately.logicx.zip
mkdir -p "$R"
rm -f "$R"/*.mp4 "$R"/*.srt "$R"/*.jpg "$R"/*.tar "$R"/*.zip "$R"/SHA256SUMS
FILES=("${P}_1080p.mp4")
ln "deliverables/${P}_1080p.mp4" "$R/${P}_1080p.mp4"
for s in "${SHORTS[@]}"; do
  ln "deliverables/${P}_short_$s.mp4" "$R/${P}_short_$s.mp4"
  FILES+=("${P}_short_$s.mp4")
done
cp "deliverables/$P.en.srt" "$R/$P.en.srt"
FILES+=("$P.en.srt")
for s in "${SHORTS[@]}"; do
  cp "deliverables/${P}_short_$s.en.srt" "$R/${P}_short_$s.en.srt"
  FILES+=("${P}_short_$s.en.srt")
done
cp "deliverables/thumbnails/${P}_thumbnail_A.jpg" "$R/${P}_thumbnail.jpg"
ln "audio/logic/$LOGIC" "$R/$LOGIC"
FILES+=("${P}_thumbnail.jpg" "$LOGIC")
# Sorted, without the local user and group, so the same files give the same tar.
TAR=(tar --sort=name --owner=0 --group=0 --numeric-owner)
"${TAR[@]}" -cf "$R/inputs-suno.tar" audio/track audio/source audio/candidates audio/credits
"${TAR[@]}" -cf "$R/inputs-master.tar" audio/master audio/postfilter
"${TAR[@]}" -cf "$R/takes.tar" --exclude='*/frames' assets/gen
FILES+=(inputs-suno.tar inputs-master.tar takes.tar)
(cd "$R" && sha256sum "${FILES[@]}" > SHA256SUMS)
for f in "${FILES[@]}" SHA256SUMS; do
  (( $(stat -c %s "$R/$f") < 2147483648 )) || { echo "$f is over 2 GiB" >&2; exit 1; }
done
# every file in the tars as the manifest lists it
for t in inputs-suno inputs-master takes; do
  tar -tf "$R/$t.tar" | grep -v '/$' | while IFS= read -r f; do
    grep -qF "  $f" MANIFEST.sha256 || { echo "$f: not in MANIFEST.sha256" >&2; exit 1; }
  done
done
# and the manifest still matching them, the videos and the Logic project
(grep -F -e "  audio/track/" -e "  audio/source/" -e "  audio/candidates/" -e "  audio/credits/" -e "  audio/master/" \
  -e "  audio/postfilter/" -e "  audio/logic/" -e "  assets/gen/" -e "  deliverables/" MANIFEST.sha256 \
  | sha256sum -c --quiet) || { echo "MANIFEST.sha256 is stale" >&2; exit 1; }
ls -l "$R"
cat "$R/SHA256SUMS"
if [[ ${1:-} == --create ]]; then
  gh release create "$TAG" --target main --latest --title "Effective Immediately v1.0" --notes-file docs/release_notes.md \
    "${FILES[@]/#/$R/}" "$R/SHA256SUMS"
fi
