#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Any, Type

from sqlalchemy.orm import Session
from sqlalchemy_mptt import BaseNestedSets

from smorest_sfs.extensions import db
from smorest_sfs.modules.codes.models import Code
from smorest_sfs.plugins.hierachy_xlsx import HierachyParser, Transformer
from smorest_sfs.utils.paths import ProjectPath, check_ext


class CodeTransformer(Transformer):
    type_code: str = ""

    def __init__(
        self,
        parser: HierachyParser,
        model_cls: Type[BaseNestedSets],
        session: Session,
        **kwargs: Any
    ):
        self.type_code = kwargs.pop("type_code")
        super().__init__(parser, model_cls, session, **kwargs)

    def _get_instance(self, **kwargs: Any) -> BaseNestedSets:
        return self.model_cls(type_code=self.type_code, **kwargs)  # type: ignore


def _import_codes_from_filepath(filepath: Path) -> None:
    with filepath.open("rb") as f:
        parser = HierachyParser(f)
    parser.parse()
    transformer = CodeTransformer(
        parser, Code, db.session, type_code=filepath.name.replace(filepath.suffix, "")
    )
    transformer.transform()
    db.session.commit()


def import_codes_from_dir(dir_path: str = "data/codes") -> None:
    path = ProjectPath.get_subpath_from_project(dir_path)
    for codefile in path.iterdir():
        if check_ext(codefile.name, "xlsx"):
            _import_codes_from_filepath(codefile)
