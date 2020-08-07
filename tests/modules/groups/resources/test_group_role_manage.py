#!/usr/bin/env python
# -*- coding: utf-8 -*-


from functools import reduce
from typing import TYPE_CHECKING, Any, Dict, List, Set

import pytest

from tests._utils.launcher import ModifyLauncher

if TYPE_CHECKING:
    from smorest_sfs.modules.groups.models import Group
    from smorest_sfs.modules.roles.models import Role
    from smorest_sfs.modules.users.models import User


def get_roles(res: Dict[str, Any]) -> Set[str]:
    from smorest_sfs.modules.users.models import User

    uids = [i["id"] for i in res["users"]]
    roles_iter = iter(  # type: ignore
        set(r.name for r in user.roles) for user in User.id_in(uids).all()
    )
    return reduce(lambda x, y: x & y, roles_iter)


class TestGroupRoleManager(ModifyLauncher):
    fake_roles: List["Role"]
    fake_groups: List["Group"]
    fake_users: List["User"]

    fixture_names = (
        "flask_app_client",
        "flask_app",
        "regular_user",
        "fake_roles",
        "fake_groups",
        "fake_users",
    )
    item_view = "Group.GroupItemView"
    login_roles = ["GroupManager"]
    edit_param_key = "group_id"
    data = {"name": "temp_group", "description": "", "default": False, "roles": []}

    def _modify_group(self, indexlst: List[int], roles: Set[str]) -> "Group":
        self._set_up_user()
        item = self._get_modified_item()
        _roles = [
            {"id": self.fake_roles[index].id_, "name": self.fake_roles[index].name}
            for index in indexlst
        ]
        data = self.data.copy()
        data["roles"] = _roles
        res = self._item_modify_request(data)
        assert get_roles(res) >= roles
        return item

    def _set_up_user(self) -> None:
        self.fake_users[0].groups = [self.fake_groups[0]]
        self.fake_users[0].roles = list(self.fake_roles[:3])
        self.fake_users[0].save()

    @pytest.mark.parametrize(
        "group_idxlst, role_idlst",
        [
            ([0], ["a"]),
            ([0, 1, 2, 3], ["a", "b", "c", "d"]),
            ([0, 3], ["a", "d"]),
            ([], []),
        ],
    )
    def test_simple_group_modify(
        self, group_idxlst: List[int], role_idlst: List[str]
    ) -> None:
        self._modify_group(group_idxlst, set(role_idlst))

    def test_complex_group_modify(self) -> None:
        for group_idxlst, role_idlst in [
            ([0], ["a"]),
            ([0, 1, 2], ["a", "b", "c"]),
            ([0, 1], ["a", "b"]),
            ([2], ["c"]),
            ([1, 3], ["b", "d"]),
        ]:
            self._modify_group(group_idxlst, set(role_idlst))

    def _get_modified_item(self) -> "Group":
        return self.fake_groups[0]
