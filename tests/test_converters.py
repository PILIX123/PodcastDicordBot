from utils.converters import Converters
from pytest import raises


def test_converters_hrsToMs() -> None:
    assert Converters.hourStrToMs("01:01:01") == 3661000


def test_converters_hrsToMs_Raise() -> None:
    with raises(ValueError):
        assert Converters.hourStrToMs("01:01")
