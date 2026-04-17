"""
Rename post-merged bids
"""

from utils.cbigr_api import get_loris_ids
from utils.config import Config
from pathlib import Path
import os

SES_NAME = 'ses-Q1KDeepPhenotyping01'


def get_merged_bids():
    """
    Get a list of renamed bids for eventual comparison to PSCID 
    from extracted_candidates
    """
    merged_bids = {f for f in os.listdir(Config.MERGED_BIDS) if f.startswith('sub-')}
    return merged_bids


def match_ids():
    """
    Associate the bids sub-type id with the CBIGR externalID
    for the purpose of renaming the BIDS.

    Returns list of dicts with keys: pscid, subid, extid
    """
    loris_ids = get_loris_ids()
    merged_bids = get_merged_bids()

    pscid_subid_extid = []
    for i in loris_ids:
        pscid = i['pscid']
        extid = i['extid']
        # ex Q1K-MHC-100119-P -> 0119P
        parts = extid.split('-')
        if len(parts) < 4:
            continue
        #extid_truncated = extid[-6:]
        extid_clean = parts[-2][-4:] + parts[-1] 
        #ls extid_clean = extid_truncated.replace("-", "")

        for m in merged_bids:
            if m == 'sub-' + extid_clean:
                pscid_subid_extid.append({
                    'pscid': pscid,
                    'subid': m,
                    'extid': extid
                })

    return pscid_subid_extid


def find_sub(bids_dir, subid):
    """
    Recursively find all paths in the bids_dir that contain subid.
    Returns a sorted list of Path objects, deepest first (bottom-up).
    """
    bids_path = Path(bids_dir)
    hits = sorted(bids_path.rglob(f'*{subid}*'), key=lambda p: len(p.parts), reverse=True)
    return hits


def find_ses(bids_dir, sesid='ses-01'):
    """
    Find all ses directories in all levels of the targeted bids_dir.
    Returns a sorted list of Path objects, deepest first (bottom-up).
    """
    bids_path = Path(bids_dir)
    hits = sorted(bids_path.rglob(f'*{sesid}*'), key=lambda p: len(p.parts), reverse=True)
    return hits


def rename_ses(bids_dir, dry_run=False):
    """Rename all instances of ses-01 to SES_NAME."""
    hits = find_ses(bids_dir)
    for path in hits:
        new_name = path.name.replace('ses-01', SES_NAME)
        if dry_run:
            print(f"{path}\n\t-> {path.parent / new_name}")
        else:
            path.rename(path.parent / new_name)


def rename_sub(bids_dir, matches, dry_run=True):
    """Rename all subid directories and files to their corresponding pscid."""
    for match in matches:
        hits = find_sub(bids_dir, match['subid'])
        for path in hits:
            new_name = path.name.replace(match['subid'], "sub-" + match['pscid'])
            if dry_run:
                print(f"{path}\n\t-> {path.parent / new_name}")
            else:
                path.rename(path.parent / new_name)


def main():
    """
    Rename all sub- and ses- level BIDS directories from subid to pscid
    and ses-01 to SES_NAME.
    """
    matches = match_ids()

    # rename ses first, then sub, from bottom up
    rename_ses(Config.MERGED_BIDS)
    rename_sub(Config.MERGED_BIDS, matches)


if __name__ == '__main__':
    main()