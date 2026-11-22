from __future__ import annotations

import os

import requests


def send(title: str, message: str, link: str = "") -> None:
    """ntfy로 푸시를 보낸다. 알림 실패가 전체 처리를 실패로 만들지 않게 예외를 삼킨다."""
    topic = os.environ.get("NTFY_TOPIC")
    if not topic:
        return
    headers = {"Title": title.encode("utf-8")}
    if link:
        headers["Click"] = link
    try:
        requests.post(f"https://ntfy.sh/{topic}", data=message.encode("utf-8"), headers=headers, timeout=15)
    except requests.RequestException:
        pass
