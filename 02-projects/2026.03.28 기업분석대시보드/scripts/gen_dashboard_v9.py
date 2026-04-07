#!/usr/bin/env python3
"""v9: UI/UX improved analyst-style commentary dashboard for NVDA
- v8 기반 UI/콘텐츠 개선
- 세부설명 폰트 크기 14px → 15px
- YoY 변동 색상 정상화 (상승=초록, 하락=빨강)
- 카드/항목 호버 효과 추가
- KPI 카드 accent border-top 강조
- 테이블 가독성 개선 (짝수 행 배경, 헤더 스타일)
- 반응형 레이아웃 개선
"""
import math

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

def peer_table():
    h='<table><thead><tr><th>티커</th><th>기업명</th><th class="nr">시가총액</th><th class="nr">P/E</th><th class="nr">P/S</th><th class="nr">매출</th><th class="nr">순이익률</th></tr></thead><tbody>'
    for p in PEERS:
        bg=' style="background:rgba(118,185,0,.1);"' if p["hl"] else ''
        sym=f'<strong>{p["sym"]}</strong>' if p["hl"] else p["sym"]
        h+=f'<tr{bg}><td>{sym}</td><td>{p["name"]}</td><td class="nr">{p["mc"]}</td><td class="nr">{p["pe"]}</td><td class="nr">{p["ps"]}</td><td class="nr">{p["rev"]}</td><td class="nr">{p["nm"]}</td></tr>'
    return h+'</tbody></table>'

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

p = PROFILE
chg_cls = "down"
chg_sign = ""

