#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Any, Dict, Union

from smorest_sfs.extensions import db
from smorest_sfs.modules.menus import models
from smorest_sfs.modules.roles.models import Permission
from smorest_sfs.plugins.hierachy_xlsx.parsers import HierachyParser
from smorest_sfs.plugins.hierachy_xlsx.transformers import Transformer
from smorest_sfs.utils.paths import ProjectPath


def get_permission(data: Dict[str, Any]) -> None:
    data["permission"] = Permission.get_by_name(data["permission"])


def import_menus_from_filepath(filepath: Union[str, Path]) -> None:
    filepath = ProjectPath.get_subpath_from_project(filepath)
    with filepath.open("rb") as f:
        parser = HierachyParser(f)
    parser.parse()
    for k in parser.mapping:
        get_permission(parser.mapping[k])
    transformer = Transformer(parser, models.Menu, db.session)
    transformer.transform()
