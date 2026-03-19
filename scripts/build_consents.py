"""
This file extracts the required CBIG consent information from the 
Q1K REDCap instance API. 
Returns:
"""
from datetime import datetime
import csv
from pathlib import Path
from utils.redcap_api import fetch_consents, get_study_id

def extract_consent_data(record):
    """
    Extract consent value and date of consent from ICF form phase 2.
    where 2 = yes, 1 = incomplete 0 = unverified. 
    The CBIGR import_consent.php script requires values 'yes' or 'no'
    """

    signed_consent = ''
    consent_value = record.get('icf_form_phase_2_complete','')
    if consent_value == '2':
        signed_consent = 'Yes'
    elif consent_value == '1':
        signed_consent = 'No'
    elif consent_value == '0':
        signed_consent = 'No'
    else:
        signed_consent = ''

    return signed_consent

def extract_date(record):
    """
    Extract the date as required by the insert_consent.php script in CBIGR
    "infile" argument.
    """
    date_given = record.get('date_persstudy_p2', '')

    if date_given and ' ' in date_given:
        date_given = date_given.split(' ')[0]

    return date_given

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
    base_name = 'phase_2_consent'
    filename = f'{base_name}_{timestamp}.csv'

    # Return the full file path
    return output_dir / filename


def write_consent_csv(consents):
    """
    Write consent data to CSV
    """

    cons_csv_path = get_output_path()

    fieldnames = ['Record ID', 'Signed Consent', 'Date Given']

    with open(cons_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(consents)

    print(f"✅ CSV written to: {cons_csv_path}")

def main():
    """Orchestrate the consent data extraction pipeline"""

    records = fetch_consents()
    consents = []

    for record in records:
        merged_id = get_study_id(record)
        consent = extract_consent_data(record)
        date = extract_date(record)


        consent_data = {
            'Record ID': merged_id,
            'Signed Consent': consent,
            'Date Given' : date
        }
        consents.append(consent_data)

    write_consent_csv(consents)

if __name__ == "__main__":
    main()