from __future__ import annotations

import base64
import os

import requests

GEMINI = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
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
    body = {"contents": [{"parts": [
        {"inline_data": {"mime_type": mime_type, "data": base64.b64encode(data).decode("ascii")}},
        {"text": PROMPT},
    ]}]}
    resp = requests.post(GEMINI.format(model=os.environ.get("GEMINI_MODEL") or "gemini-3.8-flash"),
                         headers={"x-goog-api-key": os.environ["GEMINI_API_KEY"]}, json=body, timeout=300)
    if resp.status_code >= 400:
        print(f"gemini http {resp.status_code}: {resp.text[:300]}")
        resp.raise_for_status()
    parts = resp.json()["candidates"][0]["content"]["parts"]
    return "".join(p.get("text", "") for p in parts).strip()


def from_media_url(video_url: str, audio_url: str = "") -> str:
    """릴스 영상을 Gemini가 직접 보고 듣게 해 내용을 글로 받는다.

    영상이 작으면 영상째로 보낸다(화면 속 글자도 읽힌다). 크면 음성 파일만 보낸다.
    """
    video = _download(video_url, MAX_INLINE_BYTES) if video_url else b""
    if video:
        print(f"transcribe: video {len(video) // 1024} KB")
        return _ask_gemini(video, "video/mp4")
    audio = _download(audio_url, MAX_INLINE_BYTES) if audio_url else b""
    if audio:
        print(f"transcribe: audio {len(audio) // 1024} KB")
        return _ask_gemini(audio, "audio/mp4")
    raise ValueError("영상이 너무 커서 읽을 수 없습니다")
