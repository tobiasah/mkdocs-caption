"""Setup custom logger that is mkdocs compatible."""
from __future__ import annotations

import logging
import typing as t


class PluginLogger(logging.LoggerAdapter):
    """A logger adapter to prefix messages with the originating package name.

    Args:
        prefix: The string to insert in front of every message.
            logger: The logger instance.
        filename: python script filename
        logger: logger instance
    """

    def __init__(self, prefix: str, filename: str, logger: logging.Logger) -> None:
        super().__init__(logger, {})
        self._prefix = prefix
        self._filename = filename

    def process(
        self,
        msg: str,
        kwargs: t.MutableMapping[str, t.Any],
    ) -> tuple[str, t.Any]:
        """Process the message.

        Args:
            msg: The message:
            kwargs: Remaining arguments.

        Returns:
            The processed message.
        """
        return f"{self._prefix}: {self._filename}: {msg}", kwargs


def get_logger(filename: str) -> PluginLogger:
    """Return a logger for plugins.

    Args:
        filename: python script filename

    Returns:
        A logger configured to work well in MkDocs, prefixing each message
        with the plugin package name.
    """
    logger = logging.getLogger("mkdocs.plugins.mkdocs_caption")
    return PluginLogger("mkdocs_caption", filename, logger)
