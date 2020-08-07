from typing import Protocol, TypeVar

T_co = TypeVar("T_co", covariant=True)


class FixtureRequest(Protocol[T_co]):
    def getfixturevalue(self, fixture_name: str) -> T_co:
        ...
