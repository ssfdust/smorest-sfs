#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict, List

import pytest

from smorest_sfs.modules.auth import ROLES
from smorest_sfs.modules.logs.models import Log
from tests._utils.injection import GeneralGet


class TestLogListView(GeneralGet):

    fixture_names = ("flask_app_client", "flask_app", "regular_user", "log_items")
    view = "Log.LogView"
    login_roles = [ROLES.LogManager]
    log_items: List[Log]

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


class TestRespLogListView(GeneralGet):

    fixture_names = ("flask_app_client", "flask_app", "regular_user", "resp_log_items")
    view = "Log.ResponseLogView"
    login_roles = [ROLES.LogManager]
    log_items: List[Log]

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
