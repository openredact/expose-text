import re

from bs4 import BeautifulSoup

from expose_text.formats._base import Format
from expose_text.formats._utils import apply_buffer_to_text
from expose_text.formats.markup.utils import MarkupModifier, Mapper


class HtmlFormat(Format):
    _html = ""
    _text = ""
    _html_wrapper = None
    _soup = None

    def load(self, _bytes):
        self._soup = BeautifulSoup(_bytes, "lxml")
        self._html = "".join([str(content) if content != "\n" else "" for content in self._soup.body.contents])

        mapper = HtmlMapper(self._html)
        self._text, mapping = mapper.simultaneous_text_extraction_and_mapping()

        self._html_wrapper = MarkupModifier(self._html, mapping)

    @property
    def text(self):
        return self._text

    @property
    def bytes(self):
        new_content = BeautifulSoup(self._html, "lxml")
        body_attributes = self._soup.body.attrs
        self._soup.body.replace_with(new_content.body)
        self._soup.body.attrs = body_attributes
        return self._soup.encode("UTF-8")

    def apply_alters(self):
        self._text = apply_buffer_to_text(self._buffer, self._text)
        self._html = self._html_wrapper.apply_buffer(self._buffer)
        self._buffer.clear()


class HtmlMapper(Mapper):
    def simultaneous_text_extraction_and_mapping(self):
        self._remove_pattern(r"<br ?\/?>", replace_with="\n")  # html linebreaks
        self._remove_pattern(
            r"""<script[^>]*>.*?<\/script>  # remove scripts
                |<style[^>]*>.*?<\/style>  # remove styles
                |<template[^>]*>.*?<\/template> # remove templates
                |<[^>]+>  # remove all tags """,
            flags=re.DOTALL | re.VERBOSE,
        )
        self._remove_pattern(r"(^[ \xc2\xa0]+)", flags=re.MULTILINE)  # leading (non-breaking) whitespace
        self._remove_pattern(r"(\n\r?){3,}", replace_with="\n\n")  # excess newlines

        return self._text, self._text_to_markup_idx
