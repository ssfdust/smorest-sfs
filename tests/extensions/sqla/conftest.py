#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

import datetime
from typing import TYPE_CHECKING, Any, Iterator, Type

import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from tests._utils.tables import drop_tables

if TYPE_CHECKING:
    from .app import TestCRUDTable as TestCRUDTable_

FAKE_TIME = datetime.datetime(1994, 9, 11, 8, 20)
TABLES = ["sqla_test_crud_table"]


@pytest.fixture(scope="package")
def sqla_db() -> SQLAlchemy:
    from .app import sqla_db as sqla_db_instance

    return sqla_db_instance


@pytest.fixture(scope="package")
def TestCRUDTable(sqla_db: SQLAlchemy) -> Type["TestCRUDTable_"]:
    from .app import TestCRUDTable as TestCRUDTable__

    return TestCRUDTable__


@pytest.fixture(scope="package", autouse=True)
def sqla_app(sqla_db: SQLAlchemy) -> Iterator[Flask]:
    # pylint: disable=W0621, W0613
    from .app import flask_app

    with flask_app.app_context():
        sqla_db.create_all()
        yield flask_app
        drop_tables(sqla_db, TABLES)
        sqla_db.engine.dispose()


@pytest.fixture(autouse=True)
def fake_session(
    monkeypatch: Any, sqla_app: Flask, sqla_db: SQLAlchemy
) -> Iterator[None]:
    from smorest_sfs.extensions.sqla.db_instance import BaseModel

    monkeypatch.setattr(BaseModel, "_session", sqla_db.session)
    yield
    sqla_db.session.close_all()
