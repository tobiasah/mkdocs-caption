"""Custom caption handling."""

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
            allow_indented_caption=config.allow_indented_caption,
        )
    return markdown


def _wrap_in_figure(
    caption_info: CaptionInfo,
    *,
    index: int,
    config: IdentifierCaption,
    logger: PluginLogger,
) -> str | None:
    """Wrap an element in a figure element with a custom caption.

    This function takes an XML tree, a target element, a caption element, an
    index, and an identifier, and wraps the target element in a figure element
    with a custom caption based on the caption element, index, and identifier.

    Args:
        caption_info: The caption info.
        index: The index of the figure element.
        config: The plugin configuration.
        logger: Current plugin logger.
    """
    if caption_info.target_element is None:
        logger.error("Custom caption does not semm to have a element that follows it")
        return None

    figure_element = etree.Element("figure", None, None)
    figure_element.attrib.update(caption_info.attributes)
    # wrap target element
    caption_info.target_element.addprevious(figure_element)

    # add caption
    caption_prefix = config.get_caption_prefix(
        identifier=caption_info.identifier,
        index=index,
    )
    try:
        fig_caption_element = etree.fromstring(
            f"<figcaption>{caption_prefix} {caption_info.caption}</figcaption>",
        )
    except etree.XMLSyntaxError:
        logger.error(
            'Invalid XML in caption: <caption style="caption-side:%s">%s %s</caption>',
            config.position,
            caption_prefix,
            caption_info.caption,
        )
        return None
    if config.position == "top":
        figure_element.append(fig_caption_element)
        figure_element.append(caption_info.target_element)
    else:
        figure_element.append(caption_info.target_element)
        figure_element.append(fig_caption_element)

    figure_id = caption_info.attributes.get(
        "id",
        config.get_default_id(identifier=caption_info.identifier, index=index),
    )
    figure_element.attrib["id"] = figure_id
    return figure_id


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
    index_dict: dict[str, int] = {}
    for caption_info in iter_caption_elements(CAPTION_TAG, tree):
        index = index_dict.get(caption_info.identifier, config.start_index)
        index_dict[caption_info.identifier] = index + config.increment_index
        figure_id = _wrap_in_figure(
            caption_info,
            index=index,
            config=config,
            logger=logger,
        )
        if figure_id is None:
            continue
        post_processor.register_target(
            figure_id,
            config.get_reference_text(index=index, identifier=caption_info.identifier),
            page,
        )
