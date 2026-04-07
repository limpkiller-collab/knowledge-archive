#!/usr/bin/env python3
"""Portfolio Dashboard v5 — 10종목 멀티 스톡 대시보드, v13 Supanova 디자인 기반
- 10개 종목 개별 분석 (NVDA, AAPL, MSFT, GOOGL, O, ABBV, PLTR, CRWV, IONQ, SMR)
- 각 종목별 6개 탭 (기업개요, 재무분석, 사업부문, 밸류에이션, 실적발표, 투자포인트)
- 주식 선택 바로 스톡별 탭 전환 가능
- v13 디자인 시스템, CSS, SVG 차트 완전 동일
- 단일 HTML 파일 결과물
"""
import math
import os
import sys

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD META
# ══════════════════════════════════════════════════════════════════════════════

DASHBOARD_META = {
    "created_date": "2026.03.28",
    "data_basis": "2026.03.28 기준 최신 공시 데이터",
    "data_source": "IR Newsroom, SEC Filings, FactSet Consensus",
    "next_update_event": "Q1 FY2027 실적발표 (NVDA)",
    "next_update_date": "2026.05.28 (수) 한국시간",
    "next_update_ticker": "NVDA",
}

# ══════════════════════════════════════════════════════════════════════════════
# LOAD STOCK DATA FROM FILES
# ══════════════════════════════════════════════════════════════════════════════

sys.path.insert(0, '/sessions/exciting-gracious-pasteur')

# Group 1: AAPL, MSFT, GOOGL (structured as TICKER_DATA dicts)
from stock_data_group1 import AAPL_DATA, MSFT_DATA, GOOGL_DATA

# O: Realty Income (prefixed with O_)
import stock_data_O as _o
O_DATA = {
    "profile": _o.O_PROFILE,
    "income": _o.O_INCOME,
    "quarterly": _o.O_QUARTERLY,
    "extra": _o.O_EXTRA if hasattr(_o, 'O_EXTRA') else {},
    "segments": _o.O_SEGMENTS if hasattr(_o, 'O_SEGMENTS') else {"labels":[], "series":[]},
    "quarterly_segments": _o.O_QUARTERLY_SEGMENTS if hasattr(_o, 'O_QUARTERLY_SEGMENTS') else {"labels":[], "series":[]},
    "quarterly_detail": _o.O_QUARTERLY_DETAIL if hasattr(_o, 'O_QUARTERLY_DETAIL') else [],
    "quarterly_financial_items": _o.O_QUARTERLY_FINANCIAL_ITEMS if hasattr(_o, 'O_QUARTERLY_FINANCIAL_ITEMS') else [],
    "financial_items": _o.O_FINANCIAL_ITEMS if hasattr(_o, 'O_FINANCIAL_ITEMS') else [],
    "next_earnings": _o.O_NEXT_EARNINGS if hasattr(_o, 'O_NEXT_EARNINGS') else {"key_watch":[]},
    "peers": _o.O_PEERS if hasattr(_o, 'O_PEERS') else [],
    "ratios": _o.O_RATIOS if hasattr(_o, 'O_RATIOS') else {},
    "invest": _o.O_INVEST if hasattr(_o, 'O_INVEST') else {"strengths":[], "risks":[], "opportunities":[], "watchlist":[]},
    "overview_money": _o.O_OVERVIEW_MONEY if hasattr(_o, 'O_OVERVIEW_MONEY') else [],
    "overview_growth": _o.O_OVERVIEW_GROWTH if hasattr(_o, 'O_OVERVIEW_GROWTH') else [],
    "overview_risks": _o.O_OVERVIEW_RISKS if hasattr(_o, 'O_OVERVIEW_RISKS') else [],
    "earnings_quarters": _o.O_EARNINGS_QUARTERS if hasattr(_o, 'O_EARNINGS_QUARTERS') else [],
}

# ABBV: AbbVie (unprefixed PROFILE, INCOME, etc.)
_abbv_ns = {}
with open('/sessions/exciting-gracious-pasteur/stock_data_ABBV.py') as f:
    exec(f.read(), _abbv_ns)
ABBV_DATA = {
    "profile": _abbv_ns.get("PROFILE", {}),
    "income": _abbv_ns.get("INCOME", []),
    "quarterly": _abbv_ns.get("QUARTERLY", []),
    "extra": _abbv_ns.get("EXTRA", {}),
    "segments": _abbv_ns.get("SEGMENTS", {"labels":[], "series":[]}),
    "quarterly_segments": _abbv_ns.get("QUARTERLY_SEGMENTS", {"labels":[], "series":[]}),
    "quarterly_detail": _abbv_ns.get("QUARTERLY_DETAIL", []),
    "quarterly_financial_items": _abbv_ns.get("QUARTERLY_FINANCIAL_ITEMS", []),
    "financial_items": _abbv_ns.get("FINANCIAL_ITEMS", []),
    "next_earnings": _abbv_ns.get("NEXT_EARNINGS", {"key_watch":[]}),
    "peers": _abbv_ns.get("PEERS", []),
    "ratios": _abbv_ns.get("RATIOS", {}),
    "invest": _abbv_ns.get("INVEST", {"strengths":[], "risks":[], "opportunities":[], "watchlist":[]}),
    "overview_money": _abbv_ns.get("OVERVIEW_MONEY", []),
    "overview_growth": _abbv_ns.get("OVERVIEW_GROWTH", []),
    "overview_risks": _abbv_ns.get("OVERVIEW_RISKS", []),
    "earnings_quarters": _abbv_ns.get("EARNINGS_QUARTERS", []),
}

# PLTR: Palantir (unprefixed)
_pltr_ns = {}
with open('/sessions/exciting-gracious-pasteur/stock_data_PLTR.py') as f:
    exec(f.read(), _pltr_ns)
PLTR_DATA = {
    "profile": _pltr_ns.get("PROFILE", {}),
    "income": _pltr_ns.get("INCOME", []),
    "quarterly": _pltr_ns.get("QUARTERLY", []),
    "extra": _pltr_ns.get("EXTRA", {}),
    "segments": _pltr_ns.get("SEGMENTS", {"labels":[], "series":[]}),
    "quarterly_segments": _pltr_ns.get("QUARTERLY_SEGMENTS", {"labels":[], "series":[]}),
    "quarterly_detail": _pltr_ns.get("QUARTERLY_DETAIL", []),
    "quarterly_financial_items": _pltr_ns.get("QUARTERLY_FINANCIAL_ITEMS", []),
    "financial_items": _pltr_ns.get("FINANCIAL_ITEMS", []),
    "next_earnings": _pltr_ns.get("NEXT_EARNINGS", {"key_watch":[]}),
    "peers": _pltr_ns.get("PEERS", []),
    "ratios": _pltr_ns.get("RATIOS", {}),
    "invest": _pltr_ns.get("INVEST", {"strengths":[], "risks":[], "opportunities":[], "watchlist":[]}),
    "overview_money": _pltr_ns.get("OVERVIEW_MONEY", []),
    "overview_growth": _pltr_ns.get("OVERVIEW_GROWTH", []),
    "overview_risks": _pltr_ns.get("OVERVIEW_RISKS", []),
    "earnings_quarters": _pltr_ns.get("EARNINGS_QUARTERS", []),
}

# Group 3: CRWV, IONQ, SMR (ticker-prefixed: CRWV_PROFILE, etc.)
import stock_data_group3 as _g3
CRWV_DATA = {
    "profile": _g3.CRWV_PROFILE,
    "income": _g3.CRWV_INCOME,
    "quarterly": _g3.CRWV_QUARTERLY,
    "extra": _g3.CRWV_EXTRA if hasattr(_g3, 'CRWV_EXTRA') else {},
    "segments": _g3.CRWV_SEGMENTS if hasattr(_g3, 'CRWV_SEGMENTS') else {"labels":[], "series":[]},
    "quarterly_segments": _g3.CRWV_QUARTERLY_SEGMENTS if hasattr(_g3, 'CRWV_QUARTERLY_SEGMENTS') else {"labels":[], "series":[]},
    "quarterly_detail": _g3.CRWV_QUARTERLY_DETAIL if hasattr(_g3, 'CRWV_QUARTERLY_DETAIL') else [],
    "quarterly_financial_items": _g3.CRWV_QUARTERLY_FINANCIAL_ITEMS if hasattr(_g3, 'CRWV_QUARTERLY_FINANCIAL_ITEMS') else [],
    "financial_items": _g3.CRWV_FINANCIAL_ITEMS if hasattr(_g3, 'CRWV_FINANCIAL_ITEMS') else [],
    "next_earnings": _g3.CRWV_NEXT_EARNINGS if hasattr(_g3, 'CRWV_NEXT_EARNINGS') else {"key_watch":[]},
    "peers": _g3.CRWV_PEERS if hasattr(_g3, 'CRWV_PEERS') else [],
    "ratios": _g3.CRWV_RATIOS if hasattr(_g3, 'CRWV_RATIOS') else {},
    "invest": _g3.CRWV_INVEST if hasattr(_g3, 'CRWV_INVEST') else {"strengths":[], "risks":[], "opportunities":[], "watchlist":[]},
    "overview_money": _g3.CRWV_OVERVIEW_MONEY if hasattr(_g3, 'CRWV_OVERVIEW_MONEY') else [],
    "overview_growth": _g3.CRWV_OVERVIEW_GROWTH if hasattr(_g3, 'CRWV_OVERVIEW_GROWTH') else [],
    "overview_risks": _g3.CRWV_OVERVIEW_RISKS if hasattr(_g3, 'CRWV_OVERVIEW_RISKS') else [],
    "earnings_quarters": _g3.CRWV_EARNINGS_QUARTERS if hasattr(_g3, 'CRWV_EARNINGS_QUARTERS') else [],
}

