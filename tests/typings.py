from typing import Callable, Iterator, List, TypeVar, Union

M = TypeVar("M")

INS_HELPER = Callable[..., Iterator[Union[M, List[M]]]]
