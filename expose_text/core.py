import os

from expose_text.formats import registry

registry.register_formats()


class FileWrapper:
    """A wrapper for various file formats that exposes their text content for modification.

    Open a file and inspect its text content.

    >>> fw = FileWrapper('../tests/files/doctest.txt')
    >>> fw.text
    'This is the content as string.'

    This string provides the indices for the modification of the file. Queue new alterations and when you are done
    apply them to change the file.

    >>> fw.add_alter(0, 4, 'That')
    >>> fw.apply_alters()
    >>> fw.text
    'That is the content as string.'

    Now create a new file that looks like the original one but with the altered content.
    >>> fw.save('../tests/files/doctest_altered.txt')
    """

    def __init__(self, file_path):
        _, extension = os.path.splitext(file_path)
        format_cls = registry.find_format(extension)

        with open(file_path, "r") as f:
            raw = f.read()

        self.file = format_cls()
        self.file.load(raw)

    @property
    def text(self):
        """Returns the text content of the file."""
        return self.file.text

    def add_alter(self, start, end, new_text):
        """Queue a new change up for alteration.

        The `start` and `end` indices refer to the current value of the `text` property. Apply the queued alterations
        by calling `apply_alters()`.
        """
        self.file.add_alter(start, end, new_text)

    def apply_alters(self):
        """Apply all queued alterations."""
        self.file.apply_alters()

    def save(self, file_path):
        """Save the file to disk."""
        with open(file_path, "w") as f:
            f.write(self.file.raw)
