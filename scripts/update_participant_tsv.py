"""
Fetches and writes non-private information into participant.tsv as per
BIDS specification

fields:
participant_id<tab>species<tab>age<tab>sex<tab>handedness<tab>HED
NULL values are to be written : "n/a"

"""

from pathlib import Path
import csv
from utils.config import Config
# from utils.cbigr_api import get_candidates
from utils.redcap_api import fetch_eeg_fields, get_study_id
from utils.cbigr_api import get_loris_ids
# from scripts.build_candidates import get_personal_fields
# from scripts.build_sessions import get_sessions
renamed_dir = Config.RENAMED_BIDS


def get_eeg_fields():
    """
    Build a dict containing the necessary fields for most detailed participant tsv possible
    participant_id, age, sex, handedness
    """
    
    SPECIES = 'homo sapiens'
    eeg_raw_data = fetch_eeg_fields()

    eeg_fields = {}

    for r in eeg_raw_data:

        record_id = r.get('record_id')
        age_value = r.get('eeg_age_years_testdate')

        if age_value == '':
            age = 'n/a'
        else:
            age = int(round(float(age_value)))

        sex_map = {'1': 'Female', '2': 'Male', '99': 'Other'}
        sex_value = r.get('eeg_sex_birth') 
        sex = sex_map.get(sex_value, 'n/a')

        handedness_map = {'1':'Right-handed', '2':'Left-handed','3':'Ambidextrous','4':'n/a'}
        handedness_value = r.get('eeg_participant_handedness')
        handedness = handedness_map.get(handedness_value, 'n/a')

        eeg_fields[record_id] = {
            "participant_id": record_id,
            "species" : SPECIES,
            "age" : age,
            "sex" : sex,
            "handedness" : handedness
        }

    return eeg_fields

# def get_cohort():
#     """
#     """
#     cbigr_candidates = get_candidates()

#     return None

# def get_output_path():
#     """
#     Get the output CSV path and ensure directory exists
#     """
#     output_dir = Config.RENAMED_BIDS
#     filename = 'participants.tsv'
    
#     return output_dir / filename


def replace_record_id():
    """
    replace the record_id with the PSCID
    """

def write_participant_tsv(tsv_dict):
    """
    Write the dict to the CSV
    """

    with open("participants.tsv", "w", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["participant_id", "species", "age", "sex", "handedness"])
        
        for item in sorted(renamed_dir.iterdir()):
            if item.is_dir():
                value = item.name.removeprefix("sub-")  # or item.is_file(), depending on your structure
                writer.writerow([value, "..."])


def main():
    """
    Main function to write csv
    """
    eeg_fields = get_eeg_fields()
    
    write_participant_tsv(eeg_fields)

if __name__ == "__main__":
    main()
