#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3.6 -> v3.7: NEARBY_DATA + JS rendering + FOOD/CAFE 확장 + 일정 설명 보강"""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(BASE, '프랑스여행_여행일정대시보드_v3.6_2026.03.30.html')
DST  = os.path.join(BASE, '프랑스여행_여행일정대시보드_v3.7_2026.03.30.html')

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

changes = 0
def do(text, old, new, label=""):
    global changes
    if old not in text:
        print(f"  SKIP [{label}]")
        return text
    changes += 1
    print(f"  OK   [{label}]")
    return text.replace(old, new, 1)

# ====================================================================
# 1. NEARBY_DATA 상수 (SCHEDULE_DATA 끝 다음에 삽입)
# ====================================================================
NEARBY_DATA_JS = """
/* ===== 목적지별 근처 추천 스팟 ===== */
const NEARBY_DATA = {
  /* ── DAY 3 마르세유 ── */
  'Vieux-Port de Marseille': [
    { type:'meal', name:'Coquille Bistrot Marin', walk:'도보 2분', desc:'정어리·앤초비 피자 전문. 현지인 단골집', map:'https://www.google.com/maps/search/Coquille+Bistrot+Marin+Marseille' },
    { type:'cafe', name:'Maison Charlie', walk:'도보 5분', desc:'포카치나·핫초코 유명 항구 근처 로컬 빵집', map:'https://www.google.com/maps/search/Maison+Charlie+Marseille' },
    { type:'spot', name:'Marché des Noailles', walk:'도보 10분', desc:'향신료·파니스(튀긴 병아리콩) 길거리음식 로컬 시장', map:'https://www.google.com/maps/search/Marche+Noailles+Marseille' }
  ],
  'Notre-Dame de la Garde': [
    { type:'spot', name:'Le Panier 골목', walk:'도보 15분', desc:'마르세유 최고(最古) 동네. 거리예술 & 로컬 공방', map:'https://www.google.com/maps/search/Le+Panier+Marseille' },
    { type:'cafe', name:'Les Navettes des Accoules', walk:'도보 20분', desc:'오렌지꽃향 전통 나베트(배모양 비스킷) 원조 빵집', map:'https://www.google.com/maps/search/Les+Navettes+des+Accoules+Marseille' },
    { type:'meal', name:'Lou Pistou', walk:'도보 15분', desc:'르 파니에 지역 소박한 프로방스 채소 수프 가정식', map:'https://www.google.com/maps/search/Lou+Pistou+Marseille+Le+Panier' }
  ],
  /* ── DAY 4 프로방스 드라이브 ── */
  '고르드 (Gordes)': [
    { type:'spot', name:'Abbaye de Sénanque', walk:'차로 10분', desc:'라벤더 밭 속 12세기 수도원. 6월 개화 절정', map:'https://www.google.com/maps/search/Abbaye+de+Senanque+Gordes' },
    { type:'cafe', name:'Le Café de la Fontaine', walk:'도보 2분', desc:'고르드 마을 광장 카페. 로컬 타르트 & 카페오레', map:'https://www.google.com/maps/search/Café+Fontaine+Gordes+village' },
    { type:'spot', name:'Village des Bories', walk:'차로 5분', desc:'선사시대 돌집 마을. 독특한 건식석조 건축 포토스팟', map:'https://www.google.com/maps/search/Village+des+Bories+Gordes' }
  ],
  '루시용 (Roussillon)': [
    { type:'spot', name:'Sentier des Ocres', walk:'도보 5분', desc:'오커 채석장 트레일. 불꽃빛 절벽 하이킹 45분 코스', map:'https://www.google.com/maps/search/Sentier+des+Ocres+Roussillon' },
    { type:'cafe', name:'Bar Le Roussillon', walk:'도보 1분', desc:'마을 광장 테라스 카페. 현지인 아페로 & 와인', map:'https://www.google.com/maps/search/Bar+Le+Roussillon+Village' },
    { type:'meal', name:'Le Castrum', walk:'도보 3분', desc:'루시용 뷰 테라스 런치. 프로방스 살러드 €15 내외', map:'https://www.google.com/maps/search/Le+Castrum+Roussillon+Provence' }
  ],
  '발랑솔 (Valensole)': [
    { type:'spot', name:'발랑솔 라벤더 협동농장', walk:'도보 10분', desc:'라벤더 오일·꿀·비누 직거래 판매. 6월 초 개화 시작', map:'https://www.google.com/maps/search/Valensole+lavender+farm+cooperative' },
    { type:'cafe', name:'La Terrasse du Village', walk:'도보 5분', desc:'마을 테라스 카페. 라벤더 레모네이드 & 아이스크림', map:'https://www.google.com/maps/search/cafe+terrasse+Valensole+village' }
  ],
  '무스티에생트마리': [
    { type:'spot', name:'Notre-Dame de Beauvoir 성당', walk:'도보 20분', desc:'절벽 성당까지 258계단 트레킹. 마을 파노라마 뷰', map:'https://www.google.com/maps/search/Notre-Dame+de+Beauvoir+Moustiers-Sainte-Marie' },
    { type:'cafe', name:'Café Marguerite', walk:'도보 2분', desc:'유기농 음료·타파스. 성당·폭포 뷰 테라스 카페', map:'https://www.google.com/maps/search/Café+Marguerite+Moustiers-Sainte-Marie' },
    { type:'cafe', name:'Café & Gourmandises', walk:'도보 3분', desc:'폭포 옆 테라스. 수제 파이·페이스트리 간식', map:'https://www.google.com/maps/search/Café+Gourmandises+Moustiers-Sainte-Marie' }
  ],
  /* ── DAY 5 베르동·생폴드방스 ── */
  '베르동 협곡 (Gorges du Verdon)': [
    { type:'spot', name:'Point Sublime', walk:'차로 15분', desc:'베르동 최고 전망 포인트. 에메랄드 협곡 조감 뷰', map:'https://www.google.com/maps/search/Point+Sublime+Gorges+du+Verdon' },
    { type:'spot', name:'Lac de Sainte-Croix', walk:'차로 20분', desc:'청록빛 인공호수. 카약·패들보드 체험 €10~', map:'https://www.google.com/maps/search/Lac+de+Sainte+Croix+Verdon' },
    { type:'meal', name:'Auberge des Cavaliers', walk:'차로 10분', desc:'협곡 입구 오베르주. 프로방스 양고기 & 라벤더 꿀', map:'https://www.google.com/maps/search/Auberge+Gorges+du+Verdon+restaurant' }
  ],
  '생폴드방스 (Saint-Paul-de-Vence)': [
    { type:'spot', name:'Fondation Maeght', walk:'도보 5분', desc:'미로·샤갈·칼더 소장. 현대미술관 €20. 조각 정원 필수', map:'https://www.google.com/maps/search/Fondation+Maeght+Saint-Paul-de-Vence' },
    { type:'cafe', name:'Le Café de la Place', walk:'도보 2분', desc:'마을 광장 카페. 현지인 페탕크 경기 보며 카페오레', map:'https://www.google.com/maps/search/Le+Café+de+la+Place+Saint-Paul-de-Vence' },
    { type:'spot', name:'Remparts de Saint-Paul', walk:'도보 5분', desc:'16세기 성벽 산책로. 알프스·지중해 전망 포토스팟', map:'https://www.google.com/maps/search/Remparts+Saint-Paul-de-Vence' }
  ],
  /* ── DAY 6 코트다쥐르 해안 ── */
  '빌프랑슈쉬르메르': [
    { type:'spot', name:'Chapelle Saint-Pierre', walk:'도보 5분', desc:'장 콕토가 직접 그린 프레스코 예배당. 입장 €3', map:'https://www.google.com/maps/search/Chapelle+Saint+Pierre+Villefranche+sur+Mer' },
    { type:'cafe', name:'La Baleine Joyeuse', walk:'도보 3분', desc:'해변 로컬 카페. 현지인 아침 커피 & 크루아상', map:'https://www.google.com/maps/search/La+Baleine+Joyeuse+Villefranche' },
    { type:'meal', name:'Les Garçons', walk:'도보 2분', desc:'가성비 해안 식당. 니수아즈 샐러드 & 신선 생선 €15', map:'https://www.google.com/maps/search/Les+Garcons+Villefranche+sur+Mer' }
  ],
  '에즈 (Èze)': [
    { type:'spot', name:'Jardin Exotique d\'Eze', walk:'도보 10분', desc:'해발 800m 절벽 선인장 정원. 지중해 360° 뷰. €6', map:'https://www.google.com/maps/search/Jardin+Exotique+Eze+Village' },
    { type:'cafe', name:'Le Nid d\'Aigle', walk:'도보 15분', desc:'마을 최고봉 카페. 지중해·모나코·이탈리아 뷰', map:'https://www.google.com/maps/search/Le+Nid+Aigle+Eze' },
    { type:'spot', name:'Parfumerie Fragonard Eze', walk:'도보 5분', desc:'향수 공장 무료 투어. 코트다쥐르 향수 제조 과정', map:'https://www.google.com/maps/search/Fragonard+Eze+parfumerie' }
  ],
  '망통 (Menton)': [
    { type:'spot', name:'Basilique Saint-Michel', walk:'도보 5분', desc:'이탈리아 바로크 양식 성당. 모자이크 광장 포토', map:'https://www.google.com/maps/search/Basilique+Saint+Michel+Archange+Menton' },
    { type:'cafe', name:'Café du Commerce Menton', walk:'도보 3분', desc:'구시가지 현지인 카페. 레몬 타르트가 이 도시의 명물', map:'https://www.google.com/maps/search/Café+du+Commerce+Menton+old+town' },
    { type:'spot', name:'Promenade du Soleil', walk:'도보 5분', desc:'망통 해안 산책로. 이탈리아 국경 뷰 & 레몬 벽화', map:'https://www.google.com/maps/search/Promenade+du+Soleil+Menton' }
  ],
  /* ── DAY 7 니스 ── */
  '니스 구시가지 (Vieille Ville)': [
    { type:'meal', name:'Chez Acchiardo', walk:'도보 5분', desc:'1927년 5대째 니수아즈 가정식. 라따뚜이·소카 €18', map:'https://www.google.com/maps/search/Chez+Acchiardo+Nice+Vieux' },
    { type:'meal', name:'Lou Pilha Leva', walk:'도보 3분', desc:'Place Centrale 소카·니수아즈 패스트푸드 서서 먹기 €4~', map:'https://www.google.com/maps/search/Lou+Pilha+Leva+Nice' },
    { type:'spot', name:'Chapelle de la Miséricorde', walk:'도보 5분', desc:'니스 바로크 성당. 스투코·금박 내부 장식이 압도적', map:'https://www.google.com/maps/search/Chapelle+de+la+Misericorde+Nice' }
  ],
  '프롬나드 데 장글레': [
    { type:'spot', name:'Plage Beau Rivage (무료해변)', walk:'도보 2분', desc:'무료 공공 자갈해변. 지중해 수영 & 일광욕', map:'https://www.google.com/maps/search/Plage+Beau+Rivage+Nice+public' },
    { type:'cafe', name:'Oui Jelato', walk:'도보 10분', desc:'니스 구시가지 수제 젤라또. 라벤더·피스타치오 추천', map:'https://www.google.com/maps/search/Oui+Jelato+Nice+Vieux' },
    { type:'spot', name:'Musée Masséna (무료)', walk:'도보 5분', desc:'무료 입장 니스 역사박물관. 벨에포크 빌라 & 정원', map:'https://www.google.com/maps/search/Musée+Masséna+Nice' }
  ],
  /* ── DAY 8 니스 ── */
  '살레야 꽃시장 (Cours Saleya)': [
    { type:'meal', name:'Chez Thérésa', walk:'도보 1분', desc:'1925년 소카 원조. 병아리콩 크레페 즉석 구이 €4~', map:'https://www.google.com/maps/search/Chez+Thérésa+Cours+Saleya+Nice' },
    { type:'cafe', name:'Boulangerie Serain Cappa', walk:'도보 5분', desc:'판 바냐·피살라디에르 전문 빵집. 현지인 아침 단골', map:'https://www.google.com/maps/search/Boulangerie+Serain+Cappa+Nice' },
    { type:'spot', name:'Cathédrale Sainte-Réparate', walk:'도보 3분', desc:'니스 수호성인 성당. 살레야 바로 옆 바로크 양식', map:'https://www.google.com/maps/search/Cathédrale+Sainte+Réparate+Nice' }
  ],
  '니스 성곽 공원 (Colline du Château)': [
    { type:'spot', name:'니스 구항구 (Vieux Port)', walk:'도보 10분', desc:'어선 정박 로컬 항구. 일몰 시 황금빛 분위기 최고', map:'https://www.google.com/maps/search/Vieux+Port+Nice+harbour' },
    { type:'meal', name:'Chez Pipo', walk:'도보 15분', desc:'1923년 항구 소카 전문점. 장작화덕 소카+피살라디에르', map:'https://www.google.com/maps/search/Chez+Pipo+Nice+Port' },
    { type:'cafe', name:'Fenocchio', walk:'도보 5분', desc:'1966년 구시가지 젤라또. 94가지 플레이버. 라벤더·올리브', map:'https://www.google.com/maps/search/Fenocchio+Glaces+Nice+Place+Rossetti' }
  ],
  /* ── DAY 9-10 파리 ── */
  '에펠탑 (Tour Eiffel)': [
    { type:'spot', name:'Champ de Mars', walk:'도보 2분', desc:'에펠탑 앞 무료 잔디밭. 피크닉 & 야경 최고 명당', map:'https://www.google.com/maps/search/Champ+de+Mars+Paris' },
    { type:'meal', name:'Le Café du Commerce', walk:'도보 10분', desc:'15구 현지인 전통 브라스리. 스테이크 프리트 €16', map:'https://www.google.com/maps/search/Le+Café+du+Commerce+Paris+15+arrondissement' },
    { type:'cafe', name:'Le Moulin de la Croix Nivert', walk:'도보 8분', desc:'수상경력 크루아상·팡오쇼콜라 빵집. 아침 필수 방문', map:'https://www.google.com/maps/search/Le+Moulin+de+la+Croix+Nivert+Paris+15' }
  ],
  '루브르 박물관 (Musée du Louvre)': [
    { type:'spot', name:'Jardin du Palais Royal', walk:'도보 3분', desc:'무료 왕궁 정원. 부리 콜롱 설치미술 & 아케이드 카페', map:'https://www.google.com/maps/search/Jardin+du+Palais+Royal+Paris' },
    { type:'cafe', name:'Café Verlet', walk:'도보 5분', desc:'1880년 로스터리 카페. 팔레루아얄 옆 싱글오리진 에스프레소', map:'https://www.google.com/maps/search/Café+Verlet+Paris+Rue+Saint-Honoré' },
    { type:'meal', name:'Bouillon Chartier', walk:'도보 15분', desc:'1896년 전통 부이용. 파리지앵 코스 €15~. 웅장한 빈티지 인테리어', map:'https://www.google.com/maps/search/Bouillon+Chartier+Montmartre+Paris' }
  ],
  '콩코르드 광장 → 샹젤리제': [
    { type:'spot', name:'Arc de Triomphe 옥상', walk:'도보 10분', desc:'개선문 옥상 전망대. 샹젤리제 방사형 조감 뷰. €13', map:'https://www.google.com/maps/search/Arc+de+Triomphe+Paris' },
    { type:'spot', name:'Grand Palais', walk:'도보 5분', desc:'아르누보 철·유리 전시궁전. 외관만으로 포토스팟', map:'https://www.google.com/maps/search/Grand+Palais+Paris' },
    { type:'cafe', name:'Ladurée Champs-Élysées', walk:'도보 5분', desc:'마카롱 원조. 장미·라벤더·살구 플레이버. €2.2/개', map:'https://www.google.com/maps/search/Ladurée+Champs+Elysées+Paris' }
  ],
  /* ── DAY 11 파리 ── */
  '몽마르트르 (Montmartre)': [
    { type:'spot', name:'Place du Tertre', walk:'도보 5분', desc:'화가들의 광장. 초상화 즉석 제작 & 거리 예술가', map:'https://www.google.com/maps/search/Place+du+Tertre+Montmartre+Paris' },
    { type:'cafe', name:'Café Lomi', walk:'도보 10분', desc:'원두 직접 로스팅. 현지 커피 애호가 아지트 스페셜티', map:'https://www.google.com/maps/search/Café+Lomi+Paris+Montmartre' },
    { type:'meal', name:'Bouillon Pigalle', walk:'도보 15분', desc:'가성비 최고 프랑스 전통 부이용. 현지인 줄 서도 가치 있음 €15~', map:'https://www.google.com/maps/search/Bouillon+Pigalle+Paris' }
  ],
  '오르세 미술관 or 마레 지구': [
    { type:'cafe', name:'Boot Café', walk:'도보 5분', desc:'전 구두방 개조 미니 카페. 마레 최고 커피 & 미니멀 인테리어', map:'https://www.google.com/maps/search/Boot+Café+Marais+Paris' },
    { type:'spot', name:'Île Saint-Louis', walk:'도보 10분', desc:'파리 속 작은 섬. 베르티용 아이스크림 & 한적한 산책 코스', map:'https://www.google.com/maps/search/Île+Saint-Louis+Paris' },
    { type:'meal', name:'Chez Janou', walk:'도보 8분', desc:'마레 프로방스 비스트로. 압생트 무스 & 올리브 타프나드 €20~', map:'https://www.google.com/maps/search/Chez+Janou+Paris+Marais' }
  ],
  '생제르맹 데 프레': [
    { type:'spot', name:'Jardin du Luxembourg', walk:'도보 10분', desc:'파리 대표 무료 공원. 분수·조각상·체스 테이블 산책', map:'https://www.google.com/maps/search/Jardin+du+Luxembourg+Paris' },
    { type:'cafe', name:'Maison Landemaine', walk:'도보 5분', desc:'수제빵·비에누아즈리 빵집. 현지인이 줄 서는 곳', map:'https://www.google.com/maps/search/Maison+Landemaine+Saint-Germain+Paris' },
    { type:'meal', name:'Les Philosophes', walk:'도보 15분', desc:'마레 코너 테라스 비스트로. 치즈보드·와인 €15~', map:'https://www.google.com/maps/search/Les+Philosophes+Paris+Marais' }
  ]
};
"""

