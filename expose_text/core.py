import os

from expose_text.formats import registry
from expose_text.formats._base import Format

registry.register_formats()


class BinaryWrapper:
    """A wrapper for files in various formats given as binary data to exposes their text content for modification.

    >>> from pathlib import Path
    >>> root = Path(__file__).parent.parent
    >>> f = open(root / 'tests/files/doctest.txt', 'rb')
    >>> _bytes = f.read()

    Open binary data and inspect the text content.

    >>> bw = BinaryWrapper(_bytes, '.txt')
    >>> bw.text
    'This is the content as string.'

    This string provides the indices for the modification of the file. Queue new alterations and when you are done
    apply them to change the file.

    >>> bw.add_alter(0, 4, 'That')
    >>> bw.apply_alters()
    >>> bw.text
    'That is the content as string.'

    Return the content in binary format.
    >>> bw.bytes
    b'That is the content as string.'
    """

    def __init__(self, _bytes, _format):
        format_cls = registry.find_format(_format)
        self.file = format_cls()  # type: Format
        self.file.load(_bytes)

    @property
    def text(self):
        """Returns the text content of the file."""
        return self.file.text

    @property
    def bytes(self):
        """TODO"""
        return self.file.bytes

    def add_alter(self, start, end, text):
        """Queue a new change up for alteration.

        The `start` and `end` indices refer to the current value of the `text` property. Apply the queued alterations
        by calling `apply_alters()`.
        """
        self.file.add_alter(start, end, text)

    def apply_alters(self):
        """Apply all queued alterations."""
        self.file.apply_alters()


class FileWrapper(BinaryWrapper):
    """A wrapper for various file formats that exposes their text content for modification.

    >>> from pathlib import Path
    >>> root = Path(__file__).parent.parent

    Open a file and inspect its text content.

    >>> fw = FileWrapper(root / 'tests/files/doctest.txt')
    >>> fw.text
    'This is the content as string.'

    This string provides the indices for the modification of the file. Queue new alterations and when you are done
    apply them to change the file.

    >>> fw.add_alter(0, 4, 'That')
    >>> fw.apply_alters()
    >>> fw.text
    'That is the content as string.'

    Now create a new file that looks like the original one but with the altered content.
    >>> fw.save(root / 'tests/files/doctest_altered.txt')
    """

    def __init__(self, file_path):
        _, extension = os.path.splitext(file_path)

        with open(file_path, "rb") as f:
            _bytes = f.read()

        super().__init__(_bytes, extension)

    def save(self, file_path):
        """Save the file to disk."""
        with open(file_path, "wb") as f:
            f.write(self.file.bytes)
