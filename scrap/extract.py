from __future__ import annotations

import html as html_lib
import os
import re
from urllib.parse import urlsplit

import requests
import trafilatura

from . import gemini
from . import transcribe as stt
from .models import Extracted, ExtractError
from .urls import classify, youtube_id

IG_ACTOR = "apify~instagram-scraper"
WATCH_PROMPT = """이 영상의 내용을 한국어로 빠짐없이 글로 풀어 써라.
첫 줄에 영상 제목과 채널 이름을 적는다. 이어서 영상이 말하는 주장, 근거, 수치, 순서, 예시를 시간 순서대로 적는다.
화면에만 나오는 글자나 도표의 내용도 포함한다. 의견이나 평가는 덧붙이지 않는다."""
APIFY = "https://api.apify.com/v2/acts/{actor}/run-sync-get-dataset-items"


def _apify(actor: str, payload: dict) -> dict:
    resp = requests.post(APIFY.format(actor=actor), params={"token": os.environ["APIFY_TOKEN"]}, json=payload, timeout=320)
    if resp.status_code >= 400:
        # 실패 원인을 실행 기록에서 볼 수 있게 남긴다. Apify의 오류 본문에는 비밀 값이 없다.
        print(f"apify http {resp.status_code}: {resp.text[:300]}")
        raise ExtractError(f"인스타그램을 읽지 못했습니다 (Apify 오류 {resp.status_code})")
    items = resp.json()
    if not items:
        print("apify returned no items")
        raise ExtractError("게시물을 가져오지 못했습니다 (비공개이거나 차단됨)")
    if items[0].get("error"):
        print(f"apify item error: {items[0].get('error')} / {str(items[0].get('errorDescription'))[:200]}")
        # 인스타그램이 로그인하지 않은 방문자에게 일부 정보만 주는 게시물이 있다. 캡션이라도 있으면 그것으로 진행한다.
        if not (items[0].get("caption") or items[0].get("displayUrl")):
            raise ExtractError("게시물을 가져오지 못했습니다 (비공개이거나 열람이 제한됨)")
        items[0]["_partial"] = True
    print("apify item keys:", sorted(items[0].keys()))
    return items[0]


def _from_article(url: str, html: str) -> Extracted:
    text = trafilatura.extract(html, include_comments=False) or ""
    if len(text.strip()) < 200:
        raise ExtractError("기사 본문을 찾지 못했습니다")
    meta = trafilatura.extract_metadata(html)
    # 출처 이름은 사이트 이름을 쓴다. 본문에서 뽑은 작성자 값은 엉뚱한 글자가 섞이는 일이 있어 쓰지 않는다.
    site = ((meta.sitename or "") if meta else "") or urlsplit(url).netloc.replace("www.", "", 1)
    return Extracted(source_type="article", url=url, text=text, title=(meta.title or "") if meta else "",
                     author=site, published_at=(meta.date or "") if meta else "",
                     thumbnail_url=(meta.image or "") if meta else "")


def _post_images(item: dict) -> list[str]:
    """게시물에 들어 있는 이미지 주소를 순서대로 모은다. 여러 장 게시물은 images 또는 childPosts에 담겨 온다."""
    urls = list(item.get("images") or [])
    if not urls:
        urls = [c.get("displayUrl") for c in (item.get("childPosts") or []) if c.get("displayUrl")]
    if not urls and item.get("displayUrl"):
        urls = [item["displayUrl"]]
    return urls


