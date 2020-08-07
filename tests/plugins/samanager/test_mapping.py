from inspect import getmodule
from typing import TYPE_CHECKING, Type

from sqlalchemy.orm import Session

from smorest_sfs.plugins.samanager.manager import SqlaManager

if TYPE_CHECKING:
    from marshmallow import Schema
    from typing import Union
    from .models import Parent as Parent_, Child as Child_, Base
    from .schemas import (
        ParentSchema as ParentSchema_,
        ChildSchema as ChildSchema_,
    )

    MAP_UNION = Union[Type[Base], Type[Schema], Session]
    SqlaManagerT = SqlaManager[Base]


class TestMaSQLAMapping:
    def test_register(
        self,
        Parent: Type["Parent_"],
        ParentSchema: Type["ParentSchema_"],
        session: Session,
    ) -> None:
        manager: "SqlaManagerT" = SqlaManager(session)
        manager.register_mappings(Parent, ParentSchema)
        mappings = manager.get_mappings()
        assert mappings[Parent] == ParentSchema

    def test_register_str(
        self,
        Child: Type["Child_"],
        ChildSchema: Type["ChildSchema_"],
        session: Session,
    ) -> None:
        manager: "SqlaManagerT" = SqlaManager(session)
        model_module: str = getattr(getmodule(Child), "__name__")
        schema_module: str = getattr(getmodule(ChildSchema), "__name__")
        sample_two_str = f"{model_module}.Child"
        sample_two_schema_str = f"{schema_module}.ChildSchema"
        manager.register_mappings(sample_two_str, sample_two_schema_str)
        mappings = manager.get_mappings()
        assert mappings[Child] == ChildSchema
