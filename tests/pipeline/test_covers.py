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