# SCHEDULE_DATA 끝 다음, FOOD_DATA 시작 전에 삽입
html = do(html,
    'const FOOD_DATA = [',
    NEARBY_DATA_JS + 'const FOOD_DATA = [',
    'NEARBY_DATA 삽입')

# ====================================================================
# 2. JS 렌더링: nearby 박스 표시 로직 추가
# ====================================================================
OLD_RENDER_END = """      html += '</div>';
      html += '</div></div>';
    });

    html += '</div>';
    content.innerHTML = html;"""

NEW_RENDER_END = """      html += '</div>';
      // ── 근처 추천 스팟 ──
      var nearbyItems = NEARBY_DATA[item.title] || [];
      if (nearbyItems.length > 0) {
        html += '<div class="nearby-box">';
        html += '<div class="nearby-title">📍 근처 추천 스팟</div>';
        html += '<div class="nearby-list">';
        nearbyItems.forEach(function(n) {
          var nIcon = n.type === \'meal\' ? \'🍽️\' : n.type === \'cafe\' ? \'☕\' : \'🏛️\';
          var nMap = n.map ? \' <a class="map-link" href="\' + n.map + \'" target="_blank" rel="noopener">\' + MAP_SVG + \'</a>\' : \'\';
          html += \'<div>· <strong>\' + n.name + \'</strong>(\' + n.walk + \') — \' + n.desc + nMap + \'</div>\';
        });
        html += '</div></div>';
      }
      html += '</div></div>';
    });

    html += '</div>';
    content.innerHTML = html;"""

