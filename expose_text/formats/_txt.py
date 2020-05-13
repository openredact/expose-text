from expose_text.formats._base import Format
from expose_text.formats._utils import apply_buffer_to_text

ENCODING = "UTF-8"


class TxtFormat(Format):
    _content = ""

    def load(self, _bytes):
        self._content = _bytes.decode(ENCODING)

    @property
    def text(self):
        return self._content

    @property
    def bytes(self):
        return self._content.encode(ENCODING)

    def apply_alters(self):
        self._content = apply_buffer_to_text(self._buffer, self._content)
        self._buffer.clear()
