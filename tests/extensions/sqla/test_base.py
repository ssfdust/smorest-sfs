#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试mixin模块"""

from copy import copy
from typing import TYPE_CHECKING, Type

from flask_sqlalchemy import SQLAlchemy

if TYPE_CHECKING:
    from .app import TestCRUDTable as TestCRUDTable_


class TestSqlaCRUD:
    def test_save_should_update_modified(
        self, TestCRUDTable: Type["TestCRUDTable_"], sqla_db: SQLAlchemy
    ) -> None:
        item = TestCRUDTable.create(name="save_should_update_modified")
        pre_modified = copy(item.modified)
        sqla_db.session.commit()

        item.name = "save_should_updated"
        item.save()
        sqla_db.session.commit()

        assert item.modified > pre_modified

    def test_update_should_success(
        self, TestCRUDTable: Type["TestCRUDTable_"], sqla_db: SQLAlchemy
    ) -> None:
        item = TestCRUDTable.create(name="update_never_success")
        pre_modified = copy(item.modified)
        sqla_db.session.commit()

        item.update(name="update_should_success")
        sqla_db.session.commit()

        assert item.name == "update_should_success" and item.modified > pre_modified

    def test_soft_delete_id_should_exists(
        self, TestCRUDTable: Type["TestCRUDTable_"], sqla_db: SQLAlchemy
    ) -> None:
        item = TestCRUDTable.create(name="soft_delete_id_should_exists")
        item.delete()
        notfound = TestCRUDTable.find(item.id_)
        found = TestCRUDTable.where(id_=item.id_).with_deleted().first()
        deleted = item.deleted

        assert deleted is True and notfound is None and found is not None

    def test_destory(
        self, TestCRUDTable: Type["TestCRUDTable_"], sqla_db: SQLAlchemy
    ) -> None:
        ids = []
        for name in ["a", "b", "c"]:
            new = TestCRUDTable.create(name=name)
            ids.append(new.id_)
        sqla_db.session.commit()
        TestCRUDTable.destroy(*ids[1:])
        found = TestCRUDTable.find(ids[0])
        notfound = TestCRUDTable.find(ids[1])
        assert found and notfound is None
