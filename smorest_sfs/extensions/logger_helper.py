#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kombu import Queue

from .logger import Logger


def create_logger(queue_name: str = "logger-queue") -> Logger:
    from smorest_sfs.plugins.rpc import Publisher

    queue = get_logger_queue(queue_name)

    return Logger(Publisher, publish_args={"queue": queue})


def get_logger_queue(name: str) -> Queue:
    return Queue(name, "logger", durable=True, routing_key="logger")
