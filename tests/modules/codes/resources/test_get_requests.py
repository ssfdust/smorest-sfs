#!/usr/bin/env python
# -*- coding: utf-8 -*-

from smorest_sfs.modules.auth import ROLES
from tests._utils.injection import GeneralGet


class TestListView(GeneralGet):

    fixture_names = ("flask_app_client", "flask_app", "regular_user", "fake_codes")
    listview = "Code.CodeListView"
    login_roles = [ROLES.CodeManager]

    def test_get_options(self) -> None:
        assert self._get_options(type_code="test-002") == [
            {"id": 4, "name": "A001"},
            {"id": 5, "name": "B001", "children": [{"id": 7, "name": "B010"}]},
            {
                "id": 6,
                "name": "C001",
                "children": [
                    {"id": 8, "name": "C010"},
                    {"id": 9, "name": "C011"},
                    {"id": 10, "name": "C100"},
                ],
            },
        ]
