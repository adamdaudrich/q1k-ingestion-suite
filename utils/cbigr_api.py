"""
Get authentication token once
"""
import requests
from utils.config import Config


_SESSION = None
_TOKEN = None

def authenticate():
    """
    Authenticate the session
    """
    global _SESSION, _TOKEN

    credentials = {
        'username': Config.CBIGR_USERNAME,
        'password': Config.CBIGR_PASSWORD
    }

    _SESSION = requests.Session()
    auth_response = _SESSION.post(
        Config.CBIGR_LOGIN_URL,
        json=credentials,
        timeout=30
    )

    auth_response.raise_for_status()  # Raise if 4xx/5xx

    _TOKEN = auth_response.json().get('token')

    if not _TOKEN:
        raise ValueError("No token in response")

    # Set headers for future requests
    _SESSION.headers.update({
        'Authorization': f'Bearer {_TOKEN}',
        'Content-Type': 'application/json'
    })

    return _SESSION, _TOKEN, auth_response

def fetch_candidates():
    """
    Fetch candidates using authenticated session
    """

    if not _SESSION or not _TOKEN:
        authenticate()

    response = _SESSION.get(
        f"{Config.CBIGR_CANDIDATES_URL}",
        timeout=30
    )

    response.raise_for_status()
    return response

def get_candidates():
    """
    Get the candidate list and extract data from each candidate dict
    Returns a list of candidate dictionaries with extracted fields
    """
    # Get the response object
    response = fetch_candidates()
    
    # Get the actual list from the 'Candidates' key
    candidate_list = response.json()['Candidates']
    
    extracted_candidates = []
    
    for c in candidate_list:
        candid = c.get('CandID')
        project = c.get('Project')
        project_id = c.get('ProjectID')
        pscid = c.get('PSCID')
        site = c.get('Site')
        edc = c.get('EDC')
        dob = c.get('DoB')
        sex = c.get('Sex')

        # Handle nested ExtStudyIDs safely
        ext_study_ids = c.get('ExtStudyIDs') or {}
        extid = ext_study_ids.get('Q1K')

        session_ids = c.get('SessionIDs')
     
        # Store in a dict to return
        candidate_data = {
            'CandID': candid,
            'Project': project,
            'ProjectID': project_id,
            'PSCID': pscid,
            'Site': site,
            'EDC': edc,
            'DoB': dob,
            'Sex': sex,
            'ExtStudyID_Q1K': extid,
            'SessionIDs': session_ids
        }
        
        extracted_candidates.append(candidate_data)
    
    return extracted_candidates


def extract_pscid_extid():
    """
    Make a dict with PSCID and ExtStudyID
    Returns: dict
    """

    candidates = fetch_candidates()
    candidates_data = candidates.json()
    
    pscid_extid = []

    for i in candidates_data['Candidates']:
            pscid = i['PSCID']
            ext_study_ids = i['ExtStudyIDs']

            if ext_study_ids is not None or '':
                record = {
                    'pscid': pscid, 
                    'extid': ext_study_ids['Q1K']
                }
                pscid_extid.append(record)

    return pscid_extid



# def delete_diagnosis(pscid, diagnosis_name):
#     """DELETE a diagnosis"""
#     global _session
    
#     try:
#         payload = {'PSCID': pscid, 'Diagnosis': diagnosis_name}
#         response = _session.delete(
#             Config.CBIGR_DIAGNOSIS_URL,
#             json=payload,
#             headers=_get_headers(),
#             timeout=10
#         )
        
#         if response.status_code == 200:
#             print(f"✓ Deleted {diagnosis_name} for {pscid}")
#             return True
#         else:
#             print(f"✗ Failed: {response.status_code}")
#             return False
#     except Exception as e:
#         print(f"✗ Error: {e}")
#         return False


    
#     except Exception as e:
#         print(f"✗ Error: {e}")
#         return False