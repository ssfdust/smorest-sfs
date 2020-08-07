#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Dict, List, Optional, Type

from sqlalchemy.orm.session import Session
from sqlalchemy_mptt.mixins import BaseNestedSets

from .parsers import HierachyParser


class Transformer:
    def __init__(
        self,
        parser: HierachyParser,
        model_cls: Type[BaseNestedSets],
        session: Session,
        **kwargs: Any
    ):
        self.parser = parser
        self.model_cls = model_cls
        self.session = session
        self._ident_mapping: Dict[str, BaseNestedSets] = {}

    def transform(self) -> None:
        for idx, items in enumerate(self.parser.relation_list):
            if idx > 0:
                pid: int = self._ident_mapping[items[0]].get_pk_value()
                self._transform(items[1:], pid)
            else:
                self._transform(items)

    def _get_instance(self, **kwargs: Any) -> BaseNestedSets:
        return self.model_cls(**kwargs)  # type: ignore

    def _transform(self, items: List[str], pid: Optional[int] = None) -> None:
        for item in items:
            item_kwargs = self.parser.mapping[item]
            model = self._get_instance(parent_id=pid, **item_kwargs)
            self.__add_to_session(item, model)
        self.session.flush()

    def __add_to_session(self, ident: str, model: BaseNestedSets) -> None:
        self.session.add(model)
        self._ident_mapping[ident] = model