html = do(html, OLD_RENDER_END, NEW_RENDER_END, 'nearby 렌더링 JS')

# ====================================================================
# 3. 일정 설명 보강 (key spot 항목들)
# ====================================================================
# 고르드
html = do(html,
    "'고르드 (Gordes)', desc: '프로방스 대표 <strong>절벽 마을</strong>. \"프랑스에서 가장 아름다운 마을\" 선정.'",
    "'고르드 (Gordes)', desc: '프로방스 대표 <strong>절벽 마을</strong>. \"프랑스에서 가장 아름다운 마을\" 선정. 돌담길 & 성 주변 산책. 인근 Abbaye de Sénanque(라벤더 수도원)까지 드라이브 강력 추천.'",
    '고르드 desc 보강')

# 루시용
html = do(html,
    "'루시용 (Roussillon)', desc: '<strong>오렌지빛 절벽</strong> 마을. 오커 채석장 트레일 산책.'",
    "'루시용 (Roussillon)', desc: '<strong>오렌지빛 절벽</strong> 마을. Sentier des Ocres(오커 트레일) 45분 하이킹 필수. 신발이 오커 가루에 물드니 어두운 색 착용 권장.'",
    '루시용 desc 보강')

# 발랑솔
html = do(html,
    "'발랑솔 (Valensole)', desc: '<strong>라벤더 밭</strong> (6월 초 개화 시작). 광활한 보라색 들판 포토.'",
    "'발랑솔 (Valensole)', desc: '<strong>라벤더 밭</strong> (6월 초~중순 개화). 광활한 보라색 들판 포토. 이른 아침 6~8시 방문 시 안개와 라벤더 조합 황금빛 사진 가능.'",
    '발랑솔 desc 보강')