IONQ_DATA = {
    "profile": _g3.IONQ_PROFILE,
    "income": _g3.IONQ_INCOME,
    "quarterly": _g3.IONQ_QUARTERLY,
    "extra": _g3.IONQ_EXTRA if hasattr(_g3, 'IONQ_EXTRA') else {},
    "segments": _g3.IONQ_SEGMENTS if hasattr(_g3, 'IONQ_SEGMENTS') else {"labels":[], "series":[]},
    "quarterly_segments": _g3.IONQ_QUARTERLY_SEGMENTS if hasattr(_g3, 'IONQ_QUARTERLY_SEGMENTS') else {"labels":[], "series":[]},
    "quarterly_detail": _g3.IONQ_QUARTERLY_DETAIL if hasattr(_g3, 'IONQ_QUARTERLY_DETAIL') else [],
    "quarterly_financial_items": _g3.IONQ_QUARTERLY_FINANCIAL_ITEMS if hasattr(_g3, 'IONQ_QUARTERLY_FINANCIAL_ITEMS') else [],
    "financial_items": _g3.IONQ_FINANCIAL_ITEMS if hasattr(_g3, 'IONQ_FINANCIAL_ITEMS') else [],
    "next_earnings": _g3.IONQ_NEXT_EARNINGS if hasattr(_g3, 'IONQ_NEXT_EARNINGS') else {"key_watch":[]},
    "peers": _g3.IONQ_PEERS if hasattr(_g3, 'IONQ_PEERS') else [],
    "ratios": _g3.IONQ_RATIOS if hasattr(_g3, 'IONQ_RATIOS') else {},
    "invest": _g3.IONQ_INVEST if hasattr(_g3, 'IONQ_INVEST') else {"strengths":[], "risks":[], "opportunities":[], "watchlist":[]},
    "overview_money": _g3.IONQ_OVERVIEW_MONEY if hasattr(_g3, 'IONQ_OVERVIEW_MONEY') else [],
    "overview_growth": _g3.IONQ_OVERVIEW_GROWTH if hasattr(_g3, 'IONQ_OVERVIEW_GROWTH') else [],
    "overview_risks": _g3.IONQ_OVERVIEW_RISKS if hasattr(_g3, 'IONQ_OVERVIEW_RISKS') else [],
    "earnings_quarters": _g3.IONQ_EARNINGS_QUARTERS if hasattr(_g3, 'IONQ_EARNINGS_QUARTERS') else [],
}

SMR_DATA = {
    "profile": _g3.SMR_PROFILE,
    "income": _g3.SMR_INCOME,
    "quarterly": _g3.SMR_QUARTERLY,
    "extra": _g3.SMR_EXTRA if hasattr(_g3, 'SMR_EXTRA') else {},
    "segments": _g3.SMR_SEGMENTS if hasattr(_g3, 'SMR_SEGMENTS') else {"labels":[], "series":[]},
    "quarterly_segments": _g3.SMR_QUARTERLY_SEGMENTS if hasattr(_g3, 'SMR_QUARTERLY_SEGMENTS') else {"labels":[], "series":[]},
    "quarterly_detail": _g3.SMR_QUARTERLY_DETAIL if hasattr(_g3, 'SMR_QUARTERLY_DETAIL') else [],
    "quarterly_financial_items": _g3.SMR_QUARTERLY_FINANCIAL_ITEMS if hasattr(_g3, 'SMR_QUARTERLY_FINANCIAL_ITEMS') else [],
    "financial_items": _g3.SMR_FINANCIAL_ITEMS if hasattr(_g3, 'SMR_FINANCIAL_ITEMS') else [],
    "next_earnings": _g3.SMR_NEXT_EARNINGS if hasattr(_g3, 'SMR_NEXT_EARNINGS') else {"key_watch":[]},
    "peers": _g3.SMR_PEERS if hasattr(_g3, 'SMR_PEERS') else [],
    "ratios": _g3.SMR_RATIOS if hasattr(_g3, 'SMR_RATIOS') else {},
    "invest": _g3.SMR_INVEST if hasattr(_g3, 'SMR_INVEST') else {"strengths":[], "risks":[], "opportunities":[], "watchlist":[]},
    "overview_money": _g3.SMR_OVERVIEW_MONEY if hasattr(_g3, 'SMR_OVERVIEW_MONEY') else [],
    "overview_growth": _g3.SMR_OVERVIEW_GROWTH if hasattr(_g3, 'SMR_OVERVIEW_GROWTH') else [],
    "overview_risks": _g3.SMR_OVERVIEW_RISKS if hasattr(_g3, 'SMR_OVERVIEW_RISKS') else [],
    "earnings_quarters": _g3.SMR_EARNINGS_QUARTERS if hasattr(_g3, 'SMR_EARNINGS_QUARTERS') else [],
}

# For NVDA, we'll create minimal data structure for portfolio view
NVDA_DATA = {
    "profile": {
        "symbol": "NVDA", "name": "NVIDIA Corporation", "price": 167.52,
        "changes": -2.31, "changesPct": -1.36, "exchange": "NASDAQ",
        "sector": "Technology", "industry": "Semiconductors", "country": "US",
        "mktCap": "$4.07T", "beta": 2.37, "range": "86.62 - 212.19",
        "employees": "36,000",
        "desc": "NVIDIA는 GPU(그래픽 처리 장치) 및 AI 컴퓨팅 플랫폼의 글로벌 리더입니다.",
        "accent": "#76b900"
    },
    "income": [
        {"year":"2022","rev":26.91,"ni":9.75,"oi":10.04,"gp":17.48,"eps":0.39,"gm":64.93,"om":37.31,"nm":36.23,"rnd":7.34,"capex":0.98,"ocf":9.11,"fcf":8.13,"src":"10-K"},
        {"year":"2023","rev":26.97,"ni":4.37,"oi":4.22,"gp":15.36,"eps":0.17,"gm":56.93,"om":15.66,"nm":16.19,"rnd":7.34,"capex":1.83,"ocf":5.64,"fcf":3.81,"src":"10-K"},
        {"year":"2024","rev":60.92,"ni":29.76,"oi":32.97,"gp":44.30,"eps":1.19,"gm":72.72,"om":54.12,"nm":48.85,"rnd":8.68,"capex":1.07,"ocf":28.09,"fcf":27.02,"src":"10-K"},
        {"year":"2025","rev":130.50,"ni":72.88,"oi":81.45,"gp":97.86,"eps":2.94,"gm":74.99,"om":62.42,"nm":55.85,"rnd":12.91,"capex":3.23,"ocf":64.09,"fcf":60.86,"src":"10-K"},
        {"year":"2026","rev":215.94,"ni":120.07,"oi":130.39,"gp":153.46,"eps":4.90,"gm":71.07,"om":60.38,"nm":55.60,"rnd":18.50,"capex":6.04,"ocf":102.72,"fcf":96.58,"src":"IR"},
    ],
    "quarterly": [
        {"q":"Q1'25","rev":26.04,"ni":14.88},{"q":"Q2'25","rev":30.04,"ni":16.60},
        {"q":"Q3'25","rev":35.08,"ni":19.31},{"q":"Q4'25","rev":39.33,"ni":22.09},
        {"q":"Q1'26","rev":44.06,"ni":18.78,"gm":60.5},{"q":"Q2'26","rev":46.70,"ni":26.42,"gm":72.4},
        {"q":"Q3'26","rev":57.00,"ni":31.90,"gm":73.4},{"q":"Q4'26","rev":68.13,"ni":42.96,"gm":75.0},
    ],
    "extra": {},
    "segments": {"labels":["FY2022","FY2023","FY2024","FY2025","FY2026"],"series":[
        {"name":"Data Center","color":"#76b900","data":[10.6,15.0,47.5,115.2,193.7]},
        {"name":"Gaming","color":"#4ecdc4","data":[12.5,9.1,10.4,11.4,16.0]},
        {"name":"Pro Visualization","color":"#4dabf7","data":[2.1,1.5,1.6,1.9,3.2]},
        {"name":"Automotive","color":"#b197fc","data":[0.6,0.9,1.1,1.7,2.3]},
    ]},
    "quarterly_segments": {"labels":["Q1'26","Q2'26","Q3'26","Q4'26"],"series":[
        {"name":"Data Center","color":"#76b900","data":[39.1,41.1,51.2,62.3]},
        {"name":"Gaming","color":"#4ecdc4","data":[3.8,4.3,4.3,3.7]},
        {"name":"Pro Visualization","color":"#4dabf7","data":[0.509,0.601,0.760,1.3]},
        {"name":"Automotive","color":"#b197fc","data":[0.567,0.586,0.592,0.604]},
    ]},
    "quarterly_detail": [
        {"q":"Q1'26","rev":44.06,"ni":18.78,"gm":60.5,"om":37.0,"nm":42.6,"note":"H20 재고충당"},
        {"q":"Q2'26","rev":46.70,"ni":26.42,"gm":72.4,"om":58.2,"nm":56.6,"note":"Blackwell 출하 시작"},
        {"q":"Q3'26","rev":57.00,"ni":31.90,"gm":73.4,"om":63.1,"nm":55.9,"note":"Blackwell 본격"},
        {"q":"Q4'26","rev":68.13,"ni":42.96,"gm":75.0,"om":66.5,"nm":63.1,"note":"역대 최고"},
    ],
    "quarterly_financial_items": [],
    "financial_items": [],
    "next_earnings": {"key_watch":[]},
    "peers": [],
    "ratios": {},
    "invest": {"strengths":[], "risks":[], "opportunities":[], "watchlist":[]},
    "overview_money": [],
    "overview_growth": [],
    "overview_risks": [],
    "earnings_quarters": [],
}

