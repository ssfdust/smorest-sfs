#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

NAME_PATTERN = re.compile(r"(.)([A-Z][a-z]+)")
RESULT_PATTERN = re.compile(r"([a-z0-9])([A-Z])")


def camel_to_snake(name: str) -> str:
    name = NAME_PATTERN.sub(r"\1_\2", name)
    return RESULT_PATTERN.sub(r"\1_\2", name).lower()
