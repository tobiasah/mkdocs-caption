"""Handle image related captioning."""

from __future__ import annotations

import urllib.parse
from typing import TYPE_CHECKING

from lxml import etree

from mkdocs_caption.helper import (
    TreeElement,
    iter_caption_elements,
    wrap_md_captions,
)

if TYPE_CHECKING:
    from collections.abc import Iterator

    from mkdocs.structure.pages import Page

    from mkdocs_caption.config import FigureCaption
    from mkdocs_caption.logger import PluginLogger
    from mkdocs_caption.post_processor import PostProcessor

IMG_CAPTION_TAG = "figure-caption"


def preprocess_markdown(markdown: str, *, config: FigureCaption) -> str:
    """Preprocess markdown to wrap image captions.

    The image captions are wrapped in a custom html
    tag to make them easier to find later.

    Args:
        markdown: markdown string
        config: plugin configuration for images

    Returns:
        markdown string with custom captions wrapped
    """
    if not config.enable:
        return markdown
    identifier = config.get_markdown_identifier("figure")
    return wrap_md_captions(
        markdown,
        identifier=identifier,
        html_tag=IMG_CAPTION_TAG,
        allow_indented_caption=config.allow_indented_caption,
    )


def wrap_image(
    *,
    img: TreeElement,
    caption: TreeElement,
    position: str,
    figure_attrib: dict[str, str],
    siblings: list[TreeElement],
) -> None:
    """Wrap an image element in a figure element with a custom caption.

    This function takes an image element and wraps it in a figure element with the
    custom caption. If the image element is already wrapped in an anchor element,
    the figure element is inserted after the anchor element instead.

    Args:
        img: The image element to wrap.
        caption: The caption element to use.
        position: The position of the caption relative to the image. (top, bottom)
        figure_attrib: Additional attributes for the figure element.
        siblings: Images that belong to the image and should be wrapped in the
            same figure.
    """
    target = img
    parent = img.getparent()
    if parent is not None and parent.tag == "a":
        target = parent
    figure_element = etree.Element("figure", None, None)
    figure_element.attrib.update(figure_attrib)
    target.addnext(figure_element)
    if position == "top":
        figure_element.append(caption)
        figure_element.append(target)
        for sibling in siblings:
            figure_element.append(sibling)
    else:
        figure_element.append(target)
        for sibling in siblings:
            figure_element.append(sibling)
        figure_element.append(caption)


def postprocess_image(
    *,
    img_element: TreeElement,
    title: str,
    config: FigureCaption,
    logger: PluginLogger,
    index: int,
    figure_attrib: dict[str, str] | None,
    page: Page,
    post_processor: PostProcessor,
    siblings: list[TreeElement],
) -> None:
    """Postprocess an image element to handle custom image captions.

    This function takes an image element and postprocesses it to handle custom
    image captions. If the image has a title attribute, it wraps the image in a
    figure element with a custom caption.

    Args:
        img_element: The image element to postprocess.
        title: The title of the image.
        config: The plugin configuration.
        logger: Current plugin logger.
        index: The index of the image element.
        figure_attrib: Additional attributes for the figure element.
        page: The current page.
        post_processor: The post processor to register targets.
        siblings: Images that belong to the image and should be wrapped in the
            same figure.
    """
    # Its a bit of a tricky situation here. The user can specify a custom id
    # both on the figure element and the image element. The references to both
    # of these elements needs to be updated.
    if "id" in img_element.attrib:
        post_processor.register_target(
            img_element.attrib["id"],
            config.get_reference_text(index=index, identifier="figure"),
            page,
        )
    if not figure_attrib:
        figure_attrib = {}
    if "id" not in figure_attrib:
        figure_attrib["id"] = config.get_default_id(index=index, identifier="figure")
    post_processor.register_target(
        figure_attrib["id"],
        config.get_reference_text(index=index, identifier="figure"),
        page,
    )
    # assemble the caption element
    caption_prefix = config.get_caption_prefix(
        index=index,
        identifier="figure",
    )
    try:
        caption_element = etree.fromstring(
            f"<figcaption>{caption_prefix} {title}</figcaption>",
        )
    except etree.XMLSyntaxError:
        logger.error("Invalid XML in caption: %s", title)
        return
    # wrap the image in figure with the caption element
    wrap_image(
        img=img_element,
        caption=caption_element,
        position=config.position,
        figure_attrib=figure_attrib,
        siblings=siblings,
    )


