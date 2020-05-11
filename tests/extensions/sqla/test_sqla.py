"""测试sqla"""

from typing import Callable, List, Type

import pytest
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema
from pendulum import datetime
from werkzeug.exceptions import NotFound

from smorest_sfs.extensions.sqla import Model
from tests._utils.injection import FixturesInjectBase


class ItemsFixtureBase(FixturesInjectBase):
    TestCRUDTable: Type[Model]
    TestChildTable: Type[Model]

    @pytest.fixture
    def temp_item_generator(self) -> Callable[[Type[Model]], List[Model]]:
        def temp_item_generator_func(cls: Type[Model]) -> List[Model]:
            return [
                cls.create(
                    id=idx,
                    name=name,
                    created=datetime(1994, 9, 11, 8, 20),
                    modified=datetime(1994, 9, 11, 8, 20),
                )
                for idx, name in enumerate(["aaabbb", "bbbbcccc", "bbcccc", "bbc"], 1)
            ]

        return temp_item_generator_func

    @pytest.fixture
    def crud_items(
        self, temp_item_generator: Callable[[Type[Model]], List[Model]]
    ) -> List[Model]:
        return temp_item_generator(self.TestCRUDTable)

    @pytest.fixture
    def child_items(
        self, temp_item_generator: Callable[[Type[Model]], List[Model]]
    ) -> List[Model]:
        return temp_item_generator(self.TestChildTable)


class TestBaseQuery(ItemsFixtureBase):
    fixture_names = ("TestCRUDTable",)

    @pytest.mark.usefixtures("TestTableTeardown")
    def test_soft_delete(self, crud_items: List[Model]) -> None:
        pre_cnt = self.TestCRUDTable.query.count()
        deleted_one = crud_items[0]
        deleted_one.delete()

        direct_get_by_id = self.TestCRUDTable.query.filter_by(id=deleted_one.id).first()
        with_deleted_get_by_id = self.TestCRUDTable.query.with_deleted().get(
            deleted_one.id
        )
        cur_cnt = self.TestCRUDTable.query.count()

        assert (
            direct_get_by_id is None
            and with_deleted_get_by_id is deleted_one
            and cur_cnt == pre_cnt - 1
        )

    def test_surrogatepk_keys(self) -> None:
        for key in ["id", "deleted", "modified", "created"]:
            assert hasattr(self.TestCRUDTable, key)

    @pytest.mark.usefixtures("TestTableTeardown")
    def test_surrogatepk_defaults(self) -> None:
        item = self.TestCRUDTable.create(name="test_defaults")
        assert (
            item.id is not None
            and item.deleted is False
            and item.created.strftime("%Y-%m-%d %H:%M:%S")
            and item.modified.strftime("%Y-%m-%d %H:%M:%S")
        )


class TestBaseRUDByID(ItemsFixtureBase):
    TestParentTable: Type[Model]
    TestParentSchema: Type[Schema]

    fixture_names = ("TestCRUDTable", "TestParentSchema", "TestParentTable")

    @pytest.mark.usefixtures("TestTableTeardown")
    def test_base_read_by_id(self, crud_items: List[Model]) -> None:
        item = crud_items[0]
        assert self.TestCRUDTable.get_by_id(item.id) == item

    @pytest.mark.usefixtures("TestTableTeardown")
    def test_base_delete_by_id(self, crud_items: List[Model]) -> None:
        item = crud_items[0]
        self.TestCRUDTable.delete_by_id(item.id)
        with pytest.raises(NotFound):
            self.TestCRUDTable.get_by_id(item.id)

    @pytest.mark.usefixtures("TestTableTeardown")
    def test_base_delete_by_idlst(self, crud_items: List[Model]) -> None:
        items = crud_items[0:-1]
        idlst = [item.id for item in items]
        self.TestCRUDTable.delete_by_ids(idlst)
        for item_id in idlst:
            with pytest.raises(NotFound):
                self.TestCRUDTable.get_by_id(item_id)

    def test_base_update_by_id(self, sqla_db: SQLAlchemy) -> None:
        item = self.TestParentTable.create(name="base_update_by_id")
        temp_item = self.TestParentTable(name="test_update_by_id")
        self.TestParentTable.update_by_id(item.id, self.TestParentSchema, temp_item)
        assert temp_item not in sqla_db.session and item.name == "test_update_by_id"
