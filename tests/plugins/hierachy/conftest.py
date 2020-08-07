#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import TYPE_CHECKING, Callable, Type

import pytest
from sqlalchemy.orm import Session

from smorest_sfs.plugins.hierachy_xlsx.parsers import HierachyParser
from smorest_sfs.utils.paths import ProjectPath

from .utils import get_parsed_reader

if TYPE_CHECKING:
    from .models import (
        TestCodeTable as TestCodeTable_,
        TestHierachyTable as TestHierachyTable_,
    )


@pytest.fixture
def xlsx_path_func() -> Callable[[str], Path]:
    def xlsx_path(filename: str) -> Path:
        xlsx_path = Path("tests", "data", "excels", filename)
        return ProjectPath.get_subpath_from_project(xlsx_path)

    return xlsx_path


@pytest.fixture
def TestHierachyTable() -> Type["TestHierachyTable_"]:
    # pylint: disable=W0621
    from .models import TestHierachyTable as TestHierachyTable__

    return TestHierachyTable__


@pytest.fixture
def parser(xlsx_path_func: Callable[[str], Path]) -> HierachyParser:
    # pylint: disable=W0621
    return get_parsed_reader("test-code.xlsx", xlsx_path_func)


@pytest.fixture
def TestCodeTable() -> Type["TestCodeTable_"]:
    # pylint: disable=W0621
    from .models import TestCodeTable as TestCodeTable__

    return TestCodeTable__


@pytest.fixture
def session() -> "Session":
    from .models import Session_

    session: "Session" = Session_()
    return session
