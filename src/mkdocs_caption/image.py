from lxml import etree

from mkdocs_caption.config import IdentifierCaption
from mkdocs_caption.helper import update_references


def wrap_image(img: etree._Element, custom_id: str, caption: etree._Element, position: str) -> None:
    """Wrap an image element in a figure element with a custom caption.

    This function takes an image element and wraps it in a figure element with the
    custom caption. If the image element is already wrapped in an anchor element,
    the figure element is inserted after the anchor element instead.

    Args:
        img: The image element to wrap.
        custom_id: The identifier of the custom caption.
        caption: The caption element to use.
    """
    target = img
    parent = img.getparent()
    if parent is not None and parent.tag == "a":
        target = parent
    figure_element = etree.Element("figure", None, None)
    figure_element.attrib["id"] = custom_id
    target.addnext(figure_element)
    if position == "top":
        figure_element.append(caption)
        figure_element.append(target)
    else:
        figure_element.append(target)
        figure_element.append(caption)


def postprocess_html(tree: etree._Element, config: IdentifierCaption) -> None:
    """Postprocess an XML tree to handle custom image captions.

    This function takes an XML tree and postprocesses it to handle custom image
    captions. It searches for all image elements in the tree, and if an image
    has a title attribute, it wraps the image in a figure element with a custom
    caption.

    Args:
        tree: The root element of the XML tree.
    """
    if not config.enable:
        return
    index = config.start_index
    for img_element in tree.xpath("//p/a/img|//p/img"):
        title = img_element.get("title")
        custom_id = img_element.get("id", config.identifier.format(index=index, identifier="figure"))
        update_references(tree, custom_id, config.reference_text.format(index=index, identifier="figure"))
        if title is not None:
            caption_element = etree.Element("figcaption", None, None)
            caption_prefix = config.caption_prefix.format(index=index, identifier="Figure")
            caption_element.text = f"{caption_prefix} {title}"
            wrap_image(img_element, custom_id, caption_element, config.position)
            index += config.increment_index
