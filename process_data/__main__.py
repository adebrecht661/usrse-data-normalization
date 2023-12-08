"""
Created on Apr 7, 2023

@author: Alex
"""
import argparse
import json

import pandas

from process_data.data.filepaths import (
    DUPE_RECORD_FILEPATH,
    IGNORED_RECORD_FILEPATH,
    INPUT_DF_FILEPATH,
)
from process_data.data_operations.get_data import (
    get_dataframe,
    get_existing_states,
    get_unique_items,
)
from process_data.data_operations.update_data import update_data
from process_data.datatypes.recorded_ignores import RecordedIgnores
from process_data.datatypes.recorded_states import RecordedDupes
from process_data.match_items.get_matches import update_duplicates


def normalize_items(
    data: pandas.DataFrame,
    match_score: int,
    rescan_non_dupes: bool,
    recorded_dupes: RecordedDupes,
    recorded_ignores: RecordedIgnores,
    skip_ror: bool,
    rematch_ror: bool,
) -> pandas.DataFrame:
    """Normalize items"""

    unique_items = get_unique_items(data)

    print(f"Starting with {len(unique_items)} unique items.")

    print(
        "Processing possible misspellings."
        + " You may hit ctrl+C at any point to exit, or enter `e` at the prompt."
        + " Progress will be saved."
    )
    print()

    update_duplicates(
        unique_items,
        match_score,
        rescan_non_dupes,
        recorded_dupes,
        recorded_ignores,
    )

    with DUPE_RECORD_FILEPATH.open("w", encoding="utf8") as dupe_file:
        json.dump(recorded_dupes.to_data(), dupe_file, indent=2)

    print("Updating data.")
    data = update_data(data, recorded_dupes, recorded_ignores, match_score, skip_ror, rematch_ror)
    print("Data updated.")

    return data


def print_statistics(data: pandas.DataFrame) -> None:
    """Collect statistics on normalized items"""

    print(
        data.reset_index()
        .groupby(["Organization", "ROR ID"], dropna=False)
        .count()
        .sort_values("index", ascending=False)
    )


def main(args: argparse.Namespace) -> None:
    """Process data"""

    data = get_dataframe(INPUT_DF_FILEPATH)

    print("Loading data.")
    recorded_duplicates, recorded_ignores = get_existing_states(
        DUPE_RECORD_FILEPATH, IGNORED_RECORD_FILEPATH, args.skip_updates
    )

    if args.skip_updates is False:
        updated_data = normalize_items(
            data,
            args.match_score,
            args.rescan_keys,
            recorded_duplicates,
            recorded_ignores,
            args.skip_match_for_ror,
            args.rematch_for_ror,
        )

    print("Collecting statistics.")
    print_statistics(updated_data)


def cli() -> argparse.Namespace:
    """Define command-line interface for this program"""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--match-score",
        type=int,
        default=90,
        help="""
        The minimum score to allow for a match. Fairly sensitive.
        Default = 90
        """,
    )

    parser.add_argument(
        "--rescan-keys",
        action="store_true",
        help="""
        Pass this to check for duplicates that were previously not matched.
        Best paired with a lower `match-score` than the default.
        """,
    )

    parser.add_argument(
        "--skip-updates",
        action="store_true",
        help="""
        Use the existing resolved duplicates, don't attempt to find new duplicates 
        """,
    )

    parser.add_argument(
        "--skip-match-for-ror",
        action="store_true",
        help="""
        Skip attempting to find the correct key for the ROR data if it's not found. 
        """,
    )

    parser.add_argument(
        "--rematch-for-ror",
        action="store_true",
        help="""
        Attempt to match ROR data even if a match was previously not found. 
        """,
    )

    return parser.parse_args()


if __name__ == "__main__":
    main(cli())
