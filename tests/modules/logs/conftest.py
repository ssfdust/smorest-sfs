#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Callable, Iterator, Tuple, Type

import pytest
from flask import Flask
from marshmallow import Schema

from smorest_sfs.modules.logs.models import Log, ResponseLog


@pytest.fixture
def log_items(
    flask_app: Flask, temp_db_instance_helper: Callable[..., Iterator[Any]],
) -> Iterator[Tuple[Log, ...]]:
    # pylint: disable=W0613
    for _ in temp_db_instance_helper(
        Log(
            module="test.info",
            line=15,
            level="info",
            message="test",
            created="2020-04-12 09:00:00",
            modified="2020-04-12 10:00:00",
        ),
        Log(
            module="test.info",
            line=15,
            level="info",
            message="test",
            created="2020-04-13 17:00:00",
            modified="2020-04-13 17:00:00",
        ),
        Log(
            module="test.info",
            line=15,
            level="info",
            message="test",
            created="2020-04-13 09:00:00",
            modified="2020-04-13 10:00:00",
        ),
        Log(
            module="test.debug",
            line=15,
            level="debug",
            message="test",
            created="2020-04-12 09:00:00",
            modified="2020-04-12 18:00:00",
        ),
        Log(
            module="test.debug",
            line=15,
            level="debug",
            message="test",
            created="2020-04-12 09:00:00",
            modified="2020-04-12 10:00:00",
        ),
        Log(
            module="test.error",
            line=15,
            level="error",
            message="test",
            created="2020-04-12 09:00:00",
            modified="2020-04-12 10:00:00",
        ),
        Log(
            module="test.warn",
            line=15,
            level="warn",
            message="test",
            created="2020-04-12 09:00:00",
            modified="2020-04-12 10:00:00",
        ),
        Log(
            module="test.warn",
            line=15,
            level="warn",
            message="test",
            created="2020-04-12 09:00:00",
            modified="2020-04-12 10:00:00",
        ),
    ):
        yield _


@pytest.fixture
def resp_log_items(
    flask_app: Flask, temp_db_instance_helper: Callable[..., Iterator[Any]],
) -> Iterator[Tuple[ResponseLog, ...]]:
    # pylint: disable=W0613
    for _ in temp_db_instance_helper(
        ResponseLog(
            module="test.test_1",
            status_code=200,
            ip="127.0.0.1",
            method="PUT",
            url="/test/test_1",
            created="2020-04-11 09:00:00",
            modified="2020-04-12 10:00:00",
        ),
        ResponseLog(
            module="test.test_2",
            status_code=200,
            ip="127.0.0.1",
            method="PUT",
            url="/test/test_2",
            created="2020-04-12 09:00:00",
            modified="2020-04-12 10:00:00",
        ),
        ResponseLog(
            module="test.test_3",
            status_code=200,
            ip="127.0.0.1",
            method="GET",
            url="/test/test_3",
            created="2020-04-12 09:00:00",
            modified="2020-04-12 10:00:00",
        ),
        ResponseLog(
            module="test.test_4",
            status_code=200,
            ip="127.0.0.1",
            method="OPTIONS",
            url="/test/test_4",
            created="2020-04-12 09:00:00",
            modified="2020-04-12 10:00:00",
        ),
        ResponseLog(
            module="test.test_5",
            status_code=301,
            ip="127.0.0.1",
            method="POST",
            url="/test/test_5",
            created="2020-04-12 09:00:00",
            modified="2020-04-12 10:00:00",
        ),
        ResponseLog(
            module="test.test_6",
            status_code=200,
            ip="127.0.0.1",
            method="POST",
            url="/test/test_6",
            created="2020-04-13 17:00:00",
            modified="2020-04-13 17:00:00",
        ),
        ResponseLog(
            module="test.test_7",
            status_code=200,
            ip="127.0.0.1",
            method="DELETE",
            url="/test/test_7",
            created="2020-04-13 15:00:00",
            modified="2020-04-13 15:00:00",
        ),
    ):
        yield _


@pytest.fixture
def LogSchema(flask_app: Flask) -> Type[Schema]:
    # pylint: disable=W0621, W0613
    from smorest_sfs.modules.logs.schemas import LogSchema

    return LogSchema
