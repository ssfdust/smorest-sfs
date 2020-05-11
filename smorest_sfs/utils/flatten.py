#!/usr/bin/env python
# -*- coding: utf-8 -*-
from operator import itemgetter
from typing import Any, Callable, Iterator, List


def flatten_nested_tree(
    nodes: List[Any], node_dump: Callable[[Any], Any] = itemgetter("label")
) -> Iterator[Any]:
    stack = list(reversed(nodes))
    while stack:
        node = stack.pop()
        yield node_dump(node)
        if "children" in node:
            stack += list(reversed(node["children"]))
