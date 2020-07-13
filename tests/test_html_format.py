import filecmp

import pytest

from expose_text import FileWrapper
from expose_text.formats._html import HtmlFormat

ENCODING = "UTF-8"


@pytest.fixture
def html_snippet():
    return """<div class="foo"><h1>German paragraph</h1>\n<p>1. … macht mich glücklich</p></div>""".encode(ENCODING)


@pytest.fixture
def format_cls(html_snippet):
    format_cls = HtmlFormat()
    format_cls.load(html_snippet)
    return format_cls


def test_text_property(format_cls):
    assert format_cls.text == "German paragraph\n1. … macht mich glücklich"


def test_bytes_property(format_cls):
    assert format_cls.bytes == '<div class="foo"><h1>German paragraph</h1>\n' "<p>1. … macht mich glücklich</p></div>".encode(
        ENCODING
    )


def test_unescaping_html():
    html_bytes = '<div class="foo"><h1>&lt;&gt;&amp;</h1>\n<p>&hellip; macht mich gl&uuml;cklich</p></div>'.encode(ENCODING)
    format_cls = HtmlFormat()
    format_cls.load(html_bytes)
    assert format_cls.text == "<>&\n… macht mich glücklich"
    assert format_cls.bytes == '<div class="foo"><h1>&lt;&gt;&amp;</h1>\n' "<p>… macht mich glücklich</p></div>".encode(
        ENCODING
    )


def test_same_length_replacing(format_cls):
    format_cls.add_alter(0, 6, "XXXXXX")
    format_cls.apply_alters()
    assert format_cls.text == "XXXXXX paragraph\n1. … macht mich glücklich"
    assert format_cls.bytes == '<div class="foo"><h1>XXXXXX paragraph</h1>\n' "<p>1. … macht mich glücklich</p></div>".encode(
        ENCODING
    )


def test_replacing_with_longer_text(format_cls):
    format_cls.add_alter(0, 6, "XXXXXXXXX")
    format_cls.apply_alters()
    assert format_cls.text == "XXXXXXXXX paragraph\n1. … macht mich glücklich"
    assert (
        format_cls.bytes == '<div class="foo"><h1>XXXXXXXXX paragraph</h1>\n'
        "<p>1. … macht mich glücklich</p></div>".encode(ENCODING)
    )


def test_replacing_with_shorter_text(format_cls):
    format_cls.add_alter(0, 6, "XXX")
    format_cls.apply_alters()
    assert format_cls.text == "XXX paragraph\n1. … macht mich glücklich"
    assert format_cls.bytes == '<div class="foo"><h1>XXX paragraph</h1>\n' "<p>1. … macht mich glücklich</p></div>".encode(
        ENCODING
    )


def test_removing_text(format_cls):
    format_cls.add_alter(0, 7, "")
    format_cls.apply_alters()
    assert format_cls.text == "paragraph\n1. … macht mich glücklich"
    assert format_cls.bytes == '<div class="foo"><h1>paragraph</h1>\n' "<p>1. … macht mich glücklich</p></div>".encode(
        ENCODING
    )


def test_removing_entire_content_of_element(format_cls):
    format_cls.add_alter(0, 16, "")
    format_cls.apply_alters()
    assert format_cls.text == "\n1. … macht mich glücklich"
    assert format_cls.bytes == '<div class="foo"><h1></h1>\n' "<p>1. … macht mich glücklich</p></div>".encode(ENCODING)


def test_removing_over_element_borders(format_cls):
    format_cls.add_alter(0, 20, "")
    format_cls.apply_alters()
    assert format_cls.text == "… macht mich glücklich"
    assert format_cls.bytes == '<div class="foo"><h1></h1>\n' "<p>… macht mich glücklich</p></div>".encode(ENCODING)


def test_replacing_over_element_borders(format_cls):
    format_cls.add_alter(0, 20, "All content goes in the first element. ")
    format_cls.apply_alters()
    assert format_cls.text == "All content goes in the first element. … macht mich glücklich"
    assert (
        format_cls.bytes == '<div class="foo"><h1>All content goes in the first element. </h1>\n'
        "<p>… macht mich glücklich</p></div>".encode(ENCODING)
    )


