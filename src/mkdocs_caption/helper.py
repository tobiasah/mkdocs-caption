"""General helper functions for the mkdocs-caption plugin."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterator

from lxml import etree

TreeElement = etree._Element  # noqa: SLF001


def update_references(root: TreeElement, custom_id: str, text: str) -> None:
    """Update references to a custom caption in an XML tree.

    This function takes an XML tree, a custom caption identifier, and a new
    caption text, and updates all references to the custom caption in the tree
    to use the new caption text.

    Args:
        root: The root element of the XML tree.
        custom_id: The identifier of the custom caption to update.
        text: The new caption text to use.
    """
    for ref in root.xpath(f"//a[@href='#{custom_id}']"):
        if not ref.text:
            ref.text = text


def _parse_extended_markdown(options: str | None) -> str:
    """Parse special extended markdown syntax.

    The extended markdown syntax allows for adding classes and ids to
    markdown elements through the use of the following syntax: .class #id
    This function parses the options and converts these two use cases into
    valid html attributes.

    Args:
        options: The options to parse.

    Returns:
        The parsed options.
    """
    if not options:
        return ""
    # Not the nicest solution but I could not find the place where python
    # markdown parses the options.
    split_options = options.split(" ")
    output_options = []
    for option in split_options:
        if option.startswith("."):
            output_options.append("class=" + option[1:])
        elif option.startswith("#"):
            output_options.append("id=" + option[1:])
        else:
            output_options.append(option)
    return " ".join(output_options)


def _escape_md_caption(match: re.Match, *, target_tag: str) -> str:
    """Escape custom captions in a markdown string.

    This function takes a regular expression match object and returns a string
    with the custom caption escaped using a custom HTML tag.

    Args:
        match: A regular expression match object.
        target_tag: The target HTML tag to use.

    Returns:
        A string with the custom caption escaped using a custom HTML tag.
    """
    prefix = match.group(1)
    identifier = match.group(2).rstrip(":")
    caption = match.group(3).replace("\n", " ")
    options = _parse_extended_markdown(match.group(5))
    return str(
        f'\n{prefix}<{target_tag} identifier="{identifier}"'
        f"{options}>\n\n{prefix}{caption}\n\n{prefix}<{target_tag}-end>\n\n",
    )


def wrap_md_captions(
    markdown: str,
    *,
    identifier: str,
    html_tag: str,
    allow_indented_caption: bool,
) -> str:
    """Preprocess markdown to wrap custom captions.

    The custom captions are wrapped in a custom html
    tag to make them easier to find later.

    Args:
        markdown: markdown string
        identifier: identifier to wrap
        html_tag: html tag to wrap the caption in
        allow_indented_caption: Flag if indented captions are allowed

    Returns:
        markdown string with custom captions wrapped
    """
    prefix = r"([^\S\r\n]*?)" if allow_indented_caption else "^()"
    return re.sub(
        rf"{prefix}({identifier}) (.*?)({{(.*?)}})?\n\n",
        lambda match: _escape_md_caption(match, target_tag=html_tag),
        markdown,
        flags=re.MULTILINE | re.DOTALL,
    )


def create_caption_str(caption_text_elements: list[TreeElement]) -> str:
    """Create a htaml string from a list of caption text elements.

    This function takes a list of caption text elements and returns a string
    with the caption text.

    Args:
        caption_text_elements: The list of caption text elements.

    Returns:
        A string with the caption text.
    """
    caption_text = ""
    for text_element in caption_text_elements:
        caption_text += etree.tostring(
            text_element,
            encoding="unicode",
            method="html",
        ).strip("\n")
    if len(caption_text_elements) == 1:
        caption_text = caption_text.strip("<p>").strip("</p>")
    return caption_text


@dataclass
class CaptionInfo:
    """Dataclass to store information about a caption."""

    target_element: TreeElement
    attributes: dict[str, str]
    caption: str
    identifier: str


def iter_caption_elements(tag: str, tree: TreeElement) -> Iterator[CaptionInfo]:
    """Iterate over all caption elements in an XML tree.

    This function takes an XML tree and iterates over all caption elements
    in the tree. It yields a tuple with the target element, the attributes
    of the caption element, the caption text, and the identifier of the
    caption element.

    Args:
        tag: The tag of the caption elements.
        tree: The XML tree to iterate over.

    Yields:
        A tuple with the target element, the attributes of the caption
        element, the caption text, and the identifier of the caption element.
    """
    for caption_element in tree.xpath(f"//{tag}"):
        a_wrapper = caption_element.getparent()
        caption_text_elements = []
        a_wrapper_end = a_wrapper.getnext()
        while a_wrapper_end is not None and not a_wrapper_end.xpath(f"{tag}-end"):
            caption_text_elements.append(a_wrapper_end)
            a_wrapper_end = a_wrapper_end.getnext()

        target_element = a_wrapper_end.getnext()
        # unused attribute identifier
        identifier = caption_element.attrib.pop("identifier")

        try:
            yield CaptionInfo(
                target_element=target_element,
                attributes=caption_element.attrib,
                caption=create_caption_str(caption_text_elements),
                identifier=identifier,
            )
        finally:
            a_wrapper.remove(caption_element)
            a_wrapper.getparent().remove(a_wrapper)
            for caption_text_element in caption_text_elements:
                caption_text_element.getparent().remove(caption_text_element)
            a_wrapper_end.getparent().remove(a_wrapper_end)
