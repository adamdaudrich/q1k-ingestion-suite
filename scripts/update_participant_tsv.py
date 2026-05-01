"""
Fetches and writes non-private information into participant.tsv as per
BIDS specification

fields:
participant_id<tab>species<tab>age<tab>sex<tab>handedness<tab>HED
NULL values are to be written : "n/a"

"""

from pathlib import Path
import csv
from utils.config import Config, 
from utils.cbigr_api import get_candidates
from scripts.build_candidates import get_personal_fields
from scripts.build_sessions import get_sessions
renamed_dir = Config.RENAMED_BIDS


def get_pscid_id_from_record_id()
    

def get_participant_tsv()
"""
"""
    
    SPECIES = 'homo spaiens'
    records = fetch_eeg_fields()

    tsv = {}

    for r in records:
        #record_id
        record_id = r.get['record_id']
        
        #age
        age_value = r.get['eeg_age_years_testdate']
        age = int(age_value)

        #sex
        sex_map = {'1': 'Female', '2': 'Male', '99': 'Other'}
        sex_value = r.get('eeg_sex_birth') 
        sex = sex_map.get(sex_value, 'n/a')

        #handedness
        handedness_value = 'eeg_participant_handedness'
        handedness_map = {'1':'Right-handed', '2':'Left-handed','3':'Ambidextrous','4':'n/a'}

        
        tsv[record_id] = {
            "species" : SPECIES,
            "age" : age,
            "sex" : sex,
            "handedness" : handedness,
            "strain" : 
            "strain_md" :
            "HED" :
        }

def get_cohort()
"""
"""
    cbigr_candidates = get_candidates()


def main()

with open("participants.tsv", "w", newline="") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["participant_id", "species", "age", "sex", "handedness", "HED"])
    
    for item in sorted(renamed_dir.iterdir()):
        if item.is_dir():
            value = item.name.removeprefix("sub-")  # or item.is_file(), depending on your structure
            writer.writerow([value, "..."])
