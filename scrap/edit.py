from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from types import SimpleNamespace

from . import html_store, notify, notion_store
from .delete import CARD_ID
from .main import SITE, git_publish

REAL = SimpleNamespace(publish=git_publish, notion_update=notion_store.update_meta, notify=notify.send)


def _clean(s, limit: int) -> str:
    return re.sub(r"\s+", " ", str(s or "")).strip()[:limit]


def clean_tags(tags) -> list[str]:
    """태그 목록을 다듬는다. 문자열 하나로 와도 쉼표·공백으로 나눈다. 앞의 #은 뗀다."""
    if isinstance(tags, str):
        tags = re.split(r"[,\s]+", tags)
    out = []
    for t in tags if isinstance(tags, list) else []:
        t = _clean(t, 30).lstrip("#").strip()
        if t and t not in out:
            out.append(t)
    return out[:10]


def process(payload: dict, root: Path, deps=REAL) -> str:
    """자동 스크랩 카드의 제목·분류·태그를 사이트와 노션에서 고친다.

    payload에 series가 있으면 시리즈 연결도 바꾼다(빈 값이면 해제). 시리즈는 사이트에만 저장한다."""
    card_id = str(payload.get("id") or "")
    title, category = _clean(payload.get("title"), 120), _clean(payload.get("category"), 20)
    if not CARD_ID.match(card_id) or not title or not category:
        deps.notify("수정 실패", "고칠 수 없는 카드이거나 제목·분류가 비어 있습니다")
        return "실패"
    tags = clean_tags(payload.get("tags"))
    series = _clean(payload.get("series"), 40) if "series" in payload else None
    entry = html_store.update(card_id, root, title, category, tags, series)
    if entry is None:
        deps.notify("수정 실패", "이미 지워졌거나 없는 카드입니다")
        return "없음"
    deps.publish(root, f"scrap: 수정 {title}")
    problems = []
    try:
        deps.notion_update(entry["sourceUrl"], title, category, tags)
    except Exception as e:
        print(f"notion update failed: {type(e).__name__}")
        problems.append("노션에는 반영하지 못했습니다")
    deps.notify("수정 완료" if not problems else "부분 수정", "\n".join([title, *problems]), SITE + entry["file"])
    return "부분 완료" if problems else "완료"


if __name__ == "__main__":
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
    print(process(event.get("client_payload") or {}, Path.cwd()))
    sys.exit(0)
