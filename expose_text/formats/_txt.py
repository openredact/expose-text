import chardet

from expose_text.formats._base import Format
from expose_text.formats._utils import apply_buffer_to_text


class TxtFormat(Format):
    _encoding = None
    _content = ""

    def load(self, bytes_):
        self._encoding = chardet.detect(bytes_)["encoding"]
        self._content = bytes_.decode(self._encoding)

    @property
    def text(self):
        return self._content

    @property
    def bytes(self):
        return self._content.encode(self._encoding)

    def apply_alters(self):
        self._content = apply_buffer_to_text(self._buffer, self._content)
        self._buffer.clear()
