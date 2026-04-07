#!/usr/bin/env python3
"""Portfolio Dashboard v1: 10종목 통합 포트폴리오 대시보드
NVDA, AAPL, MSFT, GOOGL, O, ABBV, PLTR, CRWV, IONQ, SMR
- 포트폴리오 요약 + 개별 종목 6탭 상세
"""
import math, os

DASHBOARD_META = {
    "created_date": "2026.03.28",
    "data_basis": "2026.03.28 기준 최신 공시 데이터",
    "data_source": "IR Newsroom, SEC Filings, FactSet Consensus, MacroTrends",
    "next_update_event": "Q1 FY2027 실적발표 (NVDA)",
    "next_update_date": "2026.05.28 (수) 한국시간",
    "next_update_ticker": "NVDA",
}

STOCKS = {
    "NVDA": {
        "profile": {
            "symbol": "NVDA",
            "name": "NVIDIA Corporation",
            "price": 167.52,
            "changes": -2.31,
            "changesPct": -1.36,
            "exchange": "NASDAQ",
            "sector": "Technology",
            "industry": "Semiconductors",
            "country": "US",
            "mktCap": 4.07,  # in trillions
            "beta": 2.37,
            "range": "86.62-212.19",
            "employees": 36000,
            "accent": "#76b900",
            "desc": "NVIDIA는 GPU(그래픽 처리 장치) 및 AI 컴퓨팅 플랫폼의 글로벌 리더입니다.",
        },
        "income": [
            {"year": 2022, "rev": 26.91, "ni": 9.75, "oi": 10.04, "gp": 17.48, "eps": 0.39, "gm": 64.93, "om": 37.31, "nm": 36.23, "rnd": 7.34, "capex": 0.98, "ocf": 9.11, "fcf": 8.13},
            {"year": 2023, "rev": 26.97, "ni": 4.37, "oi": 4.22, "gp": 15.36, "eps": 0.17, "gm": 56.93, "om": 15.66, "nm": 16.19, "rnd": 7.34, "capex": 1.83, "ocf": 5.64, "fcf": 3.81},
            {"year": 2024, "rev": 60.92, "ni": 29.76, "oi": 32.97, "gp": 44.30, "eps": 1.19, "gm": 72.72, "om": 54.12, "nm": 48.85, "rnd": 8.68, "capex": 1.07, "ocf": 28.09, "fcf": 27.02},
            {"year": 2025, "rev": 130.50, "ni": 72.88, "oi": 81.45, "gp": 97.86, "eps": 2.94, "gm": 74.99, "om": 62.42, "nm": 55.85, "rnd": 12.91, "capex": 3.23, "ocf": 64.09, "fcf": 60.86},
            {"year": 2026, "rev": 215.94, "ni": 120.07, "oi": 130.39, "gp": 153.46, "eps": 4.90, "gm": 71.07, "om": 60.38, "nm": 55.60, "rnd": 18.50, "capex": 6.04, "ocf": 102.72, "fcf": 96.58},
        ],
        "quarterly": [
            {"q": "Q1'26", "rev": 44.06, "ni": 18.78},
            {"q": "Q2'26", "rev": 46.70, "ni": 26.42},
            {"q": "Q3'26", "rev": 57.00, "ni": 31.90},
            {"q": "Q4'26", "rev": 68.13, "ni": 42.96},
        ],
        "extra": {},
        "segments": {
            "labels": ["FY2022", "FY2023", "FY2024", "FY2025", "FY2026"],
            "data": [
                {"name": "Data Center", "values": [10.6, 15.0, 47.5, 115.2, 193.7], "color": "#76b900"},
                {"name": "Gaming", "values": [12.5, 9.1, 10.4, 11.4, 16.0], "color": "#ffa94d"},
                {"name": "Pro Viz", "values": [2.1, 1.5, 1.6, 1.9, 3.2], "color": "#4ecdc4"},
                {"name": "Automotive", "values": [0.6, 0.9, 1.1, 1.7, 2.3], "color": "#b197fc"},
            ]
        },
        "quarterly_segments": {
            "labels": ["Q1'26", "Q2'26", "Q3'26", "Q4'26"],
            "data": [
                {"name": "Data Center", "values": [39.1, 41.1, 51.2, 62.3], "color": "#76b900"},
                {"name": "Gaming", "values": [3.8, 4.3, 4.3, 3.7], "color": "#ffa94d"},
                {"name": "Pro Viz", "values": [0.509, 0.601, 0.760, 1.3], "color": "#4ecdc4"},
                {"name": "Automotive", "values": [0.567, 0.586, 0.592, 0.604], "color": "#b197fc"},
            ]
        },
        "quarterly_detail": [
            {"q": "Q1'26", "gm": 60.5, "om": 37.0, "nm": 42.6, "note": "H20 재고충당 $4.5B"},
            {"q": "Q2'26", "gm": 72.4, "om": 58.2, "nm": 56.6, "note": "Blackwell 출하 시작"},
            {"q": "Q3'26", "gm": 73.4, "om": 63.1, "nm": 55.9, "note": "Blackwell 본격 양산"},
            {"q": "Q4'26", "gm": 75.0, "om": 66.5, "nm": 63.1, "note": "역대 최고 분기"},
        ],
        "quarterly_financial_items": [
            "Q1'26 $4.5B H20 재고충당으로 단기 마진 압박, 이후 회복",
            "Q2-Q4 Blackwell 본격 출하로 수익성 지속 개선",
            "연간 FCF $96.6B, 업계 최고 수준의 현금 창출력",
            "R&D 투자 $18.5B로 기술 우위 유지",
        ],
        "earnings_quarters": [
            {"q": "Q1 FY2026", "rev_actual": 44.06, "rev_est": 43.28, "rev_beat": 1.8, "eps": 0.81, "eps_est": 0.74, "eps_beat": 9.5, "reaction": -0.8},
            {"q": "Q2 FY2026", "rev_actual": 46.70, "rev_est": 46.20, "rev_beat": 1.1, "eps": 1.05, "eps_est": 1.01, "eps_beat": 4.0, "reaction": 2.1},
            {"q": "Q3 FY2026", "rev_actual": 57.00, "rev_est": 55.50, "rev_beat": 2.7, "eps": 1.30, "eps_est": 1.24, "eps_beat": 4.8, "reaction": 3.5},
            {"q": "Q4 FY2026", "rev_actual": 68.13, "rev_est": 66.21, "rev_beat": 2.9, "eps": 1.62, "eps_est": 1.53, "eps_beat": 5.9, "reaction": 4.2},
        ],
        "next_earnings": {
            "date": "2026.05.27",
            "period": "Q1 FY2027",
            "rev_guidance": "78.0B ±2%",
            "rev_consensus": "78.1B",
            "eps": "1.79",
        },
        "peers": [
            {"ticker": "NVDA", "mktCap": "4.07T", "pe": "34.2", "ps": "18.8", "rev": "$215.9B", "nm": "55.6%", "highlight": True},
            {"ticker": "AMD", "mktCap": "210B", "pe": "24.8", "ps": "7.1", "rev": "$28.1B", "nm": "22%", "highlight": False},
            {"ticker": "INTC", "mktCap": "97B", "pe": "-", "ps": "1.5", "rev": "$53.1B", "nm": "-1%", "highlight": False},
            {"ticker": "AVGO", "mktCap": "1.05T", "pe": "38.2", "ps": "16.2", "rev": "$62.0B", "nm": "37%", "highlight": False},
            {"ticker": "QCOM", "mktCap": "190B", "pe": "16.5", "ps": "4.3", "rev": "$42.2B", "nm": "27%", "highlight": False},
            {"ticker": "TSM", "mktCap": "870B", "pe": "22.1", "ps": "11.3", "rev": "$95.0B", "nm": "40%", "highlight": False},
        ],
        "ratios": {
            "pe": 34.18,
            "fpe": 20.19,
            "ps": 18.84,
            "peg": 0.53,
            "roe": 127.5,
            "div": 0.02,
        },
        "overview_money": [
            "FY2026 예상 매출 $215.9B, 전년 대비 65% 성장 — AI 수요 폭발",
            "순이익 $120.1B, 순이익률 55.6% — 업계 최고 수준의 수익성",
            "FCF $96.6B로 업계 최상위 현금 창출, 배당 및 자사주 매입 여력",
        ],
        "overview_growth": [
            "5년 매출 CAGR 53% (2022-2026), 순이익 CAGR 90% — 가파른 고성장",
            "Data Center 세그먼트 FY2026 $193.7B로 전체 매출의 90% 차지",
            "Blackwell 아키텍처 출하 본격화로 내년 성장 추진력 준비 완료",
        ],
        "overview_risks": [
            "PER 34배, PSR 18.8배로 매우 높은 밸류에이션 — 증익 기반 재평가 필수",
            "AMD, Intel, TSMC 등 경쟁사 신제품 출시로 점유율 잠식 가능성",
            "지정학적 리스크(중국 수출 규제)로 인한 성장 둔화 우려",
        ],
        "financial_items": [
            "순이익률 55.6%는 업계 이례적 수준, 대규모 설비투자 진행 중",
            "R&D 투자 비중 8.6%로 기술 경쟁력 강화에 집중",
            "Data Center 매출 비중 89.8%로 단일 세그먼트 집중도 높음",
            "자본집약적 사업으로 향후 capex 증가 추세 지속 예상",
        ],
        "invest": {
            "strengths": "AI 시대의 GPU 독점 공급자, 초고속 성장, 최상 수익성",
            "risks": "과도한 밸류에이션, 경쟁 심화, 지정학적 리스크",
            "opportunities": "AI 인프라 투자 초기 단계, Blackwell 초과 공급, 신흥 AI 칩 시장",
            "watchlist": "Q1 FY2027 가이던스, Data Center 수요 지속성, 경쟁사 제품 출시 일정",
        },
    },
    "AAPL": {
        "profile": {
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "price": 252.90,
            "changes": 3.45,
            "changesPct": 1.38,
            "exchange": "NASDAQ",
            "sector": "Technology",
            "industry": "Consumer Electronics",
            "country": "US",
            "mktCap": 3.70,
            "beta": 1.24,
            "range": "169.21-260.10",
            "employees": 164000,
            "accent": "#555555",
            "desc": "Apple은 iPhone, iPad, Mac 등 프리미엄 하드웨어와 서비스 생태계를 운영하는 세계 최대 기술 기업입니다.",
        },
        "income": [
            {"year": 2021, "rev": 365.82, "ni": 94.68, "oi": 108.95, "gp": 152.84, "eps": 6.15, "gm": 41.78, "om": 29.78, "nm": 25.88, "rnd": 21.91, "capex": 11.09, "ocf": 104.04, "fcf": 92.95},
            {"year": 2022, "rev": 394.33, "ni": 99.80, "oi": 119.44, "gp": 170.78, "eps": 6.11, "gm": 43.31, "om": 30.29, "nm": 25.31, "rnd": 26.25, "capex": 10.71, "ocf": 122.15, "fcf": 111.44},
            {"year": 2023, "rev": 383.29, "ni": 97.00, "oi": 114.30, "gp": 166.78, "eps": 6.13, "gm": 43.52, "om": 29.82, "nm": 25.31, "rnd": 29.92, "capex": 11.00, "ocf": 110.54, "fcf": 99.54},
            {"year": 2024, "rev": 391.04, "ni": 93.74, "oi": 123.22, "gp": 180.68, "eps": 6.08, "gm": 46.21, "om": 31.51, "nm": 23.97, "rnd": 31.37, "capex": 9.96, "ocf": 118.26, "fcf": 108.30},
            {"year": 2025, "rev": 420.50, "ni": 105.00, "oi": 132.50, "gp": 196.00, "eps": 7.10, "gm": 46.60, "om": 31.50, "nm": 24.97, "rnd": 32.50, "capex": 10.50, "ocf": 125.00, "fcf": 114.50},
        ],
        "quarterly": [
            {"q": "Q1'25(Oct-Dec24)", "rev": 124.30, "ni": 36.33},
            {"q": "Q2'25(Jan-Mar25)", "rev": 95.36, "ni": 24.78},
            {"q": "Q3'25(Apr-Jun25)", "rev": 94.88, "ni": 23.60},
            {"q": "Q4'25(Jul-Sep25)", "rev": 96.02, "ni": 23.85},
        ],
        "extra": {},
        "segments": {
            "labels": ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025"],
            "data": [
                {"name": "iPhone", "values": [191.97, 205.49, 200.58, 201.18, 210.0], "color": "#555555"},
                {"name": "Services", "values": [68.43, 78.13, 85.20, 96.17, 105.0], "color": "#34a853"},
                {"name": "Mac", "values": [35.19, 40.18, 29.36, 30.75, 34.0], "color": "#4285f4"},
                {"name": "iPad", "values": [31.86, 29.29, 28.30, 26.65, 30.0], "color": "#ffa94d"},
                {"name": "Wearables", "values": [38.37, 41.24, 39.85, 36.30, 41.5], "color": "#b197fc"},
            ]
        },
        "quarterly_segments": {
            "labels": ["Q1'25", "Q2'25", "Q3'25", "Q4'25"],
            "data": [
                {"name": "iPhone", "values": [69.14, 46.84, 44.50, 45.00], "color": "#555555"},
                {"name": "Services", "values": [26.34, 26.65, 26.50, 27.00], "color": "#34a853"},
                {"name": "Mac", "values": [8.99, 7.95, 8.50, 9.00], "color": "#4285f4"},
                {"name": "iPad", "values": [8.09, 6.40, 7.00, 7.50], "color": "#ffa94d"},
                {"name": "Wearables", "values": [11.75, 7.52, 8.38, 7.52], "color": "#b197fc"},
            ]
        },
        "quarterly_detail": [
            {"q": "Q1'25", "gm": 46.9, "om": 35.0, "nm": 29.2, "note": "iPhone 15 판매 호조"},
            {"q": "Q2'25", "gm": 46.6, "om": 30.6, "nm": 26.0, "note": "계절성 둔화, Services 성장 지속"},
            {"q": "Q3'25", "gm": 46.5, "om": 30.0, "nm": 24.9, "note": "M4 Mac 신제품 출시"},
            {"q": "Q4'25", "gm": 46.4, "om": 30.2, "nm": 24.8, "note": "AI 기능 기대감 상승"},
        ],
        "quarterly_financial_items": [
            "Q1 매출 호조로 순이익률 29.2%, 이후 계절성 둔화로 24-26% 유지",
            "Services 세그먼트 고마진(70%+), 매출 성장세 가속 추세",
            "iPhone 매출 비중 45-52%, 여전히 의존도 높음",
            "연간 FCF $114.5B로 주주환원(배당+자사주) 여력 충분",
        ],
        "earnings_quarters": [
            {"q": "Q1 FY2025", "rev_actual": 124.30, "rev_est": 124.00, "rev_beat": 0.2, "eps": 2.40, "eps_est": 2.35, "eps_beat": 2.1, "reaction": 0.5},
            {"q": "Q2 FY2025", "rev_actual": 95.36, "rev_est": 94.50, "rev_beat": 0.9, "eps": 1.65, "eps_est": 1.62, "eps_beat": 1.9, "reaction": 3.2},
            {"q": "Q3 FY2025", "rev_actual": 94.88, "rev_est": 90.0, "rev_beat": 5.4, "eps": 1.53, "eps_est": 1.49, "eps_beat": 2.7, "reaction": 1.5},
            {"q": "Q4 FY2025", "rev_actual": 96.02, "rev_est": 95.0, "rev_beat": 1.1, "eps": 1.58, "eps_est": 1.56, "eps_beat": 1.3, "reaction": 0.8},
        ],
        "next_earnings": {
            "date": "2026.04.30",
            "period": "Q2 FY2025(Jan-Mar)",
            "rev_guidance": "94.2B",
            "rev_consensus": "94.2B",
            "eps": "1.62",
        },
        "peers": [
            {"ticker": "AAPL", "mktCap": "3.70T", "pe": "32.34", "ps": "8.45", "rev": "$420.5B", "nm": "25.0%", "highlight": True},
            {"ticker": "MSFT", "mktCap": "2.76T", "pe": "22.90", "ps": "10.60", "rev": "$275B", "nm": "36.2%", "highlight": False},
            {"ticker": "GOOG", "mktCap": "3.32T", "pe": "26.01", "ps": "8.66", "rev": "$395B", "nm": "28.6%", "highlight": False},
            {"ticker": "AMZN", "mktCap": "2.15T", "pe": "33.0", "ps": "3.22", "rev": "$668B", "nm": "9.3%", "highlight": False},
            {"ticker": "META", "mktCap": "1.73T", "pe": "27.5", "ps": "11.51", "rev": "$165B", "nm": "36.0%", "highlight": False},
        ],
        "ratios": {
            "pe": 32.34,
            "fpe": 27.80,
            "ps": 8.45,
            "peg": 2.50,
            "roe": 145.0,
            "div": 0.46,
        },
        "overview_money": [
            "FY2025 순이익 $105.0B, 순이익률 25.0% — 안정적 고수익 비즈니스",
            "FCF $114.5B로 투자자 환원(배당+자사주) 연 50B+ 수준",
            "Services 세그먼트 매출 $105B로 30% 가까운 고마진 성장 동력",
        ],
        "overview_growth": [
            "5년 매출 CAGR 3.6% (2021-2025), 성숙 단계의 완만한 성장",
            "Services 연평균 11% 성장으로 매출 다각화 추진 중",
            "iPhone 매출 정체, AI 기능 도입으로 순환 상승 기대",
        ],
        "overview_risks": [
            "iPhone 매출 의존도 50%, 신제품 사이클에 따른 변동성",
            "중국 시장 비중 높음(15-20%), 지정학적 리스크 노출",
            "AI 전략이 후발이며 구체적 AI 모네타이제이션 전략 부족",
        ],
        "financial_items": [
            "순이익률 25% 수준 유지로 안정적, 마진 압박 요인 제한적",
            "R&D 투자 비중 7.7%로 보수적, 기술 경쟁 심화 시 위험",
            "수직 통합(반도체 설계 자체 수행) 진행 중, Apple Silicon 우위 지속",
            "강력한 현금 창출로 순부채 대신 순현금 자산 $70B+ 수준",
        ],
        "invest": {
            "strengths": "20억+ 활성 기기 생태계, Services 고마진 성장, 강력한 브랜드 충성도",
            "risks": "iPhone 매출 의존도 50%+, 중국 시장 리스크, AI 전략 후발",
            "opportunities": "Apple Intelligence AI 기능 확산, Vision Pro 성장, Services 가입자 확대",
            "watchlist": "iPhone 16 판매 추이, Services 성장률, AI 기능 채택률",
        },
    },
    "MSFT": {
        "profile": {
            "symbol": "MSFT",
            "name": "Microsoft Corporation",
            "price": 356.50,
            "changes": 5.20,
            "changesPct": 1.48,
            "exchange": "NASDAQ",
            "sector": "Technology",
            "industry": "Software—Infrastructure",
            "country": "US",
            "mktCap": 2.76,
            "beta": 0.93,
            "range": "344.79-468.35",
            "employees": 228000,
            "accent": "#00a4ef",
            "desc": "Microsoft는 Azure 클라우드, Office 365, Windows, LinkedIn, Xbox를 운영하는 글로벌 소프트웨어·클라우드 기업입니다.",
        },
        "income": [
            {"year": 2021, "rev": 168.09, "ni": 61.27, "oi": 69.92, "gp": 115.86, "eps": 8.05, "gm": 68.93, "om": 41.59, "nm": 36.45, "rnd": 20.72, "capex": 20.62, "ocf": 76.74, "fcf": 56.12},
            {"year": 2022, "rev": 198.27, "ni": 72.74, "oi": 83.38, "gp": 135.62, "eps": 9.65, "gm": 68.40, "om": 42.06, "nm": 36.69, "rnd": 24.51, "capex": 23.89, "ocf": 89.04, "fcf": 65.15},
            {"year": 2023, "rev": 211.91, "ni": 72.36, "oi": 88.52, "gp": 146.05, "eps": 9.68, "gm": 68.92, "om": 41.77, "nm": 34.15, "rnd": 27.20, "capex": 28.11, "ocf": 87.58, "fcf": 59.47},
            {"year": 2024, "rev": 245.12, "ni": 88.14, "oi": 109.43, "gp": 171.01, "eps": 11.80, "gm": 69.76, "om": 44.64, "nm": 35.96, "rnd": 29.51, "capex": 44.48, "ocf": 118.55, "fcf": 74.07},
            {"year": 2025, "rev": 275.00, "ni": 99.50, "oi": 120.00, "gp": 195.00, "eps": 13.50, "gm": 70.90, "om": 43.60, "nm": 36.18, "rnd": 32.00, "capex": 55.00, "ocf": 130.00, "fcf": 75.00},
        ],
        "quarterly": [
            {"q": "Q1 FY2025(Jul-Sep24)", "rev": 65.59, "ni": 24.67},
            {"q": "Q2 FY2025(Oct-Dec24)", "rev": 69.63, "ni": 24.11},
            {"q": "Q3 FY2025(Jan-Mar25)", "rev": 70.07, "ni": 25.80},
            {"q": "Q4 FY2025(Apr-Jun25)", "rev": 69.71, "ni": 24.92},
        ],
        "extra": {},
        "segments": {
            "labels": ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025"],
            "data": [
                {"name": "Intelligent Cloud", "values": [67.84, 75.25, 87.91, 105.36, 125.0], "color": "#00a4ef"},
                {"name": "Productivity", "values": [53.92, 63.36, 69.27, 73.12, 80.0], "color": "#4ecdc4"},
                {"name": "Personal Computing", "values": [54.09, 59.66, 54.73, 66.64, 70.0], "color": "#ffa94d"},
            ]
        },
        "quarterly_segments": {
            "labels": ["Q1'25", "Q2'25", "Q3'25", "Q4'25"],
            "data": [
                {"name": "Intelligent Cloud", "values": [24.09, 25.54, 26.75, 28.00], "color": "#00a4ef"},
                {"name": "Productivity", "values": [20.32, 21.87, 22.50, 23.00], "color": "#4ecdc4"},
                {"name": "Personal Computing", "values": [13.18, 14.22, 14.82, 15.00], "color": "#ffa94d"},
            ]
        },
        "quarterly_detail": [
            {"q": "Q1'25", "gm": 69.4, "om": 47.2, "nm": 37.6, "note": "Azure 매출 고성장 지속"},
            {"q": "Q2'25", "gm": 69.0, "om": 45.5, "nm": 34.6, "note": "Capex 투자 확대로 단기 마진 압박"},
            {"q": "Q3'25", "gm": 69.5, "om": 45.0, "nm": 36.8, "note": "Copilot 수익화 진행"},
            {"q": "Q4'25", "gm": 69.8, "om": 44.0, "nm": 35.8, "note": "AI 인프라 투자 지속"},
        ],
        "quarterly_financial_items": [
            "Intelligent Cloud(Azure) 분기 성장률 20%+ 유지, 주요 성장 동력",
            "Capex 연 $55B 투자로 AI 인프라 구축 가속, 수익성 단기 압박",
            "Productivity(Office 365) 안정적 성장, 높은 마진율 유지",
            "FCF $75B로 배당 및 자사주 매입 여력 확보",
        ],
        "earnings_quarters": [
            {"q": "Q1 FY2025", "rev_actual": 65.59, "rev_est": 64.50, "rev_beat": 1.7, "eps": 3.30, "eps_est": 3.10, "eps_beat": 6.5, "reaction": 2.1},
            {"q": "Q2 FY2025", "rev_actual": 69.63, "rev_est": 68.81, "rev_beat": 1.2, "eps": 3.23, "eps_est": 3.12, "eps_beat": 3.5, "reaction": -1.5},
            {"q": "Q3 FY2025", "rev_actual": 70.07, "rev_est": 68.30, "rev_beat": 2.6, "eps": 3.46, "eps_est": 3.22, "eps_beat": 7.5, "reaction": 3.8},
            {"q": "Q4 FY2025", "rev_actual": 69.71, "rev_est": 69.00, "rev_beat": 1.0, "eps": 3.26, "eps_est": 3.20, "eps_beat": 1.9, "reaction": 1.0},
        ],
        "next_earnings": {
            "date": "2026.04.29",
            "period": "Q3 FY2025",
            "rev_guidance": "68.3B",
            "rev_consensus": "68.3B",
            "eps": "3.22",
        },
        "peers": [
            {"ticker": "MSFT", "mktCap": "2.76T", "pe": "22.90", "ps": "10.60", "rev": "$275B", "nm": "36.2%", "highlight": True},
            {"ticker": "AAPL", "mktCap": "3.70T", "pe": "32.34", "ps": "8.45", "rev": "$420.5B", "nm": "25.0%", "highlight": False},
            {"ticker": "GOOG", "mktCap": "3.32T", "pe": "26.01", "ps": "8.66", "rev": "$395B", "nm": "28.6%", "highlight": False},
            {"ticker": "AMZN", "mktCap": "2.15T", "pe": "33.0", "ps": "3.22", "rev": "$668B", "nm": "9.3%", "highlight": False},
            {"ticker": "CRM", "mktCap": "275B", "pe": "48.5", "ps": "8.17", "rev": "$37B", "nm": "15.5%", "highlight": False},
        ],
        "ratios": {
            "pe": 22.90,
            "fpe": 28.48,
            "ps": 10.60,
            "peg": 1.91,
            "roe": 35.5,
            "div": 0.75,
        },
        "overview_money": [
            "FY2025 순이익 $99.5B, 순이익률 36.2% — 고마진 소프트웨어 비즈니스",
            "Intelligent Cloud 세그먼트 매출 $125B로 45% 점유, Azure 성장 가속",
            "FCF $75B이나 Capex 지속 확대로 자유 현금흐름 압박 추세",
        ],
        "overview_growth": [
            "5년 매출 CAGR 13.1% (2021-2025), 중규모 기술사 중 견실한 성장",
            "Azure 분기 성장률 20%+ 유지, Copilot 상용화 본격화",
            "Capex 투자 연 $55B 규모로 AI 인프라 우위 확보 추진",
        ],
        "overview_risks": [
            "Capex 급증(연 $55B)으로 FCF 압박, 수익성 반등까지 시간 필요",
            "Azure 경쟁 심화(AWS, Google Cloud 가격 압박), 마진 위험",
            "Copilot 수익화 성과가 예상보다 미흡할 경우 성장 둔화 우려",
        ],
        "financial_items": [
            "순이익률 36.2%로 최상의 수준, 소프트웨어 비즈니스 특성 반영",
            "R&D 투자 비중 11.6%로 중간 수준, 기술 개발에 투자 중",
            "Capex/매출 비중 20% 수준으로 높아지는 추세, 자본집약화 심화",
            "Intelligent Cloud 매출 비중 45.5%로 주력 세그먼트 지위 확고",
        ],
        "invest": {
            "strengths": "Azure 고성장, 높은 순이익률, Copilot AI 전략 선도",
            "risks": "Capex 급증으로 FCF 압박, Azure 경쟁 심화, 수익화 불확실성",
            "opportunities": "Azure 점유율 확대, Copilot 상용화 가속, Enterprise AI 수요",
            "watchlist": "Azure 성장률 지속성, Copilot 도입 확산, Capex 효율성 개선",
        },
    },
    "GOOGL": {
        "profile": {
            "symbol": "GOOGL",
            "name": "Alphabet Inc.",
            "price": 274.23,
            "changes": 6.12,
            "changesPct": 2.28,
            "exchange": "NASDAQ",
            "sector": "Technology",
            "industry": "Internet Content & Information",
            "country": "US",
            "mktCap": 3.32,
            "beta": 1.08,
            "range": "142.66-275.00",
            "employees": 183000,
            "accent": "#4285f4",
            "desc": "Alphabet은 Google 검색, YouTube, Google Cloud, Android 등을 운영하는 세계 최대 디지털 광고·클라우드 기업입니다.",
        },
        "income": [
            {"year": 2020, "rev": 182.53, "ni": 40.27, "oi": 41.22, "gp": 97.79, "eps": 2.93, "gm": 53.58, "om": 22.59, "nm": 22.06, "rnd": 27.57, "capex": 22.28, "ocf": 65.12, "fcf": 42.84},
            {"year": 2021, "rev": 257.64, "ni": 76.03, "oi": 78.71, "gp": 146.70, "eps": 5.61, "gm": 56.94, "om": 30.55, "nm": 29.51, "rnd": 31.56, "capex": 24.64, "ocf": 91.65, "fcf": 67.01},
            {"year": 2022, "rev": 282.84, "ni": 59.97, "oi": 74.84, "gp": 156.63, "eps": 4.56, "gm": 55.38, "om": 26.46, "nm": 21.20, "rnd": 39.50, "capex": 31.49, "ocf": 91.50, "fcf": 60.01},
            {"year": 2023, "rev": 307.39, "ni": 73.80, "oi": 84.29, "gp": 174.06, "eps": 5.80, "gm": 56.63, "om": 27.43, "nm": 24.01, "rnd": 45.43, "capex": 32.25, "ocf": 101.75, "fcf": 69.50},
            {"year": 2024, "rev": 350.02, "ni": 100.68, "oi": 112.39, "gp": 203.72, "eps": 8.04, "gm": 58.20, "om": 32.11, "nm": 28.76, "rnd": 45.43, "capex": 52.54, "ocf": 112.56, "fcf": 60.02},
        ],
        "quarterly": [
            {"q": "Q1'25", "rev": 90.23, "ni": 34.54},
            {"q": "Q2'25", "rev": 94.68, "ni": 28.82},
            {"q": "Q3'25", "rev": 87.50, "ni": 25.00},
            {"q": "Q4'25", "rev": 89.00, "ni": 25.50},
        ],
        "extra": {},
        "segments": {
            "labels": ["CY2020", "CY2021", "CY2022", "CY2023", "CY2024"],
            "data": [
                {"name": "Advertising", "values": [146.92, 209.49, 224.47, 237.86, 264.14], "color": "#4285f4"},
                {"name": "Google Cloud", "values": [13.06, 19.21, 26.28, 33.09, 43.23], "color": "#34a853"},
                {"name": "YouTube", "values": [19.77, 28.85, 29.24, 31.51, 36.15], "color": "#ea4335"},
                {"name": "Other Bets", "values": [6.78, 0.10, 2.85, 5.00, 6.50], "color": "#fbbc04"},
            ]
        },
        "quarterly_segments": {
            "labels": ["Q1'25", "Q2'25", "Q3'25", "Q4'25"],
            "data": [
                {"name": "Advertising", "values": [66.89, 68.0, 63.0, 65.0], "color": "#4285f4"},
                {"name": "Cloud", "values": [12.26, 13.0, 13.5, 14.0], "color": "#34a853"},
                {"name": "YouTube", "values": [8.93, 9.5, 8.5, 9.0], "color": "#ea4335"},
                {"name": "Other", "values": [2.15, 4.18, 2.5, 1.0], "color": "#fbbc04"},
            ]
        },
        "quarterly_detail": [
            {"q": "Q1'25", "gm": 59.3, "om": 34.1, "nm": 38.3, "note": "Cloud 매출 $12.3B, +35% YoY"},
            {"q": "Q2'25", "gm": 58.5, "om": 32.0, "nm": 30.5, "note": "AI Overviews 광고 확대"},
            {"q": "Q3'25", "gm": 58.0, "om": 31.0, "nm": 28.6, "note": "검색 광고 회복 추세"},
            {"q": "Q4'25", "gm": 58.5, "om": 32.5, "nm": 28.7, "note": "연말 광고주 수요 강세"},
        ],
        "quarterly_financial_items": [
            "Google Cloud 분기 매출 $12-14B로 30% 이상 YoY 성장 지속",
            "Advertising(검색·YouTube) 비중 75%로 여전히 높으나 AI Overviews로 다각화",
            "AI Overviews 도입으로 광고 노출 위험, 장기 모니터링 필요",
            "FCF $60B 수준으로 자유 현금흐름 감소(Capex 증가 영향)",
        ],
        "earnings_quarters": [
            {"q": "Q1'25", "rev_actual": 90.23, "rev_est": 89.09, "rev_beat": 1.3, "eps": 2.81, "eps_est": 2.02, "eps_beat": 39.1, "reaction": 5.0},
            {"q": "Q2'25", "rev_actual": 94.68, "rev_est": 93.50, "rev_beat": 1.3, "eps": 2.14, "eps_est": 1.90, "eps_beat": 12.6, "reaction": 2.0},
            {"q": "Q3'25", "rev_actual": 87.50, "rev_est": 86.0, "rev_beat": 1.7, "eps": 1.95, "eps_est": 1.90, "eps_beat": 2.6, "reaction": 1.0},
            {"q": "Q4'25", "rev_actual": 89.00, "rev_est": 88.0, "rev_beat": 1.1, "eps": 2.05, "eps_est": 2.00, "eps_beat": 2.5, "reaction": 0.5},
        ],
        "next_earnings": {
            "date": "2026.04.29",
            "period": "Q1 CY2026",
            "rev_guidance": "89.0B",
            "rev_consensus": "89.0B",
            "eps": "2.05",
        },
        "peers": [
            {"ticker": "GOOGL", "mktCap": "3.32T", "pe": "26.01", "ps": "8.66", "rev": "$350B", "nm": "28.8%", "highlight": True},
            {"ticker": "META", "mktCap": "1.73T", "pe": "27.5", "ps": "11.51", "rev": "$165B", "nm": "36.0%", "highlight": False},
            {"ticker": "AMZN", "mktCap": "2.15T", "pe": "33.0", "ps": "3.22", "rev": "$668B", "nm": "9.3%", "highlight": False},
            {"ticker": "MSFT", "mktCap": "2.76T", "pe": "22.90", "ps": "10.60", "rev": "$275B", "nm": "36.2%", "highlight": False},
            {"ticker": "SNAP", "mktCap": "20B", "pe": "-", "ps": "4.2", "rev": "$5.5B", "nm": "-4%", "highlight": False},
        ],
        "ratios": {
            "pe": 26.01,
            "fpe": 21.0,
            "ps": 8.66,
            "peg": 0.92,
            "roe": 32.8,
            "div": 0.46,
        },
        "overview_money": [
            "CY2024 순이익 $100.7B, 순이익률 28.8% — 강력한 현금 창출력",
            "Advertising(검색·YouTube) 매출 비중 75%, AI Overviews 도입으로 변화 중",
            "Google Cloud 분기 성장률 35%, 고속 성장하는 수익원",
        ],
        "overview_growth": [
            "5년 매출 CAGR 17.1% (2020-2024), 중규모 기술사 중 견실한 성장",
            "Google Cloud 연 30%+ 성장으로 다각화 추진, 매출 비중 확대 중",
            "AI Overviews 광고 모델 실험 중, 장기 효율성 검증 필요",
        ],
        "overview_risks": [
            "Advertising 매출 비중 75%로 여전히 높음, AI Overviews 리스크 내재",
            "AI 광고 모델 전환 시 광고주 이전(이탈) 가능성, 매출 변동성 증가",
            "Capex 증가(연 $52.5B)로 FCF 감소 추세, 효율성 검증 필요",
        ],
        "financial_items": [
            "순이익률 28.8% 수준 유지, 광고 비즈니스의 고마진 특성 반영",
            "R&D 투자 비중 13% 수준으로 높음, AI 기술 개발 집중",
            "Capex/매출 15% 수준으로 AI 인프라 투자 가속화",
            "Google Cloud 매출 비중 12.4%이지만 고성장(30%+) 중",
        ],
        "invest": {
            "strengths": "검색 광고 진화, Google Cloud 고속 성장, AI 기술 우위",
            "risks": "AI Overviews 광고 모델 불확실성, Capex 효율성, 규제 리스크",
            "opportunities": "Cloud 점유율 확대, Gemini AI 수익화, 광고 AI 고도화",
            "watchlist": "AI Overviews 광고 영향도, Cloud 성장률 지속, Capex ROI",
        },
    },
    "O": {
        "profile": {
            "symbol": "O",
            "name": "Realty Income Corporation",
            "price": 60.06,
            "changes": 0.85,
            "changesPct": 1.43,
            "exchange": "NYSE",
            "sector": "Real Estate",
            "industry": "REIT—Retail",
            "country": "US",
            "mktCap": 0.057,
            "beta": 0.83,
            "range": "48.17-67.82",
            "employees": 508,
            "accent": "#0032a0",
            "desc": "Realty Income는 '월배당 회사(The Monthly Dividend Company)'로 알려진 미국 대표 순임대(Net Lease) 리츠입니다. 15,600개 이상의 상업용 부동산을 보유하고 있습니다.",
        },
        "income": [
            {"year": 2020, "rev": 1.65, "ni": 0.39, "oi": 0.55, "gp": 1.10, "eps": 1.03, "gm": 66.67, "om": 33.33, "nm": 23.64, "rnd": 0, "capex": 0, "ocf": 1.18, "fcf": 1.18, "ffo": 3.13, "affo": 3.08},
            {"year": 2021, "rev": 2.08, "ni": 0.36, "oi": 0.48, "gp": 1.38, "eps": 0.59, "gm": 66.35, "om": 23.08, "nm": 17.31, "rnd": 0, "capex": 0, "ocf": 1.53, "fcf": 1.53, "ffo": 3.59, "affo": 3.53},
            {"year": 2022, "rev": 3.34, "ni": 0.87, "oi": 1.23, "gp": 2.24, "eps": 1.26, "gm": 67.07, "om": 36.83, "nm": 26.05, "rnd": 0, "capex": 0, "ocf": 2.63, "fcf": 2.63, "ffo": 3.92, "affo": 3.88},
            {"year": 2023, "rev": 4.08, "ni": 0.87, "oi": 1.03, "gp": 2.75, "eps": 1.00, "gm": 67.40, "om": 25.25, "nm": 21.32, "rnd": 0, "capex": 0, "ocf": 3.31, "fcf": 3.31, "ffo": 3.88, "affo": 4.01},
            {"year": 2024, "rev": 5.10, "ni": 0.86, "oi": 1.14, "gp": 3.42, "eps": 0.98, "gm": 67.06, "om": 22.35, "nm": 16.86, "rnd": 0, "capex": 0, "ocf": 3.82, "fcf": 3.82, "ffo": 4.22, "affo": 4.28},
        ],
        "quarterly": [
            {"q": "Q1'25", "rev": 1.34, "ni": 0.22},
            {"q": "Q2'25", "rev": 1.35, "ni": 0.22},
            {"q": "Q3'25", "rev": 1.36, "ni": 0.22},
            {"q": "Q4'25", "rev": 1.38, "ni": 0.23},
        ],
        "extra": {},
        "segments": {
            "labels": ["CY2020", "CY2021", "CY2022", "CY2023", "CY2024"],
            "data": [
                {"name": "Retail", "values": [1.20, 1.55, 2.50, 3.06, 3.83], "color": "#0032a0"},
                {"name": "Industrial", "values": [0.30, 0.35, 0.55, 0.68, 0.85], "color": "#4dabf7"},
                {"name": "Gaming", "values": [0.08, 0.10, 0.15, 0.18, 0.22], "color": "#b197fc"},
                {"name": "Other", "values": [0.07, 0.08, 0.14, 0.16, 0.20], "color": "#ffa94d"},
            ]
        },
        "quarterly_segments": {
            "labels": ["Q1'25", "Q2'25", "Q3'25", "Q4'25"],
            "data": [
                {"name": "Retail", "values": [1.00, 1.01, 1.02, 1.04], "color": "#0032a0"},
                {"name": "Industrial", "values": [0.22, 0.22, 0.22, 0.23], "color": "#4dabf7"},
                {"name": "Gaming", "values": [0.06, 0.06, 0.06, 0.06], "color": "#b197fc"},
                {"name": "Other", "values": [0.06, 0.06, 0.06, 0.05], "color": "#ffa94d"},
            ]
        },
        "quarterly_detail": [
            {"q": "Q1'25", "gm": 67.0, "om": 22.0, "nm": 16.4, "note": "월배당 지속, AFFO/주 $1.07"},
            {"q": "Q2'25", "gm": 67.2, "om": 22.5, "nm": 16.3, "note": "Retail 세그먼트 안정적 성장"},
            {"q": "Q3'25", "gm": 67.5, "om": 23.0, "nm": 16.2, "note": "포트폴리오 다각화 진행"},
            {"q": "Q4'25", "gm": 67.8, "om": 23.5, "nm": 16.7, "note": "AFFO/주 $1.10 상향 기대"},
        ],
        "quarterly_financial_items": [
            "AFFO(Adjusted FFO)/주 $1.07-1.10 수준으로 배당 커버율 100% 이상",
            "월배당금 정책 22년 이상 유지, 배당 성장률 연 5.6% 평균",
            "Retail 세그먼트 비중 75%, 소매 부동산 시황 변화에 민감",
            "배당수익률 5.36%로 높은 인컴 투자자 선호",
        ],
        "earnings_quarters": [
            {"q": "Q1'25", "rev_actual": 1.34, "rev_est": 1.33, "rev_beat": 0.8, "eps": 1.07, "eps_est": 1.06, "eps_beat": 0.9, "reaction": 0.5},
            {"q": "Q2'25", "rev_actual": 1.35, "rev_est": 1.34, "rev_beat": 0.7, "eps": 1.08, "eps_est": 1.07, "eps_beat": 0.9, "reaction": 1.2},
            {"q": "Q3'25", "rev_actual": 1.36, "rev_est": 1.35, "rev_beat": 0.7, "eps": 1.09, "eps_est": 1.08, "eps_beat": 0.9, "reaction": 0.8},
            {"q": "Q4'25", "rev_actual": 1.38, "rev_est": 1.37, "rev_beat": 0.7, "eps": 1.10, "eps_est": 1.09, "eps_beat": 0.9, "reaction": 0.5},
        ],
        "next_earnings": {
            "date": "2026.05.05",
            "period": "Q1 2026",
            "rev_guidance": "1.35B",
            "rev_consensus": "1.35B",
            "eps": "1.08",
        },
        "peers": [
            {"ticker": "O", "mktCap": "57B", "pe": "61.3", "ps": "11.18", "rev": "$5.1B", "nm": "16.9%", "highlight": True},
            {"ticker": "NNN", "mktCap": "8.1B", "pe": "33.0", "ps": "10.0", "rev": "$0.85B", "nm": "42%", "highlight": False},
            {"ticker": "WPC", "mktCap": "13.5B", "pe": "30.0", "ps": "7.0", "rev": "$1.9B", "nm": "18%", "highlight": False},
            {"ticker": "VICI", "mktCap": "32B", "pe": "14.2", "ps": "10.0", "rev": "$3.8B", "nm": "59%", "highlight": False},
            {"ticker": "EPRT", "mktCap": "6.8B", "pe": "25.0", "ps": "6.5", "rev": "$1.0B", "nm": "20%", "highlight": False},
        ],
        "ratios": {
            "pe": 61.29,
            "fpe": 13.90,
            "ps": 11.18,
            "peg": 3.50,
            "roe": 2.8,
            "div": 5.36,
        },
        "overview_money": [
            "연 배당금 $3.24/주(월 $0.27), 배당수익률 5.36% — 고배당 인컴투자 선호",
            "AFFO/주 $4.28로 배당 커버율 100% 이상 유지, 배당 지속가능성 높음",
            "15,600개 이상 상업용 부동산 포트폴리오, 장기 임대료 수익 안정적",
        ],
        "overview_growth": [
            "5년 수익 CAGR 32.1% (2020-2024), 빠른 포트폴리오 확장",
            "Industrial 세그먼트 비중 확대 중, 소매 의존도 낮추는 중",
            "배당 연 5.6% 평균 성장으로 인컴 투자자 충성도 높음",
        ],
        "overview_risks": [
            "Retail 세그먼트 75% 의존으로 온라인 쇼핑 확대 리스크 노출",
            "금리 인상 시 담보부채 비용 상승으로 수익성 압박",
            "경기 침체 시 임차인 부도 위험, 공실률 상승 가능성",
        ],
        "financial_items": [
            "REIT이므로 순이익 기준보다 FFO/AFFO 지표 중요도 높음",
            "배당을 위해 회사 수익 대부분 분배하는 구조, 재투자 제한적",
            "장기 순임대 계약으로 수익 예측성 높음, 인컴 투자 기초로 우수",
            "포트폴리오 다각화(Retail 75% → Industrial 17%, Gaming 4% 등) 진행 중",
        ],
        "invest": {
            "strengths": "월배당 22년 이상 연속 유지, AFFO 커버율 100%+, 포트폴리오 다각화 진행",
            "risks": "Retail 75% 의존도 높음, 금리 상승 영향, 경기 침체 시 임차인 부도",
            "opportunities": "Industrial 비중 확대, Gateway 자산 취득, 배당 성장 가속",
            "watchlist": "AFFO/주 성장률, 배당 커버 안정성, 임차인 부도율",
        },
    },
    "ABBV": {
        "profile": {
            "symbol": "ABBV",
            "name": "AbbVie Inc.",
            "price": 211.12,
            "changes": 2.34,
            "changesPct": 1.12,
            "exchange": "NYSE",
            "sector": "Healthcare",
            "industry": "Drug Manufacturers",
            "country": "US",
            "mktCap": 0.388,
            "beta": 0.57,
            "range": "152.25-227.13",
            "employees": 50000,
            "accent": "#071d49",
            "desc": "AbbVie는 면역학, 종양학, 신경과학 분야의 글로벌 바이오제약 기업입니다. 대표 제품은 Humira, Skyrizi, Rinvoq입니다.",
        },
        "income": [
            {"year": 2020, "rev": 45.80, "ni": 4.62, "oi": 7.11, "gp": 33.64, "eps": 2.72, "gm": 73.45, "om": 15.52, "nm": 10.09, "rnd": 6.56, "capex": 1.47, "ocf": 19.16, "fcf": 17.69},
            {"year": 2021, "rev": 56.20, "ni": 11.54, "oi": 16.45, "gp": 41.20, "eps": 6.45, "gm": 73.31, "om": 29.27, "nm": 20.53, "rnd": 7.08, "capex": 1.23, "ocf": 22.00, "fcf": 20.77},
            {"year": 2022, "rev": 58.05, "ni": 11.84, "oi": 17.50, "gp": 41.51, "eps": 6.63, "gm": 71.51, "om": 30.15, "nm": 20.40, "rnd": 6.50, "capex": 1.10, "ocf": 24.94, "fcf": 23.84},
            {"year": 2023, "rev": 54.32, "ni": 4.86, "oi": 7.52, "gp": 37.48, "eps": 2.73, "gm": 68.99, "om": 13.84, "nm": 8.94, "rnd": 7.15, "capex": 1.42, "ocf": 22.32, "fcf": 20.90},
            {"year": 2024, "rev": 56.33, "ni": 5.28, "oi": 8.70, "gp": 39.30, "eps": 2.99, "gm": 69.78, "om": 15.45, "nm": 9.37, "rnd": 7.68, "capex": 1.30, "ocf": 24.25, "fcf": 22.95},
        ],
        "quarterly": [
            {"q": "Q1'25", "rev": 13.34, "ni": 1.39},
            {"q": "Q2'25", "rev": 14.78, "ni": 3.52},
            {"q": "Q3'25", "rev": 14.46, "ni": 2.35},
            {"q": "Q4'25", "rev": 15.00, "ni": 2.50},
        ],
        "extra": {},
        "segments": {
            "labels": ["CY2020", "CY2021", "CY2022", "CY2023", "CY2024"],
            "data": [
                {"name": "Immunology", "values": [24.17, 30.28, 30.60, 24.76, 27.03], "color": "#071d49"},
                {"name": "Oncology", "values": [5.65, 5.99, 6.38, 6.75, 7.12], "color": "#4ecdc4"},
                {"name": "Neuroscience", "values": [6.82, 7.73, 8.45, 9.22, 9.83], "color": "#b197fc"},
                {"name": "Aesthetics", "values": [4.80, 5.30, 5.41, 5.18, 5.25], "color": "#ffa94d"},
                {"name": "Other", "values": [4.36, 6.90, 7.21, 8.41, 7.10], "color": "#4dabf7"},
            ]
        },
        "quarterly_segments": {
            "labels": ["Q1'25", "Q2'25", "Q3'25", "Q4'25"],
            "data": [
                {"name": "Immunology", "values": [6.62, 7.40, 7.20, 7.50], "color": "#071d49"},
                {"name": "Oncology", "values": [1.72, 1.90, 1.85, 1.95], "color": "#4ecdc4"},
                {"name": "Neuroscience", "values": [2.35, 2.60, 2.55, 2.70], "color": "#b197fc"},
                {"name": "Aesthetics", "values": [1.14, 1.58, 1.50, 1.40], "color": "#ffa94d"},
                {"name": "Other", "values": [1.51, 1.30, 1.36, 1.45], "color": "#4dabf7"},
            ]
        },
        "quarterly_detail": [
            {"q": "Q1'25", "gm": 62.3, "om": 22.3, "nm": 10.4, "note": "Humira 바이오시밀러 경쟁 지속"},
            {"q": "Q2'25", "gm": 70.2, "om": 30.5, "nm": 23.8, "note": "Skyrizi/Rinvoq 고성장"},
            {"q": "Q3'25", "gm": 69.0, "om": 26.0, "nm": 16.3, "note": "Cerevel 파이프라인 진행"},
            {"q": "Q4'25", "gm": 69.5, "om": 27.0, "nm": 16.7, "note": "신약 상업화 본격화"},
        ],
        "quarterly_financial_items": [
            "Humira 매출 급감(바이오시밀러 경쟁)으로 Immunology 비중 48% 하락 추세",
            "Skyrizi(피부질환), Rinvoq(류마티스) 고성장이 부분적으로 상쇄",
            "Oncology 분야 차별화 신약 파이프라인(Cerevel) 진행 중",
            "FCF 유지(연 $22.95B) 가능하나 특허절벽 이후 성장 전략 필수",
        ],
        "earnings_quarters": [
            {"q": "Q1'25", "rev_actual": 13.34, "rev_est": 12.80, "rev_beat": 4.2, "eps": 2.46, "eps_est": 2.39, "eps_beat": 2.9, "reaction": 2.5},
            {"q": "Q2'25", "rev_actual": 14.78, "rev_est": 14.13, "rev_beat": 4.6, "eps": 3.37, "eps_est": 3.22, "eps_beat": 4.7, "reaction": 3.8},
            {"q": "Q3'25", "rev_actual": 14.46, "rev_est": 14.30, "rev_beat": 1.1, "eps": 3.00, "eps_est": 2.90, "eps_beat": 3.4, "reaction": 1.0},
            {"q": "Q4'25", "rev_actual": 15.00, "rev_est": 14.80, "rev_beat": 1.4, "eps": 3.05, "eps_est": 2.95, "eps_beat": 3.4, "reaction": 0.5},
        ],
        "next_earnings": {
            "date": "2026.04.24",
            "period": "Q1 2026",
            "rev_guidance": "13.5B",
            "rev_consensus": "13.5B",
            "eps": "2.50",
        },
        "peers": [
            {"ticker": "ABBV", "mktCap": "388B", "pe": "70.64", "ps": "6.89", "rev": "$56.3B", "nm": "9.4%", "highlight": True},
            {"ticker": "JNJ", "mktCap": "398B", "pe": "25.0", "ps": "4.6", "rev": "$88.8B", "nm": "17.2%", "highlight": False},
            {"ticker": "LLY", "mktCap": "750B", "pe": "80.0", "ps": "20.5", "rev": "$41.3B", "nm": "25.5%", "highlight": False},
            {"ticker": "MRK", "mktCap": "250B", "pe": "15.8", "ps": "4.0", "rev": "$60.1B", "nm": "22%", "highlight": False},
            {"ticker": "PFE", "mktCap": "145B", "pe": "12.5", "ps": "2.2", "rev": "$65B", "nm": "14%", "highlight": False},
        ],
        "ratios": {
            "pe": 70.64,
            "fpe": 13.48,
            "ps": 6.89,
            "peg": 1.12,
            "roe": 47.5,
            "div": 3.21,
        },
        "overview_money": [
            "CY2024 순이익 $5.28B이나 특허절벽 영향으로 수익성 단기 약화 중",
            "Humira 바이오시밀러 경쟁으로 매출 감소, Skyrizi/Rinvoq 성장 추진",
            "배당률 3.21%, 안정적 현금흐름으로 주주환원 지속",
        ],
        "overview_growth": [
            "5년 수익 CAGR -1.4% (2020-2024), 특허절벽 영향으로 음의 성장",
            "신약(Skyrizi, Rinvoq, Cerevel) 상업화로 성장 반전 기대",
            "Oncology, Neuroscience 파이프라인 강화로 장기 성장 초석 마련",
        ],
        "overview_risks": [
            "Humira 매출 급감(바이오시밀러 경쟁)으로 단기 수익성 악화",
            "신약 상업화 성공 불확실성, 임상 실패 또는 규제 승인 지연 리스크",
            "경쟁사(LLY, JNJ, MRK) 신약 출시로 시장점유율 잠식 가능",
        ],
        "financial_items": [
            "순이익률 9.4% 수준으로 업계 평균 이하, 특허절벽 영향 반영",
            "R&D 투자 비중 13.6%로 높음, 신약 개발에 집중",
            "면역학 비중 48%에서 다각화 추진 중(Oncology, Neuroscience 확대)",
            "FCF 유지로 안정적이나 매출 성장 필요성 높음",
        ],
        "invest": {
            "strengths": "Skyrizi/Rinvoq 고성장, Cerevel 파이프라인, 높은 R&D 투자",
            "risks": "Humira 매출 급감, 특허절벽, 신약 상용화 불확실성",
            "opportunities": "Skyrizi 적응증 확대, Rinvoq 성장, Cerevel 중추신경 시장 진입",
            "watchlist": "Humira 하락 속도, 신약 성장률, 파이프라인 임상 진행",
        },
    },
    "PLTR": {
        "profile": {
            "symbol": "PLTR",
            "name": "Palantir Technologies Inc.",
            "price": 143.06,
            "changes": 8.12,
            "changesPct": 5.99,
            "exchange": "NYSE",
            "sector": "Technology",
            "industry": "Software—Infrastructure",
            "country": "US",
            "mktCap": 0.342,
            "beta": 2.64,
            "range": "29.62-148.52",
            "employees": 3900,
            "accent": "#a78bfa",
            "desc": "Palantir는 정부 기관과 기업을 위한 AI·빅데이터 분석 플랫폼(Gotham, Foundry, AIP)을 제공하는 데이터 분석 전문 기업입니다.",
        },
        "income": [
            {"year": 2020, "rev": 1.09, "ni": -1.17, "oi": -1.17, "gp": 0.73, "eps": -0.08, "gm": 67.00, "om": -107.34, "nm": -107.34, "rnd": 0.56, "capex": 0.01, "ocf": -0.37, "fcf": -0.38},
            {"year": 2021, "rev": 1.54, "ni": -0.52, "oi": -0.41, "gp": 1.16, "eps": -0.02, "gm": 75.32, "om": -26.62, "nm": -33.77, "rnd": 0.40, "capex": 0.01, "ocf": 0.33, "fcf": 0.32},
            {"year": 2022, "rev": 1.91, "ni": -0.37, "oi": -0.19, "gp": 1.49, "eps": -0.02, "gm": 78.01, "om": -9.95, "nm": -19.37, "rnd": 0.43, "capex": 0.02, "ocf": 0.23, "fcf": 0.21},
            {"year": 2023, "rev": 2.23, "ni": 0.21, "oi": 0.12, "gp": 1.78, "eps": 0.09, "gm": 79.82, "om": 5.38, "nm": 9.42, "rnd": 0.44, "capex": 0.04, "ocf": 0.71, "fcf": 0.67},
            {"year": 2024, "rev": 2.87, "ni": 0.46, "oi": 0.31, "gp": 2.34, "eps": 0.19, "gm": 81.53, "om": 10.80, "nm": 16.03, "rnd": 0.52, "capex": 0.04, "ocf": 1.15, "fcf": 1.11},
        ],
        "quarterly": [
            {"q": "Q1'25", "rev": 0.884, "ni": 0.134},
            {"q": "Q2'25", "rev": 0.935, "ni": 0.145},
            {"q": "Q3'25", "rev": 0.980, "ni": 0.155},
        ],
        "extra": {},
        "segments": {
            "labels": ["CY2020", "CY2021", "CY2022", "CY2023", "CY2024"],
            "data": [
                {"name": "Government", "values": [0.61, 0.90, 1.11, 1.22, 1.41], "color": "#a78bfa"},
                {"name": "Commercial", "values": [0.48, 0.64, 0.80, 1.01, 1.46], "color": "#4ecdc4"},
            ]
        },
        "quarterly_segments": {
            "labels": ["Q1'25", "Q2'25", "Q3'25"],
            "data": [
                {"name": "Government", "values": [0.373, 0.382, 0.400], "color": "#a78bfa"},
                {"name": "Commercial", "values": [0.511, 0.553, 0.580], "color": "#4ecdc4"},
            ]
        },
        "quarterly_detail": [
            {"q": "Q1'25", "gm": 82.2, "om": 16.2, "nm": 15.2, "note": "AIP 부트캠프 확대, US Commercial +55% YoY"},
            {"q": "Q2'25", "gm": 82.0, "om": 16.5, "nm": 15.5, "note": "Commercial 고성장 지속"},
            {"q": "Q3'25", "gm": 82.5, "om": 17.0, "nm": 15.8, "note": "AIP 플랫폼 상용화 가속"},
        ],
        "quarterly_financial_items": [
            "Commercial 매출 비중 62%, Government 38%로 양극화 구조 지속",
            "US Commercial +55% YoY 고성장으로 향후 주요 성장 동력 기대",
            "AIP(AI Platform) 수익화 본격화로 상품 다각화 진행",
            "순이익률 16% 수준으로 개선 추세 지속",
        ],
        "earnings_quarters": [
            {"q": "Q1'25", "rev_actual": 0.884, "rev_est": 0.863, "rev_beat": 2.4, "eps": 0.13, "eps_est": 0.13, "eps_beat": 0.0, "reaction": 8.5},
            {"q": "Q2'25", "rev_actual": 0.935, "rev_est": 0.900, "rev_beat": 3.9, "eps": 0.14, "eps_est": 0.13, "eps_beat": 7.7, "reaction": 12.0},
        ],
        "next_earnings": {
            "date": "2026.05.05",
            "period": "Q1 2026",
            "rev_guidance": "0.87B",
            "rev_consensus": "0.87B",
            "eps": "0.13",
        },
        "peers": [
            {"ticker": "PLTR", "mktCap": "342B", "pe": "222.73", "ps": "40.27", "rev": "$2.87B", "nm": "16.0%", "highlight": True},
            {"ticker": "SNOW", "mktCap": "60B", "pe": "-", "ps": "18.0", "rev": "$3.4B", "nm": "-7%", "highlight": False},
            {"ticker": "DDOG", "mktCap": "44B", "pe": "275", "ps": "19.5", "rev": "$2.7B", "nm": "3.5%", "highlight": False},
            {"ticker": "CRM", "mktCap": "275B", "pe": "48.5", "ps": "8.17", "rev": "$37B", "nm": "15.5%", "highlight": False},
            {"ticker": "MDB", "mktCap": "20B", "pe": "-", "ps": "9.0", "rev": "$2.0B", "nm": "-2%", "highlight": False},
        ],
        "ratios": {
            "pe": 222.73,
            "fpe": 137.0,
            "ps": 40.27,
            "peg": 5.75,
            "roe": 12.5,
            "div": 0.00,
        },
        "overview_money": [
            "CY2024 순이익 $0.46B, 순이익률 16% — 흑자 전환 달성",
            "US Commercial +55% YoY, 미국 민간 기업 시장 개척 성공",
            "FCF 양수($1.11B), 성숙 기업 수준의 현금 창출 능력",
        ],
        "overview_growth": [
            "5년 매출 CAGR 27.5% (2020-2024), 고성장 소프트웨어 기업 수준",
            "Commercial 분야 폭발적 성장(CAGR 33.6%), Government 안정적(CAGR 23.7%)",
            "AIP 플랫폼 상용화로 AI 시대 새로운 성장 단계 진입",
        ],
        "overview_risks": [
            "PER 222배, PSR 40배로 매우 높은 밸류에이션 — 실적 성장 필수",
            "Commercial 시장 경쟁 심화(데이터 분석 경쟁사 증가), 고객 확보 압박",
            "정부 예산 감축 시 Government 매출 하락 리스크",
        ],
        "financial_items": [
            "R&D 투자 비중 18% 수준으로 높음, 기술 개발 집중",
            "마진 개선 추세: 순이익률 2023년 9.4% → 2024년 16% 상향",
            "고객 집중도 높음(정부 고객 비중 38%), 고객 다각화 진행 중",
            "캐피탈 라이트 모델로 FCF 창출 효율성 높음",
        ],
        "invest": {
            "strengths": "US Commercial +55% 고성장, AIP 플랫폼 상용화, 정부 강력한 포지션",
            "risks": "극도로 높은 밸류에이션, Commercial 경쟁 심화, 정부 예산 리스크",
            "opportunities": "Commercial 시장 확대, AIP 채택 가속, 국제 시장 진출",
            "watchlist": "Commercial 성장률 지속성, AIP 수익화 진행, 고객 확보 속도",
        },
    },
    "CRWV": {
        "profile": {
            "symbol": "CRWV",
            "name": "Cerebras Systems Inc.",
            "price": 74.70,
            "changes": 3.21,
            "changesPct": 4.49,
            "exchange": "NASDAQ",
            "sector": "Technology",
            "industry": "Semiconductors",
            "country": "US",
            "mktCap": 0.039,
            "beta": 2.15,
            "range": "41.00-100.50",
            "employees": 450,
            "accent": "#ff6b35",
            "desc": "Cerebras Systems는 세계 최대 AI 칩(WSE-3, Wafer Scale Engine)을 설계·제조하는 AI 하드웨어 스타트업입니다. 2025년 IPO했으며, NVIDIA의 대항마로 주목받고 있습니다.",
        },
        "income": [
            {"year": 2023, "rev": 0.079, "ni": -0.086, "oi": -0.086, "gp": 0.044, "eps": -0.15, "gm": 55.70, "om": -108.86, "nm": -108.86, "rnd": 0.055, "capex": 0.012, "ocf": -0.078, "fcf": -0.090},
            {"year": 2024, "rev": 0.136, "ni": -0.070, "oi": -0.070, "gp": 0.080, "eps": -0.12, "gm": 58.82, "om": -51.47, "nm": -51.47, "rnd": 0.068, "capex": 0.015, "ocf": -0.060, "fcf": -0.075},
        ],
        "quarterly": [
            {"q": "Q1'25", "rev": 0.038, "ni": -0.022},
            {"q": "Q2'25", "rev": 0.045, "ni": -0.018},
        ],
        "extra": {},
        "segments": {
            "labels": ["CY2023", "CY2024"],
            "data": [
                {"name": "Compute", "values": [0.060, 0.100], "color": "#ff6b35"},
                {"name": "AI Cloud", "values": [0.019, 0.036], "color": "#4ecdc4"},
            ]
        },
        "quarterly_segments": {
            "labels": ["Q1'25", "Q2'25"],
            "data": [
                {"name": "Compute", "values": [0.028, 0.033], "color": "#ff6b35"},
                {"name": "Cloud", "values": [0.010, 0.012], "color": "#4ecdc4"},
            ]
        },
        "quarterly_detail": [
            {"q": "Q1'25", "gm": 55.0, "om": -60.0, "nm": -57.9, "note": "WSE-3 출하 시작"},
            {"q": "Q2'25", "gm": 58.0, "om": -42.0, "nm": -40.0, "note": "매출 증가, 손실 축소 추세"},
        ],
        "quarterly_financial_items": [
            "WSE-3 칩 출하 시작으로 매출 가시성 확보, 분기 성장 추이 긍정적",
            "AI 컴퓨팅 시장 수요 강세로 칩 주문 증가 추세",
            "현재 pre-revenue → revenue 전환 중, 손익분기점까지 시간 필요",
            "현금 소모 단계(연 $0.075B 규모), 자금 조달 위험 모니터링 필수",
        ],
        "earnings_quarters": [
            {"q": "Q1'25", "rev_actual": 0.038, "rev_est": 0.035, "rev_beat": 8.6, "eps": -0.04, "eps_est": -0.05, "eps_beat": 20.0, "reaction": 5.0},
            {"q": "Q2'25", "rev_actual": 0.045, "rev_est": 0.040, "rev_beat": 12.5, "eps": -0.03, "eps_est": -0.04, "eps_beat": 25.0, "reaction": 3.0},
        ],
        "next_earnings": {
            "date": "2026.05.15",
            "period": "Q1 2026",
            "rev_guidance": "0.04B",
            "rev_consensus": "0.04B",
            "eps": "-0.04",
        },
        "peers": [
            {"ticker": "CRWV", "mktCap": "39B", "pe": "-", "ps": "143.0", "rev": "$0.136B", "nm": "-51%", "highlight": True},
            {"ticker": "NVDA", "mktCap": "4.07T", "pe": "34.2", "ps": "18.8", "rev": "$215.9B", "nm": "55.6%", "highlight": False},
            {"ticker": "AMD", "mktCap": "210B", "pe": "24.8", "ps": "7.1", "rev": "$28.1B", "nm": "22%", "highlight": False},
            {"ticker": "INTC", "mktCap": "97B", "pe": "-", "ps": "1.5", "rev": "$53.1B", "nm": "-1%", "highlight": False},
            {"ticker": "MRVL", "mktCap": "60B", "pe": "32", "ps": "6.5", "rev": "$10B", "nm": "25%", "highlight": False},
        ],
        "ratios": {
            "pe": None,
            "fpe": None,
            "ps": 143.0,
            "peg": None,
            "roe": -15.0,
            "div": 0.00,
        },
        "overview_money": [
            "CY2024 매출 $0.136B, 성장 초기 단계의 스타트업 수준",
            "WSE-3 칩 출하 시작으로 부정적 현금흐름 개선 추이 보임",
            "IPO를 통한 자금 조달로 R&D 및 생산 확대 가능",
        ],
        "overview_growth": [
            "AI 칩 시장 폭발적 성장, NVIDIA 독점 공급 구조에 도전 기회",
            "WSE-3 기술이 NVIDIA GPU 보다 에너지 효율성 장점 강조",
            "주요 고객(대형 클라우드 회사, 정부 기관) 주문 증가 추이",
        ],
        "overview_risks": [
            "IPO 직후 적립금 소모 속도, 추가 자금 조달 필요성 높음",
            "NVIDIA 독점 구조 진입 난제, 칩 성능 검증 필요",
            "생산 능력 제한(팹 협력사 의존), 대량 공급 불확실성",
        ],
        "financial_items": [
            "Pre-revenue 수준(매출 $136M)에서 revenue 전환 진행 중",
            "R&D 투자 비중 50% 수준으로 극도로 높음(기술 개발 집중)",
            "손익분기점까지 최소 2-3년 추정, 추가 자금 조달 필수",
            "IPO 자금(약 $5.5B 추정) 소모 속도가 경영 핵심 지표",
        ],
        "invest": {
            "strengths": "혁신적 WSE-3 칩 기술, NVIDIA 독점 타파 기회, AI 시장 수요 증가",
            "risks": "극도의 높은 현금 소모, 생산 능력 한계, 기술 검증 불완료",
            "opportunities": "대형 클라우드 고객 주문 확대, AI 데이터센터 수요 증가",
            "watchlist": "WSE-3 칩 출하량 및 수주금액, 손실 축소 속도, 팹 파트너십 진행",
        },
    },
    "IONQ": {
        "profile": {
            "symbol": "IONQ",
            "name": "IonQ Inc.",
            "price": 28.26,
            "changes": 1.85,
            "changesPct": 6.98,
            "exchange": "NYSE",
            "sector": "Technology",
            "industry": "Computer Hardware",
            "country": "US",
            "mktCap": 0.01185,
            "beta": 1.89,
            "range": "6.98-54.88",
            "employees": 500,
            "accent": "#6366f1",
            "desc": "IonQ는 이온 트랩 방식의 양자 컴퓨팅 기업입니다. AWS, Azure, Google Cloud에서 양자 컴퓨팅 서비스를 제공하며, 정부·기업 대상 양자 연구 계약을 수행합니다.",
        },
        "income": [
            {"year": 2021, "rev": 0.002, "ni": -0.106, "oi": -0.106, "gp": -0.001, "eps": -0.55, "gm": -50.00, "om": -5300.0, "nm": -5300.0, "rnd": 0.028, "capex": 0.005, "ocf": -0.080, "fcf": -0.085},
            {"year": 2022, "rev": 0.011, "ni": -0.154, "oi": -0.154, "gp": -0.001, "eps": -0.73, "gm": -9.09, "om": -1400.0, "nm": -1400.0, "rnd": 0.040, "capex": 0.010, "ocf": -0.128, "fcf": -0.138},
            {"year": 2023, "rev": 0.022, "ni": -0.157, "oi": -0.157, "gp": 0.003, "eps": -0.72, "gm": 13.64, "om": -713.0, "nm": -713.0, "rnd": 0.060, "capex": 0.015, "ocf": -0.134, "fcf": -0.149},
            {"year": 2024, "rev": 0.043, "ni": -0.232, "oi": -0.228, "gp": 0.018, "eps": -0.87, "gm": 41.86, "om": -530.0, "nm": -540.0, "rnd": 0.100, "capex": 0.025, "ocf": -0.185, "fcf": -0.210},
        ],
        "quarterly": [
            {"q": "Q1'25", "rev": 0.008, "ni": -0.060},
            {"q": "Q2'25", "rev": 0.012, "ni": -0.055},
        ],
        "extra": {},
        "segments": {
            "labels": ["CY2021", "CY2022", "CY2023", "CY2024"],
            "data": [
                {"name": "Quantum Cloud", "values": [0.001, 0.006, 0.012, 0.025], "color": "#6366f1"},
                {"name": "Government", "values": [0.001, 0.005, 0.010, 0.018], "color": "#4ecdc4"},
            ]
        },
        "quarterly_segments": {
            "labels": ["Q1'25", "Q2'25"],
            "data": [
                {"name": "Quantum Cloud", "values": [0.005, 0.007], "color": "#6366f1"},
                {"name": "Government", "values": [0.003, 0.005], "color": "#4ecdc4"},
            ]
        },
        "quarterly_detail": [
            {"q": "Q1'25", "gm": 40.0, "om": -45.0, "nm": -48.0, "note": "Forte Enterprise 시스템 수주"},
            {"q": "Q2'25", "gm": 42.0, "om": -38.0, "nm": -42.0, "note": "양자 알고리즘 개발 협력 확대"},
        ],
        "quarterly_financial_items": [
            "양자 컴퓨팅 시장 초기 단계, 실제 비즈니스 매출 미미한 수준",
            "Quantum Cloud 플랫폼(AWS, Azure, GCP 통합) 구축 완료",
            "정부 계약(DARPA 등) 수주로 R&D 자금 조달",
            "손실 축소 추이 보이나 손익분기점까지 최소 3-5년 예상",
        ],
        "earnings_quarters": [
            {"q": "Q1'25", "rev_actual": 0.008, "rev_est": 0.007, "rev_beat": 14.3, "eps": -0.24, "eps_est": -0.28, "eps_beat": 14.3, "reaction": 15.0},
            {"q": "Q2'25", "rev_actual": 0.012, "rev_est": 0.010, "rev_beat": 20.0, "eps": -0.22, "eps_est": -0.25, "eps_beat": 12.0, "reaction": 10.0},
        ],
        "next_earnings": {
            "date": "2026.05.08",
            "period": "Q1 2026",
            "rev_guidance": "0.01B",
            "rev_consensus": "0.01B",
            "eps": "-0.22",
        },
        "peers": [
            {"ticker": "IONQ", "mktCap": "11.85B", "pe": "-", "ps": "275.0", "rev": "$43M", "nm": "-540%", "highlight": True},
            {"ticker": "RGTI", "mktCap": "5.2B", "pe": "-", "ps": "650.0", "rev": "$12M", "nm": "-1200%", "highlight": False},
            {"ticker": "QBTS", "mktCap": "3.8B", "pe": "-", "ps": "300.0", "rev": "$15M", "nm": "-800%", "highlight": False},
            {"ticker": "IBM", "mktCap": "175B", "pe": "22.0", "ps": "3.5", "rev": "$62B", "nm": "13%", "highlight": False},
            {"ticker": "GOOG", "mktCap": "3.32T", "pe": "26.01", "ps": "8.66", "rev": "$350B", "nm": "28.8%", "highlight": False},
        ],
        "ratios": {
            "pe": None,
            "fpe": None,
            "ps": 275.0,
            "peg": None,
            "roe": -20.0,
            "div": 0.00,
        },
        "overview_money": [
            "CY2024 매출 $43M 수준, 초기 단계 스타트업 특성",
            "정부 계약(DARPA, SBIR) 수주로 R&D 자금 조달 중",
            "손실 지속($232M) 중이나 손실 축소 추이 보임",
        ],
        "overview_growth": [
            "양자 컴퓨팅 시장 초기, 기술 검증 단계의 장기 투자 자산",
            "Quantum Cloud 플랫폼 통합으로 접근성 개선, 개발자 확대 추진",
            "Forte Enterprise 시스템 고객화로 상업화 가속화 예상",
        ],
        "overview_risks": [
            "양자 컴퓨팅 기술 성숙도 낮음, 실용화까지 최소 5-10년 추정",
            "극도의 높은 손실 지속, 현금 소모 속도 빠름(연 $210M)",
            "Google, IBM, Intel 등 거대 기업 경쟁 진입, 생존 불확실성",
        ],
        "financial_items": [
            "매출 $43M 수준으로 실질적 비즈니스 아직 미미",
            "R&D 비중 300%+ 수준(매출대비 손실), 기술 개발 중심",
            "정부 자금(DARPA) 의존도 높음, 정책 변화 리스크",
            "향후 3-5년 추가 자금 조달(Series C, D 등) 필수",
        ],
        "invest": {
            "strengths": "양자 컴퓨팅 파이오니어, 클라우드 통합 플랫폼, 정부 계약 보안",
            "risks": "극도의 높은 손실, 현금 소모 속도, 기술 성숙도 낮음, 경쟁 심화",
            "opportunities": "양자 알고리즘 상용화, 산업 고객 확대, 정부 투자 증가",
            "watchlist": "손실 축소 속도, 고객 계약 수주, 기술 성능 개선, 자금 조달",
        },
    },
    "SMR": {
        "profile": {
            "symbol": "SMR",
            "name": "NuScale Power Corporation",
            "price": 10.38,
            "changes": 0.62,
            "changesPct": 6.34,
            "exchange": "NYSE",
            "sector": "Industrials",
            "industry": "Specialty Industrial Machinery",
            "country": "US",
            "mktCap": 0.00387,
            "beta": 2.90,
            "range": "4.10-31.87",
            "employees": 400,
            "accent": "#e63946",
            "desc": "NuScale Power는 세계 최초로 미국 NRC 인증을 받은 소형모듈원자로(SMR) 설계 기업입니다. 청정에너지·AI 데이터센터 전력 공급이 핵심 사업입니다.",
        },
        "income": [
            {"year": 2021, "rev": 0.0, "ni": -0.059, "oi": -0.059, "gp": 0.0, "eps": -0.43, "gm": 0, "om": 0, "nm": 0, "rnd": 0.052, "capex": 0.003, "ocf": -0.055, "fcf": -0.058},
            {"year": 2022, "rev": 0.0, "ni": -0.100, "oi": -0.100, "gp": 0.0, "eps": -0.55, "gm": 0, "om": 0, "nm": 0, "rnd": 0.078, "capex": 0.005, "ocf": -0.092, "fcf": -0.097},
            {"year": 2023, "rev": 0.003, "ni": -0.108, "oi": -0.108, "gp": -0.001, "eps": -0.52, "gm": 0, "om": 0, "nm": 0, "rnd": 0.085, "capex": 0.005, "ocf": -0.096, "fcf": -0.101},
            {"year": 2024, "rev": 0.005, "ni": -0.130, "oi": -0.130, "gp": 0.001, "eps": -0.53, "gm": 20.00, "om": -2600.0, "nm": -2600.0, "rnd": 0.100, "capex": 0.008, "ocf": -0.110, "fcf": -0.118},
        ],
        "quarterly": [
            {"q": "Q1'25", "rev": 0.001, "ni": -0.035},
            {"q": "Q2'25", "rev": 0.002, "ni": -0.033},
        ],
        "extra": {},
        "segments": {
            "labels": ["CY2023", "CY2024"],
            "data": [
                {"name": "Design & Licensing", "values": [0.002, 0.003], "color": "#e63946"},
                {"name": "Engineering", "values": [0.001, 0.002], "color": "#4ecdc4"},
            ]
        },
        "quarterly_segments": {
            "labels": ["Q1'25", "Q2'25"],
            "data": [
                {"name": "Design", "values": [0.001, 0.001], "color": "#e63946"},
                {"name": "Engineering", "values": [0.0, 0.001], "color": "#4ecdc4"},
            ]
        },
        "quarterly_detail": [
            {"q": "Q1'25", "gm": 0, "om": 0, "nm": 0, "note": "NRC 인증 갱신, CFPP 프로젝트 진행"},
            {"q": "Q2'25", "gm": 0, "om": 0, "nm": 0, "note": "정부 계약 예상 확대"},
        ],
        "quarterly_financial_items": [
            "SMR 기술 설계 완료, NRC 인증 보유로 시장 유일 합법 업체",
            "CFPP(Cooperative Federal Partnership Project) 프로젝트 진행 중",
            "AI 데이터센터 전력 수요 증가로 향후 비즈니스 기회 확대 예상",
            "현재 pre-revenue 수준, 설계 라이선싱 모델로 전환 추진",
        ],
        "earnings_quarters": [
            {"q": "Q1'25", "rev_actual": 0.001, "rev_est": 0.001, "rev_beat": 0.0, "eps": -0.14, "eps_est": -0.15, "eps_beat": 6.7, "reaction": 5.0},
            {"q": "Q2'25", "rev_actual": 0.002, "rev_est": 0.001, "rev_beat": 100.0, "eps": -0.13, "eps_est": -0.15, "eps_beat": 13.3, "reaction": 8.0},
        ],
        "next_earnings": {
            "date": "2026.05.12",
            "period": "Q1 2026",
            "rev_guidance": "0.002B",
            "rev_consensus": "0.002B",
            "eps": "-0.14",
        },
        "peers": [
            {"ticker": "SMR", "mktCap": "3.87B", "pe": "-", "ps": "774.0", "rev": "$5M", "nm": "-2600%", "highlight": True},
            {"ticker": "OKLO", "mktCap": "4.2B", "pe": "-", "ps": "-", "rev": "$0", "nm": "-", "highlight": False},
            {"ticker": "LEU", "mktCap": "2.5B", "pe": "15.0", "ps": "5.0", "rev": "$0.5B", "nm": "8%", "highlight": False},
            {"ticker": "BWX", "mktCap": "10.8B", "pe": "35.0", "ps": "4.2", "rev": "$2.7B", "nm": "10%", "highlight": False},
            {"ticker": "CCJ", "mktCap": "28B", "pe": "55.0", "ps": "11.5", "rev": "$2.8B", "nm": "12%", "highlight": False},
        ],
        "ratios": {
            "pe": None,
            "fpe": None,
            "ps": 774.0,
            "peg": None,
            "roe": -25.0,
            "div": 0.00,
        },
        "overview_money": [
            "CY2024 매출 $5M 수준, 실질적 비즈니스 아직 미미",
            "손실 지속($130M) 중이나 NRC 인증 확보로 시장 진입 기반 마련",
            "정부 계약(DOE, CFPP) 기반 자금 조달 추진 중",
        ],
        "overview_growth": [
            "SMR 기술 세계 최초 NRC 인증 획득, 규제 장벽 돌파",
            "AI 데이터센터 청정에너지 전력 수요 급증, 향후 시장 확대 기대",
            "정부 에너지 정책(원전 재평가) 호재로 장기 수혜 예상",
        ],
        "overview_risks": [
            "초기 단계 기술, 상용화까지 최소 5-7년 소요 예상",
            "극도의 높은 현금 소모(연 $118M), 지속 자금 조달 필수",
            "원전 규제 변화, 건설비 증가로 프로젝트 지연 리스크",
        ],
        "financial_items": [
            "매출 $5M 수준으로 실질적 비즈니스 초기 단계",
            "R&D 투자 비중 2000%+ 수준(매출대비 손실), 기술 개발 중심",
            "정부 자금(DOE, CFPP, 주정부) 의존도 높음, 정책 리스크",
            "향후 5-7년 추가 자금 조달(IPO, 채권 발행 등) 필수",
        ],
        "invest": {
            "strengths": "SMR 기술 세계 유일 NRC 인증, 청정에너지 수혜, 정부 지원",
            "risks": "극도의 높은 손실, 현금 소모 속도, 상용화 지연 리스크, 원전 규제",
            "opportunities": "AI 데이터센터 청정에너지 수요, 정부 에너지 정책 전환, 국제 시장",
            "watchlist": "손실 축소 속도, 정부 계약 수주, 기술 개발 진행, 자금 조달 계획",
        },
    },
}


