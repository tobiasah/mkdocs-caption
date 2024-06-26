"""Handle table related captioning."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lxml import etree

from mkdocs_caption.helper import (
    CaptionInfo,
    TreeElement,
    iter_caption_elements,
    wrap_md_captions,
)

if TYPE_CHECKING:
    from mkdocs.structure.pages import Page

    from mkdocs_caption.config import IdentifierCaption
    from mkdocs_caption.logger import PluginLogger
    from mkdocs_caption.post_processor import PostProcessor

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
    return wrap_md_captions(
        markdown,
        identifier=identifier,
        html_tag=TABLE_CAPTION_TAG,
        allow_indented_caption=config.allow_indented_caption,
    )


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
    caption_info: CaptionInfo,
    *,
    index: int,
    config: IdentifierCaption,
    logger: PluginLogger,
) -> str | None:
    """Add a caption to a table element in an XML tree.

    This function takes an XML tree, a table element, a caption element, and an
    index, and adds a caption to the table element based on the caption element
    and index.

    Args:
        caption_info: Caption info
        tree: The root element of the XML tree.
        index: The index of the table element.
        config: The plugin configuration.
        logger: Current plugin logger.
    """
    caption_prefix = config.get_caption_prefix(index=index, identifier="table")
    try:
        table_caption_element = etree.fromstring(
            str(
                f'<caption style="caption-side:{config.position}">'
                f"{caption_prefix} {caption_info.caption}</caption>",
            ),
        )
    except etree.XMLSyntaxError:
        logger.error(
            'Invalid XML in caption: <caption style="caption-side:%s">%s %s</caption>',
            config.position,
            caption_prefix,
            caption_info.caption,
        )
        return None
    caption_info.target_element.insert(0, table_caption_element)

    if "cols" in caption_info.attributes:
        caption_info.target_element.insert(
            0,
            _create_colgroups(caption_info.attributes["cols"]),
        )
        caption_info.attributes.pop("cols")
    caption_info.target_element.attrib.update(caption_info.attributes)
    table_id = caption_info.target_element.attrib.get(
        "id",
        config.get_default_id(index=index, identifier="table"),
    )
    caption_info.target_element.attrib["id"] = table_id
    return table_id


def postprocess_html(
    *,
    tree: TreeElement,
    config: IdentifierCaption,
    page: Page,
    post_processor: PostProcessor,
    logger: PluginLogger,
) -> None:
    """Handle custom captions in an XML tree.

    This function takes an XML tree and replaces all custom captions in the tree
    with custom HTML tags.

    Args:
        tree: The root element of the XML tree.
        config: The plugin configuration.
        page: The current page.
        post_processor: The post processor to register targets.
        logger: Current plugin logger.
    """
    if not config.enable:
        return
    index = config.start_index
    for caption_info in iter_caption_elements(TABLE_CAPTION_TAG, tree):
        if caption_info.target_element.tag != "table":
            logger.error(
                "Table caption must be followed by a table element. Skipping: %s",
                caption_info.caption,
            )
            continue
        table_id = _add_caption_to_table(
            caption_info=caption_info,
            index=index,
            config=config,
            logger=logger,
        )
        if table_id is None:
            continue
        post_processor.register_target(
            table_id,
            config.get_reference_text(index=index, identifier="table"),
            page,
        )
        index += config.increment_index
