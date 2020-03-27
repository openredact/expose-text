import pytest

from expose_text.formats._txt import TxtFormat


@pytest.fixture
def raw_txt():
    return "This is the content of a text file.\n\nWith multiple lines.\n\nTry alter me."


@pytest.fixture()
def format_cls(raw_txt):
    format_cls = TxtFormat()
    format_cls.load(raw_txt)
    return format_cls


def test_text_property(format_cls, raw_txt):
    assert format_cls.text == raw_txt


def test_raw_property(format_cls, raw_txt):
    assert format_cls.raw == raw_txt


def test_alterations(format_cls):
    # all indices are for the original string (raw_txt)
    format_cls.add_alter(0, 4, "That")
    format_cls.add_alter(35, 59, " ")
    format_cls.add_alter(63, 68, "change")
    format_cls.apply_alters()
    assert format_cls.text == "That is the content of a text file. Try change me."
    assert format_cls.raw == "That is the content of a text file. Try change me."
