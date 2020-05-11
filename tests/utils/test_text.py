#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from smorest_sfs.utils.text import camel_to_snake


@pytest.mark.parametrize(
    "camel, snake",
    [
        ("AdminAvator", "admin_avator"),
        ("getHTTPResponseCode", "get_http_response_code"),
        ("HTTPResponseCodeXYZ", "http_response_code_xyz"),
    ],
)
def test_check_ext_success(camel: str, snake: str) -> None:
    assert camel_to_snake(camel) == snake
