#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from typing import Iterator, Type

import marshmallow as ma
import pytest
from flask import Flask

from smorest_sfs.extensions import babel
from smorest_sfs.extensions.api import Api
from smorest_sfs.extensions.marshal.bases import BasePageSchema
from smorest_sfs.extensions.sqla import Model, SurrogatePK
from smorest_sfs.extensions.sqla.db_instance import SQLAlchemy  # type: ignore
from tests._utils.tables import drop_tables

TABLES = ["test_pagination"]


def init_flaskapp(db: SQLAlchemy) -> Flask:  # type: ignore
    # pylint: disable=W0621
    flask_app = Flask("TestApi")
    flask_app.config["OPENAPI_VERSION"] = "3.0.2"
    flask_app.config["BABEL_DEFAULT_TIMEZONE"] = "Asia/Shanghai"
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "PG_URI", "postgresql://postgres@localhost/postgres"
    )

    babel.init_app(flask_app)
    db.init_app(flask_app)

    return flask_app


@pytest.fixture(scope="package")
def api_db() -> SQLAlchemy:
    from smorest_sfs.extensions import db as db_instance

    return db_instance


@pytest.fixture(scope="package")
def TestPagination(api_db: SQLAlchemy) -> Type[Model]:  # type: ignore
    # pylint: disable=W0621
    class TestPagination(SurrogatePK, Model):

        __tablename__ = "test_pagination"

        name = api_db.Column(api_db.String(10))

    return TestPagination


@pytest.fixture(scope="package")
def api_app(api_db: SQLAlchemy) -> Iterator[Flask]:  # type: ignore
    # pylint: disable=W0621
    flask_app = init_flaskapp(api_db)

    with flask_app.app_context():
        api_db.create_all()
        yield flask_app
        api_db.session.rollback()
        drop_tables(api_db, TABLES)


@pytest.fixture(scope="package")
def api(api_app: Flask) -> Api:
    # pylint: disable=W0621
    return Api(api_app)


@pytest.fixture(scope="package")
def TestSchema() -> Type[ma.Schema]:
    # pylint: disable=W0621
    class TestSchema(ma.Schema):
        id = ma.fields.Int(dump_only=True)
        name = ma.fields.String()

    return TestSchema


@pytest.fixture(scope="package")
def TestPageSchema(TestSchema: ma.Schema) -> Type[ma.Schema]:
    # pylint: disable=W0621
    class TestPageSchema(BasePageSchema):

        data = ma.fields.List(ma.fields.Nested(TestSchema))

    return TestPageSchema


@pytest.fixture(scope="package", autouse=True)
def setup_db(api_app: Flask, api_db: SQLAlchemy, TestPagination: Type[Model]):  # type: ignore
    # pylint: disable=W0613, W0621
    api_db.create_all()
    data = [TestPagination(name=str(i + 1)) for i in range(20)]
    api_db.session.bulk_save_objects(data)
    api_db.session.commit()
