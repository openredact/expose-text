from pathlib import Path

import pytest

from expose_text import FileWrapper


@pytest.fixture
def tmp_files():
    return Path(__file__).parent / "files" / "tmp"


@pytest.fixture
def test_files():
    return Path(__file__).parent / "files" / "pdf"


def test_pdf_text(tmp_files, test_files):
    input_fp = test_files / "doc.pdf"
    output_fp = tmp_files / "doc.altered.pdf"

    fw = FileWrapper(input_fp)

    print(fw.text[:100])

    fw.add_alter(0, 9, "XXXXXXX")  # replace "Deutscher"
    fw.apply_alters()

    print(fw.text[:100])

    assert "XXXXXXX" == fw.text[0:7]  # TODO there is something wrong with indexing

    fw.save(output_fp)
