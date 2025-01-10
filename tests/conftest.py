"""Pytest configuration file for the tests."""

import pytest
from mkdocs.structure.files import File
from mkdocs.structure.pages import Page


@pytest.fixture
def dummy_page():
    return Page(
        title="Test",
        file=File(path="test.md", src_dir="", dest_dir="", use_directory_urls=False),
        config={},
    )
