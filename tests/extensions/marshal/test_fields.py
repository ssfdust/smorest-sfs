#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Dict, Tuple, Union

import pytest
from flask import Flask
from marshmallow import Schema, ValidationError
from pendulum import DateTime, tz

utc = tz.timezone("utc")


def test_fields_dump(ma_app: Flask, pendulum_field_schema: Schema) -> None:
    with ma_app.app_context():
        data = {"time": datetime(1994, 9, 11, 8, 20)}
        res = pendulum_field_schema.dump(data)
        assert res["time"] == "1994-09-11 16:20:00"


def test_fields_load(ma_app: Flask, pendulum_field_schema: Schema) -> None:
    with ma_app.app_context():
        data = {"time": "1994-09-11 08:20:00"}
        res = pendulum_field_schema.load(data)
        assert str(res["time"]) == "1994-09-11T00:20:00+00:00"


def test_fileds_none_load_handle(ma_app: Flask, pendulum_field_schema: Schema) -> None:
    with ma_app.app_context():
        data = {"time": None}
        res = pendulum_field_schema.load(data)
        assert res["time"] is None


def test_fields_empty_load_handle(ma_app: Flask, pendulum_field_schema: Schema) -> None:
    with ma_app.app_context():
        data = {"time": ""}
        with pytest.raises(ValidationError):
            pendulum_field_schema.load(data)


def test_fileds_none_dump_handle(ma_app: Flask, pendulum_field_schema: Schema) -> None:
    with ma_app.app_context():
        data = {"time": None}
        res = pendulum_field_schema.dump(data)
        assert res["time"] is None


@pytest.mark.parametrize(
    "data, result",
    [
        (
            {"created_date": "2019-04-03", "modified_date": "2019-04-03"},
            {
                "created__between": (
                    DateTime(2019, 4, 2, 16, tzinfo=utc),
                    DateTime(2019, 4, 3, 16, tzinfo=utc),
                ),
                "modified__between": (
                    DateTime(2019, 4, 2, 16, tzinfo=utc),
                    DateTime(2019, 4, 3, 16, tzinfo=utc),
                ),
            },
        ),
        (
            {"created_date": "2019-04-05"},
            {
                "created__between": (
                    DateTime(2019, 4, 4, 16, tzinfo=utc),
                    DateTime(2019, 4, 5, 16, tzinfo=utc),
                )
            },
        ),
        (
            {"modified_date": "2019-04-07"},
            {
                "modified__between": (
                    DateTime(2019, 4, 6, 16, tzinfo=utc),
                    DateTime(2019, 4, 7, 16, tzinfo=utc),
                )
            },
        ),
        (
            {
                "created_date": "2019-04-03",
                "modified_date": "2019-04-03",
                "created__ge": "2019-04-16 13:00:00",
            },
            {
                "created__between": (
                    DateTime(2019, 4, 2, 16, tzinfo=utc),
                    DateTime(2019, 4, 3, 16, tzinfo=utc),
                ),
                "modified__between": (
                    DateTime(2019, 4, 2, 16, tzinfo=utc),
                    DateTime(2019, 4, 3, 16, tzinfo=utc),
                ),
                "created__ge": DateTime(2019, 4, 16, 5, tzinfo=utc),
            },
        ),
    ],
)
def test_query_params_schema(
    ma_app: Flask,
    data: Dict[str, str],
    result: Dict[str, Union[DateTime, Tuple[DateTime, DateTime]]],
) -> None:
    from smorest_sfs.extensions.marshal.bases import BaseTimeParam

    with ma_app.app_context():
        schema = BaseTimeParam()
        assert schema.load(data) == result
