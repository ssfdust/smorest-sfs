#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Type

from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

from smorest_sfs.extensions.sqla import Model
from smorest_sfs.plugins.hierachy_xlsx.parsers import HierachyParser
from smorest_sfs.plugins.hierachy_xlsx.transformers import CodeTransformer, Transformer


class TestTransformer:
    def test_transformer(
        self, parser: HierachyParser, TestHierachyTable: Type[Model], db: SQLAlchemy
    ) -> None:
        transformer = Transformer(parser, TestHierachyTable, db.session)
        transformer.transform()
        data = TestHierachyTable.get_tree(db.session, json=True)
        assert data == [
            {"id": 1, "label": "A"},
            {"id": 2, "label": "A1"},
            {
                "children": [
                    {"id": 5, "label": "A21"},
                    {"id": 6, "label": "A22"},
                    {"id": 7, "label": "A23"},
                    {"id": 8, "label": "A24"},
                ],
                "id": 3,
                "label": "A2",
            },
            {
                "children": [{"id": 9, "label": "A31"}, {"id": 10, "label": "A32"}],
                "id": 4,
                "label": "A3",
            },
        ]

    def test_code_transformer(
        self, parser: HierachyParser, TestCodeTable: Type[Model], db: SQLAlchemy
    ) -> None:
        transformer = CodeTransformer(parser, TestCodeTable, db.session)
        transformer.transform()
        schema = Schema.from_dict(
            {"name": fields.Str(), "type_code": fields.Str(), "value": fields.Str()}
        )()

        def query(node: Any) -> Any:
            return node.filter_by(type_code=transformer.type_code)

        data = TestCodeTable.get_tree(
            db.session, json=True, json_fields=schema.dump, query=query
        )
        assert data == [
            {
                "type_code": "test-code",
                "id": 1,
                "label": "A",
                "name": "A",
                "value": "1",
            },
            {
                "type_code": "test-code",
                "id": 2,
                "label": "A1",
                "name": "A1",
                "value": "6",
            },
            {
                "children": [
                    {
                        "type_code": "test-code",
                        "id": 5,
                        "label": "A21",
                        "name": "A21",
                        "value": "5",
                    },
                    {
                        "type_code": "test-code",
                        "id": 6,
                        "label": "A22",
                        "name": "A22",
                        "value": "6",
                    },
                    {
                        "type_code": "test-code",
                        "id": 7,
                        "label": "A23",
                        "name": "A23",
                        "value": "7",
                    },
                    {
                        "type_code": "test-code",
                        "id": 8,
                        "label": "A24",
                        "name": "A24",
                        "value": "8",
                    },
                ],
                "type_code": "test-code",
                "id": 3,
                "label": "A2",
                "name": "A2",
                "value": "3",
            },
            {
                "children": [
                    {
                        "type_code": "test-code",
                        "id": 9,
                        "label": "A31",
                        "name": "A31",
                        "value": "10",
                    },
                    {
                        "type_code": "test-code",
                        "id": 10,
                        "label": "A32",
                        "name": "A32",
                        "value": "11",
                    },
                ],
                "type_code": "test-code",
                "id": 4,
                "label": "A3",
                "name": "A3",
                "value": "9",
            },
        ]
