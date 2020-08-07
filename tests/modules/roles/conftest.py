#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING, Any, Dict, Iterator, List

import pytest
from flask import Flask
from mixer.backend.marshmallow import NestedMixer
from mixer.backend.sqlalchemy import Mixer as SqlaMixer

from tests.typings import INS_HELPER

if TYPE_CHECKING:
    from smorest_sfs.modules.roles.models import Permission, Role


@pytest.fixture
def test_role(
    flask_app: Flask, temp_db_instance_helper: INS_HELPER["Role"]
) -> Iterator[List["Role"]]:
    from smorest_sfs.modules.auth import PERMISSIONS
    from smorest_sfs.modules.roles.models import Permission, Role

    for _ in temp_db_instance_helper(
        Role(
            name="1_test_name",
            permissions=Permission.where(name__in=[PERMISSIONS.User]).all(),
        ),
        Role(
            name="2_test_name",
            permissions=Permission.where(name__in=[PERMISSIONS.User]).all(),
        ),
        Role(
            name="3_test_name",
            permissions=Permission.where(name__in=[PERMISSIONS.User]).all(),
        ),
    ):
        yield _


@pytest.fixture
def test_permission(
    flask_app: Flask, temp_db_instance_helper: INS_HELPER["Permission"]
) -> Iterator["Permission"]:
    # pylint: disable=W0613
    from smorest_sfs.modules.roles.models import Permission

    for _ in temp_db_instance_helper(Permission(name="test_permission")):
        yield _


@pytest.fixture
def test_role_with_permission(
    test_role: "Role", test_permission: "Permission"
) -> "Role":
    # pylint: disable=W0621
    from smorest_sfs.modules.roles.models import Role

    new_role: Role = test_role[0].update(permissions=[test_permission])
    return new_role


@pytest.fixture
def permissions(flask_app: Flask) -> List[Dict[str, Any]]:
    # pylint: disable=W0613
    from smorest_sfs.modules.auth import PERMISSIONS
    from smorest_sfs.modules.roles.models import Permission

    return [
        {"id": p.id_, "name": p.name}
        for p in Permission.get_by_names(PERMISSIONS.RoleAdd, PERMISSIONS.RoleQuery)
    ]


@pytest.fixture
def update_permissions(flask_app: Flask) -> List[Dict[str, Any]]:
    from smorest_sfs.modules.roles.models import Permission
    from smorest_sfs.modules.auth import PERMISSIONS

    return [
        {"id": p.id_, "name": p.name}
        for p in Permission.get_by_names(
            PERMISSIONS.RoleAdd, PERMISSIONS.RoleQuery, PERMISSIONS.RoleDelete
        )
    ]


@pytest.fixture
def roles(
    flask_app: Flask,
    temp_db_instance_helper: INS_HELPER["Role"],
    sqla_mixer: SqlaMixer,
) -> Iterator[List["Role"]]:
    # pylint: disable=W0613
    from smorest_sfs.modules.roles.models import Role

    for _ in temp_db_instance_helper(
        *sqla_mixer.cycle(3).blend(Role, name=sqla_mixer.sequence("{0}_test_name"))
    ):
        yield _


@pytest.fixture
def role_args(flask_app: Flask, nested_mixer: NestedMixer) -> Dict[str, str]:
    from smorest_sfs.modules.roles.schemas import RoleSchema

    data: Dict[str, str] = nested_mixer.blend(RoleSchema)
    return data
