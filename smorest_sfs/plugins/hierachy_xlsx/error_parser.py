#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from typing import Optional


def _parse_mater(match: Optional[re.Match]) -> str:
    if match:
        return match.group(1)
    return ""


def parse_error_sheet(err: KeyError) -> str:
    message = err.args[0]
    match = re.search(r"Worksheet (.*) does not exist.", message)
    return _parse_mater(match)
