from typing import TYPE_CHECKING, Iterator, List

import pytest

from tests.typings import INS_HELPER

if TYPE_CHECKING:
    from smorest_sfs.modules.users.models import User


@pytest.fixture
def users(temp_db_instance_helper: INS_HELPER["User"],) -> Iterator[List["User"]]:
    from smorest_sfs.modules.users.models import User, UserInfo
    from smorest_sfs.modules.groups.models import Group
    from smorest_sfs.modules.roles.models import Role

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
