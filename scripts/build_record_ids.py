#!/usr/bin/env python3
"""
Output a CSV associating the record_id to the the Q1K "key" identifier
ex: "Q1K-HSJ-100119-P"
Returns: None
"""
import csv
from datetime import datetime
from pathlib import Path
from utils.redcap_api import get_record_id_external_id

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

    fieldnames = ['LorisID', 'record_id']

    with open(record_ids_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        rows = [{'record_id': k, 'LorisID': v} for k, v in ids.items()]
        writer.writerows(rows)

    print(f"✅ CSV written to: {record_ids_csv_path}")

def main():
    """
    Main function to write csv
    """
    ids = get_record_id_external_id()
    
    write_record_id_csv(ids)

if __name__ == "__main__":
    main()