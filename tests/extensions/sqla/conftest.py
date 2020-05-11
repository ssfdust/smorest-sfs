#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

import datetime
import os
from typing import Any, Iterator, Type

import pytest
import toml
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

from smorest_sfs.extensions import babel
from smorest_sfs.extensions.sqla import Model, SurrogatePK
from smorest_sfs.plugins.sa import SAQuery, SAStatement
from smorest_sfs.utils.paths import ProjectPath
from tests._utils.tables import drop_tables

FAKE_TIME = datetime.datetime(1994, 9, 11, 8, 20)
TABLES = [
    "sqla_test_crud_table",
    "test_crud_child_table",
    "test_crud_parent_table",
]


def get_pg_uri() -> str:
    test_config_path = ProjectPath.get_subpath_from_project("config/testing.toml")
    try:
        return toml.load(test_config_path)["SQLALCHEMY_DATABASE_URI"]
    except (FileNotFoundError, KeyError):
        return os.environ.get("PG_URI", "postgresql://postgres@localhost/postgres")


def get_inited_app(sqla_db: SQLAlchemy) -> Flask:
    # pylint: disable=W0621
    flask_app = Flask("TestSqla")
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = get_pg_uri()
    flask_app.config["BABEL_DEFAULT_TIMEZONE"] = "Asia/Shanghai"
    sqla_db.init_app(flask_app)
    babel.init_app(flask_app)

    return flask_app


@pytest.fixture(scope="package")
def sqla_db() -> SQLAlchemy:
    from smorest_sfs.extensions.sqla import db as sqla_db_instance

    return sqla_db_instance


@pytest.fixture(scope="package")
def TestCRUDTable(sqla_db: SQLAlchemy) -> Type[Model]:
    # pylint: disable=W0621
    class TestCRUDTable(SurrogatePK, Model):
        __tablename__ = "sqla_test_crud_table"

        name = sqla_db.Column(sqla_db.String(80), unique=True)

        def __repr__(self) -> str:
            return f"<TestCRUDTable {self.id}>"

    return TestCRUDTable


@pytest.fixture(scope="package")
def TestParentTable(sqla_db: SQLAlchemy) -> Type[Model]:
    # pylint: disable=W0621
    class TestParentTable(SurrogatePK, Model):
        __tablename__ = "test_crud_parent_table"
        name = sqla_db.Column(sqla_db.String(80), unique=True)

    return TestParentTable


@pytest.fixture(scope="package")
def TestChildTable(sqla_db: SQLAlchemy, TestParentTable: Type[Model]) -> Type[Model]:
    # pylint: disable=W0621
    class TestChildTable(SurrogatePK, Model):
        __tablename__ = "test_crud_child_table"
        name = sqla_db.Column(sqla_db.String(80), unique=True)
        pid = sqla_db.Column(sqla_db.Integer, sqla_db.ForeignKey(TestParentTable.id))
        parnet = sqla_db.relationship(
            TestParentTable,
            backref=sqla_db.backref("children", active_history=True),
            active_history=True,
        )

        def __repr__(self) -> str:
            return f"<TestChildTable {self.id}>"

    return TestChildTable


@pytest.fixture(scope="package")
def tables(TestCRUDTable: Type[Model], TestChildTable: Type[Model]) -> None:
    # pylint: disable=W0613, W0621
    pass


@pytest.fixture(scope="package", autouse=True)
def sqla_app(sqla_db: SQLAlchemy, tables: Any) -> Iterator[Flask]:
    # pylint: disable=W0621, W0613
    flask_app = get_inited_app(sqla_db)

    with flask_app.app_context():
        sqla_db.create_all()
        yield flask_app
        sqla_db.session.rollback()
        drop_tables(sqla_db, TABLES)


@pytest.fixture(scope="package")
def TestChildSchema() -> Type[Schema]:
    # pylint: disable=W0621, W0613
    class TestChildSchema(Schema):
        id = fields.Int()
        pid = fields.Int()
        name = fields.Str()
        deleted = fields.Boolean()
        modified = fields.DateTime()
        created = fields.DateTime()

    return TestChildSchema


@pytest.fixture(scope="package")
def TestParentSchema(TestChildSchema: Type[Schema]) -> Type[Schema]:
    # pylint: disable=W0621, W0613
    class TestParentSchema(TestChildSchema):  # type: ignore
        children = fields.List(fields.Nested(TestChildSchema))

        class Meta:
            exclude = ["pid"]

    return TestParentSchema


@pytest.fixture
def TestTableTeardown(sqla_db: SQLAlchemy) -> Iterator[None]:
    # pylint: disable=W0621, W0613
    yield
    for table in [
        "sqla_test_crud_table",
        "test_crud_child_table",
        "test_crud_parent_table",
    ]:
        sqla_db.session.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE ")
    sqla_db.session.commit()


@pytest.fixture
def TestSASql(sqla_db: SQLAlchemy, TestCRUDTable: Type[Model]) -> Type[SAStatement]:
    # pylint: disable=W0621, W0613
    class TestSASql(SAStatement):
        def __init__(self, name: str) -> None:
            self.sa_sql = sqla_db.select([TestCRUDTable.name]).where(
                TestCRUDTable.name == name
            )

    return TestSASql


@pytest.fixture
def TestOneTableQuery(sqla_db: SQLAlchemy, TestCRUDTable: Type[Model]) -> Type[SAQuery]:
    # pylint: disable=W0621, W0613
    class TestOneTableQuery(SAQuery):
        def __init__(self) -> None:
            self.query = TestCRUDTable.where(name="bbc")

        def get_record(self) -> Any:
            return self.query.all()

    return TestOneTableQuery


@pytest.fixture
def TestTwoTablesQuery(
    sqla_db: SQLAlchemy, TestCRUDTable: Type[Model], TestChildTable: Type[Model]
) -> Type[SAQuery]:
    # pylint: disable=W0621, W0613
    class TestTwoTablesQuery(SAQuery):
        def __init__(self) -> None:
            self.query = sqla_db.session.query(
                TestCRUDTable,
                TestChildTable,
                TestChildTable.name,
                TestCRUDTable.name,
                TestCRUDTable.id.label("crud_id"),
            ).filter(TestCRUDTable.name == "bbc")

        def get_record(self) -> Any:
            return self.query.all()

    return TestTwoTablesQuery


@pytest.fixture
def TestOneColQuery(sqla_db: SQLAlchemy, TestCRUDTable: Type[Model]) -> Type[SAQuery]:
    # pylint: disable=W0621, W0613
    class TestOneColQuery(SAQuery):
        def __init__(self) -> None:
            self.query = sqla_db.session.query(TestCRUDTable.name).filter(
                TestCRUDTable.name == "bbc"
            )

        def get_record(self) -> Any:
            return self.query.all()

    return TestOneColQuery
