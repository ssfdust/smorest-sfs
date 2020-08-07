#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from smorest_sfs.modules.roles.models import Role


@pytest.mark.usefixtures("flask_app")
@pytest.mark.parametrize(
    "is_admin, name", [(True, ("SuperUser", "User")), (False, ("User",))]
)
def test_get_template(is_admin: bool, name: str) -> None:
    from smorest_sfs.modules.roles.models import Role

    assert set(r.name for r in Role.get_by_user_default(is_admin)) == set(name)


@pytest.mark.usefixtures("flask_app")
def test_add_permissions(test_role_with_permission: "Role") -> None:
    from smorest_sfs.modules.auth.permissions import (
        DEFAULT_ROLES_PERMISSIONS_MAPPING as mapping,
    )
    from smorest_sfs.modules.roles.models import Permission

    permissions = Permission.where(name__in=mapping["User"]).all()
    test_role_with_permission.add_permissions(permissions)
    test_role_with_permission.save()
    assert set(p.name for p in test_role_with_permission.permissions) == set(
        mapping["User"] + ["test_permission"]
    )
