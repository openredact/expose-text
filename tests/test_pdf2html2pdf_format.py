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

    Run this test alone: pytest -s tests/test_pdf2html2pdf_format.py

    """
    input_fp = test_files / "doc.pdf"
    output_fp = tmp_files / "doc.altered.pdf"

    fw = FileWrapper(input_fp, Pdf2Html2PdfFormat)

    print("Before: %s" % fw.text[:25])

    # fw.add_alter(0, 9, "Deutscher")  # replace "Deutscher"
    fw.add_alter(0, 9, "".join(10 * [black_square]))  # replace "Deutscher"
    fw.apply_alters()

    print("After: %s" % fw.text[:25])

    fw.save(output_fp)

    print("Type: %s" % type(fw.file))
