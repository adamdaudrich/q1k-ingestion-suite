"""
Test to build the consents generated from the REDcap API
"""

from scripts.build_consents import (
    extract_consent_data,
    extract_date,
    get_output_path,
    write_consent_csv
)

def test_build_consents():
    """
    Test
    """
    csv_path = get_output_path

    if csv_path is not None:
        print(f"THE CSV OUT FILE PATH IS {csv_path}")
    else:
        print("THE CSV OUT FILE PATH DOES NOT EXIST")
