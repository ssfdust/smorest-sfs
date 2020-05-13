#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Callable, Iterator
import pytest

from smorest_sfs.modules.logs.models import Log, ResponseLog


@pytest.mark.usefixtures("flask_app")
def test_log(temp_db_instance_helper: Callable[..., Iterator[Any]]) -> None:
    for log in temp_db_instance_helper(
        Log(module="test", line=13, level="info", message="test")
    ):
        assert str(log) == "test"


@pytest.mark.usefixtures("flask_app")
def test_resp_log(temp_db_instance_helper: Callable[..., Iterator[Any]]) -> None:
    for resp_log in temp_db_instance_helper(
        ResponseLog(url="test", method="POST", ip="1.0.0.0", status_code=200)
    ):
        assert str(resp_log) == "POST test"