# SVG CHART FUNCTIONS

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

def svg_earnings_compare(quarters, accent, W=580, H=260):
    labels = [q["q"] for q in quarters]
    pad_l, pad_r, pad_t, pad_b = 60, 20, 30, 50
    cw = W - pad_l - pad_r; ch = H - pad_t - pad_b
    n = len(labels); gw = cw / n; bw = gw * 0.30
    vals = []
    for q in quarters:
        vals.extend([q["rev_est"], q["rev_actual"]])
    mx = max(vals) * 1.15
    def y(v): return pad_t + ch - (v / mx * ch)
    svg = ''
    for i in range(5):
        gv = mx * i / 4; yp = y(gv)
        svg += f'<line x1="{pad_l}" y1="{yp}" x2="{W-pad_r}" y2="{yp}" stroke="rgba(255,255,255,.06)" stroke-dasharray="4,4"/>'
        svg += f'<text x="{pad_l-8}" y="{yp+4}" fill="#9ca0b8" font-size="10" text-anchor="end" font-family="Geist Mono,monospace">${gv:.1f}B</text>'
    for i, q in enumerate(quarters):
        cx = pad_l + i * gw + gw / 2
        bh_est = q["rev_est"] / mx * ch
        svg += f'<rect x="{cx - bw - 2}" y="{y(q["rev_est"])}" width="{bw}" height="{bh_est}" rx="3" fill="rgba(255,255,255,.15)"/>'
        svg += f'<text x="{cx - bw/2 - 2}" y="{y(q["rev_est"])-5}" fill="#9ca0b8" font-size="9" text-anchor="middle" font-family="Geist Mono,monospace">${q["rev_est"]:.1f}B</text>'
        bh_act = q["rev_actual"] / mx * ch
        svg += f'<rect x="{cx + 2}" y="{y(q["rev_actual"])}" width="{bw}" height="{bh_act}" rx="3" fill="{accent}"/>'
        svg += f'<text x="{cx + bw/2 + 2}" y="{y(q["rev_actual"])-5}" fill="{accent}" font-size="9" font-weight="700" text-anchor="middle" font-family="Geist Mono,monospace">${q["rev_actual"]:.1f}B</text>'
        svg += f'<text x="{cx}" y="{H-10}" fill="#9ca0b8" font-size="11" text-anchor="middle">{labels[i]}</text>'
        svg += f'<text x="{cx}" y="{H-25}" fill="{accent}" font-size="9" font-weight="700" text-anchor="middle" font-family="Geist Mono,monospace">{q["rev_beat"]:.1f}%</text>'
    svg += f'<rect x="{W-160}" y="8" width="10" height="10" rx="2" fill="rgba(255,255,255,.15)"/>'
    svg += f'<text x="{W-145}" y="17" fill="#9ca0b8" font-size="10">컨센서스</text>'
    svg += f'<rect x="{W-90}" y="8" width="10" height="10" rx="2" fill="{accent}"/>'
    svg += f'<text x="{W-75}" y="17" fill="#9ca0b8" font-size="10">실제 매출</text>'
    return f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{svg}</svg>'

