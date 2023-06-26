import typing as t

from lxml import etree

from mkdocs_caption.config import IdentifierCaption
from mkdocs_caption.helper import update_references, wrap_md_captions
from mkdocs_caption.logger import PluginLogger

TABLE_CAPTION_TAG = "table-caption"


def preprocess_markdown(markdown: str, identifier: t.List[str]) -> str:
    """Preprocess markdown to wrap custom captions

    The custom captions are wrapped in a custom html
    tag to make them easier to find later.

    Args:
        markdown: markdown string

    Returns:
        markdown string with custom captions wrapped
    """
    return wrap_md_captions(markdown, identifier, TABLE_CAPTION_TAG)


def _create_colgroups(coldef: str) -> etree._Element:
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
    table_element: etree._Element,
    *,
    tree: etree._Element,
    caption_element: etree._Element,
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
    """
    caption_prefix = config.caption_prefix.format(index=index, identifier="Table")
    caption_text = (
        caption_element.text.replace(" & ", " &amp; ") if caption_element.text else ""
    )
    try:
        table_caption_element = etree.fromstring(
            f"<caption>{caption_prefix} {caption_text}</caption>"
        )
    except etree.XMLSyntaxError:
        logger.error(
            f"Invalid XML in caption: <caption>{caption_prefix} "
            f"{caption_text}</caption>"
        )
        return
    table_element.insert(0, table_caption_element)

    if "cols" in caption_element.attrib:
        table_element.insert(0, _create_colgroups(caption_element.attrib["cols"]))
        caption_element.attrib.pop("cols")
    table_element.attrib.update(caption_element.attrib)
    table_id = table_element.attrib.get(
        "id", config.identifier.format(index=index, identifier="table")
    )
    table_element.attrib["id"] = table_id
    update_references(
        tree, table_id, config.reference_text.format(index=index, identifier="Table")
    )


def postprocess_html(
    tree: etree._Element, config: IdentifierCaption, logger: PluginLogger
) -> None:
    """Handle custom captions in an XML tree.

    This function takes an XML tree and replaces all custom captions in the tree
    with custom HTML tags.

    Args:
        tree: The root element of the XML tree.
    """
    if not config.enable:
        return
    index_dict: t.Dict[str, int] = {}
    for custom_caption in tree.xpath(f"//{TABLE_CAPTION_TAG}"):
        identifier = custom_caption.attrib.pop("identifier")
        index = index_dict.get(identifier, config.start_index)
        index_dict[identifier] = index + config.increment_index
        a_wrapper = custom_caption.getparent()
        target_element = a_wrapper.getnext()
        if target_element.tag != "table":
            logger.error(
                "Table caption must be followed by a table element. "
                f"Skipping: {custom_caption.text}",
            )
            continue
        _add_caption_to_table(
            target_element,
            tree=tree,
            caption_element=custom_caption,
            index=index,
            config=config,
            logger=logger,
        )
        a_wrapper.remove(custom_caption)
        a_wrapper.getparent().remove(a_wrapper)
