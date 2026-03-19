"""
This file extracts the required the family relationship information
needed in CBIGR family table (adam modified version)
Returns:

"""
from datetime import datetime
import json
from pathlib import Path
from utils.get_family_relationships import get_family_relationships


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