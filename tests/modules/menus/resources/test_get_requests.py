#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

from smorest_sfs.modules.auth import ROLES
from smorest_sfs.modules.menus.models import Menu
from tests._utils.injection import GeneralGet


class TestListView(GeneralGet):

    fixture_names = ("flask_app_client", "flask_app", "regular_user", "fake_menus")
    item_view = "Menu.MenuItemView"
    listview = "Menu.MenuListView"
    view = "Menu.MenuView"
    login_roles = [ROLES.SuperUser, ROLES.User]
    menu_items: List[Menu]

    def test_get_list(self) -> None:
        data = self._get_list()
        assert data == [
            {
                "children": [
                    {"id": 4, "img": None, "name": "子菜单一", "url": "/parent1/1"},
                    {"id": 5, "img": None, "name": "子菜单二", "url": "/parent1/2"},
                    {"id": 6, "img": None, "name": "子菜单三", "url": "/parent1/3"},
                ],
                "id": 1,
                "img": "cat",
                "name": "父菜单一",
                "url": "/parent1",
            },
            {
                "children": [
                    {"id": 7, "img": None, "name": "子菜单四", "url": "/parent2/1"},
                    {"id": 8, "img": None, "name": "子菜单五", "url": "/parent2/2"},
                    {"id": 9, "img": None, "name": "子菜单六", "url": "/parent2/3"},
                    {"id": 10, "img": None, "name": "子菜单七", "url": "/parent2/4"},
                    {"id": 11, "img": None, "name": "子菜单八", "url": "/parent2/5"},
                ],
                "id": 2,
                "img": "dog",
                "name": "父菜单二",
                "url": "/parent2",
            },
            {
                "children": [
                    {"id": 12, "img": None, "name": "子菜单九", "url": "/parent3/1"},
                    {"id": 13, "img": None, "name": "子菜单十", "url": "/parent3/2"},
                ],
                "id": 3,
                "img": "bird",
                "name": "父菜单三",
                "url": "/parent3",
            },
        ]
