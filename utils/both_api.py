"""
Both API
"""

from utils.cbigr_api import get_candidates
from utils.redcap_api import fetch_identifiers, get_study_id, fetch_diagnosis

def get_cbigr_redcap_matches():
    """
    Match CBIGR candidates with REDCap records
    Returns: list of dicts
    """
    extracted_candidates = get_candidates()
    redcap_ids = fetch_identifiers()

    matches = []
    unmatched = []
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

            else:
                unmatched.append(r)

    return matches, unmatched

def get_cand_id_record_id():
    """
    Get record_id and merged_id
    """
    records = fetch_identifiers()
    extracted_candidates = get_candidates()

    cand_id_record_id = []

    for r in records:
        record_id = r.get('record_id')
        merged_id = get_study_id(r)

        for c in extracted_candidates:
            candid = c.get('CandID')
            extid = c.get('ExtStudyID_Q1K')
            if extid is not None and not '' and extid == merged_id:
                cand_id_record_id.append({
                    'CandID' : candid,
                    'record_id': record_id
                })

    return cand_id_record_id

def get_diagnosis():
    """
    Extract diagnoses where value is '1' (Yes)
    Returns: dict
    """
    records = fetch_diagnosis()
    extracted_candidates = get_candidates()

    diagnosis_mapping = {
        'Autism Spectrum Disorder': 'reg_diag_asd',
        'Intellectual Disability': 'reg_diag_intel',
        'Attention Deficit Hyperactivity Disorder': 'reg_diag_adhd',
        'Fetal Alcohol Syndrome Disorder': 'reg_diag_fas',
        'Learning Disability': 'reg_diag_learn',
        'Language and Communication Disorder': 'reg_diag_comm',
        'Motor Disorder': 'reg_diag_motor',
        'Hearing Disability': 'reg_diag_hearing'
        'Visual Disability': 'diag_visual',
        'Physical Disability': 'reg_diag_phys',
        'Genetic Disorder': 'reg_diag_gene',
        'Other': 'reg_diag_oth'
    }

    diagnoses = []

    for r in records:
        merged_id = get_study_id(r)

        for c in extracted_candidates:
            pscid = c.get('PSCID')
            if c['ExtStudyID_Q1K'] == merged_id:

                for name, field in diagnosis_mapping.items():
                    if r.get(field) == '1':
                        diagnoses.append({
                            'PSCID': pscid,
                            'Diagnosis': name,
                            'Familial': None,  
                            'Comment': 'Suspected Diagnosis'    
                        })

                    elif r.get(field) == '2':
                        diagnoses.append({
                            'PSCID': pscid,
                            'Diagnosis': name,
                            'Familial': None,
                            'Comment' : 'Confirmed Diagnosis'
                        })
                break
            
    return diagnoses
