"""
Configuration loader for API credentials
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration from environment variables."""
    
    #cbigr api
    CBIGR_USERNAME = os.getenv('CBIGR_USERNAME') 
    CBIGR_PASSWORD = os.getenv('CBIGR_PASSWORD')
    CBIGR_LOGIN_URL = os.getenv('CBIGR_LOGIN_URL')
    CBIGR_DIAGNOSIS_URL = os.getenv('CBIGR_DIAGNOSIS_URL')
    CBIGR_CANDIDATES_URL = os.getenv('CBIGR_CANDIDATES_URL')
    CBIGR_LOGIN_URL = os.getenv('CBIGR_LOGIN_URL')
    
    #redcap api
    REDCAP_TOKEN = os.getenv('REDCAP_TOKEN')
    REDCAP_URL = os.getenv('REDCAP_URL')

    #bids
    TEST_BIDS = os.getenv('TEST_BIDS') 
    MERGED_BIDS = os.getenv('MERGED_BIDS')
    RENAMED_BIDS = os.getenv('RENAMED_BIDS')