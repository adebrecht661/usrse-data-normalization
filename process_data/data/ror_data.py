"""
Created on Dec 7, 2023

@author: alex
"""
import json
from typing import Mapping

from process_data.data.filepaths import (
    INPUT_ROR_FILEPATH,
    ROR_NOT_FOUND_FILEPATH,
)
from process_data.datatypes.utils import to_data

with INPUT_ROR_FILEPATH.open(encoding="utf8") as ror_datafile:
    ROR_DATA: Mapping[str, str] = json.load(ror_datafile)


def get_ror_not_found() -> set[str]:
    try:
        with ROR_NOT_FOUND_FILEPATH.open(encoding="utf8") as ror_not_found_file:
            return set(json.load(ror_not_found_file))
    except FileNotFoundError:
        return set()


def write_ror_not_found(ror_not_found: set[str]) -> None:
    with ROR_NOT_FOUND_FILEPATH.open("w", encoding="utf8") as ror_not_found_file:
        json.dump(to_data(ror_not_found), ror_not_found_file)
