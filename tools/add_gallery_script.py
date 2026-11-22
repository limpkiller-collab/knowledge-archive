"""cards/*.html 에 이미지 갤러리 스크립트를 넣는다. 이미 들어 있는 파일은 건드리지 않는다.

지식카드를 새로 만든 뒤 한 번 실행하면 그 카드에서도 이미지를 추가하고 넘겨 볼 수 있다.
    python tools/add_gallery_script.py
"""
from pathlib import Path

TAGS = '<script src="../js/archive-core.js"></script>\n<script src="../js/gallery.js"></script>\n'


def patch(html: str) -> str:
    if "js/gallery.js" in html or "</body>" not in html:
        return html
    head, sep, tail = html.rpartition("</body>")
    return head + TAGS + sep + tail


if __name__ == "__main__":
    changed = 0
    for path in sorted((Path(__file__).resolve().parent.parent / "cards").glob("*.html")):
        old = path.read_text(encoding="utf-8")
        new = patch(old)
        if new != old:
            path.write_text(new, encoding="utf-8")
            changed += 1
    print(f"{changed} files updated")
