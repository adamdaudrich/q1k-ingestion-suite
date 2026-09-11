"""
Builds a hashmap of Q1K-specific participant.tsv fields:
participant_id,cohort

outputs a valid TSV file
"""

from datetime import datetime
import csv
from pathlib import Path
from utils.redcap_api import fetch_sessions, get_study_id # pylint: disable=import-error,wrong-import-position
from utils.config import Config
import os

def get_eeg_bids():
    """
    use existing list of eeg bids to make a hash table of 
    key : value (participant_id : cohort)
    """
    lookup = build_cohort_lookup()
    tsv = []

    #add bids id to the hash table
    for bids_id in os.listdir(Config.MERGED_BIDS): 
        if bids_id.startswith('sub-'):
            tsv.append({
                'bids_id' : bids_id,
                'cohort' : get_cohort(bids_id, lookup)
            })
        else:
            continue

    return tsv


def transform_q1k_to_bids(q1k_id):
    """
    Transform a q1k_id (e.g. Q1K-MHC-100101-P) into its
    corresponding bids_id (e.g. sub-0101P).
    """
    parts = q1k_id.split('-')
    if len(parts) < 2:
        return None

    q1k_clean = parts[-2][-4:] + parts[-1]
    return 'sub-' + q1k_clean


def build_cohort_lookup():
    """
    transform the q1k id ex Q1K-MHC-100101-P to bids id and
    build a hash table of bids_id : cohort
    ex: 
    0101P : Affected
    0202M1 : Not Affected
    """

    sessions = fetch_sessions()
    lookup = {}

    for s in sessions:
        cohort_value = s.get('ev_status')
        q1k_id = get_study_id(s)
        bids_id = transform_q1k_to_bids(q1k_id)

        if cohort_value == '1':
            cohort = 'Affected'
        elif cohort_value == '2':
            cohort = 'Not Affected'
        elif cohort_value == '':
            cohort = 'Affected'
        else:
            cohort = None

        lookup[bids_id] = cohort

    return lookup


def get_cohort(bids_id, lookup):
    """
    0(1) cohort lookup for a given bids_id
    """

    return lookup.get(bids_id)


def get_output_path():
    """
    Get the output CSV path and ensure directory exists
    """
    # Define output directory relative to script
    script_dir = Path(__file__).parent
    output_dir = script_dir / 'tsv'
    
    # Create directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d')
    base_name = 'participants'
    filename = f'{base_name}_{timestamp}.tsv'
    
    # Return the full file path
    return output_dir / filename

# write the tsv
def write_tsv(tsv, output_path):
    fieldnames = ['participant_id', 'cohort']

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        for i in tsv:
            writer.writerow({
                'participant_id': i['participant_id'],
                'cohort': i['cohort']
            })

    print(f"✅ TSV written to: {output_path}")

def main():
    """
    Main function to build and write the Q1K participant TSV
    """
    tsv = get_eeg_bids()

    output_path = get_output_path()

    write_tsv(tsv, output_path)

if __name__ == "__main__":
    main()