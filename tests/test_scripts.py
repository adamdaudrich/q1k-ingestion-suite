"""
Test Scripts
"""

from scripts.build_candidates import get_personal_fields, get_study_id,
get_site_from_id, get_output_path, write_registration_csv
from scripts.build_consents import
from scripts.build_family_relationships import
from scripts.build_record_ids import
from scripts.get_cbigr_redcap_unmatched import
from scripts.post_diagnoses import
from scripts.rename_bids import

def test_build_candidates():
    """
    Test
    
    Return: None
    """

    prsnl_flds = get_personal_fields()
    assert prsnl_flds is not None
    assert 'Date of Birth', 'Sex', 'First Name', 'Middle Name', 
    'Last Name', 'Place of Birth', 'Province of Birth', 
    'Country of Birth' in prsnl_flds.keys()

    fetch = {
        'record_id': 'Q1K test - (for Irini)', 
        'q1k_proband_id_1': 'Q1K-MHC-2-Q1K test - (for Carlos)-P', 
        'q1k_relative_idgenerated_1': ''
        }

    q1k_key = get_study_id(fetch)
    assert q1k_key is not None
    assert type(q1k_key) == str
    assert q1k_key == 'Q1K-MHC-2-Q1K test - (for Carlos)-P' 

    site = get_site_from_id(q1k_key)
    assert site is not None
    assert type(site) == str
    assert site == 'Monteal Neurological Institute'
    assert site == 'Casablanca'


    return None



def test_build_consents():
"""
Test
"""

def test_build_family_relationships():
"""
Test
"""


def test_build_record_ids():
"""
Test
"""

def test_cbigr_redcap_unmatched():
"""
Test
"""

def test_post_diagnoses():
"""

"""

def test_rename_bids():
"""
Test
"""


if __name__ == "__main__":
    test_build_candidates()