# Load NVDA extra data (overview, financial_items, earnings, invest, etc.)
_nvda_extra_ns = {}
with open('/sessions/exciting-gracious-pasteur/stock_data_NVDA_extra.py') as f:
    exec(f.read(), _nvda_extra_ns)
for key in ["overview_money", "overview_growth", "overview_risks", "financial_items",
            "quarterly_financial_items", "earnings_quarters", "next_earnings", "peers", "ratios", "invest"]:
    upper_key = key.upper()
    if upper_key in _nvda_extra_ns and _nvda_extra_ns[upper_key]:
        NVDA_DATA[key] = _nvda_extra_ns[upper_key]

# Build unified STOCKS dictionary
STOCKS = {
    "NVDA": NVDA_DATA,
    "AAPL": AAPL_DATA,
    "MSFT": MSFT_DATA,
    "GOOGL": GOOGL_DATA,
    "O": O_DATA,
    "ABBV": ABBV_DATA,
    "PLTR": PLTR_DATA,
    "CRWV": CRWV_DATA,
    "IONQ": IONQ_DATA,
    "SMR": SMR_DATA,
}

STOCK_ORDER = ["NVDA", "AAPL", "MSFT", "GOOGL", "O", "ABBV", "PLTR", "CRWV", "IONQ", "SMR"]

# Company logo URLs (Clearbit Logo API)
LOGO_URLS = {
    "NVDA": "https://logo.clearbit.com/nvidia.com",
    "AAPL": "https://logo.clearbit.com/apple.com",
    "MSFT": "https://logo.clearbit.com/microsoft.com",
    "GOOGL": "https://logo.clearbit.com/google.com",
    "O": "https://logo.clearbit.com/realtyincome.com",
    "ABBV": "https://logo.clearbit.com/abbvie.com",
    "PLTR": "https://logo.clearbit.com/palantir.com",
    "CRWV": "https://logo.clearbit.com/cerebras.net",
    "IONQ": "https://logo.clearbit.com/ionq.com",
    "SMR": "https://logo.clearbit.com/nuscalepower.com",
}

# ══════════════════════════════════════════════════════════════════════════════
# SVG CHART FUNCTIONS (EXACT COPY FROM v13)
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
        x=pad_l+i*(cW/n)+(cW/n)/2; lines.append(f'<text x="{x:.1f}" y="{H-pad_b+18}" fill="#9ca0b8" font-size="10" text-anchor="middle">{labels[i]}</text>')
    lx=pad_l
    for s in series:
        lines.append(f'<rect x="{lx}" y="{H-10}" width="8" height="8" rx="2" fill="{s["color"]}"/>')
        lines.append(f'<text x="{lx+12}" y="{H-3}" fill="#9ca0b8" font-size="9">{s["name"]}</text>')
        lx+=len(s["name"])*6+20
    lines.append('</svg>'); return '\n'.join(lines)

# ══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS FOR PER-STOCK HTML GENERATION
# ══════════════════════════════════════════════════════════════════════════════

def gen_overview_section(title, subtitle, items, gradient):
    """Generate a section card with emoji items."""
    html = f'<div class="section-card"><div class="section-header" style="background:{gradient}"><div class="section-subtitle">{subtitle}</div><div class="section-title">{title}</div></div><div class="section-body">'
    for item in items:
        item_emoji = item.get("emoji", "")
        item_title = item.get("title", "")
        item_desc = item.get("desc", "")
        if isinstance(item, str):
            item_desc = item
        html += f'<div class="insight-item"><div class="insight-header"><span class="insight-emoji">{item_emoji}</span><span class="insight-title">{item_title}</span></div><p class="insight-desc">{item_desc}</p></div>'
    html += '</div></div>'
    return html

def gen_financial_section(category_data):
    """Generate financial items with analyst commentary and verification badges."""
    if not category_data:
        return ""
    html = ''
    for cat in category_data:
        if isinstance(cat, str):
            continue
        cat_name = cat.get("category", "")
        items = cat.get("items", [])
        html += f'<div class="fin-category"><div class="fin-cat-title">{cat_name}</div>'
        for item in items:
            if isinstance(item, str):
                continue
            arrow = "&#9650;" if item.get("yoy_dir")=="up" else "&#9660;"
            color = "var(--green)" if item.get("yoy_dir")=="up" else "var(--red)"
            badge = '<span class="src-badge verified">IR 공시</span>' if item.get("verified") else '<span class="src-badge estimate">추정치</span>'
            html += f'''<div class="fin-item">
<div class="fin-item-label">{item.get("label","")} {badge}</div>
<div class="fin-item-headline"><span class="fin-emoji">{item.get("emoji","")}</span> {item.get("headline","")}</div>
<div class="fin-metric-row">
<div class="fin-metric-value">{item.get("value","")}</div>
<div class="fin-metric-change" style="color:{color}"><span style="font-size:11px;">{arrow}</span> 전년 대비 {item.get("yoy","")}</div>
</div>
<p class="fin-item-desc">{item.get("desc","")}</p>
</div>'''
        html += '</div>'
    return html

def fin_table(data):
    """Generate annual financial table for a stock."""
    income = data.get("income", [])
    if not income:
        return ""
    rows=[("매출 (Revenue)",[f"${d['rev']:.1f}B" for d in income]),
          ("매출총이익 (Gross Profit)",[f"${d['gp']:.1f}B" for d in income]),
          ("영업이익 (Operating Income)",[f"${d['oi']:.1f}B" for d in income]),
          ("순이익 (Net Income)",[f"${d['ni']:.1f}B" for d in income]),
          ("EPS (희석)",[f"${d['eps']:.2f}" for d in income]),
          ("R&D",[f"${d['rnd']:.1f}B" for d in income]),
          ("CapEx",[f"${d['capex']:.1f}B" for d in income]),
          ("영업CF",[f"${d['ocf']:.1f}B" for d in income]),
          ("FCF",[f"${d['fcf']:.1f}B" for d in income]),
          ("매출총이익률",[f"{d['gm']:.1f}%" for d in income]),
          ("영업이익률",[f"{d['om']:.1f}%" for d in income]),
          ("순이익률",[f"{d['nm']:.1f}%" for d in income])]
    h='<table><thead><tr><th>지표</th>'
    for d in income: h+=f'<th class="nr">FY{d["year"]}</th>'
    h+='</tr></thead><tbody>'
    for l,vs in rows:
        h+=f'<tr><td>{l}</td>'
        for v in vs: h+=f'<td class="nr">{v}</td>'
        h+='</tr>'
    return h+'</tbody></table>'

def seg_table(data):
    """Generate segment table for a stock."""
    segments = data.get("segments", {})
    labels = segments.get("labels", [])
    series = segments.get("series", [])
    if not labels or not series:
        return ""
    h='<table><thead><tr><th>부문</th>'
    for l in labels: h+=f'<th class="nr">{l}</th>'
    h+='</tr></thead><tbody>'
    for s in series:
        h+=f'<tr><td><span style="display:inline-block;width:10px;height:10px;border-radius:3px;background:{s["color"]};margin-right:8px;vertical-align:middle;"></span>{s["name"]}</td>'
        for v in s.get("data", []): h+=f'<td class="nr">${v:.1f}B</td>'
        h+='</tr>'
    return h+'</tbody></table>'

def q_seg_table(data):
    """Generate quarterly segment table with QoQ column."""
    qsegments = data.get("quarterly_segments", {})
    labels = qsegments.get("labels", [])
    series = qsegments.get("series", [])
    if not labels or not series:
        return ""
    h='<table><thead><tr><th>부문</th>'
    for l in labels: h+=f'<th class="nr">{l}</th>'
    h+='<th class="nr">QoQ</th></tr></thead><tbody>'
    for s in series:
        data_list = s.get("data", [])
        qoq = (data_list[-1] - data_list[-2]) / data_list[-2] * 100 if len(data_list) > 1 and data_list[-2] != 0 else 0
        qoq_cls = "up" if qoq >= 0 else "down"
        qoq_str = f'+{qoq:.1f}%' if qoq >= 0 else f'{qoq:.1f}%'
        h+=f'<tr><td><span style="display:inline-block;width:10px;height:10px;border-radius:3px;background:{s["color"]};margin-right:8px;vertical-align:middle;"></span>{s["name"]}</td>'
        for v in data_list: h+=f'<td class="nr">${v:.1f}B</td>' if v >= 1 else f'<td class="nr">${v*1000:.0f}M</td>'
        h+=f'<td class="nr {qoq_cls}">{qoq_str}</td></tr>'
    h+='<tr style="font-weight:700;border-top:2px solid var(--accent);"><td>Total</td>'
    for i in range(len(labels)):
        t = sum(s["data"][i] if isinstance(s.get("data"), list) else 0 for s in series)
        h+=f'<td class="nr">${t:.1f}B</td>'
    h+='<td class="nr"></td></tr>'
    return h+'</tbody></table>'

