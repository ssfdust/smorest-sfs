#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Dict, List, Union

from smorest_sfs.modules.roles.models import Role
from tests._utils.launcher import ModifyLauncher


class TestRoleModify(ModifyLauncher):
    items = "roles"
    view = "Role.RoleView"
    item_view = "Role.RoleItemView"
    login_roles = ["RoleManager"]
    model = Role
    edit_param_key = "role_id"

    fixture_names = (
        "flask_app_client",
        "flask_app",
        "regular_user",
        "db",
        "roles",
    )

    def test_add(
        self,
        role_args: Dict[str, Union[str, List[Dict[str, Union[str, int]]]]],
        permissions: List[Dict[str, Union[int, str]]],
    ) -> None:
        role_args["permissions"] = permissions
        data = self._add_request(role_args)
        assert data.keys() >= {"id", "name", "permissions"} and data["permissions"][
            0
        ].keys() == {"id", "name"}

    def test_delete(self) -> None:
        self._delete_request()

    def test_item_modify(self, update_permissions: List[Dict[str, Any]]) -> None:
        from smorest_sfs.modules.roles.schemas import RoleSchema

        item = self._get_modified_item()
        json = RoleSchema().dump(item)
        json.update(
            {"name": "tt", "description": "qaqa", "permissions": update_permissions}
        )
        data = self._item_modify_request(json)
        assert (
            data["name"] == "tt"
            and data["description"] == "qaqa"
            and set(i["name"] for i in data["permissions"])
            == set(i["name"] for i in update_permissions)
        )

    def test_item_delete(self) -> None:
        self._item_delete_request()
