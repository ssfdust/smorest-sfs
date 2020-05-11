#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from typing import Tuple, Union

import pendulum


def utcnow() -> datetime.datetime:
    return datetime.datetime.utcnow()


def _utctoday(now: datetime.datetime) -> datetime.date:
    return now.date()


def utctoday() -> datetime.date:
    now = datetime.datetime.utcnow()
    return _utctoday(now)


def convert_timezone(
    dt: Union[pendulum.DateTime, datetime.datetime], timezone: str
) -> pendulum.DateTime:
    tz = pendulum.tz.timezone(timezone)
    return tz.convert(dt)  # type: ignore


def expand_datetime(
    dt: pendulum.DateTime,
) -> Tuple[pendulum.DateTime, pendulum.DateTime]:
    return dt, dt.add(days=1)
