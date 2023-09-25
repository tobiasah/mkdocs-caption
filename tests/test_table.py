"""Tests for the image module."""
from lxml import etree

from mkdocs_caption import table
from mkdocs_caption.config import IdentifierCaption
from mkdocs_caption.logger import get_logger


def test_preprocess_disabled():
    config = IdentifierCaption()
    config.enable = False
    markdown = """\
This is a test
hkjbnk

Table: My Caption

hjkhjk
    """
    assert table.preprocess_markdown(markdown, config=config) == markdown


def test_preprocess_no_identifier():
    config = IdentifierCaption()
    markdown = """\
This is a test
hkjbnk
hjkhjk
    """
    assert table.preprocess_markdown(markdown, config=config) == markdown


def test_preprocess_default_identifier_inline():
    config = IdentifierCaption()
    markdown = """\
This is a test
hkjbnk
Table: My Caption
hjkhjk
    """
    assert table.preprocess_markdown(markdown, config=config) == markdown


def test_preprocess_default_identifier():
    config = IdentifierCaption()
    markdown = """\
This is a test
hkjbnk

Table: My Caption

hjkhjk
    """
    result = table.preprocess_markdown(markdown, config=config)
    assert '<table-caption identifier="Table">My Caption</table-caption>' in result


def test_preprocess_options_ok():
    config = IdentifierCaption()
    markdown = """\
This is a test
hkjbnk

Table: My Caption {#myid .myclass tester="test"}

hjkhjk
    """
    result = table.preprocess_markdown(markdown, config=config)
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
    result = table.preprocess_markdown(markdown, config=config)
    assert '<table-caption identifier="Custom&">My Caption</table-caption>' in result


def test_preprocess_custom_ignores_default_identifier():
    config = IdentifierCaption()
    config.markdown_identifier = "Custom&"
    markdown = """\
This is a test
hkjbnk

Table: My Caption

hjkhjk
    """
    assert table.preprocess_markdown(markdown, config=config) == markdown


def test_preprocess_multiple():
    config = IdentifierCaption()
    markdown = """\
This is a test

Table: First

hkjbnk

Table: My Caption

hjkhjk
    """
    result = table.preprocess_markdown(markdown, config=config)
    assert '<table-caption identifier="Table">My Caption</table-caption>' in result
    assert '<table-caption identifier="Table">First</table-caption>' in result


def div(*args):
    return f'<div>{"".join(args)}</div>'


def a(*args):
    return f'<a>{"".join(args)}</a>'


DEFAULT_TABLE = str(
    '<table><thead><tr><th colspan="2">logo</th></tr></thead><tbody><tr>'
    '<td colspan="2">type</td></tr><tr><td>html</td><td>pdf</td></tr></tbody></table>',
)

DEFAULT_TABLE_CAPTION = '<table-caption identifier="Table">My Caption</table-caption>'


def test_postprocess_disabled():
    config = IdentifierCaption()
    config.enable = False
    html = div(a(DEFAULT_TABLE_CAPTION), DEFAULT_TABLE)
    tree = etree.fromstring(html)
    table.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    assert result == html


def test_postprocess_no_identifier():
    config = IdentifierCaption()
    html = div(a("caption"), DEFAULT_TABLE)
    tree = etree.fromstring(html)
    table.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    assert result == html


def test_postprocess_default_identifier():
    config = IdentifierCaption()
    html = div(a(DEFAULT_TABLE_CAPTION), DEFAULT_TABLE)
    tree = etree.fromstring(html)
    table.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    assert (
        '<caption style="caption-side:bottom">Table 1: My Caption</caption>' in result
    )


def test_postprocess_multiple():
    config = IdentifierCaption()
    caption1 = '<table-caption identifier="Table">First</table-caption>'
    caption2 = '<table-caption identifier="Table">Second</table-caption>'
    html = div(div(a(caption1), DEFAULT_TABLE), div(a(caption2), DEFAULT_TABLE))
    tree = etree.fromstring(html)
    table.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    assert '<caption style="caption-side:bottom">Table 1: First</caption>' in result
    assert '<caption style="caption-side:bottom">Table 2: Second</caption>' in result


def test_postprocess_custom_start_index():
    config = IdentifierCaption()
    config.start_index = 10
    html = div(a(DEFAULT_TABLE_CAPTION), DEFAULT_TABLE)
    tree = etree.fromstring(html)
    table.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    assert (
        '<caption style="caption-side:bottom">Table 10: My Caption</caption>' in result
    )


def test_postprocess_custom_increment():
    config = IdentifierCaption()
    config.increment_index = 10
    caption1 = '<table-caption identifier="Table">First</table-caption>'
    caption2 = '<table-caption identifier="Table">Second</table-caption>'
    html = div(div(a(caption1), DEFAULT_TABLE), div(a(caption2), DEFAULT_TABLE))
    tree = etree.fromstring(html)
    table.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    assert '<caption style="caption-side:bottom">Table 1: First</caption>' in result
    assert '<caption style="caption-side:bottom">Table 11: Second</caption>' in result


