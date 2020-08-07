"""测试SqlaManager"""
from typing import TYPE_CHECKING, Type

import pytest

from ._updater_base import _TestMaSQLAUpdaterBase

if TYPE_CHECKING:
    from .models import Parent as Parent_
    from .schemas import NameOnlySchema as NameOnlySchema_


class TestMaSQLAUpdater(_TestMaSQLAUpdaterBase):
    def test_update_with_custom_schema(
        self, Parent: Type["Parent_"], NameOnlySchema: Type["NameOnlySchema_"],
    ) -> None:
        self._setup(Parent)

        self.manager.update_with(self.temp_item, NameOnlySchema)
        assert (
            self.item.code == "1"
            and self.item.name == "2"
            and self.temp_item not in self.session
            and self.temp_item.name is None
            and self.temp_item.code is not None
            and self.temp_item.id_ is None
        )

    def test_update_with_custom_schema_instance(
        self, Parent: Type["Parent_"], NameOnlySchema: Type["NameOnlySchema_"],
    ) -> None:
        self._setup(Parent)

        self.manager.update_with(self.temp_item, NameOnlySchema())
        assert (
            self.item.code == "1"
            and self.item.name == "2"
            and self.temp_item not in self.session
            and self.temp_item.name is None
            and self.temp_item.code is not None
            and self.temp_item.id_ is None
        )

    def test_update_with(self, Parent: Type["Parent_"],) -> None:
        self._setup(Parent)

        self.manager.update_with(self.temp_item)
        assert (
            self.item.code == "2"
            and self.item.name == "2"
            and self.temp_item not in self.session
            and self.temp_item.name is None
            and self.temp_item.code is None
            and self.temp_item.id_ is None
        )

    def test_nested_update_with(self, Parent: Type["Parent_"],) -> None:
        self._nest_setup(Parent)
        self.manager.update_with(self.temp_item)
        assert (
            set(
                gchild.name_3
                for child in self.item.children
                for gchild in child.grand_children
            )
            == set(["qqq", "b2", "c3"])
            and self.temp_item.id_ is None
            and self.temp_item not in self.session
        )


class TestMaSQLAError(_TestMaSQLAUpdaterBase):
    def test_update_with_the_same(self, Parent: Type["Parent_"],) -> None:
        self._setup(Parent)

        with pytest.raises(ValueError):
            self.manager.update_with(self.item)

    def test_update_with_in_session(self, Parent: Type["Parent_"],) -> None:
        self._setup(Parent)

        self.session.add(self.temp_item)

        with pytest.raises(RuntimeError):
            self.manager.update_with(self.temp_item)
