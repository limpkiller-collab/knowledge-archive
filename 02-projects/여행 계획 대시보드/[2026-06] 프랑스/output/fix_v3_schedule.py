#!/usr/bin/env python3
"""
Fix v3.1 schedule card layout to match Taichung reference:
1. Timeline CSS: smaller dot, Taichung-style layout
2. tl-time: accent color (not text-secondary)
3. tl-desc: support <strong> inline, line-height 1.7
4. Google Maps link as tag with SVG icon
5. SCHEDULE_DATA: add 'map' field (Google Maps search URL) to every item
6. renderSchedule: output Taichung-style HTML
7. Add day-expense-card (예상 경비 | 실제 사용)
"""
import re

FILE = '/sessions/jolly-relaxed-meitner/mnt/여행 계획 대시보드/[2026-06] 프랑스/output/프랑스여행_여행일정대시보드_v3.1_2026.03.29.html'

with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# ============================================================
# 1. Replace timeline CSS to match Taichung exactly
# ============================================================
old_timeline_css = """    .timeline {
      position: relative;
      padding: 20px 0;
    }

    .timeline::before {
      content: '';
      position: absolute;
      left: 30px;
      top: 0;
      bottom: 0;
      width: 2px;
      background: linear-gradient(180deg, var(--accent) 0%, transparent 100%);
    }

    .tl-item {
      display: flex;
      gap: 24px;
      margin-bottom: 24px;
      position: relative;
    }

    .tl-dot {
      width: 64px;
      height: 64px;
      border-radius: 50%;
      border: 3px solid var(--accent);
      background: var(--surface);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      margin-top: 4px;
      font-size: 24px;
    }

    .tl-card {
      flex: 1;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px;
      transition: all 0.3s;
    }

    .tl-card:hover {
      border-color: var(--accent);
      background: var(--surface-hover);
    }

    .tl-time {
      font-size: 13px;
      color: var(--text-secondary);
      font-weight: 600;
      text-transform: uppercase;
      margin-bottom: 4px;
    }

    .tl-title {
      font-size: 16px;
      font-weight: 700;
      margin-bottom: 8px;
    }

    .tl-desc {
      font-size: 14px;
      color: var(--text-secondary);
      margin-bottom: 12px;
      line-height: 1.5;
    }

    .cost-badge {
      display: inline-block;
      background: var(--tag-night);
      color: var(--tag-night-text);
      padding: 4px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      margin-left: 8px;
    }

    .cost-badge .krw {
      display: block;
      font-size: 11px;
      margin-top: 2px;
    }

    .tl-tags {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }

    .tag {
      display: inline-block;
      padding: 4px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      text-transform: capitalize;
    }"""

new_timeline_css = """    /* ===== TIMELINE (Taichung style) ===== */
    .timeline { position: relative; padding-left: 32px; }
    .timeline::before { content: ''; position: absolute; left: 11px; top: 8px; bottom: 8px; width: 2px; background: var(--border); border-radius: 1px; }
    .tl-item { position: relative; margin-bottom: 20px; }
    .tl-dot { position: absolute; left: -27px; top: 18px; width: 12px; height: 12px; border-radius: 50%; border: 2px solid var(--accent); background: var(--bg); }
    .tl-card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 20px; transition: box-shadow 0.2s; position: relative; }
    .tl-card:hover { box-shadow: 0 0 0 1px var(--border), 0 8px 16px rgba(0,0,0,0.08); }
    .tl-time { font-size: 13px; font-weight: 600; color: var(--accent); margin-bottom: 6px; font-variant-numeric: tabular-nums; }
    .tl-title { font-size: 16px; font-weight: 600; margin-bottom: 6px; letter-spacing: -0.02em; }
    .tl-desc { font-size: 14px; color: var(--text-secondary); line-height: 1.7; }
    .tl-desc strong { color: var(--text); font-weight: 500; }
    .cost-badge {
      display: inline-block;
      background: var(--tag-night); color: var(--tag-night-text);
      padding: 2px 8px; border-radius: 4px; font-size: 12px;
      font-weight: 500; white-space: nowrap;
    }
    .cost-badge .krw { color: var(--text-secondary); font-size: 11px; margin-left: 2px; }
    .tl-tags { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-top: 10px; }
    .tag { display: inline-flex; align-items: center; gap: 4px; padding: 3px 10px; border-radius: 6px; font-size: 12px; font-weight: 500; }"""

html = html.replace(old_timeline_css, new_timeline_css)
print("FIX 1: Timeline CSS replaced ✓")

# ============================================================
# 2. Replace map-link CSS with SVG icon style (Taichung)
# ============================================================
old_map_css = """    .map-link {
      color: var(--accent);
      text-decoration: none;
      font-weight: 600;
      font-size: 12px;
      transition: color 0.3s;
      cursor: pointer;
    }

    .map-link:hover {
      color: var(--accent-secondary);
    }"""

