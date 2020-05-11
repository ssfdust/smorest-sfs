from typing import Any, Callable, Iterator, Tuple, Type

import pytest
from flask import Flask
from marshmallow import Schema

from smorest_sfs.modules.groups.models import Group
from smorest_sfs.modules.roles.models import Role
from smorest_sfs.modules.users.models import User, UserInfo


@pytest.fixture
def UserSchema(flask_app: Flask) -> Type[Schema]:
    # pylint: disable=W0621, W0613
    from smorest_sfs.modules.users.schemas import UserSchema

    return UserSchema


@pytest.fixture
def user_items(
    temp_db_instance_helper: Callable[..., Iterator[Any]],
) -> Iterator[Tuple[User, User, User]]:
    for _ in temp_db_instance_helper(
        User(
            username="test_user_1",
            password="test_user_1",
            userinfo=UserInfo(),
            roles=Role.where(name__in=["c", "f"]).all(),
            groups=Group.where(name="group_with_c_f").all(),
        ),
        User(
            username="test_user_2",
            password="test_user_2",
            userinfo=UserInfo(),
            roles=Role.where(name__in=["a", "b", "c"]).all(),
            groups=Group.where(name="group_with_a_b_c").all(),
        ),
        User(
            username="test_user_3",
            password="test_user_3",
            userinfo=UserInfo(),
            roles=Role.where(name__in=["f"]).all(),
            groups=Group.where(name="group_with_f").all(),
        ),
    ):
        yield _
