#!/usr/bin/env bash
set -euo pipefail

DRY_RUN=false
ARGS=()
for arg in "$@"; do
  [[ "$arg" == "--dry-run" ]] && DRY_RUN=true || ARGS+=("$arg")
done

EEG_DIR="${ARGS[0]%/}" TARGET_DIR="${ARGS[1]%/}"
RSYNC_OPTS="-a"
$DRY_RUN && RSYNC_OPTS="-an"

for eeg_sub in "$EEG_DIR"/sub-*/; do
  sub=$(basename "$eeg_sub")
  ses="$eeg_sub/ses-01"

  if [[ -d "$TARGET_DIR/$sub" ]]; then
    eeg_target="$TARGET_DIR/$sub/ses-01/eeg"
    et_target="$TARGET_DIR/$sub/ses-01/et"

    if [[ -d "$eeg_target" ]]; then
      echo "Skipping $sub/ses-01/eeg — already exists"
    else
      $DRY_RUN && echo "Would insert eeg for $sub" || { echo "Inserting eeg for $sub"; rsync $RSYNC_OPTS "$ses/eeg/" "$eeg_target/"; }
    fi

    if [[ -d "$ses/et" ]]; then
      if [[ -d "$et_target" ]]; then
        echo "Skipping $sub/ses-01/et — already exists"
      else
        $DRY_RUN && echo "Would insert et for $sub" || { echo "Inserting et for $sub"; rsync $RSYNC_OPTS "$ses/et/" "$et_target/"; }
      fi
    fi
  else
    echo "Skipping $sub — not found in target (MRI not yet synced?)"
  fi
done