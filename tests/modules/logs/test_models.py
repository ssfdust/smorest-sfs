#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from smorest_sfs.modules.logs.models import Log, ResponseLog


@pytest.mark.usefixtures("flask_app")
def test_log() -> None:
    item = Log.create(module="test", line=13, level="info", message="test")
    assert str(item) == "test"
    item.hard_delete()


@pytest.mark.usefixtures("flask_app")
def test_resp_log() -> None:
    item = ResponseLog.create(url="test", method="POST", ip="1.0.0.0", status_code=200)
    assert str(item) == "POST test"
    item.hard_delete()
