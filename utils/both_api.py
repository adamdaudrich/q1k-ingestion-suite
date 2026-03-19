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
        'Autism Spectrum Disorder': 'cfq_diag_asd',
        'Intellectual Disability': 'cfq_diag_id',
        'Attention Deficit Hyperactivity Disorder': 'cfq_diag_adhd',
        'Fetal Alcohol Syndrome Disorder': 'cfq_diag_fasd',
        'Learning Disability': 'cfq_diag_ld',
        'Language and Communication Disorder': 'cfq_diag_lcd',
        'Motor Disorder': 'cfq_diag_md',
        'Anxiety Disorder': 'cfq_ment_bd',
        'Depression Disorder': 'cfq_ment_ocd',
        'Bipolar Disorder': 'cfq_ment_bd', 
        'Obsessive Compulsive Disorder': 'cfq_ment_ocd', 
        "Tourettes Syndrome": 'cfq_ment_ts',
        'Psychosis Episodes': 'cfq_ment_psyep',
        'Schizophrenia': 'cfq_ment_schizo',
        'Substance Abuse': 'cfq_ment_sa',
        'Epilepsy': 'cfq_ment_epilepsy',
        'Hearing Disability': 'cfq_ment_hearing_disability',
        'Visual Disability': 'cfq_ment_visual_disability',
        'Physical Disability': 'cfq_ment_physical_disability',
        'Genetic Disorder': 'cfq_ment_genetic_disorder'
    }

    diagnoses = []

    for r in records:
        merged_id = get_study_id(r)

        for c in extracted_candidates:
            pscid = c.get('pscid')
            if c['extid'] == merged_id:

                for name, field in diagnosis_mapping.items():
                    if field and r.get(field) == '1':
                        diagnoses.append({
                            'PSCID': pscid,
                            'Diagnosis': name,
                            'Familial': None,  
                            'Comment': None    
                        })
                break
    return diagnoses

