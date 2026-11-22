import json
from scrap import html_store
from scrap.models import Card


def make_card(**kw):
    base = dict(id="scrap-20261122-coat", title="코트 <b>정리</b>", summary="요약 & 정리", key_points=["첫째", "둘째"],
                category="패션", tags=["코트"], cover_word="코트", source_type="instagram_post",
                source="인스타그램", source_url="https://www.instagram.com/p/ABC/", date="2026-11-22")
    base.update(kw)
    return Card(**base)


def setup_repo(tmp_path):
    (tmp_path / "cards").mkdir()
    (tmp_path / "scraps.json").write_text("[]", encoding="utf-8")
    (tmp_path / "categories.json").write_text(json.dumps([{"name": "패션", "color": "#6b2f55"}], ensure_ascii=False), encoding="utf-8")
    return tmp_path


def test_save_writes_card_and_index(tmp_path):
    root = setup_repo(tmp_path)
    html_store.save(make_card(), root)
    html = (root / "cards/scrap-20261122-coat.html").read_text(encoding="utf-8")
    assert "코트 &lt;b&gt;정리&lt;/b&gt;" in html and "<b>정리</b>" not in html
    assert "<li>첫째</li>" in html and "https://www.instagram.com/p/ABC/" in html
    entry = json.loads((root / "scraps.json").read_text(encoding="utf-8"))[0]
    assert entry["file"] == "cards/scrap-20261122-coat.html"
    assert entry["title"] == "코트 &lt;b&gt;정리&lt;/b&gt;"
    assert entry["sourceType"] == "instagram_post" and entry["coverWord"] == "코트"


def test_save_replaces_same_url(tmp_path):
    root = setup_repo(tmp_path)
    html_store.save(make_card(), root)
    html_store.save(make_card(title="새 제목"), root)
    entries = json.loads((root / "scraps.json").read_text(encoding="utf-8"))
    assert len(entries) == 1 and entries[0]["title"] == "새 제목"


def test_find_by_url(tmp_path):
    root = setup_repo(tmp_path)
    assert html_store.find_by_url("https://www.instagram.com/p/ABC/", root) is None
    html_store.save(make_card(), root)
    assert html_store.find_by_url("https://www.instagram.com/p/ABC/", root)["id"] == "scrap-20261122-coat"


def test_ensure_category_appends_new(tmp_path):
    root = setup_repo(tmp_path)
    assert html_store.ensure_category("여행", root) is True
    assert html_store.ensure_category("패션", root) is False
    names = [c["name"] for c in json.loads((root / "categories.json").read_text(encoding="utf-8"))]
    assert names == ["패션", "여행"]
