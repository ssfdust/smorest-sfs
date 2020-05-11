#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Type

import pytest
from flask import Flask
from flask_babel import Babel
from marshmallow import Schema

from smorest_sfs.extensions.marshal.fields import PendulumField


@pytest.fixture(scope="package")
def ma_app() -> Flask:
    flask_app = Flask("TestMa")
    flask_app.config["BABEL_DEFAULT_TIMEZONE"] = "Asia/Shanghai"
    flask_app.config["BABEL_DEFAULT_LOCALE"] = "zh_cn"
    Babel(flask_app)
    return flask_app


@pytest.fixture(scope="package")
def pendulum_field_schema() -> Schema:
    class TestPendulumSchema(Schema):
        time = PendulumField(format="%Y-%m-%d %H:%M:%S", allow_none=True)

    return TestPendulumSchema()
