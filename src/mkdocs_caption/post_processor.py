"""Global post-processor for MkDocs pages."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mkdocs.structure.pages import Page


class PostProcessor:
    """Global post-processor for MkDocs pages.

    This post proccessor implements all global post-processing steps for the
    MkDocs caption. Global post-processing steps are steps that are applied to
    all pages and require information from different pages to be applied.
    """

    def __init__(self, cross_reference_text: str = "{local_ref}") -> None:
        self._regex_to_apply: dict[str, tuple[re.Pattern, str]] = {}
        self._local_regex: dict[str, list[tuple[re.Pattern, str]]] = {}
        self._global_regex: re.Pattern | None = None
        self._cross_reference_text = cross_reference_text

    def register_target(self, identifier: str, text: str, page: Page) -> None:
        """Register a new href target.

        Args:
            identifier: The identifier of the target.
            text: The text to replace the identifier with.
            page: The page the target is on.
        """
        self._global_regex = None
        target_text = self._cross_reference_text.replace(
            "{page_title}",
            page.title,
        ).replace("{local_ref}", text)
        self._regex_to_apply[rf'{page.file.src_path[:-3]}.html#{identifier}"'] = (
            re.compile(
                rf'({re.escape(page.file.src_path[:-3])}.html#{identifier}"[^>]*?>)(<\/a>)',
                flags=re.MULTILINE | re.DOTALL,
            ),
            rf"\1{target_text}\2",
        )
        if page.file.src_uri not in self._local_regex:
            self._local_regex[page.file.src_uri] = []
        self._local_regex[page.file.src_uri].append(
            (
                re.compile(
                    rf'("#{identifier}"[^>]*?>)(<\/a>)',
                    flags=re.MULTILINE | re.DOTALL,
                ),
                rf"\1{text}\2",
            ),
        )

    def post_process(self, page: Page, content: str) -> str:
        """Post-process the content of a page.

        The postprocessing replaces the empty href targets with the correct
        text.

        Args:
            page: The page to post-process.
            content: The content of the page.

        Returns:
            The post-processed content.
        """
        for local_regex, target in self._local_regex.get(page.file.src_uri, []):
            content = local_regex.sub(target, content)

        if self._global_regex is None:
            self._global_regex = re.compile(
                r"|".join(re.escape(regex) for regex in self._regex_to_apply),
            )
        result = content
        for found in self._global_regex.finditer(content):
            potential_match = found.group()
            if potential_match not in self._regex_to_apply:  # pragma: no cover
                continue
            regex, replacement = self._regex_to_apply[potential_match]
            result = regex.sub(replacement, result)

        return result

    @property
    def regex_to_apply(self) -> dict[str, tuple[re.Pattern, str]]:
        """The regex to apply to the content of the pages."""
        return self._regex_to_apply
