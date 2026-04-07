---
name: stock-dashboard-update
description: |
  NVDA 기업분석 대시보드의 데이터를 최신화하는 스킬.
  웹에서 최신 주가, 실적, 밸류에이션, 컨퍼런스콜 데이터를 수집하여
  Python 생성 스크립트의 데이터 블록을 교체하고 새 버전 HTML을 자동 생성한다.
  다음 상황에서 반드시 이 스킬을 활성화할 것:
  - "대시보드 업데이트", "대시보드 최신화", "대시보드 갱신" 요청
  - "NVDA 데이터 업데이트", "실적 반영해줘", "최신 실적으로 바꿔줘"
  - "주가 업데이트", "분기 실적 추가", "새 실적 반영"
  - 사용자가 새 분기 실적발표 이후 대시보드 내용 변경을 요청할 때
  - "종목 변경", "다른 종목으로", "AAPL로 바꿔줘" 등 종목 교체 요청
---

# 기업분석 대시보드 업데이트 스킬

## 개요

이 스킬은 StockLens 기업분석 대시보드의 모든 데이터를 최신화한다.
Python 생성 스크립트(`gen_dashboard_vN.py`)의 **데이터 블록만 수정**하고,
템플릿(CSS/HTML/JS 구조)은 그대로 유지하여 새 버전 HTML을 생성한다.

## 파일 위치

- **Python 생성 스크립트**: 프로젝트 폴더 또는 세션 루트에서 `gen_dashboard_v*.py` 중 최신 버전을 찾는다
- **HTML 출력 경로**: `02-projects/2026.03.28 기업분석대시보드/output/` 폴더
- **outputs 공유 경로**: `mnt/outputs/`

## 실행 절차

### 1단계: 현재 상태 파악

가장 먼저 최신 `gen_dashboard_v*.py` 파일을 찾아서 읽는다.
파일 상단의 데이터 블록들이 수정 대상이다:

```
DASHBOARD_META   — 작성기준일, 다음 업데이트 시점
PROFILE          — 종목 기본 정보 (주가, 시가총액, 52주 범위 등)
INCOME           — 연간 손익 데이터 (매출, 순이익, EPS, 마진율 등)
QUARTERLY        — 분기별 매출/순이익
EXTRA            — 가이던스, 주주환원, 애널리스트 컨센서스
SEGMENTS         — 연간 사업부문별 매출
QUARTERLY_SEGMENTS — 분기별 사업부문별 매출
QUARTERLY_DETAIL — 분기별 마진 상세
QUARTERLY_FINANCIAL_ITEMS — 분기별 코멘터리
EARNINGS_QUARTERS — 실적발표 데이터 (EPS Beat/Miss, 컨퍼런스콜)
NEXT_EARNINGS    — 다음 실적발표 예정 정보
PEERS            — 동종업계 비교
RATIOS           — 밸류에이션 배수
```

### 2단계: 최신 데이터 수집 (WebSearch)

다음 검색을 수행하여 최신 데이터를 수집한다:

```
1. "[종목] stock price today market cap 52 week range"
   → PROFILE 업데이트 (주가, 시가총액, 52주 범위, 등락률)

2. "[종목] latest quarterly earnings results revenue EPS"
   → INCOME, QUARTERLY 업데이트 (새 분기 실적 추가)

3. "[종목] earnings conference call highlights key takeaways"
   → EARNINGS_QUARTERS 업데이트 (컨퍼런스콜 요약, CEO 발언)

4. "[종목] earnings EPS estimate actual beat consensus"
   → EARNINGS_QUARTERS 업데이트 (EPS/매출 서프라이즈 데이터)

5. "[종목] next earnings date [year]"
   → NEXT_EARNINGS 업데이트 (다음 실적발표일)

6. "[종목] segment revenue breakdown quarterly"
   → SEGMENTS, QUARTERLY_SEGMENTS 업데이트

7. "[종목] PE ratio forward PE PS ratio PEG ROE"
   → RATIOS 업데이트

8. "[종목] competitors valuation comparison [sector]"
   → PEERS 업데이트
```

**중요**: 공식 IR 뉴스룸(예: nvidianews.nvidia.com)과 SEC 공시를 1차 출처로 우선한다.
추정치는 FactSet, Bloomberg 컨센서스를 참조하되, 반드시 `⚠️ 추정치` 표시를 남긴다.

### 3단계: 데이터 블록 수정

수집한 데이터로 Python 스크립트의 데이터 딕셔너리를 수정한다.

**반드시 지켜야 할 규칙:**

