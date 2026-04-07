#!/usr/bin/env python3
"""v6: Multi-ticker static HTML dashboard - ALL data pre-rendered, no external fetch needed."""
import math, html as html_mod

# ══════════════════════════════════════════════════════════════════════════════
# MULTI-TICKER DATA
# ══════════════════════════════════════════════════════════════════════════════

TICKERS = {
"NVDA": {
  "profile": {"symbol":"NVDA","name":"NVIDIA Corporation","price":167.52,"changes":-2.31,"changesPct":-1.36,"exchange":"NASDAQ","sector":"Technology","industry":"Semiconductors","country":"US","mktCap":"$4.07T","beta":2.37,"range":"86.62 - 212.19","employees":"36,000","desc":"NVIDIA는 GPU(그래픽 처리 장치) 및 AI 컴퓨팅 플랫폼의 글로벌 리더입니다. 데이터센터, 게이밍, 자동차, 전문 시각화 등 다양한 시장에서 AI 가속 컴퓨팅 솔루션을 제공합니다."},
  "income": [
    {"year":"2022","rev":26.91,"ni":9.75,"oi":10.04,"gp":17.48,"eps":0.39,"gm":64.93,"om":37.31,"nm":36.23},
    {"year":"2023","rev":26.97,"ni":4.37,"oi":4.22,"gp":15.36,"eps":0.17,"gm":56.93,"om":15.66,"nm":16.19},
    {"year":"2024","rev":60.92,"ni":29.76,"oi":32.97,"gp":44.30,"eps":1.19,"gm":72.72,"om":54.12,"nm":48.85},
    {"year":"2025","rev":130.50,"ni":72.88,"oi":81.45,"gp":97.87,"eps":2.94,"gm":74.99,"om":62.42,"nm":55.85},
    {"year":"2026","rev":215.94,"ni":120.07,"oi":130.39,"gp":153.44,"eps":4.90,"gm":71.07,"om":60.38,"nm":55.60},
  ],
  "quarterly": [
    {"q":"Q1'25","rev":26.04,"ni":14.88},{"q":"Q2'25","rev":30.04,"ni":16.60},
    {"q":"Q3'25","rev":35.08,"ni":19.31},{"q":"Q4'25","rev":39.33,"ni":22.09},
    {"q":"Q1'26","rev":41.79,"ni":19.31},{"q":"Q2'26","rev":49.92,"ni":24.50},
    {"q":"Q3'26","rev":56.10,"ni":33.30},{"q":"Q4'26","rev":68.13,"ni":42.96},
  ],
  "segments": {
    "labels":["FY2022","FY2023","FY2024","FY2025","FY2026"],
    "series":[
      {"name":"Data Center","color":"#76b900","data":[10.6,15.0,47.5,115.2,193.7]},
      {"name":"Gaming","color":"#4ecdc4","data":[12.5,9.1,10.4,11.4,16.0]},
      {"name":"Pro Vis","color":"#4dabf7","data":[2.1,1.5,1.6,1.9,3.2]},
      {"name":"Automotive","color":"#b197fc","data":[0.6,0.9,1.1,1.7,2.4]},
    ]
  },
  "peers": [
    {"sym":"NVDA","name":"NVIDIA","mc":"$4.07T","pe":"34.2","ps":"18.8","rev":"$215.9B","nm":"55.6%","hl":True},
    {"sym":"AMD","name":"AMD","mc":"$210B","pe":"24.8","ps":"7.1","rev":"$28.1B","nm":"22%","hl":False},
    {"sym":"INTC","name":"Intel","mc":"$97B","pe":"-","ps":"1.5","rev":"$53.1B","nm":"-1%","hl":False},
    {"sym":"AVGO","name":"Broadcom","mc":"$1.05T","pe":"38.2","ps":"16.2","rev":"$62.0B","nm":"37%","hl":False},
    {"sym":"QCOM","name":"Qualcomm","mc":"$190B","pe":"16.5","ps":"4.3","rev":"$42.2B","nm":"27%","hl":False},
    {"sym":"TSM","name":"TSMC","mc":"$870B","pe":"22.1","ps":"11.3","rev":"$95.0B","nm":"40%","hl":False},
  ],
  "ratios": {"pe":34.18,"fpe":20.19,"ps":18.84,"peg":0.53,"roe":"127.5%","div":"0.02%"},
  "invest": {
    "strengths":["AI 인프라 시장 절대 지배력: 데이터센터 GPU 시장 점유율 90%+ 유지","CUDA 생태계 락인: 소프트웨어 플랫폼으로 강력한 진입장벽 형성","FY2026 매출 $215.9B, 전년 대비 65% 성장의 초고성장 지속","순이익률 55.6%로 반도체 업계 최고 수준의 수익성"],
    "risks":["미중 반도체 수출 규제 강화에 따른 중국향 매출 감소 리스크","AMD MI300X, Intel Gaudi3, 자체 ASIC(Google TPU, AWS Trainium) 등 경쟁 심화","AI 인프라 투자 사이클 둔화 가능성 (Capex 피크 논쟁)","고밸류에이션 부담: Trailing P/E 34x, 기대치 미달 시 급락 가능"],
    "opportunities":["Sovereign AI: 각국 정부의 자체 AI 인프라 구축 수요 급증","Blackwell Ultra / Rubin 차세대 아키텍처로 성능 리더십 유지","AI 추론(Inference) 시장 본격 성장 — 학습 대비 훨씬 큰 시장","자율주행 / 로보틱스: DRIVE Thor, Isaac 플랫폼으로 새 성장동력"],
    "watchlist":["FY2027 Q1 가이던스 $45B (시장 기대 상회 여부)","Blackwell Ultra 양산 일정 및 수율 (H2 2026)","중국 수출 규제 완화/강화 방향성","AI Capex 투자 추이: MSFT, GOOG, META, AMZN의 분기별 설비투자"]
  },
  "accent":"#76b900"
},

"AAPL": {
  "profile": {"symbol":"AAPL","name":"Apple Inc.","price":217.90,"changes":1.23,"changesPct":0.57,"exchange":"NASDAQ","sector":"Technology","industry":"Consumer Electronics","country":"US","mktCap":"$3.32T","beta":1.24,"range":"164.08 - 260.10","employees":"164,000","desc":"Apple은 iPhone, iPad, Mac, Apple Watch, AirPods 등 하드웨어와 iOS, macOS 생태계 기반의 서비스(App Store, Apple Music, iCloud, Apple TV+) 사업을 운영하는 글로벌 테크 기업입니다."},
  "income": [
    {"year":"2021","rev":365.82,"ni":94.68,"oi":108.95,"gp":152.84,"eps":6.15,"gm":41.78,"om":29.78,"nm":25.88},
    {"year":"2022","rev":394.33,"ni":99.80,"oi":119.44,"gp":170.78,"eps":6.51,"gm":43.31,"om":30.29,"nm":25.31},
    {"year":"2023","rev":383.29,"ni":97.00,"oi":114.30,"gp":169.15,"eps":6.33,"gm":44.13,"om":29.82,"nm":25.31},
    {"year":"2024","rev":391.04,"ni":101.96,"oi":118.66,"gp":178.84,"eps":6.75,"gm":45.74,"om":30.35,"nm":26.07},
    {"year":"2025","rev":420.00,"ni":110.00,"oi":128.00,"gp":192.00,"eps":7.35,"gm":45.71,"om":30.48,"nm":26.19},
  ],
  "quarterly": [
    {"q":"Q1'24","rev":117.15,"ni":33.92},{"q":"Q2'24","rev":90.75,"ni":23.64},
    {"q":"Q3'24","rev":85.78,"ni":21.45},{"q":"Q4'24","rev":94.93,"ni":14.74},
    {"q":"Q1'25","rev":124.30,"ni":36.33},{"q":"Q2'25","rev":95.36,"ni":24.78},
    {"q":"Q3'25","rev":97.10,"ni":25.00},{"q":"Q4'25","rev":103.24,"ni":23.89},
  ],
  "segments": {
    "labels":["FY2021","FY2022","FY2023","FY2024","FY2025"],
    "series":[
      {"name":"iPhone","color":"#007AFF","data":[191.97,205.49,200.58,201.18,215.00]},
      {"name":"Services","color":"#34C759","data":[68.43,78.13,85.20,96.17,105.00]},
      {"name":"Mac","color":"#FF9500","data":[35.19,40.18,29.36,29.98,32.00]},
      {"name":"iPad","color":"#AF52DE","data":[31.86,29.29,28.30,26.69,28.00]},
      {"name":"Wearables","color":"#FF2D55","data":[38.37,41.24,39.85,37.02,40.00]},
    ]
  },
  "peers": [
    {"sym":"AAPL","name":"Apple","mc":"$3.32T","pe":"29.6","ps":"7.9","rev":"$420B","nm":"26.2%","hl":True},
    {"sym":"MSFT","name":"Microsoft","mc":"$3.04T","pe":"34.1","ps":"12.8","rev":"$262B","nm":"36.4%","hl":False},
    {"sym":"GOOG","name":"Alphabet","mc":"$2.08T","pe":"21.8","ps":"5.8","rev":"$386B","nm":"27.5%","hl":False},
    {"sym":"AMZN","name":"Amazon","mc":"$2.15T","pe":"35.2","ps":"3.3","rev":"$650B","nm":"9.4%","hl":False},
    {"sym":"META","name":"Meta","mc":"$1.56T","pe":"23.5","ps":"8.8","rev":"$178B","nm":"37.4%","hl":False},
    {"sym":"SSNLF","name":"Samsung","mc":"$292B","pe":"13.5","ps":"1.3","rev":"$220B","nm":"9.5%","hl":False},
  ],
  "ratios": {"pe":29.63,"fpe":26.80,"ps":7.90,"peg":2.85,"roe":"157.4%","div":"0.44%"},
  "invest": {
    "strengths":["iPhone 중심 하드웨어 생태계의 강력한 락인 효과 — 전환비용 높음","서비스 매출 $105B+ 돌파, 고마진(70%+) 사업부 비중 지속 확대","세계 최고 수준의 브랜드 가치와 고객 충성도","$150B+ 규모의 자사주 매입 프로그램으로 주주 환원 적극적"],
    "risks":["iPhone 매출 비중 50%+ — 스마트폰 시장 성숙화에 따른 성장 둔화 우려","중국 시장 리스크: 현지 브랜드(Huawei 등)와의 경쟁 심화","AI 기능 통합 지연 시 경쟁사 대비 기술 리더십 약화 가능","규제 리스크: EU DMA, 미국 App Store 독점 소송 등"],
    "opportunities":["Apple Intelligence (On-device AI) — 업그레이드 사이클 촉진 기대","India 시장 확대: 제조기지 이전 + 빠른 성장 시장 침투","Vision Pro / 공간 컴퓨팅으로 새로운 플랫폼 개척","금융서비스(Apple Card, Savings) 및 헬스케어 분야 진출"],
    "watchlist":["FY2026 iPhone 16 Super Cycle 실현 여부","서비스 매출 성장률 유지 (목표: YoY 15%+)","중국 시장 점유율 변동 추이","Apple Intelligence 채택률 및 사용자 반응"]
  },
  "accent":"#007AFF"
},

"MSFT": {
  "profile": {"symbol":"MSFT","name":"Microsoft Corporation","price":388.50,"changes":-3.15,"changesPct":-0.80,"exchange":"NASDAQ","sector":"Technology","industry":"Software—Infrastructure","country":"US","mktCap":"$3.04T","beta":0.89,"range":"340.00 - 468.35","employees":"228,000","desc":"Microsoft는 Windows, Office 365, Azure 클라우드, LinkedIn, Xbox 게이밍 등을 운영하는 글로벌 소프트웨어 및 클라우드 기업입니다. OpenAI 파트너십을 통해 AI 분야에서 선도적 위치를 확보하고 있습니다."},
  "income": [
    {"year":"2021","rev":168.09,"ni":61.27,"oi":69.92,"gp":115.86,"eps":8.12,"gm":68.93,"om":41.59,"nm":36.45},
    {"year":"2022","rev":198.27,"ni":72.74,"oi":83.38,"gp":135.62,"eps":9.65,"gm":68.40,"om":42.06,"nm":36.69},
    {"year":"2023","rev":211.92,"ni":72.36,"oi":88.52,"gp":146.05,"eps":9.68,"gm":68.92,"om":41.77,"nm":34.15},
    {"year":"2024","rev":245.12,"ni":88.14,"oi":109.43,"gp":171.01,"eps":11.86,"gm":69.76,"om":44.64,"nm":35.96},
    {"year":"2025","rev":262.00,"ni":95.30,"oi":118.00,"gp":185.00,"eps":12.80,"gm":70.61,"om":45.04,"nm":36.37},
  ],
  "quarterly": [
    {"q":"Q1'24","rev":56.52,"ni":22.29},{"q":"Q2'24","rev":62.02,"ni":21.87},
    {"q":"Q3'24","rev":61.86,"ni":21.94},{"q":"Q4'24","rev":64.73,"ni":22.04},
    {"q":"Q1'25","rev":65.59,"ni":24.67},{"q":"Q2'25","rev":69.63,"ni":24.11},
    {"q":"Q3'25","rev":64.00,"ni":23.50},{"q":"Q4'25","rev":62.78,"ni":23.02},
  ],
  "segments": {
    "labels":["FY2021","FY2022","FY2023","FY2024","FY2025"],
    "series":[
      {"name":"Intelligent Cloud","color":"#0078D4","data":[60.08,75.25,87.91,105.36,117.00]},
      {"name":"Productivity & Business","color":"#50E6FF","data":[53.92,63.36,69.27,77.39,83.00]},
      {"name":"More Personal Computing","color":"#D83B01","data":[54.09,59.65,54.73,62.37,62.00]},
    ]
  },
  "peers": [
    {"sym":"MSFT","name":"Microsoft","mc":"$3.04T","pe":"34.1","ps":"12.8","rev":"$262B","nm":"36.4%","hl":True},
    {"sym":"GOOG","name":"Alphabet","mc":"$2.08T","pe":"21.8","ps":"5.8","rev":"$386B","nm":"27.5%","hl":False},
    {"sym":"AMZN","name":"Amazon","mc":"$2.15T","pe":"35.2","ps":"3.3","rev":"$650B","nm":"9.4%","hl":False},
    {"sym":"CRM","name":"Salesforce","mc":"$275B","pe":"44.5","ps":"7.5","rev":"$38B","nm":"15%","hl":False},
    {"sym":"ORCL","name":"Oracle","mc":"$385B","pe":"35.8","ps":"6.8","rev":"$57B","nm":"22%","hl":False},
    {"sym":"SAP","name":"SAP","mc":"$310B","pe":"42.0","ps":"8.5","rev":"$36B","nm":"18%","hl":False},
  ],
  "ratios": {"pe":34.10,"fpe":28.50,"ps":12.80,"peg":2.10,"roe":"38.5%","div":"0.72%"},
  "invest": {
    "strengths":["Azure 클라우드 YoY 30%+ 성장 지속, AWS와 시장 2위 경쟁","OpenAI 파트너십으로 Copilot AI 제품 전 라인업 통합","Office 365 + LinkedIn SaaS 구독 모델의 안정적 매출 기반","기업용 AI 시장에서의 선도적 포지션 (Copilot for M365, GitHub Copilot)"],
    "risks":["Azure 성장률 둔화 시 프리미엄 밸류에이션 정당화 어려움","AI 인프라 투자(CapEx) 급증에 따른 마진 압박 가능성","Activision 인수 후 게이밍 부문 통합 리스크","반독점 규제 및 EU 디지털 시장법(DMA) 영향"],
    "opportunities":["Copilot 유료 전환: 기업 AI 도구 월 $30/user로 매출 급증 기대","Azure AI 서비스 확대로 클라우드 시장 점유율 확대","게이밍 구독(Game Pass) + 클라우드 게이밍 성장","산업별 특화 AI 솔루션 (헬스케어, 금융, 제조)"],
    "watchlist":["Azure 분기별 성장률 (30%+ 유지 여부)","Copilot 유료 고객 수 및 ARPU 추이","AI CapEx 투자 대비 수익화 속도","Windows AI PC 사이클 시작 여부"]
  },
  "accent":"#0078D4"
},

"GOOGL": {
  "profile": {"symbol":"GOOGL","name":"Alphabet Inc.","price":167.40,"changes":0.85,"changesPct":0.51,"exchange":"NASDAQ","sector":"Technology","industry":"Internet Content & Information","country":"US","mktCap":"$2.08T","beta":1.06,"range":"140.53 - 208.70","employees":"182,500","desc":"Alphabet은 Google 검색, YouTube, Android, Google Cloud Platform(GCP), Waymo 자율주행 등을 운영하는 글로벌 테크 기업입니다. 전 세계 디지털 광고 시장의 핵심 플레이어입니다."},
  "income": [
    {"year":"2021","rev":257.64,"ni":76.03,"oi":78.71,"gp":146.70,"eps":5.61,"gm":56.94,"om":30.55,"nm":29.51},
    {"year":"2022","rev":282.84,"ni":59.97,"oi":74.84,"gp":156.63,"eps":4.56,"gm":55.38,"om":26.46,"nm":21.20},
    {"year":"2023","rev":307.39,"ni":73.80,"oi":84.29,"gp":174.06,"eps":5.80,"gm":56.61,"om":27.43,"nm":24.01},
    {"year":"2024","rev":350.02,"ni":100.68,"oi":112.39,"gp":202.29,"eps":8.04,"gm":57.79,"om":32.11,"nm":28.76},
    {"year":"2025","rev":386.00,"ni":106.10,"oi":125.00,"gp":224.00,"eps":8.70,"gm":58.03,"om":32.38,"nm":27.49},
  ],
  "quarterly": [
    {"q":"Q1'24","rev":80.54,"ni":23.66},{"q":"Q2'24","rev":84.74,"ni":23.62},
    {"q":"Q3'24","rev":88.27,"ni":26.30},{"q":"Q4'24","rev":96.47,"ni":26.54},
    {"q":"Q1'25","rev":90.23,"ni":34.54},{"q":"Q2'25","rev":94.00,"ni":25.50},
    {"q":"Q3'25","rev":98.00,"ni":23.06},{"q":"Q4'25","rev":103.77,"ni":23.00},
  ],
  "segments": {
    "labels":["FY2021","FY2022","FY2023","FY2024","FY2025"],
    "series":[
      {"name":"Google Search","color":"#4285F4","data":[148.95,162.45,175.03,198.12,218.00]},
      {"name":"YouTube Ads","color":"#FF0000","data":[28.84,29.24,31.51,36.15,40.00]},
      {"name":"Google Cloud","color":"#34A853","data":[19.21,26.28,33.09,43.23,52.00]},
      {"name":"Other","color":"#FBBC05","data":[60.64,64.87,67.76,72.52,76.00]},
    ]
  },
  "peers": [
    {"sym":"GOOGL","name":"Alphabet","mc":"$2.08T","pe":"21.8","ps":"5.8","rev":"$386B","nm":"27.5%","hl":True},
    {"sym":"META","name":"Meta","mc":"$1.56T","pe":"23.5","ps":"8.8","rev":"$178B","nm":"37.4%","hl":False},
    {"sym":"MSFT","name":"Microsoft","mc":"$3.04T","pe":"34.1","ps":"12.8","rev":"$262B","nm":"36.4%","hl":False},
    {"sym":"AMZN","name":"Amazon","mc":"$2.15T","pe":"35.2","ps":"3.3","rev":"$650B","nm":"9.4%","hl":False},
    {"sym":"SNAP","name":"Snap","mc":"$19B","pe":"-","ps":"3.4","rev":"$5.4B","nm":"-5%","hl":False},
    {"sym":"TTD","name":"Trade Desk","mc":"$35B","pe":"65.0","ps":"14.5","rev":"$2.4B","nm":"21%","hl":False},
  ],
  "ratios": {"pe":21.80,"fpe":19.50,"ps":5.80,"peg":0.95,"roe":"32.8%","div":"0.48%"},
  "invest": {
    "strengths":["검색 광고 시장 90%+ 독점적 점유율 유지","Google Cloud YoY 25%+ 성장, 흑자 전환 완료","YouTube 광고+구독 합산 $40B+ 규모의 거대 플랫폼","업계 최저 수준의 P/E 21.8x로 밸류에이션 매력적"],
    "risks":["AI 검색(Perplexity, ChatGPT 등)이 기존 검색 광고 모델 위협","반독점 소송: 미국 DOJ의 검색 독점 판결 및 잠재적 기업 분할","AI 인프라 CapEx 급증 ($50B+ 연간)으로 FCF 압박","광고 시장 경기 민감도 — 경기 침체 시 광고 지출 축소"],
    "opportunities":["Gemini AI 모델 통합으로 검색 / 클라우드 / Android 전 플랫폼 강화","Google Cloud의 AI 서비스 수요 폭발적 성장","Waymo 자율주행 상용화 확대 (10만+ 유료 탑승/주)","YouTube Shorts 수익화 및 TV 광고 시장 침투"],
    "watchlist":["Google Cloud 분기별 매출 성장률 및 영업이익률","AI 검색(AI Overviews) 광고 수익화 전환율","반독점 판결 후속 조치 (구조적 분리 가능성)","Waymo 확장 도시 수 및 탑승 횟수 추이"]
  },
  "accent":"#4285F4"
},

"AMZN": {
  "profile": {"symbol":"AMZN","name":"Amazon.com, Inc.","price":197.50,"changes":-1.44,"changesPct":-0.72,"exchange":"NASDAQ","sector":"Technology","industry":"Internet Retail","country":"US","mktCap":"$2.15T","beta":1.15,"range":"151.61 - 242.52","employees":"1,551,000","desc":"Amazon은 세계 최대 전자상거래 플랫폼, 클라우드(AWS), 디지털 광고, 프라임 비디오 스트리밍, Alexa/디바이스 등을 운영하는 글로벌 테크 기업입니다."},
  "income": [
    {"year":"2021","rev":469.82,"ni":33.36,"oi":24.88,"gp":197.48,"eps":3.24,"gm":42.03,"om":5.30,"nm":7.10},
    {"year":"2022","rev":513.98,"ni":-2.72,"oi":12.25,"gp":225.15,"eps":-0.27,"gm":43.81,"om":2.38,"nm":-0.53},
    {"year":"2023","rev":574.79,"ni":30.43,"oi":36.85,"gp":254.62,"eps":2.90,"gm":44.30,"om":6.41,"nm":5.29},
    {"year":"2024","rev":620.13,"ni":59.25,"oi":68.59,"gp":279.61,"eps":5.53,"gm":45.09,"om":11.06,"nm":9.55},
    {"year":"2025","rev":650.00,"ni":61.10,"oi":72.00,"gp":296.00,"eps":5.74,"gm":45.54,"om":11.08,"nm":9.40},
  ],
  "quarterly": [
    {"q":"Q1'24","rev":143.31,"ni":10.43},{"q":"Q2'24","rev":148.00,"ni":13.49},
    {"q":"Q3'24","rev":158.88,"ni":15.33},{"q":"Q4'24","rev":187.79,"ni":20.00},
    {"q":"Q1'25","rev":155.67,"ni":17.14},{"q":"Q2'25","rev":159.00,"ni":14.50},
    {"q":"Q3'25","rev":163.00,"ni":15.00},{"q":"Q4'25","rev":172.33,"ni":14.46},
  ],
  "segments": {
    "labels":["FY2021","FY2022","FY2023","FY2024","FY2025"],
    "series":[
      {"name":"Online Stores","color":"#FF9900","data":[222.08,220.00,231.87,247.00,258.00]},
      {"name":"AWS","color":"#232F3E","data":[62.20,80.10,90.76,107.56,120.00]},
      {"name":"Advertising","color":"#146EB4","data":[31.16,37.74,46.91,56.21,62.00]},
      {"name":"Other","color":"#48A9A6","data":[154.38,176.14,205.25,209.36,210.00]},
    ]
  },
  "peers": [
    {"sym":"AMZN","name":"Amazon","mc":"$2.15T","pe":"35.2","ps":"3.3","rev":"$650B","nm":"9.4%","hl":True},
    {"sym":"MSFT","name":"Microsoft","mc":"$3.04T","pe":"34.1","ps":"12.8","rev":"$262B","nm":"36.4%","hl":False},
    {"sym":"GOOG","name":"Alphabet","mc":"$2.08T","pe":"21.8","ps":"5.8","rev":"$386B","nm":"27.5%","hl":False},
    {"sym":"WMT","name":"Walmart","mc":"$680B","pe":"34.0","ps":"1.0","rev":"$648B","nm":"3.0%","hl":False},
    {"sym":"BABA","name":"Alibaba","mc":"$290B","pe":"17.2","ps":"2.0","rev":"$135B","nm":"12%","hl":False},
    {"sym":"SHOP","name":"Shopify","mc":"$130B","pe":"72.0","ps":"15.0","rev":"$8.9B","nm":"16%","hl":False},
  ],
  "ratios": {"pe":35.20,"fpe":28.50,"ps":3.30,"peg":1.25,"roe":"22.1%","div":"0%"},
  "invest": {
    "strengths":["AWS 클라우드 시장 점유율 31%로 압도적 1위","Prime 회원 2억명+, 강력한 고객 락인 효과","광고 사업 $62B+ — 고마진 3rd Party 광고 플랫폼으로 급성장","물류 네트워크의 규모의 경제 → 배송 속도 및 비용 경쟁력"],
    "risks":["소매 부문 마진 여전히 낮음 — 물류/인건비 부담 지속","AWS 경쟁 심화: Azure, GCP의 AI 워크로드 공략","FTC 반독점 소송 및 노동 규제 리스크","AI 인프라 대규모 CapEx ($75B+ 연간) 투자 부담"],
    "opportunities":["AWS + Bedrock AI 서비스로 엔터프라이즈 AI 시장 선점","광고 사업: Prime Video 광고, DSP 확장으로 Meta/Google에 도전","Just Walk Out / 무인매장 기술 라이선싱","헬스케어(One Medical, Amazon Pharmacy) 진출 확대"],
    "watchlist":["AWS 분기별 매출 성장률 (20%+ 유지 여부)","영업이익률 개선 추이 (목표: 12%+)","Prime 구독료 인상 가능성 및 회원 이탈률","AI 인프라 투자 대비 AWS 수익화 속도"]
  },
  "accent":"#FF9900"
},

"META": {
  "profile": {"symbol":"META","name":"Meta Platforms, Inc.","price":595.00,"changes":4.22,"changesPct":0.71,"exchange":"NASDAQ","sector":"Technology","industry":"Internet Content & Information","country":"US","mktCap":"$1.56T","beta":1.24,"range":"414.50 - 740.91","employees":"72,404","desc":"Meta는 Facebook, Instagram, WhatsApp, Messenger 등 세계 최대 소셜 미디어 플랫폼을 운영하며, Reality Labs를 통해 VR/AR 메타버스 기술을 개발하고 있습니다. Llama AI 모델 오픈소스 전략으로도 주목받고 있습니다."},
  "income": [
    {"year":"2021","rev":117.93,"ni":39.37,"oi":46.75,"gp":95.56,"eps":13.77,"gm":80.79,"om":39.65,"nm":33.38},
    {"year":"2022","rev":116.61,"ni":23.20,"oi":28.94,"gp":92.46,"eps":8.59,"gm":79.28,"om":24.82,"nm":19.90},
    {"year":"2023","rev":134.90,"ni":39.10,"oi":46.75,"gp":108.40,"eps":14.87,"gm":80.35,"om":34.66,"nm":28.98},
    {"year":"2024","rev":164.50,"ni":62.36,"oi":69.38,"gp":132.49,"eps":23.86,"gm":80.54,"om":42.18,"nm":37.90},
    {"year":"2025","rev":178.00,"ni":66.53,"oi":74.00,"gp":143.60,"eps":26.20,"gm":80.67,"om":41.57,"nm":37.38},
  ],
  "quarterly": [
    {"q":"Q1'24","rev":36.46,"ni":12.37},{"q":"Q2'24","rev":39.07,"ni":13.47},
    {"q":"Q3'24","rev":40.59,"ni":15.69},{"q":"Q4'24","rev":48.39,"ni":20.84},
    {"q":"Q1'25","rev":42.31,"ni":16.64},{"q":"Q2'25","rev":43.50,"ni":16.00},
    {"q":"Q3'25","rev":44.50,"ni":16.50},{"q":"Q4'25","rev":47.69,"ni":17.39},
  ],
  "segments": {
    "labels":["FY2021","FY2022","FY2023","FY2024","FY2025"],
    "series":[
      {"name":"Family of Apps","color":"#1877F2","data":[115.66,114.45,131.95,160.85,174.00]},
      {"name":"Reality Labs","color":"#AB47BC","data":[2.27,2.16,2.95,3.65,4.00]},
    ]
  },
  "peers": [
    {"sym":"META","name":"Meta","mc":"$1.56T","pe":"23.5","ps":"8.8","rev":"$178B","nm":"37.4%","hl":True},
    {"sym":"GOOG","name":"Alphabet","mc":"$2.08T","pe":"21.8","ps":"5.8","rev":"$386B","nm":"27.5%","hl":False},
    {"sym":"SNAP","name":"Snap","mc":"$19B","pe":"-","ps":"3.4","rev":"$5.4B","nm":"-5%","hl":False},
    {"sym":"PINS","name":"Pinterest","mc":"$21B","pe":"30.0","ps":"6.0","rev":"$3.6B","nm":"18%","hl":False},
    {"sym":"TTD","name":"Trade Desk","mc":"$35B","pe":"65.0","ps":"14.5","rev":"$2.4B","nm":"21%","hl":False},
    {"sym":"SPOT","name":"Spotify","mc":"$90B","pe":"55.0","ps":"5.5","rev":"$17B","nm":"9%","hl":False},
  ],
  "ratios": {"pe":23.50,"fpe":20.80,"ps":8.80,"peg":1.05,"roe":"35.2%","div":"0.35%"},
  "invest": {
    "strengths":["Facebook + Instagram + WhatsApp 통합 MAU 39억명 — 전 세계 최대 소셜 플랫폼","디지털 광고 타겟팅 정확도 업계 최고 수준 → ROAS 높음","Llama 오픈소스 AI 모델로 AI 생태계 영향력 확보","순이익률 37%+로 수익성 대폭 개선 (2022년 대비)"],
    "risks":["Reality Labs 연간 $16B+ 적자 지속 — 메타버스 투자 회수 불확실","Apple ATT 정책으로 광고 타겟팅 제약 (일부 회복 중)","규제 리스크: EU DMA, 아동 보호법, 미국 반독점 소송","AI 인프라 투자 급증으로 CapEx $40B+ 부담"],
    "opportunities":["Reels 광고 수익화 본격화 — TikTok 규제 시 최대 수혜","AI 광고 최적화 (Advantage+) 로 광고주 ROI 대폭 개선","WhatsApp Business API로 커머스/결제 플랫폼 확장","Ray-Ban Meta 스마트 글래스 → AR 디바이스 시장 선점"],
    "watchlist":["Family of Apps 분기별 ARPU 성장 추이","Reality Labs 분기 적자 축소 여부","Reels vs TikTok 이용 시간 추이","AI CapEx 투자 규모 및 수익화 전환 시점"]
  },
  "accent":"#1877F2"
},

"TSLA": {
  "profile": {"symbol":"TSLA","name":"Tesla, Inc.","price":268.50,"changes":-5.73,"changesPct":-2.09,"exchange":"NASDAQ","sector":"Consumer Cyclical","industry":"Auto Manufacturers","country":"US","mktCap":"$860B","beta":2.31,"range":"138.80 - 488.54","employees":"140,473","desc":"Tesla는 전기차(EV), 에너지 저장(Megapack), 태양광, FSD 자율주행 소프트웨어, AI 로보틱스(Optimus) 등을 개발하는 혁신 기업입니다. EV 시장의 글로벌 리더이자 에너지 전환의 핵심 기업입니다."},
  "income": [
    {"year":"2021","rev":53.82,"ni":5.52,"oi":6.52,"gp":13.61,"eps":1.63,"gm":25.28,"om":12.12,"nm":10.25},
    {"year":"2022","rev":81.46,"ni":12.58,"oi":13.66,"gp":20.85,"eps":3.62,"gm":25.60,"om":16.76,"nm":15.44},
    {"year":"2023","rev":96.77,"ni":15.00,"oi":8.89,"gp":17.66,"eps":4.31,"gm":18.25,"om":9.19,"nm":15.50},
    {"year":"2024","rev":97.69,"ni":7.09,"oi":7.07,"gp":17.85,"eps":2.04,"gm":18.27,"om":7.24,"nm":7.26},
    {"year":"2025","rev":112.00,"ni":9.50,"oi":10.00,"gp":22.40,"eps":2.72,"gm":20.00,"om":8.93,"nm":8.48},
  ],
  "quarterly": [
    {"q":"Q1'24","rev":21.30,"ni":1.13},{"q":"Q2'24","rev":25.50,"ni":1.48},
    {"q":"Q3'24","rev":25.18,"ni":2.17},{"q":"Q4'24","rev":25.71,"ni":2.32},
    {"q":"Q1'25","rev":19.34,"ni":0.41},{"q":"Q2'25","rev":28.00,"ni":2.50},
    {"q":"Q3'25","rev":30.00,"ni":3.00},{"q":"Q4'25","rev":34.66,"ni":3.59},
  ],
  "segments": {
    "labels":["FY2021","FY2022","FY2023","FY2024","FY2025"],
    "series":[
      {"name":"Automotive","color":"#CC0000","data":[47.23,71.46,82.42,77.07,85.00]},
      {"name":"Energy & Storage","color":"#FFC107","data":[2.79,3.91,6.04,10.37,15.00]},
      {"name":"Services & Other","color":"#607D8B","data":[3.80,6.09,8.31,10.25,12.00]},
    ]
  },
  "peers": [
    {"sym":"TSLA","name":"Tesla","mc":"$860B","pe":"98.7","ps":"7.7","rev":"$112B","nm":"8.5%","hl":True},
    {"sym":"TM","name":"Toyota","mc":"$250B","pe":"8.5","ps":"0.7","rev":"$320B","nm":"9.0%","hl":False},
    {"sym":"BYD","name":"BYD","mc":"$115B","pe":"23.0","ps":"1.2","rev":"$98B","nm":"5.2%","hl":False},
    {"sym":"F","name":"Ford","mc":"$40B","pe":"6.8","ps":"0.2","rev":"$180B","nm":"3.5%","hl":False},
    {"sym":"GM","name":"GM","mc":"$52B","pe":"5.5","ps":"0.3","rev":"$175B","nm":"6.0%","hl":False},
    {"sym":"RIVN","name":"Rivian","mc":"$13B","pe":"-","ps":"2.5","rev":"$5.0B","nm":"-30%","hl":False},
  ],
  "ratios": {"pe":98.71,"fpe":78.50,"ps":7.68,"peg":3.20,"roe":"11.2%","div":"0%"},
  "invest": {
    "strengths":["EV 브랜드 인지도 및 슈퍼차저 네트워크 1위","에너지 저장(Megapack) 사업 YoY 50%+ 초고속 성장","FSD(자율주행) 소프트웨어 잠재 가치 — 고마진 구독 모델 가능","Gigafactory 글로벌 확장으로 생산 규모의 경제"],
    "risks":["자동차 마진 하락: 가격 경쟁 심화로 Gross Margin 20% 수준","중국 BYD 등 저가 EV와의 경쟁 심화 — 시장 점유율 하락","CEO 리스크: 엘론 머스크 정치 활동에 따른 브랜드 이미지 훼손","밸류에이션 극단적: Forward P/E 78.5x, 자동차 업계 평균 대비 10배+"],
    "opportunities":["Model 2 (저가형) 출시로 대중 시장 진입 → 볼륨 성장","로보택시(Cybercab) 상용화 시 기업 가치 패러다임 전환","Optimus 로봇: 장기적으로 자동차보다 큰 시장 잠재력","에너지 사업: 유틸리티용 Megapack + 가정용 Powerwall 확대"],
    "watchlist":["분기별 차량 인도량 및 평균판매가(ASP) 추이","FSD v13 이후 자율주행 안전성 데이터","에너지 부문 매출 비중 확대 속도","Model 2 / Cybercab 출시 일정 구체화 여부"]
  },
  "accent":"#CC0000"
},
}

