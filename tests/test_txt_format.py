import pytest

from expose_text.formats._txt import TxtFormat

ENCODING = "UTF-8"


@pytest.fixture
def txt_bytes():
    return b"This is the content of a text file.\n\nWith multiple lines.\n\nTry alter me."


@pytest.fixture()
def format_cls(txt_bytes):
    format_cls = TxtFormat()
    format_cls.load(txt_bytes)
    return format_cls


def test_text_property(format_cls, txt_bytes):
    assert format_cls.text == txt_bytes.decode(ENCODING)


def test_bytes_property(format_cls, txt_bytes):
    assert format_cls.bytes == txt_bytes


def test_alterations(format_cls):
    # all indices are for the original string (in_bytes)
    format_cls.add_alter(0, 4, "That")
    format_cls.add_alter(35, 59, " ")
    format_cls.add_alter(63, 68, "change")
    format_cls.apply_alters()
    assert format_cls.text == "That is the content of a text file. Try change me."
    assert format_cls.bytes == b"That is the content of a text file. Try change me."


@pytest.mark.parametrize("encoding", ["utf-8", "utf-16", "latin-1", "windows-1252"])
def test_encodings(encoding):
    encoded_string = "¾ der Mäuse sind weiß. The bread costs 7$.".encode(encoding)
    format_cls = TxtFormat()
    format_cls.load(encoded_string)
    assert format_cls.bytes == encoded_string
    assert format_cls.text == encoded_string.decode(encoding)