- **기존 버전 파일을 직접 수정하지 않는다** — 새 버전으로 복사 후 수정
- 파일명: `gen_dashboard_v{N+1}.py` (기존 최신 버전 + 1)
- docstring에 변경 내역을 기록한다
- `DASHBOARD_META`를 반드시 업데이트한다:
  ```python
  DASHBOARD_META = {
      "created_date": "YYYY.MM.DD",           # 오늘 날짜
      "data_basis": "FY20XX QN 실적 (YYYY.MM.DD 공시)",
      "data_source": "NVIDIA IR Newsroom, MacroTrends, FactSet Consensus",
      "next_update_event": "QN FY20XX 실적발표",
      "next_update_date": "YYYY.MM.DD (요일) 한국시간",  # 미국 날짜 +1일
      "next_update_ticker": "NVDA",
  }
  ```

**날짜 변환 주의**: 미국 실적발표는 보통 미국 시간 오후 → 한국 시간으로는 다음 날.
예: 미국 5/27(화) → 한국 5/28(수)

### 4단계: 코멘터리 갱신

데이터 수치만 바꾸는 것이 아니라, 다음 텍스트 콘텐츠도 함께 갱신한다:

- `QUARTERLY_FINANCIAL_ITEMS` — 새 분기 하이라이트 + 애널리스트 관점 설명
- `EARNINGS_QUARTERS` — 새 분기의 컨퍼런스콜 요약:
  - `keywords`: 핵심 키워드 3~4개
  - `ceo_quote`: CEO 핵심 발언 1~2문장 (한국어 번역)
  - `highlights`: 주요 하이라이트 4개
  - `analyst_comment`: 투자 관점 분석 코멘트 (3~4문장)
- `NEXT_EARNINGS` — 다음 실적발표 예정일 + Key Watchpoints 갱신
- `OVERVIEW_MONEY/GROWTH/RISKS` — 시장 환경 변화 반영
- `FINANCIAL_ITEMS` — 연간 재무 코멘터리 갱신

코멘터리는 반드시 **한국어**로 작성하며, 투자 초보자도 이해할 수 있는
친근하면서도 전문적인 톤을 유지한다. (~요 체 사용)

### 5단계: HTML 생성 및 배포

```bash
# 출력 디렉토리 확인
mkdir -p "02-projects/2026.03.28 기업분석대시보드/output/"

# 새 버전 실행
python3 gen_dashboard_v{N+1}.py

# outputs 폴더에 복사
cp "02-projects/.../output/기업분석_종합대시보드_v{N+1}_YYYY.MM.DD.html" mnt/outputs/
```

출력 파일명 형식: `기업분석_종합대시보드_v{N+1}_{오늘날짜}.html`

### 6단계: 검증

생성된 HTML에서 다음을 확인한다:
- update-bar에 새 작성기준일이 표시되는지
- 다음 업데이트 안내가 올바른 실적발표일을 가리키는지
- 새 분기 데이터가 차트와 테이블에 반영되었는지
- 실적발표 탭에 새 컨퍼런스콜 카드가 추가되었는지

## 분기별 업데이트 체크리스트

새 분기 실적이 발표되면 다음 항목을 순서대로 업데이트한다:

- [ ] `DASHBOARD_META` — 작성기준일 + 다음 업데이트 시점
- [ ] `PROFILE` — 주가, 시가총액, 52주 범위
- [ ] `INCOME` — 새 회계연도 데이터 추가 (연간)
- [ ] `QUARTERLY` — 새 분기 매출/순이익 추가
- [ ] `QUARTERLY_DETAIL` — 새 분기 마진 상세 추가
- [ ] `QUARTERLY_SEGMENTS` — 새 분기 사업부문별 매출
- [ ] `QUARTERLY_FINANCIAL_ITEMS` — 새 분기 코멘터리
- [ ] `EARNINGS_QUARTERS` — 새 분기 실적발표 데이터 + 컨퍼런스콜
- [ ] `NEXT_EARNINGS` — 다음 실적발표 예정 정보
- [ ] `EXTRA` — 가이던스, 컨센서스 갱신
- [ ] `RATIOS` — 밸류에이션 배수 갱신
- [ ] `PEERS` — 동종업계 비교 데이터 갱신
- [ ] 코멘터리 전체 — 시장 환경, 투자 포인트 반영

## NVIDIA 회계연도 참고

NVIDIA의 회계연도는 2월~1월:
- FY2026 = 2025.02 ~ 2026.01
- FY2027 = 2026.02 ~ 2027.01
- Q1 = 2~4월, Q2 = 5~7월, Q3 = 8~10월, Q4 = 11~1월

실적발표는 보통 분기 종료 후 약 4주 뒤:
- Q1 → 5월 말, Q2 → 8월 말, Q3 → 11월 중순, Q4 → 2월 말

## 종목 변경 시

사용자가 다른 종목으로 변경을 요청하면:
1. 기존 gen_dashboard 스크립트를 복사하여 새 파일 생성
2. 모든 데이터 블록을 새 종목 데이터로 교체
3. 회계연도 체계, 세그먼트 구조 등을 새 종목에 맞게 조정
4. accent 색상을 새 종목 브랜드 컬러로 변경
5. 코멘터리를 새 종목에 맞게 전면 재작성
