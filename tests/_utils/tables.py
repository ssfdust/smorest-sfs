#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试辅助工具集
"""
from typing import Any, List, Tuple

from flask_sqlalchemy import SQLAlchemy


def drop_tables(db: SQLAlchemy, table_names: List[str]) -> None:
    bind = db.get_engine()
    tables = [db.metadata.tables[table] for table in table_names]
    db.metadata.drop_all(bind=bind, tables=tables)


def clear_instances(db: SQLAlchemy, instances: Tuple[Any, ...]) -> None:
    for instance in instances:
        mapper = instance.__class__.__mapper__
        if instance not in db.session:
            db.session.add(instance)

        db.session.query(instance.__class__).filter(
            mapper.primary_key[0] == mapper.primary_key_from_instance(instance)[0]
        ).delete(synchronize_session="fetch")
