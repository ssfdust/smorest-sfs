#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Any, Iterator

import celery
import pytest
from celery.contrib.testing import worker
from flask import Flask
from flask.testing import FlaskClient
from loguru import logger

from smorest_sfs.extensions import Celery
from smorest_sfs.extensions.logger_helper import create_logger
from tests._utils.clear import clear_queue


@pytest.fixture(scope="package", autouse=True)
def flask_celery(flask_app: Flask, celery_session_app: celery.Celery) -> Celery:
    # pylint: disable=W0621

    celery_ext = Celery()
    celery_ext.init_app(flask_app)

    celery_ext.update_celery(celery_session_app)

    return celery_ext


@pytest.fixture(scope="package", autouse=True)
def flask_celery_app(flask_celery: Celery) -> celery.Celery:
    # pylint: disable=W0621
    celery_app = flask_celery.get_celery_app()
    celery_app.loader.import_task_module("smorest_sfs.tasks")
    return celery_app


@pytest.fixture(scope="package", autouse=True)
def flask_celery_worker(flask_celery_app: celery.Celery) -> Any:
    # pylint: disable=W0621
    with worker.start_worker(
        flask_celery_app, pool="solo", perform_ping_check=False,
    ) as w:
        yield w


@pytest.fixture
def task_logger(flask_app: Flask) -> Iterator[None]:
    clear_queue("test-logger")
    log = create_logger("test-logger")
    log.init_app(flask_app)
    yield
    logger.remove(log.handler_id)
    flask_app.after_request_funcs = {}


@pytest.fixture
def logging_info(task_logger: None, flask_app_client: FlaskClient) -> None:
    # pylint: disable=W0621,W0613
    logger.debug("test1")
    logger.info("test1")
    logger.error("test1")
    flask_app_client.get("/api/v1/")
    flask_app_client.post("/api/v1/", json={"test": "test"})
