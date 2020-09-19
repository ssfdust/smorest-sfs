#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Dict, Union, List

ELEMENT = Dict[str, Any]
JSON = Union[List[ELEMENT], ELEMENT]

def parse_dict(data: JSON) -> JSON:
    if isinstance(data, list):
        for element in data:
            parse_dict(element)
    elif isinstance(data, dict):
        if "id" in data:
            data.pop("id")
        if "children" in data:
            parse_dict(data["children"])
    return data


def test_parse_dict() -> None:
    data = [{"id": 1, "name": "a", "children": [{"id": 2, "name": "b", "children": [{"id": 4, "name": "d"}]}]}, {"id": 3, "name": "c"}]
    parse_dict(data)
    assert data == [{"name": "a", "children": [{"name": "b", "children": [{"name": "d"}]}]}, {"name": "c"}]