def q_detail_table(data):
    """Generate quarterly detail table with margins."""
    quarterly_detail = data.get("quarterly_detail", [])
    if not quarterly_detail:
        return ""
    h='<table><thead><tr><th>분기</th><th class="nr">매출</th><th class="nr">순이익</th><th class="nr">GPM</th><th class="nr">OPM</th><th class="nr">NPM</th><th>비고</th></tr></thead><tbody>'
    for d in quarterly_detail:
        h+=f'<tr><td>{d.get("q","")}</td><td class="nr">${d.get("rev",0):.1f}B</td><td class="nr">${d.get("ni",0):.1f}B</td>'
        h+=f'<td class="nr">{d.get("gm",0):.1f}%</td><td class="nr">{d.get("om",0):.1f}%</td><td class="nr">{d.get("nm",0):.1f}%</td>'
        h+=f'<td style="font-size:12px;color:var(--text2);">{d.get("note","")}</td></tr>'
    return h+'</tbody></table>'

def peer_table(data):
    """Generate peer comparison table."""
    peers = data.get("peers", [])
    if not peers:
        return ""
    h='<table><thead><tr><th>티커</th><th>기업명</th><th class="nr">시가총액</th><th class="nr">P/E</th><th class="nr">P/S</th><th class="nr">매출</th><th class="nr">순이익률</th></tr></thead><tbody>'
    for p in peers:
        if isinstance(p, str):
            continue
        bg=' style="background:rgba(118,185,0,.1);"' if p.get("hl") else ''
        sym=f'<strong>{p.get("sym","")}</strong>' if p.get("hl") else p.get("sym","")
        h+=f'<tr{bg}><td>{sym}</td><td>{p.get("name","")}</td><td class="nr">{p.get("mc","")}</td><td class="nr">{p.get("pe","")}</td><td class="nr">{p.get("ps","")}</td><td class="nr">{p.get("rev","")}</td><td class="nr">{p.get("nm","")}</td></tr>'
    return h+'</tbody></table>'

def svg_earnings_compare(quarters, W=580, H=260):
    """매출 실적 vs 컨센서스 비교 그룹드 바 차트"""
    if not quarters:
        return ""
    labels = [q.get("q","").replace("FY2026","").replace("FY2025","").replace("FY2024","").replace("FY2023","").replace("FY2022","").strip() for q in quarters]
    pad_l, pad_r, pad_t, pad_b = 60, 20, 30, 50
    cw = W - pad_l - pad_r
    ch = H - pad_t - pad_b
    n = len(labels)
    gw = cw / n
    bw = gw * 0.30
    vals = []
    for q in quarters:
        vals.extend([q.get("rev_est", 0) or 0, q.get("rev_actual", 0) or 0])
    mx = max(vals) * 1.15 if vals and max(vals) else 1
    def y(v): return pad_t + ch - (v / mx * ch)
    svg = ''
    for i in range(5):
        gv = mx * i / 4
        yp = y(gv)
        svg += f'<line x1="{pad_l}" y1="{yp}" x2="{W-pad_r}" y2="{yp}" stroke="rgba(255,255,255,.06)" stroke-dasharray="4,4"/>'
        svg += f'<text x="{pad_l-8}" y="{yp+4}" fill="var(--text2)" font-size="10" text-anchor="end" font-family="Geist Mono,monospace">${gv:.0f}B</text>'
    for i, q in enumerate(quarters):
        cx = pad_l + i * gw + gw / 2
        rev_est = q.get("rev_est", 0) or 0
        rev_actual = q.get("rev_actual", 0) or 0
        bh_est = rev_est / mx * ch if mx else 0
        svg += f'<rect x="{cx - bw - 2}" y="{y(rev_est)}" width="{bw}" height="{bh_est}" rx="3" fill="rgba(255,255,255,.15)"/>'
        svg += f'<text x="{cx - bw/2 - 2}" y="{y(rev_est)-5}" fill="var(--text2)" font-size="9" text-anchor="middle" font-family="Geist Mono,monospace">${rev_est:.1f}B</text>'
        bh_act = rev_actual / mx * ch if mx else 0
        svg += f'<rect x="{cx + 2}" y="{y(rev_actual)}" width="{bw}" height="{bh_act}" rx="3" fill="var(--accent)"/>'
        svg += f'<text x="{cx + bw/2 + 2}" y="{y(rev_actual)-5}" fill="var(--accent)" font-size="9" font-weight="700" text-anchor="middle" font-family="Geist Mono,monospace">${rev_actual:.1f}B</text>'
        svg += f'<text x="{cx}" y="{H-10}" fill="var(--text2)" font-size="11" text-anchor="middle">{labels[i]}</text>'
        svg += f'<text x="{cx}" y="{H-25}" fill="#76b900" font-size="9" font-weight="700" text-anchor="middle" font-family="Geist Mono,monospace">{q.get("rev_surprise", "")}</text>'
    svg += f'<rect x="{W-160}" y="8" width="10" height="10" rx="2" fill="rgba(255,255,255,.15)"/>'
    svg += f'<text x="{W-145}" y="17" fill="var(--text2)" font-size="10">컨센서스</text>'
    svg += f'<rect x="{W-90}" y="8" width="10" height="10" rx="2" fill="var(--accent)"/>'
    svg += f'<text x="{W-75}" y="17" fill="var(--text2)" font-size="10">실제 매출</text>'
    return f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{svg}</svg>'

def svg_eps_surprise(quarters, W=580, H=260):
    """EPS 실적 vs 컨센서스 비교 차트"""
    if not quarters:
        return ""
    labels = [q.get("q","").replace("FY2026","").replace("FY2025","").replace("FY2024","").replace("FY2023","").replace("FY2022","").strip() for q in quarters]
    pad_l, pad_r, pad_t, pad_b = 60, 20, 30, 50
    cw = W - pad_l - pad_r
    ch = H - pad_t - pad_b
    n = len(labels)
    gw = cw / n
    bw = gw * 0.30
    vals = []
    for q in quarters:
        vals.extend([q.get("eps_est", 0) or 0, q.get("eps_actual", 0) or 0])
    mx = max(vals) * 1.20 if vals and max(vals) else 1
    def y(v): return pad_t + ch - (v / mx * ch)
    svg = ''
    for i in range(5):
        gv = mx * i / 4
        yp = y(gv)
        svg += f'<line x1="{pad_l}" y1="{yp}" x2="{W-pad_r}" y2="{yp}" stroke="rgba(255,255,255,.06)" stroke-dasharray="4,4"/>'
        svg += f'<text x="{pad_l-8}" y="{yp+4}" fill="var(--text2)" font-size="10" text-anchor="end" font-family="Geist Mono,monospace">${gv:.2f}</text>'
    for i, q in enumerate(quarters):
        cx = pad_l + i * gw + gw / 2
        eps_est = q.get("eps_est", 0) or 0
        eps_actual = q.get("eps_actual", 0) or 0
        bh_est = eps_est / mx * ch if mx else 0
        svg += f'<rect x="{cx - bw - 2}" y="{y(eps_est)}" width="{bw}" height="{bh_est}" rx="3" fill="rgba(255,255,255,.15)"/>'
        svg += f'<text x="{cx - bw/2 - 2}" y="{y(eps_est)-5}" fill="var(--text2)" font-size="9" text-anchor="middle" font-family="Geist Mono,monospace">${eps_est:.2f}</text>'
        bh_act = eps_actual / mx * ch if mx else 0
        svg += f'<rect x="{cx + 2}" y="{y(eps_actual)}" width="{bw}" height="{bh_act}" rx="3" fill="#4ecdc4"/>'
        svg += f'<text x="{cx + bw/2 + 2}" y="{y(eps_actual)-5}" fill="#4ecdc4" font-size="9" font-weight="700" text-anchor="middle" font-family="Geist Mono,monospace">${eps_actual:.2f}</text>'
        svg += f'<text x="{cx}" y="{H-10}" fill="var(--text2)" font-size="11" text-anchor="middle">{labels[i]}</text>'
        svg += f'<text x="{cx}" y="{H-25}" fill="#4ecdc4" font-size="9" font-weight="700" text-anchor="middle" font-family="Geist Mono,monospace">{q.get("eps_surprise", "")}</text>'
    svg += f'<rect x="{W-160}" y="8" width="10" height="10" rx="2" fill="rgba(255,255,255,.15)"/>'
    svg += f'<text x="{W-145}" y="17" fill="var(--text2)" font-size="10">컨센서스</text>'
    svg += f'<rect x="{W-90}" y="8" width="10" height="10" rx="2" fill="#4ecdc4"/>'
    svg += f'<text x="{W-75}" y="17" fill="var(--text2)" font-size="10">실제 EPS</text>'
    return f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{svg}</svg>'

