import json

import pytest
from scrap import delete, html_store
from scrap.models import Card


class Fakes:
    def __init__(self, notion_error=None):
        self.published, self.notion, self.notes, self.notion_error = [], [], [], notion_error

    def publish(self, root, message):
        self.published.append(message)

    def notion_delete(self, url):
        if self.notion_error:
            raise self.notion_error
        self.notion.append(url)

    def notify(self, title, message, link=""):
        self.notes.append((title, message))


@pytest.fixture
def root(tmp_path):
    (tmp_path / "cards").mkdir()
    (tmp_path / "covers").mkdir()
    (tmp_path / "scraps.json").write_text("[]", encoding="utf-8")
    card = Card(id="scrap-20261122-a", title="카드", summary="s", key_points=["p"], category="etc", tags=[],
                cover_word="w", source_type="article", source="e.com", source_url="https://e.com/a", date="2026-11-22",
                cover="covers/scrap-20261122-a.jpg")
    html_store.save(card, tmp_path)
    (tmp_path / "covers/scrap-20261122-a.jpg").write_bytes(b"x")
    return tmp_path


def test_delete_removes_files_entry_and_notion(root):
    f = Fakes()
    assert delete.process("scrap-20261122-a", root, f) == "완료"
    assert json.loads((root / "scraps.json").read_text(encoding="utf-8")) == []
    assert not (root / "cards/scrap-20261122-a.html").exists() and not (root / "covers/scrap-20261122-a.jpg").exists()
    assert f.notion == ["https://e.com/a"] and len(f.published) == 1 and f.notes[0][0] == "삭제 완료"


def test_delete_unknown_card_changes_nothing(root):
    f = Fakes()
    assert delete.process("scrap-none", root, f) == "없음"
    assert f.published == [] and len(json.loads((root / "scraps.json").read_text(encoding="utf-8"))) == 1


@pytest.mark.parametrize("bad", ["", "bonds-vs-stocks", "scrap-../../x", "scrap-A", "../index"])
def test_delete_rejects_ids_outside_scraps(root, bad):
    f = Fakes()
    assert delete.process(bad, root, f) == "실패"
    assert f.published == [] and (root / "cards/scrap-20261122-a.html").exists()


def test_notion_failure_is_reported(root):
    f = Fakes(notion_error=RuntimeError("down"))
    assert delete.process("scrap-20261122-a", root, f) == "부분 완료"
    assert f.notes[0][0] == "부분 삭제" and "노션" in f.notes[0][1]
