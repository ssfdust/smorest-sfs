#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试自定义ma的创建"""
from typing import Type

from flask import Flask
from flask_sqlalchemy.model import Model
from marshmallow import EXCLUDE


class TestMaCreataion:
    def test_ma_meta(self, ma_app: Flask) -> None:
        from smorest_sfs.extensions.marshal import ma

        ma.init_app(ma_app)

        TestSchema = type("TestSchema", (ma.Schema,), dict())

        assert TestSchema.Meta.unknown == EXCLUDE  # type: ignore

    def test_ma_converter(self, ma_app: Flask, DateTimeTestTable: Type[Model]) -> None:
        from smorest_sfs.extensions.marshal import (
            SQLAlchemySchema,
            SQLAlchemyAutoSchema,
            auto_field,
        )
        from smorest_sfs.extensions.marshal.fields import PendulumField as field
        from smorest_sfs.extensions.marshal import ma

        ma.init_app(ma_app)
        with ma_app.app_context():

            class TestSchema(SQLAlchemySchema):
                time = auto_field()

                class Meta:
                    model = DateTimeTestTable

            class TestAutoSchema(SQLAlchemyAutoSchema):
                class Meta:
                    model = DateTimeTestTable

            test_schema = TestSchema()
            test_auto_schema = TestAutoSchema()
            assert isinstance(test_schema.fields["time"], field) and isinstance(
                test_auto_schema.fields["time"], field
            )