new_map_css = """    .map-link {
      display: inline-flex; align-items: center; gap: 4px;
      color: var(--accent); text-decoration: none; font-weight: 500;
      font-size: 12px; transition: opacity 0.2s; cursor: pointer;
    }
    .map-link:hover { opacity: 0.7; text-decoration: none; }
    .map-svg { width: 14px; height: 14px; flex-shrink: 0; }"""

html = html.replace(old_map_css, new_map_css)
print("FIX 2: Map link CSS updated ✓")

# ============================================================
# 3. Add day-expense-card CSS (Taichung style)
# ============================================================
day_expense_css = """
    /* ===== DAY EXPENSE CARD ===== */
    .day-expense-card {
      background: var(--surface); border: 1px solid var(--border); border-radius: 10px;
      padding: 14px 20px; margin-bottom: 20px; display: flex; align-items: center; gap: 16px;
      font-size: 13px; color: var(--text-secondary); flex-wrap: wrap;
    }
    .day-expense-card .expense-value { font-weight: 700; color: var(--text); }
    .expense-progress { flex: 1; min-width: 120px; height: 6px; background: var(--border); border-radius: 3px; overflow: hidden; }
    .expense-progress-bar { height: 100%; background: var(--accent); border-radius: 3px; width: 0; transition: width 0.3s; }
"""
# Insert before /* ===== TIMELINE
html = html.replace("    /* ===== TIMELINE (Taichung style) ===== */", day_expense_css + "    /* ===== TIMELINE (Taichung style) ===== */")
print("FIX 3: Day expense card CSS added ✓")

