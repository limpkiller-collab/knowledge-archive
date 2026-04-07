#!/usr/bin/env python3
"""Portfolio Dashboard v4 — 10종목 통합 포트폴리오, v13 Supanova 디자인 동일
- 10개 종목 (NVDA, AAPL, MSFT, GOOGL, O, ABBV, PLTR, CRWV, IONQ, SMR)
- 각 종목별 6개 탭 (기업개요, 재무분석, 사업부문, 밸류에이션, 실적발표, 투자포인트)
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
# GENERATE PORTFOLIO HTML — ONE FILE WITH ALL 10 STOCKS
# ══════════════════════════════════════════════════════════════════════════════

html_sections = []

for ticker in STOCK_ORDER:
    stock_data = STOCKS[ticker]
    profile = stock_data.get("profile", {})
    accent_color = profile.get("accent", "#76b900")

    # Tab 1: Overview
    overview_money = stock_data.get("overview_money", [])
    overview_growth = stock_data.get("overview_growth", [])
    overview_risks = stock_data.get("overview_risks", [])

    overview_money_html = gen_overview_section("주요 수입원", "돈을 버는 방법", overview_money, f"linear-gradient(135deg,{accent_color}20,{accent_color}40)")
    overview_growth_html = gen_overview_section("미래 성장 동력", "성장의 가능성", overview_growth, "linear-gradient(135deg,#0a2a4a,#1a3a5a)")
    overview_risks_html = gen_overview_section("주의해야 할 점", "잠재 위험 요소", overview_risks, "linear-gradient(135deg,#3a2a00,#4a3500)")

    # Tab 2: Financial
    financial_items = stock_data.get("financial_items", [])
    quarterly_financial_items = stock_data.get("quarterly_financial_items", [])

    financial_html = gen_financial_section(financial_items)
    quarterly_financial_html = gen_financial_section(quarterly_financial_items)
    fin_table_html = fin_table(stock_data)

    # Tab 3: Segments
    seg_table_html = seg_table(stock_data)
    q_seg_table_html = q_seg_table(stock_data)
    segments = stock_data.get("segments", {})
    quarterly_segments = stock_data.get("quarterly_segments", {})

    seg_chart_html = svg_stacked_bar(segments.get("labels",[]), segments.get("series",[])) if segments.get("labels") else ""
    q_seg_chart_html = svg_stacked_bar(quarterly_segments.get("labels",[]), quarterly_segments.get("series",[])) if quarterly_segments.get("labels") else ""

    # Tab 4: Valuation
    ratios = stock_data.get("ratios", {})
    peers = stock_data.get("peers", [])
    peer_table_html = peer_table(stock_data)

    # Tab 5: Earnings
    earnings_quarters = stock_data.get("earnings_quarters", [])
    earnings_rev_chart = svg_earnings_compare(earnings_quarters)
    earnings_eps_chart = svg_eps_surprise(earnings_quarters)
    earnings_cards_html = earnings_call_cards(stock_data)
    next_earn_html = next_earnings_card(stock_data)

    # Tab 6: Investment
    invest_html_content = invest_html(stock_data)

    # Build HTML for this stock
    stock_html = f'''<div class="stock-container" data-ticker="{ticker}">
  <div class="stock-header">
    <div class="stock-profile">
      <div class="stock-name">{profile.get("name","")}</div>
      <div class="stock-symbol">{ticker}</div>
      <div class="stock-meta">
        <span>{profile.get("sector","")}</span>
        <span>•</span>
        <span>{profile.get("industry","")}</span>
      </div>
      <div class="stock-price">
        <div class="price-main">${profile.get("price",0):.2f}</div>
        <div class="price-change {("up" if profile.get("changes",0)>0 else "down")}">{profile.get("changesPct",0):+.2f}%</div>
      </div>
    </div>
    <div class="stock-desc">{profile.get("desc","")}</div>
  </div>

  <div class="tabs">
    <div class="tab-buttons">
      <button class="tab-btn active" onclick="switchTab('{ticker}',0)">기업개요</button>
      <button class="tab-btn" onclick="switchTab('{ticker}',1)">재무분석</button>
      <button class="tab-btn" onclick="switchTab('{ticker}',2)">사업부문</button>
      <button class="tab-btn" onclick="switchTab('{ticker}',3)">밸류에이션</button>
      <button class="tab-btn" onclick="switchTab('{ticker}',4)">실적발표</button>
      <button class="tab-btn" onclick="switchTab('{ticker}',5)">투자포인트</button>
    </div>

    <div class="tab-pane active">
      {overview_money_html}
      {overview_growth_html}
      {overview_risks_html}
    </div>

    <div class="tab-pane">
      <div class="sub-tabs">
        <button class="sub-tab active" onclick="sst('{ticker}',\'annual\')">연간</button>
        <button class="sub-tab" onclick="sst('{ticker}',\'quarterly\')">분기</button>
      </div>
      <div id="{ticker}-annual" class="sub-pane active">
        <h3>연간 재무지표</h3>
        {financial_html}
        {fin_table_html}
      </div>
      <div id="{ticker}-quarterly" class="sub-pane">
        <h3>분기별 하이라이트</h3>
        {quarterly_financial_html}
        <h3>분기별 재무지표</h3>
        {q_detail_table(stock_data)}
      </div>
    </div>

    <div class="tab-pane">
      <div class="sub-tabs">
        <button class="sub-tab active" onclick="sst('{ticker}',\'annual\')">연간</button>
        <button class="sub-tab" onclick="sst('{ticker}',\'quarterly\')">분기</button>
      </div>
      <div id="{ticker}-seg-annual" class="sub-pane active">
        <h3>사업부문별 매출 추이</h3>
        {seg_chart_html}
        {seg_table_html}
      </div>
      <div id="{ticker}-seg-quarterly" class="sub-pane">
        <h3>분기별 사업부문 매출</h3>
        {q_seg_chart_html}
        {q_seg_table_html}
      </div>
    </div>

    <div class="tab-pane">
      <h3>주요 지표</h3>
      <div class="kpi-grid">
        <div class="kpi"><div class="kpi-label">P/E</div><div class="kpi-value">{ratios.get("pe","")}</div></div>
        <div class="kpi"><div class="kpi-label">P/S</div><div class="kpi-value">{ratios.get("ps","")}</div></div>
        <div class="kpi"><div class="kpi-label">ROE</div><div class="kpi-value">{ratios.get("roe","")}</div></div>
        <div class="kpi"><div class="kpi-label">배당수익률</div><div class="kpi-value">{ratios.get("div","")}</div></div>
      </div>
      <h3>경쟁사 비교</h3>
      {peer_table_html}
    </div>

    <div class="tab-pane">
      <h3>실적 서프라이즈 분석</h3>
      <div class="chart-row">
        <div class="chart-col">
          <h4>매출 (Revenue)</h4>
          {earnings_rev_chart}
        </div>
        <div class="chart-col">
          <h4>EPS</h4>
          {earnings_eps_chart}
        </div>
      </div>
      <h3>분기별 실적 발표</h3>
      {earnings_cards_html}
      <h3>다음 실적발표</h3>
      {next_earn_html}
    </div>

    <div class="tab-pane">
      {invest_html_content}
    </div>
  </div>
</div>'''

    html_sections.append(stock_html)

# ══════════════════════════════════════════════════════════════════════════════
# FULL HTML OUTPUT WITH CSS & JAVASCRIPT
# ══════════════════════════════════════════════════════════════════════════════

html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>포트폴리오 대시보드 v4 - 10 종목 통합 분석</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;500;600;700&Noto+Sans+KR:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
:root{{
  --bg:"#0f0f0f";--bg2:"#1a1a1a";--bg3:"#2a2a2a";--text:"#e4e6f0";--text2:"#9ca0b8";--accent:"#76b900";--green:"#4ecdc4";--red:"#ff6b6b";--border:"#2d3148"}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:var(--bg);color:var(--text);font-family:"Noto Sans KR",sans-serif;line-height:1.6}}
.container{{max-width:1400px;margin:0 auto;padding:40px 20px}}
.dashboard-header{{padding:30px;border-bottom:2px solid var(--border);margin-bottom:40px}}
.header-title{{font-size:32px;font-weight:700;margin-bottom:10px}}
.header-meta{{font-size:13px;color:var(--text2);display:flex;gap:20px}}
.stock-container{{margin-bottom:80px;border-radius:12px;overflow:hidden;border:1px solid var(--border)}}
.stock-header{{padding:30px;background:linear-gradient(135deg,#1a1a2e,#16213e);border-bottom:2px solid var(--border)}}
.stock-profile{{display:flex;justify-content:space-between;align-items:start;margin-bottom:20px}}
.stock-name{{font-size:24px;font-weight:700}}
.stock-symbol{{font-size:14px;color:var(--text2);margin:5px 0}}
.stock-meta{{font-size:12px;color:var(--text2)}}
.stock-price{{text-align:right}}
.price-main{{font-size:28px;font-weight:700}}
.price-change{{font-size:14px;margin-top:5px}}
.price-change.up{{color:var(--accent)}}
.price-change.down{{color:var(--red)}}
.stock-desc{{font-size:13px;color:var(--text2);line-height:1.6}}
.tabs{{}}
.tab-buttons{{display:flex;border-bottom:1px solid var(--border);background:var(--bg2)}}
.tab-btn{{flex:1;padding:16px;border:none;background:none;color:var(--text2);cursor:pointer;font-size:13px;border-bottom:3px solid transparent;transition:all .2s}}
.tab-btn.active{{color:var(--text);border-bottom-color:var(--accent)}}
.tab-btn:hover{{color:var(--text)}}
.tab-pane{{display:none;padding:30px;background:var(--bg)}}
.tab-pane.active{{display:block}}
.section-card{{margin-bottom:30px;border-radius:8px;overflow:hidden;border:1px solid var(--border)}}
.section-header{{padding:20px;color:#fff;font-weight:600}}
.section-subtitle{{font-size:12px;text-transform:uppercase;letter-spacing:1px;opacity:.7;margin-bottom:5px}}
.section-title{{font-size:18px;font-weight:700}}
.section-body{{padding:20px;background:var(--bg)}}
.insight-item{{margin-bottom:20px;padding-bottom:20px;border-bottom:1px solid var(--border)}}
.insight-item:last-child{{border-bottom:none}}
.insight-header{{display:flex;gap:12px;margin-bottom:10px;align-items:center}}
.insight-emoji{{font-size:20px}}
.insight-title{{font-size:14px;font-weight:600}}
.insight-desc{{font-size:13px;color:var(--text2);line-height:1.7}}
.fin-category{{margin-bottom:30px}}
.fin-cat-title{{font-size:14px;font-weight:700;margin-bottom:15px;color:var(--accent);text-transform:uppercase}}
.fin-item{{margin-bottom:20px;padding:15px;background:var(--bg2);border-radius:8px;border:1px solid var(--border)}}
.fin-item-label{{font-size:12px;color:var(--text2);margin-bottom:8px}}
.fin-item-headline{{font-size:13px;font-weight:600;margin-bottom:10px}}
.fin-emoji{{font-size:14px;margin-right:6px}}
.fin-metric-row{{display:flex;justify-content:space-between;margin-bottom:10px}}
.fin-metric-value{{font-size:14px;font-weight:700;color:var(--accent)}}
.fin-metric-change{{font-size:12px}}
.fin-item-desc{{font-size:12px;color:var(--text2);line-height:1.6}}
.src-badge{{display:inline-block;font-size:9px;padding:3px 8px;border-radius:3px;margin-left:6px}}
.src-badge.verified{{background:rgba(76,205,196,.15);color:#4ecdc4}}
.src-badge.estimate{{background:rgba(255,107,107,.15);color:#ff6b6b}}
table{{width:100%;border-collapse:collapse;margin:20px 0;border:1px solid var(--border)}}
table thead{{background:var(--bg2)}}
table th,table td{{padding:12px;text-align:left;border-bottom:1px solid var(--border)}}
table th{{font-weight:600;color:var(--accent)}}
table td.nr{{text-align:right;font-family:"Geist Mono",monospace}}
table td.up{{color:var(--accent)}}
table td.down{{color:var(--red)}}
.sub-tabs{{display:flex;gap:10px;margin-bottom:20px;border-bottom:1px solid var(--border)}}
.sub-tab{{padding:10px 15px;background:none;border:none;color:var(--text2);cursor:pointer;font-size:12px;border-bottom:2px solid transparent}}
.sub-tab.active{{color:var(--text);border-bottom-color:var(--accent)}}
.sub-pane{{display:none}}
.sub-pane.active{{display:block}}
.chart-row{{display:grid;grid-template-columns:1fr 1fr;gap:30px;margin:20px 0}}
.chart-col{{}}
.chart-col h4{{font-size:13px;font-weight:600;margin-bottom:15px}}
.kpi-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin:20px 0}}
.kpi{{padding:15px;background:var(--bg2);border-radius:8px;border:1px solid var(--border);text-align:center}}
.kpi-label{{font-size:12px;color:var(--text2);margin-bottom:8px}}
.kpi-value{{font-size:16px;font-weight:700;color:var(--accent)}}
.earn-card{{margin-bottom:20px;padding:20px;background:var(--bg2);border-radius:8px;border:1px solid var(--border);animation:fadeIn .3s ease}}
.earn-header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:15px;padding-bottom:15px;border-bottom:1px solid var(--border)}}
.earn-q{{font-size:14px;font-weight:700;color:var(--accent)}}
.earn-date{{font-size:12px;color:var(--text2)}}
.earn-surprise{{font-size:12px;font-weight:600;padding:4px 10px;border-radius:4px}}
.earn-surprise.up{{background:rgba(76,205,196,.15);color:#4ecdc4}}
.earn-surprise.down{{background:rgba(255,107,107,.15);color:#ff6b6b}}
.earn-badges{{display:flex;gap:8px;margin-bottom:15px;flex-wrap:wrap}}
.earn-badge{{display:inline-block;font-size:11px;padding:4px 10px;background:var(--bg);border-radius:4px;border:1px solid var(--border)}}
.earn-metrics{{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin-bottom:15px}}
.earn-metric{{}}
.earn-metric-label{{font-size:11px;color:var(--text2);margin-bottom:6px}}
.earn-metric-val{{font-size:13px;font-weight:700;color:var(--accent)}}
.earn-metric-val.up{{color:var(--accent)}}
.earn-metric-val.down{{color:var(--red)}}
.earn-metric-sub{{font-size:11px;color:var(--text2);margin-top:4px}}
.earn-ceo{{margin:15px 0;padding:15px;background:var(--bg);border-radius:6px;border-left:3px solid var(--accent)}}
.earn-ceo-label{{font-size:12px;font-weight:600;margin-bottom:8px}}
.earn-ceo-quote{{font-size:12px;color:var(--text2);font-style:italic;line-height:1.6}}
.earn-highlights{{margin:15px 0}}
.earn-hl-title{{font-size:12px;font-weight:600;margin-bottom:10px}}
.earn-highlights ul{{list-style:none;padding-left:0}}
.earn-highlights li{{font-size:12px;color:var(--text2);margin-bottom:8px;padding-left:20px;position:relative}}
.earn-highlights li:before{{content:"▸";position:absolute;left:0;color:var(--accent)}}
.earn-analyst{{margin:15px 0}}
.earn-analyst-title{{font-size:12px;font-weight:600;margin-bottom:10px}}
.earn-analyst p{{font-size:12px;color:var(--text2);line-height:1.7}}
.next-earn{{padding:20px;background:var(--bg2);border-radius:8px;border:1px solid var(--accent);animation:fadeIn .3s ease}}
.next-earn-header{{display:flex;gap:15px;margin-bottom:20px;padding-bottom:20px;border-bottom:1px solid var(--border)}}
.next-earn-icon{{font-size:24px}}
.next-earn-title{{font-size:14px;font-weight:700}}
.next-earn-date{{font-size:12px;color:var(--text2);margin-top:4px}}
.next-earn-countdown{{text-align:right;font-size:13px;font-weight:700;color:var(--accent)}}
.next-earn-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin-bottom:20px}}
.next-earn-item{{padding:12px;background:var(--bg);border-radius:6px}}
.ne-label{{font-size:11px;color:var(--text2);margin-bottom:6px}}
.ne-value{{font-size:13px;font-weight:700}}
.ne-sub{{font-size:11px;color:var(--text2);margin-top:4px}}
.next-earn-watch{{}}
.ne-watch-title{{font-size:12px;font-weight:600;margin-bottom:10px}}
.next-earn-watch ul{{list-style:none}}
.next-earn-watch li{{font-size:12px;color:var(--text2);padding:6px 0;padding-left:20px;position:relative}}
.next-earn-watch li:before{{content:"✓";position:absolute;left:0;color:var(--accent)}}
.invest-card{{margin-bottom:20px;padding:20px;background:var(--bg2);border-radius:8px;border:1px solid var(--border)}}
.invest-card h4{{font-size:13px;font-weight:700;margin-bottom:12px;display:flex;gap:10px;align-items:center}}
.dot{{width:8px;height:8px;border-radius:50%}}
.dot-green{{background:var(--accent)}}
.dot-red{{background:var(--red)}}
.dot-blue{{background:#4dabf7}}
.dot-orange{{background:#ffa500}}
.invest-card ul{{list-style:none}}
.invest-card li{{font-size:12px;color:var(--text2);margin-bottom:8px;padding-left:20px;position:relative}}
.invest-card li:before{{content:"•";position:absolute;left:0;color:var(--accent)}}
.reveal{{opacity:0;animation:slideUp .5s ease forwards}}
@keyframes slideUp{{from{{opacity:0;transform:translateY(20px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes fadeIn{{from{{opacity:0}}to{{opacity:1}}}}
@media(max-width:768px){{
  .chart-row{{grid-template-columns:1fr}}
  .kpi-grid{{grid-template-columns:repeat(2,1fr)}}
  .next-earn-grid{{grid-template-columns:1fr}}
  .earn-metrics{{grid-template-columns:repeat(2,1fr)}}
}}
  </style>
</head>
<body>
<div class="container">
  <div class="dashboard-header">
    <div class="header-title">포트폴리오 대시보드 v4</div>
    <div class="header-meta">
      <span>작성기준일: {DASHBOARD_META["created_date"]}</span>
      <span>데이터 출처: {DASHBOARD_META["data_source"]}</span>
      <span>다음 업데이트: {DASHBOARD_META["next_update_date"]}</span>
    </div>
  </div>

{''.join(html_sections)}
</div>

<script>
function switchTab(ticker, tabIndex) {{
  var container = document.querySelector('[data-ticker="' + ticker + '"]');
  var panes = container.querySelectorAll('.tab-pane');
  var btns = container.querySelectorAll('.tab-btn');
  for (var i = 0; i < panes.length; i++) {{
    panes[i].classList.remove('active');
    btns[i].classList.remove('active');
  }}
  panes[tabIndex].classList.add('active');
  btns[tabIndex].classList.add('active');
}}

function sst(ticker, view) {{
  var container = document.querySelector('[data-ticker="' + ticker + '"]');
  var tabs = container.querySelectorAll('.sub-tab');
  var panes = container.querySelectorAll('.sub-pane');
  for (var i = 0; i < tabs.length; i++) {{
    tabs[i].classList.remove('active');
    panes[i].classList.remove('active');
  }}
  if (view === 'annual') {{
    tabs[0].classList.add('active');
    panes[0].classList.add('active');
  }} else {{
    tabs[1].classList.add('active');
    panes[1].classList.add('active');
  }}
}}

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
output_dir = "/sessions/exciting-gracious-pasteur/mnt/자산 대시보드 제작/02-projects/2026.03.28 기업분석대시보드/output"
os.makedirs(output_dir, exist_ok=True)
output_path = f"{output_dir}/포트폴리오_통합분석_v4_2026.03.28.html"

with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Portfolio Dashboard v4 generated: {output_path}")
print(f"File size: {len(html):,} bytes")
print(f"Total stocks: {len(STOCK_ORDER)}")

# Count elements for verification
fin_item_count = html.count('class="fin-item"')
earn_card_count = html.count('class="earn-card')
section_card_count = html.count('class="section-card"')
sub_tab_count = html.count('class="sub-tab')
kpi_count = html.count('class="kpi"')

print(f"\nElement counts:")
print(f"  fin-item: {fin_item_count}")
print(f"  earn-card: {earn_card_count}")
print(f"  section-card: {section_card_count}")
print(f"  sub-tab: {sub_tab_count}")
print(f"  kpi: {kpi_count}")
