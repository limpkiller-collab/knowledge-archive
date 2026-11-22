"""index.html의 KNOWLEDGE_DB category 값을 통합 카테고리로 바꾼다. 여러 번 실행해도 결과가 같다."""
import re
import sys
from collections import Counter
from pathlib import Path

MAPPING = {"투자·주식": "경제·투자", "경제·거시": "경제·투자", "투자·금융": "경제·투자"}
EXPECTED = {"경제·투자": 59, "기술·산업": 26, "부동산": 6, "시사·컬처": 15}
PATTERN = re.compile(r'(category:\s*")([^"]+)(")')


def migrate(text: str) -> str:
    return PATTERN.sub(lambda m: m.group(1) + MAPPING.get(m.group(2), m.group(2)) + m.group(3), text)


if __name__ == "__main__":
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
    out = migrate(path.read_text(encoding="utf-8"))
    counts = Counter(m.group(2) for m in PATTERN.finditer(out))
    print(dict(counts))
    if dict(counts) != EXPECTED:
        sys.exit("카테고리 개수가 예상과 다릅니다. index.html에 카드가 추가됐는지 확인하고 EXPECTED를 고치세요.")
    path.write_text(out, encoding="utf-8")
