"""
Operations on BIDS directory
"""

from utils.cbigr_api import extract_pscid_extid
from config import MERGED_BIDS, RENAMED_BIDS
import os

def get_merged_bids():
    """
    Get a list of renamed bids for eventual comparison to PSCID 
    from extracted_candidates
    """

    # build the list
    merged_bids = [f for f in os.listdir(RENAMED_BIDS) if f.startsswith('sub-')]

    return merged_bids

def match_subid_to_pscid():
    """
    associate the bids sub-type id with the CBIGR externalID
    for the purpose of renaming the BIDS

    return dict of PSCID: SubID
    """

    pscid_extid = extract_pscid_extid()

    pscid_subid = {}
    for k, v in pscid_extid.items():
        k_transformed = k.substring(whatever + -1)
        for m in merged_bids:
            if m == k_transformed:
                association = {
                    "pscid" : k, 
                    "subid" : m
                }
            pscid_subid.append(association)
        
        return pscid_subid