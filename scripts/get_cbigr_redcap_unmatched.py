"""
Produce a list of matches for registration verification purposes
"""
from pprint import pprint
from utils.cbigr_api import get_candidates
from utils.redcap_api import fetch_identifiers, get_study_id


def get_cbigr_redcap_unmatched():
    """
    Match CBIGR candidates with REDCap records
    Returns: list of dicts
    """
    extracted_candidates = get_candidates()
    redcap_ids = fetch_identifiers()

    matches = []
    matched_extids = set()

    for c in extracted_candidates:
        pscid = c.get('PSCID')
        extid = c.get('ExtStudyID_Q1K')

        for r in redcap_ids:
            merged_id = get_study_id(r)
            if extid == merged_id:
                matched_extids.add(extid)
                combined_record = {'pscid': pscid, **r}
                matches.append(combined_record)

    unmatched = [r for r in redcap_ids if get_study_id(r) not in matched_extids]
    print(f"✅ Matched: {len(matches)}")
    print(f"❌ Unmatched: {len(unmatched)}")

    return unmatched

if __name__ == "__main__":
    unmatched = get_cbigr_redcap_unmatched()
