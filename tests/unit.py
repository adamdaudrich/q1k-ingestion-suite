from q1k_ingestion_suite.utils.get_family_relationships import get_family_relationship

def main():
    """Test merging the two different study identifiers in the q1k redcap."""
    print("\n=== Testing Extract REDCap Records ===")

    records = fetch_identifiers()

    for record in records:
        merged_id = get_study_id()

    assert merged_id is not None, "Should return the merged identifier"
    assert len(merged_id) > 0, "Should have at least one record"
    first_extid = merged_id[0]
    assert first_extid
    
    print(f"✓ Fetched {len(records)} records")
    print("  First 3 record IDs:")
    for id in merged_ids[:3]:
        print(record, end= '\n')

def main():
    """Test merging the two different study identifiers in the q1k redcap."""
    print("\n=== Testing Get Family Relationship ===")

    extid_family_rel = get_family_relationship()

    assert ext_id_family_rel is not None, "Should return the merged identifier"
    assert len(ext_id_family_rel) > 0, "Should have at least one record"
    first_extid_family_rel = ex_id_family_rel[0]
    assert first_extid_family_rel
    
    print(f"✓ Fetched {len(ext_id_family_rel)} records")
    print("  First 3 record IDs:")
    for i in ext_id_family_rel[:3]:
        print(i, end= '\n')

    if __name__ == "__main__":
        main()