def earnings_call_cards(data):
    """분기별 컨퍼런스콜 요약 카드 생성"""
    quarters = data.get("earnings_quarters", [])
    if not quarters:
        return ""
    h = ''
    for q in reversed(quarters):
        if isinstance(q, str) or not q:
            continue
        beat_cls = "up" if q.get("eps_beat") else "down"
        beat_txt = "Beat" if q.get("eps_beat") else "Miss"
        react_cls = "up" if str(q.get("stock_reaction", "")).startswith("+") else "down"
        keywords = q.get("keywords", []) or []
        highlights = q.get("highlights", []) or []
        badges = ''.join(f'<span class="earn-badge">{kw}</span>' for kw in keywords if kw)
        highlights_html = ''.join(f'<li>{hl}</li>' for hl in highlights if hl)
        rev_actual = q.get("rev_actual") or 0
        rev_est = q.get("rev_est") or 0
        eps_actual = q.get("eps_actual") or 0
        eps_est = q.get("eps_est") or 0
        eps_gaap = q.get("eps_gaap") or 0
        h += f'''<div class="earn-card reveal">
  <div class="earn-header">
    <div class="earn-q">{q.get("q","")}</div>
    <div class="earn-date">{q.get("date","")} 발표 | {q.get("period","")}</div>
    <div class="earn-surprise {beat_cls}">EPS {beat_txt} {q.get("eps_surprise","")}</div>
  </div>
  <div class="earn-badges">{badges}</div>
  <div class="earn-metrics">
    <div class="earn-metric">
      <div class="earn-metric-label">매출</div>
      <div class="earn-metric-val">${rev_actual:.1f}B</div>
      <div class="earn-metric-sub">vs est. ${rev_est:.1f}B ({q.get("rev_surprise","")})</div>
    </div>
    <div class="earn-metric">
      <div class="earn-metric-label">EPS (Non-GAAP)</div>
      <div class="earn-metric-val">${eps_actual:.2f}</div>
      <div class="earn-metric-sub">vs est. ${eps_est:.2f} ({q.get("eps_surprise","")})</div>
    </div>
    <div class="earn-metric">
      <div class="earn-metric-label">EPS (GAAP)</div>
      <div class="earn-metric-val">${eps_gaap:.2f}</div>
      <div class="earn-metric-sub">&nbsp;</div>
    </div>
    <div class="earn-metric">
      <div class="earn-metric-label">주가 반응</div>
      <div class="earn-metric-val {react_cls}">{q.get("stock_reaction","")}</div>
      <div class="earn-metric-sub">{q.get("reaction_note","")}</div>
    </div>
  </div>
  <div class="earn-ceo">
    <div class="earn-ceo-label">🎙️ CEO 발언</div>
    <div class="earn-ceo-quote">"{q.get("ceo_quote","")}"</div>
  </div>
  <div class="earn-highlights">
    <div class="earn-hl-title">📋 주요 하이라이트</div>
    <ul>{highlights_html}</ul>
  </div>
  <div class="earn-analyst">
    <div class="earn-analyst-title">📊 애널리스트 코멘트</div>
    <p>{q.get("analyst_comment","")}</p>
  </div>
</div>'''
    return h

def next_earnings_card(data):
    """다음 실적발표 예정 카드"""
    ne = data.get("next_earnings", {})
    if not ne:
        return ""
    watches = ne.get("key_watch", [])
    watches_html = ''.join(f'<li>{w}</li>' for w in watches)
    return f'''<div class="next-earn reveal">
  <div class="next-earn-header">
    <div class="next-earn-icon">📅</div>
    <div>
      <div class="next-earn-title">다음 실적발표 예정</div>
      <div class="next-earn-date">{ne.get("date","")} | {ne.get("quarter","")} ({ne.get("period","")})</div>
    </div>
    <div class="next-earn-countdown">D-60</div>
  </div>
  <div class="next-earn-grid">
    <div class="next-earn-item"><div class="ne-label">매출 가이던스</div><div class="ne-value" style="color:var(--accent)">{ne.get("rev_guidance","")}</div><div class="ne-sub">{ne.get("rev_range","")}</div></div>
    <div class="next-earn-item"><div class="ne-label">매출총이익률</div><div class="ne-value">{ne.get("gm_guidance","")}</div><div class="ne-sub">가이던스 기준</div></div>
    <div class="next-earn-item"><div class="ne-label">컨센서스 매출</div><div class="ne-value">{ne.get("consensus_rev","")}</div><div class="ne-sub">EPS est. {ne.get("consensus_eps","")}</div></div>
    <div class="next-earn-item"><div class="ne-label">애널리스트 의견</div><div class="ne-value" style="color:var(--accent)">{ne.get("analyst_buy_pct","")} 매수</div><div class="ne-sub">{ne.get("analyst_count","")}명 | 목표가 {ne.get("avg_target","")}</div></div>
  </div>
  <div class="next-earn-watch">
    <div class="ne-watch-title">🔍 Key Watchpoints</div>
    <ul>{watches_html}</ul>
  </div>
</div>'''

def invest_html(data):
    """투자포인트 카드 생성"""
    invest = data.get("invest", {})
    if not invest:
        return ""
    sections=[("강점 (Strengths)","strengths","dot-green"),("리스크 (Risks)","risks","dot-red"),("기회 (Opportunities)","opportunities","dot-blue"),("주요 모니터링 (Watchlist)","watchlist","dot-orange")]
    h=''
    for title,key,dot in sections:
        items = invest.get(key, [])
        h+=f'<div class="invest-card"><h4><span class="dot {dot}"></span> {title}</h4><ul>'
        for item in items:
            h+=f'<li>{item}</li>'
        h+='</ul></div>'
    return h

# ══════════════════════════════════════════════════════════════════════════════
# GENERATE PER-STOCK HTML CONTENT
# ══════════════════════════════════════════════════════════════════════════════

stock_htmls = {}