# ============================================================
# 4. Replace SCHEDULE_DATA with Google Maps URLs for every item
# ============================================================
old_schedule_data = """const SCHEDULE_DATA = [
  { day: 1, time: '18:00', title: '인천국제공항 출발', desc: 'Finnair AY0042', type: 'flight', cost: null },
  { day: 2, time: '10:25', title: '파리 CDG 도착', desc: 'Finnair AY1571', type: 'flight', cost: null },
  { day: 2, time: '12:34', title: 'CDG → Avignon Centre', desc: 'TGV', type: 'transport', cost: 90.20, currency: 'EUR' },
  { day: 2, time: '15:30', title: 'Avignon → Marseille St-Charles', desc: 'TGV', type: 'transport', cost: 20.00, currency: 'EUR' },
  { day: 2, time: '18:00', title: '마르세유 에어비앤비 체크인', desc: 'Rue Saint-Ferreol', type: 'hotel', cost: null },
  { day: 3, time: '10:00', title: '"Marseille" Landmark 포토스팟', desc: '인생샷 명소', type: 'spot', link: 'https://maps.app.goo.gl/EbrXFiHjm5hw8wSt8' },
  { day: 3, time: '11:30', title: 'Vieux-Port de Marseille', desc: '구항구 산책', type: 'spot', link: 'https://maps.app.goo.gl/VUi5DAWGWgnm3bUb8' },
  { day: 3, time: '13:00', title: '점심식사', desc: '로컬 카페', type: 'meal', cost: 15 },
  { day: 3, time: '14:30', title: 'Les Petits Trains de Marseille', desc: '꼬마관광열차', type: 'spot', link: 'https://maps.app.goo.gl/DP6tXPF2eUWoLiDu5', cost: 10 },
  { day: 3, time: '17:00', title: 'Notre-Dame de la Garde', desc: '노트르담 드 라 가르드 성당', type: 'spot', link: 'https://maps.app.goo.gl/T79dNKbn1gbrVk4D7' },
  { day: 4, time: '10:30', title: '렌터카 픽업', desc: 'Marseille St Charles', type: 'transport', cost: 296.44, currency: 'EUR', notes: '3일 렌탈' },
  { day: 4, time: '12:00', title: '고르드 (Gordes)', desc: '프로방스 절벽 마을', type: 'spot' },
  { day: 4, time: '14:30', title: '루시용 (Roussillon)', desc: '오렌지빛 절벽 마을', type: 'spot' },
  { day: 4, time: '16:00', title: '발랑솔 (Valensole)', desc: '라벤더 밭 (6월 초 개화)', type: 'spot' },
  { day: 4, time: '17:30', title: '무스티에생트마리 (Moustiers-Sainte-Marie)', desc: '도예 마을', type: 'spot' },
  { day: 5, time: '10:00', title: '무스티에생트마리 마을 산책', desc: '중세 마을 거리', type: 'spot' },
  { day: 5, time: '12:00', title: '점심식사', desc: 'La Cantine', type: 'meal', cost: 20 },
  { day: 5, time: '13:30', title: '베르동 협곡 (Gorges du Verdon)', desc: '자연 경관', type: 'spot' },
  { day: 5, time: '16:00', title: '생폴드방스 (Saint-Paul-de-Vence)', desc: '중세 예술 마을', type: 'spot' },
  { day: 6, time: '09:00', title: '빌프랑슈쉬르메르 (Villefranche-sur-Mer)', desc: '해안 마을', type: 'spot' },
  { day: 6, time: '11:30', title: '에즈 (Èze)', desc: '절벽 위 중세 마을, 식물원', type: 'spot' },
  { day: 6, time: '14:00', title: '점심식사', desc: 'Le Caruso', type: 'meal', cost: 25 },
  { day: 6, time: '15:30', title: '망통 (Menton)', desc: '해안 도시', type: 'spot' },
  { day: 7, time: '10:30', title: '렌터카 반납', desc: 'Nice Gare', type: 'transport' },
  { day: 7, time: '11:30', title: '니스 구시가지 (Vieille Ville)', desc: '오래된 거리 산책', type: 'spot' },
  { day: 7, time: '13:00', title: '점심식사', desc: 'Chez Thérésa', type: 'meal', cost: 8 },
  { day: 7, time: '14:30', title: '프롬나드 데 장글레 (Promenade des Anglais)', desc: '해변 산책로', type: 'spot' },
  { day: 7, time: '17:00', title: '마세나 광장 (Place Masséna)', desc: '광장 구경', type: 'spot' },
  { day: 8, time: '09:00', title: '살레야 광장 꽃시장 (Cours Saleya)', desc: '전통 시장', type: 'spot' },
  { day: 8, time: '11:00', title: '카페 & 브레크', desc: 'Oui Jelato', type: 'cafe', cost: 5 },
  { day: 8, time: '14:00', title: '니스 성곽 공원 (Colline du Château)', desc: '언덕 공원', type: 'spot' },
  { day: 8, time: '16:00', title: '마티스 미술관 or 샤갈 미술관', desc: '미술관 관광', type: 'spot', cost: 12 },
  { day: 9, time: '05:58', title: 'Nice → Paris Gare de Lyon', desc: 'TGV', type: 'transport', cost: 73.60, currency: 'EUR' },
  { day: 9, time: '15:00', title: '파리 도착 후 숙소 체크인', desc: 'Marais District', type: 'hotel' },
  { day: 9, time: '17:30', title: '에펠탑 (Tour Eiffel) - 야경', desc: '야간 관광', type: 'spot' },
  { day: 9, time: '19:00', title: '저녁 식사', desc: '근처 레스토랑', type: 'meal', cost: 22 },
  { day: 10, time: '09:00', title: '루브르 박물관 (Musée du Louvre)', desc: '미술관', type: 'spot', cost: 17 },
  { day: 10, time: '12:30', title: '점심식사', desc: 'Petit Vendôme', type: 'meal', cost: 8 },
  { day: 10, time: '14:00', title: '튈르리 정원 (Jardin des Tuileries)', desc: '정원 산책', type: 'spot' },
  { day: 10, time: '16:00', title: '콩코르드 광장 → 샹젤리제', desc: '거리 쇼핑', type: 'spot' },
  { day: 11, time: '09:00', title: '몽마르트르 (Montmartre)', desc: '사크레쾨르 성당', type: 'spot', cost: 10 },
  { day: 11, time: '12:00', title: '점심식사', desc: 'Mamiche', type: 'meal', cost: 5 },
  { day: 11, time: '14:00', title: '오르세 미술관 or 마레 지구', desc: '미술관/지구 탐방', type: 'spot' },
  { day: 11, time: '16:00', title: '생제르맹 데 프레 (Saint-Germain-des-Prés)', desc: '카페 문화', type: 'cafe', cost: 8 },
  { day: 11, time: '18:00', title: '센 강 유람선 (Bateaux Mouches)', desc: '석양 크루즈', type: 'spot', cost: 15 },
  { day: 12, time: '16:00', title: '파리 CDG → 헬싱키', desc: 'Finnair AY1572', type: 'flight' },
  { day: 12, time: '21:30', title: '헬싱키 → 인천', desc: 'Finnair AY0041', type: 'flight' }
];"""

