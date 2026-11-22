import json
import pytest
from scrap import main
from scrap.models import Extracted, ExtractError

SUMMARY = {"title": "제목", "summary": "한 줄", "key_points": ["a"], "category": "테크",
           "tags": ["x"], "cover_word": "키워드", "slug": "my-card"}


class Fakes:
    def __init__(self, extract_error=None, notion_error=None, warnings=()):
        self.notes, self.notion, self.published, self.links = [], [], 0, []
        self.extract_error, self.notion_error, self.warnings = extract_error, notion_error, list(warnings)

    def extract(self, url):
        if self.extract_error:
            raise self.extract_error
        return Extracted(source_type="article", url=url, text="본문", thumbnail_url="", warnings=list(self.warnings))

    def summarize(self, ex, note, chosen, cats):
        return {**SUMMARY, "category": chosen or SUMMARY["category"]}

    def cover(self, card_id, thumb, root):
        return ""

    def publish(self, root, message):
        self.published += 1

    def notion_save(self, url, status, note, card=None, raw_text="", warnings=()):
        if self.notion_error:
            raise self.notion_error
        self.notion.append((url, status, card.id if card else None))
        return "https://notion.so/page"

    def notify(self, title, message, link=""):
        self.notes.append((title, message))
        self.links.append(link)


@pytest.fixture
def root(tmp_path):
    (tmp_path / "cards").mkdir()
    (tmp_path / "scraps.json").write_text("[]", encoding="utf-8")
    (tmp_path / "categories.json").write_text(json.dumps([{"name": "테크"}, {"name": "etc"}], ensure_ascii=False), encoding="utf-8")
    return tmp_path


def run(root, fakes, url="https://e.com/a?utm_source=x", category="", note="메모"):
    return main.process(url, note, category, root, today="2026-11-22", deps=fakes)


def test_success_saves_everywhere(root):
    f = Fakes()
    assert run(root, f) == "완료"
    entry = json.loads((root / "scraps.json").read_text(encoding="utf-8"))[0]
    assert entry["id"] == "scrap-20261122-my-card" and entry["sourceUrl"] == "https://e.com/a"
    assert f.published == 1 and f.notion == [("https://e.com/a", "완료", "scrap-20261122-my-card")]
    assert f.notes[0][0] == "저장 완료"


def test_duplicate_is_skipped(root):
    run(root, Fakes())
    f = Fakes()
    assert run(root, f) == "중복"
    assert f.published == 0 and f.notion == [] and f.notes[0][0] == "이미 저장됨"


def test_extract_failure_saves_link_to_notion_only(root):
    f = Fakes(extract_error=ExtractError("비공개 게시물"))
    assert run(root, f) == "실패"
    assert json.loads((root / "scraps.json").read_text(encoding="utf-8")) == []
    assert f.notion == [("https://e.com/a", "실패", None)] and "비공개 게시물" in f.notes[0][1]


def test_warnings_make_partial(root):
    f = Fakes(warnings=["음성을 받아쓰지 못해 캡션만으로 정리했습니다"])
    assert run(root, f) == "부분 완료"
    assert f.notion[0][1] == "부분 완료"


def test_notion_failure_keeps_html_and_reports(root):
    f = Fakes(notion_error=RuntimeError("notion down"))
    assert run(root, f) == "부분 완료"
    assert len(json.loads((root / "scraps.json").read_text(encoding="utf-8"))) == 1
    assert "노션" in f.notes[0][1]


def test_new_category_is_added(root):
    run(root, Fakes(), category="여행")
    names = [c["name"] for c in json.loads((root / "categories.json").read_text(encoding="utf-8"))]
    assert names == ["테크", "etc", "여행"]


def test_invalid_url_notifies(root):
    f = Fakes()
    assert run(root, f, url="not a url") == "실패"
    assert f.notes[0][0] == "저장 실패"


def test_slug_collision_gets_suffix(root):
    run(root, Fakes(), url="https://e.com/a")
    run(root, Fakes(), url="https://e.com/b")
    ids = [e["id"] for e in json.loads((root / "scraps.json").read_text(encoding="utf-8"))]
    assert ids == ["scrap-20261122-my-card-2", "scrap-20261122-my-card"]


def test_read_request_prefers_event_file(tmp_path, monkeypatch):
    event = tmp_path / "event.json"
    event.write_text(json.dumps({"client_payload": {"url": "https://e.com/a", "note": "메모"}}), encoding="utf-8")
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event))
    monkeypatch.delenv("SCRAP_URL", raising=False)
    assert main.read_request() == {"url": "https://e.com/a", "note": "메모", "category": ""}


def test_notification_links_to_site_card(root):
    f = Fakes()
    run(root, f)
    assert f.links == ["https://limpkiller-collab.github.io/knowledge-archive/cards/scrap-20261122-my-card.html"]
    g = Fakes()
    run(root, g)
    assert g.links == f.links and g.notes[0] == ("이미 저장됨", "제목")


def test_auto_label_means_no_category(root):
    run(root, Fakes(), category="자동 분류")
    names = [c["name"] for c in json.loads((root / "categories.json").read_text(encoding="utf-8"))]
    assert names == ["테크", "etc"]
