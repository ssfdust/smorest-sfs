from typing import Type, TypeVar

T = TypeVar("T")


class FakeGenericMeta(type):
    def __getitem__(self, item):  # type: ignore
        return self


def create_fake_generic(cls: Type[T]) -> Type[T]:
    class FakeGeneric(cls, metaclass=FakeGenericMeta):  # type: ignore
        pass

    return FakeGeneric
