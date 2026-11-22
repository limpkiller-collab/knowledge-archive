from __future__ import annotations

import base64
import os
import subprocess
import tempfile
from pathlib import Path

import requests

GEMINI = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
PROMPT = "이 음성을 들리는 그대로 받아 적어라. 원래 언어를 유지하고, 설명이나 요약은 덧붙이지 않는다."
MAX_AUDIO_BYTES = 14 * 1024 * 1024  # base64로 늘어난 뒤에도 요청 한도 20MB 안에 들도록


def from_media_url(media_url: str) -> str:
    """영상 주소에서 음성만 뽑아 Gemini로 받아쓴다. 16kHz 모노 mp3로 줄여 요청 크기를 작게 유지한다."""
    with tempfile.TemporaryDirectory() as tmp:
        src, audio = Path(tmp) / "in.mp4", Path(tmp) / "out.mp3"
        with requests.get(media_url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(src, "wb") as f:
                for chunk in r.iter_content(1 << 20):
                    f.write(chunk)
        subprocess.run(["ffmpeg", "-y", "-i", str(src), "-vn", "-ac", "1", "-ar", "16000", "-b:a", "32k", str(audio)],
                       check=True, capture_output=True)
        data = audio.read_bytes()
    if len(data) > MAX_AUDIO_BYTES:
        raise ValueError("음성이 너무 길어 받아쓸 수 없습니다")
    body = {"contents": [{"parts": [
        {"inline_data": {"mime_type": "audio/mp3", "data": base64.b64encode(data).decode("ascii")}},
        {"text": PROMPT},
    ]}]}
    resp = requests.post(GEMINI.format(model=os.environ.get("GEMINI_MODEL") or "gemini-3.8-flash"),
                         headers={"x-goog-api-key": os.environ["GEMINI_API_KEY"]}, json=body, timeout=300)
    resp.raise_for_status()
    parts = resp.json()["candidates"][0]["content"]["parts"]
    return "".join(p.get("text", "") for p in parts).strip()
