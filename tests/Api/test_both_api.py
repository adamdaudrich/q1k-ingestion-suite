"""
Test Both Api
"""
from utils.both_api import (
    get_cbigr_redcap_matches,
    get_cand_id_record_id
)

def test_get_cbigr_redcap_matches():
    """
    Test
    Returns: None
    """

    matches = get_cbigr_redcap_matches()

    assert matches is not None
    print('\n')
    for i in matches[:3]:
        print(i, end ='\n')


def test_get_cand_id_record_id():
    """
    Test
    """

    cand_id_record_id = get_cand_id_record_id()

    assert cand_id_record_id is not None
    assert len(cand_id_record_id) > 0
    print(len(cand_id_record_id))


