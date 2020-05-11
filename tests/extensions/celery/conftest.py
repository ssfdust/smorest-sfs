#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any, Iterator, Type

import celery
import pytest
from celery.contrib.pytest import worker
from flask import Flask


@pytest.fixture(scope="package")
def config() -> Type[Any]:
    class TestConfig:
        CELERY_BACKEND = "redis://"
        CELERY_BROKER = "amqp://"
        CELERY_ACCEPT_CONTENT = ["json"]
        CELERY_REDBEAT_REDIS_URL = "redis://"
        CELERY_REDBEAT_LOCK_TIMEOUT = 30

    return TestConfig


@pytest.fixture(scope="package")
def celery_flask_app(config: Any) -> Flask:
    # pylint: disable=W0621
    flask_app = Flask("TestCelery")
    flask_app.config.from_object(config)

    return flask_app


@pytest.fixture
def celery_ext(celery_flask_app: Flask, celery_app: celery.Celery) -> Any:
    # pylint: disable=W0621
    from smorest_sfs.extensions.celery import Celery

    celery_extension = Celery(celery_flask_app, update_celery_immediately=False)
    celery_extension.update_celery(celery_app)

    return celery_extension


@pytest.fixture
def celery_worker(celery_ext: Any) -> Iterator[Any]:
    # pylint: disable=W0621
    _celery_app = celery_ext.get_celery_app()
    with worker.start_worker(_celery_app, pool="solo",) as w:
        yield w
