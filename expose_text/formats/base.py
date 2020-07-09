from abc import ABC, abstractmethod

from ._utils import AlterationsBuffer


class Format(ABC):
    def __init__(self):
        self._buffer = AlterationsBuffer()

    @abstractmethod
    def load(self, bytes_):
        """Load the file in binary format into the internal representation."""
        pass

    @property
    @abstractmethod
    def text(self):
        """Get the current text content."""
        pass

    @property
    @abstractmethod
    def bytes(self):
        """Get the current file content as binary data."""

    def add_alter(self, start, end, new_text):
        """Queue an alteration of the text.

        The `start` and `end` indices are based on the current `text` content. The `text` and `bytes` content are not
        changed by calling this method. To apply the changes call `apply_alters()`.
        """
        self._buffer += (start, end, new_text)

    @abstractmethod
    def apply_alters(self):
        """Apply all queued alterations.

        After calling this method, `text` and `bytes` will be updated.
        """
        pass
