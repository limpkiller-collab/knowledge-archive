from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Extracted:
    source_type: str  # article | instagram_post | instagram_reel | youtube
    url: str
    title: str = ""
    author: str = ""
    published_at: str = ""
    text: str = ""
    images: list[str] = field(default_factory=list)
    transcript: str = ""
    thumbnail_url: str = ""
    media_url: str = ""
    warnings: list[str] = field(default_factory=list)


@dataclass
class Card:
    id: str
    title: str
    summary: str
    key_points: list[str]
    category: str
    tags: list[str]
    cover_word: str
    source_type: str
    source: str
    source_url: str
    date: str
    cover: str = ""
    images: list[str] = field(default_factory=list)  # 게시물에 들어 있던 이미지 전체(스와이프 갤러리)


class ExtractError(Exception):
    """내용을 가져오지 못했을 때. 메시지는 알림에 그대로 쓴다."""
