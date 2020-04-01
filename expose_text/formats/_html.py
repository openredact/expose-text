import html
import re

from expose_text.formats._base import Format
from expose_text.formats._utils import apply_buffer_to_text


class HtmlFormat(Format):
    _html = ""
    _text = ""
    _html_wrapper = None

    def load(self, raw):
        self._html = unescape_html(raw)
        self._html_wrapper = HtmlWrapper()
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


class HtmlWrapper:
    def __init__(self):
        self._text_to_html_idx = []
        self._html = ""

    def create_mapping(self, _html):
        self._html = _html

        html_to_text = HtmlToTextTransformer()
        text, self._text_to_html_idx = html_to_text.transform_to_text_and_create_mapping(_html)
        return text

    def apply_buffer(self, buffer):
        new_html = ""
        cur = 0
        for start, end, new_text in buffer.sort():
            new_html += self._html[cur : self._text_to_html_idx[start]] + html.escape(new_text)

            # inner - 1: get the html index of last text char, outer + 1: get the next char in html
            cur = self._text_to_html_idx[end - 1] + 1

            # add any html tags that got skipped (in case end spanned further than the starting element)
            new_html += self._get_skipped_tags(self._text_to_html_idx[start], cur)
        new_html += self._html[cur:]
        self._html = new_html
        return self._html

    def _get_skipped_tags(self, start, end):
        """Return all tags between start and end."""
        pattern = re.compile(r"<[^>]*>")
        tags = pattern.findall(self._html[start:end])
        return "\n".join(tags)


class HtmlToTextTransformer:
    def __init__(self):
        self._text_to_html_idx = []
        self._text = ""
        self._html = ""

    def transform_to_text_and_create_mapping(self, _html):
        self._text = _html
        self._html = _html

        self._text_to_html_idx = list(range(len(_html)))
        self._remove_tags()
        self._remove_newlines_and_whitespace()
        return self._text, self._text_to_html_idx

    def _remove_tags(self):
        self._remove_pattern(r"<br.*>", replace_with=" ")  # html linebreaks
        self._remove_pattern(r"<[^>]+>")  # html tags

    def _remove_newlines_and_whitespace(self):
        self._remove_pattern(r"\n+", replace_with=" ")  # newlines
        self._remove_pattern(r"\xa0+| {2,}", replace_with=" ")  # excess and nobreaking whitespace
        self._remove_pattern(r"(^ +)|( +$)", flags=re.MULTILINE)  # leading or trailing whitespace

    def _remove_pattern(self, regex, replace_with="", flags=0):
        pattern = re.compile(regex, flags=flags)
        while True:
            m = re.search(pattern, self._text)
            if m is None:
                break

            self._replace_content_in_html(m.start(0), m.end(0), replace_with)

    def _replace_content_in_html(self, start, end, new_text):
        if len(new_text) > end - start:
            raise NotImplementedError()
        self._text = self._text[:start] + new_text + self._text[end:]
        del self._text_to_html_idx[start + len(new_text) : end]
