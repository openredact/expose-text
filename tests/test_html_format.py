import pytest

from expose_text.formats._html import HtmlFormat, Mapper


@pytest.fixture
def raw_html():
    return '<div class="foo">\n<h1>German paragraph</h1>\n<p>1. Glücklich macht mich …\n</p>\n</div>'


@pytest.fixture()
def format_cls(raw_html):
    format_cls = HtmlFormat()
    format_cls.load(raw_html)
    return format_cls


def test_text_property(format_cls, raw_html):
    assert format_cls.text == "German paragraph 1. Glücklich macht mich …"


def test_raw_property(format_cls):
    assert format_cls.raw == '<div class="foo">\n<h1>German paragraph</h1>\n<p>1. Glücklich macht mich …\n</p>\n</div>'


def test_unescaping_html():
    raw_html = '<div class="foo">\n<h1>&lt;&gt;&amp;</h1>\n<p>Gl&uuml;cklich macht mich &hellip;\n</p>\n</div>'
    format_cls = HtmlFormat()
    format_cls.load(raw_html)
    assert format_cls.raw == '<div class="foo">\n<h1>&lt;&gt;&amp;</h1>\n<p>Glücklich macht mich …\n</p>\n</div>'


def test_same_length_replacing(format_cls):
    format_cls.add_alter(0, 6, "XXXXXX")
    format_cls.apply_alters()
    assert format_cls.text == "XXXXXX paragraph 1. Glücklich macht mich …"
    assert format_cls.raw == '<div class="foo">\n<h1>XXXXXX paragraph</h1>\n<p>1. Glücklich macht mich …\n</p>\n</div>'


def test_replacing_with_longer_text(format_cls):
    format_cls.add_alter(0, 6, "XXXXXXXXX")
    format_cls.apply_alters()
    assert format_cls.text == "XXXXXXXXX paragraph 1. Glücklich macht mich …"
    assert format_cls.raw == '<div class="foo">\n<h1>XXXXXXXXX paragraph</h1>\n<p>1. Glücklich macht mich …\n</p>\n</div>'


def test_replacing_with_shorter_text(format_cls):
    format_cls.add_alter(0, 6, "XXX")
    format_cls.apply_alters()
    assert format_cls.text == "XXX paragraph 1. Glücklich macht mich …"
    assert format_cls.raw == '<div class="foo">\n<h1>XXX paragraph</h1>\n<p>1. Glücklich macht mich …\n</p>\n</div>'


def test_removing_text(format_cls):
    format_cls.add_alter(0, 7, "")
    format_cls.apply_alters()
    assert format_cls.text == "paragraph 1. Glücklich macht mich …"
    assert format_cls.raw == '<div class="foo">\n<h1>paragraph</h1>\n<p>1. Glücklich macht mich …\n</p>\n</div>'


def test_removing_entire_tag(format_cls):
    format_cls.add_alter(0, 16, "")
    format_cls.apply_alters()
    assert format_cls.text == " 1. Glücklich macht mich …"
    assert format_cls.raw == '<div class="foo">\n<h1></h1>\n<p>1. Glücklich macht mich …\n</p>\n</div>'


def test_alterations_longer_than_tags(format_cls):
    format_cls.add_alter(0, 20, "")
    format_cls.apply_alters()
    assert format_cls.text == "Glücklich macht mich …"
    assert format_cls.raw == '<div class="foo">\n<h1></h1>\n<p>Glücklich macht mich …\n</p>\n</div>'


def test_html_characters(format_cls):
    format_cls.add_alter(0, 6, "<Language>")
    format_cls.apply_alters()
    assert format_cls.text == "<Language> paragraph 1. Glücklich macht mich …"
    assert (
        format_cls.raw == '<div class="foo">\n<h1>&lt;Language&gt; paragraph</h1>\n<p>1. Glücklich macht mich …\n</p>\n</div>'
    )


def test_umlauts(format_cls):
    format_cls.add_alter(41, 42, "ein Äffchen")
    format_cls.apply_alters()
    assert format_cls.text == "German paragraph 1. Glücklich macht mich ein Äffchen"
    assert (
        format_cls.raw == '<div class="foo">\n<h1>German paragraph</h1>\n<p>1. Glücklich macht mich ein Äffchen\n</p>\n</div>'
    )


def test_chained_alterations(format_cls):
    format_cls.add_alter(30, 40, "bin ich mit")
    format_cls.add_alter(0, 6, "Deutscher")
    format_cls.add_alter(7, 19, "Paragraph:")
    format_cls.add_alter(41, 42, "Essen")
    format_cls.apply_alters()
    assert format_cls.text == "Deutscher Paragraph: Glücklich bin ich mit Essen"
    assert format_cls.raw == '<div class="foo">\n<h1>Deutscher Paragraph:</h1>\n<p> Glücklich bin ich mit Essen\n</p>\n</div>'


def test_mapper_text_to_html_index(raw_html):
    mapper = Mapper(raw_html)
    assert raw_html[50:59] == mapper.text[20:29]
    assert mapper.text_to_html_index(20) == 50
    assert mapper.text_to_html_index(29) == 59
