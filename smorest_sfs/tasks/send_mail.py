#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Any

from smorest_sfs.extensions import celery, mail


@celery.task("send-email")
def send_mail(content: Any) -> None:
    mail.send(content)