html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>StockLens - NVDA 종합분석</title>
<style>
:root{{--bg:#0f1117;--card:#1a1d28;--card2:#232736;--border:#2d3148;--text:#e4e6f0;--text2:#9ca0b8;--accent:#76b900;--red:#ff6b6b;--blue:#4dabf7;--purple:#b197fc;--orange:#ffa94d;--green:#76b900;--radius:12px}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--text);min-height:100vh}}

/* Header */
.hdr{{background:linear-gradient(135deg,#1a1d28,#232736);padding:20px 32px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:16px;flex-wrap:wrap}}
.logo{{font-size:22px;font-weight:800;color:var(--accent)}}.logo span{{color:var(--text2);font-weight:400;font-size:14px;margin-left:8px}}

/* Tabs */
.tabs{{display:flex;gap:4px;padding:16px 32px 0;background:var(--card);border-bottom:1px solid var(--border);overflow-x:auto}}
.tab{{padding:12px 20px;cursor:pointer;color:var(--text2);font-size:13px;font-weight:600;border-bottom:2px solid transparent;white-space:nowrap;transition:all .15s}}
.tab:hover{{color:var(--text)}}.tab.active{{color:var(--accent);border-bottom-color:var(--accent)}}
.main{{max-width:1200px;margin:0 auto;padding:24px 32px}}
.tc{{display:none}}.tc.active{{display:block}}

/* Company Header */
.ch{{display:flex;align-items:center;gap:20px;margin-bottom:24px;padding:24px;background:var(--card);border:1px solid var(--border);border-radius:var(--radius);border-left:4px solid var(--accent)}}
.ch-tk{{font-size:36px;font-weight:900;color:var(--accent)}}.ch-nm{{font-size:18px}}.ch-desc{{font-size:13px;color:var(--text2);margin-top:4px;max-width:700px;line-height:1.5}}
.ch-meta{{margin-left:auto;text-align:right}}.ch-price{{font-size:32px;font-weight:800}}.ch-chg{{font-size:14px;margin-top:4px}}

/* KPIs */
.kpi-row{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px;margin-bottom:24px}}
.kpi{{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:20px;border-top:3px solid var(--accent);transition:transform .2s,box-shadow .2s}}
.kpi:hover{{transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.3)}}
.kpi-l{{font-size:11px;color:var(--text2);text-transform:uppercase;letter-spacing:1px;margin-bottom:8px}}
.kpi-v{{font-size:26px;font-weight:800;letter-spacing:-1px}}.kpi-s{{font-size:12px;margin-top:6px}}
.up{{color:var(--green)}}.down{{color:var(--red)}}

/* Section Cards (Overview style - 토스 스타일) */
.section-card{{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);margin-bottom:24px;overflow:hidden;transition:transform .2s,box-shadow .2s}}
.section-card:hover{{transform:translateY(-2px);box-shadow:0 8px 32px rgba(0,0,0,.25)}}
.section-header{{padding:32px 28px;text-align:center}}
.section-subtitle{{font-size:13px;color:rgba(255,255,255,.6);margin-bottom:8px;letter-spacing:1px}}
.section-title{{font-size:20px;font-weight:800;color:#fff}}
.section-body{{padding:8px 24px 24px}}
.insight-item{{padding:24px 0;border-bottom:1px dashed var(--border);transition:background .15s;border-radius:8px;padding-left:12px;padding-right:12px;margin:0 -12px}}
.insight-item:hover{{background:rgba(118,185,0,.03)}}
.insight-item:last-child{{border-bottom:none}}
.insight-header{{display:flex;align-items:center;gap:10px;margin-bottom:12px}}
.insight-emoji{{font-size:22px}}
.insight-title{{font-size:16px;font-weight:700;color:var(--text)}}
.insight-desc{{font-size:15px;color:var(--text2);line-height:1.75}}

/* Financial Items (재무 분석 - 토스 스타일) */
.fin-category{{margin-bottom:32px}}
.fin-cat-title{{font-size:12px;color:var(--text2);text-transform:uppercase;letter-spacing:2px;margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid var(--border)}}
.fin-item{{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:24px;margin-bottom:16px;transition:transform .2s,box-shadow .2s,border-color .2s}}
.fin-item:hover{{transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,0,0,.2);border-color:rgba(118,185,0,.3)}}
.fin-item-label{{font-size:12px;color:var(--text2);margin-bottom:8px}}
.fin-item-headline{{font-size:16px;font-weight:700;margin-bottom:16px;display:flex;align-items:center;gap:8px;line-height:1.4}}
.fin-emoji{{font-size:20px}}
.fin-metric-row{{display:flex;align-items:center;justify-content:space-between;background:var(--card2);border-radius:10px;padding:14px 20px;margin-bottom:16px}}
.fin-metric-value{{font-size:22px;font-weight:800;letter-spacing:-0.5px}}
.fin-metric-change{{font-size:14px;font-weight:700}}
.fin-item-desc{{font-size:15px;color:var(--text2);line-height:1.75}}
.src-badge{{font-size:10px;padding:2px 8px;border-radius:4px;margin-left:8px;font-weight:600;vertical-align:middle}}
.src-badge.verified{{background:rgba(118,185,0,.15);color:#76b900}}
.src-badge.estimate{{background:rgba(255,169,77,.15);color:#ffa94d}}
.guidance-card{{background:linear-gradient(135deg,rgba(118,185,0,.08),rgba(118,185,0,.02));border:1px solid rgba(118,185,0,.25);border-radius:var(--radius);padding:24px;margin-bottom:24px}}
.guidance-title{{font-size:16px;font-weight:700;margin-bottom:16px;display:flex;align-items:center;gap:8px;color:var(--accent)}}
.guidance-grid{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px}}
.guidance-item{{text-align:center}}
.guidance-item .g-label{{font-size:11px;color:var(--text2);margin-bottom:4px}}
.guidance-item .g-value{{font-size:22px;font-weight:800}}
.data-note{{background:var(--card2);border-radius:8px;padding:14px 18px;margin-bottom:24px;font-size:12px;color:var(--text2);line-height:1.7;display:flex;align-items:flex-start;gap:10px}}
.data-note-icon{{font-size:16px;flex-shrink:0}}

/* Charts & Tables */
.cg{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:24px}}
.cc{{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:20px;transition:box-shadow .2s}}.cc:hover{{box-shadow:0 4px 16px rgba(0,0,0,.15)}}.cc.full{{grid-column:1/-1}}
.ct{{font-size:15px;font-weight:700;margin-bottom:16px;display:flex;align-items:center;gap:8px}}
.badge{{font-size:11px;background:var(--card2);color:var(--text2);padding:2px 8px;border-radius:4px;font-weight:500}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th{{background:var(--card2);color:var(--text2);padding:12px 16px;text-align:left;font-weight:600;white-space:nowrap;border-bottom:2px solid var(--accent);font-size:12px;text-transform:uppercase;letter-spacing:0.5px}}
td{{padding:12px 16px;border-bottom:1px solid var(--border);white-space:nowrap}}
tr:nth-child(even) td{{background:rgba(35,39,54,.5)}}
tr:hover td{{background:rgba(118,185,0,.07)}}
.nr{{text-align:right;font-variant-numeric:tabular-nums}}.tw{{overflow-x:auto}}

/* Invest cards */
.ig{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.invest-card{{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:24px;transition:transform .2s,box-shadow .2s}}
.invest-card:hover{{transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,0,0,.2)}}
.invest-card h4{{font-size:15px;margin-bottom:12px;display:flex;align-items:center;gap:8px}}
.invest-card ul{{list-style:none;padding:0}}.invest-card li{{padding:8px 0;color:var(--text2);font-size:13px;line-height:1.6;border-bottom:1px solid var(--border)}}
.invest-card li:last-child{{border:none}}
.dot{{width:8px;height:8px;border-radius:50%;display:inline-block}}.dot-green{{background:var(--green)}}.dot-red{{background:var(--red)}}.dot-blue{{background:var(--blue)}}.dot-orange{{background:var(--orange)}}

/* Watermark & SVG */
.wm{{text-align:center;padding:32px;color:var(--border);font-size:12px}}
svg{{width:100%;height:auto;display:block}}

/* Responsive */
@media(max-width:768px){{
  .cg,.ig{{grid-template-columns:1fr}}
  .ch{{flex-direction:column;text-align:center}}.ch-meta{{margin-left:0;text-align:center}}
  .kpi-row{{grid-template-columns:repeat(2,1fr)}}
  .main{{padding:16px}}
  .tabs{{padding:12px 16px 0}}
  .tab{{padding:10px 14px;font-size:12px}}
  .guidance-grid{{grid-template-columns:1fr}}
  .fin-metric-row{{flex-direction:column;align-items:flex-start;gap:8px}}
  .section-header{{padding:24px 20px}}
  .section-title{{font-size:18px}}
  .insight-item{{padding-left:8px;padding-right:8px;margin:0 -8px}}
}}
</style>
</head>
<body>

<div class="hdr">
  <div class="logo">StockLens <span>기업 종합분석</span></div>
</div>

<div class="tabs" id="tabBar">
  <div class="tab active" onclick="st('overview')">기업 개요</div>
  <div class="tab" onclick="st('financial')">재무 분석</div>
  <div class="tab" onclick="st('segments')">사업부문</div>
  <div class="tab" onclick="st('valuation')">밸류에이션</div>
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
  {overview_money_html}
  {overview_growth_html}
  {overview_risks_html}
</div>

<!-- ===== TAB 2: 재무 분석 ===== -->
<div class="tc" id="t-financial">

  <!-- Data Source Note -->
  <div class="data-note">
    <div class="data-note-icon">📋</div>
    <div>FY2026(2025.02~2026.01) 실적은 NVIDIA IR 공시(2026.02.25) 기반으로 검증되었습니다. <span class="src-badge verified">IR 공시</span> 마크가 있는 항목은 공식 발표 수치이며, <span class="src-badge estimate">추정치</span>는 과거 10-K 기반 추정입니다.</div>
  </div>

  <!-- Q1 FY2027 Guidance -->
  <div class="guidance-card">
    <div class="guidance-title">📌 Q1 FY2027 가이던스 (2026.04~06)</div>
    <div class="guidance-grid">
      <div class="guidance-item"><div class="g-label">매출 가이던스</div><div class="g-value" style="color:var(--accent);">$78.0B</div><div style="font-size:11px;color:var(--text2);">±2% ($76.4~$79.6B)</div></div>
      <div class="guidance-item"><div class="g-label">매출총이익률</div><div class="g-value">74.9%</div><div style="font-size:11px;color:var(--text2);">GAAP 기준</div></div>
      <div class="guidance-item"><div class="g-label">애널리스트 컨센서스</div><div class="g-value" style="color:var(--accent);">93% 매수</div><div style="font-size:11px;color:var(--text2);">70명 중 | 목표가 $267</div></div>
    </div>
  </div>

  <!-- KPI Summary -->
  <div class="kpi-row">
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

  <!-- Charts -->
  <div class="cg">
    <div class="cc"><div class="ct">매출 &amp; 순이익 추이 <span class="badge">연간</span></div>{rev_chart}</div>
    <div class="cc"><div class="ct">수익성 지표 추이 <span class="badge">마진율</span></div>{margin_chart}</div>
    <div class="cc"><div class="ct">R&amp;D &amp; CapEx 추이 <span class="badge">투자</span></div>{rnd_capex_chart}</div>
    <div class="cc"><div class="ct">영업CF &amp; FCF 추이 <span class="badge">현금흐름</span></div>{cashflow_chart}</div>
    <div class="cc full"><div class="ct">분기별 매출 추이 <span class="badge">최근 8분기</span></div>{q_chart}</div>
  </div>

  <!-- Detailed Table -->
  <div class="cc"><div class="ct">연간 재무 데이터 <span class="badge">상세</span></div><div class="tw">{fin_table()}</div></div>
</div>

<!-- ===== TAB 3: 사업부문 ===== -->
<div class="tc" id="t-segments">
  <div class="cg">
    <div class="cc"><div class="ct">사업부문별 매출 비중 <span class="badge">FY2026</span></div>{donut_chart}</div>
    <div class="cc"><div class="ct">사업부문별 매출 추이 <span class="badge">연간</span></div>{stacked_chart}</div>
    <div class="cc full"><div class="ct">사업부문 상세 데이터</div><div class="tw">{seg_table()}</div></div>
  </div>
</div>

<!-- ===== TAB 4: 밸류에이션 ===== -->
<div class="tc" id="t-valuation">
  <div class="kpi-row">
    <div class="kpi"><div class="kpi-l">P/E (TTM)</div><div class="kpi-v">{RATIOS["pe"]}</div></div>
    <div class="kpi"><div class="kpi-l">Forward P/E</div><div class="kpi-v">{RATIOS["fpe"]}</div></div>
    <div class="kpi"><div class="kpi-l">P/S</div><div class="kpi-v">{RATIOS["ps"]}</div></div>
    <div class="kpi"><div class="kpi-l">PEG</div><div class="kpi-v">{RATIOS["peg"]}</div></div>
    <div class="kpi"><div class="kpi-l">ROE</div><div class="kpi-v">{RATIOS["roe"]}</div></div>
    <div class="kpi"><div class="kpi-l">배당수익률</div><div class="kpi-v">{RATIOS["div"]}</div></div>
  </div>
  <div class="cg">
    <div class="cc"><div class="ct">EPS 추이 &amp; PER 밴드 <span class="badge">연간</span></div>{eps_chart}</div>
    <div class="cc"><div class="ct">동종업계 P/E 비교</div><svg viewBox="0 0 580 200" xmlns="http://www.w3.org/2000/svg">{peer_pe_bars}</svg></div>
  </div>
  <div class="cc"><div class="ct">동종업계 밸류에이션 비교</div><div class="tw">{peer_table()}</div></div>
</div>

<!-- ===== TAB 5: 투자 포인트 ===== -->
<div class="tc" id="t-invest"><div class="ig">{invest_html()}</div></div>

</div><!-- end main -->

<div class="wm">StockLens Dashboard v9.0 | NVDA 종합분석 | 데이터: NVIDIA IR 공시 (FY2026 Q4, 2026.02.25) + 애널리스트 리포트 | 생성일: 2026.03.28<br>주요 출처: NVIDIA Newsroom, MacroTrends, FactSet Consensus | ⚠️ 투자 참고용이며 투자 권유가 아닙니다.</div>

<script>
var currentTab = 'overview';
function st(id) {{
  currentTab = id;
  var tabNames = ['overview','financial','segments','valuation','invest'];
  var tabs = document.querySelectorAll('.tab');
  for (var i = 0; i < tabs.length; i++) tabs[i].className = (i === tabNames.indexOf(id)) ? 'tab active' : 'tab';
  var panes = document.querySelectorAll('.tc');
  for (var i = 0; i < panes.length; i++) panes[i].className = (panes[i].id === 't-' + id) ? 'tc active' : 'tc';
}}
</script>
</body>
</html>'''

# Write to file
output_path = "/sessions/exciting-gracious-pasteur/mnt/자산 대시보드 제작/02-projects/2026.03.28 기업분석대시보드/output/기업분석_종합대시보드_v9_2026.03.28.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"v9 Dashboard generated: {output_path}")
print(f"File size: {len(html):,} bytes")
