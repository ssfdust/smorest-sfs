import pytest

from smorest_sfs.plugins.hierachy_xlsx.error_parser import parse_error_sheet


@pytest.mark.parametrize("key", ["sheet", "010", "工程", "  工 司 "])
def test_parse_error(key: str) -> None:
    err = KeyError("Worksheet {0} does not exist.".format(key))
    assert key == parse_error_sheet(err)


def test_none_key() -> None:
    err = KeyError("does not exist.")
    assert "" == parse_error_sheet(err)
