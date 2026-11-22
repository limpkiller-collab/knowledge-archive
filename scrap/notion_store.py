from __future__ import annotations

import os

from notion_client import Client

from .html_store import TYPE_LABELS
from .models import Card

SITE = "https://limpkiller-collab.github.io/knowledge-archive/"


def _text(s: str) -> list:
    return [{"type": "text", "text": {"content": s[:2000]}}]


def _chunks(s: str, size: int = 1900) -> list[str]:
    return [s[i:i + size] for i in range(0, len(s), size)] or [""]


def _props(url: str, status: str, note: str, card: Card | None) -> dict:
    props = {"URL": {"url": url}, "상태": {"select": {"name": status}}, "메모": {"rich_text": _text(note)}}
    if card is None:
        props["제목"] = {"title": _text(url)}
        return props
    props.update({
        "제목": {"title": _text(card.title)},
        "출처 유형": {"select": {"name": TYPE_LABELS.get(card.source_type, "기사")}},
        "카테고리": {"select": {"name": card.category}},
        "태그": {"multi_select": [{"name": t.replace(",", " ")[:100]} for t in card.tags]},
        "한 줄 요약": {"rich_text": _text(card.summary)},
        "저장일": {"date": {"start": card.date}},
        "HTML 카드": {"url": f"{SITE}cards/{card.id}.html"},
    })
    return props


def _children(card: Card | None, raw_text: str, warnings: list[str]) -> list:
    blocks = [{"type": "image", "image": {"type": "external", "external": {"url": SITE + rel}}}
              for rel in (card.images if card else [])]
    blocks += [{"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": _text(p)}}
              for p in (card.key_points if card else [])]
    blocks += [{"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [
        {"type": "text", "text": {"content": l["label"][:200], "link": {"url": l["url"]}}}]}}
        for l in (card.links if card else [])]
    blocks += [{"type": "callout", "callout": {"rich_text": _text(w)}} for w in warnings]
    if raw_text:
        blocks.append({"type": "toggle", "toggle": {
            "rich_text": _text("추출 원문"),
            "children": [{"type": "paragraph", "paragraph": {"rich_text": _text(c)}} for c in _chunks(raw_text)[:90]],
        }})
    return blocks


def save(url: str, status: str, note: str, card: Card | None = None, raw_text: str = "", warnings=()) -> str:
    """같은 URL의 행이 있으면 속성을 갱신하고, 없으면 새로 만든다. 페이지 주소를 돌려준다."""
    client = Client(auth=os.environ["NOTION_TOKEN"])
    # Notion API 2025-09-03부터 행 조회와 생성은 DB가 아니라 그 안의 데이터 소스를 대상으로 한다.
    source_id = client.databases.retrieve(database_id=os.environ["NOTION_DATABASE_ID"])["data_sources"][0]["id"]
    found = client.data_sources.query(data_source_id=source_id,
                                      filter={"property": "URL", "url": {"equals": url}}, page_size=1)
    props = _props(url, status, note, card)
    extra = {"cover": {"type": "external", "external": {"url": SITE + card.cover}}} if card and card.cover else {}
    blocks = _children(card, raw_text, list(warnings))
    if found["results"]:
        page = client.pages.update(page_id=found["results"][0]["id"], properties=props, **extra)
        if blocks:
            client.blocks.children.append(block_id=page["id"], children=blocks)
    else:
        page = client.pages.create(parent={"type": "data_source_id", "data_source_id": source_id},
                                   properties=props, children=blocks, **extra)
    return page["url"]


def delete(url: str) -> int:
    """같은 URL의 행을 모두 휴지통으로 보낸다. 보낸 개수를 돌려준다."""
    client = Client(auth=os.environ["NOTION_TOKEN"])
    source_id = client.databases.retrieve(database_id=os.environ["NOTION_DATABASE_ID"])["data_sources"][0]["id"]
    found = client.data_sources.query(data_source_id=source_id, filter={"property": "URL", "url": {"equals": url}})
    for page in found["results"]:
        client.pages.update(page_id=page["id"], in_trash=True)
    return len(found["results"])


def update_meta(url: str, title: str, category: str, tags: list[str]) -> int:
    """같은 URL의 행에서 제목·카테고리·태그를 고친다. 고친 개수를 돌려준다."""
    client = Client(auth=os.environ["NOTION_TOKEN"])
    source_id = client.databases.retrieve(database_id=os.environ["NOTION_DATABASE_ID"])["data_sources"][0]["id"]
    found = client.data_sources.query(data_source_id=source_id, filter={"property": "URL", "url": {"equals": url}})
    props = {"제목": {"title": _text(title)}, "카테고리": {"select": {"name": category}},
             "태그": {"multi_select": [{"name": t.replace(",", " ")[:100]} for t in tags]}}
    for page in found["results"]:
        client.pages.update(page_id=page["id"], properties=props)
    return len(found["results"])
