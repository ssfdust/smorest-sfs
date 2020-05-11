#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Iterator

import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from smorest_sfs.modules.codes.models import Code
from smorest_sfs.services.codes import import_codes_from_dir


@pytest.fixture
def fake_codes(flask_app: Flask, db: SQLAlchemy) -> Iterator[None]:
    # pylint: disable=W0613
    import_codes_from_dir("tests/data/codes/")
    yield
    db.session.execute("TRUNCATE TABLE {} RESTART IDENTITY".format(Code.__tablename__))
    db.session.commit()
