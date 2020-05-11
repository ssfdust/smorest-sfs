#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Dict, List, Set

import pytest

from smorest_sfs.modules.auth import ROLES
from smorest_sfs.modules.groups.models import Group
from smorest_sfs.modules.roles.models import Role
from smorest_sfs.modules.users.models import User
from tests._utils.injection import GeneralModify


def get_roles(res: Dict[str, Any]) -> Set[str]:
    return set(role["name"] for role in res["roles"])


class TestUserGroupManager(GeneralModify):
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
    schema = "UserSchema"
    item_view = "User.UserItemView"
    login_roles = [ROLES.UserManager]
    delete_param_key = "user_id"
    data = {
        "phonenum": "12121212",
        "username": "fake_1",
        "email": "66666",
        "confirmed_at": "2020-05-06 00:00:00",
        "active": True,
        "userinfo": {"first_name": "tt", "last_name": "qaqa", "sex": 2, "age": 13,},
    }

    def _modify_user_groups(self, indexlst: List[int], roles: Set[str]) -> User:
        item = self._get_modified_item()
        print(item.roles)
        groups = [
            {"id": self.fake_groups[index].id, "name": self.fake_groups[index].name}
            for index in indexlst
        ]
        data = self.data.copy()
        data["groups"] = groups  # type: ignore
        data["roles"] = [{"id": r.id, "name": r.name} for r in item.roles]
        res = self._item_modify_request(data)
        assert get_roles(res) == roles
        return item

    @pytest.mark.parametrize(
        "group_idxlst, role_idlst",
        [
            ([0], ["f", "a", "c", "b"]),
            ([2], ["e", "d", "c", "a", "f"]),
            ([0, 2], ["a", "b", "c", "f", "d", "e"]),
        ],
    )
    def test_simple_group_modify(
        self, group_idxlst: List[int], role_idlst: List[str]
    ) -> None:
        self._modify_user_groups(group_idxlst, set(role_idlst))

    def test_complex_group_modify(self) -> None:
        for group_idxlst, role_idlst in [
            ([0], ["f", "a", "c", "b"]),
            ([0, 1, 2], ["a", "b", "c", "f", "d", "e"]),
            ([0, 1], ["a", "b", "c", "f"]),
            ([2], ["e", "d", "c"]),
            ([1, 3], ["f", "c"]),
        ]:
            self._modify_user_groups(group_idxlst, set(role_idlst))

    def _get_modified_item(self) -> User:
        return self.fake_users[0]
