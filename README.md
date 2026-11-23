# 지식 Archive

링크를 보내면 핵심을 정리해 카드로 보관하는 개인 지식 아카이브입니다.
직접 정리한 지식카드와, 아이폰 공유 시트로 보낸 링크의 요약 카드를 한곳에서 봅니다.

**사이트: https://limpkiller-collab.github.io/knowledge-archive/**

## 할 수 있는 것

- **링크 저장**: 아이폰 공유 시트에서 링크를 보내면 1~2분 뒤 카드가 만들어지고 알림이 옵니다.
- **지원하는 링크**: 기사·블로그, 인스타그램 게시물과 릴스, 스레드(Threads), 유튜브.
- **자동 정리**: 제목, 한 줄 요약, 핵심 포인트, 분류, 해시태그를 자동으로 붙입니다. 본문에 적힌 링크도 카드에 담습니다.
- **이미지**: 인스타그램·스레드 게시물의 이미지를 전부 저장해 좌우로 넘겨 봅니다. 카드에 내 이미지를 직접 추가할 수도 있습니다.
- **대시보드**: 그리드·카드·리스트 보기, 분류·출처·태그 필터, 검색, 읽음 표시, 다크 모드, 당겨서 새로고침(홈 화면 앱).
- **카드 메뉴**: 편집(제목·분류·해시태그), 시리즈 연결, 공유, 전체 화면 캡처, 삭제.
- **노션 연동**: 저장·수정·삭제가 노션 데이터베이스에도 함께 반영됩니다.

## 동작 방식

서버 없이 GitHub Actions와 GitHub Pages만으로 동작합니다.

```
아이폰 공유 시트(단축어)
        │  repository_dispatch
        ▼
GitHub Actions (scrap-link)
  1. 내용 가져오기   기사: 본문 추출 / 인스타그램: Apify / 스레드: 임베드 페이지 / 유튜브·영상: Gemini
  2. 카드로 정리     Claude API
  3. 저장            cards/*.html, scraps.json, covers/  →  GitHub Pages
  4. 노션에 기록     Notion API
  5. 알림            ntfy
```

| 워크플로 | 하는 일 |
| --- | --- |
| `scrap-link` | 링크 하나를 카드로 저장 |
| `scrap-edit` | 카드의 제목·분류·해시태그 수정, 시리즈 연결 |
| `scrap-delete` | 카드 삭제 (사이트와 노션) |
| `test` | 자동 테스트 |

## 폴더 구조

| 경로 | 내용 |
| --- | --- |
| `index.html` | 대시보드. 직접 정리한 지식카드 목록도 이 파일에 들어 있습니다. |
| `cards/` | 카드 한 장마다 HTML 파일 하나 |
| `covers/` | 썸네일과 갤러리 이미지 |
| `scraps.json` | 링크로 저장한 카드 목록 |
| `card-images.json` | 카드에 직접 추가한 이미지 목록 |
| `categories.json` | 분류 목록과 색 |
| `js/` | 대시보드 로직, 이미지 갤러리, 카드 메뉴 |
| `scrap/` | 링크 처리 파이프라인 (Python) |
| `tests/` | 테스트 |
| `tools/` | 보조 스크립트 |
| `docs/` | 설정 안내와 설계 문서 |

## 설정

처음 설정하는 방법은 [docs/shortcut-setup.md](docs/shortcut-setup.md)에 단계별로 있습니다.

리포의 **Settings → Secrets and variables → Actions**에 아래 값을 등록합니다.

| 이름 | 용도 |
| --- | --- |
| `ANTHROPIC_API_KEY` | 카드 정리 (Claude) |
| `APIFY_TOKEN` | 인스타그램 읽기 |
| `GEMINI_API_KEY` | 유튜브·영상 읽기 |
| `NOTION_TOKEN`, `NOTION_DATABASE_ID` | 노션 기록 |
| `NTFY_TOPIC` | 완료 알림 |

사이트에서 편집·삭제·이미지 추가를 하려면 이 리포의 Contents 권한(Read and write)이 있는 GitHub 토큰이 필요합니다. 토큰은 처음 한 번 묻고, 그 기기의 브라우저에만 저장됩니다.

## 개발

```bash
python -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
```

```bash
.venv/bin/python -m pytest
```

```bash
node --test tests/*.test.js
```

```bash
node tools/serve.js 8765
```

마지막 명령은 로컬 미리보기 서버입니다. http://localhost:8765 에서 엽니다.

지식카드를 직접 만들어 `cards/`에 추가했다면 아래를 한 번 실행합니다. 그 카드에서도 이미지를 추가하고 넘겨 볼 수 있게 됩니다.

```bash
python tools/add_gallery_script.py
```

## 알아 둘 점

- 이 리포와 사이트는 공개입니다. 카드 내용과 이미지는 주소를 아는 누구나 볼 수 있습니다.
- 링크를 보낼 때 적은 메모와 추출한 원문 전체는 노션에만 저장하고, 공개 사이트에는 남기지 않습니다.
- 열람이 제한된 인스타그램 게시물, 스레드에서 글쓴이가 이어 쓴 답글은 읽지 못합니다.

설계 배경과 변경 내역은 [docs/superpowers/specs/2026-11-22-link-scrap-cards-design.md](docs/superpowers/specs/2026-11-22-link-scrap-cards-design.md)에 있습니다.
