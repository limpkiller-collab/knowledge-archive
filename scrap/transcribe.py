from __future__ import annotations

import base64

import requests

from . import gemini

PROMPT = ("이 영상(또는 음성)의 내용을 한국어로 빠짐없이 글로 옮겨라. "
          "사람이 말하는 내용은 들리는 그대로 적고, 화면에 나오는 자막과 글자도 함께 적는다. "
          "설명이나 평가는 덧붙이지 않는다.")
MAX_INLINE_BYTES = 14 * 1024 * 1024  # base64로 늘어난 뒤에도 요청 한도 20MB 안에 들도록
MAX_DOWNLOAD_BYTES = 80 * 1024 * 1024


def _download(url: str, limit: int) -> bytes:
    """파일을 내려받는다. limit를 넘으면 중단하고 빈 값을 돌려준다."""
    chunks, size = [], 0
    with requests.get(url, stream=True, timeout=60, headers={"User-Agent": "Mozilla/5.0 (compatible; link-scrap)"}) as r:
        r.raise_for_status()
        for chunk in r.iter_content(1 << 20):
            size += len(chunk)
            if size > limit:
                return b""
            chunks.append(chunk)
    return b"".join(chunks)


def _ask_gemini(data: bytes, mime_type: str) -> str:
    return gemini.generate([
        {"inline_data": {"mime_type": mime_type, "data": base64.b64encode(data).decode("ascii")}},
        {"text": PROMPT},
    ])


def from_media_url(video_url: str, audio_url: str = "") -> str:
    """릴스의 내용을 Gemini로 글로 옮긴다.

    음성 파일이 있으면 그것을 먼저 쓴다(작고 빠르다). 없거나 실패하면 영상째로 보낸다.
    """
    errors = []
    for label, url, mime in (("audio", audio_url, "audio/mp4"), ("video", video_url, "video/mp4")):
        if not url:
            continue
        try:
            data = _download(url, MAX_INLINE_BYTES)
            if not data:
                errors.append(f"{label}: too large")
                continue
            print(f"transcribe: {label} {len(data) // 1024} KB")
            text = _ask_gemini(data, mime)
            if text:
                return text
            errors.append(f"{label}: empty answer")
        except Exception as e:
            errors.append(f"{label}: {type(e).__name__}")
    raise ValueError("; ".join(errors) or "no media url")
