import html
import re
from abc import ABC, abstractmethod

"""Utils for markup languages with tags and elements like XML or HTML."""


class MarkupModifier:
    """This class takes care of altering markup."""

    def __init__(self, markup, mapping):
        """
        :param markup:  a string containing content in a markup language
        :param mapping: a mapping from the indices of the contained text to its positions in the markup,
            i.e. `mapping[text_idx] == markup_idx`
        """
        self._markup = markup
        self._text_to_markup_idx = mapping

    def apply_buffer(self, buffer):
        new_markup = ""
        cur = 0
        for start, end, new_text in buffer.sort():
            new_markup += self._markup[cur : self._text_to_markup_idx[start]] + html.escape(new_text)

            # inner - 1: get the markup index of last text char, outer + 1: get the next char in markup
            cur = self._text_to_markup_idx[end - 1] + 1

            # append any markup tags that got skipped (in case end spanned further than the starting element)
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
    """This is the base for language specific classes that map markup to text and create an index mapping.

    Initially `self._text` contains the markup which is then step by step removed by calls to `_remove_pattern` in
    `get_text_and_mapping`. While removing it an index mapping is maintained that maps each index in `self._text` to its
    position in the markup.
    """

    def __init__(self, markup):
        self._text = markup
        self._markup = markup
        self._text_to_markup_idx = list(range(len(markup)))

    @abstractmethod
    def simultaneous_text_extraction_and_mapping(self):
        """Extract the text and create an index mapping by one or more calls to `remove_patterns`."""
        return self._text, self._text_to_markup_idx

    def _remove_pattern(self, regex, replace_with="", flags=0):
        """Remove or replace patterns in the markup.

        :param regex: the regex to replace
        :param replace_with: an optional string to replace matches with
        :param flags: optional re compile flags
        """
        pattern = re.compile(regex, flags=flags)
        while True:
            m = re.search(pattern, self._text)
            if m is None:
                break

            self._replace_content_in_markup(m.start(0), m.end(0), replace_with)

    def _replace_content_in_markup(self, start, end, new_text):
        if len(new_text) > end - start:
            raise ValueError()
        self._text = self._text[:start] + new_text + self._text[end:]
        del self._text_to_markup_idx[start + len(new_text) : end]
