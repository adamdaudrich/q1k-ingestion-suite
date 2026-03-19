"""
Extracts data required for GUID-registration in CBIGR new_profile CSV-Uploader.
Each function is fed by a "for record in records" for loop, bulding the condidate
object incrementally as per function concern.
"""

from datetime import datetime
import csv
from pathlib import Path
from utils.redcap_api import fetch_registration # pylint: disable=import-error,wrong-import-position
from scripts.build_consents import extract_consent_data

def get_personal_fields(record):
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

    return {
        'Date of Birth': record.get('enr2_pro_dob', ''),
        'Sex': sex,
        'First Name': record.get('enr2_pro_prob_fname', ''),
        'Middle Name': '',
        'Last Name': record.get('enr2_pro_prob_lname', ''),
        'Place Of Birth': record.get('enr2_pro_dob_city') or 'Montreal', 
        'Province Of Birth': 'Not Available',
        'Country Of Birth': record.get('enr2_pro_dob_country') or 'Canada'
    }

def get_study_id(record):
    """
    Extract, merge and format the study ID from REDcap required by CBIGR new_profile
    """
    proband_id = record.get('q1k_proband_id_1', '')
    relative_id = record.get('q1k_relative_idgenerated_1', '')
    merged_id = proband_id or relative_id or ''

    return merged_id.replace('_', '-')


def get_site_from_id(merged_id):
    """
    Extract the site required by CBIGR new_profile from study ID substring
    """
    if len(merged_id) < 7:
        return ''
    
    site_code = merged_id[4:7]
    site_map = {
        'MHC': "Montreal Neurological Institute",
        'HSJ': "Centre Hospitalier Universitaire Sainte-Justine",
        'GAT': "Children's Hospital of Eastern Ontario",
        'OIM': "Hôpital Rivière-des-Prairies",
        'NIM': "Douglas Mental Health University Institute",
        'SHR': "Centre Hospitalier Universitaire de Sherbrooke"
    }

    return site_map.get(site_code, '')

def filter_non_consented_participants(record):
    """
    Remove participant that does not have consent
    """

    consent = extract_consent_data(record)
    print(f"CONSENT IS {consent} /n")

    return consent

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
    base_name = 'registration'
    filename = f'{base_name}_{timestamp}.csv'
    
    # Return the full file path
    return output_dir / filename


def write_registration_csv(candidates):
    """
    Write registration data to CSV
    """
    reg_csv_path = get_output_path()

    fieldnames = ['Date of Birth', 'Sex', 'Site', 'Project', 'Study Name',
                  'Study ID', 'First Name', 'Middle Name', 'Last Name',
                  'Place Of Birth', 'Province Of Birth', 'Country Of Birth']

    with open(reg_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(candidates)

    print(f"✅ CSV written to: {reg_csv_path}")


def main():
    """
    Build the candidate object and write csv
    """
    print(f"extract_consent_data function: {extract_consent_data}")
    print(f"extract_consent_data module: {extract_consent_data.__module__}")
    records = fetch_registration()

    print(f"Total records fetched: {len(records)}")

    candidates = []

    for record in records:
        consent = extract_consent_data(record)
        study_id = get_study_id(record)
        if study_id != '':
            if consent == 'Yes':
                site = get_site_from_id(study_id)
                personal = get_personal_fields(record)


                # Compose the candidate
                candidate = {
                    'Project': 'Québec 1000 Families (Q1K)',
                    'Study Name': 'Q1K',
                    'Study ID': study_id,
                    'Site': site,
                    **personal
                }
                candidates.append(candidate)
    print (f"total candidates: {len(candidates)}")

    write_registration_csv(candidates)


if __name__ == "__main__":
    main()        