from pdfrw import PdfReader, PdfDict, PdfWriter

from expose_text.formats._base import Format, CustomWriterFormat
from expose_text.formats.pdf import pdf_redactor
from expose_text.formats.pdf.pdf_redactor import InlineImage, RedactorOptions


class PdfFormat(Format, CustomWriterFormat):
    """

    Mostly based on https://github.com/JoshData/pdf-redactor

    """
    options = None # type: RedactorOptions
    document = None
    text_tokens = None
    page_tokens = None

    @staticmethod
    def get_read_mode():
        return 'rb'

    def load(self, raw):
        self.options = pdf_redactor.RedactorOptions()
        self.options.input_stream = raw

        self.document = PdfReader(fdata=raw)
        self.text_tokens, self.page_tokens = pdf_redactor.build_text_layer(self.document, self.options)

    @property
    def text(self):
        return "".join(t.value for t in self.text_tokens)

    @property
    def raw(self):
        return self.document

    def apply_alters(self):
        # Finding all matches...
        text_tokens_index = 0
        text_tokens_charpos = 0
        text_tokens_token_xdiff = 0
        text_content = self.text
        text_tokens = self.text_tokens

        # update_text_layer
        for start, end, alteration in self._buffer.sort():
            # We got a match at text_content[i1:i2].
            i1 = start
            i2 = end

            # Pass the matched text to the replacement function to get replaced text.
            replacement = alteration

            # Do a text replacement in the tokens that produced this text content.
            # It may have been produced by multiple tokens, so loop until we find them all.
            while i1 < i2:
                # Find the original tokens in the content stream that
                # produced the matched text. Start by advancing over any
                # tokens that are entirely before this span of text.
                while text_tokens_index < len(text_tokens) and \
                        text_tokens_charpos + len(text_tokens[text_tokens_index].value) - text_tokens_token_xdiff <= i1:
                    text_tokens_charpos += len(text_tokens[text_tokens_index].value) - text_tokens_token_xdiff
                    text_tokens_index += 1
                    text_tokens_token_xdiff = 0
                if text_tokens_index == len(text_tokens): break
                assert (text_tokens_charpos <= i1)

                # The token at text_tokens_index, and possibly subsequent ones,
                # are responsible for this text. Replace the matched content
                # here with replacement content.
                tok = text_tokens[text_tokens_index]

                # Where does this match begin within the token's text content?
                mpos = i1 - text_tokens_charpos
                assert mpos >= 0

                # How long is the match within this token?
                mlen = min(i2 - i1, len(tok.value) - text_tokens_token_xdiff - mpos)
                assert mlen >= 0

                # How much should we replace here?
                if mlen < (i2 - i1):
                    # There will be more replaced later, so take the same number
                    # of characters from the replacement text.
                    r = replacement[:mlen]
                    replacement = replacement[mlen:]
                else:
                    # This is the last token in which we'll replace text, so put
                    # all of the remaining replacement content here.
                    r = replacement
                    replacement = None  # sanity

                # Do the replacement.
                tok.value = tok.value[:mpos + text_tokens_token_xdiff] + r + tok.value[
                                                                             mpos + mlen + text_tokens_token_xdiff:]
                text_tokens_token_xdiff += len(r) - mlen

                # Advance for next iteration.
                i1 += mlen

        # Replace page content streams with updated tokens.
        # apply_updated_text

        # Create a new content stream for each page by concatenating the
        # tokens in the page_tokens lists.
        from pdfrw import PdfArray
        for i, page in enumerate(self.document.pages):
            if page.Contents is None: continue  # nothing was here

            # Replace the page's content stream with our updated tokens.
            # The content stream may have been an array of streams before,
            # so replace the whole thing with a single new stream. Unfortunately
            # the str on PdfArray and PdfDict doesn't work right.
            def tok_str(tok):
                if isinstance(tok, PdfArray):
                    return "[ " + " ".join(tok_str(x) for x in tok) + "] "
                if isinstance(tok, InlineImage):
                    return "BI " + " ".join(
                        tok_str(x) + " " + tok_str(y) for x, y in tok.items()) + " ID " + tok.stream + " EI "
                if isinstance(tok, PdfDict):
                    return "<< " + " ".join(tok_str(x) + " " + tok_str(y) for x, y in tok.items()) + ">> "
                return str(tok)

            page.Contents = PdfDict()
            page.Contents.stream = "\n".join(tok_str(tok) for tok in self.page_tokens[i])
            page.Contents.Length = len(page.Contents.stream)  # reset

        self._buffer.clear()

    def write(self, file_path):
        """Use PdfWriter for output"""
        writer = PdfWriter()
        writer.trailer = self.document

        with open(file_path, 'wb') as f:
            writer.write(f)
