from pytest import raises
from botpackage.utils.converters import Converters


def test_converters_hrsToMs() -> None:
    assert Converters.hourStrToMs("01:01:01") == 3661000


def test_converters_hrsToMs_Raise() -> None:
    with raises(ValueError):
        assert Converters.hourStrToMs("01:01")
