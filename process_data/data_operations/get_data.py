"""
Created on Apr 7, 2023

@author: Alex
"""
import json
from collections import defaultdict
from pathlib import Path

import pandas

from process_data.datatypes.recorded_ignores import RecordedIgnores
from process_data.datatypes.recorded_states import RecordedDupes


def get_existing_states(
    dupe_path: Path, ignore_path: Path, skip_updates: bool
) -> tuple[RecordedDupes, RecordedIgnores]:
    """Attempt to retrieve existing RecordedDupes, returning empty on failure"""
    try:
        with dupe_path.open("r", encoding="utf8") as dupe_file:
            dupes = RecordedDupes.from_data(json.load(dupe_file), skip_updates)
        with ignore_path.open("r", encoding="utf8") as ignore_file:
            ignores = RecordedIgnores.from_data(json.load(ignore_file))
        return dupes, ignores
    except IOError:
        return RecordedDupes(dupes=defaultdict(set)), RecordedIgnores(
            ignored_dupes=defaultdict(set)
        )


def get_dataframe(filepath: Path) -> pandas.DataFrame:
    """Create a Pandas DataFrame of the data in the target CSV"""
    return pandas.read_csv(filepath, keep_default_na=False)


def get_unique_items(data: pandas.DataFrame, item_col: str = "Organization") -> frozenset[str]:
    """Get every unique item in data"""
    return frozenset(data[item_col])
