#!/bin/bash

SOURCE_BASE="/data/q1k/data"
TARGET_BASE="/data/q1k/data/CBIG/dicoms"

echo "Source: $SOURCE_BASE"
echo "Target: $TARGET_BASE"
echo "========================================="

# Build target study list once
ls "$TARGET_BASE" | sort > /tmp/target_dirs.txt

missing_total=0

for id_pattern in "id100*" "id200*" "id1525*"; do
    for id_dir in $SOURCE_BASE/$id_pattern; do
        if [ -d "$id_dir" ]; then
            for sub_dir in "$id_dir"/*; do
                if [ -d "$sub_dir" ]; then
                    for q1k_dir in "$sub_dir"/Q1K_*; do
                        if [ -d "$q1k_dir" ]; then
                            q1k_basename=$(basename "$q1k_dir")

                            if ! grep -qx "$q1k_basename" /tmp/target_dirs.txt; then
                                echo "MISSING: $q1k_dir"
                                ((missing_total++))
                            fi
                        fi
                    done
                fi
            done
        fi
    done
done

echo "========================================="
echo "Total missing: $missing_total"

rm -f /tmp/target_dirs.txt