# 베르동 협곡
html = do(html,
    "'베르동 협곡 (Gorges du Verdon)', desc: '유럽의 <strong>그랜드 캐니언</strong>. 에메랄드 빛 협곡 드라이브.'",
    "'베르동 협곡 (Gorges du Verdon)', desc: '유럽의 <strong>그랜드 캐니언</strong>. 에메랄드빛 협곡 드라이브. Corniche Sublime 루트 추천. Point Sublime 전망대 & Lac de Sainte-Croix 카약 체험.'",
    '베르동 desc 보강')

# 생폴드방스
html = do(html,
    "'생폴드방스 (Saint-Paul-de-Vence)', desc: '<strong>중세 예술 마을</strong>. 갤러리 & 아틀리에 산책. 숙박.'",
    "'생폴드방스 (Saint-Paul-de-Vence)', desc: '<strong>중세 예술 마을</strong>. 갤러리 & 아틀리에 산책. Fondation Maeght(현대미술관) 방문 추천. 마을 광장에서 페탕크 경기 구경.'",
    '생폴드방스 desc 보강')

# 에즈
html = do(html,
    "'에즈 (Èze)', desc: '절벽 위 <strong>중세 마을</strong>. 이국적 식물원(Jardin Exotique) 필수 방문.'",
    "'에즈 (Èze)', desc: '해발 427m 절벽 위 <strong>중세 마을</strong>. Jardin Exotique(선인장 정원, €6) 필수. Parfumerie Fragonard 무료 향수 공장 투어. 니체도 걸었던 Le Sentier Friedrich Nietzsche 하이킹로.'",
    '에즈 desc 보강')

