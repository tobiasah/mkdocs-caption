"""General helper functions for the mkdocs-caption plugin."""
from __future__ import annotations

import re

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
    identifier = match.group(1).rstrip(":")
    caption = match.group(2).replace("\n", " ")
    options = _parse_extended_markdown(match.group(4))
    return str(
        f'\n<{target_tag} identifier="{identifier}"'
        f"{options}>{caption}</{target_tag}>\n\n",
    )


def wrap_md_captions(markdown: str, *, identifier: str, html_tag: str) -> str:
    """Preprocess markdown to wrap custom captions.

    The custom captions are wrapped in a custom html
    tag to make them easier to find later.

    Args:
        markdown: markdown string
        identifier: identifier to wrap
        html_tag: html tag to wrap the caption in

    Returns:
        markdown string with custom captions wrapped
    """
    return re.sub(
        rf"^({identifier}) (.*?)({{(.*?)}})?\n\n",
        lambda match: _escape_md_caption(match, target_tag=html_tag),
        markdown,
        flags=re.MULTILINE | re.DOTALL,
    )


def sanitize_caption(caption: str | None) -> str:
    """Sanitize a caption to be used as an id.

    Args:
        caption: The caption to sanatize.

    Returns:
        The sanitized caption.
    """
    return caption.replace(" & ", " &amp; ") if caption else ""