# ══════════════════════════════════════════════════════════════════════════════
# SVG CHART GENERATORS
# ══════════════════════════════════════════════════════════════════════════════

def svg_grouped_bar(labels, datasets, W=580, H=260, unit="B"):
    pad_l,pad_r,pad_t,pad_b=55,15,15,45; cW=W-pad_l-pad_r; cH=H-pad_t-pad_b
    all_vals=[v for ds in datasets for v in ds["data"]]; max_v=max(all_vals)*1.15 if all_vals else 1
    n=len(labels); g_count=len(datasets); g_w=cW/n; b_w=(g_w*0.65)/g_count
    lines=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
    for i in range(5):
        y=pad_t+cH-(cH*i/4); val=max_v*i/4
        lines.append(f'<line x1="{pad_l}" y1="{y}" x2="{W-pad_r}" y2="{y}" stroke="#2d3148"/>')
        lines.append(f'<text x="{pad_l-6}" y="{y+4}" fill="#9ca0b8" font-size="10" text-anchor="end">${val:.0f}{unit}</text>')
    for di,ds in enumerate(datasets):
        for vi,v in enumerate(ds["data"]):
            x=pad_l+vi*g_w+g_w*0.175+di*b_w; bh=(v/max_v)*cH; y=pad_t+cH-bh
            lines.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{b_w:.1f}" height="{bh:.1f}" rx="3" fill="{ds["color"]}" opacity="0.8"/>')
            if g_count<=2: lines.append(f'<text x="{x+b_w/2:.1f}" y="{y-3}" fill="{ds["color"]}" font-size="8" text-anchor="middle" font-weight="600">${v:.1f}{unit}</text>')
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
    max_eps=max(abs(e) for e in eps_vals)*1.2 if eps_vals else 1; max_per=max(per_vals)*1.2 if per_vals and max(per_vals)>0 else 50; n=len(income); bw=cW/n*0.5
    if max_eps==0: max_eps=1
    if max_per==0: max_per=1
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
# HTML SECTION GENERATORS (per ticker)
# ══════════════════════════════════════════════════════════════════════════════

