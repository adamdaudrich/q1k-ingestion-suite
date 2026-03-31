#!/usr/bin/env bash
set -euo pipefail

DRY_RUN=false
ARGS=()
for arg in "$@"; do
  [[ "$arg" == "--dry-run" ]] && DRY_RUN=true || ARGS+=("$arg")
done

MRI_DIR="${ARGS[0]%/}" EEG_DIR="${ARGS[1]%/}" TARGET_DIR="${ARGS[2]%/}"
RSYNC_OPTS="-av --stats -h"
$DRY_RUN && RSYNC_OPTS="-avn --itemize-changes --stats -h"

mkdir -p "$TARGET_DIR"
rsync $RSYNC_OPTS --exclude="participants.tsv" "$MRI_DIR/" "$TARGET_DIR/"

for eeg_sub in "$EEG_DIR"/sub-*/; do
  sub=$(basename "$eeg_sub")
  ses="$eeg_sub/ses-01"

  if [[ -d "$TARGET_DIR/$sub" ]]; then
    rsync $RSYNC_OPTS "$ses/eeg/" "$TARGET_DIR/$sub/ses-01/eeg/"
    [[ -d "$ses/et" ]] && rsync $RSYNC_OPTS "$ses/et/" "$TARGET_DIR/$sub/ses-01/et/"
  else
    rsync $RSYNC_OPTS "$eeg_sub/" "$TARGET_DIR/$sub/"
  fi
done

TSV="$TARGET_DIR/participants.tsv"
if $DRY_RUN; then
  echo "--- participants.tsv changes ---"
  [[ ! -f "$TSV" ]] && echo "  Would create participants.tsv with header"
  for sub_path in "$TARGET_DIR"/sub-*/; do
    sub=$(basename "$sub_path")
    grep -qx "$sub" "$TSV" 2>/dev/null || echo "  Would add: $sub"
  done
else
  [[ ! -f "$TSV" ]] && echo "participant_id" > "$TSV"
  for sub_path in "$TARGET_DIR"/sub-*/; do
    sub=$(basename "$sub_path")
    grep -qx "$sub" "$TSV" || echo "$sub" >> "$TSV"
  done
fi