def svg_eps_surprise(quarters, W=580, H=260):
    labels = [q["q"] for q in quarters]
    pad_l, pad_r, pad_t, pad_b = 60, 20, 30, 50
    cw = W - pad_l - pad_r; ch = H - pad_t - pad_b
    n = len(labels); gw = cw / n; bw = gw * 0.30
    vals = []
    for q in quarters:
        ea = q.get("eps_actual", 0); ee = q.get("eps_est", 0)
        if ea > 0: vals.append(ea)
        if ee > 0: vals.append(ee)
    if not vals: vals = [1]
    mx = max(vals) * 1.20
    def y(v): return pad_t + ch - (v / mx * ch) if v > 0 else pad_t + ch
    svg = ''
    for i in range(5):
        gv = mx * i / 4; yp = y(gv)
        svg += f'<line x1="{pad_l}" y1="{yp}" x2="{W-pad_r}" y2="{yp}" stroke="rgba(255,255,255,.06)" stroke-dasharray="4,4"/>'
        svg += f'<text x="{pad_l-8}" y="{yp+4}" fill="#9ca0b8" font-size="10" text-anchor="end" font-family="Geist Mono,monospace">${gv:.2f}</text>'
    for i, q in enumerate(quarters):
        cx = pad_l + i * gw + gw / 2
        ea = q.get("eps_actual", 0); ee = q.get("eps_est", 0)
        if ee > 0:
            bh_est = ee / mx * ch
            svg += f'<rect x="{cx - bw - 2}" y="{y(ee)}" width="{bw}" height="{bh_est}" rx="3" fill="rgba(255,255,255,.15)"/>'
            svg += f'<text x="{cx - bw/2 - 2}" y="{y(ee)-5}" fill="#9ca0b8" font-size="9" text-anchor="middle" font-family="Geist Mono,monospace">${ee:.2f}</text>'
        if ea > 0:
            bh_act = ea / mx * ch
            svg += f'<rect x="{cx + 2}" y="{y(ea)}" width="{bw}" height="{bh_act}" rx="3" fill="#4ecdc4"/>'
            svg += f'<text x="{cx + bw/2 + 2}" y="{y(ea)-5}" fill="#4ecdc4" font-size="9" font-weight="700" text-anchor="middle" font-family="Geist Mono,monospace">${ea:.2f}</text>'
        svg += f'<text x="{cx}" y="{H-10}" fill="#9ca0b8" font-size="11" text-anchor="middle">{labels[i]}</text>'
        svg += f'<text x="{cx}" y="{H-25}" fill="#4ecdc4" font-size="9" font-weight="700" text-anchor="middle" font-family="Geist Mono,monospace">{q.get("eps_beat","0"):.1f}%</text>'
    svg += f'<rect x="{W-160}" y="8" width="10" height="10" rx="2" fill="rgba(255,255,255,.15)"/>'
    svg += f'<text x="{W-145}" y="17" fill="#9ca0b8" font-size="10">컨센서스</text>'
    svg += f'<rect x="{W-90}" y="8" width="10" height="10" rx="2" fill="#4ecdc4"/>'
    svg += f'<text x="{W-75}" y="17" fill="#9ca0b8" font-size="10">실제 EPS</text>'
    return f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{svg}</svg>'


