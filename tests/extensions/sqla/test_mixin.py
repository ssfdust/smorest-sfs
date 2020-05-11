#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试mixin模块"""

from copy import copy
from typing import Any, List, Type

import pytest
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema

from smorest_sfs.extensions.sqla import CharsTooLong, DuplicateEntry, Model
from smorest_sfs.extensions.sqla.helpers import set_default_for_instance
from tests._utils.injection import FixturesInjectBase


class TestSqlaCRUD:
    def test_created_must_have_id(self, TestCRUDTable: Type[Model]) -> None:
        item = TestCRUDTable.create(name="created_must_have_id")
        assert item.id is not None and item.name == "created_must_have_id"

    def test_save_must_have_id(self, TestCRUDTable: Type[Model]) -> None:
        item = TestCRUDTable(name="save_must_have_id")
        item.save()
        assert item.id is not None and item.name == "save_must_have_id"

    def test_save_should_update_modified(self, TestCRUDTable: Type[Model]) -> None:
        item = TestCRUDTable.create(name="save_should_update_modified")
        pre_modified = copy(item.modified)
        item.name = "save_should_updated"
        item.save()
        assert item.modified > pre_modified

    def test_update_should_success(self, TestCRUDTable: Type[Model]) -> None:
        item = TestCRUDTable.create(name="update_never_success")
        pre_modified = copy(item.modified)
        item.update(name="update_should_success")
        assert item.name == "update_should_success" and item.modified > pre_modified

    def test_update_should_not_update_blacked_keys(
        self, TestCRUDTable: Type[Model]
    ) -> None:
        item = TestCRUDTable.create(name=1)
        item.update(
            id=10000,
            name="update_should_not_update_blacked_keys",
            deleted=True,
            created="2008-04-12",
            modified="2008-04-12",
        )
        assert (
            item.name == "update_should_not_update_blacked_keys"
            and item.id != 10000
            and item.deleted is False
            and item.modified.strftime("%Y-%M-%d") != "2008-04-12"
            and item.created.strftime("%Y-%M-%d") != "2008-04-12"
        )

    def test_soft_delete_id_should_exists(
        self, TestCRUDTable: Type[Model], sqla_db: SQLAlchemy  # type: ignore
    ) -> None:
        item = TestCRUDTable.create(name="soft_delete_id_should_exists")
        item.delete()

        assert (
            item.deleted is True
            and sqla_db.session.query(TestCRUDTable).get(item.id) is not None
        )

    def test_hard_delete_id_never_exists(
        self, TestCRUDTable: Type[Model], sqla_db: SQLAlchemy  # type: ignore
    ) -> None:
        item = TestCRUDTable.create(name="hard_delete_id_never_exists")
        item.hard_delete()

        assert (
            item.deleted is False
            and sqla_db.session.query(TestCRUDTable).get(item.id) is None
        )

    def test_errors(self, TestCRUDTable: Type[Model]) -> None:
        very_long_text = (
            "sdjiasdjuwhqyuh1274yh7hsduaihsduwhqeuhquiehuhdnuq"
            "sajdasoijdsahjduhasduhsaduhasudhausidhuashduhaish"
            "sadasdasdasdasdasdasd"
        )
        with pytest.raises(DuplicateEntry):
            TestCRUDTable.create(name="duplicate_entry")
            TestCRUDTable.create(name="duplicate_entry")
        with pytest.raises(CharsTooLong):
            TestCRUDTable.create(name=very_long_text)


