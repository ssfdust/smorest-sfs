#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kombu import Queue


def get_default_queue(key: str = "default") -> Queue:
    mapping = {
        "default": Queue(
            "default",
            "default",
            durable=True,
            max_length=1000,
            routing_key="default",
            auto_delete=False,
            expires=None,
        )
    }
    return mapping[key]
