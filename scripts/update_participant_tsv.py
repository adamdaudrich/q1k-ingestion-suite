"""
Fetches and writes non-private information into participant.tsv as per
BIDS specification

fields:
participant_id<tab>species<tab>age<tab>sex<tab>handedness<tab>HED

"""

from pathlib import Path
import csv
From utils.config import Config

renamed_dir = Config.RENAMED_BIDS


def get_whatever
"""

"""


def get_the_other_thing
"""

"""


with open("participants.tsv", "w", newline="") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["participant_id", "species", "age", "sex", "handedness", "HED"])
    
    for item in sorted(renamed_dir.iterdir()):
        if item.is_dir():
            value = item.name.removeprefix("sub-")  # or item.is_file(), depending on your structure
            writer.writerow([value, "..."])
