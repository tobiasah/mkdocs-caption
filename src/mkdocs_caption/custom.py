"""Custom caption handling."""
from __future__ import annotations

from typing import TYPE_CHECKING

from lxml import etree

from mkdocs_caption.helper import TreeElement, update_references, wrap_md_captions

if TYPE_CHECKING:
    from mkdocs_caption.config import IdentifierCaption
    from mkdocs_caption.logger import PluginLogger

CAPTION_TAG = "custom-caption"


def preprocess_markdown(
    markdown: str,
    *,
    config: IdentifierCaption,
    identifiers: list[str],
) -> str:
    """Preprocess markdown to wrap custom captions.

    The custom captions are wrapped in a custom html
    tag to make them easier to find later.

    Args:
        markdown: markdown string
        config: plugin configuration for custom captions
        identifiers: list of identifiers to wrap

    Returns:
        markdown string with custom captions wrapped
    """
    if not config.enable:
        return markdown
    for identifier in identifiers:
        md_identifier = config.get_markdown_identifier(identifier)
        markdown = wrap_md_captions(
            markdown,
            identifier=md_identifier,
            html_tag=CAPTION_TAG,
        )
    return markdown


def _wrap_in_figure(
    caption_element: TreeElement,
    *,
    tree: TreeElement,
    index: int,
    identifier: str,
    config: IdentifierCaption,
    logger: PluginLogger,
) -> None:
    """Wrap an element in a figure element with a custom caption.

    This function takes an XML tree, a target element, a caption element, an
    index, and an identifier, and wraps the target element in a figure element
    with a custom caption based on the caption element, index, and identifier.

    Args:
        caption_element: The caption element to use for the caption text.
        tree: The root element of the XML tree.
        index: The index of the figure element.
        identifier: The identifier of the custom caption.
        config: The plugin configuration.
        logger: Current plugin logger.
    """
    a_wrapper: TreeElement = caption_element.getparent()  # type: ignore[assignment]
    target_element = a_wrapper.getnext()
    if target_element is None:
        logger.error("Custom caption does not semm to have a element that follows it")
        return

    figure_element = etree.Element("figure", None, None)
    figure_element.attrib.update(caption_element.attrib)
    # wrap target element
    target_element.addprevious(figure_element)

    # add caption
    caption_prefix = config.get_caption_prefix(identifier=identifier, index=index)
    try:
        fig_caption_element = etree.fromstring(
            f"<figcaption>{caption_prefix} {caption_element.text}</figcaption>",
        )
    except etree.XMLSyntaxError:
        logger.error("Invalid XML in caption: %s", caption_element.text)
        return
    if config.position == "top":
        figure_element.append(fig_caption_element)
        figure_element.append(target_element)
    else:
        figure_element.append(target_element)
        figure_element.append(fig_caption_element)

    figure_id = caption_element.attrib.get(
        "id",
        config.get_default_id(identifier=identifier, index=index),
    )
    figure_element.attrib["id"] = figure_id
    update_references(
        tree,
        figure_id,
        config.get_reference_text(identifier=identifier, index=index),
    )
    a_wrapper.remove(caption_element)
    a_wrapper.getparent().remove(a_wrapper)  # type: ignore[union-attr]


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
    index_dict: dict[str, int] = {}
    for custom_caption in tree.xpath(f"//{CAPTION_TAG}"):
        identifier = custom_caption.attrib.pop("identifier")
        index = index_dict.get(identifier, config.start_index)
        index_dict[identifier] = index + config.increment_index
        _wrap_in_figure(
            custom_caption,
            tree=tree,
            index=index,
            identifier=identifier,
            config=config,
            logger=logger,
        )
