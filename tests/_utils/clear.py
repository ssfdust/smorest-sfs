#!/usr/bin/env python
# -*- coding: utf-8 -*-
from amqp.exceptions import NotFound
from flask import Flask
from kombu import Connection, Queue
from kombu.pools import connections
from loguru import logger

from .celery import disconnect


def clear_dummy(app: Flask) -> None:
    logger.remove(app.extensions["logger_ext"].handler_id)
    disconnect(app)
    app.after_request_funcs = {}


def clear_queue(queue_name: str) -> None:
    conn = Connection()
    pool = connections[conn]
    queue = Queue(queue_name)
    with pool.acquire_channel(block=True) as (_, channel):
        binding = queue(channel)
        try:
            binding.purge()
        except NotFound:
            pass
