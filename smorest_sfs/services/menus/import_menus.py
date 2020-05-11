#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Union

from smorest_sfs.extensions import db
from smorest_sfs.modules.menus import models
from smorest_sfs.plugins.hierachy_xlsx.parsers import HierachyParser
from smorest_sfs.plugins.hierachy_xlsx.transformers import (
    HierachyModelProtocol,
    Transformer,
)
from smorest_sfs.utils.paths import Path, ProjectPath


class MenuTransformer(Transformer):
    def _get_instance(self, **kwargs: Any) -> HierachyModelProtocol:
        from smorest_sfs.modules.menus import schemas

        schema = schemas.MenuSchema()
        return schema.load(kwargs)


def import_menus_from_filepath(filepath: Union[str, Path]) -> None:
    filepath = ProjectPath.get_subpath_from_project(filepath)
    parser = HierachyParser(filepath=filepath)
    parser.parse()
    transformer = MenuTransformer(parser, models.Menu, db.session)
    transformer.transform()