# 망통
html = do(html,
    "'망통 (Menton)', desc: '이탈리아 국경 <strong>레몬의 도시</strong>. 컬러풀 구시가지.'",
    "'망통 (Menton)', desc: '이탈리아 국경 <strong>레몬의 도시</strong>. 파스텔 건물이 층층이 쌓인 구시가지. Basilique Saint-Michel 광장 & Promenade du Soleil 해안 산책. 레몬 타르트 꼭 맛볼 것.'",
    '망통 desc 보강')

# 살레야 꽃시장
html = do(html,
    "'살레야 꽃시장 (Cours Saleya)', desc: '니스 <strong>전통 시장</strong>. 꽃, 과일, 올리브, 라벤더 비누.'",
    "'살레야 꽃시장 (Cours Saleya)', desc: '니스 <strong>전통 꽃·먹거리 시장</strong>. 꽃, 과일, 올리브, 라벤더 비누. 시장 내 Chez Thérésa에서 소카 즉석 구이 필수. 오전 7~12시 운영(월 제외).'",
    '살레야 desc 보강')

# 성곽 공원
html = do(html,
    "'니스 성곽 공원 (Colline du Château)', desc: '언덕 공원. <strong>니스 항구 & 해안 파노라마</strong> 뷰.'",
    "'니스 성곽 공원 (Colline du Château)', desc: '해발 92m 언덕 공원. <strong>니스 항구 & 해안 파노라마</strong> 뷰. 엘리베이터 무료(해변 끝 탑승). 대형 인공 폭포도 볼 만함.'",
    '성곽공원 desc 보강')

