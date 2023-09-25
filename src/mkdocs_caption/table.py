"""Handle table related captioning."""
from __future__ import annotations

from typing import TYPE_CHECKING

from lxml import etree

from mkdocs_caption.helper import (
    TreeElement,
    sanitize_caption,
    update_references,
    wrap_md_captions,
)

if TYPE_CHECKING:
    from mkdocs_caption.config import IdentifierCaption
    from mkdocs_caption.logger import PluginLogger

TABLE_CAPTION_TAG = "table-caption"


def preprocess_markdown(markdown: str, *, config: IdentifierCaption) -> str:
    """Preprocess markdown to wrap custom captions.

    The custom captions are wrapped in a custom html
    tag to make them easier to find later.

    Args:
        markdown: markdown string
        config: plugin configuration for tables

    Returns:
        markdown string with custom captions wrapped
    """
    if not config.enable:
        return markdown
    identifier = config.get_markdown_identifier("table")
    return wrap_md_captions(markdown, identifier=identifier, html_tag=TABLE_CAPTION_TAG)


def _create_colgroups(coldef: str) -> TreeElement:
    """Create a html colgroups element from a column definition.

    A coldef is a comma separated list of integers that specify the width of
    each column. The width can be specified in any unit, but the total width
    is treated as 100%.

    Args:
        coldef: comma separated list of column widths

    Returns:
        colgroups element
    """
    widths = [int(x) for x in coldef.split(",")]
    total = sum(widths)
    colgroup = etree.Element("colgroup", None, None)
    for width in widths:
        col = etree.Element("col", {"span": "1", "width": f"{width/total*100}%"}, None)
        colgroup.append(col)
    return colgroup


def _add_caption_to_table(
    table_element: TreeElement,
    *,
    tree: TreeElement,
    caption_element: TreeElement,
    index: int,
    config: IdentifierCaption,
    logger: PluginLogger,
) -> None:
    """Add a caption to a table element in an XML tree.

    This function takes an XML tree, a table element, a caption element, and an
    index, and adds a caption to the table element based on the caption element
    and index.

    Args:
        table_element: The table element to add the caption to.
        tree: The root element of the XML tree.
        caption_element: The caption element to use for the caption text.
        index: The index of the table element.
        config: The plugin configuration.
        logger: Current plugin logger.
    """
    caption_prefix = config.get_caption_prefix(index=index, identifier="table")
    caption_text = sanitize_caption(caption_element.text)
    try:
        table_caption_element = etree.fromstring(
            str(
                f'<caption style="caption-side:{config.position}">'
                f"{caption_prefix} {caption_text}</caption>",
            ),
        )
    except etree.XMLSyntaxError:
        logger.error(
            'Invalid XML in caption: <caption style="caption-side:%s">%s %s</caption>',
            config.position,
            caption_prefix,
            caption_text,
        )
        return
    table_element.insert(0, table_caption_element)

    if "cols" in caption_element.attrib:
        table_element.insert(0, _create_colgroups(caption_element.attrib["cols"]))
        caption_element.attrib.pop("cols")
    table_element.attrib.update(caption_element.attrib)
    table_id = table_element.attrib.get(
        "id",
        config.get_default_id(index=index, identifier="table"),
    )
    table_element.attrib["id"] = table_id
    update_references(
        tree,
        table_id,
        config.get_reference_text(index=index, identifier="table"),
    )


def postprocess_html(
    *,
    tree: TreeElement,
    config: IdentifierCaption,
    logger: PluginLogger,
) -> None:
    """Handle custom captions in an XML tree.

    This function takes an XML tree and replaces all custom captions in the tree
    with custom HTML tags.

    Args:
        tree: The root element of the XML tree.
        config: The plugin configuration.
        logger: Current plugin logger.
    """
    if not config.enable:
        return
    index = config.start_index
    for table_caption in tree.xpath(f"//{TABLE_CAPTION_TAG}"):
        a_wrapper = table_caption.getparent()
        target_element = a_wrapper.getnext()
        if target_element.tag != "table":
            logger.error(
                "Table caption must be followed by a table element. Skipping: %s",
                table_caption.text,
            )
            continue
        # unused attribute identifier
        table_caption.attrib.pop("identifier")

        _add_caption_to_table(
            target_element,
            tree=tree,
            caption_element=table_caption,
            index=index,
            config=config,
            logger=logger,
        )
        a_wrapper.remove(table_caption)
        a_wrapper.getparent().remove(a_wrapper)
        index += config.increment_index
