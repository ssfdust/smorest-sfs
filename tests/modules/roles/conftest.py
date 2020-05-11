#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Any, Callable, Dict, Iterator, List, Tuple, Type

import pytest
from flask import Flask
from marshmallow import Schema

from smorest_sfs.modules.auth import PERMISSIONS
from smorest_sfs.modules.roles.models import Permission, Role


@pytest.fixture
def test_role(
    flask_app: Flask, temp_db_instance_helper: Callable[..., Iterator[Any]]
) -> Iterator[Any]:
    # pylint: disable=W0613
    for _ in temp_db_instance_helper(Role(name="test_role")):
        yield _


@pytest.fixture
def test_permission(
    flask_app: Flask, temp_db_instance_helper: Callable[..., Iterator[Any]]
) -> Iterator[Any]:
    # pylint: disable=W0613
    for _ in temp_db_instance_helper(Permission(name="test_permission")):
        yield _


@pytest.fixture
def test_role_with_permission(test_role: Role, test_permission: Permission) -> Role:
    # pylint: disable=W0621
    new_role: Role = test_role.update(permissions=[test_permission])
    return new_role


@pytest.fixture
def permissions(flask_app: Flask) -> List[Dict[str, Any]]:
    # pylint: disable=W0613
    return [
        {"id": p.id, "name": p.name}
        for p in Permission.get_by_names(PERMISSIONS.RoleAdd, PERMISSIONS.RoleQuery)
    ]


@pytest.fixture
def update_permissions(flask_app: Flask) -> List[Dict[str, Any]]:
    return [
        {"id": p.id, "name": p.name}
        for p in Permission.get_by_names(
            PERMISSIONS.RoleAdd, PERMISSIONS.RoleQuery, PERMISSIONS.RoleDelete
        )
    ]


@pytest.fixture
def role_items(
    flask_app: Flask, temp_db_instance_helper: Callable[..., Any],
) -> Iterator[Iterator[Tuple[Role, Role, Role]]]:
    # pylint: disable=W0613
    for _ in temp_db_instance_helper(Role(name="1"), Role(name="2"), Role(name="3")):
        yield _


@pytest.fixture
def RoleSchema(flask_app: Flask) -> Type[Schema]:
    # pylint: disable=W0621, W0613
    from smorest_sfs.modules.roles.schemas import RoleSchema

    return RoleSchema
