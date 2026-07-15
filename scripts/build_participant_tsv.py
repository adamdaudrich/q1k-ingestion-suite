"""
Builds a hashmap of Q1K-specific participant.tsv fields:
participant_id,cohort,species,age_at_eeg,age_at_mri,sex,handedness

outputs a TSV file
"""

from datetime import datetime
import csv
from pathlib import Path
from utils.redcap_api import fetch_bulk_p2, fetch_bulk_p3, get_study_id # pylint: disable=import-error,wrong-import-position


def get_consented_candidates():
    """
    get the records of ONLY consented candidates from phase 3
    this is a safeguard measure because most of them are consented
    
    returns: array of dicts [{'record_id':'__', 'redcap_event_name': '__', 'redcap_repeat_instrument': '__', 
    'redcap_repeat_instance': '__', 'eeg_participant_handedness': '__'}
    """
    # phase 3 records

    p3_records = fetch_bulk_p3()

    consented_p3 = []
    for record in p3_records:


        consent_value = record.get('icf_form_phase_3_complete','')
        # 2=yes
        if consent_value == '2':
            
            p3_fields = { 
                'record_id': record.get('record_id', ''),
                'eeg_participant_handedness': record.get('eeg_participant_handedness', ''),
            }

            consented_p3.append(p3_fields)

    return consented_p3

def get_p2_filtered(consented_p3):
    """
    """

    p2_records = fetch_bulk_p2()

    p2_filtered = []
    for record in p2_records:

        if record.get('record_id') in consented_p3:

            p2_fields = {
                'record_id' : record.get('record_id',''),
                'study_id' : get_study_id(record),
                'cohort' : record.get('ev_status'),
                'site' : record.get('q1k_sitechoice_1'),       
                'species' : 'homo sapiens',
                'sex' : get_sex(record),    
            }
            
            p2_fields.append(p2_fields)

    return p2_filtered


def merge(consented_p3_filtered, p2_filtered):
    """
    merge hash map of fields required for a complete q1k participant.tsv. This includes
    participant_id,cohort,species,age_at_eeg_testing,age_at_mri_testing,sex,handedness
    from the phase 3 event from redcap 
    """

    # promote the record_id to "key" pointing to the former dict 
    for r in consented_p3_filtered:
        p3_lookup[r['record_id']] = r

    merged = []
    for record in p2_filtered:
        p3_data = p3_lookup.get(record['record_id'])

        if p3_data:  # only include if a match exists in p3
            merged.append({
                **record,    # all p2 fields
                **p3_data,   # all p3 fields, joined on record_id
            })

    return merged

# helper functions

def get_study_id(record):
    """
    Extract the study ID from the records provided by 
    """
    proband_id = record.get('q1k_proband_id_1', '')
    relative_id = record.get('q1k_relative_idgenerated_1', '')
    merged_id = proband_id or relative_id or ''

    return merged_id.replace('_', '-')


def get_sex(record):
    """
    Extract personal info from REDcap required by CBIGR new_profile 
    """

    sex = ''
    sex_value = record.get('enr2_pro_sex', '')
    if sex_value == '1':
        sex = 'Female'
    elif sex_value == '2':
        sex = 'Male'
    elif sex_value == '99':
        sex = 'Unknown'
    elif sex_value =='':
        sex = 'Unknown'

    return sex

# write the tsv
def write_tsv():
    """
    Write data to tsv
    """

    sub_ids_csv_path = get_output_path()

    fieldnames = ['']

    with open(, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        rows = [{'LorisID': k, 'AdditionalExternalID': v} for k, v in external_id_sub_ids.items()]
        writer.writerows(rows)

    print(f"✅ CSV written to: {sub_ids_csv_path}")

def main():
    """
    Main function to write csv
    """
    # make hash-map of handedness and record_id of ONLY the phase 3 consented participants
    consented = get_consented_candidates()

    p2_filtered = get_p2_filtered(consented)



    
    write_tsv()

if __name__ == "__main__":
    main()