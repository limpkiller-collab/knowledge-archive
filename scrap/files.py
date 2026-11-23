"""단축어로 보낸 사진·PDF 파일을 카드로 정리한다.

파일은 링크와 달리 요청에 담기에 너무 커서, 단축어가 비공개 저장소(받은 파일함)의 inbox/<묶음>/ 에 먼저 올리고
묶음 이름만 알려 준다. 여기서 그 파일을 읽어 Claude에 그대로 넘긴다. 원본은 비공개 저장소에만 남고,
공개 사이트에는 사진(크기를 줄인 것)과 요약만 올라간다. PDF 원본은 올리지 않는다.
"""
from __future__ import annotations

import base64
import io
import json
import os
import re
import sys
from pathlib import Path
from types import SimpleNamespace

from . import covers, html_store, notify, notion_store, summarize
from .main import SITE, git_publish, today_kst, wait_live
from .models import Card, Extracted, ExtractError

INBOX_REPO = "limpkiller-collab/knowledge-archive-inbox"
BATCH = re.compile(r"^[A-Za-z0-9_-]{1,40}$")
MAX_FILES = 12
MAX_IMAGES = 10
MAX_PDF_BYTES = 20 * 1024 * 1024  # PDF를 모두 합친 크기
MAX_FILE_BYTES = 25 * 1024 * 1024
SOURCE_NAMES = {"photo": "보낸 사진", "pdf": "보낸 PDF"}


def inbox_repo() -> str:
    return os.environ.get("INBOX_REPO") or INBOX_REPO


def source_url(batch: str) -> str:
    """카드의 원본 주소. 비공개 저장소의 묶음 폴더라서 저장소 주인만 열 수 있다."""
    return f"https://github.com/{inbox_repo()}/tree/main/inbox/{batch}"


def fetch_batch(batch: str) -> list[bytes]:
    """받은 파일함에서 묶음의 파일을 이름 순서(1, 2, … 10)로 읽는다."""
    import requests

    token = os.environ.get("INBOX_TOKEN")
    if not token:
        raise ExtractError("받은 파일함 토큰(INBOX_TOKEN)이 등록되지 않았습니다")
    api = f"https://api.github.com/repos/{inbox_repo()}/contents/inbox/{batch}"
    headers = {"Authorization": f"Bearer {token}", "X-GitHub-Api-Version": "2022-11-28"}
    try:
        listing = requests.get(api, headers={**headers, "Accept": "application/vnd.github+json"}, timeout=30)
        if listing.status_code in (401, 403):
            raise ExtractError("받은 파일함을 읽을 권한이 없습니다. INBOX_TOKEN을 확인해 주세요")
        if listing.status_code == 404:
            raise ExtractError("보낸 파일을 찾지 못했습니다")
        listing.raise_for_status()
        items = [i for i in listing.json() if isinstance(i, dict) and i.get("type") == "file"]
        if len(items) > MAX_FILES:
            raise ExtractError(f"한 번에 보낼 수 있는 파일은 {MAX_FILES}개까지입니다")

        def order(item):
            m = re.match(r"\d+", item["name"])
            return (int(m.group()) if m else 10 ** 9, item["name"])

        files = []
        for item in sorted(items, key=order):
            if item.get("size", 0) > MAX_FILE_BYTES:
                raise ExtractError("파일이 너무 큽니다 (파일 하나에 25MB까지)")
            raw = requests.get(f"{api}/{item['name']}", headers={**headers, "Accept": "application/vnd.github.raw"},
                               timeout=120)
            raw.raise_for_status()
            files.append(raw.content)
        return files
    except requests.RequestException as e:
        raise ExtractError("받은 파일함에서 파일을 읽지 못했습니다") from e


def _open_image(data: bytes):
    from PIL import Image, ImageOps

    try:
        from pillow_heif import register_heif_opener  # 아이폰 사진(HEIC)
        register_heif_opener()
    except ImportError:
        pass
    img = Image.open(io.BytesIO(data))
    return ImageOps.exif_transpose(img).convert("RGB")  # 세로로 찍은 사진이 눕지 않게


def _jpeg(img, limit: int, quality: int) -> bytes:
    img = img.copy()
    img.thumbnail((limit, limit))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=quality)
    return buf.getvalue()


