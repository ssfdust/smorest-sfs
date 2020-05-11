#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Callable, Type

import pytest
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_mptt.mixins import BaseNestedSets

from smorest_sfs.extensions.sqla import Model, SurrogatePK
from smorest_sfs.plugins.hierachy_xlsx.parsers import HierachyParser
from smorest_sfs.utils.paths import ProjectPath

from .utils import get_parsed_reader


@pytest.fixture
def xlsx_path_func() -> Callable[[str], Path]:
    def xlsx_path(filename: str) -> Path:
        xlsx_path = Path("tests", "data", "excels", filename)
        return ProjectPath.get_subpath_from_project(xlsx_path)

    return xlsx_path


@pytest.fixture
def TestHierachyTable(db: SQLAlchemy) -> Type[Model]:
    # pylint: disable=W0621
    class TestHierachyTable(Model, SurrogatePK, BaseNestedSets):
        name = db.Column(db.String(length=20), nullable=False)
        value = db.Column(db.Integer, nullable=False)

        def __repr__(self) -> str:
            return self.name

    db.create_all()

    return TestHierachyTable


@pytest.fixture
def parser(xlsx_path_func: Callable[[str], Path]) -> HierachyParser:
    # pylint: disable=W0621
    return get_parsed_reader("test-code.xlsx", xlsx_path_func)


@pytest.fixture
def TestCodeTable(db: SQLAlchemy) -> Type[Model]:
    # pylint: disable=W0621
    class TestCodeTable(Model, SurrogatePK, BaseNestedSets):
        name = db.Column(db.String(length=20), nullable=False)
        type_code = db.Column(db.String(length=20), nullable=False)
        value = db.Column(db.Integer, nullable=False)

        def __repr__(self) -> str:
            return self.name

    db.create_all()

    return TestCodeTable