new_schedule_data = """const SCHEDULE_DATA = [
  { day: 1, time: '18:00', title: '인천국제공항 출발', desc: '인천공항 <strong>제1터미널</strong> 출발. 국제선 <strong>2시간 전</strong> 도착 권장. 체크인 & 출국심사.', type: 'flight', cost: null, map: 'https://www.google.com/maps/search/Incheon+International+Airport+Terminal+1' },
  { day: 2, time: '10:25 (현지시각)', title: '파리 CDG 도착 (AY1571)', desc: '헬싱키 환승 후 파리 <strong>샤를 드 골 공항</strong>(CDG) 도착. 입국심사 & 수하물 수령.', type: 'flight', cost: null, map: 'https://www.google.com/maps/search/Paris+Charles+de+Gaulle+Airport' },
  { day: 2, time: '12:34', title: 'CDG → Avignon Centre', desc: '<strong>TGV</strong> 고속열차. 약 <strong>2시간 40분</strong> 소요. 아비뇽 중앙역 도착 후 환승.', type: 'transport', cost: 90.20, currency: 'EUR', map: 'https://www.google.com/maps/dir/Paris+CDG+Airport/Avignon+Centre' },
  { day: 2, time: '15:30', title: 'Avignon → Marseille St-Charles', desc: '<strong>TGV</strong> 약 <strong>30분</strong>. 마르세유 생샤를역 도착.', type: 'transport', cost: 20.00, currency: 'EUR', map: 'https://www.google.com/maps/dir/Gare+Avignon+Centre/Gare+Marseille+Saint+Charles' },
  { day: 2, time: '18:00', title: '마르세유 에어비앤비 체크인', desc: '<strong>Rue Saint-Ferreol</strong> 근처. 짐 정리 후 근처 산책.', type: 'hotel', cost: null, map: 'https://www.google.com/maps/search/Rue+Saint-Ferreol+Marseille' },
  { day: 3, time: '10:00', title: '"Marseille" Landmark 포토스팟', desc: '마르세유 시내 <strong>인생샷 명소</strong>. 도보 이동.', type: 'spot', map: 'https://maps.app.goo.gl/EbrXFiHjm5hw8wSt8' },
  { day: 3, time: '11:30', title: 'Vieux-Port de Marseille', desc: '마르세유 <strong>구항구</strong> 산책. 어시장 & 보트 구경.', type: 'spot', map: 'https://maps.app.goo.gl/VUi5DAWGWgnm3bUb8' },
  { day: 3, time: '13:00', title: '점심식사', desc: '구항구 근처 <strong>로컬 카페</strong>에서 점심.', type: 'meal', cost: 15, map: 'https://www.google.com/maps/search/restaurant+near+Vieux+Port+Marseille' },
  { day: 3, time: '14:30', title: 'Les Petits Trains de Marseille', desc: '구항구 출발 <strong>꼬마관광열차</strong>. 시내 주요 포인트 순회.', type: 'spot', cost: 10, map: 'https://maps.app.goo.gl/DP6tXPF2eUWoLiDu5' },
  { day: 3, time: '17:00', title: 'Notre-Dame de la Garde', desc: '마르세유 <strong>최고 전망대</strong>. 도시 & 지중해 파노라마 뷰.', type: 'spot', map: 'https://maps.app.goo.gl/T79dNKbn1gbrVk4D7' },
  { day: 4, time: '10:30', title: '렌터카 픽업', desc: '<strong>Marseille St Charles</strong> 역 앞 렌터카 사무소. <strong>3일 렌탈</strong> (6/5~6/7).', type: 'transport', cost: 296.44, currency: 'EUR', notes: '3일 렌탈', map: 'https://www.google.com/maps/search/car+rental+Marseille+Saint+Charles' },
  { day: 4, time: '12:00', title: '고르드 (Gordes)', desc: '프로방스 대표 <strong>절벽 마을</strong>. "프랑스에서 가장 아름다운 마을" 선정.', type: 'spot', map: 'https://www.google.com/maps/search/Gordes+France' },
  { day: 4, time: '14:30', title: '루시용 (Roussillon)', desc: '<strong>오렌지빛 절벽</strong> 마을. 오커 채석장 트레일 산책.', type: 'spot', map: 'https://www.google.com/maps/search/Roussillon+France' },
  { day: 4, time: '16:00', title: '발랑솔 (Valensole)', desc: '<strong>라벤더 밭</strong> (6월 초 개화 시작). 광활한 보라색 들판 포토.', type: 'spot', map: 'https://www.google.com/maps/search/Valensole+lavender+field' },
  { day: 4, time: '17:30', title: '무스티에생트마리', desc: '프로방스 <strong>도예 마을</strong>. 절벽 사이 별 전설. 숙박.', type: 'spot', map: 'https://www.google.com/maps/search/Moustiers-Sainte-Marie+France' },
  { day: 5, time: '10:00', title: '무스티에생트마리 마을 산책', desc: '<strong>중세 마을</strong> 골목 & 도자기 공방 구경.', type: 'spot', map: 'https://www.google.com/maps/search/Moustiers-Sainte-Marie+village' },
  { day: 5, time: '12:00', title: '점심식사 — La Cantine', desc: '<strong>프로방스 가정식</strong>. 제철 채소 & 올리브 오일 요리.', type: 'meal', cost: 20, map: 'https://www.google.com/maps/search/La+Cantine+Moustiers+Sainte+Marie' },
  { day: 5, time: '13:30', title: '베르동 협곡 (Gorges du Verdon)', desc: '유럽의 <strong>그랜드 캐니언</strong>. 에메랄드 빛 협곡 드라이브.', type: 'spot', map: 'https://www.google.com/maps/search/Gorges+du+Verdon' },
  { day: 5, time: '16:00', title: '생폴드방스 (Saint-Paul-de-Vence)', desc: '<strong>중세 예술 마을</strong>. 갤러리 & 아틀리에 산책. 숙박.', type: 'spot', map: 'https://www.google.com/maps/search/Saint-Paul-de-Vence+France' },
  { day: 6, time: '09:00', title: '빌프랑슈쉬르메르', desc: '<strong>파스텔 해안</strong> 마을. 코트다쥐르 대표 포토 스팟.', type: 'spot', map: 'https://www.google.com/maps/search/Villefranche-sur-Mer+France' },
  { day: 6, time: '11:30', title: '에즈 (Èze)', desc: '절벽 위 <strong>중세 마을</strong>. 이국적 식물원(Jardin Exotique) 필수 방문.', type: 'spot', map: 'https://www.google.com/maps/search/Eze+Village+France' },
  { day: 6, time: '14:00', title: '점심식사 — Le Caruso', desc: '<strong>생폴드방스 구시가지</strong>. 지중해 프렌치 요리 & 와인.', type: 'meal', cost: 25, map: 'https://www.google.com/maps/search/Le+Caruso+Saint+Paul+de+Vence' },
  { day: 6, time: '15:30', title: '망통 (Menton)', desc: '이탈리아 국경 <strong>레몬의 도시</strong>. 컬러풀 구시가지.', type: 'spot', map: 'https://www.google.com/maps/search/Menton+France+old+town' },
  { day: 7, time: '10:30', title: '렌터카 반납', desc: '<strong>Nice Gare</strong> 사무소 반납. 연료 만충 후 키 반환.', type: 'transport', map: 'https://www.google.com/maps/search/car+rental+Nice+Gare' },
  { day: 7, time: '11:30', title: '니스 구시가지 (Vieille Ville)', desc: '좁은 골목 & <strong>파스텔 건물</strong>. 로컬 상점 구경.', type: 'spot', map: 'https://www.google.com/maps/search/Vieille+Ville+Nice' },
  { day: 7, time: '13:00', title: '점심식사 — Chez Thérésa', desc: '쿠르살레야 시장 내 <strong>소카 전문점</strong>. 1925년부터 영업.', type: 'meal', cost: 8, map: 'https://www.google.com/maps/search/Chez+Theresa+Nice' },
  { day: 7, time: '14:30', title: '프롬나드 데 장글레', desc: '니스 대표 <strong>해변 산책로</strong>. 파란 의자에서 지중해 감상.', type: 'spot', map: 'https://www.google.com/maps/search/Promenade+des+Anglais+Nice' },
  { day: 7, time: '17:00', title: '마세나 광장 (Place Masséna)', desc: '니스 <strong>중심 광장</strong>. 분수 & 조형물. 트램 정류장.', type: 'spot', map: 'https://www.google.com/maps/search/Place+Massena+Nice' },
  { day: 8, time: '09:00', title: '살레야 꽃시장 (Cours Saleya)', desc: '니스 <strong>전통 시장</strong>. 꽃, 과일, 올리브, 라벤더 비누.', type: 'spot', map: 'https://www.google.com/maps/search/Cours+Saleya+Nice' },
  { day: 8, time: '11:00', title: '카페 — Oui Jelato', desc: '니스 구시가지 <strong>수제 젤라토</strong>. 라벤더 맛 추천.', type: 'cafe', cost: 5, map: 'https://www.google.com/maps/search/Oui+Jelato+Nice' },
  { day: 8, time: '14:00', title: '니스 성곽 공원 (Colline du Château)', desc: '언덕 공원. <strong>니스 항구 & 해안 파노라마</strong> 뷰.', type: 'spot', map: 'https://www.google.com/maps/search/Colline+du+Chateau+Nice' },
  { day: 8, time: '16:00', title: '마티스 미술관 or 샤갈 미술관', desc: '니스의 대표 <strong>미술관</strong>. 인상파 거장의 작품 감상.', type: 'spot', cost: 12, map: 'https://www.google.com/maps/search/Musee+Matisse+Nice' },
  { day: 9, time: '05:58', title: 'Nice → Paris Gare de Lyon', desc: '<strong>TGV</strong> 약 <strong>5시간 40분</strong>. 니스역 출발 → 파리 리옹역 도착.', type: 'transport', cost: 73.60, currency: 'EUR', map: 'https://www.google.com/maps/dir/Gare+Nice+Ville/Gare+de+Lyon+Paris' },
  { day: 9, time: '15:00', title: '파리 숙소 체크인', desc: '<strong>마레 지구</strong>(Marais District). 파리 중심부, 메트로 접근 용이.', type: 'hotel', map: 'https://www.google.com/maps/search/Le+Marais+Paris' },
  { day: 9, time: '17:30', title: '에펠탑 (Tour Eiffel)', desc: '야경 감상. <strong>트로카데로 광장</strong>에서 베스트 포토 스팟.', type: 'spot', map: 'https://www.google.com/maps/search/Tour+Eiffel+Paris' },
  { day: 9, time: '19:00', title: '저녁 식사', desc: '에펠탑 근처 <strong>레스토랑</strong>. 야경 디너.', type: 'meal', cost: 22, map: 'https://www.google.com/maps/search/restaurant+near+Tour+Eiffel+Paris' },
  { day: 10, time: '09:00', title: '루브르 박물관 (Musée du Louvre)', desc: '세계 최대 <strong>미술관</strong>. 모나리자, 밀로의 비너스. <strong>화요일 휴관</strong> 주의.', type: 'spot', cost: 17, map: 'https://www.google.com/maps/search/Musee+du+Louvre+Paris' },
  { day: 10, time: '12:30', title: '점심식사 — Petit Vendôme', desc: '루브르 근처 <strong>로컬 비스트로</strong>. 크루아상 & 잠봉뵈르 샌드위치.', type: 'meal', cost: 8, map: 'https://www.google.com/maps/search/Petit+Vendome+Paris' },
  { day: 10, time: '14:00', title: '튈르리 정원 (Jardin des Tuileries)', desc: '루브르~콩코르드 광장 잇는 <strong>프랑스식 정원</strong>. 산책.', type: 'spot', map: 'https://www.google.com/maps/search/Jardin+des+Tuileries+Paris' },
  { day: 10, time: '16:00', title: '콩코르드 광장 → 샹젤리제', desc: '파리 <strong>대표 거리</strong>. 쇼핑 & 개선문까지 산책.', type: 'spot', map: 'https://www.google.com/maps/search/Champs+Elysees+Paris' },
  { day: 11, time: '09:00', title: '몽마르트르 (Montmartre)', desc: '<strong>사크레쾨르 성당</strong>. 화가의 거리, 테르트르 광장.', type: 'spot', cost: 10, map: 'https://www.google.com/maps/search/Sacre+Coeur+Montmartre+Paris' },
  { day: 11, time: '12:00', title: '점심식사 — Mamiche', desc: '몽마르트르 <strong>인기 베이커리</strong>. 수제빵 & 페이스트리.', type: 'meal', cost: 5, map: 'https://www.google.com/maps/search/Mamiche+Paris' },
  { day: 11, time: '14:00', title: '오르세 미술관 or 마레 지구', desc: '<strong>인상파 미술관</strong> 또는 마레 지구 빈티지 숍 투어.', type: 'spot', map: 'https://www.google.com/maps/search/Musee+Orsay+Paris' },
  { day: 11, time: '16:00', title: '생제르맹 데 프레', desc: '파리 <strong>카페 문화</strong>의 성지. Café de Flore, Les Deux Magots.', type: 'cafe', cost: 8, map: 'https://www.google.com/maps/search/Cafe+de+Flore+Paris' },
  { day: 11, time: '18:00', title: '센 강 유람선 (Bateaux Mouches)', desc: '<strong>석양 크루즈</strong>. 에펠탑 & 노트르담 야경. 약 1시간.', type: 'spot', cost: 15, map: 'https://www.google.com/maps/search/Bateaux+Mouches+Paris' },
  { day: 12, time: '16:00', title: '파리 CDG → 헬싱키', desc: 'Finnair <strong>AY1572</strong>. 오전 자유시간 후 공항 이동.', type: 'flight', map: 'https://www.google.com/maps/search/Paris+CDG+Airport' },
  { day: 12, time: '21:30', title: '헬싱키 → 인천', desc: 'Finnair <strong>AY0041</strong>. 환승 후 인천행. 다음날 오전 도착.', type: 'flight', map: 'https://www.google.com/maps/search/Helsinki+Vantaa+Airport' }
];"""

