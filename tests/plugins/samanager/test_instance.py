from typing import TYPE_CHECKING, Type

from sqlalchemy.orm import Session
from sqlalchemy_utils import naturally_equivalent

from smorest_sfs.plugins.samanager.manager import SqlaManager

if TYPE_CHECKING:
    from .models import Parent as Parent_


def test_pk_with(Parent: Type["Parent_"], session: Session) -> None:
    manager: SqlaManager["Parent_"] = SqlaManager(session)

    parent = Parent(name="pk_parent")
    session.add(parent)
    session.commit()

    last_id = parent.id_
    session.expunge_all()

    manager.pk_with(Parent, last_id)

    assert (
        last_id == manager.instance().id_
        and naturally_equivalent(parent, manager.instance())
        and parent is not manager.instance()
    )
