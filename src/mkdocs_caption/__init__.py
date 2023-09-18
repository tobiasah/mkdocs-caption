# SPDX-FileCopyrightText: 2023-present Tobias Ahrens <tobias.ahrens@zhinst.com>
#
# SPDX-License-Identifier: MIT
"""MkDocs plugin to add captions to images, tables and any other elements.

Simply add the plugin to your `mkdocs.yml` file under the `plugins` section.
For a detailed description of the configuration options, please refer to the
[README](https://pypi.org/project/mkdocs-caption/)
"""
from mkdocs_caption.plugin import CaptionPlugin

__all__ = ["CaptionPlugin"]
