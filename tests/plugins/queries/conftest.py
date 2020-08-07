from typing import TYPE_CHECKING, Any, Iterator, Type

import pytest
from mixer.backend.sqlalchemy import Mixer

if TYPE_CHECKING:
    from .models import User, Item
    from sqlalchemy.orm import Session as Session_
    from .quries import UserQuery as UserQuery_
    from .quries import UserItemQuery as UserItemQuery_
    from .quries import UserStatement as UserStatement_
    from .quries import UserJoinStatement as UserJoinStatement_
    from .quries import UserDeleteStatement as UserDeleteStatement_
    from .quries import UserInsertStatement as UserInsertStatement_
    from .quries import UserUpdateStatement as UserUpdateStatement_


@pytest.fixture(autouse=True)
def init(session: "Session_") -> Iterator[None]:
    from .models import Base, User, engine, Item
    from smorest_sfs.plugins.queries.abstract import RenderableStatementABC
    from sqlalchemy.dialects.sqlite import dialect

    registered = False
    if (
        hasattr(RenderableStatementABC, "_session")
        and getattr(RenderableStatementABC, "_session") is not None
    ):
        pre_session = getattr(RenderableStatementABC, "_session")
        pre_dialect = getattr(RenderableStatementABC, "_DIALECT")
        registered = True
    RenderableStatementABC.init_statement(session, dialect)

    mixer = Mixer(session=session)
    Base.metadata.create_all(engine)
    mixer.cycle(5).blend(
        User,
        name=mixer.sequence("name{0}"),
        nickname=mixer.sequence("nickname{0}"),
        items=mixer.sequence(
            lambda x: [Item(name="name{0}".format(3 * x + i)) for i in range(3)]
        ),
    )
    yield
    if registered:
        RenderableStatementABC.init_statement(pre_session, pre_dialect)
    Base.metadata.drop_all(engine)


@pytest.fixture
def UserModel() -> Type["User"]:
    from .models import User

    return User


@pytest.fixture
def session() -> "Session_":
    from .models import Session

    session: "Session_" = Session()
    return session


@pytest.fixture
def ItemModel() -> Type["Item"]:
    from .models import Item

    return Item


@pytest.fixture
def UserQuery() -> Type["UserQuery_"]:
    from .quries import UserQuery as UserQuery__

    return UserQuery__


@pytest.fixture
def UserItemQuery() -> Type["UserItemQuery_"]:
    from .quries import UserItemQuery as UserItemQuery__

    return UserItemQuery__


@pytest.fixture
def UserStatement() -> Type["UserStatement_"]:
    from .quries import UserStatement as UserStatement__

    return UserStatement__


@pytest.fixture
def UserJoinStatement() -> Type["UserJoinStatement_"]:
    from .quries import UserJoinStatement as UserJoinStatement__

    return UserJoinStatement__


@pytest.fixture
def UserDeleteStatement() -> Type["UserDeleteStatement_"]:
    from .quries import UserDeleteStatement as UserDeleteStatement__

    return UserDeleteStatement__


@pytest.fixture
def UserInsertStatement() -> Type["UserInsertStatement_"]:
    from .quries import UserInsertStatement as UserInsertStatement__

    return UserInsertStatement__


@pytest.fixture
def UserUpdateStatement() -> Type["UserUpdateStatement_"]:
    from .quries import UserUpdateStatement as UserUpdateStatement__

    return UserUpdateStatement__


@pytest.fixture
def query(request: Any) -> Type[object]:
    UserQuery: Type["UserQuery_"] = request.getfixturevalue("UserQuery")
    UserItemQuery: Type["UserItemQuery_"] = request.getfixturevalue("UserItemQuery")
    index: int = request.param
    return [UserQuery, UserItemQuery][index - 1]


@pytest.fixture
def sql(request: Any) -> Type[object]:
    index: int = request.param
    UserStatement: Type["UserStatement_"] = request.getfixturevalue("UserStatement")
    UserJoinStatement: Type["UserJoinStatement_"] = request.getfixturevalue(
        "UserJoinStatement"
    )
    UserDeleteStatement: Type["UserDeleteStatement_"] = request.getfixturevalue(
        "UserDeleteStatement"
    )
    UserInsertStatement: Type["UserInsertStatement_"] = request.getfixturevalue(
        "UserInsertStatement"
    )
    UserUpdateStatement: Type["UserUpdateStatement_"] = request.getfixturevalue(
        "UserUpdateStatement"
    )
    return [
        UserStatement,
        UserJoinStatement,
        UserDeleteStatement,
        UserInsertStatement,
        UserUpdateStatement,
    ][index - 1]


@pytest.fixture
def res_txt(request: Any) -> str:
    idx: int = request.param[1] - 1
    fname: str = request.param[0]
    with open(f"tests/plugins/queries/data/{fname}.txt", "r") as f:
        text = f.read()
        return text.split("---")[idx].strip()


@pytest.fixture
def delete_items(session: "Session_") -> None:
    session.execute("delete from users where id > 1")
    session.execute("delete from items where id > 1")
