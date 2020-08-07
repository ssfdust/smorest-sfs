#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Callable, Iterator

import pytest


@pytest.mark.usefixtures("flask_app")
def test_group(temp_db_instance_helper: Callable[..., Iterator[Any]]) -> None:
    from smorest_sfs.modules.groups.models import Group

    for group in temp_db_instance_helper(Group(name="test")):
        assert str(group) == "test"
    group.delete()
    group.session.commit()
