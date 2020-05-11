#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Union

import pytest

from smorest_sfs.modules.users.models import User, UserInfo
from tests._utils.injection import FixturesInjectBase


@pytest.mark.parametrize("key", ["12345678", "regular_user", "regular_user@email.com"])
@pytest.mark.usefixtures("flask_app")
def test_get_by_unique(regular_user: User, key: str) -> None:
    user = User.get_by_keyword(key)
    assert user is regular_user


class TestUserInfo(FixturesInjectBase):
    fixture_names = ("flask_app", "regular_user", "temp_db_instance_helper")

    @pytest.mark.parametrize("sex, label", [(None, "未填写"), (1, "男"), (2, "女")])
    def test_userinfo_sex(self, sex: Union[None, int], label: str) -> None:
        self.regular_user.userinfo.update(sex=sex)
        assert self.regular_user.userinfo.sex_label == label

    @pytest.mark.parametrize(
        "first_name, last_name, nickname",
        [(None, "b", "regular_user"), ("a", None, "regular_user"), ("a", "b", "a b")],
    )
    def test_userinfo_nickname(
        self, first_name: str, last_name: str, nickname: str
    ) -> None:
        self.regular_user.userinfo.update(first_name=first_name, last_name=last_name)
        assert self.regular_user.nickname == nickname


@pytest.mark.usefixtures("flask_app")
def test_model_creation() -> None:
    user = User.create(username="1212", password="1212", userinfo=UserInfo())
    assert user.nickname == "1212" and user.password == "1212" and str(user.userinfo) == "1212"
    UserInfo.query.filter_by(id=user.userinfo.id).delete()
    User.query.filter_by(id=user.id).delete()
