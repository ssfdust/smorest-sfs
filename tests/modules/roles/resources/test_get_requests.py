#!/usr/bin/env python
# -*- coding: utf-8 -*-
from smorest_sfs.modules.auth import ROLES
from tests._utils.injection import GeneralGet


class TestListView(GeneralGet):

    fixture_names = ("flask_app_client", "flask_app", "regular_user")
    item_view = "Role.RoleItemView"
    listview = "Role.RoleListView"
    view = "Role.RoleView"
    login_roles = [ROLES.RoleManager]

    def test_get_options(self) -> None:
        self._get_options()

    def test_get_list(self) -> None:
        data = self._get_list(name="e")
        assert data[0].keys() >= {
            "id",
            "name",
            "permissions",
            "user_default",
            "group_default",
        } and data[0]["permissions"][0].keys() == {"id", "name"}

    def test_get_item(self) -> None:
        data = self._get_item(role_id=1)
        assert data.keys() > {"id", "name", "created", "modified", "deleted"} and data[
            "permissions"
        ][0].keys() >= {"id", "name"}
