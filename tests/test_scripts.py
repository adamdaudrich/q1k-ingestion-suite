"""
Test Scripts
"""

from scripts.build_candidates import get_personal_fields, get_study_id, get_site_from_id, get_output_path, write_registration_csv
from scripts.rename_bids import get_merged_bids, match_ids, find_ses, find_sub, rename_ses, rename_sub 
from utils.config import Config

def test_build_candidates():
    """
    Test
    
    Return: None
    """

    prsnl_flds = get_personal_fields()
    assert prsnl_flds is not None
    assert all(k in prsnl_flds for k in ('Date of Birth', 'Sex', 'First Name', 
    'Middle Name', 'Last Name', 'Place of Birth', 'Province of Birth', 
    'Country of Birth'))

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

def get_merged_bids():
    """
    Test
    """

    merged_bids = get_merged_bids()
    print(f"The number of bids directories is {len(merged_bids)}")
    print(f"{type(merged_bids)}")
    for i in merged_bids:
        print(i, end =" ")

def test_match_ids():
    """
    Test the matching of subid from the brain imaging centre filesystem, and pscid and extid
    from the cbigr api. Extid originates from REDcap
    """
    #match the pscid, extid and sub id
    pscid_subid_extid = match_ids()
    assert pscid_subid_extid is not None
    assert len(pscid_subid_extid) > 0
    print('\n')
    print(f"The number of matches is {(len(pscid_subid_extid))}")

    print(type(pscid_subid_extid)) 
    for i in pscid_subid_extid[0:10]:
        print(i, end = '\n')

def test_find_sub():
    """
    Test
    """
    # set the path to the test bids_dir
    test_bids_dir = Config.TEST_BIDS

    hits = find_sub(test_bids_dir, subid='sub-0296P')
    assert hits is not None
    print(f"The return of file paths is {type(hits)}")
    for i in hits:
        print(i)

def test_find_ses():
    """
    Test
    """
    test_bids_dir = Config.TEST_BIDS
    hits = find_ses(test_bids_dir)
    assert hits is not None
    print(f"The return of file paths is {type(hits)}")
    for i in hits:
        print(i)

def test_rename_ses():
    """
    Test
    """
    rename_ses(Config.TEST_BIDS, dry_run=True)

def test_rename_sub():
    """
    Test
    """
    matches = match_ids()
    print(f"WOULD RENAME {Config.TEST_BIDS} AS FOLLOWS:")
    print("\n")
    rename_sub(Config.TEST_BIDS, matches, dry_run=True)


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
    Test
    """

if __name__ == "__main__":
    test_build_candidates()
    test_match_ids()
    find_ses()
    test_find_sub()
    rename_ses()
    rename_sub()
