#!/bin/bash

SOURCE_BASE="/data/q1k/data"
TARGET_BASE="/data/q1k/data/CBIG/dicoms"
COMPARE_SCRIPT="./find_missing_dicoms.sh"

DRY_RUN=false
if [[ "${1}" == "--dry-run" ]]; then
    DRY_RUN=true
    echo "*** DRY RUN MODE - no files will be copied ***"
fi

echo "Date/Time: $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================="

# Run the compare script and extract missing full paths
missing=$($COMPARE_SCRIPT | grep "^MISSING:" | sed 's/MISSING: //')

if [ -z "$missing" ]; then
    echo "No missing directories found. Target is up to date."
    exit 0
fi

count=0

while IFS= read -r source_path; do
    q1k_basename=$(basename "$source_path")

    if $DRY_RUN; then
        echo "WOULD SYNC: $source_path → $TARGET_BASE/$q1k_basename/"
    else
        echo "Syncing: $q1k_basename"
        rsync -av "$source_path/" "$TARGET_BASE/$q1k_basename/"
    fi
    ((count++))
done <<< "$missing"

echo "========================================="
if $DRY_RUN; then
    echo "Total would sync: $count"
else
    echo "Total synced: $count"
fi