def prepare(files: list[bytes]) -> tuple[Extracted, list[bytes]]:
    """파일을 Claude에 넘길 입력으로 바꾼다. (추출 결과, 카드에 실을 사진 JPEG 목록)을 돌려준다."""
    blocks, photos, warnings, pdf_bytes, skipped = [], [], [], 0, 0
    for data in files:
        if data[:5] == b"%PDF-":
            pdf_bytes += len(data)
            if pdf_bytes > MAX_PDF_BYTES:
                raise ExtractError("PDF가 너무 큽니다 (합쳐서 20MB까지)")
            blocks.append({"type": "document", "source": {"type": "base64", "media_type": "application/pdf",
                                                           "data": base64.b64encode(data).decode("ascii")}})
            continue
        try:
            img = _open_image(data)
        except Exception as e:
            print(f"file skipped: {type(e).__name__}")
            skipped += 1
            continue
        if len(photos) >= MAX_IMAGES:
            skipped += 1
            continue
        photos.append(_jpeg(img, 1600, 85))
        blocks.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                                    "data": base64.b64encode(_jpeg(img, 1568, 85)).decode("ascii")}})
    if not blocks:
        raise ExtractError("읽을 수 있는 사진이나 PDF가 없습니다")
    if skipped:
        warnings.append(f"파일 {skipped}개는 읽지 못해 빼고 정리했습니다")
    kind = "pdf" if pdf_bytes else "photo"
    ex = Extracted(source_type=kind, url="", attachments=blocks, warnings=warnings)
    return ex, photos


REAL = SimpleNamespace(fetch=fetch_batch, summarize=summarize.run, cover=covers.save, images=covers.save_all,
                       publish=git_publish, notion_save=notion_store.save, notify=notify.send, wait_live=wait_live)


def process(payload: dict, root: Path, today: str, deps=REAL) -> str:
    batch = str(payload.get("batch") or "")
    note = str(payload.get("note") or "")
    if not BATCH.match(batch):
        deps.notify("저장 실패", "보낸 파일의 묶음 이름이 올바르지 않습니다")
        return "실패"
    url = source_url(batch)
    existing = html_store.find_by_url(url, root)
    if existing:
        deps.notify("이미 저장됨", existing["title"], SITE + existing["file"])
        return "중복"

    category = re.sub(r"\s+", " ", str(payload.get("category") or "")).strip()[:20]
    if category == "자동 분류":
        category = ""
    if category:
        html_store.ensure_category(category, root)
    categories = [c["name"] for c in json.loads((root / "categories.json").read_text(encoding="utf-8"))]

    try:
        ex, photos = prepare(deps.fetch(batch))
        out = deps.summarize(ex, note, category, categories)
    except (ExtractError, summarize.SummarizeError) as e:
        try:
            deps.notion_save(url, "실패", note)
        except Exception:
            pass
        deps.notify("저장 실패", str(e))
        return "실패"

    base_id = f"scrap-{today.replace('-', '')}-{out['slug']}"
    card_id, n = base_id, 2
    while (root / f"cards/{card_id}.html").exists():
        card_id, n = f"{base_id}-{n}", n + 1
    card = Card(id=card_id, title=out["title"], summary=out["summary"], key_points=out["key_points"],
                category=out["category"], tags=out["tags"], cover_word=out["cover_word"],
                source_type=ex.source_type, source=SOURCE_NAMES[ex.source_type], source_url=url, date=today,
                links=out.get("links") or [])
    if photos:
        keys = [str(i) for i in range(len(photos))]
        fetch = lambda key: photos[int(key)]  # noqa: E731 — 이미 받아 둔 사진을 그대로 넘긴다
        card.cover = deps.cover(card_id, keys[0], root, fetch)
        if len(photos) > 1:
            card.images = deps.images(card_id, keys, root, fetch)
            card.cover = card.cover or (card.images[0] if card.images else "")
    problems = list(ex.warnings)

    html_store.save(card, root, note=" · ".join(ex.warnings))
    deps.publish(root, f"scrap: {card.title}")

    link = f"{SITE}cards/{card.id}.html"
    try:
        deps.notion_save(url, "부분 완료" if problems else "완료", note, card=card, warnings=ex.warnings)
    except Exception:
        problems.append("노션 저장에 실패했습니다")

    deps.wait_live(link)
    if problems:
        deps.notify("부분 저장", f"{card.title}\n" + "\n".join(problems), link)
        return "부분 완료"
    deps.notify("저장 완료", card.title, link)
    return "완료"


if __name__ == "__main__":
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
    print(process(event.get("client_payload") or {}, Path.cwd(), today=today_kst()))
    sys.exit(0)
