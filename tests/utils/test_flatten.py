#!/usr/bin/env python
# -*- coding: utf-8 -*-
import string
from operator import itemgetter
from typing import Any, Set

import pytest

from smorest_sfs.utils.flatten import flatten_nested_tree

TEST_DATA = [
    {"name": "a", "age": 1},
    {
        "name": "b",
        "age": 1,
        "children": [
            {"name": "d", "age": 5},
            {"name": "e", "age": 5},
            {
                "name": "f",
                "age": 5,
                "children": [
                    {"name": "g", "age": 12},
                    {"name": "h", "age": 12},
                    {"name": "i", "age": 12},
                    {"name": "j", "age": 12},
                ],
            },
        ],
    },
    {"name": "c", "age": 1},
]


@pytest.mark.parametrize(
    "key, res", [("name", set(string.ascii_lowercase[0:10])), ("age", {1, 5, 12})]
)
def test_flatten_nested_tree_to_values(key: str, res: Set[Any]) -> None:
    assert set(flatten_nested_tree(TEST_DATA, itemgetter(key))) == res


def test_flatten_nested_tree_to_dict() -> None:
    mapping = {1: ["a", "b", "c"], 5: ["d", "e", "f"], 12: ["g", "h", "i", "j"]}
    for value in flatten_nested_tree(
        TEST_DATA, lambda x: {"name": x["name"], "age": x["age"]}
    ):
        lst = mapping[value["age"]]
        assert value["name"] in lst