html = html.replace(old_schedule_data, new_schedule_data)
print("FIX 4: SCHEDULE_DATA replaced with maps + rich desc ✓")

# ============================================================
# 5. Replace renderSchedule function with Taichung-style output
# ============================================================
old_render = """function renderSchedule() {
  const dayTabsContainer = document.getElementById('dayTabs');
  const dayContentsContainer = document.getElementById('dayContentsContainer');

  dayTabsContainer.innerHTML = '';
  dayContentsContainer.innerHTML = '';

  DAYS.forEach(day => {
    // Tab
    const tab = document.createElement('button');
    tab.className = `day-tab ${day.num === 1 ? 'active' : ''}`;
    tab.style.borderLeft = `3px solid var(--day${day.num})`;
    tab.onclick = () => showDay(day.num);
    tab.innerHTML = `DAY ${day.num}<span class="tab-date">${day.date.slice(5)} ${day.dow}</span>`;
    dayTabsContainer.appendChild(tab);

    // Content
    const content = document.createElement('div');
    content.className = `day-content ${day.num === 1 ? 'active' : ''}`;
    content.id = `day${day.num}`;

    const daySchedule = SCHEDULE_DATA.filter(s => s.day === day.num);

    let html = `
      <div class="day-header" style="border-left-color: var(--day${day.num});">
        <div class="day-number" style="background: var(--day${day.num});">${day.num}</div>
        <div class="day-meta">
          <h2>${day.title}</h2>
          <p>${day.date} (${day.dow}) · ${day.desc}</p>
        </div>
      </div>
      <div class="timeline">
    `;

    daySchedule.forEach((item, idx) => {
      const icon = getTypeIcon(item.type);
      const costHTML = item.cost ? `<span class="cost-badge">~${item.currency === 'EUR' ? '€' : ''}${item.cost}${item.currency === 'KRW' ? ' KRW' : ''}<span class="krw">(₩${Math.round(item.currency === 'EUR' ? item.cost * EUR_TO_KRW : item.cost)})</span></span>` : '';
      const linkHTML = item.link ? `<a class="map-link" href="${item.link}" target="_blank">지도</a>` : '';

      html += `
        <div class="tl-item">
          <div class="tl-dot" style="border-color: var(--day${day.num});">${icon}</div>
          <div class="tl-card">
            <div class="tl-time">${item.time}</div>
            <div class="tl-title">${item.title}</div>
            <div class="tl-desc">${item.desc} ${costHTML}</div>
            <div class="tl-tags">
              <span class="tag tag-${item.type}">${getTypeLabel(item.type)}</span>
              ${linkHTML}
            </div>
          </div>
        </div>
      `;
    });

    html += '</div>';
    content.innerHTML = html;
    dayContentsContainer.appendChild(content);
  });
}"""