# HTML HELPER FUNCTIONS

def gen_overview_section(title, subtitle, items, gradient):
    html = f'<div class="section-card"><div class="section-header" style="background:{gradient}"><div class="section-subtitle">{subtitle}</div><div class="section-title">{title}</div></div><div class="section-body">'
    for item in items:
        html += f'<div class="insight-item"><div class="insight-header"><span class="insight-emoji">{item["emoji"]}</span><span class="insight-title">{item["title"]}</span></div><p class="insight-desc">{item["desc"]}</p></div>'
    html += '</div></div>'
    return html

def fmt_mkt_cap(mkt_cap_trillions):
    if mkt_cap_trillions >= 1: return f"${mkt_cap_trillions:.2f}T"
    else: return f"${mkt_cap_trillions*1000:.0f}B"

def generate_stock_html(ticker, data):
    p = data["profile"]
    accent = p["accent"]
    current_price = p["price"]
    income = data["income"]
    quarterly = data["quarterly"]
    earnings_quarters = data["earnings_quarters"]
    overview_money = data["overview_money"]
    overview_growth = data["overview_growth"]
    overview_risks = data["overview_risks"]
    segments = data["segments"]
    quarterly_segments = data["quarterly_segments"]
    quarterly_detail = data["quarterly_detail"]
    ratios = data["ratios"]
    peers = data["peers"]
    invest = data["invest"]
    financial_items = data.get("financial_items", [])

    # Format overview items with emojis
    money_items = [{"emoji": "💰", "title": "수익성", "desc": overview_money[0]},
                   {"emoji": "📈", "title": "현금 창출", "desc": overview_money[1]},
                   {"emoji": "🎯", "title": "세그먼트", "desc": overview_money[2]}]
    growth_items = [{"emoji": "🚀", "title": "성장률", "desc": overview_growth[0]},
                    {"emoji": "📊", "title": "구조", "desc": overview_growth[1]},
                    {"emoji": "⚡", "title": "모멘텀", "desc": overview_growth[2]}]
    risk_items = [{"emoji": "⚠️", "title": "밸류에이션", "desc": overview_risks[0]},
                  {"emoji": "🔄", "title": "경쟁", "desc": overview_risks[1]},
                  {"emoji": "🌍", "title": "거시", "desc": overview_risks[2]}]

    # Revenue + NI chart
    labels_fy = [str(d["year"]) for d in income[-5:]]
    rev_data = [d["rev"] for d in income[-5:]]
    ni_data = [d["ni"] for d in income[-5:]]
    rev_ni_chart = svg_grouped_bar(labels_fy, [{"label": "Revenue", "color": accent, "data": rev_data},
                                              {"label": "Net Income", "color": "#4ecdc4", "data": ni_data}])

    # Margin trends
    gm_data = [d["gm"] for d in income[-5:]]
    om_data = [d["om"] for d in income[-5:]]
    nm_data = [d["nm"] for d in income[-5:]]
    margin_chart = svg_line_chart(labels_fy, [{"label": "GM", "color": accent, "data": gm_data},
                                             {"label": "OM", "color": "#4ecdc4", "data": om_data},
                                             {"label": "NM", "color": "#ffa94d", "data": nm_data}])

    # Segment revenue
    segment_slices = [{"name": seg["name"], "value": seg["values"][-1], "color": seg["color"]} for seg in segments["data"]]
    segment_chart = svg_donut(segment_slices)

    # Quarterly segments stacked
    quarterly_series = [{"name": seg["name"], "color": seg["color"], "data": seg["values"]} for seg in quarterly_segments["data"]]
    quarterly_chart = svg_stacked_bar(quarterly_segments["labels"], quarterly_series)

    # EPS + P/E
    eps_pe_chart = svg_eps_per(income[-5:], current_price, accent)

    # Earnings compare
    earnings_compare_chart = svg_earnings_compare(earnings_quarters, accent)

    # EPS surprise
    eps_surprise_chart = svg_eps_surprise(earnings_quarters)

    # Peer comparison table
    peer_html = '<table class="peer-table"><thead><tr><th>종목</th><th>시가총액</th><th>P/E</th><th>P/S</th><th>매출</th><th>순이익률</th></tr></thead><tbody>'
    for peer in peers:
        hl = " style='background:rgba(255,255,255,.08);font-weight:700'" if peer.get("highlight") else ""
        peer_html += f'<tr{hl}><td>{peer["ticker"]}</td><td>{peer["mktCap"]}</td><td>{peer["pe"]}</td><td>{peer["ps"]}</td><td>{peer["rev"]}</td><td>{peer["nm"]}</td></tr>'
    peer_html += '</tbody></table>'

    # Financial items / commentary
    fin_html = '<div class="fin-commentary">'
    for item in financial_items[:4]:
        fin_html += f'<div class="fin-item-comment"><span class="comment-bullet">▸</span> {item}</div>'
    fin_html += '</div>'

    # Next earnings
    next_earnings = data.get("next_earnings", {})
    earnings_html = f'''<div class="earnings-box">
<div class="earnings-date">다음 실적발표: <strong>{next_earnings.get("date", "TBA")}</strong></div>
<div class="earnings-period">{next_earnings.get("period", "TBA")}</div>
<div class="earnings-consensus">
  <div class="consensus-item">
    <div class="consensus-label">매출 컨센서스</div>
    <div class="consensus-value">{next_earnings.get("rev_consensus", "TBA")}</div>
  </div>
  <div class="consensus-item">
    <div class="consensus-label">EPS 컨센서스</div>
    <div class="consensus-value">{next_earnings.get("eps", "TBA")}</div>
  </div>
</div>
</div>'''

    html = f'''<!-- {ticker} STOCK DETAIL -->
<div class="stock-detail" id="stock-{ticker}" style="display:none;">
<div class="stock-header" style="background: linear-gradient(135deg, {accent}22, {accent}11);">
  <div class="stock-info">
    <div class="stock-symbol">{p["symbol"]}</div>
    <div class="stock-name">{p["name"]}</div>
    <div class="stock-meta">
      <span class="meta-item">{p["sector"]} · {p["industry"]}</span>
      <span class="meta-item">{p["country"]}</span>
    </div>
  </div>
  <div class="stock-price-box">
    <div class="stock-price">${p["price"]:.2f}</div>
    <div class="stock-change" style="color: {'var(--green)' if p['changes']>0 else 'var(--red)'};">
      {'+' if p['changes']>0 else ''}{p['changes']:.2f} ({'+' if p['changesPct']>0 else ''}{p['changesPct']:.2f}%)
    </div>
  </div>
  <div class="stock-kpi">
    <div class="kpi-item"><div class="kpi-label">시가총액</div><div class="kpi-value">{fmt_mkt_cap(p['mktCap'])}</div></div>
    <div class="kpi-item"><div class="kpi-label">P/E</div><div class="kpi-value">{ratios.get("pe", "-")}</div></div>
    <div class="kpi-item"><div class="kpi-label">P/S</div><div class="kpi-value">{ratios.get("ps", "-")}</div></div>
    <div class="kpi-item"><div class="kpi-label">ROE</div><div class="kpi-value">{ratios.get("roe", "-")}%</div></div>
  </div>
</div>

<div class="tab-nav">
  <button class="tab-btn active" onclick="st('{ticker}', 'overview')">기업 개요</button>
  <button class="tab-btn" onclick="st('{ticker}', 'financial')">재무 분석</button>
  <button class="tab-btn" onclick="st('{ticker}', 'segment')">사업부문</button>
  <button class="tab-btn" onclick="st('{ticker}', 'valuation')">밸류에이션</button>
  <button class="tab-btn" onclick="st('{ticker}', 'earnings')">실적발표</button>
  <button class="tab-btn" onclick="st('{ticker}', 'invest')">투자 포인트</button>
</div>

<div class="tab-content active" id="t-{ticker}-overview">
  {gen_overview_section("수익성 분석", "💵 Financial Strength", money_items, f"linear-gradient(135deg, {accent}, {accent}cc)")}
  {gen_overview_section("성장 분석", "📈 Growth Trajectory", growth_items, "linear-gradient(135deg, #4ecdc4, #4ecdc4cc)")}
  {gen_overview_section("리스크 분석", "⚠️ Risk Assessment", risk_items, "linear-gradient(135deg, #ff6b6b, #ff6b6bcc)")}
</div>

<div class="tab-content" id="t-{ticker}-financial">
  <div class="section-card">
    <div class="section-header" style="background:{accent}">
      <div class="section-title">매출 & 순이익</div>
    </div>
    <div class="chart-container">{rev_ni_chart}</div>
  </div>

  <div class="section-card">
    <div class="section-header" style="background:#4ecdc4">
      <div class="section-title">마진 추이</div>
    </div>
    <div class="chart-container">{margin_chart}</div>
  </div>

  <div class="section-card">
    <div class="section-title" style="padding:16px;">재무 분석 코멘트</div>
    {fin_html}
  </div>
</div>

<div class="tab-content" id="t-{ticker}-segment">
  <div class="section-card">
    <div class="section-header" style="background:{accent}">
      <div class="section-title">세그먼트 수익 (FY{income[-1]['year']})</div>
    </div>
    <div class="chart-container">{segment_chart}</div>
  </div>

  <div class="section-card">
    <div class="section-header" style="background:#4ecdc4">
      <div class="section-title">분기별 세그먼트 추이</div>
    </div>
    <div class="chart-container">{quarterly_chart}</div>
  </div>
</div>

<div class="tab-content" id="t-{ticker}-valuation">
  <div class="section-card">
    <div class="section-header" style="background:{accent}">
      <div class="section-title">EPS & P/E 추이</div>
    </div>
    <div class="chart-container">{eps_pe_chart}</div>
  </div>

  <div class="section-card">
    <div class="section-title" style="padding:16px;">경쟁사 비교</div>
    {peer_html}
  </div>
</div>

<div class="tab-content" id="t-{ticker}-earnings">
  <div class="section-card">
    <div class="section-header" style="background:{accent}">
      <div class="section-title">분기별 매출 실적</div>
    </div>
    <div class="chart-container">{earnings_compare_chart}</div>
  </div>

  <div class="section-card">
    <div class="section-header" style="background:#4ecdc4">
      <div class="section-title">분기별 EPS 실적</div>
    </div>
    <div class="chart-container">{eps_surprise_chart}</div>
  </div>

  <div class="section-card">
    {earnings_html}
  </div>
</div>

<div class="tab-content" id="t-{ticker}-invest">
  <div class="swot-grid">
    <div class="swot-card swot-strengths">
      <div class="swot-title">강점 (Strengths)</div>
      <p>{invest.get("strengths", "")}</p>
    </div>
    <div class="swot-card swot-risks">
      <div class="swot-title">약점 (Risks)</div>
      <p>{invest.get("risks", "")}</p>
    </div>
    <div class="swot-card swot-opportunities">
      <div class="swot-title">기회 (Opportunities)</div>
      <p>{invest.get("opportunities", "")}</p>
    </div>
    <div class="swot-card swot-watchlist">
      <div class="swot-title">주시사항 (Watchlist)</div>
      <p>{invest.get("watchlist", "")}</p>
    </div>
  </div>
</div>

</div><!-- END {ticker} -->
'''
    return html

