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


def escape_md_caption(match: re.Match, target_tag: str) -> str:
    """Escape custom captions in a markdown string.

    This function takes a regular expression match object and returns a string
    with the custom caption escaped using a custom HTML tag.

    Args:
        match: A regular expression match object.
        target_tag: The target HTML tag to use.

    Returns:
        A string with the custom caption escaped using a custom HTML tag.
    """
    identifier = match.group(1)
    caption = match.group(2)
    options = match.group(4)
    return f'<{target_tag} identifier="{identifier}" \
        {options}>{caption}</{target_tag}>\n\n'


def wrap_md_captions(markdown: str, identifier: list[str], html_tag: str) -> str:
    """Preprocess markdown to wrap custom captions.

    The custom captions are wrapped in a custom html
    tag to make them easier to find later.

    Args:
        markdown: markdown string
        identifier: list of identifiers to wrap
        html_tag: html tag to wrap the caption in

    Returns:
        markdown string with custom captions wrapped
    """
    return re.sub(
        rf"({'|'.join(identifier)}): (.*?)({{(.*?)}})?\n\n",
        lambda match: escape_md_caption(match, html_tag),
        markdown,
        flags=re.MULTILINE | re.DOTALL,
    )
