import base64
import collections
import os
import re
import shutil
import tempfile
from subprocess import run, PIPE
from typing import Dict

import pdfkit

from expose_text.exceptions import FormatError
from expose_text.formats._html import HtmlFormat
from expose_text.formats.base import Format


class Pdf2Html2PdfFormat(Format):
    """
    Use HTML as intermediate format to work with PDFs.
    Not loss-free! Layout might be different, but replacements with out-of-vocabulary characters is possible!

    Dependencies:
    - PDF to HTML: poppler-utils
    - HTML to PDF: pdfkit (wrapper for wkhtmltopdf utility to convert HTML to PDF using Webkit)

    """

    page2html = {}
    html_format = None  # type: HtmlFormat

    def __init__(
        self,
        encoding="utf-8",
        pdf_margin_left="0",
        pdf_margin_right="0",
        pdf_margin_top="0",
        pdf_margin_bottom="0",
        pdf_zoom="1.1",
    ):
        """
        For PDF settings see pdfkit (wkhtmltopdf) documentation
        """
        super().__init__()
        self.encoding = encoding
        self.html_format = HtmlFormat()
        self.pdf_margin_left = pdf_margin_left
        self.pdf_margin_right = pdf_margin_right
        self.pdf_margin_top = pdf_margin_top
        self.pdf_margin_bottom = pdf_margin_bottom
        self.pdf_zoom = pdf_zoom

    def load(self, bytes_):
        self.page2html = self.get_html_pages_from_pdf(bytes_)

        # send to html format wrapper
        self.html_format.load(self.page2html[1].encode("utf-8"))

    @property
    def text(self):
        # html to text
        return self.html_format.text

    @property
    def bytes(self):
        """Generate PDF from HTML bytes with pdfkit (wkhtmltopdf) """
        html_bytes = self.html_format.bytes

        pdf_bytes = pdfkit.from_string(
            html_bytes.decode(self.encoding),
            False,
            options={
                "load-error-handling": "ignore",
                "load-media-error-handling": "ignore",
                "margin-left": self.pdf_margin_left,
                "margin-right": self.pdf_margin_right,
                "margin-top": self.pdf_margin_top,
                "margin-bottom": self.pdf_margin_bottom,
                "zoom": self.pdf_zoom,
                # 'disable-smart-shrinking': '',
            },
        )

        return pdf_bytes

    def add_alter(self, start, end, new_text):
        """Alter only on HTML format"""
        self.html_format.add_alter(start, end, new_text)

    def apply_alters(self):
        """Alter only on HTML format"""
        self.html_format.apply_alters()

    @staticmethod
    def get_html_pages_from_pdf(pdf_bytes) -> Dict[int, str]:
        """
        Converts PDF to HTML with htmltopdf (from poppler-utils: https://poppler.freedesktop.org/)

        :param pdf_bytes:
        :return:  Page number => HTML string
        """
        page2html = {}
        file_prefix = "pdf"
        tmpdir = tempfile.mkdtemp(prefix="pdftohtml-")

        process = run(["pdftohtml", "-c", "-", tmpdir + "/" + file_prefix], stdout=PIPE, input=pdf_bytes)  # , encoding='ascii'

        if process.returncode != 0:
            raise FormatError("pdftohtml returned error exit code: %s" % process.returncode)

        # Iterate over output files
        for fn in os.listdir(tmpdir):
            if fn.startswith(file_prefix + "-") and fn.endswith(".html"):
                # Page file
                page_num = int(fn[len(file_prefix) + 1 : -5])

                with open(os.path.join(tmpdir, fn), "r") as f:
                    html = f.read()

                    # Replace body bgcolor + Margin settings
                    html = html.replace('bgcolor="#A0A0A0"', 'style="margin: 0; padding: 0;"')

                    # Replace image source with base64 encodings
                    def img_src_to_base64(match):
                        fn = match.group(1)
                        with open(os.path.join(tmpdir, fn), "rb") as image_file:
                            encoded_img = base64.b64encode(image_file.read()).decode("utf-8")

                        return f'src="data:image/png;base64, {encoded_img}"'

                    pattern = re.compile(r'src="(.*?)"')  # src="pdf001.png"
                    html = pattern.sub(img_src_to_base64, html)

                    page2html[page_num] = html

        # Remove temp files
        shutil.rmtree(tmpdir)

        # Ensure page order
        page2html = collections.OrderedDict(sorted(page2html.items()))

        return page2html
