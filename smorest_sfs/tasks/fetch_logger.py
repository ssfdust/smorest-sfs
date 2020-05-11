#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict

from kombu import Queue

from smorest_sfs.extensions import celery, db
from smorest_sfs.modules.logs.models import Log, ResponseLog
from smorest_sfs.plugins.rpc import Subscriber
from smorest_sfs.services.logs import LogCollecter


@celery.task("get-logger")
def get_logs_from_subcriber(queue_name: str = "logger-queue") -> Dict[str, int]:
    queue = Queue(queue_name, "logger", durable=True, routing_key="logger")
    subscriber = Subscriber(queue, limit=5000)
    collecter = LogCollecter()
    for item in subscriber.subscribe():
        collecter.add(item)
    db.session.bulk_insert_mappings(Log, collecter.logs)
    db.session.bulk_insert_mappings(ResponseLog, collecter.resp_logs)
    db.session.commit()

    return {"count": collecter.count}
