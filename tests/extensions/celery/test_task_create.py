#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Any

import pytest
from flask import current_app

from smorest_sfs.extensions import Celery


def test_create_task(celery_ext: Celery, celery_worker: Any) -> None:
    # pylint: disable=W0612
    @celery_ext.task("test1")
    def mul(x: int, y: int) -> int:
        return x * y

    celery_worker.reload()

    assert celery_ext.call("test1", 4, 4) == 16


def test_flask_context_included(celery_ext: Celery, celery_worker: Any) -> None:
    # pylint: disable=W0612

    @celery_ext.task("test2")
    def find_name() -> str:
        # pylint: disable=W0621
        return getattr(current_app, "name")

    celery_worker.reload()
    result = celery_ext.delay("test2")
    assert result.get(timeout=10) == "TestCelery"


def test_force_task_name(celery_ext: Celery) -> None:
    # pylint: disable=W0612
    with pytest.raises(ValueError):

        @celery_ext.task("")
        def no_name_func() -> None:
            pass
