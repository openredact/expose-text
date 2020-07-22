import io
import re
import zipfile

from defusedxml.minidom import parse

from expose_text.formats._utils import apply_buffer_to_text
from expose_text.formats.base import Format
from expose_text.formats.markup.utils import MarkupModifier, Mapper


class DocxFormat(Format):
    _docx_container = None
    _text = ""
    _xml_modifier = None

    def load(self, bytes_):
        self._docx_container = DocxContainer(bytes_)

        mapper = DocxMapper(self._docx_container.document_xml)
        self._text, mapping = mapper.simultaneous_text_extraction_and_mapping()

        self._xml_modifier = MarkupModifier(self._docx_container.document_xml, mapping)

    @property
    def text(self):
        return self._text

    @property
    def bytes(self):
        return self._docx_container.to_bytes()

    def apply_alters(self):
        self._text = apply_buffer_to_text(self._buffer, self._text)
        self._docx_container.document_xml = self._xml_modifier.apply_buffer(self._buffer)
        self._buffer.clear()


class DocxContainer:
    _docx = None
    document_xml = None

    def __init__(self, bytes_):
        docx_io = io.BytesIO(bytes_)
        self._docx = zipfile.ZipFile(docx_io)

        document_xml_bytes = self._docx.read("word/document.xml")

        document_xml_io = io.BytesIO(document_xml_bytes)
        encoding = parse(document_xml_io).encoding

        self.document_xml = document_xml_bytes.decode(encoding)

    def to_bytes(self):
        # modifying a zip file is not supported, thus it has to be rebuilt
        bytes_io = io.BytesIO()
        zout = zipfile.ZipFile(bytes_io, "w")
        for zinfo in self._docx.infolist():
            if zinfo.filename == "word/document.xml":
                zout.writestr(zinfo, self.document_xml)
                continue

            buffer = self._docx.read(zinfo.filename)
            zout.writestr(zinfo, buffer)
        zout.close()
        return bytes_io.getvalue()


class DocxMapper(Mapper):
    def simultaneous_text_extraction_and_mapping(self):
        # get plain text from word/document.xml (everything between <w:t ...> and </w:t>)
        self._remove_pattern(r"\n")  # get rid of all newlines from the xml formatting
        self._remove_pattern(r"<\/w:p>|<w:br[^>]*>", replace_with="\n")  # add newlines from paragraph ends and linebreaks
        self._remove_pattern(r"<\/w:t>.*?<w:t[^>]*>", flags=re.MULTILINE)  # delete content from text close to open tags
        self._remove_pattern(r"^.*<w:t[^>]*>", flags=re.MULTILINE)  # delete to remaining open tags
        self._remove_pattern(r"<\/w:t>.*$", flags=re.MULTILINE)  # delete from remaining close tags
        self._remove_pattern(r"^.*<.*$", flags=re.MULTILINE)  # delete leftover lines with xml content

        # unescape characters
        self._remove_pattern(r"&amp;", replace_with="&")
        self._remove_pattern(r"&lt;", replace_with="<")
        self._remove_pattern(r"&gt;", replace_with=">")
        self._remove_pattern(r"&quot;", replace_with='"')
        self._remove_pattern(r"&apos;", replace_with="'")

        # remove leading and trailing newlines
        self._remove_pattern(r"^\n+")
        self._remove_pattern(r"\n+$")

        return self._text, self._text_to_markup_idx
