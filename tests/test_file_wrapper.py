import filecmp
from pathlib import Path

import pytest

from expose_text import FileWrapper, UnsupportedFormat


@pytest.fixture
def test_files():
    return Path(__file__).parent / "files"


def test_unsupported_format(test_files):
    with pytest.raises(UnsupportedFormat):
        FileWrapper(test_files / "foo.bar")


def test_load_and_save_for_path(test_files, tmp_path):
    file_path = test_files / "test.txt"
    result_path = tmp_path / "test_out.txt"

    file_wrapper = FileWrapper(file_path)
    file_wrapper.save(result_path)

    assert filecmp.cmp(file_path, result_path, shallow=False)


def test_load_and_save_for_string(test_files, tmp_path):
    file_path = test_files / "test.txt"
    result_path = tmp_path / "test_out.txt"

    file_wrapper = FileWrapper(str(file_path))
    file_wrapper.save(str(result_path))

    assert filecmp.cmp(file_path, result_path, shallow=False)


def test_alter_file(test_files, tmp_path):
    file_path = test_files / "test.txt"
    altered_file_path = test_files / "test_altered.txt"
    result_path = tmp_path / "test_out.txt"

    file_wrapper = FileWrapper(file_path)
    file_wrapper.add_alter(20, 44, " With a single line. ")
    file_wrapper.apply_alters()
    file_wrapper.save(result_path)

    assert filecmp.cmp(altered_file_path, result_path, shallow=False)
