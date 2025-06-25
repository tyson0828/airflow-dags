#!/bin/bash
# Usage: run_github_action.sh "<lot_wafer_list>" <form_data_path> <output_csv_path>

set -e

LOT_WAFERS=$1
FORM_DATA_PATH=$2
OUTPUT_CSV_PATH=$3

# Simulated logic to run GitHub action — you can replace this with your actual logic
echo "Running job for: $LOT_WAFERS"
echo "Using form data from: $FORM_DATA_PATH"

# Simulated output
echo "wafer_id,result" > "$OUTPUT_CSV_PATH"
IFS=',' read -ra LOTS <<< "$LOT_WAFERS"
for w in "${LOTS[@]}"; do
    echo "$w,Pass" >> "$OUTPUT_CSV_PATH"
done

