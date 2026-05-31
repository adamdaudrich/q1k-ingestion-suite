#!/usr/bin/env bash
# =============================================================================
# bids_merge.sh — Perpetual BIDS merger (MRI + EEG → TARGET)
#
# Usage:
#   ./bids_merge.sh [--dry-run] <MRI_DIR> <EEG_DIR> <TARGET_DIR>
#
# Rules:
#   - MRI subject appears, no EEG match      → rsync MRI sub to TARGET
#   - EEG subject appears, no MRI match      → rsync EEG sub to TARGET
#   - Both match (MRI dir OR already TARGET) → MRI is base; inject EEG data
#       into TARGET/sub/ses-01/{eeg,et} + scans.tsv
#   - Re-running is safe: existing dirs/files are skipped (idempotent)
#   - --dry-run prints what would happen without touching anything
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------
DRY_RUN=false
ARGS=()
for arg in "$@"; do
  [[ "$arg" == "--dry-run" ]] && DRY_RUN=true || ARGS+=("$arg")
done

if [[ ${#ARGS[@]} -ne 3 ]]; then
  echo "Usage: $0 [--dry-run] <MRI_DIR> <EEG_DIR> <TARGET_DIR>" >&2
  exit 1
fi

MRI_DIR="${ARGS[0]%/}"
EEG_DIR="${ARGS[1]%/}"
TARGET_DIR="${ARGS[2]%/}"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
RSYNC_BASE_OPTS="-a --info=progress2"
$DRY_RUN && RSYNC_BASE_OPTS="-an --info=progress2"

run_rsync() {
  # run_rsync <src> <dst>
  rsync $RSYNC_BASE_OPTS "$1" "$2"
}

maybe_mkdir() {
  # Create directory unless dry-run
  if ! $DRY_RUN; then
    mkdir -p "$1"
  fi
}

log()  { echo "[INFO]  $*"; }
warn() { echo "[WARN]  $*"; }
dry()  { echo "[DRY]   $*"; }

# ---------------------------------------------------------------------------
# Inject EEG modalities into an already-present TARGET subject
#   inject_eeg <eeg_ses_dir> <target_ses_dir>
# ---------------------------------------------------------------------------
inject_eeg() {
  local eeg_ses="$1"   # e.g. EEG_DIR/sub-01/ses-01
  local tgt_ses="$2"   # e.g. TARGET_DIR/sub-01/ses-01

  # --- eeg ---
  local eeg_src="$eeg_ses/eeg"
  local eeg_dst="$tgt_ses/eeg"
  if [[ -d "$eeg_src" ]]; then
    if [[ -d "$eeg_dst" ]]; then
      log "Skipping $(basename "$(dirname "$tgt_ses")")/ses-01/eeg — already exists"
    else
      if $DRY_RUN; then
        dry "Would inject eeg → $eeg_dst"
      else
        log "Injecting eeg → $eeg_dst"
        maybe_mkdir "$eeg_dst"
        run_rsync "$eeg_src/" "$eeg_dst/"
      fi
    fi
  fi

  # --- et ---
  local et_src="$eeg_ses/et"
  local et_dst="$tgt_ses/et"
  if [[ -d "$et_src" ]]; then
    if [[ -d "$et_dst" ]]; then
      log "Skipping $(basename "$(dirname "$tgt_ses")")/ses-01/et — already exists"
    else
      if $DRY_RUN; then
        dry "Would inject et → $et_dst"
      else
        log "Injecting et → $et_dst"
        maybe_mkdir "$et_dst"
        run_rsync "$et_src/" "$et_dst/"
      fi
    fi
  fi

  # --- scans.tsv ---
  local found_scans=false
  for scans_file in "$eeg_ses"/*_scans.tsv; do
    [[ -f "$scans_file" ]] || continue
    found_scans=true
    local scans_basename; scans_basename=$(basename "$scans_file")
    local scans_dst="$tgt_ses/$scans_basename"
    if [[ -f "$scans_dst" ]]; then
      log "Skipping $(basename "$(dirname "$tgt_ses")")/ses-01/$scans_basename — already exists"
    else
      if $DRY_RUN; then
        dry "Would inject $scans_basename → $scans_dst"
      else
        log "Injecting $scans_basename → $scans_dst"
        maybe_mkdir "$tgt_ses"
        run_rsync "$scans_file" "$scans_dst"
      fi
    fi
  done
  $found_scans || warn "No *_scans.tsv found in $eeg_ses"
}

# ---------------------------------------------------------------------------
# Collect subject sets
# ---------------------------------------------------------------------------
declare -A MRI_SUBS EEG_SUBS

for d in "$MRI_DIR"/sub-*/; do
  [[ -d "$d" ]] || continue
  sub=$(basename "$d")
  MRI_SUBS["$sub"]=1
done

for d in "$EEG_DIR"/sub-*/; do
  [[ -d "$d" ]] || continue
  sub=$(basename "$d")
  EEG_SUBS["$sub"]=1
done

# Union of all subjects
declare -A ALL_SUBS
for sub in "${!MRI_SUBS[@]}" "${!EEG_SUBS[@]}"; do
  ALL_SUBS["$sub"]=1
done

# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
for sub in $(echo "${!ALL_SUBS[@]}" | tr ' ' '\n' | sort); do

  has_mri=${MRI_SUBS[$sub]+yes}
  has_eeg=${EEG_SUBS[$sub]+yes}
  in_target=$( [[ -d "$TARGET_DIR/$sub" ]] && echo yes || echo no )

  eeg_ses="$EEG_DIR/$sub/ses-01"
  tgt_ses="$TARGET_DIR/$sub/ses-01"

  # ---- Case 1: subject exists in both MRI and EEG -------------------------
  if [[ "$has_mri" == "yes" && "$has_eeg" == "yes" ]]; then
    if [[ "$in_target" == "no" ]]; then
      # Sync MRI first, then inject EEG on top
      if $DRY_RUN; then
        dry "Would rsync MRI $sub → TARGET"
        dry "Would inject EEG data for $sub"
      else
        log "Syncing MRI $sub → TARGET"
        run_rsync "$MRI_DIR/$sub/" "$TARGET_DIR/$sub/"
        log "Injecting EEG data for $sub"
      fi
    else
      # MRI sub already in TARGET — sync any new MRI data first
      if $DRY_RUN; then
        dry "Would rsync new MRI data for $sub → TARGET"
      else
        log "Syncing new MRI data for $sub → TARGET (if any)"
        run_rsync "$MRI_DIR/$sub/" "$TARGET_DIR/$sub/"
      fi
    fi
    # Inject EEG regardless (inject_eeg is idempotent)
    inject_eeg "$eeg_ses" "$tgt_ses"

  # ---- Case 2: MRI only ----------------------------------------------------
  elif [[ "$has_mri" == "yes" && "$has_eeg" != "yes" ]]; then
    if [[ "$in_target" == "no" ]]; then
      if $DRY_RUN; then
        dry "Would rsync MRI-only $sub → TARGET"
      else
        log "Syncing MRI-only $sub → TARGET"
        run_rsync "$MRI_DIR/$sub/" "$TARGET_DIR/$sub/"
      fi
    else
      # Already in target — push any new MRI data
      if $DRY_RUN; then
        dry "Would rsync new MRI data for $sub → TARGET"
      else
        log "Syncing new MRI data for $sub → TARGET (if any)"
        run_rsync "$MRI_DIR/$sub/" "$TARGET_DIR/$sub/"
      fi
    fi

  # ---- Case 3: EEG only ----------------------------------------------------
  elif [[ "$has_eeg" == "yes" && "$has_mri" != "yes" ]]; then
    if [[ "$in_target" == "no" ]]; then
      # No MRI anywhere — copy EEG sub as-is
      if $DRY_RUN; then
        dry "Would rsync EEG-only $sub → TARGET"
      else
        log "Syncing EEG-only $sub → TARGET"
        run_rsync "$EEG_DIR/$sub/" "$TARGET_DIR/$sub/"
      fi
    else
      # Sub already in TARGET (was EEG-only before) — inject any new EEG data
      inject_eeg "$eeg_ses" "$tgt_ses"
    fi
  fi

done

log "Done."
