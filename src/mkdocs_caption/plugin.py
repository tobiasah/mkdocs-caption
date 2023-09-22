"""MkDocs plugin for custom image and table captions."""
from lxml import etree
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin, event_priority
from mkdocs.structure.pages import Page

from mkdocs_caption import config, custom, image, table
from mkdocs_caption.logger import get_logger


class CaptionPlugin(BasePlugin[config.CaptionConfig]):
    """A MkDocs plugin for custom image and table captions.

    This plugin provides custom image and table caption functionality for
    MkDocs. It allows users to specify custom captions for images and tables
    using a simple syntax in Markdown, and automatically generates captions
    based on the syntax.

    Usage:
        TODO
    """

    def on_config(self, config: MkDocsConfig, **_) -> MkDocsConfig:
        """Called by MkDocs when parsing the config.

        We just store the config for later use.

        Args:
            config: The global configuration object.

        Returns:
            The global configuration object.
        """
        self._config = config.plugins["caption"].config
        return config

    def _get_config(self, page: Page) -> config.CaptionConfig:
        """Get the configuration for a page.

        This is done by merging the global configuration with the page-specific.

        Args:
            page: current page

        Returns:
            The configuration for the page.
        """
        page_config = page.meta.get("caption", {})
        return config.update_config(self._config.copy(), page_config)

    @event_priority(-100)
    def on_page_markdown(self, markdown: str, *, page: Page, **_) -> str:
        """Process the Markdown content of a page.

        The `page_markdown` event is called after the page's markdown is loaded
        from file and can be used to alter the Markdown source text. The meta-
        data has been stripped off and is available as `page.meta` at this point.

        Args:
            markdown: Markdown source text of page as string
            page: `mkdocs.nav.Page` instance
            config: global configuration object
            files: global files collection

        Returns:
            The processed Markdown content of the page.
        """
        logger = get_logger(page.file.src_path)
        config = self._get_config(page)
        try:
            markdown = table.preprocess_markdown(markdown, config=self._config.table)
        except Exception as e:  # noqa: BLE001
            logger.error(
                "Unexpected Error while preprocessing the tables, skipping: %s",
                e,
            )
        try:
            markdown = image.preprocess_markdown(markdown, config=self._config.figure)
        except Exception as e:  # noqa: BLE001
            logger.error(
                "Unexpected Error while preprocessing the images, skipping: %s",
                e,
            )
        try:
            markdown = custom.preprocess_markdown(
                markdown,
                config=self._config.custom,
                identifiers=config.additional_identifier,
            )
        except Exception as e:  # noqa: BLE001
            logger.error(
                "Unexpected Error while preprocessing the custom, skipping: %s",
                e,
            )

        return markdown

    def on_page_content(self, html: str, *, page: Page, **_) -> str:
        """Process the HTML content of a rendered page.

        The `page_content` event is called after the Markdown text is rendered to
        HTML (but before being passed to a template) and can be used to alter the
        HTML body of the page.

        Args:
            html: HTML rendered from Markdown source as string
            page: `mkdocs.nav.Page` instance
            config: global configuration object
            files: global files collection

        Returns:
            The processed HTML content of the page.
        """
        logger = get_logger(page.file.src_path)
        config = self._get_config(page)
        try:
            parser = etree.HTMLParser()
            tree = etree.fromstring(html, parser)
            if tree is None:
                return html
            table.postprocess_html(tree=tree, config=config["table"], logger=logger)
            custom.postprocess_html(tree=tree, config=config["custom"], logger=logger)
            image.postprocess_html(tree=tree, config=config["figure"], logger=logger)
            html_result = etree.tostring(tree, encoding="unicode", method="html")
            # HTMLParser adds <html><body> tags, remove them
            return html_result[len("<html><body>") : -len("</body></html>")]
        except Exception as e:  # noqa: BLE001
            logger.error("Unexpected Error skipping: %s", e)
            return html
