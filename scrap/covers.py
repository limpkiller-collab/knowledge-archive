from __future__ import annotations

import io
import os
from pathlib import Path

import requests
from PIL import Image

MAX_WIDTH = 1200
MAX_BYTES = 10 * 1024 * 1024
MAX_GALLERY = 20  # 인스타그램 게시물 한 건의 최대 장수


def _fetch(url: str) -> bytes:
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (compatible; link-scrap)"}, timeout=30)
    resp.raise_for_status()
    if len(resp.content) > MAX_BYTES:
        raise OSError("이미지가 너무 큽니다")
    return resp.content


def save(card_id: str, thumbnail_url: str, root: Path, fetch=_fetch) -> str:
    """썸네일을 covers/<id>.jpg로 저장하고 경로를 돌려준다. 실패하면 빈 문자열(생성 커버로 대체)."""
    if not thumbnail_url or os.environ.get("SCRAP_STORE_COVERS") == "0":
        return ""
    try:
        img = Image.open(io.BytesIO(fetch(thumbnail_url))).convert("RGB")
        if img.width > MAX_WIDTH:
            img = img.resize((MAX_WIDTH, round(img.height * MAX_WIDTH / img.width)))
        (root / "covers").mkdir(exist_ok=True)
        rel = f"covers/{card_id}.jpg"
        img.save(root / rel, "JPEG", quality=82)
        return rel
    except Exception:
        return ""


def save_all(card_id: str, urls: list[str], root: Path, fetch=_fetch) -> list[str]:
    """게시물의 이미지를 covers/<id>/01.jpg … 로 저장하고 경로 목록을 돌려준다. 받지 못한 장은 건너뛴다."""
    if not urls or os.environ.get("SCRAP_STORE_COVERS") == "0":
        return []
    folder = root / "covers" / card_id
    folder.mkdir(parents=True, exist_ok=True)
    for old in folder.glob("[0-9][0-9].jpg"):  # 다시 정리하는 카드는 새로 받는다. 직접 추가한 이미지(u-*)는 남긴다
        old.unlink()
    saved = []
    for url in urls[:MAX_GALLERY]:
        try:
            img = Image.open(io.BytesIO(fetch(url))).convert("RGB")
            if img.width > MAX_WIDTH:
                img = img.resize((MAX_WIDTH, round(img.height * MAX_WIDTH / img.width)))
            rel = f"covers/{card_id}/{len(saved) + 1:02d}.jpg"
            img.save(root / rel, "JPEG", quality=82)
            saved.append(rel)
        except Exception as e:
            print(f"gallery image skipped: {type(e).__name__}")
    return saved
