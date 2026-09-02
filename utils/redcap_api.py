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
    'fields[2]' : 'q1k_relative_idgenerated_1'
    }

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
        'fields[3]': 'cfq_diag_asd',
        'fields[4]': 'cfq_diag_id',
        'fields[5]': 'cfq_diag_adhd',
        'fields[6]': 'cfq_diag_fasd',
        'fields[7]': 'cfq_diag_ld',
        'fields[8]': 'cfq_diag_lcd',
        'fields[9]': 'cfq_diag_md',
        'fields[10]': 'cfq_diag_other',
        'fields[11]': 'cfq_ment_ad',
        'fields[12]': 'cfq_ment_dd',
        'fields[13]': 'cfq_ment_bd',
        'fields[14]': 'cfq_ment_ocd',
        'fields[15]': 'cfq_ment_ts',
        'fields[16]': 'cfq_ment_psyep',
        'fields[17]': 'cfq_ment_schizo',
        'fields[18]': 'cfq_ment_sa',
        'fields[19]': 'cfq_ment_epilepsy',
        'fields[20]': 'cfq_ment_hearing_disability',
        'fields[21]': 'cfq_ment_visual_disability',
        'fields[22]': 'cfq_ment_physical_disability',
        'fields[23]': 'cfq_ment_genetic_disorder'  
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

def fetch_sessions():
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



def fetch_bulk_p2():
    """
    Fetch phase 2 fields from REDCap API
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
        'fields[1]' : 'enr2_pro_sex',
        'fields[2]' : 'q1k_sitechoice_1',
        'fields[3]' : 'ev_status',
        'fields[4]' : 'record_id', 
        'fields[5]' : 'q1k_proband_id_1',
        'fields[6]' : 'q1k_relative_idgenerated_1'
    }

    response = requests.post(REDCAP_URL, data=params, timeout=10)
    response.raise_for_status()
    return response.json()

def fetch_bulk_p3():
    """
    fetch phase 3 fields from REDCAP API
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
        'events[0]' : 'phase_3_arm_1',
        'fields[1]' : 'mri_acquisition_checklist_complete',
        'fields[2]' : 'eeg_sex_birth',
        'fields[3]' : 'eeg_participant_handedness',
        'fields[4]' : 'icf_form_phase_3_complete',
        'fields[5]' : 'record_id',
        'fields[6]' : 'eeget_session_log_complete'
    }

    response = requests.post(REDCAP_URL, data=params, timeout=10)
    response.raise_for_status()
    return response.json()


def fetch_date_taken():
    """
    fetch the test date for each instrument

    abasiii_05 : abas0_5_today
    abasiii_521 : abas5_21_today
    abasiii_1889 : abas18_89_today
    ados_module_toddler : ados_module_toddler_def_text
    ados_module_1 : ados_module_1_def_text
    ados_module_2 : ados_module_2_def_text
    ados_module_3 : ados_module_3_def_text
    ados_module_4 : ados_mod4_today_day
    aseba_abcl_1859 : aseba_abcl_date
    aseba_asr_1859 : asr18_59_todaydate
    aseba_cbcl_155 : cbcl_pre_date
    aseba_cbcl_618 : aseba_cbcl_date
    aseba_oabcl_6090 : aseba_cbc?????
    aseba_oasr_6090 : oasr60_90_date
    bayley4 : bailey_testdate
    developmental_history_questionnaire :
    eeget_session_log : eeg_et_today_date
    evt3: evt3_date
    family_background_questionnaire : 
    general_health_form : ghf_date
    general_health_form_generic_testing_cnv_1 : gt_cnv_reviewer_date
    general_health_form_generic_testing_cnv_2
    general_health_form_generic_testing_cnv_3
    general_health_form_generic_testing_csv_4
    general_health_form_generic_testing_csv_5
    general_health_form_generic_testing_snv_1
    general_health_form_generic_testing_snv_2
    general_health_form_generic_testing_snv_3
    general_health_form_height_weight_head
    general_health_form_medication_and_treatements_1 : ghf_med_reviewer_date
    general_health_form_medication_and_treatements_2
    general_health_form_medication_and_treatements_3
    general_health_form_medication_and_treatements_4
    general_health_form_medication_and_treatements_5
    general_health_form_medication_and_treatements_6
    general_health_form_medication_and_treatements_7
    general_health_form_medication_and_treatements_8
    general_health_form_medication_and_treatements_9
    general_health_form_medication_and_treatements_10
    general_health_form_medication_and_treatements_11
    general_health_form_medication_and_treatements_12
    general_health_form_medication_and_treatements_13
    general_health_form_medication_and_treatements_14
    general_health_form_medication_and_treatements_15
    general_health_form_medication_and_treatements_16
    general_health_form_medication_and_treatements_17
    introduction_to_questionnaires
    leiter3_sum : leiter_3_date
    mri_aqcuisition_checklist :
    mri_safety_questionnaire
    parents_siblings_and_children_in_family_quest
    ppvt5 : ppvt5_date
    sample_tracking : track_date
    scq_418 : scq_date
    srs_adult_other_relative_19 : srs_older_today
    srs_adult_selfreport_19_phase_2 :  or srs_asr_today_p2
    srs_preschool : srs_prescho_today
    srs_preschool_2545 :
    srs_school_age_418 : srs4_18_today
    waiscv_scoring : wais_date
    wiscv scoring: wisc_date
    wppsiiv_record_form_ages_23 : wippsi23_test_date
    wppsiiv_record_form_ages_47 : wppsi_47_date 
    """