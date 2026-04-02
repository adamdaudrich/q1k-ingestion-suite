"""
Configuration loader for API credentials
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration from environment variables."""
    
    CBIGR_USERNAME = os.getenv('CBIGR_USERNAME') 
    CBIGR_PASSWORD = os.getenv('CBIGR_PASSWORD')
    CBIGR_LOGIN_URL = os.getenv('CBIGR_LOGIN_URL')
    CBIGR_DIAGNOSIS_URL = os.getenv('CBIGR_DIAGNOSIS_URL')
    CBIGR_CANDIDATES_URL = os.getenv('CBIGR_CANDIDATES_URL')
    CBIGR_LOGIN_URL = os.getenv('CBIGR_LOGIN_URL')
    REDCAP_TOKEN = os.getenv('REDCAP_TOKEN')
    REDCAP_URL = os.getenv('REDCAP_URL')
    SOURCE_DIR = '/data/q1k/data/CBIG'

    # BIDS
    KC_BIDS = 'REDACTED'
    HEATHER_BIDS = 'REDACTED'
    MERGED_BIDS = 'REDACTED'
    RENAMED_BIDS = 'REDACTED'