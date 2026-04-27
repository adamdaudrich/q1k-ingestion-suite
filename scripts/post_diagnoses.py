#!/usr/bin/env python3
"""
This file extracts the required CBIG diagnosis information from the 
Q1K REDCap instance API. It filters for only candidates that have been registered by 
cross-checking the external ID in the CBIGR API. It then outputs a CSV file.

values: 1= yes, 0 =no
Returns:
"""
from datetime import datetime
from pathlib import Path
from utils.redcap_api import fetch_diagnosis, get_study_id
from utils.cbigr_api import authenticate, get_candidates
from utils.config import Config

_SESSION = None
_TOKEN = None


def get_diagnosis():
    """
    Extract diagnoses where value is '1' (Yes)
    Returns: dict
    """
    records = fetch_diagnosis()
    extracted_candidates = get_candidates()

    diagnosis_mapping = {
        'Autism Spectrum Disorder': 'cfq_diag_asd',
        'Intellectual Disability': 'cfq_diag_id',
        'Attention Deficit Hyperactivity Disorder': 'cfq_diag_adhd',
        'Fetal Alcohol Syndrome Disorder': 'cfq_diag_fasd',
        'Learning Disorder': 'cfq_diag_ld',
        'Language and Communication Disorder': 'cfq_diag_lcd',
        'Motor Disorder': 'cfq_diag_md',
        'Anxiety Disorder': 'cfq_ment_ad',
        'Depression Disorder':'cfq_ment_dd',
        'Bipolar Disorder': 'cfq_ment_bd',
        'Obsessive Compulsive Disorder':'cfq_ment_ocd',
        'Tourettes Syndrome': 'cfq_ment_ts',
        'Psychosis Episodes': 'cfq_ment_psyep',
        'Schizophrenia': 'cfq_ment_schizo',
        'Substance Abuse': 'cfq_ment_sa',
        'Epilepsy':'cfq_ment_epilepsy',
        'Hearing Disability': 'cfq_ment_hearing_disability',
        'Visual Disability': 'cfq_ment_visual_disability',
        'Physical Disability': 'cfq_ment_physical_disability',
        'Genetic Disorder': 'cfq_ment_genetic_disorder'
    }

    diagnoses = []

    for r in records:
        merged_id = get_study_id(r)

        for c in extracted_candidates:
            pscid = c.get('PSCID')
            if c['ExtStudyID_Q1K'] == merged_id:

                for name, field in diagnosis_mapping.items():
                    if r.get(field) == '1':
                        diagnoses.append({
                            'PSCID': pscid,
                            'Diagnosis': name,
                            'Familial': None,  
                            'Comment': None    
                        })
                break
            
    return diagnoses


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
    base_name = 'diagnosis'
    filename = f'{base_name}_{timestamp}.csv'
    
    # Return the full file path
    return output_dir / filename

def write_result(results):
    """
    Write POST results to a text file
    """
    file_path = get_output_path()
    
    with open(file_path, 'w', encoding='utf-8') as f:
        for result in results:
            f.write(result + '\n')
    
    print(f"Results written to: {file_path}")
    return file_path

def post_diagnosis(diagnosis):
    """
    POST a single diagnosis to CBIGR API
   {
   'PSCID': 'Q1K0000012', 
   'Diagnosis': 'Autism Spectrum Disorder', 
   'Familial': None, 'Comment': None
   }
    """
    

    response = _SESSION.post(
        Config.CBIGR_DIAGNOSIS_URL,
        json=diagnosis,
        headers=_SESSION.headers,
        timeout=10
        )

    if response.status_code == 201:
        result = f"Added {diagnosis['Diagnosis']} for {diagnosis['PSCID']}"

    elif response.status_code == 409:
        result = f"{diagnosis['Diagnosis']} already exists for {diagnosis['PSCID']}"

    else:
        result = f"{diagnosis['Diagnosis']} Failed for {diagnosis['PSCID']}{response.status_code}"

    return result

def main():
    """
    Main function to process and POST diagnoses
    """
    global _SESSION, _TOKEN 
    _SESSION, _TOKEN, _ = authenticate()

    diagnoses = get_diagnosis()

    print(f"Processing {len(diagnoses)} diagnoses...\\n")

    results = []
    added = 0
    skipped = 0
    error = 0

    for diagnosis in diagnoses:      
        result = post_diagnosis(diagnosis)
        results.append(result)
    
        # Count the results
        if "Added" in result:
            added += 1
        elif "already exists" in result:
            skipped += 1
        else:
            error += 1

    write_result(results)

    # Summary
    print(f"\n{'='*50}")
    print(f" Successfully added: {added}")
    print(f" Skipped (no PSCID): {skipped}")
    print(f" Errors: {error}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()