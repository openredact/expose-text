from expose_text.formats._utils import apply_buffer_to_text
from expose_text.formats.base import Format

# chardet is LGPL, link it dynamically
try:
    import chardet
except ModuleNotFoundError:
    chardet = None


class TxtFormat(Format):
    _encoding = None
    _content = ""

    def load(self, bytes_):
        if chardet:
            self._encoding = chardet.detect(bytes_)["encoding"]
        else:
            # if the encoding is not detected dynamically, it is assumed to be UTF-8
            self._encoding = "UTF-8"

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
