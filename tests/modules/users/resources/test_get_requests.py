#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from smorest_sfs.modules.auth import ROLES
from tests._utils.injection import GeneralGet


class TestListView(GeneralGet):

    login_roles = [ROLES.UserManager, ROLES.User]
    listview = "User.UserListView"
    view = "User.UserView"
    item_view = "User.UserItemView"
    listkeys = {"id", "nickname"}

    fixture_names = ("flask_app_client", "flask_app", "regular_user")

    def test_get_options(self) -> None:
        self._get_options()

    @pytest.mark.parametrize("name", ["qqq", "aaa", "regular"])
    def test_get_list(self, name: str) -> None:
        self.regular_user.userinfo.update(first_name="nqqqn", last_name="baaab")
        data = self._get_list(username=name)
        assert (
            data[0].keys() > {"id", "nickname"}
            and data[0]["id"] == self.regular_user.id
            and data[0]["userinfo"]["first_name"] == "nqqqn"
            and data[0]["userinfo"]["last_name"] == "baaab"
        )

    def test_get_userinfo(self) -> None:
        resp = self._get_view("User.UserSelfView")
        assert (
            resp.status_code == 200
            and resp.json["data"]["username"] == self.regular_user.username
        )

    def test_get_item(self) -> None:
        data = self._get_item(user_id=self.regular_user.id)
        assert data.keys() >= {"id", "nickname"}
