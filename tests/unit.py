"""
Test data transformations and types
"""

from scripts.rename_bids import get_merged_bids, match_subid_to_pscid
from utils.cbigr_api import get_loris_ids


def test_get_merged_bids():
    """
    
    """

    merged_bids = get_merged_bids()
    print(f'THERE ARE: {len(merged_bids)} BIDS')
    assert isinstance(merged_bids, set)
    #for i in merged_bids:
        #print(i)

    return None

def test_rename_bids():

    merged_bids = get_merged_bids()
    assert isinstance(merged_bids, set)

    pscid_subid_extid = match_subid_to_pscid()
    assert isinstance(pscid_subid_extid, list)
    for i in pscid_subid_extid[0:3]:
        print(i)

if __name__ == "__main__":
    test_rename_bids()