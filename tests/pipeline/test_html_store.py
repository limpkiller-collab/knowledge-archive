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
    assert (root / "shortcut-menu.txt").read_text(encoding="utf-8").split("\n") == ["자동 분류", "패션", "여행", "새 카테고리 입력"]


def test_save_records_gallery_images(tmp_path):
    root = setup_repo(tmp_path)
    html_store.save(make_card(images=["covers/scrap-20261122-coat/01.jpg", "covers/scrap-20261122-coat/02.jpg"]), root)
    entry = json.loads((root / "scraps.json").read_text(encoding="utf-8"))[0]
    assert entry["images"] == ["covers/scrap-20261122-coat/01.jpg", "covers/scrap-20261122-coat/02.jpg"]
    html = (root / "cards/scrap-20261122-coat.html").read_text(encoding="utf-8")
    assert 'id="ka-gallery"' in html and "../js/gallery.js" in html
    html_store.save(make_card(), root)
    assert "images" not in json.loads((root / "scraps.json").read_text(encoding="utf-8"))[0]


def test_remove_clears_gallery_folder_and_added_images(tmp_path):
    root = setup_repo(tmp_path)
    html_store.save(make_card(), root)
    folder = root / "covers/scrap-20261122-coat"
    folder.mkdir(parents=True)
    (folder / "01.jpg").write_bytes(b"x")
    (root / "card-images.json").write_text(json.dumps({"scrap-20261122-coat": ["covers/scrap-20261122-coat/u-1.jpg"], "other": ["a.jpg"]}), encoding="utf-8")
    assert html_store.remove("scrap-20261122-coat", root)["id"] == "scrap-20261122-coat"
    assert not folder.exists()
    assert json.loads((root / "card-images.json").read_text(encoding="utf-8")) == {"other": ["a.jpg"]}
