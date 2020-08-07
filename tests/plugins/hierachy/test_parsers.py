#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Any, Callable, List

import pytest

from .utils import get_parsed_reader


class TestHierachyReader:
    @pytest.mark.parametrize(
        "path, err", [("key-err-test-code.xlsx", KeyError)],
    )
    def test_err_on_load_xlsx(
        self, path: str, err: Exception, xlsx_path_func: Callable[[str], Path]
    ) -> None:
        with pytest.raises(err):
            get_parsed_reader(path, xlsx_path_func)

    @pytest.mark.parametrize(
        "path, records",
        [("test-camel-code.xlsx", [["name", "A1"], ["snake_value", 6]])],
    )
    def test_ident_reader(
        self, path: str, xlsx_path_func: Callable[[str], Path], records: List[List[Any]]
    ) -> None:
        reader = get_parsed_reader(path, xlsx_path_func=xlsx_path_func)
        A1 = reader.mapping["A1"]
        for record in records:
            assert A1[record[0]] == record[1]

    def test_relation_reader(self, xlsx_path_func: Callable[[str], Path]) -> None:
        reader = get_parsed_reader("test-code.xlsx", xlsx_path_func=xlsx_path_func)
        assert reader.relation_list[0] == ["A", "A1", "A2", "A3"]
