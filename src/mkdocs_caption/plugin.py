from lxml import etree
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page

from mkdocs_caption import config, custom, image, table


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
        config = self._get_config(page)
        if self._config["table"]["enable"]:
            markdown = table.preprocess_markdown(markdown, ["Table"])
        identifier = []
        if config["custom"]["enable"]:
            identifier += config["additional_identifier"]
            if config["figure"]["enable"]:
                identifier += ["Figure"]
            markdown = custom.preprocess_markdown(markdown, identifier)
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
        config = self._get_config(page)
        parser = etree.HTMLParser()
        tree = etree.fromstring(html, parser)
        table.postprocess_html(tree, config["table"])
        custom.postprocess_html(tree, config["custom"])
        image.postprocess_html(tree, config["figure"])
        return etree.tostring(tree, encoding="unicode")
