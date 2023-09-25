"""Tests for the custom module."""
from lxml import etree

from mkdocs_caption import custom
from mkdocs_caption.config import IdentifierCaption
from mkdocs_caption.logger import get_logger


def test_preprocess_disabled():
    config = IdentifierCaption()
    config.enable = False
    markdown = """\
This is a test
hkjbnk

List: My Caption

hjkhjk
    """
    result = custom.preprocess_markdown(markdown, config=config, identifiers=["List"])
    assert result == markdown


def test_preprocess_no_identifier():
    config = IdentifierCaption()
    markdown = """\
This is a test
hkjbnk
hjkhjk
    """
    result = custom.preprocess_markdown(markdown, config=config, identifiers=["List"])
    assert result == markdown


def test_preprocess_default_identifier_inline():
    config = IdentifierCaption()
    markdown = """\
This is a test
hkjbnk
List: My Caption
hjkhjk
    """
    result = custom.preprocess_markdown(markdown, config=config, identifiers=["List"])
    assert result == markdown


def test_preprocess_default_identifier():
    config = IdentifierCaption()
    markdown = """\
This is a test
hkjbnk

List: My Caption

hjkhjk
    """
    result = custom.preprocess_markdown(markdown, config=config, identifiers=["List"])
    assert '<custom-caption identifier="List">My Caption</custom-caption>' in result


def test_preprocess_options_ok():
    config = IdentifierCaption()
    markdown = """\
This is a test
hkjbnk

List: My Caption {#myid .myclass tester="test"}

hjkhjk
    """
    result = custom.preprocess_markdown(markdown, config=config, identifiers=["List"])
    assert "id=myid" in result
    assert "class=myclass" in result
    assert 'tester="test"' in result


def test_preprocess_custom_identifier():
    config = IdentifierCaption()
    config.markdown_identifier = "Custom&"
    markdown = """\
This is a test
hkjbnk

Custom& My Caption

hjkhjk
    """
    result = custom.preprocess_markdown(markdown, config=config, identifiers=["List"])
    assert '<custom-caption identifier="Custom&">My Caption</custom-caption>' in result


def test_preprocess_custom_ignores_default_identifier():
    config = IdentifierCaption()
    config.markdown_identifier = "Custom&"
    markdown = """\
This is a test
hkjbnk

List: My Caption

hjkhjk
    """
    assert (
        custom.preprocess_markdown(markdown, config=config, identifiers=["List"])
        == markdown
    )


def test_preprocess_multiple():
    config = IdentifierCaption()
    markdown = """\
This is a test

List: First

hkjbnk

List: My Caption

hjkhjk
    """
    result = custom.preprocess_markdown(markdown, config=config, identifiers=["List"])
    assert '<custom-caption identifier="List">My Caption</custom-caption>' in result
    assert '<custom-caption identifier="List">First</custom-caption>' in result


def test_preprocess_multiple_indentifier():
    config = IdentifierCaption()
    markdown = """\
This is a test

List: First

hkjbnk

Equation: My Caption

hjkhjk
    """
    result = custom.preprocess_markdown(
        markdown,
        config=config,
        identifiers=["List", "Equation"],
    )
    assert '<custom-caption identifier="Equation">My Caption</custom-caption>' in result
    assert '<custom-caption identifier="List">First</custom-caption>' in result


def p(*args):
    return f'<p>{"".join(args)}</p>'


def a(*args):
    return f'<a>{"".join(args)}</a>'


DEFAULT_INNER = "<span>Inner</span>"
DEFAULT_CAPTION = '<custom-caption identifier="List">My Caption</custom-caption>'


def test_postprocess_disabled():
    config = IdentifierCaption()
    config.enable = False
    html = p(a(DEFAULT_CAPTION), DEFAULT_INNER)
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    custom.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert result == html


def test_postprocess_no_identifier():
    config = IdentifierCaption()
    html = p(a("caption"), DEFAULT_INNER)
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    custom.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert result == html


def test_postprocess_default_identifier():
    config = IdentifierCaption()
    html = p(a(DEFAULT_CAPTION), DEFAULT_INNER)
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    custom.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert "</figure>" in result
    assert "<figcaption>List 1: My Caption</figcaption>" in result


def test_postprocess_multiple():
    config = IdentifierCaption()
    caption1 = '<custom-caption identifier="List">First</custom-caption>'
    caption2 = '<custom-caption identifier="List">Second</custom-caption>'

    html = p(
        p(a(caption1), DEFAULT_INNER),
        p(a(caption2), '<img id="test2" src="test2.png" alt="Test2">'),
    )
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    custom.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert "<figcaption>List 1: First</figcaption>" in result
    assert "<figcaption>List 2: Second</figcaption>" in result


