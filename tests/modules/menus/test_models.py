#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from flask_sqlalchemy import SQLAlchemy


@pytest.mark.usefixtures("flask_app", "fake_menus")
def test_menu() -> None:
    from smorest_sfs.modules.auth import PERMISSIONS
    from smorest_sfs.modules.menus.models import Menu

    menus = Menu.query.all()
    permissions = {menu.permission.name for menu in menus}
    assert permissions <= {PERMISSIONS.SuperUser, PERMISSIONS.User}


@pytest.mark.usefixtures("flask_app", "fake_menus")
def test_sub_menu_should_not_load(db: SQLAlchemy) -> None:
    from smorest_sfs.modules.menus.models import Menu
    from smorest_sfs.modules.roles.models import Permission
    from smorest_sfs.modules.auth import PERMISSIONS
    from smorest_sfs.utils.flatten import flatten_nested_tree

    permission = Permission.get_by_name(PERMISSIONS.User)
    assert permission is not None
    menus_list = Menu.where(permission_id=permission.id_).all()
    menus_json = {menu.name for menu in menus_list}
    menus = Menu.get_tree(
        db.session,
        json=True,
        query=lambda q: q.filter(Menu.permission_id == permission.id_),
    )
    menu_names = set(flatten_nested_tree(menus))
    assert menus_json > menu_names
