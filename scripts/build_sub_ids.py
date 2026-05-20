#!/usr/bin/env python3
"""
Output a CSV associating the sub_id to the the Q1K "key" identifier
ex: "Q1K-HSJ-100119-P"
Returns: None
"""
import csv
from datetime import datetime
from pathlib import Path
from utils.redcap_api import fetch_identifiers, get_study_id
from scripts.rename_bids import get_merged_bids


def get_external_ids():
    """
    Extract external IDS from the fetch from REDCap
    """
    
    identifiers = fetch_identifiers()

    external_ids = []
    for i in identifiers:
        external_id = get_study_id(i)
        external_ids.append(external_id)
    
    return external_ids 


def get_external_id_sub_id():
    """
    Extract record_id and study_id from fetch_identifiers
    Return: dict
    """

    external_ids = get_external_ids()
    sub_ids = get_merged_bids()

    external_id_sub_id = {}

    for i in external_ids:
        if not i or '-' not in i:
            continue
        parts = i.split('-')
        crunched = 'sub-' + parts [-2][-4:] + parts[-1]
        #print(repr(crunched))
        if crunched in sub_ids:
                external_id_sub_id[i] = crunched

    print(list(sub_ids)[:5]) 

    return external_id_sub_id

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
    base_name = 'sub_ids'
    filename = f'{base_name}_{timestamp}.csv'
    
    # Return the full file path
    return output_dir / filename

def write_record_id_csv(external_id_sub_ids):
    """
    Write consent data to CSV
    """

    sub_ids_csv_path = get_output_path()

    fieldnames = ['LorisID', 'AdditionalExternalID']

    with open(sub_ids_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        rows = [{'LorisID': k, 'AdditionalExternalID': v} for k, v in external_id_sub_ids.items()]
        writer.writerows(rows)

    print(f"✅ CSV written to: {sub_ids_csv_path}")

def main():
    """
    Main function to write csv
    """
    external_id_sub_ids = get_external_id_sub_id()
    
    write_record_id_csv(external_id_sub_ids)

if __name__ == "__main__":
    main()