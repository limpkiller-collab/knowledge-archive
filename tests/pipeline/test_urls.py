import pytest
from scrap.urls import classify, normalize, youtube_id


@pytest.mark.parametrize("raw,expected", [
    ("https://www.instagram.com/p/ABC123/?igsh=xyz&utm_source=ig", "https://www.instagram.com/p/ABC123/"),
    ("https://example.com/a?utm_medium=x&id=7#top", "https://example.com/a?id=7"),
    ("https://youtu.be/dQw4w9WgXcQ?si=abc", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
    ("https://www.youtube.com/shorts/dQw4w9WgXcQ?feature=share", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
    ("https://m.youtube.com/watch?v=dQw4w9WgXcQ&t=10s", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
    ("  https://example.com/a/  ", "https://example.com/a/"),
    ("https://www.instagram.com/reel/ABC/?cnvx=zzz", "https://www.instagram.com/reel/ABC/"),
])
def test_normalize(raw, expected):
    assert normalize(raw) == expected


@pytest.mark.parametrize("url,expected", [
    ("https://www.instagram.com/p/ABC123/", "instagram_post"),
    ("https://www.instagram.com/reel/ABC123/", "instagram_reel"),
    ("https://www.instagram.com/reels/ABC123/", "instagram_reel"),
    ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "youtube"),
    ("https://news.example.com/story", "article"),
])
def test_classify(url, expected):
    assert classify(url) == expected


def test_normalize_rejects_non_http():
    with pytest.raises(ValueError):
        normalize("javascript:alert(1)")


def test_youtube_id():
    assert youtube_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"
    assert youtube_id("https://example.com") is None


def test_threads_links():
    assert classify("https://www.threads.com/share/_r6yYuEnH") == "threads"
    assert classify("https://www.threads.net/@a/post/B") == "threads"
    assert normalize("https://www.threads.com/@a/post/B?xmt=AQG0&slof=1") == "https://www.threads.com/@a/post/B"