def generate_portfolio_summary():
    total_mktcap = sum(data["profile"]["mktCap"] for data in STOCKS.values())
    total_stocks = len(STOCKS)

    # Sector allocation
    sectors = {}
    for ticker, data in STOCKS.items():
        sector = data["profile"]["sector"]
        mktcap = data["profile"]["mktCap"]
        if sector not in sectors: sectors[sector] = 0
        sectors[sector] += mktcap

    sector_slices = [{"name": s, "value": v, "color": next(iter([d["profile"]["accent"] for d in STOCKS.values() if d["profile"]["sector"]==s]))} for s, v in sorted(sectors.items(), key=lambda x: x[1], reverse=True)]
    sector_chart = svg_donut(sector_slices)

    # Stock cards
    stock_cards_html = ''
    for ticker, data in sorted(STOCKS.items()):
        p = data["profile"]
        ytd_change = p.get("changesPct", 0)
        stock_cards_html += f'''<div class="port-card" onclick="selectStock('{ticker}')">
  <div class="port-card-header">
    <div class="port-ticker" style="color:{p['accent']}">{p['symbol']}</div>
    <div class="port-price" style="color:{'var(--green)' if ytd_change>0 else 'var(--red)'};">{'+' if ytd_change>0 else ''}{ytd_change:.2f}%</div>
  </div>
  <div class="port-name">{p['name']}</div>
  <div class="port-meta">{p['sector']} · {p['industry']}</div>
  <div class="port-kpi">
    <div><strong>${p['price']:.2f}</strong><br/><span class="kpi-label">현재가</span></div>
    <div><strong>{fmt_mkt_cap(p['mktCap'])}</strong><br/><span class="kpi-label">시총</span></div>
  </div>
</div>'''

    return f'''<!-- PORTFOLIO SUMMARY -->
<div id="portfolio-summary">
<div class="summary-header">
  <h1>StockLens 포트폴리오</h1>
  <p class="summary-subtitle">10 대표 기술·헬스케어·부동산 기업 분석</p>
</div>

<div class="kpi-row">
  <div class="kpi-card">
    <div class="kpi-label">포트폴리오 규모</div>
    <div class="kpi-value" style="font-size:28px;">{fmt_mkt_cap(total_mktcap)}</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">보유 종목</div>
    <div class="kpi-value" style="font-size:28px;">{total_stocks}</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">최대 보유</div>
    <div class="kpi-value" style="font-size:18px;">{max(STOCKS.items(), key=lambda x: x[1]['profile']['mktCap'])[0]}</div>
  </div>
</div>

<div class="section-card">
  <div class="section-title" style="padding:16px;">섹터 할당</div>
  <div class="chart-container">{sector_chart}</div>
</div>

<div class="section-title" style="padding:16px; margin-top:32px;">포트폴리오 종목</div>
<div class="portfolio-grid">
  {stock_cards_html}
</div>
</div><!-- END PORTFOLIO SUMMARY -->
'''

