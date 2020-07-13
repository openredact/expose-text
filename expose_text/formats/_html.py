import html
import re

from bs4 import UnicodeDammit

from expose_text.formats._utils import apply_buffer_to_text
from expose_text.formats.base import Format
from expose_text.formats.markup.utils import MarkupModifier, Mapper


class HtmlFormat(Format):
    _html = ""
    _text = ""
    _html_modifier = None

    def load(self, bytes_):
        self._html = to_unicode(bytes_)

        mapper = HtmlMapper(self._html)
        self._text, mapping = mapper.simultaneous_text_extraction_and_mapping()

        self._html_modifier = MarkupModifier(self._html, mapping)

    @property
    def text(self):
        return self._text

    @property
    def bytes(self):
        return self._html.encode("UTF-8")

    def apply_alters(self):
        self._text = apply_buffer_to_text(self._buffer, self._text)
        self._html = self._html_modifier.apply_buffer(self._buffer)
        self._buffer.clear()


def to_unicode(bytes_):
    def unescape_html(html_):
        unescaped_html = ""
        pattern = re.compile(r"&#\d{1,4};|&\w{1,6};")
        cur = 0
        for m in pattern.finditer(html_):
            if m.group(0) in ["&lt;", "&gt;", "&amp;", "&quot;", "&apos;"]:
                continue

            unescaped_html += html_[cur : m.start()] + html.unescape(m.group(0))
            cur = m.end()
        unescaped_html += html_[cur:]
        return unescaped_html

    dammit = UnicodeDammit(bytes_)
    encoding = dammit.original_encoding
    decoded_html = bytes_.decode(encoding)
    return unescape_html(decoded_html)


class HtmlMapper(Mapper):
    def simultaneous_text_extraction_and_mapping(self):
        # get rid of everything but body and title
        self._remove_pattern(r"^.*<body[^>]*>", flags=re.DOTALL)  # delete everything from beginning to body
        self._remove_pattern(r"<\/body>.*$", flags=re.DOTALL)  # delete everything from body to end

        # remove html from inside body
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

        # unescape characters
        self._remove_pattern(r"&amp;", replace_with="&")
        self._remove_pattern(r"&lt;", replace_with="<")
        self._remove_pattern(r"&gt;", replace_with=">")
        self._remove_pattern(r"&quot;", replace_with='"')
        self._remove_pattern(r"&apos;", replace_with="'")

        # remove leading and trailing newlines
        self._remove_pattern(r"^\n+")
        self._remove_pattern(r"\n+$")

        return self._text, self._text_to_markup_idx
