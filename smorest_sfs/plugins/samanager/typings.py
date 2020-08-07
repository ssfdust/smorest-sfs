"""类型lib

用以存储方便的类型
"""
from typing import Dict, Type, TypeVar, Union

from marshmallow import Schema

_M = TypeVar("_M")
_O = TypeVar("_O")
_Q = TypeVar("_Q")

STRC = Union[str, Type[_Q]]
OPT_SCHEMA = Union[Schema, Type[Schema], None]
MAPPING_TYPE = Dict[Type[_M], Type[Schema]]
