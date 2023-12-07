"""
Created on Dec 7, 2023

@author: alex
"""
import json
from pathlib import Path

import pandas

from process_data.data.filepaths import INPUT_ROR_FILEPATH

ROR_DATA_PATH: Path = Path(__file__).parent / "v1.38-2023-12-07-ror-data.json"


def main() -> None:
    with ROR_DATA_PATH.open(encoding="utf8") as ror_data_file:
        ror_data = json.load(ror_data_file)

    data: dict[str, list[str]] = {"org_id": [], "org_name": []}
    for org in ror_data:
        data["org_id"].append(org["id"])
        data["org_name"].append(org["name"])

    pandas.DataFrame(data).to_csv(INPUT_ROR_FILEPATH)


if __name__ == "__main__":
    main()
