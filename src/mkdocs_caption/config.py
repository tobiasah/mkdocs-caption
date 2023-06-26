import typing as t

from mkdocs.config import base, config_options


class IdentifierCaption(base.Config):
    """The generic configuration options for a specific identifier."""

    enable = config_options.Type(bool, default=True)
    start_index = config_options.Type(int, default=1)
    increment_index = config_options.Type(int, default=1)
    position = config_options.Choice(("top", "bottom"), default="bottom")
    identifier = config_options.Type(str, default="_{identifier}-{index}")
    reference_text = config_options.Type(str, default="{identifier} {index}")
    caption_prefix = config_options.Type(str, default="{identifier} {index}:")


class CaptionConfig(base.Config):
    """The configuration options for the Caption plugin."""

    additional_identifier = config_options.ListOfItems(
        config_options.Type(str), default=[]
    )
    table = config_options.SubConfig(IdentifierCaption)
    figure = config_options.SubConfig(IdentifierCaption)
    custom = config_options.SubConfig(IdentifierCaption)


def update_config(config: CaptionConfig, updates: t.Dict[str, t.Any]) -> CaptionConfig:
    config.additional_identifier = updates.get(
        "additional_identifier", config.additional_identifier
    )
    config.table.load_dict(updates.get("table", {}))
    config.figure.load_dict(updates.get("figure", {}))
    config.custom.load_dict(updates.get("custom", {}))
    return config
