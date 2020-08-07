#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Callable

from smorest_sfs.plugins.hierachy_xlsx.parsers import HierachyParser


def get_parsed_reader(
    filename: str, xlsx_path_func: Callable[[str], Path]
) -> HierachyParser:
    xlsx_path = xlsx_path_func(filename)
    with xlsx_path.open("rb") as f:
        reader = HierachyParser(f)
    reader.parse()
    return reader