def test_postprocess_multiple_nested():
    config = IdentifierCaption()
    caption1 = '<custom-caption identifier="List">First</custom-caption>'
    caption2 = '<custom-caption identifier="List">Second</custom-caption>'

    html = p(
        p(a(caption1), a(DEFAULT_INNER)),
        p(a(caption2), a(p('<img id="test2" src="test2.png" alt="Test2">'))),
    )
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    custom.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert "<figcaption>List 1: First</figcaption>" in result
    assert "<figcaption>List 2: Second</figcaption>" in result


def test_postprocess_custom_start_index():
    config = IdentifierCaption()
    config.start_index = 10
    html = p(a(DEFAULT_CAPTION), DEFAULT_INNER)
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    custom.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert "<figcaption>List 10: My Caption</figcaption>" in result


def test_postprocess_custom_increment():
    config = IdentifierCaption()
    config.increment_index = 10
    caption1 = '<custom-caption identifier="List">First</custom-caption>'
    caption2 = '<custom-caption identifier="List">Second</custom-caption>'
    html = p(p(a(caption1), DEFAULT_INNER), p(a(caption2), DEFAULT_INNER))
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    custom.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert "<figcaption>List 1: First</figcaption>" in result
    assert "<figcaption>List 11: Second</figcaption>" in result


def test_postprocess_position():
    config = IdentifierCaption()
    config.position = "top"
    html = p(a(DEFAULT_CAPTION), DEFAULT_INNER)
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    custom.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert "</figcaption><span" in result

    config.position = "bottom"
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    custom.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert "</span><figcaption>" in result


def test_postprocess_default_id():
    config = IdentifierCaption()
    html = p(a(DEFAULT_CAPTION), DEFAULT_INNER)
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    custom.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert 'id="_list-1"' in result


def test_postprocess_custom_id():
    config = IdentifierCaption()
    config.default_id = "custom-{identifier}-{index}"
    html = p(a(DEFAULT_CAPTION), DEFAULT_INNER)
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    custom.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert 'id="custom-list-1"' in result

    config.default_id = "test-{index}"
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    custom.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert 'id="test-1"' in result


def test_postprocess_custom_caption_prefix():
    config = IdentifierCaption()
    config.caption_prefix = "custom {identifier} {index}:"
    html = p(a(DEFAULT_CAPTION), DEFAULT_INNER)
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    custom.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert "<figcaption>custom list 1: My Caption</figcaption>" in result


def test_postprocess_default_reference():
    config = IdentifierCaption()
    reference_element = '<a href="#_list-1"></a>'
    html = p(a(DEFAULT_CAPTION), DEFAULT_INNER, p(reference_element))
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    custom.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert '<a href="#_list-1">List 1</a>' in result


def test_postprocess_ignore_reference_with_text():
    config = IdentifierCaption()
    reference_element = '<a href="#_list-1">Test</a>'
    html = p(a(DEFAULT_CAPTION), DEFAULT_INNER, p(reference_element))
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    custom.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert '<a href="#_list-1">Test</a>' in result


def test_postprocess_custom_reference():
    config = IdentifierCaption()
    config.reference_text = "custom {identifier} {index}"
    reference_element = '<a href="#_list-1"></a>'
    html = p(a(DEFAULT_CAPTION), DEFAULT_INNER, p(reference_element))
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    custom.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # htmlparser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert '<a href="#_list-1">custom list 1</a>' in result


def test_custom_caption_no_targe(caplog):
    config = IdentifierCaption()
    html = p(a(DEFAULT_CAPTION))
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    logger = get_logger("test.md")
    with caplog.at_level("ERROR"):
        custom.postprocess_html(tree=tree, config=config, logger=logger)
    assert "ERROR" in caplog.text
    result = etree.tostring(tree, encoding="unicode", method="html")
    # htmlparser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert result == "<p><a><custom-caption>My Caption</custom-caption></a></p>"


def test_custom_caption_with_xml(caplog):
    config = IdentifierCaption()
    config.caption_prefix = "<not nice> {index}:"
    caption = '<custom-caption identifier="List">My Caption</custom-caption>'
    html = p(a(caption), DEFAULT_INNER)
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    logger = get_logger("test.md")
    with caplog.at_level("ERROR"):
        custom.postprocess_html(tree=tree, config=config, logger=logger)
    assert "ERROR" in caplog.text
    result = etree.tostring(tree, encoding="unicode", method="html")
    # htmlparser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert result == str(
        "<p><a><custom-caption>My Caption</custom-caption></a>"
        "<figure></figure><span>Inner</span></p>",
    )
