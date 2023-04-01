"""
Personal (nooby) implementation of `pprint`.
"""
from __future__ import annotations

import json
from typing import Any


class MyEncoder(json.JSONEncoder):
    """Encoder to serialise objects to JSON that aren't supported by JSON."""

    def default(self, obj: Any) -> str:
        """Return the repr of the object."""
        return repr(obj)


def pprint(json_text: str | dict, indent: int = 4, verbose: bool = False) -> None:
    """Pretty print JSON/dict objects."""
    if isinstance(json_text, str):
        json_text = json.loads(json_text)

    try:
        print(
            json.dumps(
                json_text,
                sort_keys=True,
                indent=indent,
                separators=(',', ': '),
                cls=MyEncoder,
            )
        )
    except TypeError as e:
        print(repr(e)) if verbose else None
        print(json_text)
