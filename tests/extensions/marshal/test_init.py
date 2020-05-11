#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试自定义ma的创建"""
from flask import Flask
from marshmallow import EXCLUDE

from smorest_sfs.extensions.marshal import ma


class TestMaCreataion:
    def test_ma_meta(self, ma_app: Flask) -> None:

        ma.init_app(ma_app)

        TestSchema = type("TestSchema", (ma.Schema,), dict())

        assert TestSchema.Meta.unknown == EXCLUDE  # type: ignore
