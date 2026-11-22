from __future__ import annotations

import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

from . import covers, extract, html_store, notify, notion_store, summarize, urls
from .models import Card, ExtractError

SITE = "https://limpkiller-collab.github.io/knowledge-archive/"
SOURCE_NAMES = {"article": "기사", "instagram_post": "인스타그램", "instagram_reel": "인스타그램 릴스", "youtube": "유튜브"}


def git_publish(root: Path, message: str) -> None:
    def git(*args):
        subprocess.run(["git", *args], cwd=root, check=True)
    paths = [p for p in ("cards", "covers", "scraps.json", "categories.json") if (root / p).exists()]
    git("add", *paths)
    git("commit", "-m", message)
    try:
        git("push")
    except subprocess.CalledProcessError:
        git("pull", "--rebase")
        git("push")


def wait_live(url: str, timeout: int = 150) -> None:
    """사이트 배포가 끝나 카드 주소가 열릴 때까지 기다린다. 알림을 눌렀을 때 빈 페이지가 뜨지 않게 하려는 것이다."""
    import time

    import requests

    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            if requests.get(url, timeout=10).status_code == 200:
                return
        except requests.RequestException:
            pass
        time.sleep(5)


REAL = SimpleNamespace(wait_live=wait_live, extract=extract.run, summarize=summarize.run, cover=covers.save,
                       publish=git_publish, notion_save=notion_store.save, notify=notify.send)


def process(raw_url: str, note: str, category: str, root: Path, today: str, deps=REAL) -> str:
    try:
        url = urls.normalize(raw_url)
    except ValueError as e:
        deps.notify("저장 실패", str(e))
        return "실패"
    existing = html_store.find_by_url(url, root)
    if existing:
        deps.notify("이미 저장됨", existing["title"], SITE + existing["file"])
        return "중복"

    category = re.sub(r"\s+", " ", category).strip()[:20]
    if category:
        html_store.ensure_category(category, root)
    categories = [c["name"] for c in json.loads((root / "categories.json").read_text(encoding="utf-8"))]

    try:
        ex = deps.extract(url)
        out = deps.summarize(ex, note, category, categories)
    except (ExtractError, summarize.SummarizeError) as e:
        try:
            deps.notion_save(url, "실패", note)
        except Exception:
            pass
        deps.notify("저장 실패", f"{e}\n{url}")
        return "실패"

    base_id = f"scrap-{today.replace('-', '')}-{out['slug']}"
    card_id, n = base_id, 2
    while (root / f"cards/{card_id}.html").exists():
        card_id, n = f"{base_id}-{n}", n + 1
    card = Card(id=card_id, title=out["title"], summary=out["summary"], key_points=out["key_points"],
                category=out["category"], tags=out["tags"], cover_word=out["cover_word"],
                source_type=ex.source_type, source=ex.author or SOURCE_NAMES[ex.source_type],
                source_url=url, date=today)
    card.cover = deps.cover(card_id, ex.thumbnail_url, root)
    problems = list(ex.warnings)

    html_store.save(card, root, note=" · ".join(ex.warnings))
    deps.publish(root, f"scrap: {card.title}")

    link = f"{SITE}cards/{card.id}.html"
    try:
        status = "부분 완료" if problems else "완료"
        deps.notion_save(url, status, note, card=card,
                                raw_text="\n\n".join(p for p in [ex.text, ex.transcript] if p), warnings=ex.warnings)
    except Exception:
        problems.append("노션 저장에 실패했습니다")

    getattr(deps, "wait_live", lambda u: None)(link)
    if problems:
        deps.notify("부분 저장", f"{card.title}\n" + "\n".join(problems), link)
        return "부분 완료"
    deps.notify("저장 완료", card.title, link)
    return "완료"


def read_request() -> dict:
    """요청 내용을 읽는다. Actions에서는 이벤트 파일에서 직접 읽어 메모가 공개 실행 기록에 찍히지 않게 한다."""
    path = os.environ.get("GITHUB_EVENT_PATH")
    if path and not os.environ.get("SCRAP_URL"):
        payload = json.loads(Path(path).read_text(encoding="utf-8")).get("client_payload") or {}
        return {k: str(payload.get(k) or "") for k in ("url", "note", "category")}
    return {"url": os.environ.get("SCRAP_URL", ""), "note": os.environ.get("SCRAP_NOTE", ""),
            "category": os.environ.get("SCRAP_CATEGORY", "")}


if __name__ == "__main__":
    req = read_request()
    result = process(req["url"], req["note"], req["category"], Path.cwd(), today=datetime.date.today().isoformat())
    print(result)
    sys.exit(0)
