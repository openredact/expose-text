import html
import re

from expose_text.formats._base import Format
from expose_text.formats._markup_utils import MarkupWrapper, Mapper
from expose_text.formats._utils import apply_buffer_to_text


class HtmlFormat(Format):
    _html = ""
    _text = ""
    _html_wrapper = None

    def load(self, raw):
        self._html = unescape_html(raw)

        mapper = HtmlMapper(self._html)
        self._html_wrapper = MarkupWrapper(mapper)
        self._text = self._html_wrapper.create_mapping(self._html)

    @property
    def text(self):
        return self._text

    @property
    def raw(self):
        return self._html

    def apply_alters(self):
        self._text = apply_buffer_to_text(self._buffer, self._text)
        self._html = self._html_wrapper.apply_buffer(self._buffer)
        self._buffer.clear()


def unescape_html(_html):
    unescaped_html = ""
    pattern = re.compile(r"&\d{1,4};|&\w{1,6};")
    cur = 0
    for m in pattern.finditer(_html):
        if m.group(0) in ["&lt;", "&gt;", "&amp;"]:
            continue

        unescaped_html += _html[cur : m.start()] + html.unescape(m.group(0))
        cur = m.end()
    unescaped_html += _html[cur:]
    return unescaped_html


class HtmlMapper(Mapper):
    def get_text_and_mapping(self):
        self._remove_tags()
        self._remove_newlines_and_whitespace()
        return self._text, self._text_to_markup_idx

    def _remove_tags(self):
        self._remove_pattern(r"<br.*>", replace_with=" ")  # html linebreaks
        self._remove_pattern(r"<[^>]+>")  # html tags

    def _remove_newlines_and_whitespace(self):
        self._remove_pattern(r"\n+", replace_with=" ")  # newlines
        self._remove_pattern(r"\xa0+| {2,}", replace_with=" ")  # excess and nobreaking whitespace
        self._remove_pattern(r"(^ +)|( +$)", flags=re.MULTILINE)  # leading or trailing whitespace
