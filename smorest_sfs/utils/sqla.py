#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import namedtuple
from typing import List, Optional

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, UniqueConstraint, inspect

from smorest_sfs.extensions.sqla import Model

RelateTableArgs = namedtuple(
    "RelateTableArgs", ["tablename", "related_key", "the_ohter_related_key"]
)


class AttrHistory:
    def __init__(self, added: Optional[List[Model]], deleted: Optional[List[Model]]):
        self.added: List[Model] = added or []
        self.deleted: List[Model] = deleted or []


def create_relation_table(db: SQLAlchemy, table_args: RelateTableArgs) -> Table:
    return db.Table(
        table_args.tablename,
        db.Column(table_args.related_key, db.Integer(), nullable=False),
        db.Column(table_args.the_ohter_related_key, db.Integer(), nullable=False),
        UniqueConstraint(table_args.related_key, table_args.the_ohter_related_key),
    )


def get_histroy(model: Model, attr: str) -> AttrHistory:
    model_state = inspect(model)
    attr_state = getattr(model_state.attrs, attr)
    attr_hist = attr_state.history
    if not attr_hist.has_changes():
        raise ValueError("No changes found")
    return AttrHistory(attr_hist.added, attr_hist.deleted)
