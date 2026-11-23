from __future__ import annotations

import json
import re
import shutil
from html import escape
from pathlib import Path
from string import Template

from .models import Card

TYPE_LABELS = {"article": "기사", "instagram_post": "인스타그램", "instagram_reel": "릴스", "youtube": "유튜브", "threads": "스레드",
               "photo": "사진", "pdf": "PDF"}
TEMPLATE = Template((Path(__file__).parent / "card_template.html").read_text(encoding="utf-8"))


def _read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def find_by_url(url: str, root: Path):
    return next((e for e in _read(root / "scraps.json") if e.get("sourceUrl") == url), None)


def ensure_category(name: str, root: Path) -> bool:
    path = root / "categories.json"
    cats = _read(path)
    if any(c["name"] == name for c in cats):
        return False
    cats.append({"name": name})
    _write(path, cats)
    write_menu(root)
    return True


def write_menu(root: Path) -> None:
    """단축어가 그대로 보여줄 메뉴를 만든다. 한 줄에 항목 하나."""
    names = [c["name"] for c in _read(root / "categories.json")]
    lines = ["자동 분류", *names, "새 카테고리 입력"]
    (root / "shortcut-menu.txt").write_text("\n".join(lines), encoding="utf-8")


def _tags_html(tags) -> str:
    return " ".join(f"#{escape(t)}" for t in tags)


def _links_html(links) -> str:
    if not links:
        return ""
    items = "\n".join(
        f'<li><a href="{escape(l["url"])}" rel="noopener noreferrer" target="_blank">{escape(l["label"])}</a>'
        f'<span>{escape(l["url"])}</span></li>' for l in links)
    return f'<h2 class="links-title">본문에 나온 링크</h2>\n<ul class="links">\n{items}\n</ul>'


def render(card: Card, note: str = "") -> str:
    cover = f'<img class="cover" src="../{escape(card.cover)}" alt="">' if card.cover else ""
    return TEMPLATE.substitute(
        tags_html=_tags_html(card.tags), links_html=_links_html(card.links),
        title=escape(card.title), summary=escape(card.summary), category=escape(card.category),
        type_label=TYPE_LABELS.get(card.source_type, "기사"), date=card.date,
        cover_html=cover, points_html="\n".join(f"<li>{escape(p)}</li>" for p in card.key_points),
        note=escape(note), source_url=escape(card.source_url), source=escape(card.source),
    )


def save(card: Card, root: Path, note: str = "") -> None:
    file = f"cards/{card.id}.html"
    (root / file).write_text(render(card, note), encoding="utf-8")
    entry = {
        "id": card.id, "title": escape(card.title), "file": file, "date": card.date,
        "source": escape(card.source), "sourceUrl": card.source_url, "sourceType": card.source_type,
        "tags": [escape(t) for t in card.tags], "summary": escape(card.summary),
        "category": escape(card.category), "cover": card.cover, "coverWord": escape(card.cover_word),
    }
    if card.images:
        entry["images"] = card.images
    if note:
        entry["partial"] = True  # 일부만 정리된 카드. 같은 링크를 다시 보내면 재처리한다
    path = root / "scraps.json"
    entries = [e for e in _read(path) if e.get("sourceUrl") != card.source_url]
    entries.insert(0, entry)
    _write(path, entries)


def remove(card_id: str, root: Path):
    """카드 파일, 커버·갤러리 이미지, 목록 항목을 지운다. 지운 항목을 돌려주고, 없으면 None."""
    path = root / "scraps.json"
    entries = _read(path)
    entry = next((e for e in entries if e.get("id") == card_id), None)
    if entry is None:
        return None
    _write(path, [e for e in entries if e.get("id") != card_id])
    for rel in (f"cards/{card_id}.html", f"covers/{card_id}.jpg"):
        target = root / rel
        if target.is_file():
            target.unlink()
    shutil.rmtree(root / "covers" / card_id, ignore_errors=True)  # 갤러리 이미지와 직접 추가한 이미지
    manifest = root / "card-images.json"
    if manifest.is_file():
        added = _read(manifest)
        if added.pop(card_id, None) is not None:
            _write(manifest, added)
    return entry


def update(card_id: str, root: Path, title: str, category: str, tags: list[str], series: str | None = None):
    """카드의 제목·분류·태그를 고친다. 목록과 카드 파일을 함께 바꾸고 고친 항목을 돌려준다. 없으면 None.

    series를 주면 시리즈도 바꾼다. 빈 문자열이면 연결을 푼다. 직접 정리한 지식카드의 시리즈 이름과
    글자 그대로 같아야 한 시리즈로 묶이므로 이스케이프하지 않고, 꺾쇠만 뺀 채 저장한다."""
    path = root / "scraps.json"
    entries = _read(path)
    entry = next((e for e in entries if e.get("id") == card_id), None)
    if entry is None:
        return None
    entry.update({"title": escape(title), "category": escape(category), "tags": [escape(t) for t in tags]})
    if series is not None:
        series = re.sub(r"[<>]", "", series).strip()
        if series:
            entry["series"] = series
        else:
            entry.pop("series", None)
    _write(path, entries)
    ensure_category(category, root)
    file = root / entry["file"]
    if file.is_file():
        html = file.read_text(encoding="utf-8")
        html = re.sub(r"<title>.*?</title>", lambda m: f"<title>{escape(title)}</title>", html, count=1, flags=re.S)
        html = re.sub(r"<h1>.*?</h1>", lambda m: f"<h1>{escape(title)}</h1>", html, count=1, flags=re.S)
        html = re.sub(r'(<div class="kicker">)[^<]*?( · [^<]*</div>)',
                      lambda m: m.group(1) + escape(category) + m.group(2), html, count=1)
        tags_p = f'<p class="tags">{_tags_html(tags)}</p>'
        if '<p class="tags">' in html:
            html = re.sub(r'<p class="tags">.*?</p>', lambda m: tags_p, html, count=1, flags=re.S)
        else:
            html = re.sub(r'(<p class="summary">.*?</p>)', lambda m: m.group(1) + "\n" + tags_p, html, count=1, flags=re.S)
        file.write_text(html, encoding="utf-8")
    return entry
