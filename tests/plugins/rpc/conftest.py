#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps
from socket import timeout
from typing import Callable

import pytest
from flask import Flask
from kombu import Connection, Queue


@pytest.fixture
def listen(
    flask_app: Flask,
) -> Callable[..., Callable[[Callable[..., None]], Callable[..., None]]]:
    conn = Connection(flask_app.config["CELERY_BROKER_URL"])

    def _listen(queue: Queue) -> Callable[[Callable[..., None]], Callable[..., None]]:
        def decorate(
            func: Callable[..., None]
        ) -> Callable[[Callable[..., None]], None]:
            @wraps(func)
            def wrapper() -> None:
                with conn.Consumer(queue, callbacks=[func]):
                    while True:
                        try:
                            conn.drain_events(timeout=1)
                        except timeout:
                            break

            return wrapper

        return decorate

    return _listen
