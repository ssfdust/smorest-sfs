#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Dict, List, Union

import pytest
from flask import url_for

from smorest_sfs.modules.auth import ROLES
from smorest_sfs.modules.roles.models import Role
from smorest_sfs.modules.users.models import User
from tests._utils.injection import GeneralModify


class TestUserModify(GeneralModify):

    roles: List[Role]
    regular_user: User
    forget_passwd_user: User
    inactive_user: User
    guest_user: User
    items = "user_items"
    delete_param_key = "user_id"
    item_view = "User.UserItemView"
    view = "User.UserView"
    login_roles = [ROLES.UserManager]
    role_dict: List[Dict[str, Union[str, int]]]

    fixture_names = (
        "flask_app_client",
        "flask_app",
        "regular_user",
        "forget_passwd_user",
        "inactive_user",
        "guest_user",
        "fake_roles",
        "fake_groups",
        "user_items",
    )
    data = {
        "phonenum": "12121212",
        "username": "guest_user",
        "confirmed_at": None,
        "email": "66666",
        "password": "7777",
        "active": False,
        "userinfo": {"first_name": "tt", "last_name": "qaqa", "sex": 2, "age": 13,},
    }

    @pytest.fixture(autouse=True)
    def inject_roles(self) -> None:
        setattr(
            self,
            "roles",
            Role.where(name__in=[ROLES.GroupManager, ROLES.EmailTemplateManager]).all(),
        )
        setattr(self, "role_dict", [{"id": r.id, "name": r.name} for r in self.roles])

    def _get_data(self, **kwargs: Any) -> Dict[str, Any]:
        data = self.data.copy()
        data.update(**kwargs)
        return data

    def test_delete(self) -> None:
        _, users = self._delete_request()
        for user in users:
            assert not user.roles and not user.groups

    def test_register(self) -> None:
        with self.flask_app.test_request_context():
            data = self._get_data(
                username="fake_user", email="fake_user@email.com", phonenum="1234"
            )
            url = url_for("User.UserRegisterView")
            resp = self.flask_app_client.put(url, json=data)
            fake_user = User.get_by_keyword("fake_user")
            assert (
                resp.status_code == 200
                and {r.name for r in fake_user.roles} >= {"a", "User"}
                and {g.name for g in fake_user.groups} >= {"默认用户组"}
            )

    def test_modify_userinfo(self) -> None:
        with self.flask_app_client.login(self.regular_user, [ROLES.User]) as client:
            with self.flask_app.test_request_context():
                url = url_for("User.UserSelfView")
                data = self._get_data(
                    username="asasarqwrasdasd",
                    email=self.regular_user.email,
                    phonenum="2345",
                )
                client.patch(url, json=data)
                assert (
                    self.regular_user.phonenum == "2345"
                    and self.regular_user.username != "asasarqwrasdasd"
                )

    def test_item_modify(self) -> None:
        with self.flask_app_client.login(
            self.guest_user, [ROLES.UserManager]
        ) as client:
            with self.flask_app.test_request_context():
                url = url_for("User.UserItemView", user_id=self.guest_user.id)
                data = self._get_data(
                    username=self.guest_user.username,
                    email=self.guest_user.email,
                    phonenum="9527",
                    roles=[{"id": r.id, "name": r.name} for r in self.roles],
                )
                resp = client.put(url, json=data)
                assert (
                    resp.status_code == 200
                    and self.guest_user.phonenum == "9527"
                    and self.guest_user.nickname == "tt qaqa"
                    and self.guest_user.userinfo.sex_label == "女"
                    and self.guest_user.userinfo.age == 13
                    and set(self.guest_user.roles) >= set(r for r in self.roles)
                )

    def test_item_delete(self) -> None:
        _, user = self._item_delete_request()
        assert user.groups == [] and user.roles == []
