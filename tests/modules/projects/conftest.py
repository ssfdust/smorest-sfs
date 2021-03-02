#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Dict

import pytest
from flask import Flask
from mixer.backend.marshmallow import NestedMixer


@pytest.fixture
def project_args(flask_app: Flask, nested_mixer: NestedMixer) -> Dict[str, str]:
    # pylint: disable=W0613
    from smorest_sfs.modules.projects.schemas import ProjectSchema

    data: Dict[str, str] = nested_mixer.blend(ProjectSchema)

    return data
