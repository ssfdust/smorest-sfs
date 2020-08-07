"""配置MaSqla插件tests"""

from typing import TYPE_CHECKING, Type

import pytest
from sqlalchemy.orm import Session

if TYPE_CHECKING:
    from .models import Parent as Parent_, Child as Child_
    from .schemas import (
        ParentSchema as ParentSchema_,
        ChildSchema as ChildSchema_,
        NameOnlySchema as NameOnlySchema_,
    )


@pytest.fixture
def session() -> Session:
    from .models import session as session__

    return session__


@pytest.fixture
def Parent() -> Type["Parent_"]:
    from .models import Parent as Parent__

    return Parent__


@pytest.fixture
def Child() -> Type["Child_"]:
    from .models import Child as Child__

    return Child__


@pytest.fixture
def ParentSchema() -> Type["ParentSchema_"]:
    from .schemas import ParentSchema as ParentSchema__

    return ParentSchema__


@pytest.fixture
def ChildSchema() -> Type["ChildSchema_"]:
    from .schemas import ChildSchema as ChildSchema__

    return ChildSchema__


@pytest.fixture
def NameOnlySchema() -> Type["NameOnlySchema_"]:
    from .schemas import NameOnlySchema as NameOnlySchema__

    return NameOnlySchema__
