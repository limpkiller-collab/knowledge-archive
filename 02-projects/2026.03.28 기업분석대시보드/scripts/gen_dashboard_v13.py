#!/usr/bin/env python3
"""v13: 작성기준일 + 업데이트 안내 바 추가
- 헤더 하단에 작성기준일, 데이터 출처, 다음 업데이트 시점 안내 바
- DASHBOARD_META 데이터 구조 분리 (스킬에서 업데이트 용이)
- v12 실적발표 탭 + v11 Supanova Design System 유지
"""
import math

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD META — 작성기준일 & 업데이트 안내 (스킬에서 이 블록만 수정)
# ══════════════════════════════════════════════════════════════════════════════

DASHBOARD_META = {
    "created_date": "2026.03.28",           # 작성(최종 업데이트)일
    "data_basis": "FY2026 Q4 실적 (2026.02.25 공시)",  # 데이터 기준
    "data_source": "NVIDIA IR Newsroom, MacroTrends, FactSet Consensus",
    "next_update_event": "Q1 FY2027 실적발표",
    "next_update_date": "2026.05.28 (수) 한국시간",  # 미국 5/27 → 한국 5/28
    "next_update_ticker": "NVDA",
}

# ══════════════════════════════════════════════════════════════════════════════
# NVDA COMPREHENSIVE DATA
# ══════════════════════════════════════════════════════════════════════════════

PROFILE = {
    "symbol":"NVDA","name":"NVIDIA Corporation","price":167.52,
    "changes":-2.31,"changesPct":-1.36,"exchange":"NASDAQ",
    "sector":"Technology","industry":"Semiconductors","country":"US",
    "mktCap":"$4.07T","beta":2.37,"range":"86.62 - 212.19",
    "employees":"36,000",
    "desc":"NVIDIA는 GPU(그래픽 처리 장치) 및 AI 컴퓨팅 플랫폼의 글로벌 리더입니다. 데이터센터, 게이밍, 자동차, 전문 시각화 등 다양한 시장에서 AI 가속 컴퓨팅 솔루션을 제공합니다.",
    "accent":"#76b900"
}

# ✅ = NVIDIA IR 공시 확인 완료 | ⚠️ = 추정치 (과거 FY는 10-K/10-Q 기반이나 일부 추정 포함)
INCOME = [
    {"year":"2022","rev":26.91,"ni":9.75,"oi":10.04,"gp":17.48,"eps":0.39,"gm":64.93,"om":37.31,"nm":36.23,"rnd":7.34,"capex":0.98,"ocf":9.11,"fcf":8.13,"src":"10-K"},  # ⚠️ 과거 데이터
    {"year":"2023","rev":26.97,"ni":4.37,"oi":4.22,"gp":15.36,"eps":0.17,"gm":56.93,"om":15.66,"nm":16.19,"rnd":7.34,"capex":1.83,"ocf":5.64,"fcf":3.81,"src":"10-K"},  # ⚠️ 과거 데이터
    {"year":"2024","rev":60.92,"ni":29.76,"oi":32.97,"gp":44.30,"eps":1.19,"gm":72.72,"om":54.12,"nm":48.85,"rnd":8.68,"capex":1.07,"ocf":28.09,"fcf":27.02,"src":"10-K"},  # ⚠️ 과거 데이터
    {"year":"2025","rev":130.50,"ni":72.88,"oi":81.45,"gp":97.86,"eps":2.94,"gm":74.99,"om":62.42,"nm":55.85,"rnd":12.91,"capex":3.23,"ocf":64.09,"fcf":60.86,"src":"10-K"},  # ✅ IR 공시
    {"year":"2026","rev":215.94,"ni":120.07,"oi":130.39,"gp":153.46,"eps":4.90,"gm":71.07,"om":60.38,"nm":55.60,"rnd":18.50,"capex":6.04,"ocf":102.72,"fcf":96.58,"src":"IR"},  # ✅ IR 공시 (2026.02.25)
]

# ✅ 분기별 데이터 — NVIDIA IR Earnings Release 기반 교차 검증 완료
QUARTERLY = [
    {"q":"Q1'25","rev":26.04,"ni":14.88},{"q":"Q2'25","rev":30.04,"ni":16.60},
    {"q":"Q3'25","rev":35.08,"ni":19.31},{"q":"Q4'25","rev":39.33,"ni":22.09},
    {"q":"Q1'26","rev":44.06,"ni":18.78,"gm":60.5,"note":"H20 재고충당 $4.5B 반영"},  # ✅ IR 공시
    {"q":"Q2'26","rev":46.70,"ni":26.42,"gm":72.4},  # ✅ IR 공시
    {"q":"Q3'26","rev":57.00,"ni":31.90,"gm":73.4},  # ✅ IR 공시
    {"q":"Q4'26","rev":68.13,"ni":42.96,"gm":75.0},  # ✅ IR 공시
]

# ✅ 추가 공시 데이터
EXTRA = {
    "share_repurchase": 40.09,  # $40.1B 자사주 매입 (FY2026) ✅
    "dividends_paid": 0.97,     # $974M 배당금 ✅
    "q1_fy27_guidance": 78.0,   # Q1 FY2027 가이던스 $78B ±2% ✅
    "q1_fy27_gm_guide": 74.9,   # Q1 FY2027 Gross Margin 가이던스 ✅
    "sga": 4.58,                 # SG&A $4.58B ✅
    "analyst_consensus": "Buy",  # 70명 중 93% 매수 의견
    "avg_target_price": 267,     # 평균 목표가 $267
}

# ✅ FY2025, FY2026 세그먼트: IR 공시 확인 | ⚠️ FY2022~2024: 과거 10-K 기반 추정
SEGMENTS = {
    "labels":["FY2022","FY2023","FY2024","FY2025","FY2026"],
    "series":[
      {"name":"Data Center","color":"#76b900","data":[10.6,15.0,47.5,115.2,193.7]},  # ✅ FY2026 IR확인
      {"name":"Gaming","color":"#4ecdc4","data":[12.5,9.1,10.4,11.4,16.0]},          # ✅ FY2026 IR확인
      {"name":"Pro Visualization","color":"#4dabf7","data":[2.1,1.5,1.6,1.9,3.2]},   # ✅ FY2026 IR확인
      {"name":"Automotive","color":"#b197fc","data":[0.6,0.9,1.1,1.7,2.3]},           # ✅ FY2026: $2.3B (수정)
    ]
}

# ✅ 분기별 세그먼트 데이터 — NVIDIA IR Earnings Release 기반 교차 검증 완료
QUARTERLY_SEGMENTS = {
    "labels": ["Q1'26","Q2'26","Q3'26","Q4'26"],
    "series": [
        {"name":"Data Center","color":"#76b900","data":[39.1,41.1,51.2,62.3]},     # ✅ IR 공시
        {"name":"Gaming","color":"#4ecdc4","data":[3.8,4.3,4.3,3.7]},              # ✅ IR 공시
        {"name":"Pro Visualization","color":"#4dabf7","data":[0.509,0.601,0.760,1.3]}, # ✅ IR 공시
        {"name":"Automotive","color":"#b197fc","data":[0.567,0.586,0.592,0.604]},   # ✅ IR 공시
    ]
}

# ✅ 분기별 마진 데이터
QUARTERLY_DETAIL = [
    {"q":"Q1'26","rev":44.06,"ni":18.78,"gm":60.5,"om":37.0,"nm":42.6,"note":"H20 재고충당 $4.5B 반영"},
    {"q":"Q2'26","rev":46.70,"ni":26.42,"gm":72.4,"om":58.2,"nm":56.6,"note":"Blackwell 출하 시작"},
    {"q":"Q3'26","rev":57.00,"ni":31.90,"gm":73.4,"om":63.1,"nm":55.9,"note":"Blackwell 본격 양산"},
    {"q":"Q4'26","rev":68.13,"ni":42.96,"gm":75.0,"om":66.5,"nm":63.1,"note":"역대 최고 분기 실적"},
]

