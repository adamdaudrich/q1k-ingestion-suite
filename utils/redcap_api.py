"""
Functions for fetching data from the REDCap API.
"""

import requests
from utils.config import Config

REDCAP_TOKEN = Config.REDCAP_TOKEN
REDCAP_URL = Config.REDCAP_URL

def fetch_identifiers():
    """
    Extract the REDcap record_ids and the additional id fields
    'record_id', 'q1k_proband_id_1' and 'q1k_relative_idgenerated_1'
    Returns: 
    """

    redcap_ids_fetch = {
    'token': REDCAP_TOKEN,
    'content': 'record',
    'action': 'export',
    'format': 'json',
    'type': 'flat',
    'rawOrLabel': 'raw',
    'rawOrLabelHeaders': 'raw',
    'exportCheckboxLabel': 'false',
    'exportSurveyFields': 'false',
    'exportDataAccessGroups': 'false',
    'returnFormat': 'json',
    'events[0]' : 'intake_arm_1',
    'fields[0]' : 'record_id',
    'fields[1]' : 'q1k_proband_id_1',
    'fields[2]' : 'q1k_relative_idgenerated_1'}

    redcap_ids_resp = requests.post(REDCAP_URL, data = redcap_ids_fetch, timeout = 10)
    redcap_ids_data = redcap_ids_resp.json()

    redcap_ids = []
    for j in redcap_ids_data:
        record = {
            'record_id': j['record_id'],
            'q1k_proband_id_1': j['q1k_proband_id_1'].replace('_', '-').strip(),
            'q1k_relative_idgenerated_1': j['q1k_relative_idgenerated_1'].replace('_', '-').strip(),
        }
        redcap_ids.append(record)

    return redcap_ids

def get_study_id(record):
    """
    Extract, merge and format the study ID from REDcap required by CBIGR new_profile
    """
    proband_id = record.get('q1k_proband_id_1', '')
    relative_id = record.get('q1k_relative_idgenerated_1', '')
    merged_id = proband_id or relative_id or ''

    return merged_id.replace('_', '-')

def get_record_id_external_id():
    """
    Extract record_id and study_id from fetch_identifiers
    Return: dict
    """

    identifiers = fetch_identifiers()

    recordid_extid = {}
    for i in identifiers:
        record_id = i.get('record_id', '')
        ext_id = get_study_id(i) 
        recordid_extid[record_id] = ext_id

    return recordid_extid    

def fetch_registration():
    """Fetch registration data from REDCap API"""
    params = {
        'token': REDCAP_TOKEN,
        'content': 'record',
        'action': 'export',
        'format': 'json',
        'type': 'flat',
        'rawOrLabel': 'raw',
        'rawOrLabelHeaders': 'raw',
        'exportCheckboxLabel': 'false',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': 'json',
        'events[0]' : 'intake_arm_1',
        'fields[0]' : 'enr2_pro_prob_fname',
        'fields[1]' : 'enr2_pro_prob_lname',
        'fields[2]' : 'enr2_pro_dob',
        'fields[3]' : 'enr2_pro_sex',
        'fields[4]' : 'q1k_sitechoice_1',
        'fields[5]' : 'enr2_pro_dob_city',
        'fields[6]' : 'enr2_pro_dob_country',
        'fields[7]' : 'record_id', 
        'fields[8]' : 'q1k_proband_id_1',
        'fields[9]' : 'q1k_relative_idgenerated_1',
        'fields[10]': 'icf_form_phase_2_complete'
    }

    response = requests.post(REDCAP_URL, data=params, timeout=10)
    response.raise_for_status()
    return response.json()

def fetch_consents():
    """Fetch phase 2 consent data from REDCap API"""
    params = {
        'token': REDCAP_TOKEN,
        'content': 'record',
        'action': 'export',
        'format': 'json',
        'type': 'flat',
        'rawOrLabel': 'raw',
        'rawOrLabelHeaders': 'LabelHeaders',
        'exportCheckboxLabel': 'true',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': 'json',
        'events[0]': 'intake_arm_1',
        'fields[0]': 'record_id',
        'fields[1]': 'q1k_proband_id_1',
        'fields[2]': 'q1k_relative_idgenerated_1',
        'fields[3]': 'icf_form_phase_2_complete',
        'fields[4]': 'date_persstudy_p2'
    }
    
    response = requests.post(REDCAP_URL, data=params, timeout=10)
    response.raise_for_status()  # Raise exception for bad status codes
    return response.json()

