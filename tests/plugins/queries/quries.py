from typing import Tuple, TYPE_CHECKING

from sqlalchemy import delete, insert, join, select, update
from sqlalchemy.engine import RowProxy

from smorest_sfs.plugins.queries.query import SAQuery
from smorest_sfs.plugins.queries.statement import SAStatement
from tests.plugins.queries.models import Item, User

if TYPE_CHECKING:
    from sqlalchemy.orm import Query


TUPLEQ = Tuple[User, Item]


class UserQuery(SAQuery["Query[User]", User, User]):
    def __init__(self) -> None:
        self._query = self._session.query(User)


class UserItemQuery(SAQuery["Query[TUPLEQ]", TUPLEQ, User]):
    def __init__(self) -> None:
        self._query = self._session.query(User, Item).join(Item, User.id == Item.uid)


class UserStatement(SAStatement[select, str]):
    def __init__(self) -> None:
        self._sa_sql = select([User.name, User.nickname])


class UserJoinStatement(SAStatement[select, RowProxy]):
    def __init__(self) -> None:
        self._sa_sql = select(
            [User.name, User.nickname, Item.name.label("Itemname")]
        ).select_from(join(User.__table__, Item.__table__, Item.uid == User.id))


class UserDeleteStatement(SAStatement[delete, None]):
    def __init__(self) -> None:
        self._sa_sql = delete(User.__table__)


class UserInsertStatement(SAStatement[insert, None]):
    def __init__(self) -> None:
        self._sa_sql = insert(User.__table__).values((100, "test1", "test2"))


class UserUpdateStatement(SAStatement[update, None]):
    def __init__(self) -> None:
        self._sa_sql = update(User.__table__).where(User.id == 1).values(name="updated")
