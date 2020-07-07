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
    _expose_body_only = None

    def load(self, _bytes):
        self._soup = BeautifulSoup(_bytes, "html.parser")

        if self._soup.body:
            content = "".join([str(content) for content in self._soup.body.contents])
            self._expose_body_only = True
        else:
            content = str(self._soup)
            self._expose_body_only = False

        self._html = content

        mapper = HtmlMapper(self._html)
        self._text, mapping = mapper.simultaneous_text_extraction_and_mapping()

        self._html_wrapper = MarkupModifier(self._html, mapping)

    @property
    def text(self):
        return self._text

    @property
    def bytes(self):
        new_content = BeautifulSoup(self._html, "html.parser")

        if self._expose_body_only:
            body = self._soup.body
            body.clear()
            body.append(new_content)
        else:
            self._soup.clear()
            self._soup.append(new_content)

        return str(self._soup).encode("UTF-8")

    def apply_alters(self):
        self._text = apply_buffer_to_text(self._buffer, self._text)
        self._html = self._html_wrapper.apply_buffer(self._buffer)
        self._buffer.clear()


class HtmlMapper(Mapper):
    def simultaneous_text_extraction_and_mapping(self):
        self._remove_pattern(r"<br ?\/?>", replace_with="\n")  # html linebreaks
        self._remove_pattern(
            r"""<script[^>]*>.*?<\/script>  # remove scripts with content
                |</[^>]+>  # remove all closing tags
                |<[^>]+>\n?  # remove all opening tags, if possible including newlines """,
            flags=re.DOTALL | re.VERBOSE,
        )

        return self._text, self._text_to_markup_idx
