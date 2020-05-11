#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from smorest_sfs.modules.groups.models import Group


@pytest.mark.usefixtures("flask_app")
def test_group() -> None:
    name = str(Group.create(name="test"))
    assert name == "test"
