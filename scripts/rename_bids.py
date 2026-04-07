"""
Rename post-merged bids
"""

from utils.cbigr_api import get_loris_ids
from utils.config import Config
import os

def get_merged_bids():
    """
    Get a list of renamed bids for eventual comparison to PSCID 
    from extracted_candidates
    """

    # build the list
    merged_bids = {f for f in os.listdir(Config.MERGED_BIDS) if f.startswith('sub-')}

    return merged_bids

def match_subid_to_pscid():
    """
    associate the bids sub-type id with the CBIGR externalID
    for the purpose of renaming the BIDS

    return dict of PSCID: SubID
    """

    loris_ids = get_loris_ids()
    merged_bids = get_merged_bids()

    pscid_subid_extid = []
    for item in loris_ids.items():
        pscid = item['pscid']
        extid = item['extid']
        # ex Q1K-MHC-100119-P -> 0119-P
        extid_truncated = extid[-6:]
        extid_clean = extid_truncated.replace("-", "")
        
        for m in merged_bids:
            if m == 'sub-' + extid_clean:
                pscid_subid_extid.append({
                    'pscid' : pscid,
                    'subid' : m,
                    'extid' : extid
                })
        
    return pscid_subid_extid