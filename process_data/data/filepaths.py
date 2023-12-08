"""
Created on Apr 7, 2023

@author: Alex
"""
from pathlib import Path

DUPE_RECORD_FILEPATH: Path = Path(__file__).parent / "resolved_duplicates.json"
IGNORED_RECORD_FILEPATH: Path = Path(__file__).parent / "ignored_duplicates.json"
INPUT_DF_FILEPATH: Path = Path(__file__).parent / "usrse-orgs.csv"
OUTPUT_DF_FILEPATH: Path = Path(__file__).parent / "cleaned_organizations.csv"
INPUT_ROR_FILEPATH: Path = Path(__file__).parent / "ror_data.json"
ROR_NOT_FOUND_FILEPATH: Path = Path(__file__).parent / "ror_not_found.json"