# 루브르
html = do(html,
    "'루브르 박물관 (Musée du Louvre)', desc: '세계 최대 <strong>미술관</strong>. 모나리자, 밀로의 비너스. <strong>화요일 휴관</strong> 주의.'",
    "'루브르 박물관 (Musée du Louvre)', desc: '세계 최대 <strong>미술관</strong>. 모나리자, 밀로의 비너스, 사모트라케의 니케. <strong>화요일 휴관</strong> 주의. 줄 피하려면 오전 9시 개관 전 도착 or 온라인 사전 예약 필수.'",
    '루브르 desc 보강')

# 몽마르트르
html = do(html,
    "'몽마르트르 (Montmartre)', desc: '<strong>사크레쾨르 성당</strong>. 화가의 거리, 테르트르 광장.'",
    "'몽마르트르 (Montmartre)', desc: '<strong>사크레쾨르 성당</strong> & Place du Tertre 화가의 거리. 테르트르 광장에서 초상화 즉석 제작. 좁은 계단길 & 포도밭(Vigne du Clos Montmartre) 산책 코스.'",
    '몽마르트르 desc 보강')

# ====================================================================
# 4. FOOD_DATA에 새 항목 추가 (]; 바로 앞에 삽입)
# ====================================================================
NEW_FOOD_ITEMS = """  ,
  /* ── 추가 맛집 (중저가 로컬 위주) ── */
  { name: 'Lou Pistou', subName: '루 피스투', region: 'marseille', desc: '르 파니에(Le Panier) 골목의 소박한 프로방스 가정식 식당. 신선 채소 수프 "피스투"와 아욜리(마늘 마요네즈) 소스 요리가 메인. 현지 아주머니 솜씨 그대로.', location: 'Le Panier, Marseille', reco: '수프 오 피스투(Soupe au Pistou), 아욜리 플래터', price: 12, badge: 'badge-local', mapUrl: 'https://www.google.com/maps/search/Lou+Pistou+Marseille+Le+Panier' },
  { name: 'Noailles 파니스', subName: '파니스·소시쏭 길거리', region: 'marseille', desc: '노아이 시장(Marché des Noailles) 주변 길거리음식. 파니스(Panisse: 병아리콩 튀김)는 마르세유 소울푸드. 한 접시 €3~. 시장 골목 탐험과 함께 즐기기.', location: 'Noailles, Marseille', reco: '파니스(Panisse), 피타 케밥, 향신료 시장', price: 3, badge: 'badge-local', mapUrl: 'https://www.google.com/maps/search/Marché+Noailles+Marseille+street+food' },
  { name: 'Lou Pilha Leva', subName: '루 필라 레바', region: 'nice', desc: '니스 구시가지 Place Centrale 중심 광장의 소카·니수아즈 전문 패스트푸드. 긴 테이블에 서서 먹는 현지 스타일. 소카(병아리콩 크레페), 피살라디에르(양파 타르트) 추천.', location: 'Place Centrale, Vieux Nice', reco: '소카(Socca), 피살라디에르(Pissaladière), 토르토니(Tourton)', price: 5, badge: 'badge-must', mapUrl: 'https://www.google.com/maps/search/Lou+Pilha+Leva+Nice' },
  { name: 'René Socca', subName: '르네 소카 (1943년~)', region: 'nice', desc: '1943년 개업. 니스 구시가지 뒷골목 소카 전문점. 화덕에서 막 구운 바삭한 소카를 신문지에 싸서 주는 투박한 스타일. 현지인들이 말하는 "진짜 소카".', location: 'Rue Miralheti, Vieux Nice', reco: '소카(Socca), 니수아즈 피자', price: 6, badge: 'badge-local', mapUrl: 'https://www.google.com/maps/search/René+Socca+Nice+Vieux' },
  { name: 'Bouillon Pigalle', subName: '부이용 피갈 (몽마르트르)', region: 'paris', desc: '몽마르트르 피갈 역 근처 가성비 최고 전통 부이용. 소 골수 카나페, 달팽이 버터구이, 스테이크 프리트 등 정통 파리지앵 요리를 €15 내외에. 웨이팅 있지만 가치 있음.', location: 'Bd de Clichy, 75018 Paris', reco: '소 골수 카나페, 달팽이 버터구이, 크렘 브륄레', price: 15, badge: 'badge-local-rec', mapUrl: 'https://www.google.com/maps/search/Bouillon+Pigalle+Paris+Montmartre' },
  { name: 'Chez Janou', subName: '쉐 자누 (마레)', region: 'paris', desc: '마레 지구 코너 테라스의 프로방스 비스트로. 압생트를 넣은 무스 오 쇼콜라와 올리브 타프나드가 시그니처. 현지인·여행자 모두 즐겨 찾는 아지트 분위기.', location: '2 Rue Roger Verlomme, 75003 Paris', reco: '무스 오 쇼콜라, 올리브 타프나드, 프로방스 양고기', price: 20, badge: 'badge-local', mapUrl: 'https://www.google.com/maps/search/Chez+Janou+Paris+Marais+Rue+Roger+Verlomme' },
  { name: 'Bouillon Chartier', subName: '부이용 샤르티에 (1896년~)', region: 'paris', desc: '1896년 개업. 파리 2구의 전설적 전통 부이용. 웅장한 벨에포크 홀에서 먹는 파리지앵 노동자 요리. 메뉴판이 무려 €12~15. 오전 11시 오픈 전 줄 서는 것 추천.', location: '7 Rue du Fbg Montmartre, 75009 Paris', reco: '소 골수·빵(Os à Moelle), 그라탱 도피누아, 타르트 타탱', price: 14, badge: 'badge-must', mapUrl: 'https://www.google.com/maps/search/Bouillon+Chartier+Paris+Montmartre' },
  { name: 'Les Garçons', subName: '레 가르송 (빌프랑슈)', region: 'cotedazur', desc: '빌프랑슈쉬르메르 해안의 가성비 좋은 캐주얼 레스토랑. 신선한 해산물과 니수아즈 샐러드. 테라스에서 에메랄드빛 만(灣) 뷰와 함께하는 점심이 일품.', location: 'Villefranche-sur-Mer, Côte d\'Azur', reco: '니수아즈 샐러드, 신선 생선 구이, 로제 와인', price: 15, badge: 'badge-local', mapUrl: 'https://www.google.com/maps/search/Les+Garcons+Villefranche+sur+Mer' }"""

