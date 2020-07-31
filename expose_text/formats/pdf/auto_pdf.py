import logging

from expose_text.formats import Format
from expose_text.formats._pdf import PdfFormat
from expose_text.formats.pdf.pdf2html2pdf import Pdf2Html2PdfFormat

logger = logging.getLogger(__name__)


class AutoPdfFormat(Format):
    """
    Automatically determine what PDF format can be used depending on availability of dependencies (and alters)
    """

    def __init__(self):
        super().__init__()

        pdf2html2pdf = Pdf2Html2PdfFormat()

        if pdf2html2pdf.is_installed():
            logger.info("Using pdf2html2pdf (dependencies are installed)")
            self.format = pdf2html2pdf
        else:
            logger.info("Using PdfFormat (dependencies are missing)")
            self.format = PdfFormat()

    def load(self, bytes_):
        self.format.load(bytes_)

    @property
    def text(self):
        return self.format.text

    @property
    def bytes(self):
        return self.format.bytes

    def add_alter(self, start, end, new_text):
        self.format.add_alter(start, end, new_text)

    def apply_alters(self):
        self.format.apply_alters()