def _from_instagram(url: str, kind: str, item: dict, transcribe) -> Extracted:
    ex = Extracted(source_type=kind, url=url, text=item.get("caption") or "", author=item.get("ownerUsername") or "",
                   published_at=(item.get("timestamp") or "")[:10], thumbnail_url=item.get("displayUrl") or "",
                   images=_post_images(item))
    if item.get("_partial"):
        ex.warnings.append("인스타그램이 일부 정보만 제공해 캡션 중심으로 정리했습니다")
    print(f"instagram item: type={item.get('type')} productType={item.get('productType')} "
          f"images={len(item.get('images') or [])} hasVideo={bool(item.get('videoUrl'))}")
    if kind == "instagram_reel":
        # 영상은 대표 화면 한 장만 이미지로 넘기고, 내용은 음성 받아쓰기로 얻는다.
        ex.images = [ex.thumbnail_url] if ex.thumbnail_url else []
        ex.media_url = item.get("videoUrl") or ""
        if not ex.media_url:
            ex.warnings.append("영상 파일을 받지 못해 캡션과 대표 화면만으로 정리했습니다")
        else:
            try:
                ex.transcript = transcribe(ex.media_url, item.get("audioUrl") or "")
            except Exception as e:
                print(f"transcribe failed: {type(e).__name__}: {str(e)[:200]}")
                ex.warnings.append("음성을 받아쓰지 못해 캡션과 대표 화면만으로 정리했습니다")
    if not (ex.text or ex.transcript or ex.images):
        raise ExtractError("게시물에 정리할 내용이 없습니다")
    return ex


META_TAG = re.compile(r"<meta\b[^>]*>", re.I)
META_ATTR = re.compile(r'([a-zA-Z:_-]+)\s*=\s*"([^"]*)"')
# 스레드는 로그인하지 않은 방문자에게 본문을 주지 않는다. 링크 미리보기용으로 주는 정보를 읽는다.
PREVIEW_AGENT = "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)"


def _meta(html: str) -> dict:
    """<meta property|name="…" content="…"> 값을 모은다. 같은 이름은 처음 나온 값을 쓴다."""
    found = {}
    for tag in META_TAG.findall(html):
        attrs = {k.lower(): html_lib.unescape(v) for k, v in META_ATTR.findall(tag)}
        key = attrs.get("property") or attrs.get("name")
        if key and attrs.get("content"):
            found.setdefault(key, attrs["content"])
    return found


def _from_threads(url: str, html: str) -> Extracted:
    meta = _meta(html)
    text = (meta.get("og:description") or "").strip()
    if not text:
        raise ExtractError("스레드 글을 읽지 못했습니다 (비공개이거나 삭제된 글)")
    handle = re.search(r"\(@([A-Za-z0-9._]+)\)", meta.get("og:title") or "")
    canonical = meta.get("og:url") or url
    if classify(canonical) != "threads":
        canonical = url
    image = meta.get("og:image") or ""
    return Extracted(source_type="threads", url=canonical.split("?")[0], text=text,
                     author=handle.group(1) if handle else "", thumbnail_url=image,
                     images=[image] if image else [])


def _gemini_watch(url: str) -> str:
    """Gemini가 유튜브 영상을 직접 보고 내용을 글로 풀어 준다."""
    return gemini.generate([{"file_data": {"file_uri": url}}, {"text": WATCH_PROMPT}], timeout=600)


def _from_youtube(url: str, watch=_gemini_watch) -> Extracted:
    try:
        notes = watch(url)
    except Exception as e:
        raise ExtractError("영상을 읽지 못했습니다 (비공개이거나 너무 긴 영상)") from e
    if not notes:
        raise ExtractError("영상에서 정리할 내용을 찾지 못했습니다")
    return Extracted(source_type="youtube", url=url, transcript=notes,
                     thumbnail_url=f"https://i.ytimg.com/vi/{youtube_id(url)}/hqdefault.jpg")


def run(url: str) -> Extracted:
    kind = classify(url)
    if kind == "article":
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (compatible; link-scrap)"}, timeout=30)
        resp.raise_for_status()
        return _from_article(url, resp.text)
    if kind == "youtube":
        return _from_youtube(url)
    if kind == "threads":
        resp = requests.get(url, headers={"User-Agent": PREVIEW_AGENT}, timeout=30)
        resp.raise_for_status()
        return _from_threads(url, resp.text)
    item = _apify(IG_ACTOR, {"directUrls": [url], "resultsType": "posts", "resultsLimit": 1})
    return _from_instagram(url, kind, item, transcribe=stt.from_media_url)
