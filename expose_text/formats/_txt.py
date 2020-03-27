from expose_text.formats._base import Format
from expose_text.formats._utils import apply_buffer_to_text


class TxtFormat(Format):
    _content = ""

    def load(self, raw):
        self._content = raw

    @property
    def text(self):
        return self._content

    @property
    def raw(self):
        return self._content

    def apply_alters(self):
        self._content = apply_buffer_to_text(self._buffer, self._content)
        self._buffer.clear()
