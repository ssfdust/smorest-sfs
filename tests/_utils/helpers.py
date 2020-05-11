#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Dict, List


def param_helper(**kwargs: Any) -> List[Dict[str, str]]:
    result = [{k: w + f"_{i}" for k, w in kwargs.items()} for i in range(1, 4)]
    return result
