import json

import pytest
from scrap import edit, html_store
from scrap.models import Card


class Fakes:
    def __init__(self, notion_error=None):
        self.published, self.notion, self.notes, self.notion_error = [], [], [], notion_error

    def publish(self, root, message):
        self.published.append(message)

    def notion_update(self, url, title, category, tags):
        if self.notion_error:
            raise self.notion_error
        self.notion.append((url, title, category, tags))

    def notify(self, title, message, link=""):
        self.notes.append((title, link))


@pytest.fixture
def root(tmp_path):
    (tmp_path / "cards").mkdir()
    (tmp_path / "scraps.json").write_text("[]", encoding="utf-8")
    (tmp_path / "categories.json").write_text(json.dumps([{"name": "etc"}]), encoding="utf-8")
    html_store.save(Card(id="scrap-20261122-a", title="카드", summary="s", key_points=["p"], category="etc", tags=[],
                         cover_word="w", source_type="article", source="e.com", source_url="https://e.com/a",
                         date="2026-11-22"), tmp_path)
    return tmp_path


def test_edit_updates_site_and_notion(root):
    f = Fakes()
    payload = {"id": "scrap-20261122-a", "title": "  새   제목 ", "category": "테크", "tags": "#ai, 도구  ai"}
    assert edit.process(payload, root, f) == "완료"
    entry = json.loads((root / "scraps.json").read_text(encoding="utf-8"))[0]
    assert (entry["title"], entry["category"], entry["tags"]) == ("새 제목", "테크", ["ai", "도구"])
    assert f.notion == [("https://e.com/a", "새 제목", "테크", ["ai", "도구"])]
    assert f.published == ["scrap: 수정 새 제목"] and f.notes[0][0] == "수정 완료"
    assert f.notes[0][1].endswith("cards/scrap-20261122-a.html")


def test_edit_rejects_bad_input(root):
    f = Fakes()
    assert edit.process({"id": "../index", "title": "t", "category": "c"}, root, f) == "실패"
    assert edit.process({"id": "scrap-20261122-a", "title": " ", "category": "c"}, root, f) == "실패"
    assert edit.process({"id": "scrap-none", "title": "t", "category": "c"}, root, f) == "없음"
    assert f.published == []


def test_edit_reports_notion_failure(root):
    f = Fakes(notion_error=RuntimeError("x"))
    assert edit.process({"id": "scrap-20261122-a", "title": "t", "category": "etc", "tags": []}, root, f) == "부분 완료"
    assert f.notes[0][0] == "부분 수정"


def test_edit_connects_and_disconnects_series(root):
    f = Fakes()
    base = {"id": "scrap-20261122-a", "title": "카드", "category": "etc", "tags": []}
    assert edit.process({**base, "series": "  투자 & <b>편향</b>  시리즈 "}, root, f) == "완료"
    entry = json.loads((root / "scraps.json").read_text(encoding="utf-8"))[0]
    assert entry["series"] == "투자 & b편향/b 시리즈"
    edit.process(base, root, f)  # series가 없으면 그대로 둔다
    assert json.loads((root / "scraps.json").read_text(encoding="utf-8"))[0]["series"] == "투자 & b편향/b 시리즈"
    edit.process({**base, "series": ""}, root, f)
    assert "series" not in json.loads((root / "scraps.json").read_text(encoding="utf-8"))[0]