def gen_ticker_html(sym, data):
    p = data["profile"]
    inc = data["income"]
    qtr = data["quarterly"]
    seg = data["segments"]
    peers = data["peers"]
    ratios = data["ratios"]
    invest = data["invest"]
    accent = data["accent"]

    rev_g = ((inc[-1]["rev"]-inc[-2]["rev"])/inc[-2]["rev"]*100)
    ni_g = ((inc[-1]["ni"]-inc[-2]["ni"])/inc[-2]["ni"]*100) if inc[-2]["ni"]!=0 else 0
    chg_cls = "up" if p["changes"]>=0 else "down"
    chg_sign = "+" if p["changes"]>=0 else ""

    # Charts
    rev_chart = svg_grouped_bar(
        [f'FY{d["year"]}' for d in inc],
        [{"label":"매출","color":accent,"data":[d["rev"] for d in inc]},
         {"label":"순이익","color":"#4ecdc4","data":[d["ni"] for d in inc]}]
    )
    margin_chart = svg_line_chart(
        [f'FY{d["year"]}' for d in inc],
        [{"label":"매출총이익률","color":accent,"data":[d["gm"] for d in inc]},
         {"label":"영업이익률","color":"#4dabf7","data":[d["om"] for d in inc]},
         {"label":"순이익률","color":"#b197fc","data":[d["nm"] for d in inc]}]
    )
    q_chart = svg_grouped_bar(
        [d["q"] for d in qtr],
        [{"label":"분기 매출","color":accent,"data":[d["rev"] for d in qtr]},
         {"label":"분기 순이익","color":"#4ecdc4","data":[d["ni"] for d in qtr]}]
    )
    donut_chart = svg_donut([{"name":s["name"],"value":s["data"][-1],"color":s["color"]} for s in seg["series"]])
    stacked_chart = svg_stacked_bar(seg["labels"], seg["series"])
    eps_chart = svg_eps_per(inc, p["price"], accent)

    # Peer P/E bar chart
    peer_pe_bars = ''
    pe_peers = [pp for pp in peers if pp["pe"]!="-"]
    for i,pp in enumerate(pe_peers):
        pe_val = float(pp["pe"])
        max_pe = max(float(x["pe"]) for x in pe_peers) * 1.2
        bh = pe_val / max_pe * 140 if max_pe > 0 else 0
        fill = accent if pp["hl"] else "#4dabf7"
        peer_pe_bars += f'<rect x="{50+i*90}" y="{180-bh:.0f}" width="60" height="{bh:.0f}" rx="4" fill="{fill}" opacity="0.8"/>'
        peer_pe_bars += f'<text x="{80+i*90}" y="{175-bh:.0f}" fill="{fill}" font-size="10" text-anchor="middle" font-weight="600">{pp["pe"]}x</text>'
        peer_pe_bars += f'<text x="{80+i*90}" y="198" fill="#9ca0b8" font-size="10" text-anchor="middle">{pp["sym"]}</text>'

    # Tables
    def fin_table():
        rows=[("매출 (Revenue)",[f"${d['rev']:.1f}B" for d in inc]),("매출총이익 (Gross Profit)",[f"${d['gp']:.1f}B" for d in inc]),("영업이익 (Operating Income)",[f"${d['oi']:.1f}B" for d in inc]),("순이익 (Net Income)",[f"${d['ni']:.1f}B" for d in inc]),("EPS (희석)",[f"${d['eps']:.2f}" for d in inc]),("매출총이익률",[f"{d['gm']:.1f}%" for d in inc]),("영업이익률",[f"{d['om']:.1f}%" for d in inc]),("순이익률",[f"{d['nm']:.1f}%" for d in inc])]
        h='<table><thead><tr><th>지표</th>'
        for d in inc: h+=f'<th class="nr">FY{d["year"]}</th>'
        h+='</tr></thead><tbody>'
        for l,vs in rows:
            h+=f'<tr><td>{l}</td>'
            for v in vs: h+=f'<td class="nr">{v}</td>'
            h+='</tr>'
        return h+'</tbody></table>'

    def seg_table():
        h='<table><thead><tr><th>부문</th>'
        for l in seg["labels"]: h+=f'<th class="nr">{l}</th>'
        h+='</tr></thead><tbody>'
        for s in seg["series"]:
            h+=f'<tr><td><span style="display:inline-block;width:10px;height:10px;border-radius:3px;background:{s["color"]};margin-right:8px;vertical-align:middle;"></span>{s["name"]}</td>'
            for v in s["data"]: h+=f'<td class="nr">${v:.1f}B</td>'
            h+='</tr>'
        return h+'</tbody></table>'

    def peer_table():
        h='<table><thead><tr><th>티커</th><th>기업명</th><th class="nr">시가총액</th><th class="nr">P/E</th><th class="nr">P/S</th><th class="nr">매출</th><th class="nr">순이익률</th></tr></thead><tbody>'
        for pp in peers:
            bg=f' style="background:rgba({int(accent[1:3],16)},{int(accent[3:5],16)},{int(accent[5:7],16)},.1);"' if pp["hl"] else ''
            s2=f'<strong>{pp["sym"]}</strong>' if pp["hl"] else pp["sym"]
            h+=f'<tr{bg}><td>{s2}</td><td>{pp["name"]}</td><td class="nr">{pp["mc"]}</td><td class="nr">{pp["pe"]}</td><td class="nr">{pp["ps"]}</td><td class="nr">{pp["rev"]}</td><td class="nr">{pp["nm"]}</td></tr>'
        return h+'</tbody></table>'

    def invest_html():
        sections=[("강점 (Strengths)","strengths","dot-green"),("리스크 (Risks)","risks","dot-red"),("기회 (Opportunities)","opportunities","dot-blue"),("주요 모니터링 (Watchlist)","watchlist","dot-orange")]
        h=''
        for title,key,dot in sections:
            h+=f'<div class="invest-card"><h4><span class="dot {dot}"></span> {title}</h4><ul>'
            for item in invest[key]: h+=f'<li>{item}</li>'
            h+='</ul></div>'
        return h

    mkt_cap = p["mktCap"]
    rev_last = f"${inc[-1]['rev']:.1f}B"
    ni_last = f"${inc[-1]['ni']:.1f}B"

    return f'''
<!-- ===== {sym} CONTENT ===== -->
<div class="ticker-content" id="content-{sym}" style="display:none;">

<div class="tc active" data-tab="overview" data-ticker="{sym}">
  <div class="ch" style="border-left:4px solid {accent};">
    <div><div class="ch-tk" style="color:{accent};">{sym}</div><div class="ch-nm">{p["name"]}</div><div class="ch-desc">{p["desc"]}</div><div style="margin-top:8px;font-size:12px;color:var(--text2);">{p["exchange"]} | {p["sector"]} | {p["industry"]} | {p["country"]}</div></div>
    <div class="ch-meta"><div class="ch-price">${p["price"]}</div><div class="ch-chg {chg_cls}">{chg_sign}{p["changes"]} ({chg_sign}{p["changesPct"]}%)</div><div style="font-size:12px;color:var(--text2);margin-top:8px;">52주: {p["range"]}</div></div>
  </div>
  <div class="kpi-row">
    <div class="kpi"><div class="kpi-l">시가총액</div><div class="kpi-v">{mkt_cap}</div><div class="kpi-s">Beta: {p["beta"]}</div></div>
    <div class="kpi"><div class="kpi-l">연간 매출</div><div class="kpi-v">{rev_last}</div><div class="kpi-s {"up" if rev_g>=0 else "down"}">{'+' if rev_g>=0 else ''}{rev_g:.1f}% YoY</div></div>
    <div class="kpi"><div class="kpi-l">연간 순이익</div><div class="kpi-v">{ni_last}</div><div class="kpi-s {"up" if ni_g>=0 else "down"}">{'+' if ni_g>=0 else ''}{ni_g:.1f}% YoY</div></div>
    <div class="kpi"><div class="kpi-l">EPS</div><div class="kpi-v">${inc[-1]["eps"]:.2f}</div><div class="kpi-s">순이익률 {inc[-1]["nm"]:.1f}%</div></div>
    <div class="kpi"><div class="kpi-l">P/E (TTM)</div><div class="kpi-v">{ratios["pe"]}</div><div class="kpi-s">PEG: {ratios["peg"]}</div></div>
    <div class="kpi"><div class="kpi-l">매출총이익률</div><div class="kpi-v">{inc[-1]["gm"]:.1f}%</div><div class="kpi-s">영업이익률 {inc[-1]["om"]:.1f}%</div></div>
  </div>
  <div class="cg">
    <div class="cc"><div class="ct">매출 &amp; 순이익 추이 <span class="badge">연간</span></div>{rev_chart}</div>
    <div class="cc"><div class="ct">수익성 지표 추이 <span class="badge">마진율</span></div>{margin_chart}</div>
    <div class="cc full"><div class="ct">분기별 매출 추이 <span class="badge">최근 8분기</span></div>{q_chart}</div>
  </div>
  <div class="cc"><div class="ct">연간 재무 데이터 <span class="badge">상세</span></div><div class="tw">{fin_table()}</div></div>
</div>

<div class="tc" data-tab="segments" data-ticker="{sym}">
  <div class="cg">
    <div class="cc"><div class="ct">사업부문별 매출 비중 <span class="badge">최신 FY</span></div>{donut_chart}</div>
    <div class="cc"><div class="ct">사업부문별 매출 추이 <span class="badge">연간</span></div>{stacked_chart}</div>
    <div class="cc full"><div class="ct">사업부문 상세 데이터</div><div class="tw">{seg_table()}</div></div>
  </div>
</div>

<div class="tc" data-tab="valuation" data-ticker="{sym}">
  <div class="kpi-row">
    <div class="kpi"><div class="kpi-l">P/E (TTM)</div><div class="kpi-v">{ratios["pe"]}</div></div>
    <div class="kpi"><div class="kpi-l">Forward P/E</div><div class="kpi-v">{ratios["fpe"]}</div></div>
    <div class="kpi"><div class="kpi-l">P/S</div><div class="kpi-v">{ratios["ps"]}</div></div>
    <div class="kpi"><div class="kpi-l">PEG</div><div class="kpi-v">{ratios["peg"]}</div></div>
    <div class="kpi"><div class="kpi-l">ROE</div><div class="kpi-v">{ratios["roe"]}</div></div>
    <div class="kpi"><div class="kpi-l">배당수익률</div><div class="kpi-v">{ratios["div"]}</div></div>
  </div>
  <div class="cg">
    <div class="cc"><div class="ct">EPS 추이 &amp; PER 밴드 <span class="badge">연간</span></div>{eps_chart}</div>
    <div class="cc"><div class="ct">동종업계 P/E 비교</div><svg viewBox="0 0 580 200" xmlns="http://www.w3.org/2000/svg">{peer_pe_bars}</svg></div>
  </div>
  <div class="cc"><div class="ct">동종업계 밸류에이션 비교</div><div class="tw">{peer_table()}</div></div>
</div>

<div class="tc" data-tab="invest" data-ticker="{sym}"><div class="ig">{invest_html()}</div></div>

</div>
'''


