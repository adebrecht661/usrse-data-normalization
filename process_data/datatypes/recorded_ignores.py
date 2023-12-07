"""
Created on Apr 22, 2023

@author: Alex
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import (
    dataclass,
    fields,
)
from typing import Any

from process_data.datatypes.utils import to_data


@dataclass(frozen=True)
class RecordedIgnores:
    """Duplicates that were ignored in the past"""

    ignored_dupes: defaultdict[str, set[str]]

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> RecordedIgnores:
        """Reconstruct from JSON data"""
        return cls(
            ignored_dupes=defaultdict(
                set,
                {str(key): {str(v) for v in val} for key, val in data["ignored_dupes"].items()},
            ),
        )

    def to_data(self) -> dict[str, Any]:
        """Write to JSON data"""
        out = {}
        for key, val in {field.name: getattr(self, field.name) for field in fields(self)}.items():
            out[key] = to_data(val)
        return out
