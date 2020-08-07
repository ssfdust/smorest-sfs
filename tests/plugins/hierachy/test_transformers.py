#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Type

from sqlalchemy.orm import Session

from smorest_sfs.extensions.sqla import Model
from smorest_sfs.plugins.hierachy_xlsx.parsers import HierachyParser
from smorest_sfs.plugins.hierachy_xlsx.transformers import Transformer


class TestTransformer:
    def test_transformer(
        self, parser: HierachyParser, TestHierachyTable: Type[Model], session: Session
    ) -> None:
        transformer = Transformer(parser, model_cls=TestHierachyTable, session=session)
        transformer.transform()
        session.commit()
        data = TestHierachyTable.get_tree(session, json=True)
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