def test_escaping_html_characters(format_cls):
    format_cls.add_alter(0, 6, "<Language>")
    format_cls.apply_alters()
    assert format_cls.text == "<Language> paragraph\n1. … macht mich glücklich"
    assert (
        format_cls.bytes == '<div class="foo"><h1>&lt;Language&gt; paragraph</h1>\n'
        "<p>1. … macht mich glücklich</p></div>".encode(ENCODING)
    )


def test_umlauts(format_cls):
    format_cls.add_alter(20, 21, "Ein Äffchen")
    format_cls.apply_alters()
    assert format_cls.text == "German paragraph\n1. Ein Äffchen macht mich glücklich"
    assert (
        format_cls.bytes == '<div class="foo"><h1>German paragraph</h1>\n'
        "<p>1. Ein Äffchen macht mich glücklich</p></div>".encode(ENCODING)
    )


def test_chained_alterations(format_cls):
    format_cls.add_alter(33, 42, "froh")
    format_cls.add_alter(7, 19, "Paragraph:")
    format_cls.add_alter(0, 6, "Deutscher")
    format_cls.add_alter(20, 21, "Essen")
    format_cls.apply_alters()
    assert format_cls.text == "Deutscher Paragraph: Essen macht mich froh"
    assert format_cls.bytes == '<div class="foo"><h1>Deutscher Paragraph:</h1>\n' "<p> Essen macht mich froh</p></div>".encode(
        ENCODING
    )


def test_altering_html_body():
    html_bytes = (
        '<body class="bar"><div class="foo"><h1>German paragraph</h1>\n<p>1. … macht mich glücklich</p></div></body>'
    ).encode(ENCODING)
    format_cls = HtmlFormat()
    format_cls.load(html_bytes)
    print(format_cls.text)
    format_cls.add_alter(0, 6, "Deutscher")
    format_cls.add_alter(20, 21, "Essen")
    format_cls.apply_alters()
    assert format_cls.text == "Deutscher paragraph\n1. Essen macht mich glücklich"
    assert (
        format_cls.bytes == '<body class="bar"><div class="foo"><h1>Deutscher paragraph</h1>\n'
        "<p>1. Essen macht mich glücklich</p></div></body>".encode(ENCODING)
    )


def test_altering_html_document():
    html_bytes = """
<!DOCTYPE html>

<html class="client-nojs" dir="ltr" lang="de">
<head>
<meta charset="UTF-8"/>
<title>The title is not considered.</title>
<script>document.documentElement.className="client-js";</script>
<link href="//github.com" rel="dns-prefetch"/>
<!--[if lt IE 9]><script src="/w/lnjnsef4/3nklnfasldcnal.js"></script><![endif]-->
</head>
<body class="bar">
<div class="foo">
<h1>German paragraph</h1>
<p>1. … macht mich glücklich</p>
</div>
</body>
</html>""".encode(
        ENCODING
    )
    format_cls = HtmlFormat()
    format_cls.load(html_bytes)
    format_cls.add_alter(0, 6, "Deutscher")
    format_cls.add_alter(20, 21, "Essen")
    format_cls.apply_alters()
    assert format_cls.text == "Deutscher paragraph\n1. Essen macht mich glücklich"
    assert (
        format_cls.bytes
        == """
<!DOCTYPE html>

<html class="client-nojs" dir="ltr" lang="de">
<head>
<meta charset="UTF-8"/>
<title>The title is not considered.</title>
<script>document.documentElement.className="client-js";</script>
<link href="//github.com" rel="dns-prefetch"/>
<!--[if lt IE 9]><script src="/w/lnjnsef4/3nklnfasldcnal.js"></script><![endif]-->
</head>
<body class="bar">
<div class="foo">
<h1>Deutscher paragraph</h1>
<p>1. Essen macht mich glücklich</p>
</div>
</body>
</html>""".encode(
            ENCODING
        )
    )


def test_alter_file(test_files, tmp_path):
    file_path = test_files / "test.html"
    altered_file_path = test_files / "test_altered.html"
    tmp_out_path = tmp_path / "test_out.html"

    file_wrapper = FileWrapper(file_path)
    file_wrapper.add_alter(71, 102, "A new sentence.")
    file_wrapper.apply_alters()
    file_wrapper.save(tmp_out_path)

    assert filecmp.cmp(altered_file_path, tmp_out_path, shallow=False)
