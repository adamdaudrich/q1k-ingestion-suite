"""
This file extracts the required the family relationship information
needed in CBIGR family table (adam modified version)
Returns:

"""
from datetime import datetime
import json
from pathlib import Path
from utils.redcap_api import fetch_family_relationship
from utils.cbigr_api import get_candidates


def get_family_relationships():
    """
    Get the family relationship to the external ID
    returns: Dict
    """

    records = fetch_family_relationship()
    extracted_candidates = get_candidates()

#[{'Q1k-100101-P': {'biological_mother': 'Q1K-MHC-100101-M1','biological_father': 'Q1K-MHC-100101-F1','sibling': 'Q1k-MHC-100101-S1'}}]

    family_dict = {}

    extid_set = {c['ExtStudyID_Q1K'] for c in extracted_candidates}

    for r in records:

        rel_proband_id = r.get('q1k_rel_proband_id')
        hyphen_rel_proband_id = None
        if rel_proband_id:
            hyphen_rel_proband_id = rel_proband_id.strip("()").split(": ")[1].replace("_", "-")

        rel_id = r.get('q1k_relative_idgenerated_1')
        hyphen_rel_id = None
        if rel_id:
            hyphen_rel_id = rel_id.replace("_","-")


        # Determine which ID to use as the key
        key = None
        if hyphen_rel_proband_id in extid_set:
            key = hyphen_rel_proband_id

        # Initialize the proband if needed
        if key and key not in family_dict:
            family_dict[key] = {}
        
        # Now add the relationship data in the SAME loop
        if key:
            relationship_code = r.get('enr2_pro_rel_prob_2')
            family_dict[key][relationship_code] = hyphen_rel_id

            
    #now you have a list of objects that are candid=>code
    #map the readable word on the code, returning candid=>relationship

    family_rel_map = {
    '13':'half_sibling',
    '9':'full_sibling',
    '2':'adoptive_mother',
    '6':'adoptive_father',
    '15':'adoptive_child',
    '10':'adoptive_sibling',
    '1':'biological_mother',
    '5':'biological_father',
    '14':'biological_child',
    '4':'foster_mother',
    '8':'foster_father',
    '17':'foster_child',
    '12':'foster_sibling',
    '3':'step_mother',
    '7':'step_father',
    '16':'step_child',
    '11':'step_sibling',
    '99':'other'
    }

    family_relationships = []

    # Create new dict with readable relationships
    family_relationships = {}
    for proband, family_members in family_dict.items():
        family_relationships[proband] = {}
        for code, member_id in family_members.items():
            readable_rel = family_rel_map.get(code, 'unknown')
            family_relationships[proband][readable_rel] = member_id

    return family_relationships


def get_output_path():
    """
    Get the output CSV path and ensure directory exists
    """
    # Define output directory relative to script
    script_dir = Path(__file__).parent
    output_dir = script_dir / 'json'

    # Create directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d')
    base_name = 'family_relationships'
    filename = f'{base_name}_{timestamp}.json'

    # Return the full file path
    return output_dir / filename

def write_relationships_json(relationships):
    """
    Write consent data to CSV
    """

    relationships_json_path = get_output_path()

    fieldnames = ['CandID', 'Relationship Type']

    with open(relationships_json_path, 'w', newline='', encoding='utf-8') as f:
        json.dump(relationships, f, indent = 4)

    print(f"✅ JSON written to: {relationships_json_path}")


def main():
    """create a json file from the object"""

    relationships = get_family_relationships()
    write_relationships_json(relationships)

if __name__ == "__main__":
    main()