# ══════════════════════════════════════════════════════════════════════════════
# GENERATE FULL HTML
# ══════════════════════════════════════════════════════════════════════════════

ticker_list = list(TICKERS.keys())
# Generate ticker buttons for quick selection
ticker_buttons = ''
for i, sym in enumerate(ticker_list):
    d = TICKERS[sym]
    active = ' active' if i == 0 else ''
    ticker_buttons += f'<div class="ticker-btn{active}" data-sym="{sym}" onclick="switchTicker(\'{sym}\')" style="--accent-color:{d["accent"]}">{sym}</div>'

# Generate all ticker content blocks
all_ticker_html = ''
for sym, data in TICKERS.items():
    all_ticker_html += gen_ticker_html(sym, data)

html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>StockLens - 기업 종합분석 대시보드</title>
<style>
:root{{--bg:#0f1117;--card:#1a1d28;--card2:#232736;--border:#2d3148;--text:#e4e6f0;--text2:#9ca0b8;--accent:#76b900;--red:#ff6b6b;--blue:#4dabf7;--purple:#b197fc;--orange:#ffa94d;--green:#76b900;--radius:12px}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--text);min-height:100vh}}
.hdr{{background:linear-gradient(135deg,#1a1d28,#232736);padding:16px 32px;border-bottom:1px solid var(--border)}}
.hdr-top{{display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin-bottom:12px}}
.logo{{font-size:22px;font-weight:800;color:var(--accent)}}.logo span{{color:var(--text2);font-weight:400;font-size:14px;margin-left:8px}}
.ticker-bar{{display:flex;gap:8px;align-items:center;flex-wrap:wrap}}
.ticker-btn{{padding:8px 16px;border-radius:8px;cursor:pointer;font-weight:700;font-size:14px;color:var(--text2);background:var(--bg);border:1px solid var(--border);transition:all .2s}}
.ticker-btn:hover{{border-color:var(--text);color:var(--text)}}
.ticker-btn.active{{background:var(--accent-color,var(--accent));color:#000;border-color:transparent}}
.search-inline{{display:flex;align-items:center;gap:6px;margin-left:auto}}
.search-inline input{{background:var(--bg);border:1px solid var(--border);color:var(--text);padding:8px 14px;border-radius:8px;font-size:14px;width:140px;outline:none;text-transform:uppercase}}
.search-inline input:focus{{border-color:var(--accent)}}
.search-inline button{{background:var(--accent);color:#000;border:none;padding:8px 16px;border-radius:8px;font-weight:700;cursor:pointer;font-size:13px}}
.search-inline button:hover{{opacity:.85}}
.tabs{{display:flex;gap:4px;padding:16px 32px 0;background:var(--card);border-bottom:1px solid var(--border)}}
.tab{{padding:12px 24px;cursor:pointer;color:var(--text2);font-size:14px;font-weight:600;border-bottom:2px solid transparent;transition:all .15s}}
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
.ch-tk{{font-size:36px;font-weight:900}}.ch-nm{{font-size:18px}}.ch-desc{{font-size:13px;color:var(--text2);margin-top:4px;max-width:700px;line-height:1.5}}
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
.not-found{{text-align:center;padding:80px 20px;color:var(--text2)}}
.not-found h3{{color:var(--text);margin-bottom:12px;font-size:20px}}
.not-found p{{line-height:1.8;font-size:14px}}
.avail-tickers{{display:flex;gap:8px;justify-content:center;margin-top:16px;flex-wrap:wrap}}
.avail-tickers span{{background:var(--card2);padding:4px 12px;border-radius:6px;font-size:13px;cursor:pointer}}
.avail-tickers span:hover{{background:var(--accent);color:#000}}
@media(max-width:768px){{.cg,.ig{{grid-template-columns:1fr}}.ch{{flex-direction:column;text-align:center}}.ch-meta{{margin-left:0;text-align:center}}.kpi-row{{grid-template-columns:repeat(2,1fr)}}.hdr-top{{flex-direction:column}}.search-inline{{margin-left:0;width:100%}}.search-inline input{{flex:1}}}}
</style>
</head>
<body>

<div class="hdr">
  <div class="hdr-top">
    <div class="logo">StockLens <span>기업 종합분석</span></div>
    <div class="search-inline">
      <input id="tickerInput" type="text" placeholder="티커 검색" />
      <button onclick="searchTicker()">분석</button>
    </div>
  </div>
  <div class="ticker-bar" id="tickerBar">
    {ticker_buttons}
  </div>
</div>

<div class="tabs" id="tabBar">
  <div class="tab active" onclick="switchTab('overview')">개요 &amp; 재무</div>
  <div class="tab" onclick="switchTab('segments')">사업부문</div>
  <div class="tab" onclick="switchTab('valuation')">밸류에이션</div>
  <div class="tab" onclick="switchTab('invest')">투자 포인트</div>
</div>

<div class="main">
{all_ticker_html}

<div id="notFound" class="not-found" style="display:none;">
  <h3>해당 티커를 찾을 수 없습니다</h3>
  <p>현재 다음 기업의 분석 데이터가 제공됩니다:</p>
  <div class="avail-tickers" id="availTickers"></div>
  <p style="margin-top:20px;font-size:13px;color:var(--border);">추가 기업 분석이 필요하시면 요청해 주세요.</p>
</div>
</div>

<div class="wm">StockLens Dashboard v6.0 | 7개 기업 종합분석 | 생성일: 2026.03.28</div>

<script>
var currentTicker = '{ticker_list[0]}';
var currentTab = 'overview';
var availableTickers = {str(ticker_list)};

/* Show first ticker */
(function() {{
  var first = document.getElementById('content-' + currentTicker);
  if (first) first.style.display = '';
  var panes = first ? first.querySelectorAll('.tc[data-tab="overview"]') : [];
  for (var i = 0; i < panes.length; i++) panes[i].classList.add('active');
  /* populate available tickers list */
  var at = document.getElementById('availTickers');
  if (at) {{
    for (var i = 0; i < availableTickers.length; i++) {{
      var s = document.createElement('span');
      s.textContent = availableTickers[i];
      s.onclick = (function(t) {{ return function() {{ switchTicker(t); }}; }})(availableTickers[i]);
      at.appendChild(s);
    }}
  }}
}})();

function switchTicker(sym) {{
  /* Hide all ticker contents */
  var all = document.querySelectorAll('.ticker-content');
  for (var i = 0; i < all.length; i++) all[i].style.display = 'none';
  document.getElementById('notFound').style.display = 'none';
  /* Show selected */
  var el = document.getElementById('content-' + sym);
  if (el) {{
    el.style.display = '';
    currentTicker = sym;
    switchTab(currentTab);
    /* Update ticker bar */
    var btns = document.querySelectorAll('.ticker-btn');
    for (var i = 0; i < btns.length; i++) {{
      btns[i].className = btns[i].getAttribute('data-sym') === sym ? 'ticker-btn active' : 'ticker-btn';
    }}
    /* Update input */
    document.getElementById('tickerInput').value = sym;
  }} else {{
    document.getElementById('notFound').style.display = '';
  }}
}}

function switchTab(tab) {{
  currentTab = tab;
  var tabNames = ['overview','segments','valuation','invest'];
  /* Update tab bar */
  var tabs = document.querySelectorAll('.tab');
  for (var i = 0; i < tabs.length; i++) {{
    tabs[i].className = (i === tabNames.indexOf(tab)) ? 'tab active' : 'tab';
  }}
  /* Show/hide panes for current ticker */
  var container = document.getElementById('content-' + currentTicker);
  if (!container) return;
  var panes = container.querySelectorAll('.tc');
  for (var i = 0; i < panes.length; i++) {{
    panes[i].className = (panes[i].getAttribute('data-tab') === tab) ? 'tc active' : 'tc';
  }}
}}

function searchTicker() {{
  var input = document.getElementById('tickerInput').value.trim().toUpperCase();
  if (!input) return;
  switchTicker(input);
}}

/* Enter key support */
document.getElementById('tickerInput').onkeydown = function(e) {{
  if (e.keyCode === 13) searchTicker();
}};
</script>
</body>
</html>'''

# Write to file
output_path = "/sessions/exciting-gracious-pasteur/mnt/자산 대시보드 제작/02-projects/2026.03.28 기업분석대시보드/output/기업분석_종합대시보드_v6_2026.03.28.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)
print(f"✅ Dashboard v6 generated: {output_path}")
print(f"   Tickers: {', '.join(ticker_list)}")
print(f"   File size: {len(html):,} bytes")
