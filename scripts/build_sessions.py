"""
This file extracts the cohort and site values
needed for batch session renaming in CBIGR
"""
from datetime import datetime
import csv
from pathlib import Path
from utils.redcap_api import get_study_id, fetch_session   

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
        q1k_id = get_study_id(s)
        cohort_value = s.get("ev_status")
    

        # if proband = 1 (YES), then this candidate is affected
        if cohort_value == '1':
            cohort = 'Affected'
        elif cohort_value == "2":
            cohort = 'Not Affected'

        # set the proband to Affected
        elif cohort_value == "" :
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
        
        sessions[q1k_id] = {
            "Cohort": cohort, 
            "Site": site
        } 

    return sessions


def get_output_path():
    """
    Get the output CSV path and ensure directory exists
    """
    # Define output directory relative to script
    script_dir = Path(__file__).parent
    output_dir = script_dir / 'csv'

    # Create directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d')
    base_name = 'q1k_sessions'
    filename = f'{base_name}_{timestamp}.csv'

    # Return the full file path
    return output_dir / filename


def write_sessions_csv(sessions):
    """
    Write consent data to CSV
    """

    csv_path = get_output_path()

    fieldnames = ['LorisID', 'Cohort', 'Site']

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        rows = [{"LorisID": q1k_id, **data} for q1k_id, data in sessions.items()]
        writer.writerows(rows)

    print(f"✅ CSV written to: {csv_path}")


def main():
    """Orchestrate the consent data extraction pipeline"""

    sessions = get_sessions()

    write_sessions_csv(sessions)

if __name__ == "__main__":
    main()