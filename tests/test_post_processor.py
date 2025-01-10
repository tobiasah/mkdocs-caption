"""Tests for the post processor."""

from mkdocs_caption.post_processor import PostProcessor


def test_post_processor_register(dummy_page):
    post_processor = PostProcessor()
    post_processor.register_target("identifier", "text", dummy_page)
    assert 'test.html#identifier"' in post_processor.regex_to_apply
    assert dummy_page.file.src_uri in post_processor._local_regex  # noqa: SLF001


def test_post_processor_replace_ok(dummy_page):
    post_processor = PostProcessor()
    post_processor.register_target("identifier", "text", dummy_page)
    content = '<a href="test.html#identifier"></a>'
    assert (
        post_processor.post_process(dummy_page, content)
        == '<a href="test.html#identifier">text</a>'
    )


def test_post_processor_replace_multiple(dummy_page):
    post_processor = PostProcessor()
    post_processor.register_target("identifier", "text", dummy_page)
    post_processor.register_target("dummy", "dummy", dummy_page)
    content = '<a href="test.html#identifier"></a>...<a href="test.html#dummy"></a>'
    assert (
        post_processor.post_process(dummy_page, content)
        == '<a href="test.html#identifier">text</a>...<a href="test.html#dummy">dummy</a>'  # noqa: E501
    )


def test_post_processor_replace_no_match(dummy_page):
    post_processor = PostProcessor()
    post_processor.register_target("identifier", "text", dummy_page)
    content = '<a href="test.html#unkown"></a>'
    assert (
        post_processor.post_process(dummy_page, content)
        == '<a href="test.html#unkown"></a>'
    )


def test_post_processor_replace_existing_text(dummy_page):
    post_processor = PostProcessor()
    post_processor.register_target("identifier", "text", dummy_page)
    content = '<a href="test.html#identifier">hello</a>'
    assert (
        post_processor.post_process(dummy_page, content)
        == '<a href="test.html#identifier">hello</a>'
    )


def test_post_processor_similar_tag(dummy_page):
    post_processor = PostProcessor()
    post_processor.register_target("test", "wrong", dummy_page)
    post_processor.register_target("test2", "right", dummy_page)
    content = '<a href="#test2"></a>'
    assert (
        post_processor.post_process(dummy_page, content) == '<a href="#test2">right</a>'
    )
