# 링크 스크랩 설정 안내

링크를 보내 카드로 저장하려면 아래 설정을 한 번 해야 한다. 키와 토큰은 본인만 볼 수 있는 곳(GitHub Secrets, 단축어)에만 넣는다.

## 1. API 키 발급

| 서비스 | 용도 | 발급 위치 |
|---|---|---|
| Anthropic | 카드 요약 | Claude Console의 API Keys |
| Apify | 인스타그램 게시물·릴스 읽기 | Apify Console의 Settings › API & Integrations |
| OpenAI | 릴스 음성 받아쓰기 | OpenAI Platform의 API keys |
| Google AI Studio | 유튜브 영상 읽기 (Gemini) | Google AI Studio의 Get API key |

## 2. 노션 연결

1. 노션에서 내부 통합(integration)을 새로 만들고 토큰을 복사한다.
2. "링크 스크랩" DB 페이지의 `···` › 연결에서 방금 만든 통합을 추가한다.
3. DB 주소에서 DB ID(32자리)를 복사한다. `notion.so/<DB ID>?v=...` 형태다.

DB 속성 이름은 코드와 정확히 같아야 한다: 제목, URL, 출처 유형, 카테고리, 태그, 한 줄 요약, 저장일, 상태, 메모, HTML 카드.

## 3. 알림 (ntfy)

1. 아이폰에 ntfy 앱을 설치한다.
2. 추측하기 어려운 긴 임의 문자열로 토픽을 정해 구독한다. 예: `scrap-` 뒤에 무작위 영문·숫자 24자.

토픽 이름을 아는 사람은 누구나 알림을 볼 수 있으므로 공개하지 않는다.

## 4. GitHub에 값 등록

리포 Settings › Secrets and variables › Actions.

Secrets:

- `ANTHROPIC_API_KEY`
- `NOTION_TOKEN`
- `NOTION_DATABASE_ID`
- `APIFY_TOKEN`
- `OPENAI_API_KEY`
- `GEMINI_API_KEY`
- `NTFY_TOPIC`

Variables (모두 선택 사항, 비우면 기본값):

| 이름 | 기본값 | 설명 |
|---|---|---|
| `CLAUDE_MODEL` | `claude-opus-5-5` | 요약에 쓰는 Claude 모델 |
| `GEMINI_MODEL` | `gemini-3.8-flash` | 유튜브를 읽는 Gemini 모델 |
| `SCRAP_STORE_COVERS` | 저장함 | `0`이면 썸네일을 저장하지 않고 글자형 커버만 쓴다 |

## 5. 단축어용 GitHub 토큰

1. GitHub Settings › Developer settings › Fine-grained tokens에서 새 토큰을 만든다.
2. Repository access는 `knowledge-archive` 하나만 고른다.
3. Repository permissions에서 Contents를 Read and write로 둔다. 다른 권한은 주지 않는다.
4. 만료일을 정한다. 만료되면 단축어의 토큰만 바꾸면 된다.

## 6. 단축어 만들기

단축어 앱에서 새 단축어를 만들고 "공유 시트에 표시"를 켠 뒤, 받는 입력을 URL로 제한한다. 동작은 순서대로:

1. **URL 내용 가져오기**: `https://limpkiller-collab.github.io/knowledge-archive/categories.json` (공개 주소라 토큰이 필요 없다)
2. **사전 값 가져오기**로 각 항목의 `name`을 뽑아 목록을 만든다. 앞에 "자동 분류", 뒤에 "새 카테고리 입력"을 붙인다.
3. **목록에서 선택**: "카테고리"
4. **만약**: 선택이 "새 카테고리 입력"이면 **입력 요청**으로 이름을 받고, "자동 분류"면 빈 텍스트로 둔다.
5. **입력 요청**: "메모 (비워도 됨)"
6. **URL 내용 가져오기**
   - URL: `https://api.github.com/repos/limpkiller-collab/knowledge-archive/dispatches`
   - 방식: POST
   - 헤더: `Authorization: Bearer <5번의 토큰>`, `Accept: application/vnd.github+json`
   - 본문(JSON): `event_type`은 `scrap-link`, `client_payload`는 사전으로 `url`(공유받은 URL), `category`, `note`
7. **알림 표시**: "보냈습니다. 1~3분 뒤 알림이 옵니다"

1번에서 목록을 읽지 못하면 2~4번을 건너뛰고 카테고리를 빈 값으로 보내도록 "만약" 분기를 둔다.

토큰은 단축어 안에 그대로 들어가므로 이 단축어를 다른 사람과 공유하지 않는다.

## 7. 동작 확인

워크플로는 `main` 브랜치에 있어야 실행된다. 병합한 뒤 기사, 인스타그램 게시물, 릴스, 유튜브 링크를 하나씩 보내 본다.

- 1~3분 뒤 "저장 완료" 알림이 온다.
- 사이트와 노션 DB에 카드가 생긴다.
- 같은 링크를 다시 보내면 "이미 저장됨" 알림이 온다.

문제가 있으면 리포의 Actions 탭에서 `scrap-link` 실행 기록을 본다.

## 알려진 한계

- 비공개 인스타그램 계정, 비공개·일부 공개 유튜브 영상은 읽지 못한다.
- 인스타그램 추출은 외부 서비스에 의존하므로 인스타그램 쪽 변경으로 예고 없이 실패할 수 있다.
- 공개 사이트에는 제목, 요약, 핵심 포인트, 원문 링크, 커버만 올라간다. 메모와 추출 원문은 노션에만 저장된다.
