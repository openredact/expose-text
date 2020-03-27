class AlterationsBuffer:
    """This class is used to safely queue alterations.

    Add new alterations to this buffer by using one of the two interfaces. The logic makes sure that no overlapping
    alterations are added, i.e. that each part of the original text can only be altered once.

    >>> buffer = AlterationsBuffer()
    >>> buffer.add(0, 10, 'new_text')
    >>> buffer += (0, 10, 'new_text')

    Access the alterations by using the iterable interface of this class.
    """

    def __init__(self):
        self.buffer = []

    def __iter__(self):
        return iter(self.buffer)

    def __iadd__(self, alter):
        if not isinstance(alter, tuple) or len(alter) != 3:
            raise TypeError("Invalid alteration! Valid ones are (start, end, new_text) tuples.")
        self.add(*alter)
        return self

    def __len__(self):
        return len(self.buffer)

    def add(self, start, end, new_text):
        alter = (start, end, new_text)
        if self._overlaps_with_existing_alter(alter):
            raise ValueError("The given alteration overlaps with an existing one!")

        self.buffer += [alter]

    def sort(self, reverse=False):
        self.buffer.sort(key=lambda alter: alter[0], reverse=reverse)
        return self

    def clear(self):
        self.buffer = []

    def _overlaps_with_existing_alter(self, new_alter):
        new_start = new_alter[0]
        new_end = new_alter[1]

        for existing_alter in self.buffer:
            existing_start = existing_alter[0]
            existing_end = existing_alter[1]
            if existing_start <= new_start < existing_end or existing_start < new_end <= existing_end:
                return True

        return False


def apply_buffer_to_text(buffer, text):
    """Apply all alterations from the buffer to the text.

    This replaces the original text at the indices specified in the alterations by the respective altered texts.
    """
    new_text = ""
    cur = 0
    for start, end, alteration in buffer.sort():
        new_text += text[cur:start] + alteration
        cur = end
    new_text += text[cur:]
    return new_text
