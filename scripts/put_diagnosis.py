#!/usr/bin/env python3
"""
This file extracts the required CBIG diagnosis information from the 
Q1K REDCap instance API. It filters for only candidates that have been registered by 
cross-checking the external ID in the CBIGR API. It then outputs a CSV file.

values: 1= yes, 0 =no
Returns:
"""
from utils.get_diagnoses import get_diagnosis
from utils.cbigr_api import authenticate
from utils.config import Config
from scripts.post_diagnosis import get_diagnosis

_SESSION = None
_TOKEN = None


def put_diagnosis(diagnosis):
    """
    POST a single diagnosis to CBIGR API
   {
   'PSCID': 'Q1K0000012', 
   'Diagnosis': 'Autism Spectrum Disorder', 
   'Familial': None, 'Comment': None
   }
    """

    if not _SESSION or not _TOKEN:
        authenticate()

    response = _SESSION.put(
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
        result = f"Failed ({response.status_code}): {response.text}"

    return result

def main():
    """
    Main function to process and POST diagnoses
    """

    diagnoses = get_diagnosis()

    print(f"Processing {len(diagnoses)} diagnoses...\\n")

    added = 0
    skipped = 0
    error = 0

    for diagnosis in diagnoses:       
        put_diagnosis(diagnosis)

    # Summary
    print(f"\n{'='*50}")
    print(f" Successfully added: {added}")
    print(f" Skipped (no PSCID): {skipped}")
    print(f" Errors: {error}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()