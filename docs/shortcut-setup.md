# 링크 스크랩 설정 안내

링크를 보내 카드로 저장하려면 아래 설정을 한 번 해야 한다. 키와 토큰은 본인만 볼 수 있는 곳(GitHub Secrets, 단축어)에만 넣는다.

## 1. API 키 발급

| 서비스 | 용도 | 발급 위치 |
|---|---|---|
| Anthropic | 카드 요약 | Claude Console의 API Keys |
| Apify | 인스타그램 게시물·릴스 읽기 | Apify Console의 Settings › API & Integrations |
| Google AI Studio | 유튜브 영상 읽기, 릴스 음성 받아쓰기 (Gemini) | Google AI Studio의 Get API key |

## 2. 노션 연결

"링크 스크랩" DB는 개인 워크스페이스에 만들어 두었다(2026-11-22).

- DB 주소: https://app.notion.com/p/4209cb66facf8184aa63d7a80fbbeb90
- `NOTION_DATABASE_ID` 값: `4209cb66facf8184aa63d7a80fbbeb90`

남은 일:

1. 노션에서 내부 통합(integration)을 새로 만들고 토큰을 복사한다. 이 값이 `NOTION_TOKEN`이다.
2. "링크 스크랩" DB 페이지의 `···` › 연결에서 방금 만든 통합을 추가한다.
3. "카드" 갤러리 뷰의 레이아웃 설정에서 카드 미리보기를 "페이지 커버"로 바꾼다. 썸네일이 카드 위에 보인다.

DB 속성 이름은 코드와 정확히 같아야 하므로 바꾸지 않는다: 제목, URL, 출처 유형, 카테고리, 태그, 한 줄 요약, 저장일, 상태, 메모, HTML 카드.

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
- `GEMINI_API_KEY`
- `NTFY_TOPIC`

Variables (모두 선택 사항, 비우면 기본값):

| 이름 | 기본값 | 설명 |
|---|---|---|
| `CLAUDE_MODEL` | `claude-opus-5-5` | 요약에 쓰는 Claude 모델 |
| `GEMINI_MODEL` | `gemini-3.8-flash` | 유튜브를 읽고 릴스 음성을 받아쓰는 Gemini 모델 |
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

## 8. 사진·PDF 보내기

사진이나 PDF 파일을 보내도 카드로 정리된다. 파일은 링크와 달리 크기가 커서, 단축어가 **비공개 저장소**(받은 파일함)에 먼저 올리고 나서 정리를 요청한다. 원본 파일은 이 비공개 저장소에만 남는다.

### 8-1. 받은 파일함 저장소 만들기

1. GitHub에서 새 저장소를 만든다. 이름은 `knowledge-archive-inbox`, 공개 범위는 반드시 **Private**.
2. "Add a README file"을 켜서 만든다(빈 저장소로 두지 않는다).

### 8-2. 토큰 권한

1. 5번에서 만든 단축어용 토큰의 Repository access에 `knowledge-archive-inbox`를 추가한다. Contents 권한(Read and write)이 두 저장소에 함께 적용된다. 토큰을 새로 만들었다면 단축어의 토큰도 바꾼다.
2. `knowledge-archive` 리포의 Settings › Secrets and variables › Actions에 Secret `INBOX_TOKEN`을 추가한다. 값은 받은 파일함을 읽을 수 있는 토큰이다. 위의 단축어용 토큰을 그대로 넣어도 되고, `knowledge-archive-inbox`의 Contents 읽기 권한만 가진 토큰을 따로 만들어 넣어도 된다.

저장소 이름을 다르게 지었다면 Variables에 `INBOX_REPO`를 `계정/저장소이름`으로 등록한다.

### 8-3. 단축어 만들기

새 단축어를 만들고 "공유 시트에 표시"를 켠 뒤, 받는 입력을 **이미지, PDF, 파일**로 제한한다. 동작은 순서대로:

1. **현재 날짜** → **날짜 포맷**: 사용자화, 포맷 문자열 `yyyyMMdd-HHmmss`. 결과를 변수 `묶음`에 넣는다.
2. (선택) 6번 단축어의 1~5번과 같은 방식으로 카테고리와 메모를 받는다. 생략하면 자동 분류된다.
3. **각 항목 반복**: 단축어 입력
   1. **Base64 인코딩**: 반복 항목, 줄 바꿈은 **없음**
   2. **URL 내용 가져오기**
      - URL: `https://api.github.com/repos/limpkiller-collab/knowledge-archive-inbox/contents/inbox/` 뒤에 `묶음` 변수, `/`, **반복 인덱스**를 붙인다. 예: `…/contents/inbox/20261124-101500/1`
      - 방식: **PUT**
      - 헤더: `Authorization: Bearer <토큰>`, `Accept: application/vnd.github+json`
      - 본문(JSON): `message`는 `add`, `content`는 Base64 인코딩 결과
4. **반복 끝** 다음에 **URL 내용 가져오기**
   - URL: `https://api.github.com/repos/limpkiller-collab/knowledge-archive/dispatches`
   - 방식: POST, 헤더는 위와 같다
   - 본문(JSON): `event_type`은 `scrap-file`, `client_payload`는 사전으로 `batch`(`묶음` 변수), `category`, `note`
5. **알림 표시**: "보냈습니다. 1~3분 뒤 알림이 옵니다"

파일 이름과 확장자는 신경 쓰지 않아도 된다. 내용으로 사진인지 PDF인지 구분한다.

### 8-4. 동작

- 한 번에 보낸 파일은 카드 한 장이 된다. 사진은 10장, 파일은 12개까지, PDF는 합쳐서 20MB까지.
- 사진은 크기를 줄여 카드의 커버와 갤러리에 싣는다. 사이트가 공개이므로 사진도 공개된다.
- PDF 원본은 사이트에 올리지 않는다. 요약만 카드가 된다.
- 아이폰 사진(HEIC)도 그대로 보내면 된다.
- 카드의 "원문 보기"는 받은 파일함의 해당 폴더로 연결된다. 비공개 저장소라 본인만 열 수 있다.

## 알려진 한계

- 사진·PDF로 만든 카드는 본문에 적힌 링크를 따로 모으지 않는다.
- 받은 파일함의 원본은 자동으로 지우지 않는다. 필요하면 저장소에서 직접 지운다.

- 비공개 인스타그램 계정, 비공개·일부 공개 유튜브 영상은 읽지 못한다.
- 인스타그램 추출은 외부 서비스에 의존하므로 인스타그램 쪽 변경으로 예고 없이 실패할 수 있다.
- 공개 사이트에는 제목, 요약, 핵심 포인트, 원문 링크, 커버만 올라간다. 메모와 추출 원문은 노션에만 저장된다.
