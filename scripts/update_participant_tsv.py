"""
Fetches and writes non-private information into participant.tsv as per
BIDS specification

fields:
participant_id<tab>species<tab>age<tab>sex<tab>handedness<tab>HED
NULL values are to br written : "n/a"

"""

from pathlib import Path
import csv
from utils.config import Config, 
from utils. cbigr_api import get_candidates
from scripts.build_candidates import get_personal_fields

renamed_dir = Config.RENAMED_BIDS


def get_participant_tsv_fields()


# Get sex from REDcap
personal_fields = get_personal_fields()
sex = personal_fields['Sex']
age = {what should we use to calculate age}
handedness = 



def get_handedness():
"""
eeg_session_log eeg_participant_handedness 
(values: 1=Right-handed, 2=Left_handed, 3=Ambidextrous, 4=N/A)
"""





def main()

with open("participants.tsv", "w", newline="") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["participant_id", "species", "age", "sex", "handedness", "HED"])
    
    for item in sorted(renamed_dir.iterdir()):
        if item.is_dir():
            value = item.name.removeprefix("sub-")  # or item.is_file(), depending on your structure
            writer.writerow([value, "..."])
