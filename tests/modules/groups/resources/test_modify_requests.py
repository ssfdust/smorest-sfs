#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests._utils.launcher import ModifyLauncher


class TestGroupModify(ModifyLauncher):
    items = "groups"
    fixture_names = ("flask_app_client", "flask_app", "regular_user", "db",) + (items,)
    view = "Group.GroupView"
    item_view = "Group.GroupItemView"
    login_roles = ["GroupManager"]
    edit_param_key = "group_id"

    def test_add(self) -> None:
        json = {
            "name": "test_add_group",
            "description": "",
            "default": False,
            "roles": [],
        }
        data = self._add_request(json)
        assert data.keys() > {"id", "name"}

    def test_item_modify(self) -> None:
        data = self._item_modify_request(
            json={
                "name": "renamed",
                "description": "renamed",
                "default": True,
                "roles": [],
            }
        )
        assert (
            data["name"] == "renamed"
            and data["description"] == "renamed"
            and data["default"] is True
            and data["roles"] == []
        )

    def test_item_delete(self) -> None:
        self._item_delete_request()
