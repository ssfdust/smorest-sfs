#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING, Dict, List

import pytest

from tests._utils.launcher import AccessLauncher

if TYPE_CHECKING:
    from smorest_sfs.modules.logs.models import Log


class TestLogListView(AccessLauncher):

    fixture_names = ("flask_app_client", "flask_app", "regular_user", "logs")
    view = "Log.LogView"
    login_roles = ["LogManager"]
    log_items: List["Log"]

    @pytest.mark.parametrize(
        "params, count",
        (
            ({"module": "info"}, 3),
            ({"level": "in"}, 0),
            ({"level": "info"}, 3),
            ({"created_date": "2020-04-14"}, 1),
            ({"created_date": "2020-04-14", "created__ge": "2020-04-14 09:00:00"}, 0),
            ({"created_date": "2020-04-14", "created__le": "2020-04-14 09:00:00"}, 1),
            ({"modified_date": "2020-04-14"}, 1),
            ({"modified_date": "2020-04-14", "modified__ge": "2020-04-14 09:00:00"}, 0),
            ({"modified_date": "2020-04-14", "modified__le": "2020-04-14 09:00:00"}, 1),
        ),
    )
    def test_get_list(self, params: Dict[str, str], count: int) -> None:
        data = self._get_list(**params)
        assert len(data) == count
        if count:
            assert data[0].keys() > {"id", "level", "line", "module", "message"}


class TestRespLogListView(AccessLauncher):

    fixture_names = ("flask_app_client", "flask_app", "regular_user", "resp_logs")
    view = "Log.ResponseLogView"
    login_roles = ["LogManager"]
    logs: List["Log"]

    @pytest.mark.parametrize(
        "params, count",
        (
            ({"url": "test_"}, 7),
            ({"method": "PO"}, 0),
            ({"method": "post"}, 2),
            ({"ip": "127.0.0.1"}, 7),
            ({"status_code": "301"}, 1),
            ({"created_date": "2020-04-14"}, 1),
            ({"created_date": "2020-04-14", "created__ge": "2020-04-14 09:00:00"}, 0),
            ({"created_date": "2020-04-14", "created__le": "2020-04-14 09:00:00"}, 1),
            ({"modified_date": "2020-04-14"}, 1),
            ({"modified_date": "2020-04-14", "modified__ge": "2020-04-14 09:00:00"}, 0),
            ({"modified_date": "2020-04-14", "modified__le": "2020-04-14 09:00:00"}, 1),
        ),
    )
    def test_get_list(self, params: Dict[str, str], count: int) -> None:
        data = self._get_list(**params)
        assert len(data) == count
        if count:
            assert data[0].keys() > {
                "id",
                "module",
                "status_code",
                "ip",
                "method",
                "url",
            }
