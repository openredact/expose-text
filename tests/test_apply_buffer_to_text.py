import pytest

from expose_text.formats._utils import apply_buffer_to_text, AlterationsBuffer


@pytest.fixture
def text():
    return "This is the content of a text file.\n\nWith multiple lines.\n\nTry alter me."


@pytest.fixture
def buffer():
    return AlterationsBuffer()


def test_replace_text(buffer, text):
    buffer.add(0, 4, "That")
    altered_text = apply_buffer_to_text(buffer, text)
    assert altered_text == "That is the content of a text file.\n\nWith multiple lines.\n\nTry alter me."


def test_remove_text(buffer, text):
    buffer.add(35, 59, " ")
    altered_text = apply_buffer_to_text(buffer, text)
    assert altered_text == "This is the content of a text file. Try alter me."
