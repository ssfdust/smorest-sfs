#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Callable, Iterator, Tuple

import pytest
from flask import Flask

from smorest_sfs.modules.groups.models import Group
from smorest_sfs.modules.roles.models import Role
from smorest_sfs.modules.users.models import User, UserInfo


@pytest.fixture
def fake_roles(
    flask_app: Flask, temp_db_instance_helper: Callable[..., Iterator[Any]],
) -> Iterator[Tuple[Role, ...]]:
    # pylint: disable=W0613
    for _ in temp_db_instance_helper(
        Role(name="a", user_default=True),
        Role(name="b"),
        Role(name="c"),
        Role(name="d"),
        Role(name="e"),
        Role(name="f"),
    ):
        yield _


@pytest.fixture
def fake_groups(
    flask_app: Flask, temp_db_instance_helper: Callable[..., Iterator[Any]],
) -> Iterator[Tuple[Group, ...]]:
    # pylint: disable=W0613
    for _ in temp_db_instance_helper(
        Group(
            id=4,
            name="temp_group_with_a_b_c",
            roles=Role.where(name__in=["a", "b", "c"]).all(),
        ),
        Group(
            id=5,
            name="temp_group_with_c_f",
            roles=Role.where(name__in=["c", "f"]).all(),
        ),
        Group(
            id=6,
            name="temp_group_with_c_d_e",
            roles=Role.where(name__in=["c", "d", "e"]).all(),
        ),
        Group(
            id=7, name="temp_group_with_f", roles=Role.where(name__in=["f", "q"]).all()
        ),
    ):
        yield _


@pytest.fixture
def fake_users(
    flask_app: Flask, temp_db_instance_helper: Callable[..., Iterator[Any]],
) -> Iterator[Tuple[User, ...]]:
    # pylint: disable=W0613
    for _ in temp_db_instance_helper(
        User(
            username="fake_1",
            password="password",
            email="fake_1",
            active=True,
            roles=Role.where(name__in=["f", "a"]).all(),
            userinfo=UserInfo(),
        ),
        User(
            username="fake_2",
            password="password",
            email="fake_2",
            active=True,
            roles=Role.where(name__in=["c", "a", "b"]).all(),
            groups=[Group.get_by_id(4)],
            userinfo=UserInfo(),
        ),
        User(
            username="fake_3",
            password="password",
            email="fake_3",
            active=True,
            groups=[Group.get_by_id(5)],
            roles=Role.where(name__in=["f", "c"]).all(),
            userinfo=UserInfo(),
        ),
        User(
            username="fake_4",
            password="password",
            email="fake_4",
            active=True,
            roles=Role.where(name__in=["f", "a", "c", "d", "e"]).all(),
            groups=[Group.get_by_id(6)],
            userinfo=UserInfo(),
        ),
        User(
            username="fake_5",
            password="password",
            email="fake_5",
            active=True,
            userinfo=UserInfo(),
        ),
        User(
            username="fake_6",
            password="password",
            email="fake_6",
            active=True,
            userinfo=UserInfo(),
        ),
    ):
        yield _
