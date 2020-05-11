#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Dict, List, Protocol, Type

from sqlalchemy.orm.session import Session

from .parsers import HierachyParser


class HierachyModelProtocol(Protocol):
    parent_id: int

    def __init__(self, *args: Any, **kwargs: Any):  # pragma: no cover
        # pylint: disable=W0231
        ...


class Transformer:
    def __init__(
        self,
        parser: HierachyParser,
        model_cls: Type[HierachyModelProtocol],
        session: Session,
    ):
        self.parser = parser
        self.model_cls = model_cls
        self.session = session
        self._ident_mapping: Dict[str, Any] = {}

    def transform(self) -> None:
        for idx, items in enumerate(self.parser.relation_list):
            if idx > 0:
                self._transform_nodes(items)
            else:
                self._transform_root(items)
        self.session.commit()

    def _get_instance(self, **kwargs: Any) -> HierachyModelProtocol:
        return self.model_cls(**kwargs)

    def _transform_root(self, items: List[str]) -> None:
        for item in items:
            item_kwargs = self.parser.mapping[item]
            model = self._get_instance(**item_kwargs)
            self.__add_to_session(item, model)
        self.session.flush()

    def _transform_nodes(self, items: List[str]) -> None:
        parent = self._ident_mapping[items[0]]
        for item in items[1:]:
            item_kwargs = self.parser.mapping[item]
            model = self._get_instance(parent_id=parent.id, **item_kwargs)
            self.__add_to_session(item, model)
        self.session.flush()

    def __add_to_session(self, ident: str, model: HierachyModelProtocol) -> None:
        self.session.add(model)
        self._ident_mapping[ident] = model


class CodeTransformer(Transformer):
    type_code: str = ""

    def _get_instance(self, **kwargs: Any) -> HierachyModelProtocol:
        return self.model_cls(type_code=self.type_code, **kwargs)

    @staticmethod
    def __parse_filename(filename: str) -> str:
        return filename.split(".")[0]

    def transform(self) -> None:
        if self.parser.filename:
            self.type_code = self.__parse_filename(self.parser.filename)
            super().transform()