def fetch_diagnosis():
    """Fetch diagnosis data from REDCap API"""
    params = {
        'token': REDCAP_TOKEN,
        'content': 'record',
        'action': 'export',
        'format': 'json',
        'type': 'flat',
        'rawOrLabel': 'raw',
        'rawOrLabelHeaders': 'LabelHeaders',
        'exportCheckboxLabel': 'true',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': 'json',
        'events[0]': 'intake_arm_1',
        'fields[0]': 'record_id',
        'fields[1]': 'q1k_proband_id_1',
        'fields[2]': 'q1k_relative_idgenerated_1',
        'fields[3]': 'reg_diag_asd',
        'fields[4]': 'reg_diag_intel',
        'fields[5]': 'reg_diag_adhd',
        'fields[6]': 'reg_diag_fas',
        'fields[7]': 'reg_diag_learn',
        'fields[8]': 'reg_diag_comm',
        'fields[9]': 'reg_diag_motor',
        'fields[10]': 'reg_diag_hearing',
        'fields[11]': 'reg_diag_visual',
        'fields[12]': 'reg_diag_phys',
        'fields[13]': 'reg_diag_gene',
        'fields[14]': 'diag_oth',     
    }

    response = requests.post(REDCAP_URL, data=params, timeout=10)
    response.raise_for_status()
    return response.json()

def fetch_family_relationship():
    """Fetch the Family relationship"""
    params = {
        'token': REDCAP_TOKEN,
        'content': 'record',
        'action': 'export',
        'format': 'json',
        'type': 'flat',
        'rawOrLabel': 'raw',
        'rawOrLabelHeaders': 'raw',
        'exportCheckboxLabel': 'false',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': 'json',
        'events[0]' : 'intake_arm_1',
        'fields[0]' : 'record_id', 
        'fields[1]' : 'q1k_proband_id_1',
        'fields[2]' : 'q1k_relative_idgenerated_1',
        'fields[3]' : 'enr2_pro_rel_prob_2',
        'fields[4]' : 'q1k_rel_proband_id'
    }

    response = requests.post(REDCAP_URL, data=params, timeout=10)
    response.raise_for_status()
    return response.json()

def fetch_session():
    """ 
    Fetch site, ev_status, and ids of the participant
    """
    params = {
        'token': REDCAP_TOKEN,
        'content': 'record',
        'action': 'export',
        'format': 'json',
        'type': 'flat',
        'rawOrLabel': 'raw',
        'rawOrLabelHeaders': 'raw',
        'exportCheckboxLabel': 'false',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': 'json',
        'events[0]' : 'intake_arm_1',
        'fields[0]' : 'record_id', 
        'fields[1]' : 'q1k_proband_id_1',
        'fields[2]' : 'q1k_relative_idgenerated_1',
        'fields[3]' : 'ev_status',
        'fields[4]' : 'q1k_proband_yn_1',
        'fields[5]' : 'q1k_adminsite_1'
    }

    response = requests.post(REDCAP_URL, data=params, timeout=10)
    response.raise_for_status()
    return response.json()

def get_sessions():
    """
    get cohorts and sites for all candidates for eventual
    q1k_proband_yn 1= yes 0= no
    ev_status 1=affected 2 = not affected
    db session inserts
    """

    session_data = fetch_session()

    sessions = {}
    for s in session_data:
        record_id = s.get("record_id")
        cohort_value = s.get("ev_status")
        proband_value = s.get("q1k_proband_yn")
    

        # if proband = 1 (YES), then this candidate is affected
        if cohort_value == '1':
            cohort = 'Affected'
        elif cohort_value == "2":
            cohort = 'Not Affected'

        # set the proband to Affected
        elif cohort_value == "" and proband_value == '1':
            cohort = "Affected"
        
        else:
            cohort = 'Unknown'

        site_value = s.get("q1k_adminsite_1")
        if site_value == '1':
            #HSJ
            site = "Centre Hospitalier Universitaire Sainte-Justine"
        elif site_value == '2':
            #MHC
            site = "Montreal Neurological Institute"
        elif site_value == '3':
            #NIM
            site = "Hôpital Rivière-des-Prairies"
        elif site_value == '4':
            # OIM
            site = "Douglas Mental Health Institute"
        elif site_value == '5':
            # SHR
            site = "Centre Hospitalier Universitaire de Sherbrooke"
        elif site_value == '6':
            # GAT
            site = "Children's Hospital of Eastern Ontario"
        
        sessions[record_id] = {
            "cohort": cohort, 
            "site": site
        } 

    return sessions