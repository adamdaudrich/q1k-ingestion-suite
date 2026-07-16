"""
Builds a hashmap of Q1K-specific participant.tsv fields:
participant_id,cohort,site,species,sex,handedness

outputs a TSV file
"""

from datetime import datetime
import csv
from pathlib import Path
from utils.redcap_api import fetch_bulk_p2, fetch_bulk_p3, get_study_id # pylint: disable=import-error,wrong-import-position
import json

def get_imaging():
    """
    get the records of ONLY candidates from phase 3 that have done mri or eeg
    this is to constrain the participants to just those in BIDS dataset
    
    returns: array of dicts [{'record_id':'__', 'redcap_event_name': '__', 'redcap_repeat_instrument': '__', 
    'redcap_repeat_instance': '__', 'eeg_participant_handedness': '__'}
    """
    # phase 3 records

    p3_records = fetch_bulk_p3()

    p3 = []
    for record in p3_records:

        #filter them down to just those who completed mri or eeg or both
        #if mri_test = yes or eeg_test = yes

        mri_acquisition_complete_value = record.get('mri_acquisition_checklist_complete','')
        print(f'MRI COMPLETE IS: {mri_acquisition_complete_value}, end = \n')
        eeget_log_complete_value = record.get('eeget_session_log_complete','')

        # 2=yes
        if mri_acquisition_complete_value == '2' or eeget_log_complete_value == '2':
            
            p3_fields = { 
                'record_id': record.get('record_id', ''),
                'handedness': get_handedness(record)
            }

            p3.append(p3_fields)
    #print(json.dumps(p3)[0:3])
    return p3

def get_p2(p3):
    """
    """
    #make hash map
    p2_records = fetch_bulk_p2()
    p3_record_ids = {r.get('record_id', '') for r in p3}

    p2 = []

    for record in p2_records:
        study_id = get_study_id(record)

        if record.get('record_id') in p3_record_ids:

            p2_fields = {
                'record_id' : record.get('record_id',''),
                'participant_id' : study_id,
                'cohort' : record.get('ev_status'),
                'site' : get_site_from_id(study_id),       
                'species' : 'homo sapiens',
                'sex' : get_sex(record),    
            }
            
            p2.append(p2_fields)
    #print(json.dumps(p2, indent=2))
    return p2


def merge(p3, p2):
    """
    merge hash map of fields required for a complete q1k participant.tsv. This includes
    participant_id,cohort,species,age_at_eeg_testing,age_at_mri_testing,sex,handedness
    from the phase 3 event from redcap 
    """

    # promote the record_id to "key" pointing to the former dict

    p3_lookup = {r['record_id']: r for r in p3}

    merged = []
    for record in p2:
        p3_data = p3_lookup.get(record['record_id'])

        if p3_data:  # only include if a match exists in p3
            merged.append({
                **record,    # all p2 fields
                **p3_data,   # all p3 fields, joined on record_id
            })
    print(json.dumps(merged, indent=2))
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

def get_site_from_id(merged_id):
    """
    Extract the site required by CBIGR new_profile from study ID substring
    Return: str
    """
    if len(merged_id) < 7:
        return ''
    
    site_code = merged_id[4:7]
    site_map = {
        'MHC': "Montreal Neurological Institute",
        'HSJ': "Centre Hospitalier Universitaire Sainte-Justine",
        'GAT': "Children's Hospital of Eastern Ontario",
        'NIM': "Hôpital Rivière-des-Prairies",
        'OIM': "Douglas Mental Health University Institute",
        'SHR': "Centre Hospitalier Universitaire de Sherbrooke"
    }

    return site_map.get(site_code, '')

def get_handedness(record):
    """
    #1=left, 2=right, 3=ambi, 4=unknown 
    """

    value = record.get('eeg_participant_handedness', ''),
    if value:
        if value == '1':
            translated_value = 'left'
        elif value == '2':
            translated_value = 'right'
        elif value == '3':
            translated_value = 'ambidextrous'
        elif value == '4':
            translated_value = 'unknown'
    else: 
        translated_value = 'unknown'
    
    return translated_value

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
def write_tsv(merged, output_path):
    fieldnames = ['participant_id', 'cohort', 'site', 'species', 'sex', 'handedness']

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        for record in merged:
            writer.writerow({
                'participant_id': record['participant_id'],
                'cohort': record['cohort'],
                'site': record['site'],
                'species': record['species'],
                'sex': record['sex'],
                'handedness': record['handedness'],
            })

    print(f"✅ TSV written to: {output_path}")

def main():
    """
    Main function to build and write the Q1K participant TSV
    """
    p3 = get_imaging()
    p2 = get_p2(p3)
    merged = merge(p3, p2)

    output_path = get_output_path()

    write_tsv(merged, output_path)

if __name__ == "__main__":
    main()