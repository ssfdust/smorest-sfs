#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING, Any, List, Optional, Tuple

import pytest
from _pytest.monkeypatch import MonkeyPatch
from freezegun import freeze_time

from tests._utils.uniqueue import UniqueQueue

if TYPE_CHECKING:
    from smorest_sfs.modules.users.models import User

SENDED: UniqueQueue[str] = UniqueQueue()


@pytest.fixture
def patch_code(monkeypatch: MonkeyPatch) -> None:
    """为编码补丁"""
    from smorest_sfs.extensions.storage import redis_store

    def fake_code(key: str) -> Optional[bytes]:
        return b"2345"

    monkeypatch.setattr(redis_store, "get", fake_code)


@pytest.fixture
def patch_none_code(monkeypatch: MonkeyPatch) -> None:
    """为编码补丁"""
    from smorest_sfs.extensions.storage import redis_store

    def none_code(key: str) -> None:
        return None

    monkeypatch.setattr(redis_store, "get", none_code)


@pytest.fixture
def permissions() -> List[str]:
    from smorest_sfs.modules.auth.permissions import PERMISSIONS

    return [PERMISSIONS.UserEdit, PERMISSIONS.GroupQuery, PERMISSIONS.GroupAdd]


def fake_send(self: Any) -> None:
    SENDED.put(self.content["url"])


@pytest.fixture
def patched_mail(monkeypatch: MonkeyPatch) -> None:
    from smorest_sfs.services.mail import PasswdMailSender

    monkeypatch.setattr(PasswdMailSender, "send", fake_send)


@pytest.fixture
@freeze_time("1990-01-01 00:00:00")
def expired_token_headers(regular_user: "User") -> Tuple[Tuple[str, str]]:
    from smorest_sfs.services.auth.auth import login_user

    access_token = login_user(regular_user)["tokens"]["access_token"]
    expired_headers = (("Authorization", "Bearer {token}".format(token=access_token)),)
    return expired_headers
