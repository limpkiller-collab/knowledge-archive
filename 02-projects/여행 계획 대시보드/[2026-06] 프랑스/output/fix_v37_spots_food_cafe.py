#!/usr/bin/env python3
"""v3.7 -> v3.8: 맛집/카페 NEARBY 스팟 추가(+5/+9), 관광스팟 탭 신설(35곳), 탭카운트 업데이트"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, '프랑스여행_여행일정대시보드_v3.7_2026.03.30.html')
DST = os.path.join(BASE, '프랑스여행_여행일정대시보드_v3.8_2026.03.30.html')

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

changes = 0

def do(text, old, new, label=""):
    global changes
    if old not in text:
        print(f"  SKIP: {label}")
        return text
    changes += 1
    print(f"  OK: {label}")
    return text.replace(old, new, 1)

# ==== 1. FOOD_DATA: 5개 추가 (맛집 21→26) ====
NEW_FOOD = """,
  /* ── NEARBY 맛집 추가 ── */
  { name: 'Coquille Bistrot Marin', subName: '코킬 비스트로 마랭', region: 'marseille', desc: '마르세유 구항구 바로 앞 현지인 단골 비스트로. 정어리·앤초비 피자와 해산물 스프가 시그니처. 점심 시간 줄 서는 진짜 로컬 맛집.', location: 'Quai du Port, Vieux-Port, Marseille', reco: '정어리 피자, 앤초비 피자, 해산물 수프', price: 15, badge: 'badge-local', mapUrl: 'https://www.google.com/maps/search/Coquille+Bistrot+Marin+Marseille+Vieux+Port', inSchedule: 'DAY 3 근처' },
  { name: 'Le Castrum', subName: '르 카스트룸 (루시용)', region: 'provence', desc: '루시용 오커 절벽 마을의 전망 테라스 레스토랑. 불꽃빛 절벽을 바라보며 즐기는 프로방스 런치. 지역 제철 식재료 활용 일일 특선 메뉴(Plat du Jour).', location: 'Roussillon, Vaucluse, Provence', reco: '프로방스 샐러드, 일일 특선 메뉴(Plat du Jour)', price: 15, badge: 'badge-local', mapUrl: 'https://www.google.com/maps/search/Le+Castrum+Roussillon+Provence', inSchedule: 'DAY 4 근처' },
  { name: 'Auberge des Cavaliers', subName: '오베르주 데 카발리에', region: 'provence', desc: '베르동 협곡 입구 오베르주(시골 여관) 레스토랑. 프로방스산 어린 양고기 구이와 라벤더 꿀 소스가 시그니처. 협곡 드라이브 전후 들르기 좋은 소박한 향토식.', location: 'Route des Gorges du Verdon, Var', reco: '프로방스 양고기 구이, 라벤더 꿀 소스, 로컬 로제 와인', price: 22, badge: 'badge-local-rec', mapUrl: 'https://www.google.com/maps/search/Auberge+Gorges+du+Verdon+restaurant', inSchedule: 'DAY 5 근처' },
  { name: 'Le Café du Commerce', subName: '르 카페 뒤 코메르스 (15구)', region: 'paris', desc: '파리 15구 에펠탑 근처 현지인 전통 브라스리. 넓고 화려하지 않은 공간에서 스테이크 프리트(Steak Frites)를 €16에 즐기는 파리지앵 일상식. 대형 목조 인테리어가 따뜻한 분위기.', location: '51 Rue du Commerce, 75015 Paris', reco: '스테이크 프리트(Steak Frites), 달팽이 버터구이(Escargot)', price: 16, badge: 'badge-local', mapUrl: 'https://www.google.com/maps/search/Le+Café+du+Commerce+Paris+15+arrondissement', inSchedule: 'DAY 9 근처' },
  { name: 'Les Philosophes', subName: '레 필로조프 (마레)', region: 'paris', desc: '파리 마레 지구 코너 테라스의 클래식 비스트로. 치즈보드와 로컬 와인 조합이 압권. 점심 세트 €15~로 합리적이며 생제르맹 주변 산책 후 방문하기 좋음. 테라스 분위기 최고.', location: '28 Rue Vieille du Temple, 75004 Paris', reco: '치즈보드, 로컬 와인, 프랑스 전통 스튜(Pot-au-Feu)', price: 15, badge: 'badge-local', mapUrl: 'https://www.google.com/maps/search/Les+Philosophes+Paris+Marais', inSchedule: 'DAY 11 근처' }"""

html = do(html,
    '];\n\nconst CAFE_DATA',
    NEW_FOOD + '\n];\n\nconst CAFE_DATA',
    'FOOD_DATA 5개 추가')

# ==== 2. CAFE_DATA: 9개 추가 (카페 9→18) ====
NEW_CAFE = """,
  /* ── NEARBY 카페·빵집 추가 ── */
  { name: 'Café Marguerite', subName: '카페 마르게리트 (무스티에)', region: 'provence', desc: '무스티에생트마리 마을 성당 뷰 테라스 유기농 카페. 라벤더 음료, 유기농 타파스, 홈메이드 케이크. 절벽 폭포 소리 들으며 즐기는 힐링 카페.', location: 'Moustiers-Sainte-Marie, Provence', reco: '라벤더 레모네이드, 유기농 타르트, 카페오레', price: 5, badge: 'badge-cafe-type', mapUrl: 'https://www.google.com/maps/search/Café+Marguerite+Moustiers-Sainte-Marie', inSchedule: 'DAY 4 근처' },
  { name: 'Le Café de la Fontaine', subName: '르 카페 드 라 퐁텐 (고르드)', region: 'provence', desc: '고르드 마을 광장 분수 앞 로컬 테라스 카페. 프로방스식 로컬 타르트와 카페오레가 대표 메뉴. 절벽 마을 골목 산책 후 쉬어가기 딱 좋은 곳.', location: 'Gordes, Vaucluse, Provence', reco: '로컬 타르트, 카페오레, 라벤더 아이스크림', price: 4, badge: 'badge-cafe-type', mapUrl: 'https://www.google.com/maps/search/Café+Fontaine+Gordes+village+Provence', inSchedule: 'DAY 4 근처' },
  { name: 'Le Café de la Place', subName: '르 카페 드 라 플라스 (생폴)', region: 'cotedazur', desc: '생폴드방스 마을 광장 앞 카페. 현지인들이 페탕크(쇠공 굴리기) 경기를 하며 카페오레를 즐기는 진짜 프로방스 일상 풍경. 마을 게이트 바로 앞 위치.', location: 'Saint-Paul-de-Vence, Alpes-Maritimes', reco: '카페오레, 밀크피즈, 크루아상', price: 5, badge: 'badge-cafe-type', mapUrl: 'https://www.google.com/maps/search/Le+Café+de+la+Place+Saint-Paul-de-Vence', inSchedule: 'DAY 5 근처' },
  { name: 'La Baleine Joyeuse', subName: '라 발렌 주아이즈 (빌프랑슈)', region: 'cotedazur', desc: '빌프랑슈쉬르메르 항구 앞 해변 로컬 카페. 에메랄드빛 만(灣)을 바라보며 즐기는 아침 크루아상과 에스프레소. 현지인들이 매일 아침 들르는 단골집.', location: 'Villefranche-sur-Mer, Alpes-Maritimes', reco: '에스프레소, 크루아상, 오렌지 주스', price: 4, badge: 'badge-cafe-type', mapUrl: 'https://www.google.com/maps/search/La+Baleine+Joyeuse+Villefranche+sur+Mer', inSchedule: 'DAY 6 근처' },
  { name: 'Café du Commerce Menton', subName: '카페 뒤 코메르스 (망통 구시가)', region: 'cotedazur', desc: '망통 구시가지 현지인 카페. 이 도시 명물인 레몬 타르트(Tarte au Citron)를 꼭 주문해볼 것. 이탈리아 국경 도시 특유의 활기찬 분위기.', location: 'Vieux Menton, Alpes-Maritimes', reco: '레몬 타르트(Tarte au Citron), 에스프레소', price: 4, badge: 'badge-dessert', mapUrl: 'https://www.google.com/maps/search/Café+du+Commerce+Menton+old+town', inSchedule: 'DAY 6 근처' },
  { name: 'Boulangerie Serain Cappa', subName: '불랑주리 세랭 카파 (니스)', region: 'nice', desc: '니스 살레야 꽃시장 근처 현지인 아침 단골 빵집. 판 바냐(Pan Bagnat: 니스식 참치 샌드위치)와 피살라디에르(양파 타르트)가 메인. 8시 오픈 후 빠르게 소진.', location: 'Cours Saleya, Vieux Nice', reco: '판 바냐(Pan Bagnat), 피살라디에르(Pissaladière), 버터 크루아상', price: 3, badge: 'badge-dessert', mapUrl: 'https://www.google.com/maps/search/Boulangerie+Serain+Cappa+Nice', inSchedule: 'DAY 8 근처' },
  { name: 'Fenocchio', subName: '페노키오 (1966년~)', region: 'nice', desc: '1966년 개업한 니스 구시가지 전설의 젤라또. Place Rossetti에서 도보 1분. 무려 94가지 플레이버 중 라벤더·올리브·피스타치오 추천. 현지인도 줄 서는 곳.', location: 'Place Rossetti, Vieux Nice', reco: '라벤더 젤라또, 올리브 젤라또, 피스타치오', price: 3, badge: 'badge-dessert', mapUrl: 'https://www.google.com/maps/search/Fenocchio+Glaces+Nice+Place+Rossetti', inSchedule: 'DAY 8 근처' },
  { name: 'Maison Landemaine', subName: '메종 랑드멘 (생제르맹)', region: 'paris', desc: '파리 생제르맹 데 프레 수제 빵집. 현지인들이 줄 서는 비에누아즈리(버터 페이스트리) 전문점. 크루아상과 팡 오 쇼콜라가 시그니처. 아침 빵 구입 필수 코스.', location: 'Saint-Germain-des-Prés, 75006 Paris', reco: '크루아상, 팡 오 쇼콜라(Pain au Chocolat), 갸또 브르통', price: 5, badge: 'badge-dessert', mapUrl: 'https://www.google.com/maps/search/Maison+Landemaine+Saint-Germain+Paris', inSchedule: 'DAY 11 근처' },
  { name: 'Ladurée Champs-Élysées', subName: '라뒤레 샹젤리제 (마카롱 원조)', region: 'paris', desc: '1862년 창업한 파리 마카롱 원조. 장미·라벤더·살구·피스타치오 플레이버가 시그니처. 샹젤리제 지점은 화려한 인테리어로 경험 자체가 특별. 개당 €2.2~.', location: '75 Av. des Champs-Élysées, 75008 Paris', reco: '로즈 마카롱, 라벤더 마카롱, 피스타치오 마카롱', price: 7, badge: 'badge-dessert', mapUrl: 'https://www.google.com/maps/search/Ladurée+Champs+Elysées+Paris', inSchedule: 'DAY 10 근처' }"""

html = do(html,
    '];\n\nconst HOTEL_DATA = [',
    NEW_CAFE + '\n];\n\nconst HOTEL_DATA = [',
    'CAFE_DATA 9개 추가')

# ==== 3. SPOT_DATA 신설 (35곳) — HOTEL_DATA 앞에 삽입 ====
SPOT_DATA = """
const SPOT_DATA = [
  /* ── 마르세유 ── */
  { name: 'Notre-Dame de la Garde', subName: '노트르담 드 라 가르드', region: 'marseille', desc: '마르세유를 수호하는 언덕 위 네오비잔틴 성당. 도시 전체와 지중해 파노라마 뷰 제공. 마르세유 방문 시 절대 빠질 수 없는 필수 전망대.', location: 'Rue Fort du Sanctuaire, Marseille', admission: '무료(외부) / €2(내부)', badge: 'badge-spot-view', mapUrl: 'https://maps.app.goo.gl/T79dNKbn1gbrVk4D7', inSchedule: 'DAY 3' },
  { name: 'Vieux-Port de Marseille', subName: '마르세유 구항구', region: 'marseille', desc: '2600년 역사의 마르세유 구항구. 매일 아침 어시장이 열리고 지중해를 오가는 페리·보트가 정박. 주변 카페·레스토랑과 함께 산책하기 최고의 장소.', location: 'Vieux-Port, Marseille', admission: '무료', badge: 'badge-spot-view', mapUrl: 'https://maps.app.goo.gl/VUi5DAWGWgnm3bUb8', inSchedule: 'DAY 3' },
  { name: 'Marché des Noailles', subName: '노아이 시장', region: 'marseille', desc: '마르세유 다문화 지역의 활기찬 시장. 향신료·파니스(병아리콩 튀김)·케밥 등 길거리음식 천국. 현지 이민자 문화와 지중해 식재료가 뒤섞인 진짜 마르세유.', location: 'Rue des Noailles, Marseille', admission: '무료', badge: 'badge-spot-market', mapUrl: 'https://www.google.com/maps/search/Marche+Noailles+Marseille' },
  /* ── 프로방스 ── */
  { name: '고르드 (Gordes)', subName: 'Gordes · 프랑스 최아름마을', region: 'provence', desc: '프로방스 대표 절벽 마을. "프랑스에서 가장 아름다운 마을" 중 하나로 선정. 돌담길·성·공방이 가득한 중세 마을. 인근 세낭크 수도원까지 드라이브 강력 추천.', location: 'Gordes, Vaucluse', admission: '무료', badge: 'badge-spot-history', mapUrl: 'https://www.google.com/maps/search/Gordes+France', inSchedule: 'DAY 4' },
  { name: 'Abbaye de Sénanque', subName: '세낭크 수도원 (12세기)', region: 'provence', desc: '12세기 시스터회 수도원. 라벤더 밭 한가운데 자리한 프로방스 최고의 포토스팟. 6월 라벤더 절정 시기에 보라색 물결과 회색 수도원의 조화가 압도적.', location: 'Gordes, Vaucluse (고르드 차로 10분)', admission: '€7(투어) / 외관 무료', badge: 'badge-spot-history', mapUrl: 'https://www.google.com/maps/search/Abbaye+de+Senanque+Gordes' },
  { name: 'Village des Bories', subName: '보리 마을', region: 'provence', desc: '고르드 인근 선사시대 건식석조 돌집 마을. 모르타르 없이 쌓은 독특한 원형·반원형 돌집들이 보존. 역사 마을 자체가 포토스팟. 6월 라벤더 시즌과 최고 궁합.', location: 'Gordes, Vaucluse (고르드 차로 5분)', admission: '€6', badge: 'badge-spot-history', mapUrl: 'https://www.google.com/maps/search/Village+des+Bories+Gordes' },
  { name: '루시용 (Roussillon) 오커 트레일', subName: 'Sentier des Ocres', region: 'provence', desc: '오렌지·빨강빛 오커 절벽 마을. Sentier des Ocres 45분 하이킹 필수. 신발이 오커 가루로 물들 수 있으니 어두운 색 착용 권장. 일몰 직전 빛이 가장 아름다움.', location: 'Roussillon, Vaucluse', admission: '€3(트레일)', badge: 'badge-spot-nature', mapUrl: 'https://www.google.com/maps/search/Sentier+des+Ocres+Roussillon', inSchedule: 'DAY 4' },
  { name: '발랑솔 라벤더 밭 (Valensole)', subName: '6월 라벤더 절정', region: 'provence', desc: '6월 초중순 라벤더 절정. 보라색 광활한 들판이 지평선까지 펼쳐지는 프로방스 최고의 포토스팟. 이른 아침 6~8시 방문 시 안개와 라벤더 황금빛 사진 가능.', location: 'Valensole, Alpes-de-Haute-Provence', admission: '무료', badge: 'badge-spot-nature', mapUrl: 'https://www.google.com/maps/search/Valensole+lavender+field', inSchedule: 'DAY 4' },
  { name: '무스티에생트마리', subName: 'Moustiers-Sainte-Marie', region: 'provence', desc: '절벽 사이 별 전설이 있는 프로방스 도예마을. 중세 마을 골목 & 도자기 공방 구경. Notre-Dame de Beauvoir 성당까지 258계단 트레킹 후 파노라마 뷰가 최고.', location: 'Moustiers-Sainte-Marie, Provence', admission: '무료', badge: 'badge-spot-history', mapUrl: 'https://www.google.com/maps/search/Moustiers-Sainte-Marie+France', inSchedule: 'DAY 4/5' },
  { name: '베르동 협곡 (Gorges du Verdon)', subName: '유럽의 그랜드 캐니언', region: 'provence', desc: '유럽의 그랜드 캐니언. 에메랄드빛 협곡 드라이브 코스. Corniche Sublime 루트 추천. Point Sublime 전망대에서 압도적인 뷰. Lac de Sainte-Croix 카약·패들보드 €10~.', location: 'Gorges du Verdon, Var/Alpes-de-Haute-Provence', admission: '무료(드라이브) / €10~(카약)', badge: 'badge-spot-nature', mapUrl: 'https://www.google.com/maps/search/Gorges+du+Verdon', inSchedule: 'DAY 5' },
  { name: 'Lac de Sainte-Croix', subName: '생트크루아 호수', region: 'provence', desc: '베르동 협곡 인근 청록빛 인공호수. 패들보드·카약 체험 €10~. 여름 수영 포인트. 협곡 색깔과 호수 에메랄드빛의 조화가 사진빨 최고.', location: 'Sainte-Croix-de-Verdon, Var', admission: '무료(수영) / €10~(카약체험)', badge: 'badge-spot-nature', mapUrl: 'https://www.google.com/maps/search/Lac+de+Sainte+Croix+Verdon' },
  /* ── 코트다쥐르 ── */
  { name: 'Fondation Maeght', subName: '폰다시옹 마에그 (현대미술관)', region: 'cotedazur', desc: '미로·샤갈·칼더 작품을 소장한 사립 현대미술관. 조각 정원 & 야외 설치미술 필수 관람. 생폴드방스 마을 바로 위. 미술관 자체가 건축예술 작품.', location: 'Saint-Paul-de-Vence, Alpes-Maritimes', admission: '€20', badge: 'badge-spot-art', mapUrl: 'https://www.google.com/maps/search/Fondation+Maeght+Saint-Paul-de-Vence', inSchedule: 'DAY 5 근처' },
  { name: '생폴드방스 성벽 (Remparts)', subName: '16세기 성곽 산책로', region: 'cotedazur', desc: '16세기 군사 성벽 위 산책로. 알프스와 지중해가 동시에 보이는 전망 포토스팟. 마을을 한 바퀴 도는 성벽 투어는 약 20분. 성벽 위 꽃장식이 아름다움.', location: 'Saint-Paul-de-Vence, Alpes-Maritimes', admission: '무료', badge: 'badge-spot-view', mapUrl: 'https://www.google.com/maps/search/Remparts+Saint-Paul-de-Vence' },
  { name: 'Chapelle Saint-Pierre', subName: '생피에르 예배당 (장 콕토)', region: 'cotedazur', desc: '빌프랑슈쉬르메르 항구 앞 예배당. 시인·화가 장 콕토가 1957년 직접 그린 어민들을 위한 프레스코화로 가득. 작은 공간이지만 예술적 가치 충분. 입장 €3.', location: 'Quai Courbet, Villefranche-sur-Mer', admission: '€3', badge: 'badge-spot-history', mapUrl: 'https://www.google.com/maps/search/Chapelle+Saint+Pierre+Villefranche+sur+Mer', inSchedule: 'DAY 6 근처' },
  { name: 'Jardin Exotique d\\'Eze', subName: '에즈 선인장 정원', region: 'cotedazur', desc: '해발 800m 절벽 마을 꼭대기 이국적 선인장 정원. 지중해·모나코·이탈리아까지 360° 파노라마 뷰. 니체가 산책했던 Le Sentier Nietzsche 하이킹 코스 시작점.', location: 'Rue du Château, Eze Village', admission: '€6', badge: 'badge-spot-nature', mapUrl: 'https://www.google.com/maps/search/Jardin+Exotique+Eze+Village', inSchedule: 'DAY 6' },
  { name: 'Parfumerie Fragonard (에즈)', subName: '프라고나르 향수 공장', region: 'cotedazur', desc: '코트다쥐르 향수 제조의 역사를 볼 수 있는 향수 공장. 무료 가이드 투어로 향수 제조 과정 체험. 기념품 쇼핑도 가능. 에즈 마을 하산 중 들르기 좋음.', location: 'Eze Village, Alpes-Maritimes', admission: '무료(투어)', badge: 'badge-spot-free', mapUrl: 'https://www.google.com/maps/search/Fragonard+Eze+parfumerie', inSchedule: 'DAY 6 근처' },
  { name: 'Basilique Saint-Michel (망통)', subName: '바질리크 생미셸 (이탈리아 바로크)', region: 'cotedazur', desc: '이탈리아 바로크 양식의 망통 대성당. 앞 광장에는 화려한 모자이크 타일 바닥이 포토스팟. 이탈리아 국경 도시답게 이탈리아 건축 영향이 짙음.', location: 'Place de l\'Eglise, Vieux Menton', admission: '무료', badge: 'badge-spot-history', mapUrl: 'https://www.google.com/maps/search/Basilique+Saint+Michel+Archange+Menton', inSchedule: 'DAY 6' },
  { name: 'Promenade du Soleil (망통)', subName: '망통 해안 산책로', region: 'cotedazur', desc: '망통 해안 산책로. 이탈리아 국경 바로 옆까지 걸어서 이동 가능. 레몬 테마 벽화와 파스텔 건물 배경 포토 추천. 망통의 구시가지와 해변을 연결하는 코스.', location: 'Promenade du Soleil, Menton', admission: '무료', badge: 'badge-spot-nature', mapUrl: 'https://www.google.com/maps/search/Promenade+du+Soleil+Menton', inSchedule: 'DAY 6 근처' },
  /* ── 니스 ── */
  { name: '살레야 꽃시장 (Cours Saleya)', subName: '니스 전통 꽃·먹거리 시장', region: 'nice', desc: '니스 구시가지 전통 꽃·과일·먹거리 시장. 오전 7~12시 운영(월 제외). 꽃, 과일, 올리브, 라벤더 비누. 시장 내 Chez Thérésa에서 소카 즉석 구이 필수.', location: 'Cours Saleya, Vieux Nice', admission: '무료', badge: 'badge-spot-market', mapUrl: 'https://www.google.com/maps/search/Cours+Saleya+Nice', inSchedule: 'DAY 8' },
  { name: 'Colline du Château (니스 성곽)', subName: '해발 92m 언덕 공원', region: 'nice', desc: '해발 92m 언덕 공원. 니스 구항구·구시가지·프롬나드 해안 파노라마 뷰. 엘리베이터 무료(해변 끝 탑승) 또는 계단 등반. 대형 인공 폭포와 전망 테라스가 인상적.', location: 'Colline du Château, Nice', admission: '무료', badge: 'badge-spot-view', mapUrl: 'https://www.google.com/maps/search/Colline+du+Chateau+Nice', inSchedule: 'DAY 8' },
  { name: 'Chapelle de la Miséricorde', subName: '미제리코르드 예배당', region: 'nice', desc: '니스 구시가지 바로크 양식 예배당. 황금빛 스투코와 금박 내부 장식이 압도적. 규모는 작지만 단위 면적당 화려함 1위. 살레야 시장에서 도보 3분.', location: 'Cours Saleya, Vieux Nice', admission: '무료', badge: 'badge-spot-history', mapUrl: 'https://www.google.com/maps/search/Chapelle+de+la+Misericorde+Nice' },
  { name: 'Plage Beau Rivage (무료해변)', subName: '니스 지중해 자갈해변', region: 'nice', desc: '지중해 자갈해변. 무료 공공해변으로 수영·일광욕 가능. 프롬나드 데 장글레 인접. 지중해 특유의 청록색 바다에서 수영하는 경험. 선베드 유료(€20~).', location: 'Promenade des Anglais, Nice', admission: '무료(해변) / €20~(선베드)', badge: 'badge-spot-free', mapUrl: 'https://www.google.com/maps/search/Plage+Beau+Rivage+Nice+public', inSchedule: 'DAY 7 근처' },
  { name: 'Musée Masséna (무료)', subName: '마세나 박물관', region: 'nice', desc: '무료 입장 니스 역사박물관. 벨에포크 스타일 빌라와 지중해 정원. 니스의 역사와 문화를 담은 전시. 프롬나드 데 장글레 옆에 위치해 접근성 최고.', location: 'Promenade des Anglais, 65 Rue de France, Nice', admission: '무료', badge: 'badge-spot-free', mapUrl: 'https://www.google.com/maps/search/Musée+Masséna+Nice', inSchedule: 'DAY 7 근처' },
  { name: '니스 구항구 (Vieux Port Nice)', subName: '어선 정박 로컬 항구', region: 'nice', desc: '어선이 정박한 니스 로컬 항구. 성곽 공원 아래 위치. 일몰 시 황금빛 분위기가 최고. 주변에 소카 전문점(Chez Pipo)과 카페들이 몰려 있어 식사하기도 좋음.', location: 'Port Lympia, Nice', admission: '무료', badge: 'badge-spot-view', mapUrl: 'https://www.google.com/maps/search/Vieux+Port+Nice+harbour', inSchedule: 'DAY 8 근처' },
  /* ── 파리 ── */
  { name: 'Champ de Mars', subName: '샹 드 마르스 공원', region: 'paris', desc: '에펠탑 앞 무료 공원. 피크닉 명당으로 낮에는 잔디밭에서 여유, 저녁에는 에펠탑 야경 감상. 매시 정각 5분간 반짝이는 에펠탑 조명 쇼는 꼭 볼 것.', location: 'Champ de Mars, 75007 Paris', admission: '무료', badge: 'badge-spot-free', mapUrl: 'https://www.google.com/maps/search/Champ+de+Mars+Paris', inSchedule: 'DAY 9 근처' },
  { name: 'Musée du Louvre', subName: '루브르 박물관', region: 'paris', desc: '세계 최대 미술관. 모나리자·밀로의 비너스·사모트라케의 니케. 화요일 휴관 주의. 줄 피하려면 오전 9시 개관 전 도착 또는 온라인 사전 예약 필수.', location: 'Rue de Rivoli, 75001 Paris', admission: '€17', badge: 'badge-spot-art', mapUrl: 'https://www.google.com/maps/search/Musee+du+Louvre+Paris', inSchedule: 'DAY 10' },
  { name: 'Jardin des Tuileries', subName: '튈르리 정원', region: 'paris', desc: '루브르~콩코르드 광장을 잇는 프랑스식 정원. 조각상과 연못, 카페가 배치된 산책 코스. 콩코르드 쪽 끝에는 개선문 방향 샹젤리제 뷰도 가능.', location: 'Jardin des Tuileries, 75001 Paris', admission: '무료', badge: 'badge-spot-free', mapUrl: 'https://www.google.com/maps/search/Jardin+des+Tuileries+Paris', inSchedule: 'DAY 10' },
  { name: 'Jardin du Palais Royal', subName: '팔레루아얄 정원', region: 'paris', desc: '무료 왕궁 정원. 다니엘 뷔랑의 흑백 줄무늬 기둥 설치미술(Colonnes de Buren)이 포토스팟. 아케이드를 따라 갤러리·카페·레스토랑이 늘어선 세련된 공간.', location: 'Place du Palais Royal, 75001 Paris', admission: '무료', badge: 'badge-spot-free', mapUrl: 'https://www.google.com/maps/search/Jardin+du+Palais+Royal+Paris', inSchedule: 'DAY 10 근처' },
  { name: 'Arc de Triomphe (개선문)', subName: '옥상 전망대 · €13', region: 'paris', desc: '나폴레옹이 건설한 개선문. 옥상 전망대에서 샹젤리제~에펠탑까지 방사형 거리 조감 뷰. 전망 자체로는 에펠탑 2층보다 가성비가 좋음. 지하도로 안전하게 접근.', location: 'Place Charles de Gaulle, 75008 Paris', admission: '€13', badge: 'badge-spot-view', mapUrl: 'https://www.google.com/maps/search/Arc+de+Triomphe+Paris', inSchedule: 'DAY 10' },
  { name: 'Sacré-Cœur (사크레쾨르)', subName: '몽마르트르 언덕 성당', region: 'paris', desc: '몽마르트르 언덕 꼭대기 흰색 성당. 돔 옥상에서 파리 전체 파노라마 가능. 좁은 계단 골목·포도밭(6월 미개방)·Place du Tertre 화가 광장과 함께 반나절 코스.', location: 'Parvis du Sacré-Cœur, 75018 Paris', admission: '무료(성당) / €8(돔)', badge: 'badge-spot-history', mapUrl: 'https://www.google.com/maps/search/Sacre+Coeur+Montmartre+Paris', inSchedule: 'DAY 11' },
  { name: 'Place du Tertre', subName: '화가들의 광장 (몽마르트르)', region: 'paris', desc: '몽마르트르 화가들의 광장. 초상화 즉석 제작 & 거리 예술가들의 아지트. 사크레쾨르 옆 공간. 관광지화됐지만 파리 예술 에너지를 느끼기 좋음.', location: 'Place du Tertre, Montmartre, 75018 Paris', admission: '무료', badge: 'badge-spot-market', mapUrl: 'https://www.google.com/maps/search/Place+du+Tertre+Montmartre+Paris', inSchedule: 'DAY 11 근처' },
  { name: 'Musée d\\'Orsay', subName: '오르세 미술관', region: 'paris', desc: '인상파·후기인상파 미술관. 모네·르누아르·반 고흐·세잔 원화. 구 기차역 건물 개조. 목요일 야간 개방(~21:45). 루브르보다 대기 짧고 개인적으로 더 감동적.', location: 'Esplanade Valéry Giscard d\\'Estaing, 75007 Paris', admission: '€16', badge: 'badge-spot-art', mapUrl: 'https://www.google.com/maps/search/Musee+Orsay+Paris', inSchedule: 'DAY 11' },
  { name: 'Jardin du Luxembourg', subName: '뤽상부르 정원', region: 'paris', desc: '파리 대표 무료 공원. 분수·조각상·야외 체스 테이블. 봄~여름 야외 카페와 좌석 대여. 생제르맹 데 프레 산책과 연계하기 좋음. 현지인 산책·조깅 명소.', location: 'Rue de Médicis, 75006 Paris', admission: '무료', badge: 'badge-spot-free', mapUrl: 'https://www.google.com/maps/search/Jardin+du+Luxembourg+Paris', inSchedule: 'DAY 11 근처' }
];

"""

html = do(html,
    '\nconst HOTEL_DATA = [',
    SPOT_DATA + 'const HOTEL_DATA = [',
    'SPOT_DATA 신설')

# ==== 4. 탭 버튼: 카운트 업데이트 + 관광스팟 탭 추가 ====
html = do(html,
    """  <button class="main-tab" onclick="showPanel('food')">🍜 맛집 <span>(14)</span></button>
  <button class="main-tab" onclick="showPanel('cafe')">☕ 카페 <span>(5)</span></button>
  <button class="main-tab" onclick="showPanel('hotel')">🏨 숙소</button>""",
    """  <button class="main-tab" onclick="showPanel('food')">🍜 맛집 <span>(26)</span></button>
  <button class="main-tab" onclick="showPanel('cafe')">☕ 카페 <span>(18)</span></button>
  <button class="main-tab" onclick="showPanel('spot')">🗺️ 관광스팟</button>
  <button class="main-tab" onclick="showPanel('hotel')">🏨 숙소</button>""",
    '탭 버튼 업데이트 + 관광스팟 추가')

# ==== 5. 패널 HTML: panel-spot 추가 (panel-cafe 뒤, panel-hotel 앞) ====
html = do(html,
    '<!-- ===== HOTEL PANEL ===== -->',
    """<!-- ===== SPOT PANEL ===== -->
<style>
.badge-spot-view { background: rgba(59,130,246,0.15); color:#3b82f6; }
.badge-spot-art { background: rgba(139,92,246,0.15); color:#8b5cf6; }
.badge-spot-history { background: rgba(245,158,11,0.15); color:#d97706; }
.badge-spot-nature { background: rgba(16,185,129,0.15); color:#10b981; }
.badge-spot-market { background: rgba(236,72,153,0.15); color:#ec4899; }
.badge-spot-free { background: rgba(16,185,129,0.1); color:#059669; }
</style>
<div class="main-panel" id="panel-spot">
  <h2 style="font-size:22px; margin-bottom:8px;">프랑스 관광스팟</h2>
  <p class="text-secondary" style="font-size:13px; margin-bottom:16px;">5개 지역별 관광명소 · 자연 · 무료입장 포함 총 35곳</p>
  <div class="region-filters" id="spot-filters"></div>
  <div id="spot-list"></div>
</div>

<!-- ===== HOTEL PANEL ===== -->""",
    'panel-spot HTML 삽입')

# ==== 6. getBadgeLabel에 관광스팟 배지 레이블 추가 ====
html = do(html,
    "    'badge-view': '뷰'\n  };\n  return labels[badgeClass] || '추천';",
    "    'badge-view': '뷰',\n    'badge-spot-view': '뷰포인트',\n    'badge-spot-art': '미술·갤러리',\n    'badge-spot-history': '역사유적',\n    'badge-spot-nature': '자연',\n    'badge-spot-market': '시장',\n    'badge-spot-free': '무료입장'\n  };\n  return labels[badgeClass] || '추천';",
    'getBadgeLabel 스팟 배지 추가')

# ==== 7. renderSpotPanel() + filterSpot() 추가 (getBadgeLabel 앞) ====
RENDER_SPOT_JS = """// ===== SPOT PANEL =====
function renderSpotPanel() {
  var MAP_SVG = '<svg class="map-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>';
  const filterContainer = document.getElementById('spot-filters');
  const listContainer = document.getElementById('spot-list');

  // Filters
  filterContainer.innerHTML = `
    <button class="region-btn active" onclick="filterSpot('all')">전체 <span class="region-count">${SPOT_DATA.length}</span></button>
  `;

  Object.entries(REGIONS).forEach(([key, region]) => {
    const count = SPOT_DATA.filter(s => s.region === key).length;
    if (count > 0) {
      filterContainer.innerHTML += `
        <button class="region-btn" onclick="filterSpot('${key}')">${region.emoji} ${region.name} <span class="region-count">${count}</span></button>
      `;
    }
  });

  // List
  listContainer.innerHTML = '';
  Object.entries(REGIONS).forEach(([key, region]) => {
    const items = SPOT_DATA.filter(s => s.region === key);
    if (items.length === 0) return;

    let html = `
      <div class="region-section" data-region="${key}">
        <div class="region-section-title"><span class="region-emoji">${region.emoji}</span> ${region.name}</div>
        <div class="list-grid">
    `;

    items.forEach(item => {
      var mapLink = item.mapUrl
        ? '<a class="map-link" href="' + item.mapUrl + '" target="_blank" rel="noopener">' + MAP_SVG + '구글지도</a>'
        : '';
      var scheduleTag = item.inSchedule
        ? '<div class="in-schedule">📌 ' + item.inSchedule + ' 포함</div>'
        : '';
      var admissionStr = item.admission || '현장 확인';
      html += `
        <div class="list-card">
          <div class="list-card-header"><div><h3>${item.name}</h3>${item.subName ? '<div class="cn-name">' + item.subName + '</div>' : ''}</div><span class="badge-type ${item.badge}">${getBadgeLabel(item.badge)}</span></div>
          <div class="list-desc">${item.desc}</div>
          <div class="address">${item.location}</div>
          <div class="list-meta"><span class="price">입장: ${admissionStr}</span>${mapLink}</div>
          ${scheduleTag}
        </div>
      `;
    });

    html += '</div></div>';
    listContainer.innerHTML += html;
  });
}

function filterSpot(regionKey) {
  const buttons = document.querySelectorAll('#spot-filters .region-btn');
  buttons.forEach((btn, idx) => {
    if ((regionKey === 'all' && idx === 0) || btn.textContent.includes(REGIONS[regionKey]?.name)) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });

  const sections = document.querySelectorAll('#spot-list .region-section');
  sections.forEach(section => {
    if (regionKey === 'all') {
      section.style.display = 'block';
    } else {
      section.style.display = section.dataset.region === regionKey ? 'block' : 'none';
    }
  });
}

"""

html = do(html,
    'function getBadgeLabel(badgeClass) {',
    RENDER_SPOT_JS + 'function getBadgeLabel(badgeClass) {',
    'renderSpotPanel + filterSpot 함수 삽입')

# ==== 8. DOMContentLoaded init에 renderSpotPanel() 추가 ====
html = do(html,
    '  renderCafePanel();\n  renderHotelPanel();',
    '  renderCafePanel();\n  renderSpotPanel();\n  renderHotelPanel();',
    'DOMContentLoaded renderSpotPanel 추가')

# ==== 9. KPI 카드 맛집/카페 수 업데이트 ====
html = do(html,
    '<span class="kpi-value">14 / 5곳</span>',
    '<span class="kpi-value">26 / 18곳</span>',
    'KPI 카드 맛집/카페 수')

# ==== 10. 맛집 패널 소제목 업데이트 ====
html = do(html,
    '5개 지역별 14곳의 맛집. 현지인 추천 위주로 선정했습니다.',
    '5개 지역별 26곳의 맛집. 현지인 추천 & NEARBY 스팟 위주로 선정했습니다.',
    '맛집 패널 소제목')

# ==== 11. 카페 패널 소제목 업데이트 ====
html = do(html,
    '니스·파리 지역 카페 5곳. 로컬 명소 위주.',
    '5개 지역별 카페·빵집 18곳. 로컬 명소 & 현지인 단골 위주.',
    '카페 패널 소제목')

# ==== 12. 버전 히스토리 업데이트 ====
html = do(html,
    '<!-- Version History (최신순) -->\n<!-- v3.7',
    '<!-- Version History (최신순) -->\n<!-- v3.8 (2026.03.30) : 맛집 +5(NEARBY) → 26곳, 카페 +9(NEARBY) → 18곳, 관광스팟 탭 신설 35곳 -->\n<!-- v3.7',
    '버전 히스토리')

html = do(html,
    '프랑스 여행 대시보드 v3.7',
    '프랑스 여행 대시보드 v3.8',
    '푸터 버전')

# ==== WRITE ====
with open(DST, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n=== v3.8 generated: {os.path.basename(DST)} ===")
print(f"    File size: {len(html):,} chars")
print(f"    Changes applied: {changes}")
