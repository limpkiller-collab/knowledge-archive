"""홈 화면 아이콘을 만든다: 검은 바탕에 카드 네 장, 왼쪽 위만 붉은색."""
import struct
import zlib
from pathlib import Path

BG, RED, WHITE = (0x11, 0x11, 0x11), (0xE5, 0x48, 0x3D), (0xFF, 0xFF, 0xFF)


def pixels(size: int):
    pad, gap = round(size * 28 / 180), round(size * 12 / 180)
    cell = (size - 2 * pad - gap) // 2
    starts = (pad, pad + cell + gap)

    def color(x, y):
        for row, y0 in enumerate(starts):
            for col, x0 in enumerate(starts):
                if x0 <= x < x0 + cell and y0 <= y < y0 + cell:
                    return RED if (row, col) == (0, 0) else WHITE
        return BG

    return [[color(x, y) for x in range(size)] for y in range(size)]


def write_png(path: Path, size: int) -> None:
    raw = b"".join(b"\x00" + bytes(c for px in row for c in px) for row in pixels(size))

    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))

    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))
    path.parent.mkdir(exist_ok=True)
    path.write_bytes(png)


if __name__ == "__main__":
    write_png(Path("icons/apple-touch-icon.png"), 180)
    write_png(Path("icons/icon-512.png"), 512)
