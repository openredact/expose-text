from expose_text.formats._base import Format


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
        new_content = ""
        cur = 0
        for start, end, new_text in self._buffer.sort():
            new_content += self._content[cur:start] + new_text
            cur = end
        new_content += self._content[cur:]
        self._content = new_content
        self._buffer.clear()
