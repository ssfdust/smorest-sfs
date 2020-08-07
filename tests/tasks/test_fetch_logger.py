#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING

import pytest
from flask_sqlalchemy import SQLAlchemy

if TYPE_CHECKING:
    from smorest_sfs.extensions.celery import Celery


@pytest.mark.usefixtures("logging_info")
def test_fetch_logger(flask_celery: "Celery", db: SQLAlchemy) -> None:
    from smorest_sfs.modules.logs.models import Log, ResponseLog

    result = flask_celery.delay("get-logger", "test-logger")
    item = result.get()
    db_cnt = (
        db.session.query(Log.id_).union_all(db.session.query(ResponseLog.id_)).count()
    )
    assert item["count"] == db_cnt
    db.session.query(Log).delete()
    db.session.query(ResponseLog).delete()
    db.session.commit()
