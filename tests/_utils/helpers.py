#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Dict, List


def param_helper(**kwargs: Any) -> List[Dict[str, str]]:
    result = []
    for i in range(1, 4):
        param = {}
        for k, w in kwargs.items():
            if callable(w):
                param[k] = w(i)
            else:
                param[k] = w
        result.append(param)
    return result
