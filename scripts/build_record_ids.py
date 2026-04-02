#!/usr/bin/env python3
"""
This file posts the REDcap record_id in the ExtStudyID field of the candidate object
in the CBIGR candidates endpoint

values: 1= yes, 0 =no
Returns:
"""
import csv
from datetime import datetime
from pathlib import Path
from utils.both_api import get_cand_id_record_id

def get_output_path():
    """
    Get the output CSV path and ensure directory exists
    """
    # Define output directory relative to script
    script_dir = Path(__file__).parent
    output_dir = script_dir / 'csv'
    
    # Create directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d')
    base_name = 'record_ids'
    filename = f'{base_name}_{timestamp}.csv'
    
    # Return the full file path
    return output_dir / filename

def write_record_id_csv(ids):
    """
    Write consent data to CSV
    """

    record_ids_csv_path = get_output_path()

    fieldnames = ['CandID', 'record_id']

    with open(record_ids_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(ids)

    print(f"✅ CSV written to: {record_ids_csv_path}")

def main():
    """
    Main function to write csv
    """
    ids = get_cand_id_record_id()
    
    write_record_id_csv(ids)

if __name__ == "__main__":
    main()