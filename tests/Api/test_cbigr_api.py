"""
Test CBIGR API Authentication
"""
import json
from utils.config import Config
from utils.cbigr_api import (
    authenticate,
    fetch_candidates,
    get_candidates
)

def test_authenticate():
    """
    Test
    """

    print("\n=== Testing CBIGR Login ===")

    # Make the call
    session, token, response = authenticate()

    # 1. HTTP Response
    print("\n1. HTTP Response:")
    print("   Status: {response.status_code}")
    print("   Time: {response.elapsed.total_seconds():.2f}s")
    assert response.status_code == 200, f"Login failed: {response.status_code}"

    # 2. Response Headers
    print("\n2. Response Headers:")
    print("   Content-Type: {response.headers.get('Content-Type')}")
    assert 'application/json' in response.headers.get('Content-Type', '')

    # 3. Response Body
    print("\n3. Response Body:")
    data = response.json()
    print(f"   Keys: {list(data.keys())}")
    assert 'token' in data, "No token in response"

    # 4. Token
    print("\n4. Token:")
    print(f"   Length: {len(token)}")
    print(f"   Preview: {token[:30]}...")
    assert token is not None
    assert len(token) > 0

    # 5. Session Headers
    print("\n5. Session Headers:")
    print(f"   Authorization: {session.headers['Authorization'][:50]}...")
    print(f"   Content-Type: {session.headers['Content-Type']}")
    assert 'Authorization' in session.headers
    assert f'Bearer {token}' == session.headers['Authorization']

    print("\n✓ All checks passed")
    return None


def test_fetch_candidates():
    """
    Test gives you a list of dicts
    """
    response = fetch_candidates()
    assert response.status_code == 200
    candidates = response.json()
    print(f'Candidate object is {candidates}')
 
def test_get_candidates():
    """
    Test
    """

    extracted_candidates = get_candidates()
    assert extracted_candidates is not None
    assert len(extracted_candidates) > 0
    print(type(extracted_candidates))
    print(f' TOTAL Accessed Candidates: {len(extracted_candidates)}')
    print(extracted_candidates[0])
    print(extracted_candidates[-1])

def test_post_diagnosis():
    """
    Test connection to CBIGR diagnosis endpoint
    """
    global _SESSION, _TOKEN 

    _SESSION, _TOKEN, _ = authenticate()

    print(f"Session headers: {_SESSION.headers}")
    print(f"Token: {_TOKEN}")
    print(f"URL: {Config.CBIGR_DIAGNOSIS_URL}")
    

    # Test data
    test_diagnosis = {
        'PSCID': 'Q1K0001076',
        'Diagnosis': 'Ataxia',
        'Familial': None,
        'Comment': 'Test comment'
    }

    response = _SESSION.post(
        Config.CBIGR_DIAGNOSIS_URL,
        json=test_diagnosis,
        headers=_SESSION.headers,
        timeout=10
        )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    return None

if __name__ == "__main__":
    test_authenticate()
    test_fetch_candidates()
    test_get_candidates()
    test_post_diagnosis()