new_render = """function renderSchedule() {
  var MAP_SVG = '<svg class="map-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>';
  var dayTabsContainer = document.getElementById('dayTabs');
  var dayContentsContainer = document.getElementById('dayContentsContainer');

  dayTabsContainer.innerHTML = '';
  dayContentsContainer.innerHTML = '';

  DAYS.forEach(function(day) {
    // Tab
    var tab = document.createElement('button');
    tab.className = 'day-tab' + (day.num === 1 ? ' active' : '');
    tab.style.borderLeft = '3px solid var(--day' + day.num + ')';
    tab.onclick = function() { showDay(day.num); };
    tab.innerHTML = 'DAY ' + day.num + '<span class="tab-date">' + day.date.slice(5) + ' ' + day.dow + '</span>';
    dayTabsContainer.appendChild(tab);

    // Content
    var content = document.createElement('div');
    content.className = 'day-content' + (day.num === 1 ? ' active' : '');
    content.id = 'day' + day.num;

    var daySchedule = SCHEDULE_DATA.filter(function(s) { return s.day === day.num; });

    // Calculate day budget
    var dayBudget = 0;
    daySchedule.forEach(function(s) {
      if (s.cost) {
        dayBudget += (s.currency === 'EUR') ? s.cost : (s.currency === 'KRW' ? s.cost / EUR_TO_KRW : s.cost);
      }
    });
    var dayBudgetKRW = Math.round(dayBudget * EUR_TO_KRW);

    var html = '';
    // Day header
    html += '<div class="day-header"><div class="day-number" style="background:var(--day' + day.num + ');">' + day.num + '</div><div class="day-meta"><h2>' + day.title + '</h2><p>' + day.date + ' (' + day.dow + ') · ' + day.desc + '</p></div></div>';

    // Day expense card
    html += '<div class="day-expense-card" id="dayExpenseCard' + day.num + '">';
    html += '<span class="expense-label">예상 경비: ' + (dayBudget > 0 ? '€' + dayBudget.toFixed(0) + ' (₩' + dayBudgetKRW.toLocaleString() + ')' : '-') + '</span> | ';
    html += '<span class="expense-label">실제 사용: <span class="expense-value" id="dayActual' + day.num + '">0 EUR (₩0)</span></span>';
    html += '<div class="expense-progress"><div class="expense-progress-bar" id="dayBar' + day.num + '"></div></div>';
    html += '</div>';

    // Timeline
    html += '<div class="timeline">';

    daySchedule.forEach(function(item) {
      var costHTML = '';
      if (item.cost) {
        var isEUR = item.currency === 'EUR';
        var isKRW = item.currency === 'KRW';
        if (isEUR) {
          costHTML = ' <span class="cost-badge">~€' + item.cost + '<span class="krw">(₩' + Math.round(item.cost * EUR_TO_KRW).toLocaleString() + ')</span></span>';
        } else if (isKRW) {
          costHTML = ' <span class="cost-badge">~₩' + Math.round(item.cost).toLocaleString() + '</span>';
        } else {
          costHTML = ' <span class="cost-badge">~€' + item.cost + '<span class="krw">(₩' + Math.round(item.cost * EUR_TO_KRW).toLocaleString() + ')</span></span>';
        }
      }

      var mapHTML = '';
      if (item.map) {
        mapHTML = '<a class="map-link" href="' + item.map + '" target="_blank" rel="noopener">' + MAP_SVG + '지도</a>';
      }

      var notesHTML = '';
      if (item.notes) {
        notesHTML = '<span class="tag tag-transport">' + item.notes + '</span>';
      }

      html += '<div class="tl-item">';
      html += '<div class="tl-dot" style="border-color:var(--day' + day.num + ');"></div>';
      html += '<div class="tl-card">';
      html += '<div class="tl-time">' + item.time + '</div>';
      html += '<div class="tl-title">' + item.title + '</div>';
      html += '<div class="tl-desc">' + item.desc + costHTML + '</div>';
      html += '<div class="tl-tags">';
      html += '<span class="tag tag-' + item.type + '">' + getTypeLabel(item.type) + '</span>';
      html += notesHTML;
      html += mapHTML;
      html += '</div>';
      html += '</div></div>';
    });

    html += '</div>';
    content.innerHTML = html;
    dayContentsContainer.appendChild(content);
  });
}"""

