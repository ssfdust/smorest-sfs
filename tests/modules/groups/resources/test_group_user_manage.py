#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import reduce
from typing import TYPE_CHECKING, Any, Dict, List, Set

import pytest
from deepdiff import DeepDiff

from tests._utils.launcher import ModifyLauncher

if TYPE_CHECKING:
    from smorest_sfs.modules.groups.models import Group
    from smorest_sfs.modules.roles.models import Role
    from smorest_sfs.modules.users.models import User


def get_roles(res: Dict[str, Any]) -> Set[str]:
    uids = [i["id"] for i in res["users"]]
    roles_iter = iter(
        set(r.name for r in user.roles) for user in User.where(id__in=uids).all()
    )
    return reduce(lambda x, y: x & y, roles_iter)


class TestGroupRoleManager(ModifyLauncher):
    """
    group_1: fake_2
    """

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
    item_view = "Group.GroupUserView"
    login_roles = ["GroupManager"]
    edit_param_key = "group_id"
    data = {"users": [{"id": 1, "username": "fake_"}]}

    def _modify_group(self, indexlst: List[int]) -> DeepDiff:
        from smorest_sfs.modules.users.schemas import UserSchema

        user_schema = UserSchema(many=True, only=["roles", "id_", "username"])
        pre_user_info = user_schema.dump(self.fake_users)
        users = [
            {
                "id": self.fake_users[index].id_,
                "username": self.fake_users[index].username,
            }
            for index in indexlst
        ]
        data = self.data.copy()
        data["users"] = users
        self._item_modify_request(data)
        current_user_info = user_schema.dump(self.fake_users)
        diff = DeepDiff(pre_user_info, current_user_info)
        for i in diff:
            for j in diff[i]:
                diff[i][j].pop("id")
        return diff

    @pytest.mark.parametrize(
        "user_idxlst, diff",
        [
            (
                [4, 5],
                {
                    "iterable_item_added": {
                        "root[4]['roles'][0]": {"name": "a"},
                        "root[4]['roles'][1]": {"name": "b"},
                        "root[4]['roles'][2]": {"name": "c"},
                        "root[5]['roles'][0]": {"name": "a"},
                        "root[5]['roles'][1]": {"name": "b"},
                        "root[5]['roles'][2]": {"name": "c"},
                    },
                    "iterable_item_removed": {
                        "root[1]['roles'][0]": {"name": "a"},
                        "root[1]['roles'][1]": {"name": "b"},
                        "root[1]['roles'][2]": {"name": "c"},
                    },
                },
            ),
            (
                [1, 4, 5],
                {
                    "iterable_item_added": {
                        "root[4]['roles'][0]": {"name": "a"},
                        "root[4]['roles'][1]": {"name": "b"},
                        "root[4]['roles'][2]": {"name": "c"},
                        "root[5]['roles'][0]": {"name": "a"},
                        "root[5]['roles'][1]": {"name": "b"},
                        "root[5]['roles'][2]": {"name": "c"},
                    },
                },
            ),
            ([1], {}),
        ],
    )
    def test_simple_group_modify(
        self, user_idxlst: List[int], diff: Dict[str, Any]
    ) -> None:
        assert diff == self._modify_group(user_idxlst)

    def _get_modified_item(self) -> "Group":
        return self.fake_groups[0]
