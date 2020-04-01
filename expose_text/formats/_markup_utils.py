import html
import re
from abc import ABC, abstractmethod

"""Utils for XML and HTML like elements and tags based languages."""


class MarkupWrapper:
    def __init__(self, mapper):
        self._mapper = mapper
        self._text_to_markup_idx = []
        self._markup = ""

    def create_mapping(self, _markup):
        self._markup = _markup
        text, self._text_to_markup_idx = self._mapper.get_text_and_mapping()
        return text

    def apply_buffer(self, buffer):
        new_markup = ""
        cur = 0
        for start, end, new_text in buffer.sort():
            new_markup += self._markup[cur : self._text_to_markup_idx[start]] + html.escape(new_text)

            # inner - 1: get the markup index of last text char, outer + 1: get the next char in markup
            cur = self._text_to_markup_idx[end - 1] + 1

            # add any markup tags that got skipped (in case end spanned further than the starting element)
            new_markup += self._get_skipped_tags(self._text_to_markup_idx[start], cur)
        new_markup += self._markup[cur:]
        self._markup = new_markup
        return self._markup

    def _get_skipped_tags(self, start, end):
        """Return all tags between start and end."""
        pattern = re.compile(r"<[^>]*>")
        tags = pattern.findall(self._markup[start:end])
        return "\n".join(tags)


class Mapper(ABC):
    def __init__(self, markup):
        self._text = markup
        self._markup = markup
        self._text_to_markup_idx = list(range(len(markup)))

    @abstractmethod
    def get_text_and_mapping(self):
        # implement logic here
        return self._text, self._text_to_markup_idx

    def _remove_pattern(self, regex, replace_with="", flags=0):
        pattern = re.compile(regex, flags=flags)
        while True:
            m = re.search(pattern, self._text)
            if m is None:
                break

            self._replace_content_in_markup(m.start(0), m.end(0), replace_with)

    def _replace_content_in_markup(self, start, end, new_text):
        if len(new_text) > end - start:
            raise NotImplementedError()
        self._text = self._text[:start] + new_text + self._text[end:]
        del self._text_to_markup_idx[start + len(new_text) : end]
