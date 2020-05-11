#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from typing import Iterator

import pytest
from flask import Flask


@pytest.fixture(scope="package", autouse=True)
def captcha_app() -> Iterator[Flask]:
    app = Flask("TestStorage")
    with app.app_context():
        yield app
