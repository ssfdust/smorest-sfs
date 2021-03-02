#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING, Iterator, List

import pytest
from flask import Flask
from mixer.backend.sqlalchemy import Mixer as SqlaMixer

from tests.typings import INS_HELPER

if TYPE_CHECKING:
    from smorest_sfs.modules.projects.models import Project


@pytest.fixture
def projects(
    flask_app: Flask,
    temp_db_instance_helper: INS_HELPER["EmailTemplate"],
    sqla_mixer: SqlaMixer,
) -> Iterator[List["EmailTemplate"]]:
    # pylint: disable=W0613
    from smorest_sfs.modules.projects.models import Project

    for _ in temp_db_instance_helper(
        *sqla_mixer.cycle(3).blend(Project, name=sqla_mixer.sequence("{0}_test_name"))
    ):
        yield _
