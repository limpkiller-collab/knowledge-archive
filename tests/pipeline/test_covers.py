import io
from PIL import Image
from scrap import covers


def png_bytes(w, h):
    buf = io.BytesIO()
    Image.new("RGBA", (w, h), (200, 30, 30, 255)).save(buf, "PNG")
    return buf.getvalue()


def test_saves_resized_jpeg(tmp_path):
    path = covers.save("scrap-1", "https://cdn/x.png", tmp_path, fetch=lambda u: png_bytes(2400, 1200))
    assert path == "covers/scrap-1.jpg"
    with Image.open(tmp_path / path) as img:
        assert img.format == "JPEG" and img.size == (1200, 600)


def test_returns_empty_on_failure(tmp_path):
    def boom(u):
        raise OSError("blocked")
    assert covers.save("scrap-1", "https://cdn/x.png", tmp_path, fetch=boom) == ""


def test_returns_empty_when_disabled(tmp_path, monkeypatch):
    monkeypatch.setenv("SCRAP_STORE_COVERS", "0")
    assert covers.save("scrap-1", "https://cdn/x.png", tmp_path, fetch=lambda u: png_bytes(10, 10)) == ""


def test_save_all_numbers_files_and_skips_failures(tmp_path):
    def fetch(u):
        if u.endswith("bad"):
            raise OSError("blocked")
        return png_bytes(2400, 3000)
    keep = tmp_path / "covers/scrap-1/u-1.jpg"
    keep.parent.mkdir(parents=True)
    keep.write_bytes(b"x")
    (tmp_path / "covers/scrap-1/09.jpg").write_bytes(b"old")
    paths = covers.save_all("scrap-1", ["https://c/a", "https://c/bad", "https://c/b"], tmp_path, fetch=fetch)
    assert paths == ["covers/scrap-1/01.jpg", "covers/scrap-1/02.jpg"]
    with Image.open(tmp_path / paths[1]) as img:
        assert img.size == (1200, 1500)
    assert keep.exists() and not (tmp_path / "covers/scrap-1/09.jpg").exists()


def test_save_all_caps_count_and_can_be_disabled(tmp_path, monkeypatch):
    urls = [f"https://c/{i}" for i in range(30)]
    assert len(covers.save_all("scrap-2", urls, tmp_path, fetch=lambda u: png_bytes(10, 10))) == covers.MAX_GALLERY
    monkeypatch.setenv("SCRAP_STORE_COVERS", "0")
    assert covers.save_all("scrap-3", urls, tmp_path, fetch=lambda u: png_bytes(10, 10)) == []
