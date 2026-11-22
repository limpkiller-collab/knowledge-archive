"""cards/*.html 에 이미지 갤러리와 카드 메뉴 스크립트를 넣는다. 이미 들어 있는 파일은 건드리지 않는다.

지식카드를 새로 만든 뒤 한 번 실행하면 그 카드에서도 이미지를 추가하고 넘겨 볼 수 있다.
카드 메뉴(편집·공유·캡처·삭제)는 링크로 저장한 카드(scrap-*)에만 넣는다.
    python tools/add_gallery_script.py
"""
from pathlib import Path

GALLERY = '<script src="../js/archive-core.js"></script>\n<script src="../js/gallery.js"></script>\n'
MENU = '<script src="../js/card-menu.js"></script>\n'


def patch(html: str, with_menu: bool = False) -> str:
    if "</body>" not in html:
        return html
    add = ("" if "js/gallery.js" in html else GALLERY) + ("" if not with_menu or "js/card-menu.js" in html else MENU)
    if not add:
        return html
    head, sep, tail = html.rpartition("</body>")
    return head + add + sep + tail


if __name__ == "__main__":
    changed = 0
    for path in sorted((Path(__file__).resolve().parent.parent / "cards").glob("*.html")):
        old = path.read_text(encoding="utf-8")
        new = patch(old, with_menu=path.name.startswith("scrap-"))
        if new != old:
            path.write_text(new, encoding="utf-8")
            changed += 1
    print(f"{changed} files updated")