for ticker in STOCK_ORDER:
    stock_data = STOCKS[ticker]
    p = stock_data.get("profile", {})
    accent = p.get("accent", "#76b900")
    logo_url = LOGO_URLS.get(ticker, "")
    income = stock_data.get("income", [])

    # Change class for price
    chg_cls = "up" if p.get("changes", 0) >= 0 else "down"

    # Revenue growth
    rev_g = ((income[-1]["rev"] - income[-2]["rev"]) / income[-2]["rev"] * 100) if len(income) >= 2 and income[-2]["rev"] else 0
    ni_g = ((income[-1]["ni"] - income[-2]["ni"]) / income[-2]["ni"] * 100) if len(income) >= 2 and income[-2]["ni"] else 0

    # Latest year data
    latest = income[-1] if income else {}

    # Tab 1: Overview
    overview_money = stock_data.get("overview_money", [])
    overview_growth = stock_data.get("overview_growth", [])
    overview_risks = stock_data.get("overview_risks", [])
    overview_money_html = gen_overview_section("주요 수입원", "돈을 버는 방법", overview_money, f"linear-gradient(135deg,rgba(118,185,0,.04),rgba(118,185,0,.01))")
    overview_growth_html = gen_overview_section("미래 성장 동력", "성장의 가능성", overview_growth, "linear-gradient(135deg,#0a2a4a,#1a3a5a)")
    overview_risks_html = gen_overview_section("주의해야 할 점", "잠재 위험 요소", overview_risks, "linear-gradient(135deg,#3a2a00,#4a3500)")

    # Tab 2: Financial
    financial_items = stock_data.get("financial_items", [])
    quarterly_financial_items = stock_data.get("quarterly_financial_items", [])
    financial_html = gen_financial_section(financial_items)
    quarterly_financial_html = gen_financial_section(quarterly_financial_items)
    fin_table_html = fin_table(stock_data)
    q_detail_html = q_detail_table(stock_data)

    # Charts for financials
    if income:
        labels = [f'FY{d["year"]}' for d in income]
        rev_chart = svg_grouped_bar(labels, [{"label":"매출","color":"#76b900","data":[d["rev"] for d in income]},{"label":"순이익","color":"#4ecdc4","data":[d["ni"] for d in income]}])
        margin_chart = svg_line_chart(labels, [{"label":"GPM","color":"#76b900","data":[d["gm"] for d in income]},{"label":"OPM","color":"#4ecdc4","data":[d["om"] for d in income]},{"label":"NPM","color":"#a78bfa","data":[d["nm"] for d in income]}])
        rnd_capex_chart = svg_grouped_bar(labels, [{"label":"R&D","color":"#4dabf7","data":[d["rnd"] for d in income]},{"label":"CapEx","color":"#b197fc","data":[d["capex"] for d in income]}])
        cashflow_chart = svg_grouped_bar(labels, [{"label":"영업CF","color":"#76b900","data":[d["ocf"] for d in income]},{"label":"FCF","color":"#4ecdc4","data":[d["fcf"] for d in income]}])
    else:
        rev_chart = margin_chart = rnd_capex_chart = cashflow_chart = ""

    quarterly = stock_data.get("quarterly", [])
    if quarterly:
        q_labels = [d["q"] for d in quarterly[-8:]]
        q_rev_data = [d["rev"] for d in quarterly[-8:]]
        q_ni_data = [d["ni"] for d in quarterly[-8:]]
        q_chart = svg_grouped_bar(q_labels, [{"label":"매출","color":"#76b900","data":q_rev_data},{"label":"순이익","color":"#4ecdc4","data":q_ni_data}])
        q_gm = [d.get("gm", 0) for d in quarterly[-4:]]
        q_margin_chart = svg_line_chart([d["q"] for d in quarterly[-4:]], [{"label":"GPM","color":"#76b900","data":q_gm}]) if any(q_gm) else ""
    else:
        q_chart = q_margin_chart = ""

    # Tab 3: Segments
    segments = stock_data.get("segments", {})
    quarterly_segments = stock_data.get("quarterly_segments", {})
    seg_labels = segments.get("labels", [])
    seg_series = segments.get("series", [])

    if seg_series and seg_labels:
        latest_seg = [{"name": s["name"], "value": s["data"][-1] if s["data"] else 0, "color": s["color"]} for s in seg_series]
        donut_chart = svg_donut(latest_seg)
        stacked_chart = svg_stacked_bar(seg_labels, seg_series)
    else:
        donut_chart = stacked_chart = ""
    seg_table_html = seg_table(stock_data)

    q_seg_labels = quarterly_segments.get("labels", [])
    q_seg_series = quarterly_segments.get("series", [])
    if q_seg_series and q_seg_labels:
        latest_q_seg = [{"name": s["name"], "value": s["data"][-1] if s["data"] else 0, "color": s["color"]} for s in q_seg_series]
        q_seg_donut = svg_donut(latest_q_seg)
        q_seg_stacked = svg_stacked_bar(q_seg_labels, q_seg_series)
    else:
        q_seg_donut = q_seg_stacked = ""
    q_seg_table_html = q_seg_table(stock_data)

    # Tab 4: Valuation
    ratios = stock_data.get("ratios", {})
    peer_table_html = peer_table(stock_data)

    # EPS chart for valuation
    if income:
        eps_chart = svg_grouped_bar([f'FY{d["year"]}' for d in income], [{"label":"EPS","color":"#76b900","data":[d["eps"] for d in income]}])
    else:
        eps_chart = ""

    # Tab 5: Earnings
    earnings_quarters = stock_data.get("earnings_quarters", [])
    earnings_rev_chart = svg_earnings_compare(earnings_quarters)
    earnings_eps_chart = svg_eps_surprise(earnings_quarters)
    earnings_cards_html = earnings_call_cards(stock_data)
    next_earn_html = next_earnings_card(stock_data)

    # Tab 6: Investment
    invest_html_content = invest_html(stock_data)

    # KPIs
    kpi_annual = ""
    if income and len(income) >= 1:
        li = income[-1]
        kpi_annual = f'''<div class="kpi-row reveal">
      <div class="kpi"><div class="kpi-l">시가총액</div><div class="kpi-v">{p.get("mktCap","N/A")}</div><div class="kpi-s">Beta: {p.get("beta","")}</div></div>
      <div class="kpi"><div class="kpi-l">연간 매출</div><div class="kpi-v">${li["rev"]:.1f}B</div><div class="kpi-s {"up" if rev_g>0 else "down"}">{rev_g:+.1f}% YoY</div></div>
      <div class="kpi"><div class="kpi-l">연간 순이익</div><div class="kpi-v">${li["ni"]:.1f}B</div><div class="kpi-s {"up" if ni_g>0 else "down"}">{ni_g:+.1f}% YoY</div></div>
      <div class="kpi"><div class="kpi-l">EPS</div><div class="kpi-v">${li["eps"]:.2f}</div><div class="kpi-s">순이익률 {li["nm"]:.1f}%</div></div>
      <div class="kpi"><div class="kpi-l">P/E (TTM)</div><div class="kpi-v">{ratios.get("pe","N/A")}</div><div class="kpi-s">PEG: {ratios.get("peg","")}</div></div>
      <div class="kpi"><div class="kpi-l">FCF Margin</div><div class="kpi-v">{li.get("fcf",0)/li["rev"]*100:.1f}%</div><div class="kpi-s">FCF: ${li.get("fcf",0):.1f}B</div></div>
    </div>'''

    # Quarterly KPIs
    quarterly_detail = stock_data.get("quarterly_detail", [])
    kpi_quarterly = ""
    if quarterly_detail:
        lq = quarterly_detail[-1]
        kpi_quarterly = f'''<div class="kpi-row reveal">
      <div class="kpi"><div class="kpi-l">{lq.get("q","")} 매출</div><div class="kpi-v">${lq.get("rev",0):.1f}B</div></div>
      <div class="kpi"><div class="kpi-l">{lq.get("q","")} 순이익</div><div class="kpi-v">${lq.get("ni",0):.1f}B</div></div>
      <div class="kpi"><div class="kpi-l">{lq.get("q","")} GPM</div><div class="kpi-v">{lq.get("gm",0):.1f}%</div></div>
      <div class="kpi"><div class="kpi-l">{lq.get("q","")} OPM</div><div class="kpi-v">{lq.get("om",0):.1f}%</div></div>
    </div>'''

    # Segment KPIs for quarterly
    seg_kpi_q = ""
    if q_seg_series:
        seg_kpi_q = '<div class="kpi-row reveal">'
        for s in q_seg_series:
            latest_val = s["data"][-1] if s["data"] else 0
            display_val = f"${latest_val:.1f}B" if latest_val >= 1 else f"${latest_val*1000:.0f}M"
            seg_kpi_q += f'<div class="kpi"><div class="kpi-l">{q_seg_labels[-1] if q_seg_labels else ""} {s["name"]}</div><div class="kpi-v">{display_val}</div></div>'
        seg_kpi_q += '</div>'

    # Build the stock section HTML using EXACT v13 structure
    # Use scoped IDs: t-{ticker}-overview, fin-{ticker}-annual, etc.
    stock_htmls[ticker] = f'''
<div class="stock-section" id="s-{ticker}" style="display:none;">

<div class="tabs" id="tabBar-{ticker}">
  <div class="tab active" onclick="st_for('{ticker}','overview')">기업 개요</div>
  <div class="tab" onclick="st_for('{ticker}','financial')">재무 분석</div>
  <div class="tab" onclick="st_for('{ticker}','segments')">사업부문</div>
  <div class="tab" onclick="st_for('{ticker}','valuation')">밸류에이션</div>
  <div class="tab" onclick="st_for('{ticker}','earnings')">실적발표</div>
  <div class="tab" onclick="st_for('{ticker}','invest')">투자 포인트</div>
</div>

<div class="main">

<!-- Company Header -->
<div class="ch">
  <img class="ch-logo" src="{logo_url}" alt="{ticker}" onerror="this.style.display='none'"/>
  <div>
    <div class="ch-tk">{ticker}</div>
    <div class="ch-nm">{p.get("name","")}</div>
    <div class="ch-desc">{p.get("desc","")}</div>
    <div style="margin-top:8px;font-size:12px;color:var(--text2);">{p.get("exchange","")} | {p.get("sector","")} | {p.get("industry","")} | {p.get("country","")}</div>
  </div>
  <div class="ch-meta">
    <div class="ch-price">${p.get("price",0):.2f}</div>
    <div class="ch-chg {chg_cls}">{p.get("changes",0):+.2f} ({p.get("changesPct",0):+.2f}%)</div>
    <div style="font-size:12px;color:var(--text2);margin-top:8px;">52주: {p.get("range","")}</div>
  </div>
</div>

<!-- TAB 1: 기업 개요 -->
<div class="tc active" id="t-{ticker}-overview">
  <div class="reveal">{overview_money_html}</div>
  <div class="reveal">{overview_growth_html}</div>
  <div class="reveal">{overview_risks_html}</div>
</div>

<!-- TAB 2: 재무 분석 -->
<div class="tc" id="t-{ticker}-financial">
  <div class="sub-tabs" id="finSubTabs-{ticker}">
    <div class="sub-tab active" onclick="sst_for('{ticker}','fin','annual')">연간</div>
    <div class="sub-tab" onclick="sst_for('{ticker}','fin','quarterly')">분기별</div>
  </div>
  <div class="sub-pane active" id="fin-{ticker}-annual">
    {kpi_annual}
    {financial_html}
    <div class="cg reveal">
      <div class="cc"><div class="ct">매출 &amp; 순이익 추이 <span class="badge">연간</span></div>{rev_chart}</div>
      <div class="cc"><div class="ct">수익성 지표 추이 <span class="badge">마진율</span></div>{margin_chart}</div>
      <div class="cc"><div class="ct">R&amp;D &amp; CapEx 추이 <span class="badge">투자</span></div>{rnd_capex_chart}</div>
      <div class="cc"><div class="ct">영업CF &amp; FCF 추이 <span class="badge">현금흐름</span></div>{cashflow_chart}</div>
    </div>
    <div class="cc"><div class="ct">연간 재무 데이터</div><div class="tw">{fin_table_html}</div></div>
  </div>
  <div class="sub-pane" id="fin-{ticker}-quarterly">
    {kpi_quarterly}
    {quarterly_financial_html}
    <div class="cg reveal">
      <div class="cc"><div class="ct">분기별 매출 &amp; 순이익</div>{q_chart}</div>
      <div class="cc"><div class="ct">분기별 수익성 추이</div>{q_margin_chart}</div>
    </div>
    <div class="cc"><div class="ct">분기별 재무 상세</div><div class="tw">{q_detail_html}</div></div>
  </div>
</div>

<!-- TAB 3: 사업부문 -->
<div class="tc" id="t-{ticker}-segments">
  <div class="sub-tabs" id="segSubTabs-{ticker}">
    <div class="sub-tab active" onclick="sst_for('{ticker}','seg','annual')">연간</div>
    <div class="sub-tab" onclick="sst_for('{ticker}','seg','quarterly')">분기별</div>
  </div>
  <div class="sub-pane active" id="seg-{ticker}-annual">
    <div class="cg reveal">
      <div class="cc"><div class="ct">사업부문별 매출 비중</div>{donut_chart}</div>
      <div class="cc"><div class="ct">사업부문별 매출 추이</div>{stacked_chart}</div>
      <div class="cc full reveal"><div class="ct">사업부문 연간 상세 데이터</div><div class="tw">{seg_table_html}</div></div>
    </div>
  </div>
  <div class="sub-pane" id="seg-{ticker}-quarterly">
    {seg_kpi_q}
    <div class="cg reveal">
      <div class="cc"><div class="ct">분기별 사업부문 비중</div>{q_seg_donut}</div>
      <div class="cc"><div class="ct">분기별 사업부문 추이</div>{q_seg_stacked}</div>
      <div class="cc full reveal"><div class="ct">분기별 사업부문 상세 데이터</div><div class="tw">{q_seg_table_html}</div></div>
    </div>
  </div>
</div>

<!-- TAB 4: 밸류에이션 -->
<div class="tc" id="t-{ticker}-valuation">
  <div class="kpi-row reveal">
    <div class="kpi"><div class="kpi-l">P/E (TTM)</div><div class="kpi-v">{ratios.get("pe","N/A")}</div></div>
    <div class="kpi"><div class="kpi-l">Forward P/E</div><div class="kpi-v">{ratios.get("fpe","N/A")}</div></div>
    <div class="kpi"><div class="kpi-l">P/S</div><div class="kpi-v">{ratios.get("ps","N/A")}</div></div>
    <div class="kpi"><div class="kpi-l">PEG</div><div class="kpi-v">{ratios.get("peg","N/A")}</div></div>
    <div class="kpi"><div class="kpi-l">ROE</div><div class="kpi-v">{ratios.get("roe","N/A")}</div></div>
    <div class="kpi"><div class="kpi-l">배당수익률</div><div class="kpi-v">{ratios.get("div","N/A")}</div></div>
  </div>
  <div class="cg reveal">
    <div class="cc"><div class="ct">EPS 추이 <span class="badge">연간</span></div>{eps_chart}</div>
    <div class="cc"><div class="ct">동종업계 밸류에이션 비교</div><div class="tw">{peer_table_html}</div></div>
  </div>
</div>

<!-- TAB 5: 실적발표 -->
<div class="tc" id="t-{ticker}-earnings">
  {next_earn_html}
  <div class="cg reveal">
    <div class="cc"><div class="ct">분기별 매출: 실적 vs 컨센서스</div>{earnings_rev_chart}</div>
    <div class="cc"><div class="ct">분기별 EPS: 실적 vs 컨센서스</div>{earnings_eps_chart}</div>
  </div>
  <div style="margin-top:4px;">{earnings_cards_html}</div>
</div>

<!-- TAB 6: 투자 포인트 -->
<div class="tc" id="t-{ticker}-invest"><div class="ig reveal">{invest_html_content}</div></div>

</div><!-- end main -->
</div><!-- end stock-section -->
'''