def _has_url_fragment(img_element: TreeElement) -> bool:
    """Check if a URL has a hash fragment.

    Args:
        img_element: The image element to check.

    Returns:
        True if the URL has a hash fragment, False otherwise.
    """
    return urllib.parse.urlparse(img_element.get("src")).fragment is not None


def _get_siblings(
    img_element: TreeElement,
    config: FigureCaption,
    img_iter: Iterator[TreeElement],
) -> list[TreeElement]:
    """Get potential siblings of an image element.

    A sibling is an image element that directly follows the current image element.
    This makes only sense if the image element has a URL with a hash fragment.

    This allows two have separate images for e.g light and dark mode:

    https://squidfunk.github.io/mkdocs-material/reference/images/#light-and-dark-mode

    Args:
        img_element: The image element to check.
        config: The plugin configuration.
        img_iter: An iterator over the image elements.

    Returns:
        A list of sibling image elements
    """
    siblings = []
    next_element = img_element.getnext()
    if (
        not config.ignore_hash
        and _has_url_fragment(img_element)
        and next_element is not None
        and next_element.tag == "img"
        and _has_url_fragment(next_element)
    ):
        next_element.attrib.pop("title", None)
        siblings.append(next_element)
        next(img_iter)
        siblings = [*siblings, *_get_siblings(next_element, config, img_iter)]
    return siblings


def postprocess_html(
    *,
    tree: TreeElement,
    config: FigureCaption,
    page: Page,
    post_processor: PostProcessor,
    logger: PluginLogger,
) -> None:
    """Postprocess an XML tree to handle custom image captions.

    This function takes an XML tree and postprocesses it to handle custom image
    captions. It searches for all image elements in the tree, and if an image
    has a title attribute, it wraps the image in a figure element with a custom
    caption.

    Args:
        tree: The root element of the XML tree.
        config: The plugin configuration.
        page: The current page.
        post_processor: The post processor to register targets.
        logger: Current plugin logger.
    """
    if not config.enable:
        return

    # Handle additional figure caption elements
    custom_figure_attrib = {}
    for caption_info in iter_caption_elements(IMG_CAPTION_TAG, tree):
        try:
            target_element = (
                caption_info.target_element
                if caption_info.target_element.tag == "img"
                else caption_info.target_element.xpath(".//img")[0]
            )
        except IndexError:
            logger.error(
                "Figure caption must be followed by a img element. Skipping: %s",
                caption_info.caption,
            )
            continue
        target_element.attrib["title"] = caption_info.caption
        custom_figure_attrib[target_element] = caption_info.attributes

    # Iterate through all images and wrap them in a figure element if requested
    index = config.start_index
    img_elements = tree.xpath("//p/a/img|//p/img")
    img_iter = iter(img_elements)
    for img_element in img_iter:
        figure_attrib = custom_figure_attrib.get(img_element, {})
        if img_element.attrib.get("class") in config.ignore_classes:
            continue
        siblings = _get_siblings(img_element, config=config, img_iter=img_iter)
        # We pop the title here so its not duplicated in the img element
        title = img_element.attrib.pop("title", None)
        if title is None:
            # Use the alt text if provided
            title = img_element.get("alt", None)
            if (
                config.ignore_alt
                or not title
                or (img_element.tail is not None and len(siblings) == 0)
            ):
                continue
        postprocess_image(
            img_element=img_element,
            title=title,
            config=config,
            logger=logger,
            index=index,
            figure_attrib=figure_attrib,
            page=page,
            post_processor=post_processor,
            siblings=siblings,
        )
        index += config.increment_index
