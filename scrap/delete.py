from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from types import SimpleNamespace

from . import html_store, notify, notion_store
from .main import git_publish

CARD_ID = re.compile(r"^scrap-[a-z0-9-]{1,120}$")

REAL = SimpleNamespace(publish=git_publish, notion_delete=notion_store.delete, notify=notify.send)


def process(card_id: str, root: Path, deps=REAL) -> str:
    """자동 스크랩 카드 하나를 사이트와 노션에서 지운다."""
    if not CARD_ID.match(card_id or ""):
        deps.notify("삭제 실패", "지울 수 없는 카드입니다")
        return "실패"
    entry = html_store.remove(card_id, root)
    if entry is None:
        deps.notify("삭제 실패", "이미 지워졌거나 없는 카드입니다")
        return "없음"
    deps.publish(root, f"scrap: 삭제 {entry['title']}")
    problems = []
    try:
        deps.notion_delete(entry["sourceUrl"])
    except Exception as e:
        print(f"notion delete failed: {type(e).__name__}")
        problems.append("노션에서는 지우지 못했습니다")
    deps.notify("삭제 완료" if not problems else "부분 삭제", "\n".join([entry["title"], *problems]))
    return "부분 완료" if problems else "완료"


if __name__ == "__main__":
    payload = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8")).get("client_payload") or {}
    print(process(str(payload.get("id") or ""), Path.cwd()))
    sys.exit(0)
