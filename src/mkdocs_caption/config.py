"""The configuration options for the Caption plugin."""
from __future__ import annotations

import typing as t

from mkdocs.config import base, config_options


class IdentifierCaption(base.Config):
    """The generic configuration options for a specific identifier.

    Args:
        enable: Whether to enable the identifier.
        start_index: The start index (displayed value) for the identifier.
        increment_index: The increment value for the identifier.
        position: The position of the identifier relative to the caption.
        identifier: The identifier to use for the caption.
        reference_text: The text to use for the reference (if empty).
        caption_prefix: The prefix to use for the caption.
    """

    enable = config_options.Type(bool, default=True)
    start_index = config_options.Type(int, default=1)
    increment_index = config_options.Type(int, default=1)
    position = config_options.Choice(("top", "bottom"), default="bottom")
    identifier = config_options.Type(str, default="_{identifier}-{index}")
    reference_text = config_options.Type(str, default="{identifier} {index}")
    caption_prefix = config_options.Type(str, default="{identifier} {index}:")


class CaptionConfig(base.Config):
    """The configuration options for the Caption plugin.

    Args:
        additional_identifier: The additional identifiers to use.
            (e.g. ["List"])
        table: The configuration options for tables.
        figure: The configuration options for figures.
        custom: The configuration options for custom elements.
    """

    additional_identifier = config_options.ListOfItems(
        config_options.Type(str),
        default=[],
    )
    table = config_options.SubConfig(IdentifierCaption)
    figure = config_options.SubConfig(IdentifierCaption)
    custom = config_options.SubConfig(IdentifierCaption)


def update_config(config: CaptionConfig, updates: dict[str, t.Any]) -> CaptionConfig:
    """Update the configuration options with the given updates.

    Args:
        config: The configuration options to update.
        updates: The updates to apply to the configuration options.

    Returns:
        The updated configuration options.
    """
    config.additional_identifier = updates.get(
        "additional_identifier",
        config.additional_identifier,
    )
    config.table.load_dict(updates.get("table", {}))
    config.figure.load_dict(updates.get("figure", {}))
    config.custom.load_dict(updates.get("custom", {}))
    return config
