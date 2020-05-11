#!/usr/bin/env python
# -*- coding: utf-8 -*-
from celery import signals
from flask import Flask


def disconnect(app: Flask) -> None:
    for sig in ["task_postrun", "task_prerun", "worker_process_init"]:
        if "celery_ext" in app.extensions:
            signal = getattr(signals, sig)
            connected = getattr(app.extensions["celery_ext"], "_" + sig)
            signal.disconnect(connected)
