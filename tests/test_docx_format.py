import filecmp

import pytest

from expose_text import FileWrapper
from expose_text.formats._docx import DocxFormat

ENCODING = "UTF-8"


@pytest.fixture
def docx_bytes(test_files):
    with open(test_files / "test.docx", "rb") as f:
        return f.read()


@pytest.fixture
def docx_text():
    return """Title

Some body lines.

A text in different colors and styles.

This is a paragraph with a line
break and nasty <w:t> tags."""


@pytest.fixture
def format_cls(docx_bytes):
    format_cls = DocxFormat()
    format_cls.load(docx_bytes)
    return format_cls


@pytest.fixture
def replace():
    def function(string, start, stop, new_content):
        return string[:start] + new_content + string[stop:]

    return function


def test_text_property(format_cls, docx_text):
    assert format_cls.text == docx_text


def test_bytes_property(format_cls, docx_text):
    format_again = DocxFormat()
    format_again.load(format_cls.bytes)
    assert format_again.text == docx_text


def test_replacing_with_longer_text(format_cls, docx_text, replace):
    args = 25, 63, "This is the replaced line."
    format_cls.add_alter(*args)
    format_cls.apply_alters()
    assert format_cls.text == replace(docx_text, *args)


def test_replacing_with_shorter_text(format_cls, docx_text, replace):
    args = 7, 23, "XXX"
    format_cls.add_alter(*args)
    format_cls.apply_alters()
    assert format_cls.text == replace(docx_text, *args)


def test_removing_text(format_cls, docx_text, replace):
    args = 64, 124, ""
    format_cls.add_alter(*args)
    format_cls.apply_alters()
    assert format_cls.text == replace(docx_text, *args)


def test_alter_file(test_files, tmp_path):
    file_path = test_files / "test.docx"
    altered_file_path = test_files / "test_altered.docx"
    tmp_out_path = tmp_path / "test_out.docx"

    file_wrapper = FileWrapper(file_path)
    file_wrapper.add_alter(7, 23, "XXX")
    file_wrapper.add_alter(25, 63, "This is the replaced line.")
    file_wrapper.add_alter(64, 124, "")
    file_wrapper.apply_alters()
    file_wrapper.save(tmp_out_path)

    assert (
        file_wrapper.text
        == """Title

XXX

This is the replaced line.
"""
    )
    assert filecmp.cmp(altered_file_path, tmp_out_path, shallow=False)
