"""一些工具函数

* get_the_obj 根据字符串返回对象
"""
from importlib import import_module
from typing import Union

from .typings import _O


def get_the_obj(obj: Union[str, _O]) -> _O:
    """将模块字符串转为目标对象

    传递一个类或者对象将返回原对象，而传递一个字符串的时候
    将会返回这个字符串代表的模块对象

    例如: "pathlib.Path" 将会返回```pathlib.Path```这个对象

    Args:
        obj (Union[str, _O]): 字符串或者对象

    Returns:
        _O: 最终对象

    Raises:
        ImportError: 未找到模块，模块路径错误
    """
    if isinstance(obj, str):
        parts = obj.split(".")
        module_path = ".".join(parts[0:-1])
        obj_name = parts[-1]
        module = import_module(module_path)
        if hasattr(module, parts[-1]):
            obj_: _O = getattr(module, obj_name)
            return obj_
        raise ImportError(
            f"Object {obj_name} can't load from {module}"
        )  # pragma: no cover
    return obj
