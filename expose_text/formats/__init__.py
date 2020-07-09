from importlib import import_module

from expose_text.exceptions import UnsupportedFormat


class Registry:
    """This class registers the supported file formats.

    If you implement a new format, make sure to add it to `register_formats()`.
    """

    _formats = {}

    def find_format(self, key):
        if key not in self._formats:
            raise UnsupportedFormat(f"Format {key} is not supported!")
        return self._formats[key]

    def register_formats(self):
        self._register(".txt", "expose_text.formats._txt.TxtFormat")
        self._register(".html", "expose_text.formats._html.HtmlFormat")
        self._register(".pdf", "expose_text.formats._pdf.PdfFormat")
        self._register(".docx", "expose_text.formats._docx.DocxFormat")

    def _register(self, key, class_path):
        module_path, class_name = class_path.rsplit(".", 1)
        format_cls = getattr(import_module(module_path), class_name)
        self._formats[key] = format_cls


registry = Registry()
