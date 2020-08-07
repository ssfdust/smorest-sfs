from typing import TYPE_CHECKING, Iterator, List

import pytest
from flask import Flask
from mixer.backend.sqlalchemy import Mixer as SqlaMixer

from tests.typings import INS_HELPER

if TYPE_CHECKING:
    from smorest_sfs.modules.groups.models import Group


@pytest.fixture
def groups(
    flask_app: Flask,
    temp_db_instance_helper: INS_HELPER["Group"],
    sqla_mixer: SqlaMixer,
) -> Iterator[List["Group"]]:
    from smorest_sfs.modules.groups.models import Group

    for _ in temp_db_instance_helper(
        *sqla_mixer.cycle(3).blend(Group, name=sqla_mixer.sequence("{0}_test_name"))
    ):
        yield _
