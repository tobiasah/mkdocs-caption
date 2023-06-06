import typing as t

from lxml import etree

from mkdocs_caption.config import IdentifierCaption
from mkdocs_caption.helper import update_references, wrap_md_captions

CAPTION_TAG = "custom-caption"


def preprocess_markdown(markdown: str, identifier: t.List[str]) -> str:
    """Preprocess markdown to wrap custom captions

    The custom captions are wrapped in a custom html
    tag to make them easier to find later.

    Args:
        markdown: markdown string

    Returns:
        markdown string with custom captions wrapped
    """
    return wrap_md_captions(markdown, identifier, CAPTION_TAG)


def _wrap_in_figure(
    tree: etree._Element,
    caption_element: etree._Element,
    index: int,
    identifier: str,
    config: IdentifierCaption,
) -> None:
    """Wrap an element in a figure element with a custom caption.

    This function takes an XML tree, a target element, a caption element, an
    index, and an identifier, and wraps the target element in a figure element
    with a custom caption based on the caption element, index, and identifier.

    Args:
        tree: The root element of the XML tree.
        target_element: The element to wrap in a figure element.
        caption_element: The caption element to use for the caption text.
        index: The index of the figure element.
        identifier: The identifier of the custom caption.
    """
    a_wrapper = caption_element.getparent()
    if a_wrapper is None:
        cause = "Custom caption is not wrapped in a link"
        raise RuntimeError(cause)
    target_element = a_wrapper.getnext()
    if target_element is None:
        cause = "Custom caption does not semm to have a element that follows it"
        raise RuntimeError(cause)

    figure_element = etree.Element("figure", None, None)
    figure_element.attrib.update(caption_element.attrib)
    # wrap target element
    target_element.addprevious(figure_element)
    figure_element.insert(0, target_element)

    # add caption
    fig_caption_element = etree.Element("figcaption", None, None)
    fig_caption_element.text = (
        f"{config.caption_prefix.format(identifier = identifier, index = index)} {caption_element.text}"
    )
    figure_element.append(fig_caption_element)

    figure_id = caption_element.attrib.get("id", config.identifier.format(identifier=identifier, index=index))
    figure_element.attrib["id"] = figure_id
    update_references(tree, figure_id, config.reference_text.format(identifier=identifier, index=index))
    a_wrapper.remove(caption_element)
    parent = a_wrapper.getparent()
    if parent is not None:
        parent.remove(a_wrapper)


def postprocess_html(tree: etree._Element, config: IdentifierCaption) -> None:
    """Handle custom captions in an XML tree.

    This function takes an XML tree and replaces all custom captions in the tree
    with custom HTML tags.

    Args:
        tree: The root element of the XML tree.
    """
    if not config.enable:
        return
    index_dict: t.Dict[str, int] = {}
    for custom_caption in tree.xpath(f"//{CAPTION_TAG}"):
        identifier = custom_caption.attrib.pop("identifier")
        index = index_dict.get(identifier, 1)
        index_dict[identifier] = index + 1
        _wrap_in_figure(tree, custom_caption, index, identifier, config)