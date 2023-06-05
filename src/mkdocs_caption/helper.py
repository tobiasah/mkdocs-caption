import re
import typing as t

from lxml import etree


def update_references(root: etree._Element, custom_id: str, text: str) -> None:
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

    Returns:
        A string with the custom caption escaped using a custom HTML tag.
    """
    identifier = match.group(1)
    caption = match.group(2)
    options = match.group(4)
    return f'<{target_tag} identifier="{identifier}" \
        {options}>{caption}</{target_tag}>\n\n'


def wrap_md_captions(markdown: str, identifier: t.List[str], html_tag: str) -> str:
    """Preprocess markdown to wrap custom captions

    The custom captions are wrapped in a custom html
    tag to make them easier to find later.

    Args:
        markdown: markdown string

    Returns:
        markdown string with custom captions wrapped
    """
    return re.sub(
        rf"({'|'.join(identifier)}): (.*?)({{(.*?)}})?\n\n",
        lambda match: escape_md_caption(match, html_tag),
        markdown,
        flags=re.MULTILINE | re.DOTALL,
    )
