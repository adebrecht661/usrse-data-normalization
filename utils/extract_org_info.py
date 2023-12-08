"""
Created on Dec 7, 2023

@author: alex
"""
import json
from pathlib import Path

from process_data.data.filepaths import INPUT_ROR_FILEPATH

ROR_DATA_PATH: Path = Path(__file__).parents[1] / "v1.38-2023-12-07-ror-data.json"


def main() -> None:
    with ROR_DATA_PATH.open(encoding="utf8") as ror_data_file:
        ror_data = json.load(ror_data_file)

    data = {}
    for org in ror_data:
        data[org["name"]] = org["id"]

    with INPUT_ROR_FILEPATH.open("w", encoding="utf8") as ror_dict_file:
        json.dump(dict(sorted(data.items())), ror_dict_file, indent=2)


if __name__ == "__main__":
    main()
