import pytest
from scrap import extract
from scrap.models import ExtractError


def test_instagram_post_maps_fields():
    item = {"caption": "캡션", "ownerUsername": "acct", "timestamp": "2026-11-20T01:00:00Z",
            "displayUrl": "https://cdn/1.jpg", "images": ["https://cdn/1.jpg", "https://cdn/2.jpg"]}
    ex = extract._from_instagram("https://www.instagram.com/p/A/", "instagram_post", item, transcribe=None)
    assert (ex.text, ex.author, ex.thumbnail_url) == ("캡션", "acct", "https://cdn/1.jpg")
    assert ex.images == ["https://cdn/1.jpg", "https://cdn/2.jpg"] and ex.published_at == "2026-11-20"


def test_reel_transcription_failure_becomes_warning():
    def boom(url):
        raise RuntimeError("stt down")
    item = {"caption": "캡션", "videoUrl": "https://cdn/v.mp4", "displayUrl": "https://cdn/t.jpg"}
    ex = extract._from_instagram("https://www.instagram.com/reel/A/", "instagram_reel", item, transcribe=boom)
    assert ex.transcript == "" and any("음성" in w for w in ex.warnings)


def test_youtube_uses_video_notes_and_thumbnail():
    ex = extract._from_youtube("https://www.youtube.com/watch?v=dQw4w9WgXcQ", watch=lambda u: "영상 내용 정리")
    assert ex.transcript == "영상 내용 정리" and ex.source_type == "youtube"
    assert ex.thumbnail_url == "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg"


def test_youtube_failure_raises():
    def boom(u):
        raise RuntimeError("video too long")
    with pytest.raises(ExtractError):
        extract._from_youtube("https://www.youtube.com/watch?v=dQw4w9WgXcQ", watch=boom)


def test_empty_article_raises():
    with pytest.raises(ExtractError):
        extract._from_article("https://e.com/a", html="<html><body></body></html>")
