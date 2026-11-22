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
SOURCE_NAMES = {"article": "기사", "instagram_post": "인스타그램", "instagram_reel": "인스타그램 릴스", "youtube": "유튜브", "threads": "스레드"}


def git_publish(root: Path, message: str) -> None:
    def git(*args, check=True):
        return subprocess.run(["git", *args], cwd=root, check=check)
    # 경로마다 따로 반영한다. 아직 없는 경로는 건너뛰고, 지워진 파일은 삭제로 반영된다.
    for path in ("cards", "covers", "scraps.json", "categories.json", "shortcut-menu.txt", "card-images.json"):
        git("add", "-A", "--", path, check=False)
    if git("diff", "--cached", "--quiet", check=False).returncode == 0:
        return  # 바뀐 것이 없다(값을 그대로 저장한 편집 등)
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
                       images=covers.save_all,
                       publish=git_publish, notion_save=notion_store.save, notify=notify.send)


def process(raw_url: str, note: str, category: str, root: Path, today: str, deps=REAL) -> str:
    try:
        url = urls.normalize(raw_url)
    except ValueError as e:
        deps.notify("저장 실패", str(e))
        return "실패"
    existing = html_store.find_by_url(url, root)
    if existing and not existing.get("partial"):
        deps.notify("이미 저장됨", existing["title"], SITE + existing["file"])
        return "중복"

    category = re.sub(r"\s+", " ", category).strip()[:20]
    if category == "자동 분류":  # 단축어 메뉴의 "자동 분류" 항목은 빈 값과 같다
        category = ""
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

    if ex.url and ex.url != url:
        # 공유용 짧은 주소였다. 실제 글 주소로 저장하고, 그 주소로 이미 저장한 카드는 그대로 둔다.
        url = ex.url
        existing = html_store.find_by_url(url, root)
        if existing and not existing.get("partial"):
            deps.notify("이미 저장됨", existing["title"], SITE + existing["file"])
            return "중복"
    if existing:
        card_id = existing["id"]  # 부분 완료였던 카드를 같은 주소로 다시 만든다
    else:
        base_id = f"scrap-{today.replace('-', '')}-{out['slug']}"
        card_id, n = base_id, 2
        while (root / f"cards/{card_id}.html").exists():
            card_id, n = f"{base_id}-{n}", n + 1
    card = Card(id=card_id, title=out["title"], summary=out["summary"], key_points=out["key_points"],
                category=out["category"], tags=out["tags"], cover_word=out["cover_word"],
                source_type=ex.source_type, source=ex.author or SOURCE_NAMES[ex.source_type],
                source_url=url, date=today, links=[l for l in out.get("links") or [] if l["url"] != url])
    card.cover = deps.cover(card_id, ex.thumbnail_url, root)
    if ex.source_type in ("instagram_post", "threads") and len(ex.images) > 1:
        # 여러 장 게시물은 전부 저장해 카드에서 넘겨 볼 수 있게 한다
        card.images = getattr(deps, "images", lambda *a: [])(card_id, ex.images, root)
        card.cover = card.cover or (card.images[0] if card.images else "")
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
