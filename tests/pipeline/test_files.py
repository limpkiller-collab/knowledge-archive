import io
import json

import pytest
from PIL import Image
from scrap import files, summarize
from scrap.models import ExtractError

SUMMARY = {"title": "영수증 정리", "summary": "한 줄", "key_points": ["a"], "category": "etc",
           "tags": ["x"], "cover_word": "영수증", "slug": "receipt", "links": []}
PDF = b"%PDF-1.7\n%fake"


def photo(color="red", size=(2000, 1000), fmt="PNG"):
    buf = io.BytesIO()
    Image.new("RGB", size, color).save(buf, fmt)
    return buf.getvalue()


class Fakes:
    def __init__(self, batch_files, fetch_error=None, summarize_error=None):
        self.batch_files, self.fetch_error, self.summarize_error = batch_files, fetch_error, summarize_error
        self.notes, self.notion, self.published, self.seen = [], [], [], None

    def fetch(self, batch):
        if self.fetch_error:
            raise self.fetch_error
        return self.batch_files

    def summarize(self, ex, note, chosen, cats):
        if self.summarize_error:
            raise self.summarize_error
        self.seen = ex
        return {**SUMMARY, "category": chosen or "etc"}

    cover = staticmethod(files.covers.save)
    images = staticmethod(files.covers.save_all)

    def publish(self, root, message):
        self.published.append(message)

    def notion_save(self, url, status, note, card=None, raw_text="", warnings=()):
        self.notion.append((url, status, note, card.id if card else None))

    def notify(self, title, message, link=""):
        self.notes.append((title, message, link))

    def wait_live(self, link):
        pass


@pytest.fixture
def root(tmp_path):
    (tmp_path / "cards").mkdir()
    (tmp_path / "scraps.json").write_text("[]", encoding="utf-8")
    (tmp_path / "categories.json").write_text(json.dumps([{"name": "etc"}]), encoding="utf-8")
    return tmp_path


def entries(root):
    return json.loads((root / "scraps.json").read_text(encoding="utf-8"))


def test_prepare_turns_photos_and_pdfs_into_blocks():
    ex, photos = files.prepare([photo(), PDF, b"not a file"])
    assert ex.source_type == "pdf" and [b["type"] for b in ex.attachments] == ["image", "document"]
    assert ex.attachments[0]["source"]["media_type"] == "image/jpeg"
    assert len(photos) == 1 and max(Image.open(io.BytesIO(photos[0])).size) == 1600
    assert ex.warnings == ["파일 1개는 읽지 못해 빼고 정리했습니다"]


def test_prepare_rejects_unreadable_and_oversized(monkeypatch):
    with pytest.raises(ExtractError):
        files.prepare([b"junk"])
    monkeypatch.setattr(files, "MAX_PDF_BYTES", 10)
    with pytest.raises(ExtractError):
        files.prepare([PDF])


def test_photos_become_card_with_gallery(root):
    f = Fakes([photo("red"), photo("blue")])
    assert files.process({"batch": "20261124-101500", "note": "메모", "category": "자동 분류"}, root, "2026-11-24", f) == "완료"
    entry = entries(root)[0]
    assert entry["id"] == "scrap-20261124-receipt" and entry["sourceType"] == "photo" and entry["source"] == "보낸 사진"
    assert entry["sourceUrl"].endswith("/knowledge-archive-inbox/tree/main/inbox/20261124-101500")
    assert entry["cover"] == "covers/scrap-20261124-receipt.jpg"
    assert entry["images"] == ["covers/scrap-20261124-receipt/01.jpg", "covers/scrap-20261124-receipt/02.jpg"]
    assert all((root / p).is_file() for p in entry["images"] + [entry["cover"]])
    assert len(f.seen.attachments) == 2
    html = (root / "cards/scrap-20261124-receipt.html").read_text(encoding="utf-8")
    assert "etc · 사진 · 2026-11-24" in html and "메모" not in html  # 메모는 노션에만 간다
    assert f.notion == [(entry["sourceUrl"], "완료", "메모", entry["id"])]
    assert f.notes[0][0] == "저장 완료" and f.notes[0][2].endswith("cards/scrap-20261124-receipt.html")


def test_pdf_card_has_no_images_and_same_batch_is_duplicate(root):
    f = Fakes([PDF])
    assert files.process({"batch": "b1", "category": "문서"}, root, "2026-11-24", f) == "완료"
    entry = entries(root)[0]
    assert entry["sourceType"] == "pdf" and entry["category"] == "문서" and entry["cover"] == "" and "images" not in entry
    assert not (root / "covers").exists()
    assert files.process({"batch": "b1"}, root, "2026-11-24", f) == "중복" and len(entries(root)) == 1


@pytest.mark.parametrize("fakes, payload", [
    (Fakes([photo()]), {"batch": "../etc"}),
    (Fakes([], fetch_error=ExtractError("보낸 파일을 찾지 못했습니다")), {"batch": "b1"}),
    (Fakes([photo()], summarize_error=summarize.SummarizeError("거절")), {"batch": "b1"}),
])
def test_failures_notify_and_save_nothing(root, fakes, payload):
    assert files.process(payload, root, "2026-11-24", fakes) == "실패"
    assert entries(root) == [] and fakes.published == [] and fakes.notes[0][0] == "저장 실패"


def test_build_payload_passes_attachments():
    ex, _ = files.prepare([PDF])
    payload = summarize.build_payload(ex, "", ["etc"])
    assert payload["blocks"] == ex.attachments and "첨부한 사진·문서" in payload["text"]
