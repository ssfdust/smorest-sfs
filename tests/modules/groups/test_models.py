#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Callable, Iterator

import pytest

from smorest_sfs.modules.groups.models import Group


@pytest.mark.usefixtures("flask_app")
def test_group(temp_db_instance_helper: Callable[..., Iterator[Any]]) -> None:
    for group in temp_db_instance_helper(Group(name="test")):
        assert str(group) == "test"
