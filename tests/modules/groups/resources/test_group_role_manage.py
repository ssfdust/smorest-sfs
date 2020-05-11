#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Any, Dict, List, Set
from functools import reduce

import pytest

from smorest_sfs.modules.auth import ROLES
from smorest_sfs.modules.groups.models import Group
from smorest_sfs.modules.roles.models import Role
from smorest_sfs.modules.users.models import User
from tests._utils.injection import GeneralModify


def get_roles(res: Dict[str, Any]) -> Set[str]:
    uids = [i["id"] for i in res["users"]]
    roles_iter = iter(set(r.name for r in user.roles) for user in User.where(id__in=uids).all())
    return reduce(lambda x, y: x & y, roles_iter)


class TestGroupRoleManager(GeneralModify):
    fake_roles: List[Role]
    fake_groups: List[Group]
    fake_users: List[User]

    fixture_names = (
        "flask_app_client",
        "flask_app",
        "regular_user",
        "fake_roles",
        "fake_groups",
        "fake_users",
    )
    schema = "GroupSchema"
    item_view = "Group.GroupItemView"
    login_roles = [ROLES.GroupManager]
    delete_param_key = "group_id"
    data = {
        "name": "temp_group",
        "description": "",
        "default": False,
        "roles": []
    }

    def _modify_group(self, indexlst: List[int], roles: Set[str]) -> Group:
        self._set_up_user()
        item = self._get_modified_item()
        _roles = [
            {"id": self.fake_roles[index].id, "name": self.fake_roles[index].name}
            for index in indexlst
        ]
        data = self.data.copy()
        data["roles"] = _roles  # type: ignore
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
            ([0, 1, 2, 3], ["a", 'b', 'c', 'd']),
            ([0, 3], ["a", 'd']),
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

    def _get_modified_item(self) -> Group:
        return self.fake_groups[0]