class TestUpdateBySchema(FixturesInjectBase):
    TestParentTable: Model
    TestParentSchema: Type[Schema]
    item: Model
    fixture_names = ("TestParentTable", "TestParentSchema")
    schema: Type[Schema]

    def do_init_update_by_schema(self, **kwargs: Any) -> Any:
        temp_instance = self.TestParentTable(**kwargs)
        temp_instance = set_default_for_instance(temp_instance)
        self.item.update_by_ma(self.schema, temp_instance)
        return temp_instance

    def create_item_and_schema(self, schema_kwargs: Any, **item_kwargs: Any) -> None:
        setattr(self, "item", self.TestParentTable(**item_kwargs))
        setattr(self, "schema", self.TestParentSchema(only=schema_kwargs))

    def teardown_method(self, _: Any) -> None:
        setattr(self, "item", None)
        setattr(self, "schema", None)

    @pytest.mark.usefixtures("TestTableTeardown")
    def test_normal_schema_should_update_successfully(self) -> None:
        self.create_item_and_schema(None, name="the_name_should_be_changed")
        self.do_init_update_by_schema(name="the_changed_name")
        assert self.item.name == "the_changed_name"

    @pytest.mark.usefixtures("TestTableTeardown")
    def test_no_keys_in_schema_should_update_nothing(self) -> None:
        self.create_item_and_schema((), name="the_name_should_not_be_changed")
        self.do_init_update_by_schema(name="the_name_should_never_changed")
        assert self.item.name == "the_name_should_not_be_changed"

    @pytest.mark.usefixtures("TestTableTeardown")
    @pytest.mark.parametrize("key", ["id", "deleted", "modified", "created"])
    def test_blacked_keys_in_schema_should_update_nothing(self, key: str) -> None:
        self.create_item_and_schema(
            (key,), name="the_blacked_key_should_not_be_changed"
        )
        temp_instance = self.do_init_update_by_schema(
            name="the_key_should_never_changed"
        )
        updated_val = getattr(temp_instance, key)
        assert self.item.name != updated_val

    @pytest.mark.usefixtures("TestTableTeardown")
    def test_temp_instance_should_not_be_saved(self) -> None:
        self.create_item_and_schema(None, name="temp_instance_should_not_be_saved")
        temp_instance = self.do_init_update_by_schema(name="the_id_is_none")
        assert temp_instance.id is None

    @pytest.mark.usefixtures("TestTableTeardown")
    def test_temp_instance_should_not_in_session(self, sqla_db: SQLAlchemy) -> None:  # type: ignore
        self.create_item_and_schema(None, name="temp_instance_should_not_in_session")
        temp_instance = self.do_init_update_by_schema(
            name="the_temp_instance_not_in_session"
        )
        assert temp_instance not in sqla_db.session

    @pytest.mark.usefixtures("TestTableTeardown")
    def test_temp_instance_should_be_flushed(self, sqla_db: SQLAlchemy) -> None:  # type: ignore
        self.create_item_and_schema(None, name="temp_instance_should_not_be_flushed")
        temp_instance = self.do_init_update_by_schema(
            name="the_temp_instance_not_be_flushed"
        )
        sqla_db.session.flush()
        assert temp_instance.id is None

    @pytest.mark.usefixtures("TestTableTeardown")
    def test_temp_instance_should_be_commited(self, sqla_db: SQLAlchemy) -> None:  # type: ignore
        self.create_item_and_schema(None, name="temp_instance_should_not_be_commited")
        temp_instance = self.do_init_update_by_schema(
            name="the_temp_instance_not_be_commited"
        )
        sqla_db.session.commit()
        assert temp_instance.id is None

    @pytest.mark.usefixtures("TestTableTeardown")
    def test_temp_instance_should_be_flushed_after_query(self, sqla_db: SQLAlchemy) -> None:  # type: ignore
        self.create_item_and_schema(None, name="should_not_be_flushed_after_query")
        temp_instance = self.do_init_update_by_schema(
            name="should_not_be_flushed_after_query"
        )
        query_cls = temp_instance.__class__
        query_cls.query.first()
        assert temp_instance.id is None and temp_instance not in sqla_db.session


class TestComplexParentChildrenUpdateBySchema(FixturesInjectBase):
    fixture_names = (
        "TestChildSchema",
        "TestChildTable",
        "TestParentSchema",
        "TestParentTable",
        "sqla_db",
    )
    TestChildTable: Model
    TestParentTable: Model
    TestParentSchema: Schema
    TestChildSchema: Schema
    sqla_db: Type[SQLAlchemy]

    @pytest.fixture
    def children_lst(self) -> List[Model]:
        return [
            self.TestChildTable.create(name=name) for name in ["1", "2", "3", "4", "5"]
        ]

    @pytest.fixture
    def origin_a_children_lst(self, children_lst: List[Model]) -> List[Model]:
        return children_lst[0:3]

    @pytest.fixture
    def origin_b_children_lst(self, children_lst: List[Model]) -> List[Model]:
        return children_lst[0:2]

    @pytest.fixture
    def modified_a_children_lst(self, children_lst: List[Model]) -> List[Model]:
        return [children_lst[3]]

    @pytest.fixture
    def a_children_lst_after_b_modified(self, children_lst: List[Model]) -> List[Model]:
        return [children_lst[2]]

    @pytest.fixture
    def parent_a(self, origin_a_children_lst: List[Model]) -> Any:
        parent = self.TestParentTable.create(name="A", children=origin_a_children_lst)
        return parent

    @pytest.mark.usefixtures("TestTableTeardown")
    def test_complex_update_by_ma(
        self, parent_a: Model, modified_a_children_lst: List[Model]
    ) -> None:
        temp_parent = self.TestParentTable(
            name="modified_a", children=modified_a_children_lst
        )
        pre_modified = copy(parent_a.modified)
        parent_a.update_by_ma(self.TestParentSchema, temp_parent)
        assert (
            temp_parent.id is None
            and parent_a.children == modified_a_children_lst
            and parent_a.name == "modified_a"
            and parent_a.modified > pre_modified
            and temp_parent not in self.sqla_db.session
        )

    @pytest.mark.usefixtures("TestTableTeardown")
    def test_created_new_instance_after_update_by_ma(
        self,
        parent_a: Model,
        a_children_lst_after_b_modified: List[Model],
        origin_b_children_lst: List[Model],
    ) -> None:
        temp_parent = self.TestParentTable(
            name="modified_a_complex", children=parent_a.children
        )
        parent_a.update_by_ma(self.TestParentSchema, temp_parent)
        new_parenet = self.TestParentTable.create(
            name="B", children=origin_b_children_lst
        )
        assert (
            new_parenet.id == parent_a.id + 1
            and parent_a.name == "modified_a_complex"
            and new_parenet.children == origin_b_children_lst
            and parent_a.children == a_children_lst_after_b_modified
        )
