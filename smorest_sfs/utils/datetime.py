#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from typing import Tuple, Union

import pendulum
from pendulum.datetime import DateTime


def utcnow() -> datetime.datetime:
    return datetime.datetime.utcnow()


def _utctoday(now: datetime.datetime) -> datetime.date:
    return now.date()


def utctoday() -> datetime.date:
    now = datetime.datetime.utcnow()
    return _utctoday(now)


def convert_timezone(dt: Union[DateTime, datetime.datetime], timezone: str) -> DateTime:
    tz = pendulum.tz.timezone(timezone)
    return tz.convert(dt)  # type: ignore


def expand_datetime(dt: DateTime,) -> Tuple[DateTime, DateTime]:
    return dt, dt.add(days=1)