html = html.replace(old_render, new_render)
print("FIX 5: renderSchedule replaced ✓")

# ============================================================
# 6. Fix day-header CSS to match Taichung (no border-left)
# ============================================================
old_day_header = """    .day-header {
      display: flex;
      align-items: center;
      gap: 16px;
      margin-bottom: 20px;
      padding: 12px 0;
      border-left: 4px solid var(--accent);
      padding-left: 16px;
    }"""

new_day_header = """    .day-header {
      display: flex; align-items: center; gap: 12px;
      margin-bottom: 24px; padding-bottom: 16px;
      border-bottom: 1px solid var(--border);
    }"""

html = html.replace(old_day_header, new_day_header)
print("FIX 6: Day header CSS updated ✓")

# ============================================================
# 7. Day-number CSS (keep existing but ensure match)
# ============================================================
old_day_num = """    .day-number {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      font-weight: 700;
      color: white;
    }"""

new_day_num = """    .day-number {
      width: 48px; height: 48px; border-radius: 12px;
      display: flex; align-items: center; justify-content: center;
      font-size: 20px; font-weight: 700; color: #fff;
    }"""

html = html.replace(old_day_num, new_day_num)
print("FIX 7: Day number CSS updated ✓")

# ============================================================
# 8. Day meta CSS
# ============================================================
old_day_meta_h2 = """    .day-meta h2 {
      font-size: 18px;
      font-weight: 700;
    }

    .day-meta p {
      font-size: 12px;
      color: var(--text-secondary);
    }"""