# 분기별 재무 코멘터리
QUARTERLY_FINANCIAL_ITEMS = [
    {
        "category": "분기별 하이라이트",
        "items": [
            {
                "label": "Q1 FY2026 (2025.02~04)",
                "emoji": "⚠️",
                "headline": "H20 재고충당 $4.5B로 마진 급락 — 그러나 매출은 견조",
                "value": "$44.1B",
                "yoy": "+69.1% YoY",
                "yoy_dir": "up",
                "verified": True,
                "desc": "미중 수출 규제 강화로 중국향 H20 칩 재고충당금 $4.5B을 반영하면서 매출총이익률이 60.5%로 급락했어요. 하지만 매출 자체는 $44.1B로 전년 동기($26.0B) 대비 69% 성장하며 견조했습니다. 데이터센터 $39.1B(+73% YoY), 게이밍 $3.8B(+42% YoY)이 성장을 이끌었어요."
            },
            {
                "label": "Q2 FY2026 (2025.05~07)",
                "emoji": "🔄",
                "headline": "Blackwell 출하 시작 — 마진 빠르게 회복",
                "value": "$46.7B",
                "yoy": "+55.5% YoY",
                "yoy_dir": "up",
                "verified": True,
                "desc": "Blackwell 아키텍처 출하가 본격 시작되면서 매출총이익률이 72.4%로 빠르게 회복했어요. 데이터센터 $41.1B(+56% YoY)으로 전분기 대비 5% 성장했고, 게이밍은 $4.3B(+49% YoY)으로 분기 신고가를 기록했습니다. Pro Viz도 $601M으로 전분기 대비 18% 성장하며 반등 중이에요."
            },
            {
                "label": "Q3 FY2026 (2025.08~10)",
                "emoji": "🚀",
                "headline": "Blackwell 양산 가속 — 데이터센터 $51.2B 돌파",
                "value": "$57.0B",
                "yoy": "+62.5% YoY",
                "yoy_dir": "up",
                "verified": True,
                "desc": "Blackwell 양산이 본격화되면서 데이터센터 매출이 $51.2B(+66% YoY)로 단일 분기 $50B을 처음 넘겼어요. 매출총이익률도 73.4%로 추가 개선됐습니다. Pro Viz는 $760M(+56% YoY), Automotive는 $592M(+32% YoY)으로 전 사업부문이 YoY 성장을 기록했어요."
            },
            {
                "label": "Q4 FY2026 (2025.11~2026.01)",
                "emoji": "🏆",
                "headline": "역대 최고 분기 — $68.1B 매출, 순이익률 63%",
                "value": "$68.1B",
                "yoy": "+73.5% YoY",
                "yoy_dir": "up",
                "verified": True,
                "desc": "분기 매출 $68.1B로 역대 최고를 갈아치웠어요. 데이터센터 $62.3B(+75% YoY)이 전체의 91%를 차지했고, 매출총이익률은 75.0%로 FY2026 최고치를 기록했습니다. Pro Viz는 처음으로 분기 $1B을 돌파한 $1.3B(+159% YoY)이 인상적이에요. Q1 FY2027 가이던스 $78B은 시장 기대를 상회했습니다."
            },
        ]
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# EARNINGS DATA — 실적발표 탭 데이터
# ══════════════════════════════════════════════════════════════════════════════

EARNINGS_QUARTERS = [
    {
        "q": "Q1 FY2026", "period": "2025.02~04", "date": "2025.05.28",
        "rev_actual": 44.06, "rev_est": 43.28, "rev_beat": True, "rev_surprise": "+1.8%",
        "eps_actual": 0.81, "eps_est": 0.74, "eps_beat": True, "eps_surprise": "+9.5%",
        "eps_gaap": 0.76,
        "stock_reaction": "-0.8%", "reaction_note": "H20 재고충당 우려로 소폭 하락",
        "keywords": ["H20 수출규제", "Blackwell 양산", "Sovereign AI"],
        "ceo_quote": "블랙웰 NVL72는 추론을 위한 '생각하는 기계'입니다. AI 추론 토큰 생성량이 1년 만에 10배 급증했고, AI 에이전트가 주류가 되면서 AI 컴퓨팅 수요는 더욱 가속될 것입니다.",
        "highlights": [
            "미중 수출 규제 강화로 H20 재고충당금 $4.5B 반영 → GPM 60.5%로 급락",
            "데이터센터 $39.1B (+73% YoY) — Blackwell NVL72 풀스케일 양산 돌입",
            "추가 $2.5B 규모 H20 매출이 수출 제한으로 인식 불가",
            "미국 내 공급망 구축 계획 발표 — 온쇼어링 전략 본격화",
        ],
        "analyst_comment": "H20 관련 일회성 비용($4.5B)이 마진을 왜곡했지만, 이를 제외한 실질 매출 성장률은 예상을 상회했습니다. Blackwell 양산이 확인된 점이 핵심 포인트이며, 중국 리스크는 이미 가이던스에서 제외되어 향후 추가 충격은 제한적입니다. 수출 규제의 실질 영향보다 Blackwell 수요의 폭발력에 주목해야 할 분기입니다."
    },
    {
        "q": "Q2 FY2026", "period": "2025.05~07", "date": "2025.08.27",
        "rev_actual": 46.70, "rev_est": 46.20, "rev_beat": True, "rev_surprise": "+1.1%",
        "eps_actual": 1.05, "eps_est": 1.01, "eps_beat": True, "eps_surprise": "+4.0%",
        "eps_gaap": 1.08,
        "stock_reaction": "+2.1%", "reaction_note": "네트워킹 매출 서프라이즈에 상승",
        "keywords": ["Blackwell 출하", "네트워킹 급증", "Sovereign AI $20B"],
        "ceo_quote": "블랙웰은 세계가 기다려온 AI 플랫폼입니다. 블랙웰 울트라의 양산이 전속력으로 가속 중이며, 수요는 경이적입니다. H100, H200, 블랙웰 모두 완판 상태입니다.",
        "highlights": [
            "네트워킹 매출 $7.3B (+98% YoY) — 컨센서스 $5.1B 대폭 상회",
            "데이터센터 $41.1B (+56% YoY) — Blackwell 본격 출하 시작",
            "게이밍 $4.3B (+49% YoY) — 분기 사상 최고 기록",
            "Sovereign AI 연매출 $20B 이상 전망 — 유럽·중동 정부 계약 확대",
        ],
        "analyst_comment": "네트워킹 매출의 서프라이즈(+43% vs 컨센서스)가 이 분기의 하이라이트입니다. NVLink 스케일업 네트워크의 채택이 예상보다 빠르게 진행되고 있어, GPU 매출뿐 아니라 인프라 전체에서 NVIDIA의 지배력이 확장되고 있음을 확인했습니다. Q3 가이던스 $54B(+15.6% QoQ)도 양호합니다."
    },
    {
        "q": "Q3 FY2026", "period": "2025.08~10", "date": "2025.11.19",
        "rev_actual": 57.00, "rev_est": 55.50, "rev_beat": True, "rev_surprise": "+2.7%",
        "eps_actual": 1.30, "eps_est": 1.24, "eps_beat": True, "eps_surprise": "+4.8%",
        "eps_gaap": 1.30,
        "stock_reaction": "+3.5%", "reaction_note": "GB300 전환 성공에 시장 환호",
        "keywords": ["GB300 전환", "DC $51B 돌파", "마진 73.4%"],
        "ceo_quote": "블랙웰 매출이 폭발적입니다. 클라우드 GPU는 모두 완판됐습니다. GB300이 GB200을 넘어서 블랙웰 매출의 약 2/3를 차지하며, 주요 CSP로의 양산 출하가 이미 시작됐습니다.",
        "highlights": [
            "데이터센터 $51.2B (+66% YoY) — 단일 분기 $50B 최초 돌파",
            "GB300이 Blackwell 매출의 ~2/3 차지 — GB200→GB300 전환 순조",
            "네트워킹 매출 2배 이상 성장 — NVLink + Spectrum-X + InfiniBand",
            "중국향 매출 지정학적 이슈로 미달 — 그러나 전체 성장에는 미미",
        ],
        "analyst_comment": "데이터센터가 $50B을 돌파한 것은 상징적입니다. GB300으로의 빠른 전환은 고객들이 최신 아키텍처에 대한 확신을 갖고 있다는 증거이며, ASP 상승도 동반합니다. 다만 CFO가 '원가 상승 압력'을 언급한 부분은 FY2027 마진 가이던스에 주의가 필요한 시그널입니다."
    },
    {
        "q": "Q4 FY2026", "period": "2025.11~2026.01", "date": "2026.02.25",
        "rev_actual": 68.13, "rev_est": 66.21, "rev_beat": True, "rev_surprise": "+2.9%",
        "eps_actual": 1.62, "eps_est": 1.53, "eps_beat": True, "eps_surprise": "+5.9%",
        "eps_gaap": 1.76,
        "stock_reaction": "+4.2%", "reaction_note": "가이던스 $78B에 시간외 급등",
        "keywords": ["역대 최고 분기", "가이던스 $78B", "Agentic AI", "Rubin 로드맵"],
        "ceo_quote": "컴퓨팅 수요가 기하급수적으로 증가하고 있습니다 — 에이전틱 AI의 변곡점이 도래했습니다. Grace Blackwell과 NVLink는 오늘의 추론 왕이며, Vera Rubin이 그 리더십을 더욱 확장할 것입니다.",
        "highlights": [
            "매출 $68.1B (+73% YoY, +20% QoQ) — 역대 최고 분기 기록",
            "데이터센터 $62.3B (+75% YoY) — 전체 매출의 91% 차지",
            "Q1 FY2027 가이던스 $78B — 컨센서스 $72.6B 대비 +7.4% 상회",
            "Top 5 하이퍼스케일러 2026년 CapEx $700B 접근 — 연초 대비 +$120B 증가",
        ],
        "analyst_comment": "Q4 실적도 인상적이지만, 진짜 서프라이즈는 Q1 FY2027 가이던스 $78B입니다. 시장 컨센서스 $72.6B을 7.4%나 상회하며, NVIDIA의 성장이 아직 가속 구간에 있음을 증명했습니다. Agentic AI라는 새로운 수요 드라이버의 부상과 하이퍼스케일러 CapEx의 지속 확대는 2026년 전체에 걸쳐 순차적 성장을 뒷받침할 것입니다."
    },
]

NEXT_EARNINGS = {
    "date": "2026.05.27 (수)",
    "quarter": "Q1 FY2027",
    "period": "2026.02~04",
    "rev_guidance": "$78.0B ±2%",
    "rev_range": "$76.4B ~ $79.6B",
    "gm_guidance": "74.9% (GAAP) / 75.0% (Non-GAAP)",
    "consensus_rev": "$78.1B",
    "consensus_eps": "$1.79",
    "analyst_buy_pct": "93%",
    "analyst_count": 70,
    "avg_target": "$267",
    "key_watch": [
        "Blackwell Ultra 양산 진행률 및 수율 확인",
        "Rubin 아키텍처 개발 진척도 및 샘플 출하 시점",
        "미중 수출 규제 추가 강화 여부 및 매출 영향",
        "하이퍼스케일러 CapEx 전망 유지/상향 여부",
        "Non-GAAP GPM 75% 유지 가능성 (원가 상승 압력 대응)",
    ],
}

PEERS = [
    {"sym":"NVDA","name":"NVIDIA","mc":"$4.07T","pe":"34.2","ps":"18.8","rev":"$215.9B","nm":"55.6%","hl":True},
    {"sym":"AMD","name":"AMD","mc":"$210B","pe":"24.8","ps":"7.1","rev":"$28.1B","nm":"22%","hl":False},
    {"sym":"INTC","name":"Intel","mc":"$97B","pe":"-","ps":"1.5","rev":"$53.1B","nm":"-1%","hl":False},
    {"sym":"AVGO","name":"Broadcom","mc":"$1.05T","pe":"38.2","ps":"16.2","rev":"$62.0B","nm":"37%","hl":False},
    {"sym":"QCOM","name":"Qualcomm","mc":"$190B","pe":"16.5","ps":"4.3","rev":"$42.2B","nm":"27%","hl":False},
    {"sym":"TSM","name":"TSMC","mc":"$870B","pe":"22.1","ps":"11.3","rev":"$95.0B","nm":"40%","hl":False},
]

RATIOS = {"pe":34.18,"fpe":20.19,"ps":18.84,"peg":0.53,"roe":"127.5%","div":"0.02%"}

# ══════════════════════════════════════════════════════════════════════════════
# ANALYST COMMENTARY DATA
# ══════════════════════════════════════════════════════════════════════════════

# Tab 1: 기업 개요 (돈을 버는 방법 / 미래 성장 동력 / 주의해야 할 점)
OVERVIEW_MONEY = [
    {
        "emoji": "🏢",
        "title": "데이터센터 GPU — AI 시대의 핵심 엔진",
        "desc": "FY2026 매출 $193.7B로 전체의 약 90%를 차지하는 절대적 핵심 사업입니다. ChatGPT, Gemini, Claude 같은 대규모 AI 모델을 학습하고 추론하는 데 필요한 고성능 GPU를 전 세계 빅테크 기업(Microsoft, Google, Meta, Amazon)과 클라우드 사업자에게 공급해요. 젠슨 황 CEO는 최근 실적 발표에서 '블랙웰의 수요가 미쳤다(Insane)'고 표현할 만큼, 공급이 수요를 따라가지 못하는 상황이 계속되고 있습니다."
    },
    {
        "emoji": "🎮",
        "title": "게이밍 GPU — 브랜드의 출발점이자 기술의 쇼케이스",
        "desc": "GeForce 시리즈로 잘 알려진 PC 게이밍 GPU 사업입니다. FY2026 매출 $16.0B으로 전년 대비 41% 성장하며 다시 반등했어요. 매출 비중은 7.4%로 줄었지만, DLSS 등 AI 기반 그래픽 기술로 게이머 충성도가 높고, 데이터센터 기술을 소비자에게 알리는 브랜드 접점 역할을 합니다."
    },
    {
        "emoji": "🚗",
        "title": "자동차 & 로보틱스 — 자율주행의 두뇌",
        "desc": "DRIVE Thor 플랫폼을 통해 자율주행차의 중앙 컴퓨터 역할을 하는 칩을 공급합니다. FY2026 매출 $2.3B(전년 대비 39% 성장)으로 비중은 약 1%이지만, Mercedes-Benz, BYD 등 주요 완성차 업체와 파트너십을 맺고 있어요. GTC 2026에서 공개한 로보틱스 플랫폼과 함께 장기 성장 잠재력이 큰 사업입니다."
    },
    {
        "emoji": "🖥️",
        "title": "전문 시각화 — 산업용 그래픽의 표준",
        "desc": "건축 설계, 영상 제작, 의료 영상 분석 등 전문 분야 워크스테이션 GPU를 제공합니다. FY2026 매출 $3.2B으로 전년 대비 70% 급성장했어요. Omniverse 플랫폼과 결합한 디지털 트윈 기술이 제조업, 물류 등 산업 현장에서 채택이 확대되고 있습니다."
    },
]

OVERVIEW_GROWTH = [
    {
        "emoji": "🤖",
        "title": "AI 추론 시장의 본격 개화",
        "desc": "지금까지 AI 수요는 '학습(Training)' 중심이었지만, 이제 학습된 모델을 실제 서비스에 적용하는 '추론(Inference)' 수요가 폭발적으로 늘고 있어요. 추론 시장은 학습보다 잠재 규모가 훨씬 크고, NVIDIA의 TensorRT와 최적화된 GPU가 이 시장에서도 지배적입니다."
    },
    {
        "emoji": "🌍",
        "title": "Sovereign AI — 각국 정부의 AI 인프라 투자",
        "desc": "미국, 일본, 인도, 사우디, UAE 등 전 세계 정부가 자국 데이터를 기반으로 한 AI 인프라 구축에 나서고 있어요. 이 'Sovereign AI' 수요는 기존 빅테크 의존에서 벗어나는 새로운 고객층으로, NVIDIA에게는 추가적인 대규모 성장 기회입니다."
    },
    {
        "emoji": "⚡",
        "title": "차세대 아키텍처: Blackwell Ultra → Rubin",
        "desc": "2026년 하반기 Blackwell Ultra, 2027년 Rubin 아키텍처가 순차 출시됩니다. 세대마다 성능이 2~3배 향상되면서 고객의 업그레이드 수요를 지속적으로 창출하는 'GPU 교체 사이클'이 형성되고 있어요."
    },
    {
        "emoji": "🦾",
        "title": "로보틱스와 자율주행의 가속화",
        "desc": "Isaac 플랫폼(산업용 로봇)과 DRIVE Thor(자율주행) 등 물리적 AI 시장으로 확장 중입니다. 휴머노이드 로봇 개발사들의 대부분이 NVIDIA 칩을 채택하면서, 이 시장이 열리면 데이터센터에 이은 차세대 핵심 사업이 될 수 있어요."
    },
]

OVERVIEW_RISKS = [
    {
        "emoji": "⚠️",
        "title": "미중 반도체 수출 규제의 불확실성",
        "desc": "미국 정부의 대중국 반도체 수출 규제가 지속 강화되고 있어요. 중국은 NVIDIA 매출의 약 10~15%를 차지하는데, 규제가 더 강해지면 이 매출이 추가로 줄어들 수 있습니다. 규제 회피용 저사양 칩(H20)도 제재 대상이 될 가능성이 있어요."
    },
    {
        "emoji": "🔥",
        "title": "치열해지는 AI 칩 경쟁",
        "desc": "AMD MI300X, Intel Gaudi3 등 경쟁 GPU뿐 아니라, Google TPU, Amazon Trainium, Microsoft Maia 등 빅테크의 자체 AI 칩(ASIC) 개발이 가속화되고 있어요. 당장은 CUDA 생태계의 진입장벽이 높지만, 장기적으로 시장 점유율 잠식 가능성을 주시해야 합니다."
    },
    {
        "emoji": "📉",
        "title": "AI 투자 사이클의 피크 논쟁",
        "desc": "빅테크 기업들의 AI 인프라 투자(CapEx)가 급증하고 있지만, 이 투자가 실제 수익으로 충분히 전환되고 있는지에 대한 의문이 제기되고 있어요. 만약 기업들이 투자 속도를 줄이면 NVIDIA 매출 성장률도 둔화될 수 있습니다."
    },
    {
        "emoji": "💰",
        "title": "높은 밸류에이션 부담",
        "desc": "Trailing P/E 34배는 초고성장 감안 시 합리적이지만, 시장 기대치가 매우 높은 상태입니다. 분기 실적이 컨센서스를 소폭이라도 하회하면 주가가 큰 폭으로 조정받을 수 있어요. Forward P/E 20배 수준에서의 하방 리스크 관리가 필요합니다."
    },
]

# Tab 2: 재무 분석 — 주요 계정별 애널리스트 코멘터리
FINANCIAL_ITEMS = [
    {
        "category": "손익계산서",
        "items": [
            {
                "label": "매출액",
                "emoji": "🚀",
                "headline": "AI 인프라 수요 폭발로 사상 최대 매출 경신",
                "value": "$215.9B",
                "yoy": "+65.5%",
                "yoy_dir": "up",
                "verified": True,
                "desc": "FY2026 연간 매출이 $215.9B(약 315조원)로 전년($130.5B) 대비 65.5% 급증했어요. Q1 $44.1B → Q2 $46.7B → Q3 $57.0B → Q4 $68.1B로 분기마다 가속 성장하는 모습이 인상적입니다. 데이터센터 부문($193.7B, +68% YoY)이 전체 성장을 견인했으며, 젠슨 황 CEO가 '블랙웰 수요가 미쳤다(Insane)'고 표현할 만큼 공급이 수요를 따라가지 못하고 있어요."
            },
            {
                "label": "매출총이익",
                "emoji": "💎",
                "headline": "71% 마진 — H20 충당금에도 업계 독보적",
                "value": "$153.5B",
                "yoy": "+56.8%",
                "yoy_dir": "up",
                "verified": True,
                "desc": "연간 매출총이익률 71.1%로 반도체 업계 독보적 수준입니다. 다만 분기별로 보면 Q1은 H20(중국향 제품) 재고충당금 $4.5B 반영으로 60.5%까지 급락했다가, Q2 72.4% → Q3 73.4% → Q4 75.0%로 빠르게 회복했어요. Q4의 75% 회복은 Blackwell 양산 안정화와 시스템 솔루션 믹스 개선 덕분이며, Q1 FY2027 가이던스도 74.9%로 높은 수준을 유지할 전망입니다."
            },
            {
                "label": "영업이익",
                "emoji": "⚡",
                "headline": "영업이익률 60% — 규모의 경제 본격 발현",
                "value": "$130.4B",
                "yoy": "+60.1%",
                "yoy_dir": "up",
                "verified": True,
                "desc": "영업이익률이 60.4%로 전년(62.4%)과 유사한 수준을 유지하고 있어요. 매출이 65% 성장하는 동안 R&D($18.5B, +43%)와 판관비($4.6B, +31%) 증가를 효과적으로 통제했다는 의미입니다. 특히 R&D 매출 비중이 9.9%→8.6%로 줄어든 점은 매출 성장의 영업 레버리지가 강하게 작용하고 있음을 보여줘요."
            },
            {
                "label": "순이익",
                "emoji": "📈",
                "headline": "순이익 $120B 돌파, 반도체 역사상 최초",
                "value": "$120.1B",
                "yoy": "+64.8%",
                "yoy_dir": "up",
                "verified": True,
                "desc": "순이익률 55.6%로 빅테크 전체를 통틀어도 최고 수준입니다. 반도체 기업이 연간 순이익 $100B을 넘긴 것은 역사상 처음이에요. 유효세율이 약 12%로 낮은 것은 해외 법인(아일랜드, 이스라엘 등)의 세제 혜택 덕분인데, 글로벌 최저한세(Pillar Two) 시행 시 일부 영향이 있을 수 있습니다."
            },
            {
                "label": "EPS (주당순이익)",
                "emoji": "📊",
                "headline": "EPS $4.90 — 2년 전 대비 4배 이상 증가",
                "value": "$4.90",
                "yoy": "+66.7%",
                "yoy_dir": "up",
                "verified": True,
                "desc": "희석 EPS가 $4.90으로 FY2024($1.19) 대비 4배 이상 급증했어요. FY2026에만 $40.1B의 자사주를 매입(유통주식의 약 3% 소각)하며 EPS 성장에도 기여했습니다. 현재 주가 $167.5 기준 Trailing P/E 34.2배이지만, 애널리스트 70명 중 93%가 매수 의견을 유지하고 평균 목표가는 $267입니다."
            },
        ]
    },
    {
        "category": "투자 효율성",
        "items": [
            {
                "label": "연구개발비 (R&D)",
                "emoji": "🧠",
                "headline": "차세대 AI 칩 경쟁력을 쌓기 위한 공격적 투자",
                "value": "$18.5B",
                "yoy": "+43.3%",
                "yoy_dir": "up",
                "verified": True,
                "desc": "연구개발비가 전년($12.9B) 대비 43% 증가했지만, 매출 대비 비중은 8.6%로 오히려 줄었어요(FY2025: 9.9%). GTC 2026에서 공개한 차세대 Vera Rubin 아키텍처, AI 추론 전용 칩, CUDA 소프트웨어 생태계 확장 등에 집중 투자 중입니다. 애널리스트들은 CUDA 생태계의 '한 번 들어가면 나올 수 없는' 락인 효과를 핵심 해자(Moat)로 평가하고 있어요."
            },
            {
                "label": "유형자산의 취득 (CapEx)",
                "emoji": "🏗️",
                "headline": "팹리스 기업답게 CapEx는 절제된 투자",
                "value": "$6.0B",
                "yoy": "+87.0%",
                "yoy_dir": "up",
                "verified": True,
                "desc": "CapEx가 전년($3.2B) 대비 87% 증가했지만, 매출 대비 비율은 2.8%에 불과해요. 빅테크의 AI CapEx가 매출의 20~30%인 것과 비교하면 NVIDIA는 '직접 공장을 짓지 않고 삽을 파는' 팹리스 모델의 강점이 극명하게 드러납니다. 투자는 자체 AI 슈퍼컴퓨터(DGX SuperPOD) 확충과 제품 검증 인프라에 집중되고 있어요."
            },
        ]
    },
    {
        "category": "현금의 흐름",
        "items": [
            {
                "label": "영업활동현금흐름",
                "emoji": "💰",
                "headline": "연간 $103B — 역대 최고의 현금 창출력",
                "value": "$102.7B",
                "yoy": "+60.3%",
                "yoy_dir": "up",
                "verified": True,
                "desc": "영업현금흐름이 $102.7B로 역대 최고를 기록했어요. 순이익($120B) 대비 85.6%의 현금전환율을 보이며, 이익의 질(Quality of Earnings)이 매우 높습니다. 특히 Q4에만 $36.2B의 영업현금을 창출해 분기별로도 가속되는 모습이에요. 팩트셋은 FY2027 잉여현금흐름을 $178B으로 전망하고 있습니다."
            },
            {
                "label": "잉여현금흐름 (FCF)",
                "emoji": "📐",
                "headline": "FCF $96.6B — 주주환원의 원천",
                "value": "$96.6B",
                "yoy": "+58.7%",
                "yoy_dir": "up",
                "verified": True,
                "desc": "잉여현금흐름이 $96.6B로 전년($60.9B) 대비 59% 급증했어요. FCF 마진이 44.7%로, 벌어들인 매출의 거의 절반이 자유롭게 쓸 수 있는 현금으로 전환됩니다. 이 현금의 상당 부분이 자사주 매입($40.1B)과 배당($1.0B)으로 주주에게 환원되고 있으며, 나머지는 전략적 투자와 미래 성장을 위해 유보되고 있어요."
            },
        ]
    },
]

INVEST = {
    "strengths":["AI 인프라 시장 절대 지배력: 데이터센터 GPU 시장 점유율 90%+ 유지","CUDA 생태계 락인: 소프트웨어 플랫폼으로 강력한 진입장벽 형성","FY2026 매출 $215.9B, 전년 대비 65% 성장의 초고성장 지속","순이익률 55.6%로 반도체 업계 최고 수준의 수익성"],
    "risks":["미중 반도체 수출 규제 강화에 따른 중국향 매출 감소 리스크","AMD MI300X, Intel Gaudi3, 자체 ASIC(Google TPU, AWS Trainium) 등 경쟁 심화","AI 인프라 투자 사이클 둔화 가능성 (Capex 피크 논쟁)","고밸류에이션 부담: Trailing P/E 34x, 기대치 미달 시 급락 가능"],
    "opportunities":["Sovereign AI: 각국 정부의 자체 AI 인프라 구축 수요 급증","Blackwell Ultra / Rubin 차세대 아키텍처로 성능 리더십 유지","AI 추론(Inference) 시장 본격 성장 — 학습 대비 훨씬 큰 시장","자율주행 / 로보틱스: DRIVE Thor, Isaac 플랫폼으로 새 성장동력"],
    "watchlist":["FY2027 Q1 가이던스 $45B (시장 기대 상회 여부)","Blackwell Ultra 양산 일정 및 수율 (H2 2026)","중국 수출 규제 완화/강화 방향성","AI Capex 투자 추이: MSFT, GOOG, META, AMZN의 분기별 설비투자"]
}


# ══════════════════════════════════════════════════════════════════════════════
# SVG CHART GENERATORS (same as v6)
# ══════════════════════════════════════════════════════════════════════════════

def svg_grouped_bar(labels, datasets, W=580, H=260):
    pad_l,pad_r,pad_t,pad_b=55,15,15,45; cW=W-pad_l-pad_r; cH=H-pad_t-pad_b
    all_vals=[v for ds in datasets for v in ds["data"]]; max_v=max(all_vals)*1.15 if all_vals else 1
    n=len(labels); g_count=len(datasets); g_w=cW/n; b_w=(g_w*0.65)/g_count
    lines=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
    for i in range(5):
        y=pad_t+cH-(cH*i/4); val=max_v*i/4
        lines.append(f'<line x1="{pad_l}" y1="{y}" x2="{W-pad_r}" y2="{y}" stroke="#2d3148"/>')
        lines.append(f'<text x="{pad_l-6}" y="{y+4}" fill="#9ca0b8" font-size="10" text-anchor="end">${val:.0f}B</text>')
    for di,ds in enumerate(datasets):
        for vi,v in enumerate(ds["data"]):
            x=pad_l+vi*g_w+g_w*0.175+di*b_w; bh=(v/max_v)*cH; y=pad_t+cH-bh
            lines.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{b_w:.1f}" height="{bh:.1f}" rx="3" fill="{ds["color"]}" opacity="0.8"/>')
            if g_count<=2: lines.append(f'<text x="{x+b_w/2:.1f}" y="{y-3}" fill="{ds["color"]}" font-size="8" text-anchor="middle" font-weight="600">${v:.1f}B</text>')
    for i,l in enumerate(labels):
        x=pad_l+i*g_w+g_w/2; lines.append(f'<text x="{x:.1f}" y="{H-pad_b+18}" fill="#9ca0b8" font-size="10" text-anchor="middle">{l}</text>')
    lx=pad_l
    for ds in datasets:
        lines.append(f'<rect x="{lx}" y="{H-10}" width="8" height="8" rx="2" fill="{ds["color"]}"/>')
        lines.append(f'<text x="{lx+12}" y="{H-3}" fill="#9ca0b8" font-size="9">{ds["label"]}</text>')
        lx+=len(ds["label"])*7+22
    lines.append('</svg>'); return '\n'.join(lines)

def svg_line_chart(labels, datasets, W=580, H=260):
    pad_l,pad_r,pad_t,pad_b=45,15,15,45; cW=W-pad_l-pad_r; cH=H-pad_t-pad_b
    all_vals=[v for ds in datasets for v in ds["data"]]; max_v=max(all_vals)*1.1 if all_vals else 100
    min_v=min(all_vals)*0.85 if all_vals else 0
    if min_v<0: min_v=0
    rng=max_v-min_v if max_v!=min_v else 1; n=len(labels)
    lines=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
    for i in range(5):
        y=pad_t+cH-(cH*i/4); val=min_v+rng*i/4
        lines.append(f'<line x1="{pad_l}" y1="{y}" x2="{W-pad_r}" y2="{y}" stroke="#2d3148"/>')
        lines.append(f'<text x="{pad_l-5}" y="{y+4}" fill="#9ca0b8" font-size="10" text-anchor="end">{val:.0f}%</text>')
    for ds in datasets:
        pts=[]
        for vi,v in enumerate(ds["data"]):
            x=pad_l+(vi/max(n-1,1))*cW; y=pad_t+cH-((v-min_v)/rng)*cH; pts.append(f"{x:.1f},{y:.1f}")
        lines.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{ds["color"]}" stroke-width="2.5" stroke-linejoin="round"/>')
        for vi,v in enumerate(ds["data"]):
            x=pad_l+(vi/max(n-1,1))*cW; y=pad_t+cH-((v-min_v)/rng)*cH
            lines.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{ds["color"]}"/>')
            lines.append(f'<text x="{x:.1f}" y="{y-7}" fill="{ds["color"]}" font-size="8" text-anchor="middle" font-weight="600">{v:.1f}%</text>')
    for i,l in enumerate(labels):
        x=pad_l+(i/max(n-1,1))*cW; lines.append(f'<text x="{x:.1f}" y="{H-pad_b+18}" fill="#9ca0b8" font-size="10" text-anchor="middle">{l}</text>')
    lx=pad_l
    for ds in datasets:
        lines.append(f'<rect x="{lx}" y="{H-10}" width="8" height="8" rx="2" fill="{ds["color"]}"/>')
        lines.append(f'<text x="{lx+12}" y="{H-3}" fill="#9ca0b8" font-size="9">{ds["label"]}</text>')
        lx+=len(ds["label"])*6+20
    lines.append('</svg>'); return '\n'.join(lines)

def svg_donut(slices, W=580, H=260):
    total=sum(s["value"] for s in slices); cx,cy,R,r=180,130,105,55
    lines=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
    angle=-math.pi/2
    for s in slices:
        pct=s["value"]/total if total else 0; a1=angle; a2=angle+pct*2*math.pi; large=1 if pct>0.5 else 0
        x1o=cx+R*math.cos(a1);y1o=cy+R*math.sin(a1);x2o=cx+R*math.cos(a2);y2o=cy+R*math.sin(a2)
        x1i=cx+r*math.cos(a2);y1i=cy+r*math.sin(a2);x2i=cx+r*math.cos(a1);y2i=cy+r*math.sin(a1)
        d=f"M{x1o:.1f},{y1o:.1f} A{R},{R} 0 {large},1 {x2o:.1f},{y2o:.1f} L{x1i:.1f},{y1i:.1f} A{r},{r} 0 {large},0 {x2i:.1f},{y2i:.1f} Z"
        lines.append(f'<path d="{d}" fill="{s["color"]}" opacity="0.85"/>'); angle=a2
    lines.append(f'<text x="{cx}" y="{cy-4}" fill="#e4e6f0" font-size="14" font-weight="800" text-anchor="middle">${total:.1f}B</text>')
    lines.append(f'<text x="{cx}" y="{cy+14}" fill="#9ca0b8" font-size="10" text-anchor="middle">Total Revenue</text>')
    ly=30
    for s in slices:
        pv=s["value"]/total*100 if total else 0
        lines.append(f'<rect x="370" y="{ly}" width="12" height="12" rx="3" fill="{s["color"]}"/>')
        lines.append(f'<text x="388" y="{ly+11}" fill="#e4e6f0" font-size="11">{s["name"]}</text>')
        lines.append(f'<text x="555" y="{ly+11}" fill="#9ca0b8" font-size="11" text-anchor="end">{pv:.1f}%</text>')
        ly+=30
    lines.append('</svg>'); return '\n'.join(lines)

def svg_stacked_bar(labels, series, W=580, H=260):
    pad_l,pad_r,pad_t,pad_b=55,15,15,45; cW=W-pad_l-pad_r; cH=H-pad_t-pad_b; n=len(labels)
    totals=[sum(s["data"][i] for s in series) for i in range(n)]; max_v=max(totals)*1.1 if totals else 1; b_w=cW/n*0.6
    lines=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
    for g in range(5):
        y=pad_t+cH-(cH*g/4); val=max_v*g/4
        lines.append(f'<line x1="{pad_l}" y1="{y}" x2="{W-pad_r}" y2="{y}" stroke="#2d3148"/>')
        lines.append(f'<text x="{pad_l-6}" y="{y+4}" fill="#9ca0b8" font-size="10" text-anchor="end">${val:.0f}B</text>')
    for i in range(n):
        base_y=pad_t+cH; x=pad_l+i*(cW/n)+(cW/n-b_w)/2
        for s in series:
            v=s["data"][i]; bh=(v/max_v)*cH
            lines.append(f'<rect x="{x:.1f}" y="{base_y-bh:.1f}" width="{b_w:.1f}" height="{bh:.1f}" fill="{s["color"]}" opacity="0.8"/>'); base_y-=bh
        lx=pad_l+i*(cW/n)+(cW/n)/2
        lines.append(f'<text x="{lx:.1f}" y="{H-pad_b+18}" fill="#9ca0b8" font-size="10" text-anchor="middle">{labels[i]}</text>')
    lx=pad_l
    for s in series:
        lines.append(f'<rect x="{lx}" y="{H-10}" width="8" height="8" rx="2" fill="{s["color"]}"/>')
        lines.append(f'<text x="{lx+12}" y="{H-3}" fill="#9ca0b8" font-size="9">{s["name"]}</text>'); lx+=len(s["name"])*7+20
    lines.append('</svg>'); return '\n'.join(lines)

def svg_eps_per(income, current_price, accent):
    W,H=580,260; pad_l,pad_r,pad_t,pad_b=55,55,15,45; cW=W-pad_l-pad_r; cH=H-pad_t-pad_b
    eps_vals=[d["eps"] for d in income]; per_vals=[current_price/e if e>0 else 0 for e in eps_vals]
    max_eps=max(abs(e) for e in eps_vals)*1.2 if eps_vals else 1; max_per=max(per_vals)*1.2 if per_vals and max(per_vals)>0 else 50
    if max_eps==0: max_eps=1
    if max_per==0: max_per=1
    n=len(income); bw=cW/n*0.5
    lines=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
    for g in range(5):
        y=pad_t+cH-(cH*g/4)
        lines.append(f'<line x1="{pad_l}" y1="{y}" x2="{W-pad_r}" y2="{y}" stroke="#2d3148"/>')
        lines.append(f'<text x="{pad_l-6}" y="{y+4}" fill="{accent}" font-size="9" text-anchor="end">${max_eps*g/4:.1f}</text>')
        lines.append(f'<text x="{W-pad_r+6}" y="{y+4}" fill="#ffa94d" font-size="9">{max_per*g/4:.0f}x</text>')
    for i,e in enumerate(eps_vals):
        if e<=0: continue
        x=pad_l+i*(cW/n)+(cW/n-bw)/2; bh=(e/max_eps)*cH; y=pad_t+cH-bh
        lines.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="3" fill="{accent}" opacity="0.7"/>')
        lines.append(f'<text x="{x+bw/2:.1f}" y="{y-3}" fill="{accent}" font-size="8" text-anchor="middle" font-weight="600">${e:.2f}</text>')
    pts=[]
    for i,pe in enumerate(per_vals):
        if pe<=0: continue
        x=pad_l+i*(cW/n)+cW/n/2; y=pad_t+cH-(pe/max_per)*cH; pts.append(f"{x:.1f},{y:.1f}")
    if pts:
        lines.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#ffa94d" stroke-width="2.5"/>')
    for i,pe in enumerate(per_vals):
        if pe<=0: continue
        x=pad_l+i*(cW/n)+cW/n/2; y=pad_t+cH-(pe/max_per)*cH
        lines.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#ffa94d"/>')
        lines.append(f'<text x="{x:.1f}" y="{y-7}" fill="#ffa94d" font-size="8" text-anchor="middle" font-weight="600">{pe:.1f}x</text>')
    for i,d in enumerate(income):
        x=pad_l+i*(cW/n)+cW/n/2; lines.append(f'<text x="{x:.1f}" y="{H-pad_b+18}" fill="#9ca0b8" font-size="10" text-anchor="middle">FY{d["year"]}</text>')
    lines.append(f'<rect x="{pad_l}" y="{H-10}" width="8" height="8" rx="2" fill="{accent}"/><text x="{pad_l+12}" y="{H-3}" fill="#9ca0b8" font-size="9">EPS</text>')
    lines.append(f'<rect x="{pad_l+50}" y="{H-10}" width="8" height="8" rx="2" fill="#ffa94d"/><text x="{pad_l+62}" y="{H-3}" fill="#9ca0b8" font-size="9">P/E (현재가 기준)</text>')
    lines.append('</svg>'); return '\n'.join(lines)


# ══════════════════════════════════════════════════════════════════════════════
# GENERATE CHARTS
# ══════════════════════════════════════════════════════════════════════════════
accent = PROFILE["accent"]

rev_chart = svg_grouped_bar(
    [f'FY{d["year"]}' for d in INCOME],
    [{"label":"매출","color":accent,"data":[d["rev"] for d in INCOME]},
     {"label":"순이익","color":"#4ecdc4","data":[d["ni"] for d in INCOME]}]
)
margin_chart = svg_line_chart(
    [f'FY{d["year"]}' for d in INCOME],
    [{"label":"매출총이익률","color":accent,"data":[d["gm"] for d in INCOME]},
     {"label":"영업이익률","color":"#4dabf7","data":[d["om"] for d in INCOME]},
     {"label":"순이익률","color":"#b197fc","data":[d["nm"] for d in INCOME]}]
)
q_chart = svg_grouped_bar(
    [d["q"] for d in QUARTERLY],
    [{"label":"분기 매출","color":accent,"data":[d["rev"] for d in QUARTERLY]},
     {"label":"분기 순이익","color":"#4ecdc4","data":[d["ni"] for d in QUARTERLY]}]
)
donut_chart = svg_donut([{"name":s["name"],"value":s["data"][-1],"color":s["color"]} for s in SEGMENTS["series"]])
stacked_chart = svg_stacked_bar(SEGMENTS["labels"], SEGMENTS["series"])
eps_chart = svg_eps_per(INCOME, PROFILE["price"], accent)

# R&D / CapEx / OCF / FCF chart
rnd_capex_chart = svg_grouped_bar(
    [f'FY{d["year"]}' for d in INCOME],
    [{"label":"R&D","color":"#b197fc","data":[d["rnd"] for d in INCOME]},
     {"label":"CapEx","color":"#ffa94d","data":[d["capex"] for d in INCOME]}]
)
cashflow_chart = svg_grouped_bar(
    [f'FY{d["year"]}' for d in INCOME],
    [{"label":"영업CF","color":"#4ecdc4","data":[d["ocf"] for d in INCOME]},
     {"label":"FCF","color":"#76b900","data":[d["fcf"] for d in INCOME]}]
)

# Quarterly segment charts
q_seg_stacked = svg_stacked_bar(
    QUARTERLY_SEGMENTS["labels"],
    QUARTERLY_SEGMENTS["series"]
)

q_seg_donut = svg_donut([{"name":s["name"],"value":s["data"][-1],"color":s["color"]} for s in QUARTERLY_SEGMENTS["series"]])

# Quarterly margin chart
q_margin_chart = svg_line_chart(
    [d["q"] for d in QUARTERLY_DETAIL],
    [{"label":"매출총이익률","color":accent,"data":[d["gm"] for d in QUARTERLY_DETAIL]},
     {"label":"영업이익률","color":"#4dabf7","data":[d["om"] for d in QUARTERLY_DETAIL]},
     {"label":"순이익률","color":"#b197fc","data":[d["nm"] for d in QUARTERLY_DETAIL]}]
)

# Peer bars
peer_pe_bars = ''
pe_peers = [p for p in PEERS if p["pe"]!="-"]
for i,pp in enumerate(pe_peers):
    pe_val = float(pp["pe"])
    max_pe = max(float(x["pe"]) for x in pe_peers) * 1.2
    bh = pe_val / max_pe * 140 if max_pe > 0 else 0
    fill = accent if pp["hl"] else "#4dabf7"
    peer_pe_bars += f'<rect x="{50+i*90}" y="{180-bh:.0f}" width="60" height="{bh:.0f}" rx="4" fill="{fill}" opacity="0.8"/>'
    peer_pe_bars += f'<text x="{80+i*90}" y="{175-bh:.0f}" fill="{fill}" font-size="10" text-anchor="middle" font-weight="600">{pp["pe"]}x</text>'
    peer_pe_bars += f'<text x="{80+i*90}" y="198" fill="#9ca0b8" font-size="10" text-anchor="middle">{pp["sym"]}</text>'

rev_g = ((INCOME[-1]["rev"]-INCOME[-2]["rev"])/INCOME[-2]["rev"]*100)
ni_g = ((INCOME[-1]["ni"]-INCOME[-2]["ni"])/INCOME[-2]["ni"]*100)


# ══════════════════════════════════════════════════════════════════════════════
# HTML GENERATION HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def gen_overview_section(title, subtitle, items, gradient):
    """Generate a section card with emoji items."""
    html = f'<div class="section-card"><div class="section-header" style="background:{gradient}"><div class="section-subtitle">{subtitle}</div><div class="section-title">{title}</div></div><div class="section-body">'
    for item in items:
        html += f'<div class="insight-item"><div class="insight-header"><span class="insight-emoji">{item["emoji"]}</span><span class="insight-title">{item["title"]}</span></div><p class="insight-desc">{item["desc"]}</p></div>'
    html += '</div></div>'
    return html

def gen_financial_section(category_data):
    """Generate financial items with analyst commentary and verification badges."""
    html = ''
    for cat in category_data:
        html += f'<div class="fin-category"><div class="fin-cat-title">{cat["category"]}</div>'
        for item in cat["items"]:
            arrow = "&#9650;" if item["yoy_dir"]=="up" else "&#9660;"
            color = "var(--green)" if item["yoy_dir"]=="up" else "var(--red)"
            badge = '<span class="src-badge verified">IR 공시</span>' if item.get("verified") else '<span class="src-badge estimate">추정치</span>'
            html += f'''<div class="fin-item">
<div class="fin-item-label">{item["label"]} {badge}</div>
<div class="fin-item-headline"><span class="fin-emoji">{item["emoji"]}</span> {item["headline"]}</div>
<div class="fin-metric-row">
<div class="fin-metric-value">{item["value"]}</div>
<div class="fin-metric-change" style="color:{color}"><span style="font-size:11px;">{arrow}</span> 전년 대비 {item["yoy"]}</div>
</div>
<p class="fin-item-desc">{item["desc"]}</p>
</div>'''
        html += '</div>'
    return html

def fin_table():
    rows=[("매출 (Revenue)",[f"${d['rev']:.1f}B" for d in INCOME]),
          ("매출총이익 (Gross Profit)",[f"${d['gp']:.1f}B" for d in INCOME]),
          ("영업이익 (Operating Income)",[f"${d['oi']:.1f}B" for d in INCOME]),
          ("순이익 (Net Income)",[f"${d['ni']:.1f}B" for d in INCOME]),
          ("EPS (희석)",[f"${d['eps']:.2f}" for d in INCOME]),
          ("R&D",[f"${d['rnd']:.1f}B" for d in INCOME]),
          ("CapEx",[f"${d['capex']:.1f}B" for d in INCOME]),
          ("영업CF",[f"${d['ocf']:.1f}B" for d in INCOME]),
          ("FCF",[f"${d['fcf']:.1f}B" for d in INCOME]),
          ("매출총이익률",[f"{d['gm']:.1f}%" for d in INCOME]),
          ("영업이익률",[f"{d['om']:.1f}%" for d in INCOME]),
          ("순이익률",[f"{d['nm']:.1f}%" for d in INCOME])]
    h='<table><thead><tr><th>지표</th>'
    for d in INCOME: h+=f'<th class="nr">FY{d["year"]}</th>'
    h+='</tr></thead><tbody>'
    for l,vs in rows:
        h+=f'<tr><td>{l}</td>'
        for v in vs: h+=f'<td class="nr">{v}</td>'
        h+='</tr>'
    return h+'</tbody></table>'

def seg_table():
    h='<table><thead><tr><th>부문</th>'
    for l in SEGMENTS["labels"]: h+=f'<th class="nr">{l}</th>'
    h+='</tr></thead><tbody>'
    for s in SEGMENTS["series"]:
        h+=f'<tr><td><span style="display:inline-block;width:10px;height:10px;border-radius:3px;background:{s["color"]};margin-right:8px;vertical-align:middle;"></span>{s["name"]}</td>'
        for v in s["data"]: h+=f'<td class="nr">${v:.1f}B</td>'
        h+='</tr>'
    return h+'</tbody></table>'

def q_seg_table():
    h='<table><thead><tr><th>부문</th>'
    for l in QUARTERLY_SEGMENTS["labels"]: h+=f'<th class="nr">{l}</th>'
    h+='<th class="nr">QoQ</th></tr></thead><tbody>'
    for s in QUARTERLY_SEGMENTS["series"]:
        qoq = (s["data"][-1] - s["data"][-2]) / s["data"][-2] * 100 if s["data"][-2] != 0 else 0
        qoq_cls = "up" if qoq >= 0 else "down"
        qoq_str = f'+{qoq:.1f}%' if qoq >= 0 else f'{qoq:.1f}%'
        h+=f'<tr><td><span style="display:inline-block;width:10px;height:10px;border-radius:3px;background:{s["color"]};margin-right:8px;vertical-align:middle;"></span>{s["name"]}</td>'
        for v in s["data"]: h+=f'<td class="nr">${v:.1f}B</td>' if v >= 1 else f'<td class="nr">${v*1000:.0f}M</td>'
        h+=f'<td class="nr {qoq_cls}">{qoq_str}</td></tr>'
    # Total row
    h+='<tr style="font-weight:700;border-top:2px solid var(--accent);"><td>Total</td>'
    for i in range(len(QUARTERLY_SEGMENTS["labels"])):
        t = sum(s["data"][i] for s in QUARTERLY_SEGMENTS["series"])
        h+=f'<td class="nr">${t:.1f}B</td>'
    h+='<td class="nr"></td></tr>'
    return h+'</tbody></table>'

def q_detail_table():
    h='<table><thead><tr><th>분기</th><th class="nr">매출</th><th class="nr">순이익</th><th class="nr">GPM</th><th class="nr">OPM</th><th class="nr">NPM</th><th>비고</th></tr></thead><tbody>'
    for d in QUARTERLY_DETAIL:
        h+=f'<tr><td>{d["q"]}</td><td class="nr">${d["rev"]:.1f}B</td><td class="nr">${d["ni"]:.1f}B</td>'
        h+=f'<td class="nr">{d["gm"]:.1f}%</td><td class="nr">{d["om"]:.1f}%</td><td class="nr">{d["nm"]:.1f}%</td>'
        h+=f'<td style="font-size:12px;color:var(--text2);">{d.get("note","")}</td></tr>'
    return h+'</tbody></table>'

def peer_table():
    h='<table><thead><tr><th>티커</th><th>기업명</th><th class="nr">시가총액</th><th class="nr">P/E</th><th class="nr">P/S</th><th class="nr">매출</th><th class="nr">순이익률</th></tr></thead><tbody>'
    for p in PEERS:
        bg=' style="background:rgba(118,185,0,.1);"' if p["hl"] else ''
        sym=f'<strong>{p["sym"]}</strong>' if p["hl"] else p["sym"]
        h+=f'<tr{bg}><td>{sym}</td><td>{p["name"]}</td><td class="nr">{p["mc"]}</td><td class="nr">{p["pe"]}</td><td class="nr">{p["ps"]}</td><td class="nr">{p["rev"]}</td><td class="nr">{p["nm"]}</td></tr>'
    return h+'</tbody></table>'

def svg_earnings_compare(quarters, W=580, H=260):
    """매출 실적 vs 컨센서스 비교 그룹드 바 차트"""
    labels = [q["q"].replace("FY2026","").strip() for q in quarters]
    pad_l, pad_r, pad_t, pad_b = 60, 20, 30, 50
    cw = W - pad_l - pad_r
    ch = H - pad_t - pad_b
    n = len(labels)
    gw = cw / n
    bw = gw * 0.30
    vals = []
    for q in quarters:
        vals.extend([q["rev_est"], q["rev_actual"]])
    mx = max(vals) * 1.15
    def y(v): return pad_t + ch - (v / mx * ch)
    svg = ''
    # grid lines
    for i in range(5):
        gv = mx * i / 4
        yp = y(gv)
        svg += f'<line x1="{pad_l}" y1="{yp}" x2="{W-pad_r}" y2="{yp}" stroke="rgba(255,255,255,.06)" stroke-dasharray="4,4"/>'
        svg += f'<text x="{pad_l-8}" y="{yp+4}" fill="var(--text2)" font-size="10" text-anchor="end" font-family="Geist Mono,monospace">${gv:.0f}B</text>'
    for i, q in enumerate(quarters):
        cx = pad_l + i * gw + gw / 2
        # consensus bar (gray)
        bh_est = q["rev_est"] / mx * ch
        svg += f'<rect x="{cx - bw - 2}" y="{y(q["rev_est"])}" width="{bw}" height="{bh_est}" rx="3" fill="rgba(255,255,255,.15)"/>'
        svg += f'<text x="{cx - bw/2 - 2}" y="{y(q["rev_est"])-5}" fill="var(--text2)" font-size="9" text-anchor="middle" font-family="Geist Mono,monospace">${q["rev_est"]:.1f}B</text>'
        # actual bar (green)
        bh_act = q["rev_actual"] / mx * ch
        svg += f'<rect x="{cx + 2}" y="{y(q["rev_actual"])}" width="{bw}" height="{bh_act}" rx="3" fill="var(--accent)"/>'
        svg += f'<text x="{cx + bw/2 + 2}" y="{y(q["rev_actual"])-5}" fill="var(--accent)" font-size="9" font-weight="700" text-anchor="middle" font-family="Geist Mono,monospace">${q["rev_actual"]:.1f}B</text>'
        # label
        svg += f'<text x="{cx}" y="{H-10}" fill="var(--text2)" font-size="11" text-anchor="middle">{labels[i]}</text>'
        # surprise badge
        svg += f'<text x="{cx}" y="{H-25}" fill="#76b900" font-size="9" font-weight="700" text-anchor="middle" font-family="Geist Mono,monospace">{q["rev_surprise"]}</text>'
    # legend
    svg += f'<rect x="{W-160}" y="8" width="10" height="10" rx="2" fill="rgba(255,255,255,.15)"/>'
    svg += f'<text x="{W-145}" y="17" fill="var(--text2)" font-size="10">컨센서스</text>'
    svg += f'<rect x="{W-90}" y="8" width="10" height="10" rx="2" fill="var(--accent)"/>'
    svg += f'<text x="{W-75}" y="17" fill="var(--text2)" font-size="10">실제 매출</text>'
    return f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{svg}</svg>'

def svg_eps_surprise(quarters, W=580, H=260):
    """EPS 실적 vs 컨센서스 비교 차트"""
    labels = [q["q"].replace("FY2026","").strip() for q in quarters]
    pad_l, pad_r, pad_t, pad_b = 60, 20, 30, 50
    cw = W - pad_l - pad_r
    ch = H - pad_t - pad_b
    n = len(labels)
    gw = cw / n
    bw = gw * 0.30
    vals = []
    for q in quarters:
        vals.extend([q["eps_est"], q["eps_actual"]])
    mx = max(vals) * 1.20
    def y(v): return pad_t + ch - (v / mx * ch)
    svg = ''
    for i in range(5):
        gv = mx * i / 4
        yp = y(gv)
        svg += f'<line x1="{pad_l}" y1="{yp}" x2="{W-pad_r}" y2="{yp}" stroke="rgba(255,255,255,.06)" stroke-dasharray="4,4"/>'
        svg += f'<text x="{pad_l-8}" y="{yp+4}" fill="var(--text2)" font-size="10" text-anchor="end" font-family="Geist Mono,monospace">${gv:.2f}</text>'
    for i, q in enumerate(quarters):
        cx = pad_l + i * gw + gw / 2
        bh_est = q["eps_est"] / mx * ch
        svg += f'<rect x="{cx - bw - 2}" y="{y(q["eps_est"])}" width="{bw}" height="{bh_est}" rx="3" fill="rgba(255,255,255,.15)"/>'
        svg += f'<text x="{cx - bw/2 - 2}" y="{y(q["eps_est"])-5}" fill="var(--text2)" font-size="9" text-anchor="middle" font-family="Geist Mono,monospace">${q["eps_est"]:.2f}</text>'
        bh_act = q["eps_actual"] / mx * ch
        svg += f'<rect x="{cx + 2}" y="{y(q["eps_actual"])}" width="{bw}" height="{bh_act}" rx="3" fill="#4ecdc4"/>'
        svg += f'<text x="{cx + bw/2 + 2}" y="{y(q["eps_actual"])-5}" fill="#4ecdc4" font-size="9" font-weight="700" text-anchor="middle" font-family="Geist Mono,monospace">${q["eps_actual"]:.2f}</text>'
        svg += f'<text x="{cx}" y="{H-10}" fill="var(--text2)" font-size="11" text-anchor="middle">{labels[i]}</text>'
        svg += f'<text x="{cx}" y="{H-25}" fill="#4ecdc4" font-size="9" font-weight="700" text-anchor="middle" font-family="Geist Mono,monospace">{q["eps_surprise"]}</text>'
    svg += f'<rect x="{W-160}" y="8" width="10" height="10" rx="2" fill="rgba(255,255,255,.15)"/>'
    svg += f'<text x="{W-145}" y="17" fill="var(--text2)" font-size="10">컨센서스</text>'
    svg += f'<rect x="{W-90}" y="8" width="10" height="10" rx="2" fill="#4ecdc4"/>'
    svg += f'<text x="{W-75}" y="17" fill="var(--text2)" font-size="10">실제 EPS</text>'
    return f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{svg}</svg>'

def earnings_call_cards():
    """분기별 컨퍼런스콜 요약 카드 생성"""
    h = ''
    for q in reversed(EARNINGS_QUARTERS):
        beat_cls = "up" if q["eps_beat"] else "down"
        beat_txt = "Beat" if q["eps_beat"] else "Miss"
        react_cls = "up" if q["stock_reaction"].startswith("+") else "down"
        badges = ''.join(f'<span class="earn-badge">{kw}</span>' for kw in q["keywords"])
        highlights = ''.join(f'<li>{hl}</li>' for hl in q["highlights"])
        h += f'''<div class="earn-card reveal">
  <div class="earn-header">
    <div class="earn-q">{q["q"]}</div>
    <div class="earn-date">{q["date"]} 발표 | {q["period"]}</div>
    <div class="earn-surprise {beat_cls}">EPS {beat_txt} {q["eps_surprise"]}</div>
  </div>
  <div class="earn-badges">{badges}</div>
  <div class="earn-metrics">
    <div class="earn-metric">
      <div class="earn-metric-label">매출</div>
      <div class="earn-metric-val">${q["rev_actual"]:.1f}B</div>
      <div class="earn-metric-sub">vs est. ${q["rev_est"]:.1f}B ({q["rev_surprise"]})</div>
    </div>
    <div class="earn-metric">
      <div class="earn-metric-label">EPS (Non-GAAP)</div>
      <div class="earn-metric-val">${q["eps_actual"]:.2f}</div>
      <div class="earn-metric-sub">vs est. ${q["eps_est"]:.2f} ({q["eps_surprise"]})</div>
    </div>
    <div class="earn-metric">
      <div class="earn-metric-label">EPS (GAAP)</div>
      <div class="earn-metric-val">${q["eps_gaap"]:.2f}</div>
      <div class="earn-metric-sub">&nbsp;</div>
    </div>
    <div class="earn-metric">
      <div class="earn-metric-label">주가 반응</div>
      <div class="earn-metric-val {react_cls}">{q["stock_reaction"]}</div>
      <div class="earn-metric-sub">{q["reaction_note"]}</div>
    </div>
  </div>
  <div class="earn-ceo">
    <div class="earn-ceo-label">🎙️ Jensen Huang CEO</div>
    <div class="earn-ceo-quote">"{q["ceo_quote"]}"</div>
  </div>
  <div class="earn-highlights">
    <div class="earn-hl-title">📋 주요 하이라이트</div>
    <ul>{highlights}</ul>
  </div>
  <div class="earn-analyst">
    <div class="earn-analyst-title">📊 애널리스트 코멘트</div>
    <p>{q["analyst_comment"]}</p>
  </div>
</div>'''
    return h

def next_earnings_card():
    """다음 실적발표 예정 카드"""
    ne = NEXT_EARNINGS
    watches = ''.join(f'<li>{w}</li>' for w in ne["key_watch"])
    return f'''<div class="next-earn reveal">
  <div class="next-earn-header">
    <div class="next-earn-icon">📅</div>
    <div>
      <div class="next-earn-title">다음 실적발표 예정</div>
      <div class="next-earn-date">{ne["date"]} | {ne["quarter"]} ({ne["period"]})</div>
    </div>
    <div class="next-earn-countdown">D-60</div>
  </div>
  <div class="next-earn-grid">
    <div class="next-earn-item"><div class="ne-label">매출 가이던스</div><div class="ne-value" style="color:var(--accent)">{ne["rev_guidance"]}</div><div class="ne-sub">{ne["rev_range"]}</div></div>
    <div class="next-earn-item"><div class="ne-label">매출총이익률</div><div class="ne-value">{ne["gm_guidance"]}</div><div class="ne-sub">가이던스 기준</div></div>
    <div class="next-earn-item"><div class="ne-label">컨센서스 매출</div><div class="ne-value">{ne["consensus_rev"]}</div><div class="ne-sub">EPS est. {ne["consensus_eps"]}</div></div>
    <div class="next-earn-item"><div class="ne-label">애널리스트 의견</div><div class="ne-value" style="color:var(--accent)">{ne["analyst_buy_pct"]} 매수</div><div class="ne-sub">{ne["analyst_count"]}명 | 목표가 {ne["avg_target"]}</div></div>
  </div>
  <div class="next-earn-watch">
    <div class="ne-watch-title">🔍 Key Watchpoints</div>
    <ul>{watches}</ul>
  </div>
</div>'''

def invest_html():
    sections=[("강점 (Strengths)","strengths","dot-green"),("리스크 (Risks)","risks","dot-red"),("기회 (Opportunities)","opportunities","dot-blue"),("주요 모니터링 (Watchlist)","watchlist","dot-orange")]
    h=''
    for title,key,dot in sections:
        h+=f'<div class="invest-card"><h4><span class="dot {dot}"></span> {title}</h4><ul>'
        for item in INVEST[key]: h+=f'<li>{item}</li>'
        h+='</ul></div>'
    return h


# ══════════════════════════════════════════════════════════════════════════════
# GENERATE FULL HTML
# ══════════════════════════════════════════════════════════════════════════════

overview_money_html = gen_overview_section("NVIDIA의 주요 수입원", "돈을 버는 방법", OVERVIEW_MONEY, "linear-gradient(135deg,#1a3a00,#2d5a00)")
overview_growth_html = gen_overview_section("인공지능과 차세대 컴퓨팅", "미래 성장 동력", OVERVIEW_GROWTH, "linear-gradient(135deg,#0a2a4a,#1a3a5a)")
overview_risks_html = gen_overview_section("변화하는 환경과 새로운 도전들", "주의해야 할 점", OVERVIEW_RISKS, "linear-gradient(135deg,#3a2a00,#4a3500)")

financial_html = gen_financial_section(FINANCIAL_ITEMS)
quarterly_financial_html = gen_financial_section(QUARTERLY_FINANCIAL_ITEMS)

# Earnings charts
earnings_rev_chart = svg_earnings_compare(EARNINGS_QUARTERS)
earnings_eps_chart = svg_eps_surprise(EARNINGS_QUARTERS)
earnings_cards_html = earnings_call_cards()
next_earn_html = next_earnings_card()

p = PROFILE
chg_cls = "down"
chg_sign = ""

html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>StockLens — NVDA 종합분석</title>
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
:root{{--bg:#050508;--card:rgba(255,255,255,.03);--card2:rgba(255,255,255,.06);--card-solid:#0d0d12;--border:rgba(255,255,255,.06);--border-hover:rgba(118,185,0,.25);--text:#eaedf3;--text2:#7a7f96;--accent:#76b900;--accent-dim:rgba(118,185,0,.12);--red:#f87171;--blue:#60a5fa;--purple:#a78bfa;--orange:#fb923c;--green:#76b900;--radius:1.25rem;--radius-sm:0.75rem;--spring:cubic-bezier(0.16,1,0.3,1)}}
*{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{font-family:'Pretendard Variable',Pretendard,-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100dvh;word-break:keep-all;-webkit-font-smoothing:antialiased}}

/* Noise overlay */
body::before{{content:'';position:fixed;inset:0;z-index:60;pointer-events:none;background:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='256' height='256' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");opacity:.35}}

/* Mesh gradient background */
body::after{{content:'';position:fixed;top:-40%;left:-20%;width:80%;height:80%;background:radial-gradient(ellipse at center,rgba(118,185,0,.06) 0%,transparent 70%);z-index:-1;pointer-events:none;animation:meshFloat 20s ease-in-out infinite alternate}}
@keyframes meshFloat{{0%{{transform:translate(0,0) scale(1)}}100%{{transform:translate(5%,8%) scale(1.1)}}}}

/* Scroll reveal */
@keyframes fadeInUp{{from{{opacity:0;transform:translateY(1.5rem);filter:blur(4px)}}to{{opacity:1;transform:translateY(0);filter:blur(0)}}}}
.reveal{{opacity:0;transform:translateY(1.5rem);filter:blur(4px)}}.reveal.visible{{animation:fadeInUp .7s var(--spring) forwards}}

/* Floating glass header */
.hdr{{position:sticky;top:0;z-index:40;backdrop-filter:blur(24px) saturate(1.8);-webkit-backdrop-filter:blur(24px) saturate(1.8);background:rgba(5,5,8,.7);border-bottom:1px solid var(--border);padding:14px 32px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}}
.logo{{font-size:20px;font-weight:800;letter-spacing:-.5px;color:var(--accent);font-family:'Geist Mono',monospace}}.logo span{{color:var(--text2);font-weight:400;font-size:13px;margin-left:10px;font-family:'Pretendard Variable',sans-serif}}

/* Update Info Bar */
.update-bar{{background:linear-gradient(90deg,rgba(118,185,0,.06),rgba(78,205,196,.04));border-bottom:1px solid var(--border);padding:10px 32px;display:flex;align-items:center;gap:24px;flex-wrap:wrap;font-size:12px;color:var(--text2)}}
.ub-item{{display:flex;align-items:center;gap:6px}}.ub-icon{{font-size:14px}}
.ub-label{{color:var(--text2);opacity:.7}}.ub-value{{color:var(--text);font-weight:600;font-family:'Geist Mono',monospace}}
.ub-next{{margin-left:auto;background:rgba(255,165,0,.1);border:1px solid rgba(255,165,0,.25);border-radius:20px;padding:5px 14px;color:#ffa500;font-weight:700;font-size:11px;display:flex;align-items:center;gap:6px;white-space:nowrap}}
.ub-next .ub-blink{{display:inline-block;width:6px;height:6px;border-radius:50%;background:#ffa500;animation:blink 1.5s infinite}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:.3}}}}
@media(max-width:768px){{.update-bar{{padding:8px 16px;gap:12px;font-size:11px}}.ub-next{{margin-left:0;width:100%;justify-content:center}}}}

/* Tabs — glass pill */
.tabs{{display:flex;gap:2px;padding:12px 32px;background:rgba(5,5,8,.55);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border-bottom:1px solid var(--border);overflow-x:auto;position:sticky;top:52px;z-index:39}}
.tab{{padding:10px 22px;cursor:pointer;color:var(--text2);font-size:13px;font-weight:600;border-radius:999px;white-space:nowrap;transition:all .5s var(--spring);border:1px solid transparent}}
.tab:hover{{color:var(--text);background:rgba(255,255,255,.04)}}.tab.active{{color:#fff;background:var(--accent-dim);border-color:rgba(118,185,0,.2)}}
.main{{max-width:1200px;margin:0 auto;padding:32px 32px 64px}}
.tc{{display:none}}.tc.active{{display:block}}

/* Company Header — glass bezel */
.ch{{display:flex;align-items:center;gap:24px;margin-bottom:32px;padding:28px;background:var(--card);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border:1px solid var(--border);border-radius:var(--radius);position:relative;overflow:hidden}}
.ch::before{{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(118,185,0,.3),transparent)}}
.ch-tk{{font-size:40px;font-weight:900;letter-spacing:-2px;color:var(--accent);font-family:'Geist Mono',monospace}}.ch-nm{{font-size:17px;font-weight:600}}.ch-desc{{font-size:13px;color:var(--text2);margin-top:6px;max-width:700px;line-height:1.7}}
.ch-meta{{margin-left:auto;text-align:right}}.ch-price{{font-size:36px;font-weight:800;letter-spacing:-1.5px;font-family:'Geist Mono',monospace}}.ch-chg{{font-size:14px;margin-top:6px;font-weight:600}}

/* KPIs — glass bezel cards */
.kpi-row{{display:grid;grid-template-columns:repeat(auto-fit,minmax(175px,1fr));gap:14px;margin-bottom:28px}}
.kpi{{background:var(--card);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border:1px solid var(--border);border-radius:var(--radius);padding:22px;position:relative;overflow:hidden;transition:all .5s var(--spring)}}
.kpi::before{{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--accent),transparent);opacity:.5}}
.kpi:hover{{transform:translateY(-3px);box-shadow:0 12px 40px rgba(118,185,0,.08);border-color:var(--border-hover)}}
.kpi-l{{font-size:11px;color:var(--text2);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;font-weight:500}}
.kpi-v{{font-size:28px;font-weight:800;letter-spacing:-1px;font-family:'Geist Mono',monospace}}.kpi-s{{font-size:12px;margin-top:8px;font-weight:500}}
.up{{color:var(--green)}}.down{{color:var(--red)}}

/* Sub-tabs — glass pill switch */
.sub-tabs{{display:inline-flex;background:rgba(255,255,255,.04);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1px solid var(--border);border-radius:999px;padding:4px;margin-bottom:28px;gap:4px}}
.sub-tab{{padding:9px 24px;cursor:pointer;color:var(--text2);font-size:13px;font-weight:600;border-radius:999px;transition:all .5s var(--spring);user-select:none}}
.sub-tab:hover{{color:var(--text)}}.sub-tab.active{{background:var(--accent);color:#fff;box-shadow:0 4px 20px rgba(118,185,0,.25)}}
.sub-pane{{display:none}}.sub-pane.active{{display:block}}

/* Section Cards — double-bezel glass */
.section-card{{background:rgba(255,255,255,.02);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1px solid var(--border);border-radius:var(--radius);margin-bottom:28px;overflow:hidden;transition:all .5s var(--spring)}}
.section-card:hover{{border-color:var(--border-hover);box-shadow:0 16px 48px rgba(0,0,0,.2)}}
.section-header{{padding:36px 32px;text-align:center;position:relative}}
.section-header::after{{content:'';position:absolute;bottom:0;left:10%;right:10%;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.08),transparent)}}
.section-subtitle{{font-size:11px;color:rgba(255,255,255,.45);margin-bottom:10px;letter-spacing:2px;text-transform:uppercase;font-weight:500}}
.section-title{{font-size:22px;font-weight:800;color:#fff;letter-spacing:-.5px;text-wrap:balance}}
.section-body{{padding:12px 28px 28px}}
.insight-item{{padding:28px 16px;border-bottom:1px solid rgba(255,255,255,.04);transition:all .5s var(--spring);border-radius:var(--radius-sm);margin:0 -16px}}
.insight-item:hover{{background:rgba(118,185,0,.03)}}
.insight-item:last-child{{border-bottom:none}}
.insight-header{{display:flex;align-items:center;gap:12px;margin-bottom:14px}}
.insight-emoji{{font-size:24px}}
.insight-title{{font-size:17px;font-weight:700;color:var(--text);letter-spacing:-.3px}}
.insight-desc{{font-size:15px;color:var(--text2);line-height:1.85}}

/* Financial Items — glass card */
.fin-category{{margin-bottom:36px}}
.fin-cat-title{{font-size:11px;color:var(--text2);text-transform:uppercase;letter-spacing:3px;margin-bottom:20px;padding-bottom:10px;border-bottom:1px solid var(--border);font-weight:500}}
.fin-item{{background:var(--card);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1px solid var(--border);border-radius:var(--radius);padding:28px;margin-bottom:18px;transition:all .5s var(--spring);position:relative;overflow:hidden}}
.fin-item::before{{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.06),transparent)}}
.fin-item:hover{{transform:translateY(-3px);box-shadow:0 12px 36px rgba(0,0,0,.2);border-color:var(--border-hover)}}
.fin-item-label{{font-size:12px;color:var(--text2);margin-bottom:10px;font-weight:500}}
.fin-item-headline{{font-size:17px;font-weight:700;margin-bottom:18px;display:flex;align-items:center;gap:10px;line-height:1.5;letter-spacing:-.3px}}
.fin-emoji{{font-size:22px}}
.fin-metric-row{{display:flex;align-items:center;justify-content:space-between;background:rgba(255,255,255,.04);border:1px solid var(--border);border-radius:var(--radius-sm);padding:16px 22px;margin-bottom:18px}}
.fin-metric-value{{font-size:26px;font-weight:800;letter-spacing:-1px;font-family:'Geist Mono',monospace}}
.fin-metric-change{{font-size:14px;font-weight:700;font-family:'Geist Mono',monospace}}
.fin-item-desc{{font-size:15px;color:var(--text2);line-height:1.85}}
.src-badge{{font-size:10px;padding:3px 10px;border-radius:999px;margin-left:8px;font-weight:600;vertical-align:middle}}
.src-badge.verified{{background:var(--accent-dim);color:#76b900}}
.src-badge.estimate{{background:rgba(251,146,60,.12);color:#fb923c}}
.guidance-card{{background:linear-gradient(135deg,rgba(118,185,0,.06),rgba(118,185,0,.01));border:1px solid rgba(118,185,0,.15);border-radius:var(--radius);padding:28px;margin-bottom:28px;backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px)}}
.guidance-title{{font-size:17px;font-weight:700;margin-bottom:18px;display:flex;align-items:center;gap:10px;color:var(--accent);letter-spacing:-.3px}}
.guidance-grid{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px}}
.guidance-item{{text-align:center}}
.guidance-item .g-label{{font-size:11px;color:var(--text2);margin-bottom:6px;text-transform:uppercase;letter-spacing:1px;font-weight:500}}
.guidance-item .g-value{{font-size:24px;font-weight:800;font-family:'Geist Mono',monospace}}
.data-note{{background:rgba(255,255,255,.03);border:1px solid var(--border);border-radius:var(--radius-sm);padding:16px 20px;margin-bottom:28px;font-size:12px;color:var(--text2);line-height:1.8;display:flex;align-items:flex-start;gap:12px}}
.data-note-icon{{font-size:16px;flex-shrink:0}}

/* Charts & Tables — glass containers */
.cg{{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-bottom:28px}}
.cc{{background:var(--card);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1px solid var(--border);border-radius:var(--radius);padding:24px;transition:all .5s var(--spring);position:relative;overflow:hidden}}
.cc::before{{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.05),transparent)}}
.cc:hover{{border-color:var(--border-hover);box-shadow:0 8px 32px rgba(0,0,0,.15)}}.cc.full{{grid-column:1/-1}}
.ct{{font-size:15px;font-weight:700;margin-bottom:18px;display:flex;align-items:center;gap:10px;letter-spacing:-.2px}}
.badge{{font-size:10px;background:var(--accent-dim);color:var(--accent);padding:3px 10px;border-radius:999px;font-weight:600;letter-spacing:.5px}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th{{background:rgba(255,255,255,.04);color:var(--text2);padding:14px 18px;text-align:left;font-weight:600;white-space:nowrap;border-bottom:1px solid var(--border);font-size:11px;text-transform:uppercase;letter-spacing:1px}}
td{{padding:14px 18px;border-bottom:1px solid rgba(255,255,255,.03);white-space:nowrap;transition:background .3s var(--spring)}}
tr:nth-child(even) td{{background:rgba(255,255,255,.015)}}
tr:hover td{{background:rgba(118,185,0,.04)}}
.nr{{text-align:right;font-variant-numeric:tabular-nums;font-family:'Geist Mono',monospace}}.tw{{overflow-x:auto}}

/* Invest cards — glass bezel */
.ig{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}
.invest-card{{background:var(--card);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1px solid var(--border);border-radius:var(--radius);padding:28px;transition:all .5s var(--spring);position:relative;overflow:hidden}}
.invest-card::before{{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.06),transparent)}}
.invest-card:hover{{transform:translateY(-3px);box-shadow:0 12px 36px rgba(0,0,0,.2);border-color:var(--border-hover)}}
.invest-card h4{{font-size:15px;margin-bottom:14px;display:flex;align-items:center;gap:10px;font-weight:700}}
.invest-card ul{{list-style:none;padding:0}}.invest-card li{{padding:10px 0;color:var(--text2);font-size:13px;line-height:1.7;border-bottom:1px solid rgba(255,255,255,.04)}}
.invest-card li:last-child{{border:none}}
.dot{{width:8px;height:8px;border-radius:50%;display:inline-block}}.dot-green{{background:var(--green)}}.dot-red{{background:var(--red)}}.dot-blue{{background:var(--blue)}}.dot-orange{{background:var(--orange)}}

/* Earnings Tab */
.next-earn{{background:linear-gradient(135deg,rgba(118,185,0,.08),rgba(78,205,196,.05));backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1px solid rgba(118,185,0,.2);border-radius:var(--radius);padding:28px;position:relative;overflow:hidden}}
.next-earn::before{{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--accent),#4ecdc4)}}
.next-earn-header{{display:flex;align-items:center;gap:16px;margin-bottom:20px;flex-wrap:wrap}}
.next-earn-icon{{font-size:28px}}
.next-earn-title{{font-size:18px;font-weight:800;color:var(--text)}}
.next-earn-date{{font-size:13px;color:var(--accent);font-weight:600;margin-top:2px}}
.next-earn-countdown{{margin-left:auto;background:var(--accent);color:#000;font-weight:800;font-size:14px;padding:6px 16px;border-radius:20px;font-family:'Geist Mono',monospace}}
.next-earn-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:16px;margin-bottom:20px}}
.next-earn-item{{background:rgba(255,255,255,.03);border:1px solid var(--border);border-radius:12px;padding:16px;text-align:center}}
.ne-label{{font-size:11px;color:var(--text2);text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px}}
.ne-value{{font-size:18px;font-weight:800;color:var(--text);font-family:'Geist Mono',monospace}}
.ne-sub{{font-size:11px;color:var(--text2);margin-top:4px}}
.next-earn-watch{{background:rgba(255,255,255,.02);border:1px solid var(--border);border-radius:12px;padding:20px}}
.ne-watch-title{{font-size:14px;font-weight:700;margin-bottom:12px;color:var(--text)}}
.next-earn-watch ul{{list-style:none;padding:0;margin:0}}.next-earn-watch li{{padding:8px 0;color:var(--text2);font-size:13px;line-height:1.6;border-bottom:1px solid rgba(255,255,255,.04);padding-left:16px;position:relative}}
.next-earn-watch li::before{{content:'▸';position:absolute;left:0;color:var(--accent)}}
.next-earn-watch li:last-child{{border:none}}

.earn-card{{background:var(--card);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1px solid var(--border);border-radius:var(--radius);padding:24px;margin-bottom:20px;transition:all .5s var(--spring);position:relative;overflow:hidden}}
.earn-card::before{{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.06),transparent)}}
.earn-card:hover{{transform:translateY(-2px);box-shadow:0 12px 36px rgba(0,0,0,.2);border-color:var(--border-hover)}}
.earn-header{{display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin-bottom:14px}}
.earn-q{{font-size:18px;font-weight:800;color:var(--text)}}
.earn-date{{font-size:12px;color:var(--text2)}}
.earn-surprise{{margin-left:auto;font-size:13px;font-weight:700;padding:4px 14px;border-radius:20px;font-family:'Geist Mono',monospace}}
.earn-surprise.up{{background:rgba(118,185,0,.12);color:var(--green)}}
.earn-surprise.down{{background:rgba(255,107,107,.12);color:var(--red)}}
.earn-badges{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px}}
.earn-badge{{background:rgba(255,255,255,.05);border:1px solid var(--border);border-radius:20px;padding:4px 12px;font-size:11px;color:var(--text2)}}
.earn-metrics{{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:12px;margin-bottom:18px}}
.earn-metric{{background:rgba(255,255,255,.02);border:1px solid var(--border);border-radius:10px;padding:14px;text-align:center}}
.earn-metric-label{{font-size:10px;color:var(--text2);text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px}}
.earn-metric-val{{font-size:18px;font-weight:800;color:var(--text);font-family:'Geist Mono',monospace}}
.earn-metric-val.up{{color:var(--green)}}.earn-metric-val.down{{color:var(--red)}}
.earn-metric-sub{{font-size:10px;color:var(--text2);margin-top:3px;font-family:'Geist Mono',monospace}}
.earn-ceo{{background:rgba(118,185,0,.04);border:1px solid rgba(118,185,0,.12);border-radius:12px;padding:18px;margin-bottom:16px}}
.earn-ceo-label{{font-size:12px;font-weight:700;color:var(--accent);margin-bottom:8px}}
.earn-ceo-quote{{font-size:13px;color:var(--text2);line-height:1.8;font-style:italic}}
.earn-highlights{{margin-bottom:16px}}
.earn-hl-title{{font-size:13px;font-weight:700;color:var(--text);margin-bottom:10px}}
.earn-highlights ul{{list-style:none;padding:0;margin:0}}.earn-highlights li{{padding:7px 0;color:var(--text2);font-size:13px;line-height:1.7;border-bottom:1px solid rgba(255,255,255,.04);padding-left:16px;position:relative}}
.earn-highlights li::before{{content:'•';position:absolute;left:0;color:var(--accent)}}
.earn-highlights li:last-child{{border:none}}
.earn-analyst{{background:rgba(78,205,196,.04);border:1px solid rgba(78,205,196,.12);border-radius:12px;padding:18px}}
.earn-analyst-title{{font-size:13px;font-weight:700;color:#4ecdc4;margin-bottom:8px}}
.earn-analyst p{{font-size:13px;color:var(--text2);line-height:1.8;margin:0}}

/* Watermark & SVG */
.wm{{text-align:center;padding:48px 32px;color:rgba(255,255,255,.15);font-size:12px;letter-spacing:.5px;line-height:1.8}}
svg{{width:100%;height:auto;display:block}}

/* Responsive */
@media(max-width:768px){{
  .cg,.ig{{grid-template-columns:1fr}}
  .ch{{flex-direction:column;text-align:center;gap:16px}}.ch-meta{{margin-left:0;text-align:center}}
  .kpi-row{{grid-template-columns:repeat(2,1fr)}}
  .main{{padding:20px 16px 48px}}
  .tabs{{padding:10px 16px;top:48px}}
  .hdr{{padding:12px 16px}}
  .tab{{padding:8px 16px;font-size:12px}}
  .guidance-grid{{grid-template-columns:1fr}}
  .fin-metric-row{{flex-direction:column;align-items:flex-start;gap:8px}}
  .section-header{{padding:28px 20px}}
  .section-title{{font-size:19px}}
  .insight-item{{padding:20px 12px;margin:0 -12px}}
  .sub-tabs{{margin-bottom:20px}}
  .kpi-v{{font-size:22px}}.ch-price{{font-size:28px}}.ch-tk{{font-size:32px}}
}}
</style>
</head>
<body>

<div class="hdr">
  <div class="logo">StockLens <span>기업 종합분석</span></div>
</div>

<div class="update-bar">
  <div class="ub-item"><span class="ub-icon">📊</span><span class="ub-label">작성기준일</span><span class="ub-value">{DASHBOARD_META["created_date"]}</span></div>
  <div class="ub-item"><span class="ub-icon">📋</span><span class="ub-label">데이터</span><span class="ub-value">{DASHBOARD_META["data_basis"]}</span></div>
  <div class="ub-next"><span class="ub-blink"></span> {DASHBOARD_META["next_update_ticker"]} {DASHBOARD_META["next_update_date"]} {DASHBOARD_META["next_update_event"]} 이후 업데이트 필요</div>
</div>

<div class="tabs" id="tabBar">
  <div class="tab active" onclick="st('overview')">기업 개요</div>
  <div class="tab" onclick="st('financial')">재무 분석</div>
  <div class="tab" onclick="st('segments')">사업부문</div>
  <div class="tab" onclick="st('valuation')">밸류에이션</div>
  <div class="tab" onclick="st('earnings')">실적발표</div>
  <div class="tab" onclick="st('invest')">투자 포인트</div>
</div>

<div class="main">

<!-- ===== Company Header (shown on all tabs) ===== -->
<div class="ch">
  <div>
    <div class="ch-tk">NVDA</div>
    <div class="ch-nm">{p["name"]}</div>
    <div class="ch-desc">{p["desc"]}</div>
    <div style="margin-top:8px;font-size:12px;color:var(--text2);">{p["exchange"]} | {p["sector"]} | {p["industry"]} | {p["country"]}</div>
  </div>
  <div class="ch-meta">
    <div class="ch-price">${p["price"]}</div>
    <div class="ch-chg {chg_cls}">{p["changes"]} ({p["changesPct"]}%)</div>
    <div style="font-size:12px;color:var(--text2);margin-top:8px;">52주: {p["range"]}</div>
  </div>
</div>

<!-- ===== TAB 1: 기업 개요 ===== -->
<div class="tc active" id="t-overview">
  <div class="reveal">{overview_money_html}</div>
  <div class="reveal">{overview_growth_html}</div>
  <div class="reveal">{overview_risks_html}</div>
</div>

<!-- ===== TAB 2: 재무 분석 ===== -->
<div class="tc" id="t-financial">

  <!-- Data Source Note -->
  <div class="data-note reveal">
    <div class="data-note-icon">📋</div>
    <div>FY2026(2025.02~2026.01) 실적은 NVIDIA IR 공시(2026.02.25) 기반으로 검증되었습니다. <span class="src-badge verified">IR 공시</span> 마크가 있는 항목은 공식 발표 수치이며, <span class="src-badge estimate">추정치</span>는 과거 10-K 기반 추정입니다.</div>
  </div>

  <!-- Q1 FY2027 Guidance -->
  <div class="guidance-card reveal">
    <div class="guidance-title">📌 Q1 FY2027 가이던스 (2026.04~06)</div>
    <div class="guidance-grid">
      <div class="guidance-item"><div class="g-label">매출 가이던스</div><div class="g-value" style="color:var(--accent);">$78.0B</div><div style="font-size:11px;color:var(--text2);">±2% ($76.4~$79.6B)</div></div>
      <div class="guidance-item"><div class="g-label">매출총이익률</div><div class="g-value">74.9%</div><div style="font-size:11px;color:var(--text2);">GAAP 기준</div></div>
      <div class="guidance-item"><div class="g-label">애널리스트 컨센서스</div><div class="g-value" style="color:var(--accent);">93% 매수</div><div style="font-size:11px;color:var(--text2);">70명 중 | 목표가 $267</div></div>
    </div>
  </div>

  <!-- Sub-tabs: 연간 / 분기별 -->
  <div class="sub-tabs" id="finSubTabs">
    <div class="sub-tab active" onclick="sst('fin','annual')">연간</div>
    <div class="sub-tab" onclick="sst('fin','quarterly')">분기별</div>
  </div>

  <!-- === 연간 뷰 === -->
  <div class="sub-pane active" id="fin-annual">
    <!-- KPI Summary -->
    <div class="kpi-row reveal">
      <div class="kpi"><div class="kpi-l">시가총액</div><div class="kpi-v">{p["mktCap"]}</div><div class="kpi-s">Beta: {p["beta"]}</div></div>
      <div class="kpi"><div class="kpi-l">연간 매출</div><div class="kpi-v">$215.9B</div><div class="kpi-s up">+{rev_g:.1f}% YoY</div></div>
      <div class="kpi"><div class="kpi-l">연간 순이익</div><div class="kpi-v">$120.1B</div><div class="kpi-s up">+{ni_g:.1f}% YoY</div></div>
      <div class="kpi"><div class="kpi-l">EPS</div><div class="kpi-v">$4.90</div><div class="kpi-s">순이익률 55.6%</div></div>
      <div class="kpi"><div class="kpi-l">P/E (TTM)</div><div class="kpi-v">34.2</div><div class="kpi-s">PEG: 0.53</div></div>
      <div class="kpi"><div class="kpi-l">FCF Margin</div><div class="kpi-v">44.7%</div><div class="kpi-s">FCF: $96.6B</div></div>
    </div>

    <!-- Analyst Commentary -->
    {financial_html}

    <!-- Shareholder Return Section -->
    <div class="fin-category"><div class="fin-cat-title">주주환원</div>
    <div class="fin-item">
      <div class="fin-item-label">자사주 매입 + 배당 <span class="src-badge verified">IR 공시</span></div>
      <div class="fin-item-headline"><span class="fin-emoji">🎁</span> FY2026 총 $41.1B 주주환원 — FCF의 42.5%</div>
      <div class="fin-metric-row">
        <div class="fin-metric-value">$41.1B</div>
        <div class="fin-metric-change" style="color:var(--green)"><span style="font-size:11px;">&#9650;</span> 전년 대비 +61%</div>
      </div>
      <p class="fin-item-desc">자사주 매입 $40.1B + 배당금 $1.0B로 총 $41.1B을 주주에게 환원했어요. FCF($96.6B)의 42.5%에 해당하며, 나머지 58%는 전략적 유보입니다. 배당수익률은 0.02%로 미미하지만, 대규모 자사주 매입을 통해 유통주식 수를 꾸준히 줄이며 EPS 성장을 가속시키는 전략을 취하고 있어요.</p>
    </div>
    </div>

    <!-- Annual Charts -->
    <div class="cg reveal">
      <div class="cc"><div class="ct">매출 &amp; 순이익 추이 <span class="badge">연간</span></div>{rev_chart}</div>
      <div class="cc"><div class="ct">수익성 지표 추이 <span class="badge">마진율</span></div>{margin_chart}</div>
      <div class="cc"><div class="ct">R&amp;D &amp; CapEx 추이 <span class="badge">투자</span></div>{rnd_capex_chart}</div>
      <div class="cc"><div class="ct">영업CF &amp; FCF 추이 <span class="badge">현금흐름</span></div>{cashflow_chart}</div>
    </div>

    <!-- Annual Detailed Table -->
    <div class="cc"><div class="ct">연간 재무 데이터 <span class="badge">FY2022~2026</span></div><div class="tw">{fin_table()}</div></div>
  </div>

  <!-- === 분기별 뷰 === -->
  <div class="sub-pane" id="fin-quarterly">
    <!-- Quarterly KPIs (latest quarter) -->
    <div class="kpi-row reveal">
      <div class="kpi"><div class="kpi-l">Q4 매출</div><div class="kpi-v">$68.1B</div><div class="kpi-s up">+73.5% YoY</div></div>
      <div class="kpi"><div class="kpi-l">Q4 순이익</div><div class="kpi-v">$43.0B</div><div class="kpi-s up">+94.8% YoY</div></div>
      <div class="kpi"><div class="kpi-l">Q4 GPM</div><div class="kpi-v">75.0%</div><div class="kpi-s up">Q1 60.5% → Q4 75.0%</div></div>
      <div class="kpi"><div class="kpi-l">Q4 OPM</div><div class="kpi-v">66.5%</div><div class="kpi-s up">Q1 37.0% → Q4 66.5%</div></div>
      <div class="kpi"><div class="kpi-l">Q1→Q4 매출 성장</div><div class="kpi-v">+54.6%</div><div class="kpi-s">$44.1B → $68.1B</div></div>
      <div class="kpi"><div class="kpi-l">Q1 FY27 가이던스</div><div class="kpi-v">$78.0B</div><div class="kpi-s up">Q4 대비 +14.5%</div></div>
    </div>

    <!-- Quarterly Commentary -->
    {quarterly_financial_html}

    <!-- Quarterly Charts -->
    <div class="cg reveal">
      <div class="cc"><div class="ct">분기별 매출 &amp; 순이익 <span class="badge">Q1'25~Q4'26</span></div>{q_chart}</div>
      <div class="cc"><div class="ct">분기별 수익성 추이 <span class="badge">FY2026</span></div>{q_margin_chart}</div>
    </div>

    <!-- Quarterly Detailed Table -->
    <div class="cc"><div class="ct">분기별 재무 상세 <span class="badge">FY2026</span></div><div class="tw">{q_detail_table()}</div></div>
  </div>

</div>

<!-- ===== TAB 3: 사업부문 ===== -->
<div class="tc" id="t-segments">

  <!-- Sub-tabs: 연간 / 분기별 -->
  <div class="sub-tabs" id="segSubTabs">
    <div class="sub-tab active" onclick="sst('seg','annual')">연간</div>
    <div class="sub-tab" onclick="sst('seg','quarterly')">분기별</div>
  </div>

  <!-- === 연간 뷰 === -->
  <div class="sub-pane active" id="seg-annual">
    <div class="cg reveal">
      <div class="cc"><div class="ct">사업부문별 매출 비중 <span class="badge">FY2026</span></div>{donut_chart}</div>
      <div class="cc"><div class="ct">사업부문별 매출 추이 <span class="badge">FY2022~2026</span></div>{stacked_chart}</div>
      <div class="cc full reveal"><div class="ct">사업부문 연간 상세 데이터</div><div class="tw">{seg_table()}</div></div>
    </div>
  </div>

  <!-- === 분기별 뷰 === -->
  <div class="sub-pane" id="seg-quarterly">
    <div class="kpi-row reveal">
      <div class="kpi"><div class="kpi-l">Q4 Data Center</div><div class="kpi-v">$62.3B</div><div class="kpi-s up">+75% YoY</div></div>
      <div class="kpi"><div class="kpi-l">Q4 Gaming</div><div class="kpi-v">$3.7B</div><div class="kpi-s up">+47% YoY</div></div>
      <div class="kpi"><div class="kpi-l">Q4 Pro Viz</div><div class="kpi-v">$1.3B</div><div class="kpi-s up">+159% YoY</div></div>
      <div class="kpi"><div class="kpi-l">Q4 Automotive</div><div class="kpi-v">$604M</div><div class="kpi-s up">+6% YoY</div></div>
    </div>
    <div class="cg reveal">
      <div class="cc"><div class="ct">분기별 사업부문 비중 <span class="badge">Q4 FY2026</span></div>{q_seg_donut}</div>
      <div class="cc"><div class="ct">분기별 사업부문 추이 <span class="badge">FY2026</span></div>{q_seg_stacked}</div>
      <div class="cc full reveal"><div class="ct">분기별 사업부문 상세 데이터 <span class="badge">FY2026</span></div><div class="tw">{q_seg_table()}</div></div>
    </div>
  </div>

</div>

<!-- ===== TAB 4: 밸류에이션 ===== -->
<div class="tc" id="t-valuation">
  <div class="kpi-row reveal">
    <div class="kpi"><div class="kpi-l">P/E (TTM)</div><div class="kpi-v">{RATIOS["pe"]}</div></div>
    <div class="kpi"><div class="kpi-l">Forward P/E</div><div class="kpi-v">{RATIOS["fpe"]}</div></div>
    <div class="kpi"><div class="kpi-l">P/S</div><div class="kpi-v">{RATIOS["ps"]}</div></div>
    <div class="kpi"><div class="kpi-l">PEG</div><div class="kpi-v">{RATIOS["peg"]}</div></div>
    <div class="kpi"><div class="kpi-l">ROE</div><div class="kpi-v">{RATIOS["roe"]}</div></div>
    <div class="kpi"><div class="kpi-l">배당수익률</div><div class="kpi-v">{RATIOS["div"]}</div></div>
  </div>
  <div class="cg reveal">
    <div class="cc"><div class="ct">EPS 추이 &amp; PER 밴드 <span class="badge">연간</span></div>{eps_chart}</div>
    <div class="cc"><div class="ct">동종업계 P/E 비교</div><svg viewBox="0 0 580 200" xmlns="http://www.w3.org/2000/svg">{peer_pe_bars}</svg></div>
  </div>
  <div class="cc"><div class="ct">동종업계 밸류에이션 비교</div><div class="tw">{peer_table()}</div></div>
</div>

<!-- ===== TAB 5: 실적발표 ===== -->
<div class="tc" id="t-earnings">

  <!-- 다음 실적발표 예정 -->
  {next_earn_html}

  <!-- 실적 서프라이즈 KPI -->
  <div class="kpi-row reveal">
    <div class="kpi"><div class="kpi-l">4분기 연속</div><div class="kpi-v" style="color:var(--green)">EPS Beat</div><div class="kpi-s">Q1~Q4 FY2026 전 분기 상회</div></div>
    <div class="kpi"><div class="kpi-l">평균 EPS 서프라이즈</div><div class="kpi-v" style="color:var(--green)">+6.1%</div><div class="kpi-s">Non-GAAP 기준</div></div>
    <div class="kpi"><div class="kpi-l">평균 매출 서프라이즈</div><div class="kpi-v" style="color:var(--green)">+2.1%</div><div class="kpi-s">4분기 연속 Beat</div></div>
    <div class="kpi"><div class="kpi-l">누적 매출 (FY2026)</div><div class="kpi-v">$215.9B</div><div class="kpi-s">+65% YoY</div></div>
    <div class="kpi"><div class="kpi-l">FY2026 EPS</div><div class="kpi-v">$4.90</div><div class="kpi-s">GAAP 기준</div></div>
    <div class="kpi"><div class="kpi-l">다음 발표까지</div><div class="kpi-v" style="color:var(--accent)">D-60</div><div class="kpi-s">2026.05.27 (수)</div></div>
  </div>

  <!-- 실적 vs 컨센서스 비교 차트 -->
  <div class="cg reveal">
    <div class="cc"><div class="ct">분기별 매출: 실적 vs 컨센서스 <span class="badge">FY2026</span></div>{earnings_rev_chart}</div>
    <div class="cc"><div class="ct">분기별 EPS: 실적 vs 컨센서스 <span class="badge">Non-GAAP</span></div>{earnings_eps_chart}</div>
  </div>

  <!-- 분기별 컨퍼런스콜 요약 -->
  <div style="margin-top:4px;">
    {earnings_cards_html}
  </div>

</div>

<!-- ===== TAB 6: 투자 포인트 ===== -->
<div class="tc" id="t-invest"><div class="ig reveal">{invest_html()}</div></div>

</div><!-- end main -->

<div class="wm">StockLens Dashboard v13.0 | NVDA 종합분석 | 데이터: NVIDIA IR 공시 (FY2026 Q4, 2026.02.25) + 애널리스트 리포트 | 생성일: 2026.03.28<br>주요 출처: NVIDIA Newsroom, MacroTrends, FactSet Consensus | ⚠️ 투자 참고용이며 투자 권유가 아닙니다.</div>

<script>
var currentTab = 'overview';
function st(id) {{
  currentTab = id;
  var tabNames = ['overview','financial','segments','valuation','earnings','invest'];
  var tabs = document.querySelectorAll('.tab');
  for (var i = 0; i < tabs.length; i++) tabs[i].className = (i === tabNames.indexOf(id)) ? 'tab active' : 'tab';
  var panes = document.querySelectorAll('.tc');
  for (var i = 0; i < panes.length; i++) panes[i].className = (panes[i].id === 't-' + id) ? 'tc active' : 'tc';
}}
function sst(prefix, view) {{
  var containerId = prefix === 'fin' ? 'finSubTabs' : 'segSubTabs';
  var container = document.getElementById(containerId);
  var stabs = container.querySelectorAll('.sub-tab');
  for (var i = 0; i < stabs.length; i++) stabs[i].className = 'sub-tab';
  stabs[view === 'annual' ? 0 : 1].className = 'sub-tab active';
  var annualPane = document.getElementById(prefix + '-annual');
  var quarterlyPane = document.getElementById(prefix + '-quarterly');
  if (view === 'annual') {{
    annualPane.className = 'sub-pane active';
    quarterlyPane.className = 'sub-pane';
  }} else {{
    annualPane.className = 'sub-pane';
    quarterlyPane.className = 'sub-pane active';
  }}
}}
// Intersection Observer for scroll reveal animations
(function() {{
  var els = document.querySelectorAll('.reveal');
  if (!els.length) return;
  var observer = new IntersectionObserver(function(entries) {{
    entries.forEach(function(e) {{
      if (e.isIntersecting) {{
        e.target.classList.add('visible');
        observer.unobserve(e.target);
      }}
    }});
  }}, {{ threshold: 0.08, rootMargin: '0px 0px -40px 0px' }});
  els.forEach(function(el, i) {{
    el.style.animationDelay = (i * 60) + 'ms';
    observer.observe(el);
  }});
}})();
</script>
</body>
</html>'''

# Write to file
output_path = "/sessions/exciting-gracious-pasteur/mnt/자산 대시보드 제작/02-projects/2026.03.28 기업분석대시보드/output/기업분석_종합대시보드_v13_2026.03.28.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"v13 Dashboard generated: {output_path}")
print(f"File size: {len(html):,} bytes")
