#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import re
import sys

log = logging.getLogger(__name__)  # pylint: disable=invalid-name


class CrudOpts:
    def __init__(self, module_name: str, module_name_singular: str, module_title: str):
        self.module_name = module_name
        self.module_name_singular = module_name_singular
        self.module_title = module_title
        self.model_name = None
        self._check_module_name()
        self._prepare_render_opts()

    def _check_module_name(self):
        if not self.module_name:
            log.critical("请提供模块名")
            sys.exit(1)

        if not re.match("^[a-zA-Z0-9_]+$", self.module_name):
            log.critical("模块名中包含特殊字符" "([a-zA-Z0-9_]+)")
            sys.exit(1)

    def _prepare_render_opts(self):
        if not self.module_name_singular:
            self.module_name_singular = self.module_name[:-1]

        if not self.module_title:
            self.module_title = " ".join(
                [word.capitalize() for word in self.module_name.split("_")]
            )

        self.model_name = "".join(
            [word.capitalize() for word in self.module_name_singular.split("_")]
        )

    def to_config(self):
        return dict(
            module_name=self.module_name,
            module_name_singular=self.module_name_singular,
            module_title=self.module_title,
            module_namespace=self.module_name.replace("_", "-"),
            model_name=self.model_name,
            description="",
        )
