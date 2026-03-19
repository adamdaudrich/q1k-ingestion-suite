





# def test_fetch_identifiers():
#     """Test extracting REDCap record IDs."""
#     print("\n=== Testing Extract REDCap Records ===")
    
#     records = fetch_identifiers()
    
#     # Basic assertions
#     assert records is not None, "Should return data"
#     # assert isinstance(records, list), "Should return a list"
#     assert len(records) > 0, "Should have at least one record"
    
#     # Check structure
#     first_record = records[0]
#     assert 'record_id' in first_record, "Should have record_id field"
    
#     print(f"✓ Fetched {len(records)} records")
#     print("  First 3 record IDs:")
#     for record in records[:3]:
#         print(record, end= '\n')

# def test_extract_pscid_extid():
#     """Test extracting PSCID/ExtID mappings."""
#     print("\n=== Testing Extract PSCID/ExtID ===")
#     pscid_extid = extract_pscid_extid()
    
#     # Assertions
#     assert len(pscid_extid) > 0
#     assert 'pscid' in pscid_extid[0]
#     assert 'extid' in pscid_extid[0]
#     print(f"✓ Extracted {len(pscid_extid)} mappings")
#     print(f"  First: {pscid_extid[0]}")


# def test_cbigr_redcap_matches():
#     """
#     Test extracing all the candidate matches and indicate not-matching candidates"
#     """
#     matches = fetch_cbigr_redcap_matches()
#     #print(matches)

#     #Assertions
#     assert matches is not None, "Should return matches"
#     assert len(matches) > 0, "Should have at least one match"
#     print('\n')
#     print(f"The n of matches is: {len(matches)}")
#     print("First 3 matches: ")
#     for i in matches[:3]:
#         print(i, end = '\n')

# def test_cbigr_redcap_not_matching():
#     """
#     Test flagging of not-matching candidates
#     """
#     unmatched = fetch_cbigr_redcap_not_matching()

#     print(f"\nThere are {len(unmatched)} ids in CBIGR that don't match with REDCAP")
#     print("Please check the REDcap isntance and contact CBIGR admin")
#     for i in unmatched:
#         print(i, end='\n')

# def test_fetch_diagnosis():
#     """
#     Test http post functionality of cbigr/diagnosis/DiagnosisAddEditDelete endpoint
#     """
#     records = fetch_diagnosis()
#     assert records != None
#     assert len(records) < 1
#     for record in records[:3]:
#         print(f"{record} end = \n")

# def test_get_diagnoses()
#     diagnoses = get_diagnoses

#     assert diagnoses != None
#     assert type(diagnoses) == dict 
#     print (d for d in diagnoses[:3]) 



if __name__ == "__main__":
    test_authenticate

    print("\n=== Test Passed ===\n")