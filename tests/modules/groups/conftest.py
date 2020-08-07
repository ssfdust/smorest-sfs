#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict

import pytest
from flask import Flask
from mixer.backend.marshmallow import NestedMixer


@pytest.fixture
def group_args(flask_app: Flask, nested_mixer: NestedMixer) -> Dict[str, str]:
    from smorest_sfs.modules.groups.schemas import GroupSchema

    data: Dict[str, str] = nested_mixer.blend(GroupSchema)
    return data
