#!/usr/bin/env python3
"""v4: Static NVDA + dynamic ticker search with pure SVG charts (no CDN)."""
import math

# ── NVDA Data (same as v3) ──
PROFILE = {
    "symbol":"NVDA","name":"NVIDIA Corporation","price":167.52,
    "changes":-2.31,"changesPct":-1.36,"exchange":"NASDAQ",
    "sector":"Technology","industry":"Semiconductors","country":"US",
    "mktCap":4070000000000,"beta":2.37,"lastDiv":0.04,
    "range":"86.62 - 212.19","employees":"36,000",
    "desc":"NVIDIA는 GPU(그래픽 처리 장치) 및 AI 컴퓨팅 플랫폼의 글로벌 리더입니다. 데이터센터, 게이밍, 자동차, 전문 시각화 등 다양한 시장에서 AI 가속 컴퓨팅 솔루션을 제공합니다."
}
INCOME = [
    {"year":"2022","rev":26.91,"ni":9.75,"oi":10.04,"gp":17.48,"eps":0.39,"gm":64.93,"om":37.31,"nm":36.23},
    {"year":"2023","rev":26.97,"ni":4.37,"oi":4.22,"gp":15.36,"eps":0.17,"gm":56.93,"om":15.66,"nm":16.19},
    {"year":"2024","rev":60.92,"ni":29.76,"oi":32.97,"gp":44.30,"eps":1.19,"gm":72.72,"om":54.12,"nm":48.85},
    {"year":"2025","rev":130.50,"ni":72.88,"oi":81.45,"gp":97.87,"eps":2.94,"gm":74.99,"om":62.42,"nm":55.85},
    {"year":"2026","rev":215.94,"ni":120.07,"oi":130.39,"gp":153.44,"eps":4.90,"gm":71.07,"om":60.38,"nm":55.60},
]
QUARTERLY = [
    {"q":"Q1'25","rev":26.04,"ni":14.88},{"q":"Q2'25","rev":30.04,"ni":16.60},
    {"q":"Q3'25","rev":35.08,"ni":19.31},{"q":"Q4'25","rev":39.33,"ni":22.09},
    {"q":"Q1'26","rev":41.79,"ni":19.31},{"q":"Q2'26","rev":49.92,"ni":24.50},
    {"q":"Q3'26","rev":56.10,"ni":33.30},{"q":"Q4'26","rev":68.13,"ni":42.96},
]
SEGMENTS = {
    "labels":["FY2022","FY2023","FY2024","FY2025","FY2026"],
    "series":[
        {"name":"Data Center","color":"#76b900","data":[10.6,15.0,47.5,115.2,193.7]},
        {"name":"Gaming","color":"#4ecdc4","data":[12.5,9.1,10.4,11.4,16.0]},
        {"name":"Pro Vis","color":"#4dabf7","data":[2.1,1.5,1.6,1.9,3.2]},
        {"name":"Automotive","color":"#b197fc","data":[0.6,0.9,1.1,1.7,2.4]},
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
INVEST = {
    "strengths":["AI 인프라 시장 절대 지배력: 데이터센터 GPU 시장 점유율 90%+ 유지","CUDA 생태계 락인: 소프트웨어 플랫폼으로 강력한 진입장벽 형성","FY2026 매출 $215.9B, 전년 대비 65% 성장의 초고성장 지속","순이익률 55.6%로 반도체 업계 최고 수준의 수익성"],
    "risks":["미중 반도체 수출 규제 강화에 따른 중국향 매출 감소 리스크","AMD MI300X, Intel Gaudi3, 자체 ASIC(Google TPU, AWS Trainium) 등 경쟁 심화","AI 인프라 투자 사이클 둔화 가능성 (Capex 피크 논쟁)","고밸류에이션 부담: Trailing P/E 34x, 기대치 미달 시 급락 가능"],
    "opportunities":["Sovereign AI: 각국 정부의 자체 AI 인프라 구축 수요 급증","Blackwell Ultra / Rubin 차세대 아키텍처로 성능 리더십 유지","AI 추론(Inference) 시장 본격 성장 — 학습 대비 훨씬 큰 시장","자율주행 / 로보틱스: DRIVE Thor, Isaac 플랫폼으로 새 성장동력"],
    "watchlist":["FY2027 Q1 가이던스 $45B (시장 기대 상회 여부)","Blackwell Ultra 양산 일정 및 수율 (H2 2026)","중국 수출 규제 완화/강화 방향성","AI Capex 투자 추이: MSFT, GOOG, META, AMZN의 분기별 설비투자"]
}
RATIOS = {"pe":34.18,"fpe":20.19,"ps":18.84,"peg":0.53,"roe":"127.5%","div":"0.02%"}

# ── SVG generators (same as v3) ──
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

# ── Generate static charts ──
rev_chart=svg_grouped_bar([f'FY{d["year"]}' for d in INCOME],[{"label":"매출","color":"#76b900","data":[d["rev"] for d in INCOME]},{"label":"순이익","color":"#4ecdc4","data":[d["ni"] for d in INCOME]}])
margin_chart=svg_line_chart([f'FY{d["year"]}' for d in INCOME],[{"label":"매출총이익률","color":"#76b900","data":[d["gm"] for d in INCOME]},{"label":"영업이익률","color":"#4dabf7","data":[d["om"] for d in INCOME]},{"label":"순이익률","color":"#b197fc","data":[d["nm"] for d in INCOME]}])
q_chart=svg_grouped_bar([d["q"] for d in QUARTERLY],[{"label":"분기 매출","color":"#76b900","data":[d["rev"] for d in QUARTERLY]},{"label":"분기 순이익","color":"#4ecdc4","data":[d["ni"] for d in QUARTERLY]}])
donut_chart=svg_donut([{"name":s["name"],"value":s["data"][-1],"color":s["color"]} for s in SEGMENTS["series"]])
stacked_chart=svg_stacked_bar(SEGMENTS["labels"],SEGMENTS["series"])

def svg_eps_per():
    W,H=580,260; pad_l,pad_r,pad_t,pad_b=55,55,15,45; cW=W-pad_l-pad_r; cH=H-pad_t-pad_b
    eps_vals=[d["eps"] for d in INCOME]; per_vals=[167.52/e if e>0 else 0 for e in eps_vals]
    max_eps=max(eps_vals)*1.2; max_per=max(per_vals)*1.2; n=len(INCOME); bw=cW/n*0.5
    lines=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
    for g in range(5):
        y=pad_t+cH-(cH*g/4)
        lines.append(f'<line x1="{pad_l}" y1="{y}" x2="{W-pad_r}" y2="{y}" stroke="#2d3148"/>')
        lines.append(f'<text x="{pad_l-6}" y="{y+4}" fill="#76b900" font-size="9" text-anchor="end">${max_eps*g/4:.1f}</text>')
        lines.append(f'<text x="{W-pad_r+6}" y="{y+4}" fill="#ffa94d" font-size="9">{max_per*g/4:.0f}x</text>')
    for i,e in enumerate(eps_vals):
        x=pad_l+i*(cW/n)+(cW/n-bw)/2; bh=(e/max_eps)*cH; y=pad_t+cH-bh
        lines.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="3" fill="#76b900" opacity="0.7"/>')
        lines.append(f'<text x="{x+bw/2:.1f}" y="{y-3}" fill="#76b900" font-size="8" text-anchor="middle" font-weight="600">${e:.2f}</text>')
    pts=[]
    for i,pe in enumerate(per_vals):
        x=pad_l+i*(cW/n)+cW/n/2; y=pad_t+cH-(pe/max_per)*cH; pts.append(f"{x:.1f},{y:.1f}")
    lines.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#ffa94d" stroke-width="2.5"/>')
    for i,pe in enumerate(per_vals):
        x=pad_l+i*(cW/n)+cW/n/2; y=pad_t+cH-(pe/max_per)*cH
        lines.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#ffa94d"/>')
        lines.append(f'<text x="{x:.1f}" y="{y-7}" fill="#ffa94d" font-size="8" text-anchor="middle" font-weight="600">{pe:.1f}x</text>')
    for i,d in enumerate(INCOME):
        x=pad_l+i*(cW/n)+cW/n/2; lines.append(f'<text x="{x:.1f}" y="{H-pad_b+18}" fill="#9ca0b8" font-size="10" text-anchor="middle">FY{d["year"]}</text>')
    lines.append(f'<rect x="{pad_l}" y="{H-10}" width="8" height="8" rx="2" fill="#76b900"/><text x="{pad_l+12}" y="{H-3}" fill="#9ca0b8" font-size="9">EPS</text>')
    lines.append(f'<rect x="{pad_l+50}" y="{H-10}" width="8" height="8" rx="2" fill="#ffa94d"/><text x="{pad_l+62}" y="{H-3}" fill="#9ca0b8" font-size="9">P/E (현재가 기준)</text>')
    lines.append('</svg>'); return '\n'.join(lines)

eps_per_chart=svg_eps_per()
rev_g=((INCOME[-1]["rev"]-INCOME[-2]["rev"])/INCOME[-2]["rev"]*100)
ni_g=((INCOME[-1]["ni"]-INCOME[-2]["ni"])/INCOME[-2]["ni"]*100)

# ── Tables ──
def fin_table():
    rows=[("매출 (Revenue)",[f"${d['rev']:.1f}B" for d in INCOME]),("매출총이익 (Gross Profit)",[f"${d['gp']:.1f}B" for d in INCOME]),("영업이익 (Operating Income)",[f"${d['oi']:.1f}B" for d in INCOME]),("순이익 (Net Income)",[f"${d['ni']:.1f}B" for d in INCOME]),("EPS (희석)",[f"${d['eps']:.2f}" for d in INCOME]),("매출총이익률",[f"{d['gm']:.1f}%" for d in INCOME]),("영업이익률",[f"{d['om']:.1f}%" for d in INCOME]),("순이익률",[f"{d['nm']:.1f}%" for d in INCOME])]
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
        bg=' style="background:rgba(118,185,0,.1);"' if p["hl"] else ''; sym=f'<strong>{p["sym"]}</strong>' if p["hl"] else p["sym"]
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

peer_pe_bars=''.join(f'<rect x="{50+i*90}" y="{180-float(p["pe"])/40*140 if p["pe"]!="-" else 180}" width="60" height="{float(p["pe"])/40*140 if p["pe"]!="-" else 0}" rx="4" fill="{"#76b900" if p["hl"] else "#4dabf7"}" opacity="0.8"/><text x="{80+i*90}" y="{175-float(p["pe"])/40*140 if p["pe"]!="-" else 175}" fill="{"#76b900" if p["hl"] else "#4dabf7"}" font-size="10" text-anchor="middle" font-weight="600">{p["pe"]}x</text><text x="{80+i*90}" y="198" fill="#9ca0b8" font-size="10" text-anchor="middle">{p["sym"]}</text>' for i,p in enumerate(PEERS) if p["pe"]!="-")

# ── Full HTML ──
html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>기업 종합분석 대시보드</title>
<style>
:root{{--bg:#0f1117;--card:#1a1d28;--card2:#232736;--border:#2d3148;--text:#e4e6f0;--text2:#9ca0b8;--accent:#76b900;--red:#ff6b6b;--blue:#4dabf7;--purple:#b197fc;--orange:#ffa94d;--green:#76b900;--radius:12px}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--text);min-height:100vh}}
.hdr{{background:linear-gradient(135deg,#1a1d28,#232736);padding:20px 32px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:16px;flex-wrap:wrap}}
.logo{{font-size:22px;font-weight:800;color:var(--accent)}}.logo span{{color:var(--text2);font-weight:400;font-size:14px;margin-left:8px}}
.search-box{{display:flex;align-items:center;gap:8px;margin-left:auto}}
.search-box input{{background:var(--bg);border:1px solid var(--border);color:var(--text);padding:10px 16px;border-radius:8px;font-size:15px;width:180px;outline:none;text-transform:uppercase}}
.search-box input:focus{{border-color:var(--accent)}}
.search-box button{{background:var(--accent);color:#000;border:none;padding:10px 20px;border-radius:8px;font-weight:700;cursor:pointer;font-size:14px}}
.search-box button:hover{{opacity:.85}}
.api-btn{{background:transparent!important;border:1px solid var(--border)!important;color:var(--text2)!important;padding:8px 14px!important;font-size:12px!important}}
.api-btn:hover{{border-color:var(--accent)!important;color:var(--accent)!important}}
.modal-bg{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:1000;justify-content:center;align-items:center}}
.modal-bg.show{{display:flex}}
.modal{{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:32px;max-width:480px;width:90%}}
.modal h3{{margin-bottom:12px}}.modal p{{color:var(--text2);font-size:13px;margin-bottom:16px;line-height:1.6}}
.modal input{{width:100%;background:var(--bg);border:1px solid var(--border);color:var(--text);padding:12px;border-radius:8px;font-size:14px;margin-bottom:16px}}
.modal .br{{display:flex;gap:8px;justify-content:flex-end}}
.modal button{{padding:10px 20px;border-radius:8px;border:none;cursor:pointer;font-weight:600}}
.btn-s{{background:var(--accent);color:#000}}.btn-c{{background:var(--card2);color:var(--text2)}}
.tabs{{display:flex;gap:4px;padding:16px 32px 0;background:var(--card);border-bottom:1px solid var(--border)}}
.tab{{padding:12px 24px;cursor:pointer;color:var(--text2);font-size:14px;font-weight:600;border-bottom:2px solid transparent}}
.tab:hover{{color:var(--text)}}.tab.active{{color:var(--accent);border-bottom-color:var(--accent)}}
.main{{max-width:1400px;margin:0 auto;padding:24px 32px}}
.tc{{display:none}}.tc.active{{display:block}}
.kpi-row{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin-bottom:24px}}
.kpi{{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:20px}}
.kpi-l{{font-size:12px;color:var(--text2);text-transform:uppercase;letter-spacing:1px;margin-bottom:8px}}
.kpi-v{{font-size:28px;font-weight:800;letter-spacing:-1px}}.kpi-s{{font-size:12px;margin-top:6px}}
.up{{color:var(--green)}}.down{{color:var(--red)}}
.cg{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:24px}}
.cc{{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:20px}}.cc.full{{grid-column:1/-1}}
.ct{{font-size:15px;font-weight:700;margin-bottom:16px;display:flex;align-items:center;gap:8px}}
.badge{{font-size:11px;background:var(--card2);color:var(--text2);padding:2px 8px;border-radius:4px;font-weight:500}}
.ch{{display:flex;align-items:center;gap:20px;margin-bottom:24px;padding:24px;background:var(--card);border:1px solid var(--border);border-radius:var(--radius)}}
.ch-tk{{font-size:36px;font-weight:900;color:var(--accent)}}.ch-nm{{font-size:18px}}.ch-desc{{font-size:13px;color:var(--text2);margin-top:4px;max-width:700px;line-height:1.5}}
.ch-meta{{margin-left:auto;text-align:right}}.ch-price{{font-size:32px;font-weight:800}}.ch-chg{{font-size:14px;margin-top:4px}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th{{background:var(--card2);color:var(--text2);padding:12px 16px;text-align:left;font-weight:600;white-space:nowrap;border-bottom:1px solid var(--border)}}
td{{padding:12px 16px;border-bottom:1px solid var(--border);white-space:nowrap}}tr:hover td{{background:rgba(118,185,0,.05)}}
.nr{{text-align:right;font-variant-numeric:tabular-nums}}
.ig{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.invest-card{{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:24px}}
.invest-card h4{{font-size:15px;margin-bottom:12px;display:flex;align-items:center;gap:8px}}
.invest-card ul{{list-style:none;padding:0}}.invest-card li{{padding:8px 0;color:var(--text2);font-size:13px;line-height:1.6;border-bottom:1px solid var(--border)}}
.invest-card li:last-child{{border:none}}
.dot{{width:8px;height:8px;border-radius:50%;display:inline-block}}.dot-green{{background:var(--green)}}.dot-red{{background:var(--red)}}.dot-blue{{background:var(--blue)}}.dot-orange{{background:var(--orange)}}
.wm{{text-align:center;padding:32px;color:var(--border);font-size:12px}}
svg{{width:100%;height:auto;display:block}}.tw{{overflow-x:auto}}
.loading{{text-align:center;padding:60px 20px;color:var(--text2)}}
.spinner{{width:36px;height:36px;border:3px solid var(--border);border-top-color:var(--accent);border-radius:50%;animation:spin .8s linear infinite;margin:0 auto 12px}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
#dynamicArea{{display:none}}
@media(max-width:768px){{.cg,.ig{{grid-template-columns:1fr}}.ch{{flex-direction:column;text-align:center}}.ch-meta{{margin-left:0;text-align:center}}.kpi-row{{grid-template-columns:repeat(2,1fr)}}}}
</style>
</head>
<body>

<!-- Header with search -->
<div class="hdr">
  <div class="logo">StockLens <span>기업 종합분석</span></div>
  <div class="search-box">
    <input id="tickerInput" type="text" placeholder="티커 입력 (예: AAPL)" value="NVDA" />
    <button onclick="searchTicker()">분석</button>
    <button class="api-btn" onclick="document.getElementById('apiModal').classList.add('show')">API Key</button>
  </div>
</div>

<!-- Tabs -->
<div class="tabs" id="tabBar">
  <div class="tab active" onclick="st('overview')">개요 &amp; 재무</div>
  <div class="tab" onclick="st('segments')">사업부문</div>
  <div class="tab" onclick="st('valuation')">밸류에이션</div>
  <div class="tab" onclick="st('invest')">투자 포인트</div>
</div>

<div class="main">

<!-- ===== STATIC NVDA CONTENT (pre-rendered, no JS needed) ===== -->
<div id="staticArea">

<div class="tc active" id="t-overview">
  <div class="ch">
    <div><div class="ch-tk">NVDA</div><div class="ch-nm">{PROFILE["name"]}</div><div class="ch-desc">{PROFILE["desc"]}</div><div style="margin-top:8px;font-size:12px;color:var(--text2);">{PROFILE["exchange"]} | {PROFILE["sector"]} | {PROFILE["industry"]} | {PROFILE["country"]}</div></div>
    <div class="ch-meta"><div class="ch-price">${PROFILE["price"]}</div><div class="ch-chg down">{PROFILE["changes"]} ({PROFILE["changesPct"]}%)</div><div style="font-size:12px;color:var(--text2);margin-top:8px;">52주: {PROFILE["range"]}</div></div>
  </div>
  <div class="kpi-row">
    <div class="kpi"><div class="kpi-l">시가총액</div><div class="kpi-v">$4.07T</div><div class="kpi-s">Beta: {PROFILE["beta"]}</div></div>
    <div class="kpi"><div class="kpi-l">연간 매출</div><div class="kpi-v">$215.9B</div><div class="kpi-s up">+{rev_g:.1f}% YoY</div></div>
    <div class="kpi"><div class="kpi-l">연간 순이익</div><div class="kpi-v">$120.1B</div><div class="kpi-s up">+{ni_g:.1f}% YoY</div></div>
    <div class="kpi"><div class="kpi-l">EPS</div><div class="kpi-v">$4.90</div><div class="kpi-s">순이익률 55.6%</div></div>
    <div class="kpi"><div class="kpi-l">P/E (TTM)</div><div class="kpi-v">34.2</div><div class="kpi-s">PEG: 0.53</div></div>
    <div class="kpi"><div class="kpi-l">매출총이익률</div><div class="kpi-v">71.1%</div><div class="kpi-s">영업이익률 60.4%</div></div>
  </div>
  <div class="cg">
    <div class="cc"><div class="ct">매출 &amp; 순이익 추이 <span class="badge">연간</span></div>{rev_chart}</div>
    <div class="cc"><div class="ct">수익성 지표 추이 <span class="badge">마진율</span></div>{margin_chart}</div>
    <div class="cc full"><div class="ct">분기별 매출 추이 <span class="badge">최근 8분기</span></div>{q_chart}</div>
  </div>
  <div class="cc"><div class="ct">연간 재무 데이터 <span class="badge">상세</span></div><div class="tw">{fin_table()}</div></div>
</div>

<div class="tc" id="t-segments">
  <div class="cg">
    <div class="cc"><div class="ct">사업부문별 매출 비중 <span class="badge">FY2026</span></div>{donut_chart}</div>
    <div class="cc"><div class="ct">사업부문별 매출 추이 <span class="badge">연간</span></div>{stacked_chart}</div>
    <div class="cc full"><div class="ct">사업부문 상세 데이터</div><div class="tw">{seg_table()}</div></div>
  </div>
</div>

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
    <div class="cc"><div class="ct">EPS 추이 &amp; PER 밴드 <span class="badge">연간</span></div>{eps_per_chart}</div>
    <div class="cc"><div class="ct">동종업계 P/E 비교</div><svg viewBox="0 0 580 200" xmlns="http://www.w3.org/2000/svg">{peer_pe_bars}</svg></div>
  </div>
  <div class="cc"><div class="ct">동종업계 밸류에이션 비교</div><div class="tw">{peer_table()}</div></div>
</div>

<div class="tc" id="t-invest"><div class="ig">{invest_html()}</div></div>

</div><!-- end staticArea -->

<!-- ===== DYNAMIC CONTENT (JS-rendered for other tickers) ===== -->
<div id="dynamicArea"></div>

</div><!-- end main -->

<!-- API Key Modal -->
<div class="modal-bg" id="apiModal">
  <div class="modal">
    <h3>FMP API Key 설정</h3>
    <p>Financial Modeling Prep의 무료 API 키를 입력하세요.<br><a href="https://financialmodelingprep.com/developer/docs/" target="_blank" style="color:var(--accent);">financialmodelingprep.com</a>에서 무료 가입 후 발급받을 수 있습니다. (무료 티어: 일 250회 요청)</p>
    <input id="apiKeyInput" type="text" placeholder="API Key를 입력하세요" />
    <div class="br">
      <button class="btn-c" onclick="document.getElementById('apiModal').classList.remove('show')">취소</button>
      <button class="btn-s" onclick="saveKey()">저장</button>
    </div>
  </div>
</div>

<div class="wm">StockLens Dashboard v4.0 | 데이터 출처: Financial Modeling Prep | 생성일: 2026.03.28</div>

<script>
/* ── Minimal JS: tab switching + dynamic ticker search ── */
var API_KEY = '';
try {{ API_KEY = localStorage.getItem('fmp_api_key') || ''; }} catch(e) {{}}

function st(id) {{
  var tabs = document.querySelectorAll('.tab');
  var names = ['overview','segments','valuation','invest'];
  for (var i = 0; i < tabs.length; i++) tabs[i].className = (i === names.indexOf(id)) ? 'tab active' : 'tab';
  var panes = document.querySelectorAll('.tc');
  for (var i = 0; i < panes.length; i++) panes[i].className = (panes[i].id === 't-' + id) ? 'tc active' : 'tc';
}}

function saveKey() {{
  API_KEY = document.getElementById('apiKeyInput').value.trim();
  try {{ localStorage.setItem('fmp_api_key', API_KEY); }} catch(e) {{}}
  document.getElementById('apiModal').classList.remove('show');
}}

function searchTicker() {{
  var ticker = document.getElementById('tickerInput').value.trim().toUpperCase();
  if (!ticker) return;
  if (ticker === 'NVDA') {{
    document.getElementById('staticArea').style.display = '';
    document.getElementById('dynamicArea').style.display = 'none';
    st('overview');
    return;
  }}
  if (!API_KEY) {{
    document.getElementById('staticArea').style.display = 'none';
    document.getElementById('dynamicArea').style.display = 'block';
    document.getElementById('dynamicArea').innerHTML = '<div class="loading"><div style="color:#ffa94d;font-size:16px;margin-bottom:12px;">API Key가 필요합니다</div><div style="color:#9ca0b8;font-size:13px;margin-bottom:16px;">NVDA 이외의 티커를 검색하려면 FMP API Key를 설정해주세요.<br><a href=\\"https://financialmodelingprep.com/developer/docs/\\" target=\\"_blank\\" style=\\"color:#76b900;\\">financialmodelingprep.com</a>에서 무료 가입 후 발급받을 수 있습니다.</div><button onclick=\\"document.getElementById(\'apiModal\').classList.add(\'show\')\\" style=\\"background:#76b900;color:#000;border:none;padding:12px 24px;border-radius:8px;font-weight:700;cursor:pointer;\\">API Key 설정하기</button></div>';
    return;
  }}
  // Show loading
  document.getElementById('staticArea').style.display = 'none';
  document.getElementById('dynamicArea').style.display = 'block';
  document.getElementById('dynamicArea').innerHTML = '<div class="loading"><div class="spinner"></div><div>'+ticker+' 데이터를 불러오는 중...</div></div>';

  var base = 'https://financialmodelingprep.com/api/v3';
  Promise.all([
    fetch(base+'/profile/'+ticker+'?apikey='+API_KEY).then(function(r){{return r.json();}}).catch(function(){{return null;}}),
    fetch(base+'/income-statement/'+ticker+'?limit=5&apikey='+API_KEY).then(function(r){{return r.json();}}).catch(function(){{return null;}}),
    fetch(base+'/income-statement/'+ticker+'?period=quarter&limit=8&apikey='+API_KEY).then(function(r){{return r.json();}}).catch(function(){{return null;}})
  ]).then(function(res) {{
    var prof = res[0] && res[0][0] ? res[0][0] : null;
    var annual = res[1] || [];
    var qtr = res[2] || [];
    if (!prof) {{
      document.getElementById('dynamicArea').innerHTML = '<div class="loading"><div style="color:#ff6b6b;">데이터를 불러올 수 없습니다. 티커 또는 API Key를 확인해주세요.</div></div>';
      return;
    }}
    annual.reverse(); qtr.reverse();
    renderDynamic(prof, annual, qtr);
  }}).catch(function(err) {{
    document.getElementById('dynamicArea').innerHTML = '<div class="loading"><div style="color:#ff6b6b;">오류: '+err.message+'</div></div>';
  }});
}}

function fmtN(n) {{
  if (n==null||isNaN(n)) return '-';
  var a=Math.abs(n); if(a>=1e12) return '$'+(n/1e12).toFixed(2)+'T'; if(a>=1e9) return '$'+(n/1e9).toFixed(1)+'B'; if(a>=1e6) return '$'+(n/1e6).toFixed(0)+'M'; return '$'+n.toLocaleString();
}}
function pctN(n) {{ return n==null?'-':(n*100).toFixed(1)+'%'; }}

function makeSvgBar(labels, datasets) {{
  var W=580,H=260,pl=55,pr=15,pt=15,pb=45,cW=W-pl-pr,cH=H-pt-pb;
  var allV=[]; datasets.forEach(function(ds){{ds.data.forEach(function(v){{allV.push(v);}});}});
  var mx=Math.max.apply(null,allV)*1.15||1; var n=labels.length,gc=datasets.length,gw=cW/n,bw=(gw*0.65)/gc;
  var s='<svg viewBox="0 0 '+W+' '+H+'" xmlns="http://www.w3.org/2000/svg">';
  for(var i=0;i<=4;i++){{var y=pt+cH-(cH*i/4);var v=mx*i/4;s+='<line x1="'+pl+'" y1="'+y+'" x2="'+(W-pr)+'" y2="'+y+'" stroke="#2d3148"/>';s+='<text x="'+(pl-6)+'" y="'+(y+4)+'" fill="#9ca0b8" font-size="10" text-anchor="end">$'+(v/1e9).toFixed(0)+'B</text>';}}
  datasets.forEach(function(ds,di){{ds.data.forEach(function(v,vi){{var x=pl+vi*gw+gw*0.175+di*bw;var bh=(v/mx)*cH;var y=pt+cH-bh;s+='<rect x="'+x.toFixed(1)+'" y="'+y.toFixed(1)+'" width="'+bw.toFixed(1)+'" height="'+bh.toFixed(1)+'" rx="3" fill="'+ds.color+'" opacity="0.8"/>';}});}});
  labels.forEach(function(l,i){{var x=pl+i*gw+gw/2;s+='<text x="'+x.toFixed(1)+'" y="'+(H-pb+18)+'" fill="#9ca0b8" font-size="10" text-anchor="middle">'+l+'</text>';}});
  var lx=pl; datasets.forEach(function(ds){{s+='<rect x="'+lx+'" y="'+(H-10)+'" width="8" height="8" rx="2" fill="'+ds.color+'"/><text x="'+(lx+12)+'" y="'+(H-3)+'" fill="#9ca0b8" font-size="9">'+ds.label+'</text>';lx+=ds.label.length*7+22;}});
  return s+'</svg>';
}}

function makeSvgLine(labels, datasets) {{
  var W=580,H=260,pl=45,pr=15,pt=15,pb=45,cW=W-pl-pr,cH=H-pt-pb;
  var allV=[]; datasets.forEach(function(ds){{ds.data.forEach(function(v){{allV.push(v);}});}});
  var mx=Math.max.apply(null,allV)*1.1||100,mn=Math.min.apply(null,allV)*0.85;if(mn<0)mn=0;var rng=mx-mn||1;var n=labels.length;
  var s='<svg viewBox="0 0 '+W+' '+H+'" xmlns="http://www.w3.org/2000/svg">';
  for(var i=0;i<=4;i++){{var y=pt+cH-(cH*i/4);var v=mn+rng*i/4;s+='<line x1="'+pl+'" y1="'+y+'" x2="'+(W-pr)+'" y2="'+y+'" stroke="#2d3148"/>';s+='<text x="'+(pl-5)+'" y="'+(y+4)+'" fill="#9ca0b8" font-size="10" text-anchor="end">'+v.toFixed(0)+'%</text>';}}
  datasets.forEach(function(ds){{var pts=[];ds.data.forEach(function(v,vi){{var x=pl+(vi/Math.max(n-1,1))*cW;var y=pt+cH-((v-mn)/rng)*cH;pts.push(x.toFixed(1)+','+y.toFixed(1));}});s+='<polyline points="'+pts.join(' ')+'" fill="none" stroke="'+ds.color+'" stroke-width="2.5"/>';ds.data.forEach(function(v,vi){{var x=pl+(vi/Math.max(n-1,1))*cW;var y=pt+cH-((v-mn)/rng)*cH;s+='<circle cx="'+x.toFixed(1)+'" cy="'+y.toFixed(1)+'" r="4" fill="'+ds.color+'"/>';s+='<text x="'+x.toFixed(1)+'" y="'+(y-7)+'" fill="'+ds.color+'" font-size="8" text-anchor="middle" font-weight="600">'+v.toFixed(1)+'%</text>';}});}});
  labels.forEach(function(l,i){{var x=pl+(i/Math.max(n-1,1))*cW;s+='<text x="'+x.toFixed(1)+'" y="'+(H-pb+18)+'" fill="#9ca0b8" font-size="10" text-anchor="middle">'+l+'</text>';}});
  var lx=pl;datasets.forEach(function(ds){{s+='<rect x="'+lx+'" y="'+(H-10)+'" width="8" height="8" rx="2" fill="'+ds.color+'"/><text x="'+(lx+12)+'" y="'+(H-3)+'" fill="#9ca0b8" font-size="9">'+ds.label+'</text>';lx+=ds.label.length*6+20;}});
  return s+'</svg>';
}}

function renderDynamic(prof, annual, qtr) {{
  var latest=annual[annual.length-1]||{{}};var prev=annual[annual.length-2]||{{}};
  var revG=prev.revenue?((latest.revenue-prev.revenue)/prev.revenue*100):0;
  var niG=prev.netIncome?((latest.netIncome-prev.netIncome)/prev.netIncome*100):0;
  var chgCls=prof.changes>=0?'up':'down'; var chgSign=prof.changes>=0?'+':'';

  var h='';
  // Header
  h+='<div class="tc active" id="t-overview">';
  h+='<div class="ch"><div><div class="ch-tk">'+prof.symbol+'</div><div class="ch-nm">'+(prof.companyName||'')+'</div><div class="ch-desc">'+(prof.description||'').substring(0,200)+'</div><div style="margin-top:8px;font-size:12px;color:var(--text2);">'+(prof.exchangeShortName||'')+' | '+(prof.sector||'')+' | '+(prof.industry||'')+' | '+(prof.country||'')+'</div></div><div class="ch-meta"><div class="ch-price">$'+(prof.price?prof.price.toFixed(2):'-')+'</div><div class="ch-chg '+chgCls+'">'+chgSign+(prof.changes?prof.changes.toFixed(2):'0')+' ('+chgSign+(prof.changesPercentage?prof.changesPercentage.toFixed(2):'0')+'%)</div><div style="font-size:12px;color:var(--text2);margin-top:8px;">52주: '+(prof.range||'-')+'</div></div></div>';
  // KPIs
  h+='<div class="kpi-row">';
  h+='<div class="kpi"><div class="kpi-l">시가총액</div><div class="kpi-v">'+fmtN(prof.mktCap)+'</div><div class="kpi-s">Beta: '+(prof.beta||'-')+'</div></div>';
  h+='<div class="kpi"><div class="kpi-l">연간 매출</div><div class="kpi-v">'+fmtN(latest.revenue)+'</div><div class="kpi-s '+(revG>=0?'up':'down')+'">'+(revG>=0?'+':'')+revG.toFixed(1)+'% YoY</div></div>';
  h+='<div class="kpi"><div class="kpi-l">연간 순이익</div><div class="kpi-v">'+fmtN(latest.netIncome)+'</div><div class="kpi-s '+(niG>=0?'up':'down')+'">'+(niG>=0?'+':'')+niG.toFixed(1)+'% YoY</div></div>';
  h+='<div class="kpi"><div class="kpi-l">EPS</div><div class="kpi-v">$'+(latest.eps?latest.eps.toFixed(2):'-')+'</div><div class="kpi-s">순이익률 '+pctN(latest.netIncomeRatio)+'</div></div>';
  h+='<div class="kpi"><div class="kpi-l">P/E (TTM)</div><div class="kpi-v">'+(prof.pe?prof.pe.toFixed(1):'-')+'</div></div>';
  h+='<div class="kpi"><div class="kpi-l">매출총이익률</div><div class="kpi-v">'+pctN(latest.grossProfitRatio)+'</div><div class="kpi-s">영업이익률 '+pctN(latest.operatingIncomeRatio)+'</div></div>';
  h+='</div>';
  // Charts
  var labels=annual.map(function(a){{return 'FY'+(a.calendarYear||a.date.substring(0,4));}});
  h+='<div class="cg">';
  h+='<div class="cc"><div class="ct">매출 &amp; 순이익 추이 <span class="badge">연간</span></div>'+makeSvgBar(labels,[{{label:"매출",color:"#76b900",data:annual.map(function(a){{return a.revenue||0;}})}},{{label:"순이익",color:"#4ecdc4",data:annual.map(function(a){{return a.netIncome||0;}})}}])+'</div>';
  h+='<div class="cc"><div class="ct">수익성 지표 추이 <span class="badge">마진율</span></div>'+makeSvgLine(labels,[{{label:"매출총이익률",color:"#76b900",data:annual.map(function(a){{return (a.grossProfitRatio||0)*100;}})}},{{label:"영업이익률",color:"#4dabf7",data:annual.map(function(a){{return (a.operatingIncomeRatio||0)*100;}})}},{{label:"순이익률",color:"#b197fc",data:annual.map(function(a){{return (a.netIncomeRatio||0)*100;}})}}])+'</div>';
  h+='</div>';
  // Quarterly
  if(qtr.length>0){{
    var ql=qtr.map(function(q){{return (q.period||'')+' '+(q.calendarYear||'');}});
    h+='<div class="cc" style="margin-bottom:24px"><div class="ct">분기별 매출 추이 <span class="badge">최근 8분기</span></div>'+makeSvgBar(ql,[{{label:"분기 매출",color:"#76b900",data:qtr.map(function(q){{return q.revenue||0;}})}},{{label:"분기 순이익",color:"#4ecdc4",data:qtr.map(function(q){{return q.netIncome||0;}})}}])+'</div>';
  }}
  // Table
  h+='<div class="cc"><div class="ct">연간 재무 데이터 <span class="badge">상세</span></div><div class="tw"><table><thead><tr><th>지표</th>';
  labels.forEach(function(l){{h+='<th class="nr">'+l+'</th>';}});
  h+='</tr></thead><tbody>';
  var metrics=[["매출",function(a){{return fmtN(a.revenue);}}],["매출총이익",function(a){{return fmtN(a.grossProfit);}}],["영업이익",function(a){{return fmtN(a.operatingIncome);}}],["순이익",function(a){{return fmtN(a.netIncome);}}],["EPS",function(a){{return '$'+(a.eps?a.eps.toFixed(2):'-');}}],["매출총이익률",function(a){{return pctN(a.grossProfitRatio);}}],["영업이익률",function(a){{return pctN(a.operatingIncomeRatio);}}],["순이익률",function(a){{return pctN(a.netIncomeRatio);}}]];
  metrics.forEach(function(m){{h+='<tr><td>'+m[0]+'</td>';annual.forEach(function(a){{h+='<td class="nr">'+m[1](a)+'</td>';}});h+='</tr>';}});
  h+='</tbody></table></div></div>';
  h+='</div>';

  // Other tabs placeholder
  h+='<div class="tc" id="t-segments"><div class="loading" style="padding:40px;"><div style="color:var(--text2);">사업부문 데이터는 FMP API 무료 티어에서 제공되지 않습니다.</div></div></div>';
  h+='<div class="tc" id="t-valuation"><div class="kpi-row"><div class="kpi"><div class="kpi-l">P/E (TTM)</div><div class="kpi-v">'+(prof.pe?prof.pe.toFixed(1):'-')+'</div></div><div class="kpi"><div class="kpi-l">P/S</div><div class="kpi-v">'+(prof.priceToSalesRatio?prof.priceToSalesRatio.toFixed(1):'-')+'</div></div><div class="kpi"><div class="kpi-l">Beta</div><div class="kpi-v">'+(prof.beta?prof.beta.toFixed(2):'-')+'</div></div><div class="kpi"><div class="kpi-l">배당수익률</div><div class="kpi-v">'+(prof.lastDiv&&prof.price?((prof.lastDiv/prof.price)*100).toFixed(2)+'%':'0%')+'</div></div></div></div>';
  h+='<div class="tc" id="t-invest"><div class="ig"><div class="invest-card"><h4><span class="dot dot-green"></span> 기업 개요</h4><ul><li>'+(prof.description||'설명 없음')+'</li><li>임직원: '+(prof.fullTimeEmployees||'-')+'명</li><li>IPO: '+(prof.ipoDate||'-')+'</li></ul></div><div class="invest-card"><h4><span class="dot dot-blue"></span> 참고</h4><ul><li>상세 투자 포인트는 NVDA처럼 사전 분석이 준비된 티커에서 확인 가능합니다.</li><li>기본 재무 데이터는 개요 & 재무 탭에서 확인하세요.</li></ul></div></div></div>';

  document.getElementById('dynamicArea').innerHTML = h;
  st('overview');
}}
</script>
</body>
</html>'''

output = "/sessions/exciting-gracious-pasteur/mnt/자산 대시보드 제작/02-projects/2026.03.28 기업분석대시보드/output/기업분석_종합대시보드_v4_2026.03.28.html"
with open(output, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Generated: {output}")
print(f"Size: {len(html):,} bytes")
