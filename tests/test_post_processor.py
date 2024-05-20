"""Tests for the post processor."""

from mkdocs_caption.post_processor import PostProcessor


def test_post_processor_register(dummy_page):
    post_processor = PostProcessor()
    post_processor.register_target("identifier", "text", dummy_page)
    assert "test/#identifier" in post_processor.regex_to_apply
    assert dummy_page.file.src_uri in post_processor._local_regex  # noqa: SLF001


def test_post_processor_replace_ok(dummy_page):
    post_processor = PostProcessor()
    post_processor.register_target("identifier", "text", dummy_page)
    content = '<a href="test/#identifier"></a>'
    assert (
        post_processor.post_process(dummy_page, content)
        == '<a href="test/#identifier">text</a>'
    )


def test_post_processor_replace_multiple(dummy_page):
    post_processor = PostProcessor()
    post_processor.register_target("identifier", "text", dummy_page)
    post_processor.register_target("dummy", "dummy", dummy_page)
    content = '<a href="test/#identifier"></a>...<a href="test/#dummy"></a>'
    assert (
        post_processor.post_process(dummy_page, content)
        == '<a href="test/#identifier">text</a>...<a href="test/#dummy">dummy</a>'
    )


def test_post_processor_replace_no_match(dummy_page):
    post_processor = PostProcessor()
    post_processor.register_target("identifier", "text", dummy_page)
    content = '<a href="test/#unkown"></a>'
    assert (
        post_processor.post_process(dummy_page, content)
        == '<a href="test/#unkown"></a>'
    )


def test_post_processor_replace_existing_text(dummy_page):
    post_processor = PostProcessor()
    post_processor.register_target("identifier", "text", dummy_page)
    content = '<a href="test/#identifier">hello</a>'
    assert (
        post_processor.post_process(dummy_page, content)
        == '<a href="test/#identifier">hello</a>'
    )
