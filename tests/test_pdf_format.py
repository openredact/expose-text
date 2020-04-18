from unittest import TestCase

from pathlib import Path

from expose_text import FileWrapper


class PdfFormatTest(TestCase):
    tmp_files = Path(__file__).parent / 'files' / 'tmp'
    test_files = Path(__file__).parent / 'files' / 'pdf'

    def setUp(self) -> None:
        pass

    def test_pdf_text(self):
        input_fp = self.test_files / 'doc.pdf'
        output_fp = self.tmp_files / 'doc.altered.pdf'

        fw = FileWrapper(input_fp)

        print(fw.text[:100])

        fw.add_alter(0, 9, 'XXXXXXX')  # replace "Deutscher"
        fw.apply_alters()

        print(fw.text[:100])

        self.assertEqual('XXXXXXX', fw.text[0:7])  # TODO there is something wrong with indexing

        fw.save(output_fp)

