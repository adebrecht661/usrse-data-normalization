"""
Created on Apr 7, 2023

@author: Alex
"""

import pandas

from process_data.data.filepaths import OUTPUT_DF_FILEPATH
from process_data.datatypes.recorded_ignores import RecordedIgnores
from process_data.datatypes.recorded_states import RecordedDupes
from process_data.match_items.get_matches import get_org_id


def update_data(
    data: pandas.DataFrame,
    recorded_dupes: RecordedDupes,
    recorded_ignores: RecordedIgnores,
    match_score: int,
    skip_ror: bool,
    ror_rematch: bool,
    item_col: str = "Organization",
) -> pandas.DataFrame:
    """
    Update the dataframe with the recorded changes

    Also saves dataframe
    """

    new_data = data.copy()

    # Once to match all primary items
    for primary_item in recorded_dupes.dupes.keys():
        get_org_id(
            primary_item, recorded_dupes, recorded_ignores, match_score, skip_ror, ror_rematch
        )

    # This makes lookups easier
    inverted_replacements = {v: key for key, val in recorded_dupes.dupes.items() for v in val}

    for old_item, new_item in inverted_replacements.items():
        new_data.loc[new_data[item_col] == old_item, item_col] = new_item

    for primary_item in recorded_dupes.dupes.keys():
        new_data.loc[new_data[item_col] == primary_item, "ROR ID"] = get_org_id(
            primary_item, recorded_dupes, recorded_ignores, match_score, True, False
        )

    new_data.to_csv(OUTPUT_DF_FILEPATH)

    return new_data
