#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Callable, Iterator, Tuple, Type

import pytest
from flask import Flask
from marshmallow import Schema

from smorest_sfs.modules.groups.models import Group


@pytest.fixture
def group_items(
    flask_app: Flask, temp_db_instance_helper: Callable[..., Iterator[Any]],
) -> Iterator[Tuple[Group, Group, Group]]:
    # pylint: disable=W0613
    for _ in temp_db_instance_helper(*(Group(name=str(_) + "tqwq") for _ in range(3))):
        yield _


@pytest.fixture
def GroupSchema(flask_app: Flask) -> Type[Schema]:
    # pylint: disable=W0621, W0613
    from smorest_sfs.modules.groups.schemas import GroupSchema

    return GroupSchema
