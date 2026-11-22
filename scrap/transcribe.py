from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path

import requests

STT_URL = "https://api.openai.com/v1/audio/transcriptions"
STT_MODEL = os.environ.get("STT_MODEL", "whisper-1")


def from_media_url(media_url: str) -> str:
    """영상 주소에서 음성만 뽑아 받아쓴다. 16kHz 모노 mp3로 줄여 파일 한도를 넘지 않게 한다."""
    with tempfile.TemporaryDirectory() as tmp:
        src, audio = Path(tmp) / "in.mp4", Path(tmp) / "out.mp3"
        with requests.get(media_url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(src, "wb") as f:
                for chunk in r.iter_content(1 << 20):
                    f.write(chunk)
        subprocess.run(["ffmpeg", "-y", "-i", str(src), "-vn", "-ac", "1", "-ar", "16000", "-b:a", "32k", str(audio)],
                       check=True, capture_output=True)
        with open(audio, "rb") as f:
            resp = requests.post(STT_URL, headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
                                 data={"model": STT_MODEL}, files={"file": ("audio.mp3", f, "audio/mpeg")}, timeout=300)
        resp.raise_for_status()
        return resp.json()["text"]
