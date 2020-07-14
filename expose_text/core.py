import os

from expose_text.formats import registry
from expose_text.formats.base import Format

registry.register_formats()


class BinaryWrapper:
    """A wrapper for binary files in various formats that exposes their text content for modification.

    >>> from pathlib import Path
    >>> root = Path(__file__).parent.parent
    >>> f = open(root / 'tests/files/doctest.txt', 'rb')
    >>> _bytes = f.read()

    Open binary data and inspect the text content.

    >>> bw = BinaryWrapper(_bytes, '.txt')
    >>> bw.text
    'This is the content as string.'

    Or access the content using slicing.

    >>> bw[12:19]
    'content'
    >>> bw[29]
    '.'

    This string provides the indices for the modification of the file. Queue new alterations and when you are done
    apply them to change the file.

    >>> bw.add_alter(0, 4, 'That')
    >>> bw.apply_alters()
    >>> bw.text
    'That is the content as string.'

    The slicing interface lets you make and apply an alteration in a single call.

    >>> bw[12:19] = 'new content'
    >>> bw[33] = '!'
    >>> bw.text
    'That is the new content as string!'

    Return the content in binary format.
    >>> bw.bytes
    b'That is the new content as string!'
    """

    def __init__(self, _bytes, _format):
        format_cls = registry.find_format(_format)
        self.file = format_cls()  # type: Format
        self.file.load(_bytes)

    @property
    def text(self):
        """The text content of the file."""
        return self.file.text

    @property
    def bytes(self):
        """The binary content of the file."""
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

    def __getitem__(self, key):
        """Get a substring of the contained text using slicing or indexing."""
        return self.file.text.__getitem__(key)

    def __setitem__(self, key, value):
        """Add and apply one alter using the slicing syntax."""
        if isinstance(key, slice):
            self.add_alter(key.start, key.stop, value)
        else:
            self.add_alter(key, key + 1, value)
        self.apply_alters()


class FileWrapper(BinaryWrapper):
    """A wrapper for various file formats that exposes their text content for modification.

    >>> from pathlib import Path
    >>> root = Path(__file__).parent.parent

    Open a file and inspect its text content.

    >>> fw = FileWrapper(root / 'tests/files/doctest.txt')
    >>> fw.text
    'This is the content as string.'

    Or access the content using slicing.

    >>> fw[12:19]
    'content'
    >>> fw[29]
    '.'

    This string provides the indices for the modification of the file. Queue new alterations and when you are done
    apply them to change the file.

    >>> fw.add_alter(0, 4, 'That')
    >>> fw.apply_alters()
    >>> fw.text
    'That is the content as string.'

    The slicing interface lets you make and apply an alteration in a single call.

    >>> fw[12:19] = 'new content'
    >>> fw[33] = '!'
    >>> fw.text
    'That is the new content as string!'

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
