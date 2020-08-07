#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试auth"""


from typing import TYPE_CHECKING, Tuple

import pytest
from flask import url_for

from tests._utils.launcher import Launcher
from tests._utils.uniqueue import UniqueQueue

if TYPE_CHECKING:
    from smorest_sfs.modules.users.models import User


MAIL_QUEUE: UniqueQueue[str] = UniqueQueue()


class TestAuthHelper(Launcher):
    inactive_user: "User"
    regular_user: "User"
    forget_passwd_user: "User"

    fixture_names: Tuple[str, ...] = (
        "flask_app_client",
        "inactive_user",
        "regular_user",
        "flask_app",
        "db",
    )


class TestLogin(TestAuthHelper):
    @pytest.mark.parametrize("captcha, code", [("2345", 200), ("1111", 403)])
    @pytest.mark.usefixtures("flask_app", "regular_user", "patch_code")
    def test_user_login_captcha(self, captcha: str, code: int) -> None:
        resp = self.flask_app_client.get("/api/v1/auth/captcha")
        login_data = {
            "email": "regular_user@email.com",
            "password": "regular_user_password",
            "captcha": captcha,
        }
        resp = self.flask_app_client.post("/api/v1/auth/login", json=login_data)
        assert resp.status_code == code

    @pytest.mark.usefixtures("flask_app", "regular_user", "patch_none_code")
    def test_user_login_captcha_missing_never_auth_user(self) -> None:
        login_data = {
            "email": "unexsit_user@email.com",
            "password": "none_password",
            "captcha": "1111",
        }
        self.flask_app_client.set_cookie("", "captcha_token", "")
        resp = self.flask_app_client.post("/api/v1/auth/login", json=login_data)
        assert resp.status_code == 404 and resp.json["message"] == "验证码token不存在"

    @pytest.mark.parametrize(
        "username, password, active, code",
        [
            ("inactive_user@email.com", "test", True, 403),
            ("inactive_user@email.com", "inactive_user_password", True, 200),
            ("inactive_user@email.com", "inactive_user_password", False, 403),
        ],
    )
    @pytest.mark.usefixtures("flask_app", "patch_code")
    def test_user_login_status(
        self, username: str, password: str, active: bool, code: int
    ) -> None:
        self.inactive_user.update(active=active)
        self.flask_app_client.get("/api/v1/auth/captcha")
        login_data = {
            "email": username,
            "password": password,
            "captcha": "2345",
        }
        resp = self.flask_app_client.post("/api/v1/auth/login", json=login_data)
        assert resp.status_code == code

    def test_user_expired_login(self, expired_token_headers: str) -> None:
        with self.flask_app.test_request_context():
            url = url_for("Auth.LogoutView")
            resp = self.flask_app_client.post(url, headers=expired_token_headers)
            assert resp.status_code == 402


class TestConfirm(TestAuthHelper):
    def test_user_confirm(self) -> None:
        from smorest_sfs.services.auth.confirm import generate_confirm_token

        self.regular_user.update(confirmed_at=None)
        token = generate_confirm_token(self.regular_user, "confirm")
        resp = self.flask_app_client.get("/api/v1/auth/confirm?token={}".format(token))
        after_resp = self.flask_app_client.get(
            "/api/v1/auth/confirm?token={}".format(token)
        )
        assert (
            resp.status_code == 200
            and self.regular_user.active
            and self.regular_user.confirmed_at
            and after_resp.status_code == 401
        )

    def test_login_jwt_cannot_use_at_confirm(self) -> None:
        from smorest_sfs.services.auth.auth import login_user

        token = login_user(self.regular_user)["tokens"]["access_token"]
        resp = self.flask_app_client.get("/api/v1/auth/confirm?token={}".format(token))
        assert resp.status_code == 403


class TempStore:
    value = ""


class TestForgetPasswd(TestAuthHelper):
    url: str

    fixture_names = TestAuthHelper.fixture_names + (
        "forget_passwd_user",
        "patched_mail",
    )

    @pytest.mark.parametrize(
        "email, code", [("test", 404), ("forget_passwd_user@email.com", 200)]
    )
    def test_user_forget_password_access(self, email: str, code: str) -> None:
        resp = self.flask_app_client.post(
            "/api/v1/auth/forget-password", json={"email": email}
        )
        self.forget_passwd_user.update(active=True)
        assert resp.status_code == code

    def test_reset_passwd_pre_get(self) -> None:
        TempStore.value = MAIL_QUEUE.get(timeout=3)
        resp = self.flask_app_client.get(TempStore.value)
        assert resp.status_code == 200

    def test_passwd_must_be_the_same(self) -> None:
        resp = self.flask_app_client.put(
            TempStore.value, json={"password": "1234567", "confirm_password": "123456"}
        )
        self.flask_app_client.put(
            TempStore.value, json={"password": "123456", "confirm_password": "123456"}
        )
        assert resp.status_code == 501
        assert self.forget_passwd_user.password == "123456"

    def test_passwdurl_only_disabled(self) -> None:
        resp = self.flask_app_client.get(TempStore.value)
        assert resp.status_code == 401

    def test_user_refresh_token(self) -> None:
        from smorest_sfs.services.auth.auth import login_user

        refresh_token = login_user(self.regular_user)["tokens"]["refresh_token"]
        headers = {"Authorization": "Bearer {}".format(refresh_token)}
        resp = self.flask_app_client.post("/api/v1/auth/refresh", headers=headers)
        access_token = resp.json["data"]["access_token"]

        headers = {"Authorization": "Bearer {}".format(access_token)}
        resp = self.flask_app_client.post("/api/v1/auth/logout", headers=headers)
        assert resp.status_code == 200