# FOOD_DATA 닫는 ]; 바로 앞에 삽입
html = do(html,
    '];\n\nconst CAFE_DATA',
    NEW_FOOD_ITEMS + '\n];\n\nconst CAFE_DATA',
    'FOOD_DATA 새 항목 추가')

# ====================================================================
# 5. CAFE_DATA에 새 항목 추가
# ====================================================================
NEW_CAFE_ITEMS = """  ,
  /* ── 추가 카페·빵집 ── */
  { name: 'Maison Charlie', subName: '메종 샤를리 (마르세유)', region: 'marseille', desc: '마르세유 항구 근처 로컬 베이커리 카페. 포카치나 뒤 주르(오늘의 포카치나)와 진한 핫초코가 시그니처. 별점 4.7, 1000개 이상 리뷰. 현지인 아침 단골.', location: 'Near Vieux Port, Marseille', reco: '포카치나 뒤 주르(Focaccina du Jour), 핫초코(Chocolat Chaud)', price: 4, badge: 'badge-cafe-type', mapUrl: 'https://www.google.com/maps/search/Maison+Charlie+Marseille+bakery' },
  { name: 'Les Navettes des Accoules', subName: '레 나베뜨 데 자쿨', region: 'marseille', desc: '마르세유 전통 과자 나베트(Navette) 원조 빵집. 오렌지꽃 향이 나는 배 모양 비스킷. 이스트 없이 만드는 마르세유 소울 과자. 기념품으로도 제격.', location: 'Le Panier, Marseille', reco: '나베뜨(Navette), 피코(Ficot)', price: 3, badge: 'badge-dessert', mapUrl: 'https://www.google.com/maps/search/Les+Navettes+des+Accoules+Marseille' },
  { name: 'Boot Café', subName: '부트 카페 (마레)', region: 'paris', desc: '마레 지구 Pont aux Choux 거리의 전 구두방(cobbler\'s shop) 개조 미니 카페. 벨빌(Belleville) 원두를 사용하는 스페셜티 커피. 마레에서 가장 힙하고 맛있는 커피로 현지인 추천 1순위.', location: 'Rue du Pont aux Choux, Le Marais, 75003 Paris', reco: '플랫화이트, 에스프레소, 시즌 페이스트리', price: 5, badge: 'badge-cafe-type', mapUrl: 'https://www.google.com/maps/search/Boot+Café+Paris+Marais+Pont+aux+Choux' },
  { name: 'Café Lomi', subName: '카페 로미 (몽마르트르)', region: 'paris', desc: '몽마르트르 피갈 근처 현장 로스팅 스페셜티 카페. 원두를 직접 roasting하며 현지 커피 애호가들의 아지트. 빈티지 창고 인테리어에서 즐기는 핸드드립 & 에스프레소.', location: '3ter Rue Marcadet, 75018 Paris', reco: '싱글오리진 드립, 카푸치노, 수제 케이크', price: 5, badge: 'badge-cafe-type', mapUrl: 'https://www.google.com/maps/search/Café+Lomi+Paris+Montmartre+Marcadet' }"""

html = do(html,
    '];\n\nconst HOTEL_DATA',
    NEW_CAFE_ITEMS + '\n];\n\nconst HOTEL_DATA',
    'CAFE_DATA 새 항목 추가')

# ====================================================================
# 6. 버전 업데이트
# ====================================================================
html = do(html, '프랑스 여행 대시보드 v3.6', '프랑스 여행 대시보드 v3.7', 'footer version')
html = do(html,
    '<!-- v3.6 (2026.03.30)',
    '<!-- v3.7 (2026.03.30) : 목적지별 근처 추천 스팟 추가, 맛집·카페 확장, 일정 설명 보강 -->\n<!-- v3.6 (2026.03.30)',
    'version history')

# ====================================================================
# WRITE
# ====================================================================
with open(DST, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n=== v3.7 생성 완료: {os.path.basename(DST)} ===")
print(f"    파일 크기: {len(html):,} chars")
print(f"    적용된 변경: {changes}개")
