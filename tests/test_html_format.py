import pytest

from expose_text.formats._html import HtmlFormat, Mapper


@pytest.fixture
def raw_html():
    return '<div class="foo">\n<h1>German paragraph</h1>\n<p>1. Gl&uuml;cklich macht mich &hellip;\n</p>\n</div>'


@pytest.fixture()
def format_cls(raw_html):
    format_cls = HtmlFormat()
    format_cls.load(raw_html)
    return format_cls


def test_text_property(format_cls, raw_html):
    assert format_cls.text == "German paragraph 1. Glücklich macht mich …"


def test_raw_property(format_cls, raw_html):
    assert format_cls.raw == raw_html


def test_simple_replacing(format_cls):
    format_cls.add_alter(17, 18, "2")
    format_cls.apply_alters()
    assert format_cls.text == "German paragraph 2. Glücklich macht mich …"
    assert (
        format_cls.raw
        == '<div class="foo">\n<h1>German paragraph</h1>\n<p>2. Gl&uuml;cklich macht mich &hellip;\n</p>\n</div>'
    )


@pytest.mark.skip(reason="This is still broken")
def test_removing(format_cls):
    format_cls.add_alter(0, 20, "")
    format_cls.apply_alters()
    assert format_cls.text == "Glücklich macht mich …"
    assert format_cls.raw == '<div class="foo">\n<h1></h1>\n<p>2. Gl&uuml;cklich macht mich &hellip;\n</p>\n</div>'


@pytest.mark.skip(reason="This is still broken")
def test_umlauts(format_cls):
    format_cls.add_alter(0, 20, "Äffchen")
    format_cls.apply_alters()
    assert format_cls.text == "Äffchen 1. Glücklich macht mich …"
    assert format_cls.raw == '<div class="foo">\n<h1>&Auml;ffchen</h1>\n<p>2. Gl&uuml;cklich macht mich &hellip;\n</p>\n</div>'


@pytest.mark.skip(reason="This is still broken")
def test_chained_alterations(format_cls):
    format_cls.add_alter(17, 19, "")
    format_cls.add_alter(0, 16, "Deutscher Paragraph:")
    format_cls.add_alter(42, 43, "Essen")
    format_cls.apply_alters()
    assert (
        format_cls.raw
        == '<div class="foo">\n<h1>Deutscher Paragraph</h1>\n<p>2. Gl&uuml;cklich macht mich &hellip;\n</p>\n</div>'
    )


def test_mapper_text_to_html_index(raw_html):
    mapper = Mapper(raw_html)
    assert mapper.text[20:29] == "Glücklich"
    assert raw_html[50:64] == "Gl&uuml;cklich"
    assert mapper.text_to_html_index(20) == 50
    assert mapper.text_to_html_index(29) == 64
