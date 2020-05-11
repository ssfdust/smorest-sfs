#!/usr/bin/env python
# -*- coding: utf-8 -*-
from smorest_sfs.extensions import db
from smorest_sfs.modules.codes.models import Code
from smorest_sfs.plugins.hierachy_xlsx import CodeTransformer, HierachyParser
from smorest_sfs.utils.paths import Path, ProjectPath, check_ext


def _import_codes_from_filepath(filepath: Path) -> None:
    parser = HierachyParser(filepath=filepath)
    parser.parse()
    transformer = CodeTransformer(parser, Code, db.session)
    transformer.transform()


def import_codes_from_dir(dir_path: str = "data/codes") -> None:
    path = ProjectPath.get_subpath_from_project(dir_path)
    for codefile in path.iterdir():
        if check_ext(codefile.name, "xlsx"):
            _import_codes_from_filepath(codefile)
