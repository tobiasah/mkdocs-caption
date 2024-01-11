"""Tests for the image module."""

from lxml import etree

from mkdocs_caption import image
from mkdocs_caption.config import FigureCaption
from mkdocs_caption.logger import get_logger


def test_preprocess_disabled():
    config = FigureCaption()
    config.enable = False
    markdown = """\
This is a test
hkjbnk

Figure: My Caption

hjkhjk
    """
    assert image.preprocess_markdown(markdown, config=config) == markdown


def test_preprocess_no_identifier():
    config = FigureCaption()
    markdown = """\

This is a test
hkjbnk
hjkhjk
    """
    assert image.preprocess_markdown(markdown, config=config) == markdown


def test_preprocess_intended():
    config = FigureCaption()
    markdown = """\
    This is a test
    hkjbnk

    Figure: My Caption

    hjkhjk
    """
    result = image.preprocess_markdown(markdown, config=config)
    assert (
        '    <figure-caption identifier="Figure">My Caption</figure-caption>' in result
    )


def test_preprocess_intended_disabled():
    config = FigureCaption()
    config.allow_indented_caption = False
    markdown = """\
    This is a test
    hkjbnk

    Figure: My Caption

    hjkhjk
    """
    assert image.preprocess_markdown(markdown, config=config) == markdown


def test_preprocess_default_identifier_inline():
    config = FigureCaption()
    markdown = """\
This is a test
hkjbnk
Figure: My Caption
hjkhjk
    """
    assert image.preprocess_markdown(markdown, config=config) == markdown


def test_preprocess_default_identifier():
    config = FigureCaption()
    markdown = """\
This is a test
hkjbnk

Figure: My Caption

hjkhjk
    """
    result = image.preprocess_markdown(markdown, config=config)
    assert '<figure-caption identifier="Figure">My Caption</figure-caption>' in result


def test_preprocess_default_identifier_indent():
    config = FigureCaption()
    markdown = """\
This is a test
hkjbnk

    Figure: My Caption

hjkhjk
    """
    result = image.preprocess_markdown(markdown, config=config)
    assert (
        '    <figure-caption identifier="Figure">My Caption</figure-caption>' in result
    )


def test_preprocess_options_ok():
    config = FigureCaption()
    markdown = """\
This is a test
hkjbnk

Figure: My Caption {#myid .myclass tester="test"}

hjkhjk
    """
    result = image.preprocess_markdown(markdown, config=config)
    assert "id=myid" in result
    assert "class=myclass" in result
    assert 'tester="test"' in result


def test_preprocess_custom_identifier():
    config = FigureCaption()
    config.markdown_identifier = "Custom&"
    markdown = """\
This is a test
hkjbnk

Custom& My Caption

hjkhjk
    """
    result = image.preprocess_markdown(markdown, config=config)
    assert '<figure-caption identifier="Custom&">My Caption</figure-caption>' in result


def test_preprocess_custom_ignores_default_identifier():
    config = FigureCaption()
    config.markdown_identifier = "Custom&"
    markdown = """\

This is a test
hkjbnk

Figure: My Caption

hjkhjk
    """
    assert image.preprocess_markdown(markdown, config=config) == markdown


def test_preprocess_multiple():
    config = FigureCaption()
    markdown = """\
This is a test

Figure: First

hkjbnk

Figure: My Caption

hjkhjk
    """
    result = image.preprocess_markdown(markdown, config=config)
    assert '<figure-caption identifier="Figure">My Caption</figure-caption>' in result
    assert '<figure-caption identifier="Figure">First</figure-caption>' in result


def p(*args):
    return f'<p>{"".join(args)}</p>'


def a(*args):
    return f'<a>{"".join(args)}</a>'


DEFAULT_IMG = '<img id="test" src="test.png" alt="Test">'

DEFAULT_FIGURE_CAPTION = (
    '<figure-caption identifier="Figure">My Caption</figure-caption>'
)


def test_postprocess_disabled():
    config = FigureCaption()
    config.enable = False
    html = p(a(DEFAULT_FIGURE_CAPTION), DEFAULT_IMG)
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    image.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert result == html


def test_postprocess_no_identifier():
    config = FigureCaption()
    html = p(a("caption"), '<img id="test" src="test.png">')
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    image.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert result == html


def test_postprocess_shortcut_extendet_syntax():
    config = FigureCaption()
    img_with_caption = '<img id="test" src="test.png" alt="Test" title="My Caption">'
    html = p(a(DEFAULT_FIGURE_CAPTION), img_with_caption)
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    image.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert "</figure>" in result
    assert "<figcaption>Figure 1: My Caption</figcaption>" in result
    # title attribute is removed
    assert '<img id="test" src="test.png" alt="Test">' in result


def test_postprocess_shortcut_extendet_syntax_alt_text():
    config = FigureCaption()
    img_with_caption = '<img id="test" src="test.png" alt="Test">'
    html = p(a(DEFAULT_FIGURE_CAPTION), img_with_caption)
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    image.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert "</figure>" in result
    assert "<figcaption>Figure 1: My Caption</figcaption>" in result
    # alt is preserved
    assert '<img id="test" src="test.png" alt="Test">' in result


def test_postprocess_default_identifier():
    config = FigureCaption()
    html = p(a(DEFAULT_FIGURE_CAPTION), DEFAULT_IMG)
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    image.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert "</figure>" in result
    assert "<figcaption>Figure 1: My Caption</figcaption>" in result


def test_postprocess_multiple():
    config = FigureCaption()
    caption1 = '<figure-caption identifier="Figure">First</figure-caption>'
    caption2 = '<figure-caption identifier="Figure">Second</figure-caption>'

    html = p(
        p(a(caption1), DEFAULT_IMG),
        p(a(caption2), '<img id="test2" src="test2.png" alt="Test2">'),
    )
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    image.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert "<figcaption>Figure 1: First</figcaption>" in result
    assert "<figcaption>Figure 2: Second</figcaption>" in result