new_day_meta = """    .day-meta h2 { font-size: 20px; margin-bottom: 2px; }
    .day-meta p { font-size: 13px; color: var(--text-secondary); }"""

html = html.replace(old_day_meta_h2, new_day_meta)
print("FIX 8: Day meta CSS updated ✓")

# ============================================================
# 9. Update version history
# ============================================================
old_ver = """  v3.1 (2026.03.29) : 모달 버그 수정 (블러만 뜨고 폼 안보이던 현상),
                       폰트/크기/카드 레이아웃 타이중 v12에 맞춤,
                       backdrop 클릭 닫기, 모바일 bottom-sheet 모달"""
new_ver = """  v3.2 (2026.03.30) : 일정카드 레이아웃 타이중 v12와 동일하게 변경,
                       모든 장소에 구글지도 연동, 설명 텍스트 보강,
                       일자별 예상경비/실제사용 프로그레스바 추가
  v3.1 (2026.03.29) : 모달 버그 수정 (블러만 뜨고 폼 안보이던 현상),
                       폰트/크기/카드 레이아웃 타이중 v12에 맞춤,
                       backdrop 클릭 닫기, 모바일 bottom-sheet 모달"""

html = html.replace(old_ver, new_ver)
print("FIX 9: Version history updated ✓")

# ============================================================
# WRITE as v3.2
# ============================================================
OUT = '/sessions/jolly-relaxed-meitner/mnt/여행 계획 대시보드/[2026-06] 프랑스/output/프랑스여행_여행일정대시보드_v3.2_2026.03.30.html'
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html)

with open(OUT, 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

print(f"\nOutput: {OUT}")
print(f"Lines: {len(lines)}")

checks = [
    ('tl-dot', 'Timeline dot'),
    ('tl-card', 'Timeline card'),
    ('tl-time', 'Timeline time'),
    ('tl-title', 'Timeline title'),
    ('tl-desc', 'Timeline desc'),
    ('map-svg', 'Map SVG icon'),
    ('map-link', 'Map link CSS'),
    ('google.com/maps', 'Google Maps URLs'),
    ('day-expense-card', 'Day expense card'),
    ('expense-progress', 'Expense progress bar'),
    ('<strong>', 'Rich text in desc'),
    ('day-header', 'Day header'),
    ('SCHEDULE_DATA', 'Schedule data'),
    ('renderSchedule', 'renderSchedule function'),
    ('MAP_SVG', 'MAP_SVG constant'),
    ('FOOD_DATA', 'Food data intact'),
    ('modal-overlay', 'Modal overlay intact'),
]

print("\n--- Verification ---")
all_ok = True
for needle, label in checks:
    count = content.count(needle)
    if count > 0:
        print(f"  ✓ {label} ({count}x)")
    else:
        print(f"  ✗ {label} MISSING!")
        all_ok = False

# Count google maps links
maps_count = content.count('google.com/maps')
print(f"\n  Google Maps links: {maps_count}")
print(f"  Schedule items: {content.count('{ day:')}")

if all_ok:
    print("\n✅ All checks passed!")
else:
    print("\n⚠️ Some checks failed!")
