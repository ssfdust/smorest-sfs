#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Dict, List, Union


class LogCollecter:
    def __init__(self) -> None:
        self.resp_logs: List[Dict[str, Union[str, int, Dict[str, Any]]]] = []
        self.logs: List[Dict[str, Union[str, int]]] = []
        self.count = 0

    def add(self, val: Dict[str, Any]) -> None:
        if "log_type" not in val:
            raise ValueError("未知的日志类型")
        self._collect(val)

    def _collect(self, val: Dict[str, Any]) -> None:
        logs = self.collection_mapping[val.pop("log_type")]
        logs.append(val)
        self.count += 1

    @property
    def collection_mapping(self) -> Dict[str, List[Dict[str, Any]]]:
        return {"logging": self.logs, "response": self.resp_logs}
