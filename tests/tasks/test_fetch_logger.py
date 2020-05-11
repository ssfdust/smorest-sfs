#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from flask_sqlalchemy import SQLAlchemy

from smorest_sfs.extensions import Celery


@pytest.mark.usefixtures("logging_info")
def test_fetch_logger(flask_celery: Celery, db: SQLAlchemy) -> None:
    from smorest_sfs.modules.logs.models import Log, ResponseLog

    result = flask_celery.delay("get-logger", "test-logger")
    item = result.get()
    db_cnt = (
        db.session.query(Log.id).union_all(db.session.query(ResponseLog.id)).count()
    )
    assert item["count"] == db_cnt
