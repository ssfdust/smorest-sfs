#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING

import pytest

from tests.typings import INS_HELPER

if TYPE_CHECKING:
    from smorest_sfs.modules.logs.models import Log, ResponseLog


@pytest.mark.usefixtures("flask_app")
def test_log(temp_db_instance_helper: INS_HELPER["Log"]) -> None:
    from smorest_sfs.modules.logs.models import Log

    for log in temp_db_instance_helper(
        Log(module="test", line=13, level="info", message="test")
    ):
        assert isinstance(log, Log)
        log.save()
        assert log.module == "test" and log.id_ is not None


@pytest.mark.usefixtures("flask_app")
def test_resp_log(temp_db_instance_helper: INS_HELPER["ResponseLog"]) -> None:
    from smorest_sfs.modules.logs.models import ResponseLog

    for resp_log in temp_db_instance_helper(
        ResponseLog(url="test", method="POST", ip="1.0.0.0", status_code=200)
    ):
        assert isinstance(resp_log, ResponseLog)
        resp_log.save()
        assert resp_log.url == "test"