def test_postprocess_multiple_nested():
    config = FigureCaption()
    caption1 = '<figure-caption identifier="Figure">First</figure-caption>'
    caption2 = '<figure-caption identifier="Figure">Second</figure-caption>'

    html = p(
        p(a(caption1), a(DEFAULT_IMG)),
        p(a(caption2), a(p('<img id="test2" src="test2.png" alt="Test2">'))),
    )
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    image.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert "<figcaption>Figure 1: First</figcaption>" in result
    assert "<figcaption>Figure 2: Second</figcaption>" in result


def test_postprocess_custom_start_index():
    config = FigureCaption()
    config.start_index = 10
    html = p(a(DEFAULT_FIGURE_CAPTION), DEFAULT_IMG)
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    image.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert "<figcaption>Figure 10: My Caption</figcaption>" in result


def test_postprocess_custom_increment():
    config = FigureCaption()
    config.increment_index = 10
    caption1 = '<figure-caption identifier="Figure">First</figure-caption>'
    caption2 = '<figure-caption identifier="Figure">Second</figure-caption>'
    html = p(p(a(caption1), DEFAULT_IMG), p(a(caption2), DEFAULT_IMG))
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    image.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert "<figcaption>Figure 1: First</figcaption>" in result
    assert "<figcaption>Figure 11: Second</figcaption>" in result


def test_postprocess_position():
    config = FigureCaption()
    config.position = "top"
    html = p(a(DEFAULT_FIGURE_CAPTION), DEFAULT_IMG)
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    image.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert "</figcaption><img" in result

    config.position = "bottom"
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    image.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert 'alt="Test"><figcaption>' in result


def test_postprocess_default_id():
    config = FigureCaption()
    html = p(a(DEFAULT_FIGURE_CAPTION), DEFAULT_IMG)
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    image.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert 'id="_figure-1"' in result


def test_postprocess_custom_id():
    config = FigureCaption()
    config.default_id = "custom-{identifier}-{index}"
    html = p(a(DEFAULT_FIGURE_CAPTION), DEFAULT_IMG)
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    image.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert 'id="custom-figure-1"' in result

    config.default_id = "test-{index}"
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    image.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert 'id="test-1"' in result


def test_postprocess_custom_caption_prefix():
    config = FigureCaption()
    config.caption_prefix = "custom {identifier} {index}:"
    html = p(a(DEFAULT_FIGURE_CAPTION), DEFAULT_IMG)
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    image.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert "<figcaption>custom figure 1: My Caption</figcaption>" in result


def test_postprocess_default_reference():
    config = FigureCaption()
    reference_element = '<a href="#_figure-1"></a>'
    html = p(a(DEFAULT_FIGURE_CAPTION), DEFAULT_IMG, p(reference_element))
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    image.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert '<a href="#_figure-1">Figure 1</a>' in result


def test_postprocess_ignore_reference_with_text():
    config = FigureCaption()
    reference_element = '<a href="#_figure-1">Test</a>'
    html = p(a(DEFAULT_FIGURE_CAPTION), DEFAULT_IMG, p(reference_element))
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    image.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # HTMLParser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert '<a href="#_figure-1">Test</a>' in result


def test_postprocess_custom_reference():
    config = FigureCaption()
    config.reference_text = "custom {identifier} {index}"
    reference_element = '<a href="#_figure-1"></a>'
    html = p(a(DEFAULT_FIGURE_CAPTION), DEFAULT_IMG, p(reference_element))
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    image.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # htmlparser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert '<a href="#_figure-1">custom figure 1</a>' in result


def test_figure_caption_with_no_img(caplog):
    config = FigureCaption()
    img = '<img id="test" src="test.png">'
    html = p(a(DEFAULT_FIGURE_CAPTION), a(p("hell0")), img)
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    logger = get_logger("test.md")
    with caplog.at_level("ERROR"):
        image.postprocess_html(tree=tree, config=config, logger=logger)
    assert "ERROR" in caplog.text
    result = etree.tostring(tree, encoding="unicode", method="html")
    # htmlparser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert result == html


def test_figure_caption_with_xml(caplog):
    config = FigureCaption()
    img = '<img id="test" src="test.png" title="<hello>This is not nice"'
    html = p(img)
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    logger = get_logger("test.md")
    with caplog.at_level("ERROR"):
        image.postprocess_html(tree=tree, config=config, logger=logger)
    assert "ERROR" in caplog.text
    result = etree.tostring(tree, encoding="unicode", method="html")
    # htmlparser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    assert result == '<p><img id="test" src="test.png"></p>'


def test_figure_caption_ignores_inline():
    config = FigureCaption()
    img = 'Hello <img id="test" src="test.png" alt="alt text"> you'
    html = p(img)
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    logger = get_logger("test.md")
    image.postprocess_html(tree=tree, config=config, logger=logger)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # htmlparser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    result = result[len("<p>") : -len("</p>")]
    assert result == img


def test_figure_caption_ignores_alt_if_disabled():
    config = FigureCaption()
    config.ignore_alt = True
    img = '<img id="test" src="test.png" alt="alt text">'
    html = p(img)
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    logger = get_logger("test.md")
    image.postprocess_html(tree=tree, config=config, logger=logger)
    result = etree.tostring(tree, encoding="unicode", method="html")
    # htmlparser adds <html><body> tags, remove them
    result = result[len("<html><body>") : -len("</body></html>")]
    result = result[len("<p>") : -len("</p>")]
    assert result == img
