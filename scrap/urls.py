from __future__ import annotations

import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

TRACKING = re.compile(r"^(utm_.*|igsh|igshid|si|feature|fbclid|gclid)$")
YT_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}
THREADS_HOSTS = {"threads.com", "threads.net"}
YT_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")


def youtube_id(url: str):
    parts = urlsplit(url)
    host = parts.netloc.lower()
    if host not in YT_HOSTS:
        return None
    if host == "youtu.be":
        cand = parts.path.strip("/").split("/")[0]
    elif parts.path.startswith("/shorts/"):
        cand = parts.path.split("/")[2]
    else:
        cand = dict(parse_qsl(parts.query)).get("v", "")
    return cand if YT_ID.match(cand) else None


def normalize(raw: str) -> str:
    url = raw.strip()
    parts = urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.netloc:
        raise ValueError(f"지원하지 않는 주소입니다: {raw[:80]}")
    vid = youtube_id(url)
    if vid:
        return f"https://www.youtube.com/watch?v={vid}"
    query = urlencode([(k, v) for k, v in parse_qsl(parts.query) if not TRACKING.match(k)])
    if parts.netloc.lower().removeprefix("www.") in {"instagram.com"} | THREADS_HOSTS:
        query = ""  # 인스타그램과 스레드 주소의 꼬리표는 모두 추적용이다
    return urlunsplit(("https", parts.netloc.lower(), parts.path, query, ""))


def classify(url: str) -> str:
    parts = urlsplit(url)
    host = parts.netloc.lower().removeprefix("www.")
    if host == "instagram.com":
        if parts.path.startswith(("/reel/", "/reels/")):
            return "instagram_reel"
        if parts.path.startswith("/p/"):
            return "instagram_post"
    if host in THREADS_HOSTS:
        return "threads"
    if youtube_id(url):
        return "youtube"
    return "article"