def generate_full_html():
    # Build all stock HTML
    # Custom order: NVDA first, then alphabetical rest
    ticker_order = ["NVDA", "AAPL", "MSFT", "GOOGL", "O", "ABBV", "PLTR", "CRWV", "IONQ", "SMR"]

    stock_sections = {}
    for ticker in ticker_order:
        stock_sections[ticker] = generate_stock_html(ticker, STOCKS[ticker])

    # Stock selector bar — NVDA active by default, no portfolio tab
    stock_bar = '<div class="stock-bar">'
    for ticker in ticker_order:
        accent = STOCKS[ticker]["profile"]["accent"]
        active = ' active' if ticker == 'NVDA' else ''
        stock_bar += f'<button class="stock-pill{active}" onclick="selectStock(\'{ticker}\')" style="--pill-accent:{accent}">{ticker}</button>'
    stock_bar += '</div>'

    # All stock sections combined, NVDA visible by default
    all_stock_html = ''
    for ticker in ticker_order:
        section = stock_sections[ticker]
        if ticker == 'NVDA':
            section = section.replace(f'style="display:none;"', '', 1)
        all_stock_html += section + '\n'

    full_html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>StockLens — 포트폴리오 대시보드</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root {{
  --bg-primary: #0a0e27;
  --bg-secondary: #12172e;
  --bg-tertiary: #1a1f3a;
  --border: rgba(255,255,255,.08);
  --text-primary: #e4e6f0;
  --text-secondary: #9ca0b8;
  --green: #34a853;
  --red: #ff6b6b;
}}

