#!/usr/bin/env bash
set -euo pipefail

DRY_RUN=false
ARGS=()
for arg in "$@"; do
  [[ "$arg" == "--dry-run" ]] && DRY_RUN=true || ARGS+=("$arg")
done

EEG_DIR="${ARGS[0]%/}"
TARGET_DIR="${ARGS[1]%/}"
RSYNC_OPTS="-a"
$DRY_RUN && RSYNC_OPTS="-an"

for eeg_sub in "$EEG_DIR"/sub-*/; do
  sub=$(basename "$eeg_sub")
  ses="${eeg_sub}ses-01"   # ✅ bug fix

  if [[ -d "$TARGET_DIR/$sub" ]]; then
    eeg_target="$TARGET_DIR/$sub/ses-01/eeg"
    et_target="$TARGET_DIR/$sub/ses-01/et"
    ses_target="$TARGET_DIR/$sub/ses-01"

    # --- eeg ---
    if [[ -d "$eeg_target" ]]; then
      echo "Skipping $sub/ses-01/eeg — already exists"
    else
      $DRY_RUN && echo "Would insert eeg for $sub" || { echo "Inserting eeg for $sub"; rsync $RSYNC_OPTS "$ses/eeg/" "$eeg_target/"; }
    fi

    # --- et ---
    if [[ -d "$ses/et" ]]; then
      if [[ -d "$et_target" ]]; then
        echo "Skipping $sub/ses-01/et — already exists"
      else
        $DRY_RUN && echo "Would insert et for $sub" || { echo "Inserting et for $sub"; rsync $RSYNC_OPTS "$ses/et/" "$et_target/"; }
      fi
    fi

    # --- scans.tsv ---
    for scans_file in "$ses"/*_scans.tsv; do
      [[ -f "$scans_file" ]] || continue   # skip if no match
      scans_basename=$(basename "$scans_file")
      scans_target="$ses_target/$scans_basename"

      if [[ -f "$scans_target" ]]; then
        echo "Skipping $sub/ses-01/$scans_basename — already exists"
      else
        $DRY_RUN && echo "Would insert $scans_basename for $sub" || { echo "Inserting $scans_basename for $sub"; rsync $RSYNC_OPTS "$scans_file" "$scans_target"; }
      fi
    done

  else
    $DRY_RUN && echo "Would copy entire $sub from EEG" || { echo "Copying entire $sub from EEG"; rsync $RSYNC_OPTS "$eeg_sub" "$TARGET_DIR/$sub/"; }
  fi
done