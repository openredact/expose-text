import pytest

from expose_text.formats._utils import AlterationsBuffer


@pytest.fixture()
def buffer():
    return AlterationsBuffer()


def test_invalid_type(buffer):
    with pytest.raises(TypeError):
        buffer += 0

    with pytest.raises(TypeError):
        buffer += (1, 2)


def test_overlapping_alterations(buffer):
    buffer.add(5, 15, "luke")

    with pytest.raises(ValueError):
        buffer.add(0, 10, "vader")

    with pytest.raises(ValueError):
        buffer.add(10, 20, "obi")


def test_non_overlapping_corner_cases(buffer):
    buffer.add(5, 15, "anakin")  # existing one

    buffer.add(0, 5, "jango")
    buffer.add(15, 20, "boba")
    assert len(buffer) == 3


def test_sorting(buffer):
    buffer.add(0, 5, "yoda")
    buffer.add(20, 25, "jarjar")
    buffer.add(10, 15, "kenobi")
    buffer.sort()
    assert list(buffer) == [(0, 5, "yoda"), (10, 15, "kenobi"), (20, 25, "jarjar")]
