"""
Test Redcap API
"""

import requests
from utils.redcap_api import (
    fetch_identifiers,
    fetch_registration,
    fetch_consents,
    fetch_diagnosis,
    fetch_family_relationship,
    get_record_id_external_id,
    fetch_session,
)

from scripts.build_sessions import get_sessions
from scripts.post_diagnoses import get_diagnosis
from utils.config import Config
from pprint import pprint

REDCAP_TOKEN = Config.REDCAP_TOKEN
REDCAP_URL = Config.REDCAP_URL

def test_validate_token():
    """Test that REDCap API token is valid"""
    data = {
        'token': REDCAP_TOKEN,
        'content': 'project',
        'format': 'json'
    }

    print(data)
    
    response = requests.post(REDCAP_URL, data=data, timeout=30)
    response.raise_for_status()

    if not response.json():
        raise ValueError("Invalid REDCap API token")

    return None

def test_fetch_identifiers():
    """Test"""

    records = fetch_identifiers()
    assert records is not None
    assert len(records) > 0
    print(type(records))

    print("FIRST THREE RECORDS:")
    for i in records[:3]:
        print (i, end= '\n')

    print("LAST THREE RECORDS:")
    for i in records[-3:]:
        print (i, end= '\n')

def test_fetch_consents():
    """Test"""
    
    records = fetch_consents()

    assert records is not None
    assert len(records) > 0
    print(type(records))
    print(f'THE AMOUNT OF RECORDS IS {len(records)}')

    for i in records[:3]:
        print(i, end = '\n')

    for i in records[-3:]:
        print(i, end='\n')

    incomplete_count = 0
    unverified_count = 0
    for idx, i in enumerate(records):
        if i['icf_form_phase_2_complete'] == '0':
            incomplete_count += 1
        
        elif i['icf_form_phase_2_complete'] == '1':
            unverified_count += 1

    print(f'THE AMOUNT OF INCOMPLETE CONSENTS (Marked 0) IS {incomplete_count}')
    print(f'THE AMOUNT OF UNVERIFIED CONSENTS IS (Marked 1) {unverified_count}')

def test_fetch_registration():
    """Test """
    
    records = fetch_registration()

    assert records is not None
    assert len(records) > 0
    print(type(records))
    print(f'THE TOTAL NUMBER OF RECORDS IS {len(records)}')

def test_fetch_diagnosis():
    """Test"""

    records = fetch_diagnosis()

    assert records is not None
    assert len(records) > 0

    print(type(records))
    print(f'THE AMOUNT OF RECORDS IS {len(records)}')

    for i in records[:3]:
        print(i, end = '\n')

    for i in records[-3:]:
        print(i, end = '\n')

def test_get_diagnosis():
    """Test"""

    diagnoses = get_diagnosis()
    assert diagnoses is not None
    assert len(diagnoses) > 0
    print(type(diagnoses))
    print(f"THE AMOUNT OF DIAGNOSES IS {len(diagnoses)}")

    for i in diagnoses:
        print(i, end= '\n')

def test_get_record_id_external_id():
    """Test"""

    ids = get_record_id_external_id()
    assert isinstance(ids, dict)
    assert len(ids) > 0

    print(type(ids))
    print(f'THE AMOUNT OF RECORD_IDs and EXTERNAL IDs is {len(ids)}')

    for record_id, ext_id in list(ids.items())[:10]:
        print(f'record_id: {record_id}, ext_id: {ext_id}')

def test_fetch_family_relationship():
    """Test """

    records = fetch_family_relationship()
    assert records is not None
    assert len(records) > 0
    print(type(records))
    print(len(records))

    for i in records[10:20]:
        print(i)

def test_get_family_relationships():
    """
    Gets a list of dicitonaries with probands as keys and a list of
    family ids and their relationships as values
    Return: None
    """

    relationships = get_family_relationships()

    assert relationships is not None
    print(type(relationships))
    print(f'THE AMOUNT OF FAMILIES IS: {len(relationships)}')
    print(relationships)

def test_fetch_session():
    """
    Get a jsonified response object of the sessions per candidate
    """
    fetch = fetch_session()

    assert fetch is not None
    assert len(fetch) > 0
    print(fetch)

    return None

def test_get_sessions():

    sessions = get_sessions()
    assert sessions is not None
    assert len(sessions) > 0
    pprint(sessions)

    return None

if __name__ == "__main__":
    test_validate_token()
    test_fetch_identifiers()
    test_fetch_consents()
    test_fetch_registration()
    test_fetch_diagnosis()
    test_get_diagnosis()
    test_get_record_id_external_id()
    test_fetch_family_relationship()
    test_get_family_relationships()
    test_fetch_session()
    test_get_sessions()
 