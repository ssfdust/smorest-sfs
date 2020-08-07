from typing import TYPE_CHECKING, Type

import pytest
from sqlalchemy.orm import Session

from smorest_sfs.plugins.samanager.manager import SqlaManager

from .typings import FixtureRequest

if TYPE_CHECKING:
    from marshmallow import Schema
    from typing import Union
    from .models import Parent as Parent_, Base, Child as Child_

    MAP_UNION = Union[Type[Base], Type[Schema], Session]
    SqlaManagerT = SqlaManager[Parent_]


class _TestMaSQLAUpdaterBase:

    session: Session
    item: "Parent_"
    temp_item: "Parent_"
    manager: "SqlaManagerT"

    @pytest.fixture(autouse=True)
    def register_mappings(self, request: FixtureRequest["MAP_UNION"]) -> None:
        masqla_mappings = {
            "Parent": "ParentSchema",
            "Child": "ChildSchema",
        }
        session = request.getfixturevalue("session")
        assert isinstance(session, Session)
        self.session = session
        self.manager = SqlaManager(session)
        for model_name, schema_name in masqla_mappings.items():
            # TODO
            # 当前无法解决Union Type问题
            model = request.getfixturevalue(model_name)
            schema = request.getfixturevalue(schema_name)
            self.manager.register_mappings(model, schema)  # type: ignore

    def _setup(self, Parent: Type["Parent_"]) -> None:
        self.item = Parent(name="1", code="1")
        self.session.add(self.item)
        self.session.commit()
        self.manager.inst_with(self.item)
        self.temp_item = Parent(name="2", code="2")

    def _nest_setup(self, Parent: Type["Parent_"]) -> None:
        from .models import Child, GrandChild

        self._setup(Parent)
        self.item.children = [
            Child(name_2="a1", code_2="a1", grand_children=[GrandChild(name_3="c1")]),
            Child(name_2="a2", code_2="a2", grand_children=[GrandChild(name_3="c2")]),
        ]
        self.session.add(self.item)
        self.session.commit()

        for idx, child in enumerate(self.item.children, 1):
            child_: "Child_" = self.session.query(Child).get(child.id_)  # type: ignore
            for gchild in child_.grand_children:
                gchild.name_3 = "abc"[idx] + str(idx + 1)
            if idx > 1:
                assert isinstance(child_.grand_children, list)
                child_.grand_children.append(GrandChild(name_3="qqq"))
            assert isinstance(self.temp_item.children, list)
            self.temp_item.children.append(child_)
