#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING, List

from tests._utils.launcher import AccessLauncher

if TYPE_CHECKING:
    from smorest_sfs.modules.menus.models import Menu


class TestListView(AccessLauncher):

    fixture_names = ("flask_app_client", "flask_app", "regular_user", "fake_menus")
    item_view = "Menu.MenuItemView"
    listview = "Menu.MenuListView"
    view = "Menu.MenuView"
    login_roles = ["SuperUser", "User"]
    menu_items: List["Menu"]

    def test_get_list(self) -> None:
        data = self._get_list()
        assert data == [
            {
                "children": [
                    {"id": 4, "img": "", "name": "子菜单一", "url": "/parent1/1"},
                    {"id": 5, "img": "", "name": "子菜单二", "url": "/parent1/2"},
                    {"id": 6, "img": "", "name": "子菜单三", "url": "/parent1/3"},
                ],
                "id": 1,
                "img": "cat",
                "name": "父菜单一",
                "url": "/parent1",
            },
            {
                "children": [
                    {"id": 7, "img": "", "name": "子菜单四", "url": "/parent2/1"},
                    {"id": 8, "img": "", "name": "子菜单五", "url": "/parent2/2"},
                    {"id": 9, "img": "", "name": "子菜单六", "url": "/parent2/3"},
                    {"id": 10, "img": "", "name": "子菜单七", "url": "/parent2/4"},
                    {"id": 11, "img": "", "name": "子菜单八", "url": "/parent2/5"},
                ],
                "id": 2,
                "img": "dog",
                "name": "父菜单二",
                "url": "/parent2",
            },
            {
                "children": [
                    {"id": 12, "img": "", "name": "子菜单九", "url": "/parent3/1"},
                    {"id": 13, "img": "", "name": "子菜单十", "url": "/parent3/2"},
                ],
                "id": 3,
                "img": "bird",
                "name": "父菜单三",
                "url": "/parent3",
            },
        ]
