import html
import re

from expose_text.formats._base import Format
from expose_text.formats._utils import apply_buffer_to_text


class HtmlFormat(Format):
    _html = ""
    _text = ""
    _mapper = None

    def load(self, raw):
        self._html = raw
        self._mapper = Mapper(self._html)
        self._text = self._mapper.text

    @property
    def text(self):
        return self._text

    @property
    def raw(self):
        return self._html

    def apply_alters(self):
        self._text = apply_buffer_to_text(self._buffer, self._text)

        new_html = ""
        cur = 0
        for start, end, _new_text in self._buffer.sort():
            new_html += self._html[cur : self._mapper.text_to_html_index(start)] + _new_text
            cur = self._mapper.text_to_html_index(end)
        new_html += self._html[cur:]
        self._html = new_html

        self._buffer.clear()


class Mapper:
    _text_to_html_mapping = []
    _text = ""
    _html = ""

    def __init__(self, html):
        self._html = html
        self._text_to_html_mapping = list(range(len(html)))

        self._text = html
        self._transform_html_to_text_and_create_mapping()

    @property
    def text(self):
        return self._text

    def text_to_html_index(self, pos_start):
        """Maps text to html indices"""
        return self._text_to_html_mapping[pos_start]

    def _replace_content_in_html(self, start, end, new_text):
        if len(new_text) > end - start:
            raise NotImplementedError()
        self._text = self._text[:start] + new_text + self._text[end:]
        del self._text_to_html_mapping[start + len(new_text) : end]

    def _transform_html_to_text_and_create_mapping(self):
        self._remove_pattern(r"<br.*>", replace_with=" ")  # html linebreaks
        self._remove_pattern(r"<[^>]+>")  # html tags
        self._remove_pattern(r"\xa0+| {2,}", replace_with=" ")  # excess and nobreaking whitespace
        self._remove_pattern(r"(^ +)|( +$)", flags=re.MULTILINE)  # leading or trailing whitespace
        self._remove_pattern(r"\n+", replace_with=" ")  # newlines
        self._remove_pattern(r"(^ +)|( +$)", flags=re.MULTILINE)  # leading or trailing whitespace
        self._remove_pattern(r"&#\d{1,4};|&\w{1,6};", unescape=True)  # replace html special entities

    def _remove_pattern(self, regex, replace_with="", flags=0, unescape=False):
        pattern = re.compile(regex, flags=flags)
        while True:
            m = re.search(pattern, self._text)
            if m is None:
                break
            if unescape:
                replace_with = html.unescape(m.group(0))
            self._replace_content_in_html(m.start(0), m.end(0), replace_with)
