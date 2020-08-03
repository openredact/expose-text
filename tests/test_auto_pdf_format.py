from pathlib import Path

import pytest

from expose_text import FileWrapper
from expose_text.formats.pdf.pdf2html2pdf import Pdf2Html2PdfFormat

black_square = u"\u25A0"


@pytest.fixture
def tmp_files():
    return Path(__file__).parent / "files" / "tmp"


@pytest.fixture
def test_files():
    return Path(__file__).parent / "files" / "pdf"


def test_pdf_text(tmp_files, test_files):
    """

    Run this test alone: pytest -s tests/test_pdf_format.py

    """
    input_fp = test_files / "doc.pdf"
    output_fp = tmp_files / "doc.altered.pdf"

    fw = FileWrapper(input_fp)

    print(fw.text[:100])

    fw.add_alter(0, 9, "Deutscher")  # replace "Deutscher"
    fw.apply_alters()

    print("xxx")

    print(fw.text[:100])

    # assert "XXXXXXX" == fw.text[0:7]  # TODO there is something wrong with indexing

    fw.save(output_fp)


def test_check_dependencies():
    print(Pdf2Html2PdfFormat().is_installed())
