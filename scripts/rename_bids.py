"""
Rename post-merged bids into a new output directory (non-destructive)
"""

from utils.cbigr_api import get_loris_ids
from utils.config import Config
from pathlib import Path
import shutil
import os
import tempfile
import json
import csv

SES_NAME = 'ses-Q1KDeepPhenotyping01'


def get_merged_bids():
    merged_bids = {f for f in os.listdir(Config.MERGED_BIDS) if f.startswith('sub-')}
    return merged_bids


def match_ids():
    loris_ids = get_loris_ids()
    merged_bids = get_merged_bids()

    pscid_subid_extid = []
    for i in loris_ids:
        pscid = i['pscid']
        extid = i['extid']
        parts = extid.split('-')
        if len(parts) < 4:
            continue
        extid_clean = parts[-2][-4:] + parts[-1]

        for m in merged_bids:
            if m == 'sub-' + extid_clean:
                pscid_subid_extid.append({
                    'pscid': pscid,
                    'subid': m,
                    'extid': extid
                })

    return pscid_subid_extid


def reidentify_string(value: str, subid: str, pscid: str) -> str:
    """Replace subid pattern in a string value (for file contents)."""
    if not isinstance(value, str):
        return value
    return value.replace(subid, f'sub-{pscid}').replace('ses-01', SES_NAME)


def reidentify_in_dict(obj, subid: str, pscid: str):
    """Recursively walk a JSON-decoded structure and replace identifiers in values."""
    if isinstance(obj, dict):
        return {k: reidentify_in_dict(v, subid, pscid) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [reidentify_in_dict(item, subid, pscid) for item in obj]
    elif isinstance(obj, str):
        return reidentify_string(obj, subid, pscid)
    return obj


def handle_tsv(src: Path, dest: Path, subid: str, pscid: str):
    """Copy TSV, replacing identifiers in every cell (tab-delimited)."""
    with src.open('r', newline='', encoding='utf-8') as fin, \
         dest.open('w', newline='', encoding='utf-8') as fout:
        reader = csv.reader(fin, delimiter='\t')
        writer = csv.writer(fout, delimiter='\t')
        for row in reader:
            writer.writerow([reidentify_string(cell, subid, pscid) for cell in row])

def handle_csv(src: Path, dest: Path, subid: str, pscid: str):
    """Copy CSV, replacing identifiers in every cell (comma-delimited)."""
    with src.open('r', newline='', encoding='utf-8') as fin, \
         dest.open('w', newline='', encoding='utf-8') as fout:
        reader = csv.reader(fin)
        writer = csv.writer(fout)
        for row in reader:
            writer.writerow([reidentify_string(cell, subid, pscid) for cell in row])

def handle_json(src: Path, dest: Path, subid: str, pscid: str):
    """Copy JSON, recursively replacing identifiers in all string values."""
    data = json.loads(src.read_text(encoding='utf-8'))
    data = reidentify_in_dict(data, subid, pscid)
    dest.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')


def apply_renames(name: str, subid: str, pscid: str) -> str:
    """Apply both sub and ses renames to a file/dir name."""
    name = name.replace(subid, f'sub-{pscid}')
    name = name.replace('ses-01', SES_NAME)
    return name

def copy_and_rename(src_dir: Path, dest_dir: Path, matches: list, dry_run=True):
    """
    Copy the renamed files to a temp folder to complete the rename, 
    then transfer to new folder
    """
    
    # parents = true creates the parent paths to the eventual destination dir
    # exist_ok = don't throw error if it already exists
    dest_dir.mkdir(parents=True, exist_ok=True)

    #break it down to just subid and pscid
    subid_to_pscid = {m['subid']: m['pscid'] for m in matches}

    #iterdir is a Path method that lists everything, files and subdirectories, one deep
    for item in src_dir.iterdir():
        #checks if the current subid in matches matches the folder name
        matched_subid = next((sid for sid in subid_to_pscid if item.name.startswith(sid)), None)

        if matched_subid:
            pscid = subid_to_pscid[matched_subid]
            new_name = apply_renames(item.name, matched_subid, pscid)
        else:
            new_name = item.name

        dest_path = dest_dir / new_name

        # skip if the pscid already exists in dest dir
        if matched_subid and (dest_dir / f"sub-{pscid}").exists():
            print(f"Skipping {matched_subid} -> sub-{pscid}: already exists in {dest_dir}")
            continue

        if dry_run:
            print(f"{item}\n\t-> {dest_path}")
        else:
            #creates temporary directory in the destination dir, deleted whent he block exits
            with tempfile.TemporaryDirectory(dir=dest_dir) as tmp:
                #build path for the item inside the temp directory
                tmp_path = Path(tmp) / new_name
                if item.is_dir():
                    # call _copy_tree_renamed recursively
                    _copy_tree_renamed(item, tmp_path, matched_subid, pscid if matched_subid else None)
                else:
                    shutil.copy2(item, tmp_path)
                shutil.move(str(tmp_path), dest_path)


def _copy_tree_renamed(src: Path, dest: Path, subid: str | None, pscid: str | None):
    """Recursively copy a directory tree, renaming files and folders as we go."""
    dest.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        new_name = apply_renames(item.name, subid, pscid) if subid and pscid else item.name
        dest_item = dest / new_name
        if item.is_dir():
            _copy_tree_renamed(item, dest_item, subid, pscid)

        elif subid and pscid:
            ext = item.suffix.lower()
            # Check double extension for .nii.gz
            if ext == '.gz' and item.stem.endswith('.nii'):
                # NIfTI: just copy (header scrubbing not implemented; add nibabel call here if needed)
                shutil.copy2(item, dest_item)
            elif ext == '.tsv':
                handle_tsv(item, dest_item, subid, pscid)
            elif ext == '.csv':
                handle_csv(item, dest_item, subid, pscid)
            elif ext == '.json':
                handle_json(item, dest_item, subid, pscid)
            else:
                shutil.copy2(item, dest_item)
        else:
            shutil.copy2(item, dest_item)


def main():
    matches = match_ids()

    if not matches:
        print("All subjects already renamed.")
        return

    copy_and_rename(Config.MERGED_BIDS, Config.RENAMED_BIDS, matches, dry_run=False)  # flip to False when ready


if __name__ == '__main__':
    main()