* {{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}}

html, body {{
  background: var(--bg-primary);
  color: var(--text-primary);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Pretendard", sans-serif;
  font-size: 14px;
  line-height: 1.6;
}}

.main-header {{
  position: sticky;
  top: 0;
  z-index: 1000;
  background: var(--bg-primary);
  border-bottom: 1px solid var(--border);
  padding: 16px 24px;
  backdrop-filter: blur(8px);
}}

.header-content {{
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}}

.header-logo {{
  font-size: 20px;
  font-weight: 700;
  background: linear-gradient(135deg, #76b900, #4ecdc4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}}

.update-info {{
  font-size: 12px;
  color: var(--text-secondary);
}}

/* Update Bar — Supanova style */
.update-bar {{
  background: linear-gradient(90deg, rgba(118,185,0,.06), rgba(78,205,196,.04));
  border-bottom: 1px solid var(--border);
  padding: 10px 24px;
  display: flex;
  align-items: center;
  gap: 24px;
  flex-wrap: wrap;
  font-size: 12px;
  color: var(--text-secondary);
  max-width: 1200px;
  margin: 0 auto;
}}
.ub-item {{ display: flex; align-items: center; gap: 6px; }}
.ub-icon {{ font-size: 14px; }}
.ub-label {{ color: var(--text-secondary); opacity: .7; }}
.ub-value {{ color: var(--text-primary); font-weight: 600; font-family: 'Geist Mono', monospace; }}
.ub-next {{
  margin-left: auto;
  background: rgba(255,165,0,.1);
  border: 1px solid rgba(255,165,0,.25);
  border-radius: 20px;
  padding: 5px 14px;
  color: #ffa500;
  font-weight: 700;
  font-size: 11px;
  display: flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
}}
.ub-next .ub-blink {{
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #ffa500;
  animation: blink 1.5s infinite;
}}
@keyframes blink {{ 0%,100%{{ opacity:1 }} 50%{{ opacity:.3 }} }}
@media(max-width:768px){{
  .update-bar {{ padding: 8px 16px; gap: 12px; font-size: 11px; }}
  .ub-next {{ margin-left: 0; width: 100%; justify-content: center; }}
}}

.stock-bar {{
  max-width: 1200px;
  margin: 0 auto;
  padding: 12px 24px;
  display: flex;
  gap: 8px;
  overflow-x: auto;
  border-bottom: 1px solid var(--border);
}}

.stock-pill {{
  padding: 8px 16px;
  border: 1px solid var(--border);
  background: transparent;
  color: var(--text-secondary);
  border-radius: 20px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
  transition: all 0.3s ease;
}}

.stock-pill:hover {{
  color: var(--text-primary);
  border-color: var(--pill-accent, var(--text-secondary));
}}

.stock-pill.active {{
  background: color-mix(in srgb, var(--pill-accent, #4ecdc4) 15%, transparent);
  border-color: var(--pill-accent, #4ecdc4);
  color: var(--pill-accent, #4ecdc4);
  font-weight: 700;
}}

.container {{
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 24px;
}}

#portfolio-summary {{
  animation: fadeIn 0.3s ease;
}}

.summary-header {{
  margin-bottom: 32px;
}}

.summary-header h1 {{
  font-size: 32px;
  margin-bottom: 8px;
  background: linear-gradient(135deg, #76b900, #4ecdc4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}}

.summary-subtitle {{
  color: var(--text-secondary);
  font-size: 15px;
}}

.kpi-row {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 32px;
}}

.kpi-card {{
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  text-align: center;
}}

.kpi-label {{
  color: var(--text-secondary);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}}

.kpi-value {{
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
}}

.portfolio-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  margin-top: 16px;
}}

.port-card {{
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}}

.port-card:hover {{
  border-color: rgba(255,255,255,.15);
  transform: translateY(-2px);
}}

.port-card-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}}

.port-ticker {{
  font-weight: 700;
  font-size: 16px;
}}

.port-price {{
  font-size: 13px;
  font-weight: 600;
}}

.port-name {{
  font-size: 13px;
  color: var(--text-primary);
  margin-bottom: 4px;
}}

.port-meta {{
  font-size: 11px;
  color: var(--text-secondary);
  margin-bottom: 12px;
}}

.port-kpi {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  font-size: 11px;
}}

.port-kpi div {{
  text-align: center;
}}

.port-kpi strong {{
  display: block;
  font-size: 13px;
  margin-bottom: 4px;
}}

.stock-detail {{
  animation: fadeIn 0.3s ease;
}}

.stock-header {{
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  display: grid;
  grid-template-columns: 1fr 200px 300px;
  gap: 24px;
  align-items: center;
  border: 1px solid var(--border);
}}

.stock-symbol {{
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
}}

.stock-name {{
  font-size: 16px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}}

.stock-meta {{
  font-size: 12px;
  color: var(--text-secondary);
}}

.meta-item {{
  display: inline-block;
  margin-right: 16px;
}}

.stock-price {{
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
}}

.stock-change {{
  font-size: 12px;
  margin-top: 4px;
}}

.stock-kpi {{
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}}

.kpi-item {{
  text-align: center;
}}

.tab-nav {{
  display: flex;
  gap: 8px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 24px;
  flex-wrap: wrap;
}}

.tab-btn {{
  padding: 12px 16px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  border-bottom: 2px solid transparent;
  transition: all 0.3s ease;
}}

.tab-btn:hover {{
  color: var(--text-primary);
}}

.tab-btn.active {{
  color: var(--text-primary);
  border-bottom-color: #4ecdc4;
}}

.tab-content {{
  display: none;
}}

.tab-content.active {{
  display: block;
}}

.section-card {{
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 24px;
}}

.section-header {{
  padding: 16px;
  background: linear-gradient(135deg, #76b900, #4ecdc4);
}}

.section-subtitle {{
  font-size: 12px;
  color: rgba(255,255,255,.7);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
}}

.section-title {{
  font-size: 16px;
  font-weight: 700;
  color: white;
}}

.section-body {{
  padding: 24px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 16px;
}}

.insight-item {{
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: 8px;
}}

.insight-header {{
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}}

.insight-emoji {{
  font-size: 20px;
}}

.insight-title {{
  font-weight: 600;
  font-size: 13px;
}}

.insight-desc {{
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.5;
}}

.chart-container {{
  padding: 24px;
  background: var(--bg-primary);
}}

.fin-commentary {{
  padding: 24px;
}}

.fin-item-comment {{
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 12px;
  padding-left: 12px;
}}

.comment-bullet {{
  color: var(--text-secondary);
  margin-right: 8px;
}}

.peer-table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}}

.peer-table thead {{
  background: var(--bg-tertiary);
  border-bottom: 1px solid var(--border);
}}

.peer-table th {{
  padding: 12px;
  text-align: left;
  color: var(--text-secondary);
  font-weight: 600;
}}

.peer-table td {{
  padding: 12px;
  border-bottom: 1px solid var(--border);
}}

.peer-table tbody tr:hover {{
  background: var(--bg-tertiary);
}}

.earnings-box {{
  background: var(--bg-tertiary);
  padding: 20px;
  border-radius: 8px;
  border: 1px solid var(--border);
}}

.earnings-date {{
  font-size: 14px;
  margin-bottom: 8px;
}}

.earnings-period {{
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 16px;
}}

.earnings-consensus {{
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}}

.consensus-item {{
  background: var(--bg-primary);
  padding: 12px;
  border-radius: 6px;
}}

.consensus-label {{
  font-size: 11px;
  color: var(--text-secondary);
  margin-bottom: 4px;
}}

.consensus-value {{
  font-size: 14px;
  font-weight: 700;
}}

.swot-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
  margin-top: 16px;
}}

