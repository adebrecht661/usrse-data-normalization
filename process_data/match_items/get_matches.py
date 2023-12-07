"""
Created on Apr 7, 2023

@author: Alex
"""
import json
import traceback

from process_data.data.filepaths import (
    DUPE_RECORD_FILEPATH,
    IGNORED_RECORD_FILEPATH,
)
from process_data.datatypes.recorded_ignores import RecordedIgnores
from process_data.datatypes.recorded_states import RecordedDupes
from process_data.match_items.process_match import process_new_item


def update_duplicates(
    all_choices: frozenset[str],
    match_score: int,
    rescan_keys: bool,
    known_states: RecordedDupes,
    known_ignores: RecordedIgnores,
) -> None:
    """Determine all possible misspellings for each item"""
    try:
        get_possible_matches(
            all_choices,
            match_score,
            rescan_keys,
            known_states,
            known_ignores,
        )

    except ValueError:
        print("Saving progress and exiting")
    except Exception:  # pylint: disable=broad-exception-caught
        print("Unexpected error :")
        print(traceback.format_exc())
        print("Saving progress and exiting")
    else:
        print("All items scanned!")

    finally:
        with DUPE_RECORD_FILEPATH.open("w", encoding="utf8") as dupe_file:
            json.dump(known_states.to_data(), dupe_file, indent=2)
        with IGNORED_RECORD_FILEPATH.open("w", encoding="utf8") as ignore_file:
            json.dump(known_ignores.to_data(), ignore_file, indent=2)
        print("Updated duplicates saved.")


def get_possible_matches(
    items: frozenset[str],
    match_score: int,
    rescan_keys: bool,
    known_states: RecordedDupes,
    known_ignores: RecordedIgnores,
) -> None:
    """Get possible matches for un-checked items"""
    unscanned_items = set(
        items - (set(known_states.dupes.keys()) | set().union(*(known_states.dupes.values())))
    )
    if rescan_keys is False:
        non_dupe_str = ""
    else:
        best_items = set(known_states.dupes.keys())
        unscanned_items |= best_items
        non_dupe_str = f", of which {len(best_items)} are being rescanned"

    total_to_scan = len(unscanned_items)
    count = 0
    print(f"Scanning {len(unscanned_items)} unscanned items{non_dupe_str}.")
    while len(unscanned_items) > 0:
        count += 1
        print()
        print(f"{count}/{total_to_scan}")
        new_item = unscanned_items.pop()

        process_new_item(
            known_states.dupes,
            known_ignores.ignored_dupes,
            unscanned_items,
            new_item,
            match_score,
        )
