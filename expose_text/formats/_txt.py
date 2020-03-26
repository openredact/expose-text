from expose_text.formats._base import Format


class TxtFormat(Format):
    content = ""

    def load(self, raw):
        self.content = raw

    @property
    def text(self):
        return self.content

    @property
    def raw(self):
        return self.content

    def add_alter(self, start, end, new_text):
        self.buffer += (start, end, new_text)

    def apply_alters(self):
        new_content = ""
        cur = 0
        for start, end, new_text in self.buffer.sort():
            new_content += self.content[cur:start] + new_text
            cur = end
        new_content += self.content[cur:]
        self.content = new_content
        self.buffer.clear()
