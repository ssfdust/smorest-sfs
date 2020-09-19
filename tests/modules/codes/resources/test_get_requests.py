#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests._utils.launcher import AccessLauncher
from tests._utils.helpers import parse_dict


class TestListView(AccessLauncher):

    fixture_names = ("flask_app_client", "flask_app", "regular_user", "fake_codes")
    listview = "Code.CodeListView"
    login_roles = ["CodeManager"]

    def test_get_options(self) -> None:
        data = self._get_options(type_code="test-002")
        parsed_data = parse_dict(data)
        assert parsed_data == [
            {"name": "A001"},
            {"name": "B001", "children": [{"name": "B010"}]},
            {
                "name": "C001",
                "children": [{"name": "C010"}, {"name": "C011"}, {"name": "C100"}],
            },
        ]
