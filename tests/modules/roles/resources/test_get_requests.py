#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict

import pytest

from tests._utils.launcher import AccessLauncher


class TestListView(AccessLauncher):

    fixture_names = ("flask_app_client", "flask_app", "regular_user", "test_role")
    item_view = "Role.RoleItemView"
    listview = "Role.RoleListView"
    view = "Role.RoleView"
    login_roles = ["RoleManager"]

    def test_get_options(self) -> None:
        self._get_options()

    @pytest.mark.parametrize("params, cnt", [({"name": "1"}, 1), ({"name": "name"}, 3)])
    def test_get_list(self, params: Dict[str, str], cnt: int) -> None:
        data = self._get_list(**params)
        if data:
            assert data[0].keys() >= {
                "id",
                "name",
                "permissions",
                "user_default",
                "group_default",
            } and data[0]["permissions"][0].keys() == {"id", "name"}
        assert len(data) == cnt

    def test_get_item(self) -> None:
        data = self._get_item(role_id=1)
        assert data.keys() > {"id", "name", "created", "modified", "deleted"} and data[
            "permissions"
        ][0].keys() >= {"id", "name"}