def test_postprocess_position():
    config = IdentifierCaption()
    config.position = "top"
    html = div(a(DEFAULT_TABLE_CAPTION), DEFAULT_TABLE)
    tree = etree.fromstring(html)
    table.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    assert '<caption style="caption-side:top">Table 1: My Caption</caption>' in result

    config.position = "bottom"
    tree = etree.fromstring(html)
    table.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    assert (
        '<caption style="caption-side:bottom">Table 1: My Caption</caption>' in result
    )


def test_postprocess_default_id():
    config = IdentifierCaption()
    html = div(a(DEFAULT_TABLE_CAPTION), DEFAULT_TABLE)
    tree = etree.fromstring(html)
    table.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    assert 'id="_table-1"' in result


def test_postprocess_custom_id():
    config = IdentifierCaption()
    config.default_id = "custom-{identifier}-{index}"
    html = div(a(DEFAULT_TABLE_CAPTION), DEFAULT_TABLE)
    tree = etree.fromstring(html)
    table.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    assert 'id="custom-table-1"' in result

    config.default_id = "test-{index}"
    tree = etree.fromstring(html)
    table.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    assert 'id="test-1"' in result


def test_postprocess_custom_caption_prefix():
    config = IdentifierCaption()
    config.caption_prefix = "custom {identifier} {index}:"
    html = div(a(DEFAULT_TABLE_CAPTION), DEFAULT_TABLE)
    tree = etree.fromstring(html)
    table.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    assert (
        '<caption style="caption-side:bottom">custom table 1: My Caption</caption>'
        in result
    )


def test_postprocess_default_reference():
    config = IdentifierCaption()
    reference_element = '<a href="#_table-1"></a>'
    html = div(a(DEFAULT_TABLE_CAPTION), DEFAULT_TABLE, div(reference_element))
    tree = etree.fromstring(html)
    table.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    assert '<a href="#_table-1">Table 1</a>' in result


def test_postprocess_ignore_reference_with_text():
    config = IdentifierCaption()
    reference_element = '<a href="#_table-1">Test</a>'
    html = div(a(DEFAULT_TABLE_CAPTION), DEFAULT_TABLE, div(reference_element))
    tree = etree.fromstring(html)
    table.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    assert '<a href="#_table-1">Test</a>' in result


def test_postprocess_custom_reference():
    config = IdentifierCaption()
    config.reference_text = "custom {identifier} {index}"
    reference_element = '<a href="#_table-1"></a>'
    html = div(a(DEFAULT_TABLE_CAPTION), DEFAULT_TABLE, div(reference_element))
    tree = etree.fromstring(html)
    table.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    assert '<a href="#_table-1">custom table 1</a>' in result


def test_colgroups():
    config = IdentifierCaption()
    caption = '<table-caption identifier="Table" cols="1,3">My Caption</table-caption>'
    html = div(a(caption), DEFAULT_TABLE)
    tree = etree.fromstring(html)
    table.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    assert (
        '<colgroup><col span="1" width="25.0%"><col span="1" width="75.0%"></colgroup>'
        in result
    )


def test_colgroups_alsways_100_percent():
    config = IdentifierCaption()
    caption = (
        '<table-caption identifier="Table" cols="456,85">My Caption</table-caption>'
    )
    html = div(a(caption), DEFAULT_TABLE)
    tree = etree.fromstring(html)
    table.postprocess_html(tree=tree, config=config, logger=None)
    result = etree.tostring(tree, encoding="unicode", method="html")
    assert (
        str(
            '<colgroup><col span="1" width="84.28835489833642%">'
            '<col span="1" width="15.711645101663585%"></colgroup>',
        )
        in result
    )


def test_table_caption_without_table(caplog):
    config = IdentifierCaption()
    html = div(a(DEFAULT_TABLE_CAPTION), a("I am a table"))
    tree = etree.fromstring(html)
    logger = get_logger("test.md")
    with caplog.at_level("ERROR"):
        table.postprocess_html(tree=tree, config=config, logger=logger)
    assert "ERROR" in caplog.text
    result = etree.tostring(tree, encoding="unicode", method="html")
    assert result == html


def test_table_caption_with_xml(caplog):
    config = IdentifierCaption()
    config.caption_prefix = "<not nice> {index}:"

    caption = '<table-caption identifier="Table">My Caption</table-caption>'

    html = div(a(caption), DEFAULT_TABLE)
    tree = etree.fromstring(html)
    logger = get_logger("test.md")
    with caplog.at_level("ERROR"):
        table.postprocess_html(tree=tree, config=config, logger=logger)
    assert "ERROR" in caplog.text
    result = etree.tostring(tree, encoding="unicode", method="html")
    assert result == div(DEFAULT_TABLE)
