#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Type

import pytest
from flask import Flask
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from marshmallow import Schema


@pytest.fixture(scope="package")
def marshal_db() -> SQLAlchemy:
    db = SQLAlchemy()

    return db


@pytest.fixture(scope="package")
def ma_app(marshal_db: SQLAlchemy) -> Flask:
    flask_app = Flask("TestMa")
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    flask_app.config["BABEL_DEFAULT_TIMEZONE"] = "Asia/Shanghai"
    flask_app.config["BABEL_DEFAULT_LOCALE"] = "zh_cn"
    Babel(flask_app)
    marshal_db.init_app(flask_app)
    return flask_app


@pytest.fixture(scope="package")
def DateTimeTestTable(marshal_db: SQLAlchemy) -> Type[Model]:
    from smorest_sfs.extensions.sqla import Model

    class DateTimeTable(Model):
        __tablename__ = "datetime_table"
        id = marshal_db.Column(marshal_db.Integer, primary_key=True)
        time = marshal_db.Column(marshal_db.DateTime)

    return DateTimeTable


@pytest.fixture(scope="package")
def pendulum_field_schema() -> Schema:
    from smorest_sfs.extensions.marshal.fields import PendulumField

    class TestPendulumSchema(Schema):
        time = PendulumField(format="%Y-%m-%d %H:%M:%S", allow_none=True)

    return TestPendulumSchema()