# ══════════════════════════════════════════════════════════════════════════════
# GENERATE FULL HTML OUTPUT WITH v13 CSS + STOCK-BAR
# ══════════════════════════════════════════════════════════════════════════════

html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>StockLens 포트폴리오 종합분석</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@100;200;300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
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

/* Stock selector bar */
.stock-bar{{display:flex;gap:6px;padding:10px 32px;background:rgba(5,5,8,.6);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border-bottom:1px solid var(--border);overflow-x:auto;flex-wrap:wrap}}
.stock-pill{{padding:8px 18px;cursor:pointer;color:var(--text2);font-size:13px;font-weight:700;border-radius:999px;white-space:nowrap;transition:all .5s var(--spring);border:1px solid transparent;font-family:'Geist Mono',monospace;letter-spacing:-.5px}}
.stock-pill:hover{{color:var(--text);background:rgba(255,255,255,.04)}}
.stock-pill.active{{color:#fff;background:var(--accent-dim);border-color:rgba(118,185,0,.2)}}

/* Update Modal */
.modal-overlay{{display:none;position:fixed;inset:0;z-index:100;background:rgba(0,0,0,.6);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);justify-content:center;align-items:center}}
.modal-overlay.open{{display:flex}}
.modal-card{{background:var(--card-solid);border:1px solid var(--border);border-radius:var(--radius);max-width:560px;width:90%;max-height:85vh;overflow-y:auto;position:relative;animation:modalIn .4s var(--spring)}}
@keyframes modalIn{{from{{opacity:0;transform:translateY(24px) scale(.96)}}to{{opacity:1;transform:translateY(0) scale(1)}}}}
.modal-header{{display:flex;align-items:center;justify-content:space-between;padding:24px 28px;border-bottom:1px solid var(--border)}}
.modal-title{{font-size:17px;font-weight:800;color:var(--text);letter-spacing:-.3px}}
.modal-close{{width:32px;height:32px;display:flex;align-items:center;justify-content:center;border-radius:999px;cursor:pointer;color:var(--text2);font-size:16px;transition:all .3s var(--spring)}}
.modal-close:hover{{background:rgba(255,255,255,.08);color:var(--text)}}
.modal-body{{padding:24px 28px}}
.modal-stock-info{{background:linear-gradient(135deg,rgba(118,185,0,.08),rgba(78,205,196,.04));border:1px solid rgba(118,185,0,.15);border-radius:var(--radius-sm);padding:18px 20px;margin-bottom:24px;display:flex;align-items:center;gap:14px}}
.modal-stock-info .msi-ticker{{font-size:22px;font-weight:900;color:var(--accent);font-family:'Geist Mono',monospace}}
.modal-stock-info .msi-detail{{font-size:13px;color:var(--text2);line-height:1.6}}
.modal-stock-info .msi-date{{color:var(--text);font-weight:700}}
.modal-steps{{display:flex;flex-direction:column;gap:16px}}
.modal-step{{display:flex;gap:16px;align-items:flex-start;padding:16px;background:rgba(255,255,255,.02);border:1px solid var(--border);border-radius:var(--radius-sm);transition:all .3s var(--spring)}}
.modal-step:hover{{border-color:var(--border-hover);background:rgba(118,185,0,.03)}}
.modal-step-num{{width:32px;height:32px;flex-shrink:0;display:flex;align-items:center;justify-content:center;background:var(--accent-dim);color:var(--accent);font-size:14px;font-weight:800;border-radius:999px;font-family:'Geist Mono',monospace}}
.modal-step-title{{font-size:14px;font-weight:700;color:var(--text);margin-bottom:6px}}
.modal-step-desc{{font-size:13px;color:var(--text2);line-height:1.7}}
.modal-step-desc code{{background:rgba(118,185,0,.12);color:var(--accent);padding:2px 8px;border-radius:4px;font-family:'Geist Mono',monospace;font-size:12px}}

/* Tabs — glass pill */
.tabs{{display:flex;gap:2px;padding:12px 32px;background:rgba(5,5,8,.55);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border-bottom:1px solid var(--border);overflow-x:auto;position:sticky;top:92px;z-index:39}}
.tab{{padding:10px 22px;cursor:pointer;color:var(--text2);font-size:13px;font-weight:600;border-radius:999px;white-space:nowrap;transition:all .5s var(--spring);border:1px solid transparent}}
.tab:hover{{color:var(--text);background:rgba(255,255,255,.04)}}.tab.active{{color:#fff;background:var(--accent-dim);border-color:rgba(118,185,0,.2)}}
.main{{max-width:1200px;margin:0 auto;padding:32px 32px 64px}}
.tc{{display:none}}.tc.active{{display:block}}

/* Company Header — glass bezel */
.ch{{display:flex;align-items:center;gap:24px;margin-bottom:32px;padding:28px;background:var(--card);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border:1px solid var(--border);border-radius:var(--radius);position:relative;overflow:hidden}}
.ch::before{{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(118,185,0,.3),transparent)}}
.ch-logo{{width:64px;height:64px;border-radius:16px;object-fit:contain;background:rgba(255,255,255,.08);padding:8px;flex-shrink:0;border:1px solid var(--border)}}
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
  .tabs{{padding:10px 16px;top:92px}}
  .stock-bar{{padding:8px 16px}}
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
  <div class="logo">StockLens <span>포트폴리오 종합분석</span></div>
</div>

<div class="update-bar">
  <div class="ub-item"><div class="ub-icon">📊</div><div class="ub-label">데이터 기준</div><div class="ub-value">{DASHBOARD_META["created_date"]}</div></div>
  <div class="ub-item"><div class="ub-icon">📁</div><div class="ub-label">출처</div><div class="ub-value">{DASHBOARD_META["data_source"]}</div></div>
  <div class="ub-next" id="ubNext" onclick="toggleUpdateModal()" style="cursor:pointer;"><span class="ub-blink"></span> <span id="ubNextText">다음 실적발표: 2026.05.28 (수) — NVDA Q1 FY2027</span></div>
</div>

<div class="stock-bar" id="stockBar">
'''

# Add stock pills
for ticker in STOCK_ORDER:
    active_cls = "active" if ticker == "NVDA" else ""
    html += f'  <div class="stock-pill {active_cls}" onclick="selectStock(\'{ticker}\')">{ticker}</div>\n'

html += '</div>\n\n'

# Add all stock sections
for ticker in STOCK_ORDER:
    html += stock_htmls[ticker] + '\n'

html += f'''
<div class="wm">
<p>StockLens 포트폴리오 종합분석 대시보드 | 기업 재무·실적·밸류에이션 통합 분석<br/>
데이터 기준: {DASHBOARD_META["created_date"]} | 정보 출처: {DASHBOARD_META["data_source"]}</p>
</div>

<!-- Update Method Modal -->
<div class="modal-overlay" id="updateModal" onclick="closeModal(event)">
  <div class="modal-card" onclick="event.stopPropagation()">
    <div class="modal-header">
      <div class="modal-title">📋 대시보드 업데이트 방법</div>
      <div class="modal-close" onclick="toggleUpdateModal()">✕</div>
    </div>
    <div class="modal-body">
      <div class="modal-stock-info" id="modalStockInfo"></div>
      <div class="modal-steps">
        <div class="modal-step">
          <div class="modal-step-num">1</div>
          <div class="modal-step-content">
            <div class="modal-step-title">실적 발표 확인</div>
            <div class="modal-step-desc">해당 기업의 IR 페이지 또는 SEC Filing에서 최신 실적 데이터(매출, 순이익, EPS 등)를 확인합니다.</div>
          </div>
        </div>
        <div class="modal-step">
          <div class="modal-step-num">2</div>
          <div class="modal-step-content">
            <div class="modal-step-title">데이터 파일 수정</div>
            <div class="modal-step-desc">stock_data_*.py 파일에서 해당 종목의 INCOME, QUARTERLY, EARNINGS_QUARTERS 등 데이터를 업데이트합니다.</div>
          </div>
        </div>
        <div class="modal-step">
          <div class="modal-step-num">3</div>
          <div class="modal-step-content">
            <div class="modal-step-title">스크립트 재실행</div>
            <div class="modal-step-desc"><code>python3 gen_portfolio_v5.py</code> 를 실행하면 최신 데이터가 반영된 HTML이 자동으로 생성됩니다.</div>
          </div>
        </div>
        <div class="modal-step">
          <div class="modal-step-num">💡</div>
          <div class="modal-step-content">
            <div class="modal-step-title">Claude에게 요청하기</div>
            <div class="modal-step-desc">"[종목명] 실적 업데이트해줘" 라고 요청하면 자동으로 최신 실적 데이터를 수집하고 대시보드를 업데이트합니다.</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
var currentStock = 'NVDA';
var stockOrder = ['NVDA','AAPL','MSFT','GOOGL','O','ABBV','PLTR','CRWV','IONQ','SMR'];
'''

# Build per-stock next earnings JS data
ne_js_entries = []
for ticker in STOCK_ORDER:
    sd = STOCKS[ticker]
    ne = sd.get("next_earnings", {})
    p = sd.get("profile", {})
    ne_date = ne.get("date", "")
    ne_quarter = ne.get("quarter", "")
    ne_period = ne.get("period", "")
    ne_name = p.get("name", ticker)
    ne_js_entries.append(f'  "{ticker}": {{date:"{ne_date}",quarter:"{ne_quarter}",period:"{ne_period}",name:"{ne_name}"}}')

html += 'var nextEarningsData = {\n' + ',\n'.join(ne_js_entries) + '\n};\n'
html += '''

function selectStock(ticker) {
  currentStock = ticker;
  var sections = document.querySelectorAll('.stock-section');
  for (var i = 0; i < sections.length; i++) sections[i].style.display = 'none';
  document.getElementById('s-' + ticker).style.display = 'block';
  var pills = document.querySelectorAll('.stock-pill');
  for (var i = 0; i < pills.length; i++) {
    pills[i].className = (stockOrder[i] === ticker) ? 'stock-pill active' : 'stock-pill';
  }
  st_for(ticker, 'overview');
  updateUbNext(ticker);
  reobserve();
}

function updateUbNext(ticker) {
  var info = nextEarningsData[ticker];
  var el = document.getElementById('ubNextText');
  if (!info || !info.date) {
    el.textContent = ticker + ' \u2014 \uc2e4\uc801\ubc1c\ud45c \uc77c\uc815 \ubbf8\uc815 (\ud074\ub9ad\ud558\uc5ec \uc5c5\ub370\uc774\ud2b8 \ubc29\ubc95 \ud655\uc778)';
  } else {
    el.textContent = '\ub2e4\uc74c \uc2e4\uc801\ubc1c\ud45c: ' + info.date + ' \u2014 ' + ticker + ' ' + info.quarter;
  }
  var msi = document.getElementById('modalStockInfo');
  if (msi) {
    if (info && info.date) {
      msi.innerHTML = '<div class="msi-ticker">' + ticker + '</div><div class="msi-detail"><span class="msi-date">' + info.name + '</span><br/>' + info.quarter + ' \uc2e4\uc801\ubc1c\ud45c \uc608\uc815: <strong>' + info.date + '</strong></div>';
    } else {
      msi.innerHTML = '<div class="msi-ticker">' + ticker + '</div><div class="msi-detail"><span class="msi-date">' + info.name + '</span><br/>\uc2e4\uc801\ubc1c\ud45c \uc77c\uc815\uc774 \uc544\uc9c1 \ud655\uc815\ub418\uc9c0 \uc54a\uc558\uc2b5\ub2c8\ub2e4.</div>';
    }
  }
}

function toggleUpdateModal() {
  var modal = document.getElementById('updateModal');
  modal.classList.toggle('open');
}

function closeModal(e) {
  if (e.target === e.currentTarget) {
    e.target.classList.remove('open');
  }
}

function st_for(ticker, id) {
  var tabNames = ['overview','financial','segments','valuation','earnings','invest'];
  var bar = document.getElementById('tabBar-' + ticker);
  var tabs = bar.querySelectorAll('.tab');
  for (var i = 0; i < tabs.length; i++) tabs[i].className = (i === tabNames.indexOf(id)) ? 'tab active' : 'tab';
  for (var i = 0; i < tabNames.length; i++) {
    var el = document.getElementById('t-' + ticker + '-' + tabNames[i]);
    if (el) el.className = (tabNames[i] === id) ? 'tc active' : 'tc';
  }
}

function sst_for(ticker, prefix, view) {
  var containerId = prefix === 'fin' ? 'finSubTabs-' + ticker : 'segSubTabs-' + ticker;
  var container = document.getElementById(containerId);
  if (!container) return;
  var stabs = container.querySelectorAll('.sub-tab');
  for (var i = 0; i < stabs.length; i++) stabs[i].className = 'sub-tab';
  stabs[view === 'annual' ? 0 : 1].className = 'sub-tab active';
  var annualPane = document.getElementById(prefix + '-' + ticker + '-annual');
  var quarterlyPane = document.getElementById(prefix + '-' + ticker + '-quarterly');
  if (annualPane && quarterlyPane) {
    if (view === 'annual') {
      annualPane.className = 'sub-pane active';
      quarterlyPane.className = 'sub-pane';
    } else {
      annualPane.className = 'sub-pane';
      quarterlyPane.className = 'sub-pane active';
    }
  }
}

function reobserve() {
  var els = document.querySelectorAll('.reveal:not(.visible)');
  els.forEach(function(el, i) {
    el.style.animationDelay = (i * 60) + 'ms';
    observer.observe(el);
  });
}

var observer = new IntersectionObserver(function(entries) {
  entries.forEach(function(e) {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      observer.unobserve(e.target);
    }
  });
}, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

document.addEventListener('DOMContentLoaded', function() {
  var els = document.querySelectorAll('.reveal');
  els.forEach(function(el, i) {
    el.style.animationDelay = (i * 60) + 'ms';
    observer.observe(el);
  });
  selectStock('NVDA');
});
</script>
</body>
</html>'''

# Write to file
output_dir = "/sessions/exciting-gracious-pasteur/mnt/02-projects/2026.03.28 기업분석대시보드/output"
os.makedirs(output_dir, exist_ok=True)
output_path = f"{output_dir}/기업분석_포트폴리오대시보드_v5_2026.03.28.html"

with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Portfolio Dashboard v5 generated: {output_path}")
print(f"File size: {len(html):,} bytes")
print(f"Total stocks: {len(STOCK_ORDER)}")

# Count elements for verification
stock_section_count = html.count('class="stock-section"')
stock_pill_count = html.count('class="stock-pill')
tab_count = html.count('class="tab"')
fin_item_count = html.count('class="fin-item"')
earn_card_count = html.count('class="earn-card')
section_card_count = html.count('class="section-card"')
sub_tab_count = html.count('class="sub-tab')
kpi_count = html.count('class="kpi"')

print(f"\nElement counts:")
print(f"  stock-section: {stock_section_count}")
print(f"  stock-pill: {stock_pill_count}")
print(f"  tab: {tab_count}")
print(f"  fin-item: {fin_item_count}")
print(f"  earn-card: {earn_card_count}")
print(f"  section-card: {section_card_count}")
print(f"  sub-tab: {sub_tab_count}")
print(f"  kpi: {kpi_count}")
