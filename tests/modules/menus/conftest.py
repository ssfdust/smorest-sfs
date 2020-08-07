#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Iterator

import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


@pytest.fixture
def fake_menus(flask_app: Flask, db: SQLAlchemy) -> Iterator[None]:
    # pylint: disable=W0621, W0613
    from smorest_sfs.modules.menus.models import Menu
    from smorest_sfs.services.menus.import_menus import import_menus_from_filepath

    import_menus_from_filepath("tests/data/menus/test-menus.xlsx")
    db.session.commit()
    yield
    db.session.execute("TRUNCATE TABLE {} RESTART IDENTITY".format(Menu.__tablename__))
