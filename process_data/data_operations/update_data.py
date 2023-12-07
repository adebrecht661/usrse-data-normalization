"""
Created on Apr 7, 2023

@author: Alex
"""
from typing import (
    AbstractSet,
    Mapping,
)

import pandas

from process_data.data.filepaths import OUTPUT_DF_FILEPATH


def update_data(
    data: pandas.DataFrame,
    items_to_replace: Mapping[str, AbstractSet[str]],
    item_col: str = "Organization",
) -> pandas.DataFrame:
    """
    Update the dataframe with the recorded changes

    Also saves dataframe
    """

    new_data = data.copy()

    # This makes lookups easier
    inverted_replacements = {v: key for key, val in items_to_replace.items() for v in val}

    for old_item, new_item in inverted_replacements.items():
        new_data.loc[new_data[item_col] == old_item, item_col] = new_item

    new_data.to_csv(OUTPUT_DF_FILEPATH)

    return new_data
