#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Dict, List, Union

import pytest

from smorest_sfs.modules.roles.models import ROLES, Role
from tests._utils.helpers import param_helper
from tests._utils.injection import GeneralModify


class TestRoleModify(GeneralModify):
    items = "role_items"
    view = "Role.RoleView"
    item_view = "Role.RoleItemView"
    login_roles = [ROLES.RoleManager]
    model = Role
    schema = "RoleSchema"
    delete_param_key = "role_id"

    fixture_names = (
        "flask_app_client",
        "flask_app",
        "regular_user",
        "db",
        "role_items",
    )

    @pytest.mark.parametrize("json", param_helper(name="role", description="desc"))
    def test_add(
        self,
        json: Dict[str, Union[str, List[Dict[str, Union[str, int]]]]],
        permissions: List[Dict[str, Union[int, str]]],
    ) -> None:
        json["permissions"] = permissions
        data = self._add_request(json)
        assert data.keys() >= {"id", "name", "permissions"} and data["permissions"][
            0
        ].keys() == {"id", "name"}

    def test_delete(self) -> None:
        self._delete_request()

    def test_item_modify(self, update_permissions: List[Dict[str, Any]]) -> None:
        json = self._get_dumped_modified_item()
        json.update(
            {"name": "tt", "description": "qaqa", "permissions": update_permissions,}
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
