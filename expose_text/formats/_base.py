from abc import ABC, abstractmethod

from ._utils import AlterationsBuffer


class Format(ABC):
    _buffer = AlterationsBuffer()

    @abstractmethod
    def load(self, raw):
        """Load the raw file content into the internal representation."""
        pass

    @property
    @abstractmethod
    def text(self):
        """Get the current text content."""
        pass

    @property
    @abstractmethod
    def raw(self):
        """Get the current raw file content."""

    def add_alter(self, start, end, new_text):
        """Queue an alteration of the text.

        The `start` and `end` indices are based on the current `text` content. The `text` and `raw` content are not
        changed by calling this method. To apply the changes call `apply_alters()`.
        """
        self._buffer += (start, end, new_text)

    @abstractmethod
    def apply_alters(self):
        """Apply all queued alterations.

        After calling this method, `text` and `raw` will be updated."""
        pass