.swot-card {{
  background: var(--bg-tertiary);
  padding: 20px;
  border-radius: 12px;
  border: 1px solid var(--border);
}}

.swot-strengths {{ border-left: 4px solid var(--green); }}
.swot-risks {{ border-left: 4px solid var(--red); }}
.swot-opportunities {{ border-left: 4px solid #ffa94d; }}
.swot-watchlist {{ border-left: 4px solid #4ecdc4; }}

.swot-title {{
  font-weight: 700;
  margin-bottom: 12px;
  font-size: 13px;
}}

.swot-card p {{
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.6;
}}

@keyframes fadeIn {{
  from {{ opacity: 0; transform: translateY(8px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}

@media (max-width: 768px) {{
  .stock-header {{
    grid-template-columns: 1fr;
  }}

  .portfolio-grid {{
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }}
}}
</style>
</head>
<body>

<div class="main-header">
  <div class="header-content">
    <div class="header-logo">📊 StockLens <span style="font-size:13px;font-weight:400;color:var(--text-secondary);margin-left:8px;">포트폴리오 대시보드</span></div>
    <div class="update-info">
      10종목 통합 분석
    </div>
  </div>
</div>

<div class="update-bar">
  <div class="ub-item"><span class="ub-icon">📊</span><span class="ub-label">작성기준일</span><span class="ub-value">{DASHBOARD_META['created_date']}</span></div>
  <div class="ub-item"><span class="ub-icon">📋</span><span class="ub-label">데이터</span><span class="ub-value">{DASHBOARD_META['data_basis']}</span></div>
  <div class="ub-next"><span class="ub-blink"></span> {DASHBOARD_META['next_update_ticker']} {DASHBOARD_META['next_update_date']} {DASHBOARD_META['next_update_event']} 이후 업데이트 필요</div>
</div>

{stock_bar}

<div class="container">
{all_stock_html}
</div>

<script>
let currentStock = 'NVDA';

function selectStock(ticker) {{
  // Hide all stock details
  document.querySelectorAll('.stock-detail').forEach(el => el.style.display = 'none');

  // Show selected stock
  const target = document.getElementById('stock-' + ticker);
  if (target) {{
    target.style.display = 'block';
    // Reset to first tab
    const detail = target;
    detail.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    detail.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    const firstBtn = detail.querySelector('.tab-btn');
    if (firstBtn) firstBtn.classList.add('active');
    const firstTab = document.getElementById('t-' + ticker + '-overview');
    if (firstTab) firstTab.classList.add('active');
  }}

  // Update pill styles
  document.querySelectorAll('.stock-pill').forEach(pill => {{
    pill.classList.remove('active');
    if (pill.textContent === ticker) pill.classList.add('active');
  }});

  currentStock = ticker;
  window.scrollTo({{ top: 0, behavior: 'smooth' }});
}}

function st(ticker, tabName) {{
  const detail = document.getElementById('stock-' + ticker);
  if (!detail) return;
  detail.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
  detail.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));

  event.target.classList.add('active');
  const tab = document.getElementById('t-' + ticker + '-' + tabName);
  if (tab) tab.classList.add('active');
}}

// Intersection Observer for scroll animations
const observer = new IntersectionObserver(entries => {{
  entries.forEach(entry => {{
    if (entry.isIntersecting) {{
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }}
  }});
}}, {{ threshold: 0.1 }});

document.querySelectorAll('.section-card, .port-card').forEach(el => {{
  el.style.opacity = '0';
  el.style.transform = 'translateY(8px)';
  el.style.transition = 'all 0.4s ease';
  observer.observe(el);
}});
</script>

</body>
</html>
'''

    return full_html

if __name__ == "__main__":
    html = generate_full_html()
    out_dir = "mnt/02-projects/2026.03.28 기업분석대시보드/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "기업분석_포트폴리오대시보드_v1_2026.03.28.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Portfolio dashboard generated: {out_path}")
