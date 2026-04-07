#!/usr/bin/env python3
"""v3.3 → v3.4: Hotel CRUD ⋮ button + Food/Cafe Taichung-style cards"""

import os

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, '프랑스여행_여행일정대시보드_v3.3_2026.03.30.html')
DST = os.path.join(BASE, '프랑스여행_여행일정대시보드_v3.4_2026.03.30.html')

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

# ============================================================
# 1. UPDATE FOOD_DATA with enriched descriptions, mapUrl, subName, inSchedule
# ============================================================
OLD_FOOD_DATA = """const FOOD_DATA = [
  { name: 'Chez Étienne', region: 'marseille', desc: '피자/부야베스', location: '르 파니에 지구', reco: '피자, 부야베스', price: 15, badge: 'badge-local' },
  { name: 'La Boîte à Sardine', region: 'marseille', desc: '해산물', location: '숨겨진 보석', reco: '정어리 요리, 해산물 플래터', price: 20, badge: 'badge-local-rec' },
  { name: 'Restaurant Gérard', region: 'marseille', desc: '유기농 프로방스', location: '쿠르줄리앙', reco: '제철 채소 요리', price: 18, badge: 'badge-local' },
  { name: 'La Cantinetta', region: 'marseille', desc: '이탈리안', location: '쿠르줄리앙', reco: '파스타, 안티파스토', price: 15, badge: 'badge-local' },
  { name: 'La Cantine', region: 'provence', desc: '프로방스 가정식', location: '무스티에생트마리', reco: '제철 프로방스 요리', price: 20, badge: 'badge-local' },
  { name: 'Le Couvert', region: 'provence', desc: '현지 특산물', location: '무스티에생트마리', reco: '올리브 타프나드, 치즈', price: 22, badge: 'badge-local-rec' },
  { name: 'Le Caruso', region: 'cotedazur', desc: '프렌치 전통', location: '생폴드방스 구시가지', reco: '지중해 요리, 와인', price: 25, badge: 'badge-local' },
  { name: 'Chez Thérésa', region: 'nice', desc: '소카 전문', location: '쿠르살레야 시장 (1925년~)', reco: '소카, 파리나타', price: 8, badge: 'badge-must' },
  { name: 'Chez Pipo', region: 'nice', desc: '소카', location: '니스 항구 (1923년~)', reco: '소카, 피사라디에르', price: 10, badge: 'badge-local' },
  { name: 'Chez Acchiardo', region: 'nice', desc: '니스 가정식', location: '구시가지 (1927년~, 5대째)', reco: '라타투이, 니수아즈', price: 18, badge: 'badge-local-rec' },
  { name: 'La Maison de Marie', region: 'nice', desc: '숨겨진 비스트로', location: '안뜰 테라스', reco: '프렌치 비스트로 런치', price: 22, badge: 'badge-local' },
  { name: 'Petit Vendôme', region: 'paris', desc: '잠봉뵈르', location: '2구', reco: '잠봉뵈르 샌드위치', price: 8, badge: 'badge-must' },
  { name: 'Le Moulin de la Croix Nivert', region: 'paris', desc: '빵집/크루아상', location: '15구 에펠탑 근처', reco: '크루아상, 비에누아즈리', price: 5, badge: 'badge-local-rec' }
];"""

NEW_FOOD_DATA = """const FOOD_DATA = [
  { name: 'Chez Étienne', subName: 'シェ・エティエンヌ', region: 'marseille', desc: '마르세유 구시가지(르 파니에) 골목 안 전설적 피자집. 장작 화덕 피자와 진한 부야베스가 유명. 현지인 줄 서는 곳.', location: 'Rue de Lorette, Le Panier, Marseille', reco: '장작 화덕 피자, 부야베스(Bouillabaisse)', price: 15, badge: 'badge-local', mapUrl: 'https://www.google.com/maps/search/Chez+Étienne+Marseille+Le+Panier', inSchedule: 'DAY 2' },
  { name: 'La Boîte à Sardine', subName: '라 부아뜨 아 사르딘', region: 'marseille', desc: '마르세유 항구 근처 해산물 비스트로. 신선한 정어리 요리와 해산물 플래터가 시그니처. 숨겨진 보석 같은 곳.', location: 'Bd de la Libération, Marseille', reco: '정어리 구이, 해산물 플래터, 부야베스', price: 20, badge: 'badge-local-rec', mapUrl: 'https://www.google.com/maps/search/La+Boîte+à+Sardine+Marseille' },
  { name: 'Restaurant Gérard', subName: '레스토랑 제라르', region: 'marseille', desc: '쿠르줄리앙(Cours Julien) 지역 유기농 프로방스 레스토랑. 지중해 제철 채소와 허브를 활용한 건강한 요리.', location: 'Cours Julien, Marseille', reco: '제철 채소 요리, 프로방스 허브 샐러드', price: 18, badge: 'badge-local', mapUrl: 'https://www.google.com/maps/search/Restaurant+Gérard+Cours+Julien+Marseille' },
  { name: 'La Cantinetta', subName: '라 캉티네따', region: 'marseille', desc: '마르세유 쿠르줄리앙의 인기 이탈리안 레스토랑. 수제 파스타와 안티파스토가 훌륭. 테라스 좌석 추천.', location: 'Cours Julien, Marseille', reco: '수제 파스타, 안티파스토, 티라미수', price: 15, badge: 'badge-local', mapUrl: 'https://www.google.com/maps/search/La+Cantinetta+Marseille+Cours+Julien' },
  { name: 'La Cantine', subName: '라 캉틴', region: 'provence', desc: '무스티에생트마리 마을의 프로방스 가정식 레스토랑. 라벤더향 가득한 마을에서 즐기는 소박한 향토 요리.', location: 'Moustiers-Sainte-Marie, Provence', reco: '프로방스 제철 요리, 라따뚜이', price: 20, badge: 'badge-local', mapUrl: 'https://www.google.com/maps/search/La+Cantine+Moustiers-Sainte-Marie', inSchedule: 'DAY 4' },
  { name: 'Le Couvert', subName: '르 쿠베르', region: 'provence', desc: '무스티에생트마리의 현지 특산물 전문점. 프로방스산 올리브, 타프나드, 치즈 등을 맛볼 수 있는 델리.', location: 'Moustiers-Sainte-Marie, Provence', reco: '올리브 타프나드, 염소치즈, 로컬 와인', price: 22, badge: 'badge-local-rec', mapUrl: 'https://www.google.com/maps/search/Le+Couvert+Moustiers-Sainte-Marie' },
  { name: 'Le Caruso', subName: '르 카루소', region: 'cotedazur', desc: '중세마을 생폴드방스(Saint-Paul-de-Vence) 구시가지 내 프렌치 전통 레스토랑. 지중해 뷰와 함께하는 식사.', location: 'Rue Grande, Saint-Paul-de-Vence', reco: '지중해 요리, 프로방스 와인', price: 25, badge: 'badge-local', mapUrl: 'https://www.google.com/maps/search/Le+Caruso+Saint-Paul-de-Vence', inSchedule: 'DAY 6' },
  { name: 'Chez Thérésa', subName: 'シェ・テレサ (1925년~)', region: 'nice', desc: '1925년부터 쿠르살레야(Cours Saleya) 꽃시장에서 소카(Socca)를 구워온 <strong>니스 소카 원조</strong>. 병아리콩 반죽 크레페.', location: 'Cours Saleya, Nice Old Town', reco: '소카(Socca), 파리나타(Farinata)', price: 8, badge: 'badge-must', mapUrl: 'https://www.google.com/maps/search/Chez+Thérésa+Cours+Saleya+Nice', inSchedule: 'DAY 8' },
  { name: 'Chez Pipo', subName: 'シェ・ピポ (1923년~)', region: 'nice', desc: '1923년 개업한 니스 항구 근처 소카 전문점. 100년 역사의 장작 화덕에서 구워내는 바삭한 소카가 대표 메뉴.', location: '13 Rue Bavastro, Nice Port', reco: '소카(Socca), 피사라디에르(Pissaladière)', price: 10, badge: 'badge-local', mapUrl: 'https://www.google.com/maps/search/Chez+Pipo+Nice+Port', inSchedule: 'DAY 9' },
  { name: 'Chez Acchiardo', subName: 'シェ・アッキアルド (1927년~, 5대째)', region: 'nice', desc: '1927년부터 5대째 이어온 구시가지 니스 가정식 레스토랑. 진정한 <strong>니수아즈 퀴진</strong>을 맛볼 수 있는 현지인 성지.', location: '38 Rue Droite, Vieux Nice', reco: '라타투이(Ratatouille), 니수아즈 샐러드', price: 18, badge: 'badge-local-rec', mapUrl: 'https://www.google.com/maps/search/Chez+Acchiardo+Nice+Vieux' },
  { name: 'La Maison de Marie', subName: '라 메종 드 마리', region: 'nice', desc: '니스 구시가지 숨겨진 안뜰(Courtyard)의 프렌치 비스트로. 고즈넉한 테라스에서 즐기는 프로방스 런치 세트.', location: '5 Rue Masséna, Nice', reco: '프렌치 비스트로 런치 세트, 디저트', price: 22, badge: 'badge-local', mapUrl: 'https://www.google.com/maps/search/La+Maison+de+Marie+Nice' },
  { name: 'Petit Vendôme', subName: '쁘띠 방돔', region: 'paris', desc: '파리 2구의 전설적 잠봉뵈르(Jambon-Beurre) 샌드위치 가게. <strong>파리 최고의 바게트 샌드위치</strong>로 현지인·관광객 모두 줄 서는 곳.', location: '8 Rue des Capucines, 75002 Paris', reco: '잠봉뵈르(Jambon-Beurre) 샌드위치', price: 8, badge: 'badge-must', mapUrl: 'https://www.google.com/maps/search/Petit+Vendôme+Paris+Rue+des+Capucines', inSchedule: 'DAY 10' },
  { name: 'Le Moulin de la Croix Nivert', subName: '르 물랭 드 라 크루아 니베르', region: 'paris', desc: '에펠탑 근처 15구의 수상 경력 불랑제리. 바삭하고 버터향 가득한 크루아상과 비에누아즈리가 아침을 깨운다.', location: '15e arrondissement, Paris', reco: '크루아상(Croissant), 팡오쇼콜라(Pain au chocolat)', price: 5, badge: 'badge-local-rec', mapUrl: 'https://www.google.com/maps/search/Le+Moulin+de+la+Croix+Nivert+Paris' }
];"""

assert OLD_FOOD_DATA in html, "FOOD_DATA not found!"
html = html.replace(OLD_FOOD_DATA, NEW_FOOD_DATA)

# ============================================================
# 2. UPDATE CAFE_DATA with enriched descriptions, mapUrl, subName
# ============================================================
OLD_CAFE_DATA = """const CAFE_DATA = [
  { name: 'Oui Jelato', region: 'nice', desc: '젤라또', location: '구시가지', reco: '시즌 플레이버', price: 5, badge: 'badge-dessert' },
  { name: 'La maison de celine pâtisserie', region: 'nice', desc: '파티스리', location: '구시가지', reco: '피스타치오 크루아상, 초콜릿 마카롱', price: 6, badge: 'badge-dessert' },
  { name: 'Café Verlet', region: 'paris', desc: '로스터리 카페', location: '팔레루아얄 근처', reco: '싱글오리진 에스프레소', price: 5, badge: 'badge-cafe-type' },
  { name: 'I/O Café', region: 'paris', desc: '스페셜티', location: '마레지구', reco: '라떼, 플랫화이트', price: 5, badge: 'badge-cafe-type' },
  { name: 'Café de Flore', region: 'paris', desc: '역사적 카페', location: '생제르맹 데 프레 (1887년~)', reco: '카페오레, 크루아상', price: 8, badge: 'badge-view' }
];"""

NEW_CAFE_DATA = """const CAFE_DATA = [
  { name: 'Oui Jelato', subName: '우이 젤라또', region: 'nice', desc: '니스 구시가지 인기 젤라또 가게. 신선한 재료로 매일 만드는 수제 젤라또. 시즌별 한정 플레이버가 특별.', location: 'Vieux Nice, Rue de la Préfecture', reco: '시즌 플레이버, 피스타치오, 망고', price: 5, badge: 'badge-dessert', mapUrl: 'https://www.google.com/maps/search/Oui+Jelato+Nice+Vieux', inSchedule: 'DAY 8' },
  { name: 'La maison de celine pâtisserie', subName: '라 메종 드 셀린 파티스리', region: 'nice', desc: '니스 구시가지의 프렌치 파티스리. 피스타치오 크루아상과 수제 마카롱이 시그니처. 아침 일찍 방문 추천.', location: 'Vieux Nice', reco: '피스타치오 크루아상, 초콜릿 마카롱', price: 6, badge: 'badge-dessert', mapUrl: 'https://www.google.com/maps/search/La+maison+de+celine+patisserie+Nice' },
  { name: 'Café Verlet', subName: '카페 베를레 (1880년~)', region: 'paris', desc: '1880년부터 파리 1구에서 커피를 볶아온 역사적 로스터리. 팔레루아얄 근처에서 싱글오리진 원두를 직접 로스팅.', location: '256 Rue Saint-Honoré, 75001 Paris', reco: '싱글오리진 에스프레소, 카페크렘', price: 5, badge: 'badge-cafe-type', mapUrl: 'https://www.google.com/maps/search/Café+Verlet+Paris+Rue+Saint-Honoré', inSchedule: 'DAY 11' },
  { name: 'I/O Café', subName: '아이오 카페', region: 'paris', desc: '파리 마레지구의 3세대 스페셜티 커피숍. 미니멀한 인테리어와 정성스런 라떼아트. 현지 커피 러버들의 아지트.', location: 'Le Marais, 75004 Paris', reco: '라떼, 플랫화이트, 브이60 드립', price: 5, badge: 'badge-cafe-type', mapUrl: 'https://www.google.com/maps/search/IO+Café+Marais+Paris' },
  { name: 'Café de Flore', subName: '카페 드 플로르 (1887년~)', region: 'paris', desc: '<strong>1887년 개업</strong> 생제르맹 데 프레의 전설적 카페. 사르트르, 보부아르, 피카소가 앉았던 자리에서 커피를 마시는 경험.', location: '172 Bd Saint-Germain, 75006 Paris', reco: '카페오레(Café au Lait), 크루아상', price: 8, badge: 'badge-view', mapUrl: 'https://www.google.com/maps/search/Café+de+Flore+Paris+Boulevard+Saint-Germain', inSchedule: 'DAY 12' }
];"""

assert OLD_CAFE_DATA in html, "CAFE_DATA not found!"
html = html.replace(OLD_CAFE_DATA, NEW_CAFE_DATA)

# ============================================================
# 3. UPDATE CSS: list-card styles to match Taichung exactly
# ============================================================
OLD_LIST_CSS = """    .list-desc {
      font-size: 13px;
      color: var(--text-secondary);
      margin-bottom: 8px;
      line-height: 1.5;
    }

    .reco {
      font-size: 13px;
      margin-bottom: 8px;
      padding: 8px;
      background: var(--bg);
      border-radius: 6px;
      border-left: 3px solid var(--positive);
    }

    .address {
      font-size: 12px;
      color: var(--text-secondary);
      margin-bottom: 12px;
      line-height: 1.4;
    }

    .list-meta {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 12px;
      border-top: 1px solid var(--border);
      font-size: 13px;
    }

    .price {
      font-weight: 600;
      color: var(--accent);
    }

    .price .krw {
      display: block;
      font-size: 11px;
      color: var(--text-secondary);
      margin-top: 2px;
    }"""

NEW_LIST_CSS = """    .list-card .list-desc { font-size: 13px; color: var(--text-secondary); line-height: 1.7; margin-bottom: 10px; }
    .list-card .list-meta { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
    .list-card .price { font-size: 13px; font-weight: 600; color: var(--warning, #f59e0b); }
    .list-card .price .krw { font-weight: 400; }
    .list-card .address { font-size: 12px; color: var(--text-secondary); margin-top: 8px; line-height: 1.5; }
    .list-card .reco { font-size: 12px; color: var(--tag-food-text, #fb923c); font-weight: 500; margin-top: 8px; }
    .list-card .reco-cafe { font-size: 12px; color: var(--tag-cafe-text, #a78bfa); font-weight: 500; margin-top: 8px; }
    .in-schedule { font-size: 11px; color: var(--accent); font-weight: 500; margin-top: 6px; }
    .region-local-header { font-size: 13px; font-weight: 600; color: #34d399; margin: 20px 0 12px; padding: 8px 12px; background: rgba(16,185,129,0.08); border-left: 3px solid #34d399; border-radius: 0 6px 6px 0; }
    .local-rec-tag { font-size: 11px; color: #34d399; font-weight: 600; margin-top: 6px; display: flex; align-items: center; gap: 4px; }
    .map-link { font-size: 12px; color: var(--accent); text-decoration: none; display: inline-flex; align-items: center; gap: 3px; font-weight: 500; }
    .map-link:hover { text-decoration: underline; }
    .map-svg { width: 14px; height: 14px; flex-shrink: 0; }"""

assert OLD_LIST_CSS in html, "list CSS block not found!"
html = html.replace(OLD_LIST_CSS, NEW_LIST_CSS)

# ============================================================
# 4. REPLACE renderFoodPanel with Taichung-style cards
# ============================================================
OLD_RENDER_FOOD = """// ===== FOOD PANEL =====
function renderFoodPanel() {
  const filterContainer = document.getElementById('food-filters');
  const listContainer = document.getElementById('food-list');

  // Add CRUD bar before filters
  let crudBar = document.getElementById('food-crud-bar');
  if (!crudBar) {
    crudBar = document.createElement('div');
    crudBar.id = 'food-crud-bar';
    crudBar.className = 'crud-bar';
    crudBar.innerHTML = '<button class="btn-add" onclick="openModal(\\'food\\')">+ 🍜 맛집 추가</button>';
    filterContainer.parentNode.insertBefore(crudBar, filterContainer);
  }

  // Filters
  filterContainer.innerHTML = `
    <button class="region-btn active" onclick="filterFood('all')">전체 <span class="region-count">${FOOD_DATA.length}</span></button>
  `;

  Object.entries(REGIONS).forEach(([key, region]) => {
    const count = FOOD_DATA.filter(f => f.region === key).length;
    filterContainer.innerHTML += `
      <button class="region-btn" onclick="filterFood('${key}')">${region.emoji} ${region.name} <span class="region-count">${count}</span></button>
    `;
  });

  // List
  listContainer.innerHTML = '';
  Object.entries(REGIONS).forEach(([key, region]) => {
    const items = FOOD_DATA.filter(f => f.region === key);
    if (items.length === 0) return;

    let html = `
      <div class="region-section" data-region="${key}">
        <div class="region-section-title"><span class="region-emoji">${region.emoji}</span> ${region.name}</div>
        <div class="list-grid">
    `;

    items.forEach(item => {
      html += `
        <div class="list-card">
          <div class="list-card-header">
            <div><h3>${item.name}</h3></div>
            <span class="badge-type ${item.badge}">${getBadgeLabel(item.badge)}</span>
          </div>
          <div class="list-desc">${item.desc}</div>
          <div class="reco">추천: ${item.reco}</div>
          <div class="address">${item.location}</div>
          <div class="list-meta">
            <span class="price">~€${item.price} <span class="krw">(₩${Math.round(item.price * EUR_TO_KRW)})</span></span>
            <a class="map-link" href="#" onclick="return false;">구글지도</a>
          </div>
        </div>
      `;
    });

    html += '</div></div>';
    listContainer.innerHTML += html;
  });
}"""

NEW_RENDER_FOOD = """// ===== FOOD PANEL =====
function renderFoodPanel() {
  var MAP_SVG = '<svg class="map-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>';
  const filterContainer = document.getElementById('food-filters');
  const listContainer = document.getElementById('food-list');

  // Add CRUD bar before filters
  let crudBar = document.getElementById('food-crud-bar');
  if (!crudBar) {
    crudBar = document.createElement('div');
    crudBar.id = 'food-crud-bar';
    crudBar.className = 'crud-bar';
    crudBar.innerHTML = '<button class="btn-add" onclick="openModal(\\'food\\')">+ 🍜 맛집 추가</button>';
    filterContainer.parentNode.insertBefore(crudBar, filterContainer);
  }

  // Filters
  filterContainer.innerHTML = `
    <button class="region-btn active" onclick="filterFood('all')">전체 <span class="region-count">${FOOD_DATA.length}</span></button>
  `;

  Object.entries(REGIONS).forEach(([key, region]) => {
    const count = FOOD_DATA.filter(f => f.region === key).length;
    if (count > 0) {
      filterContainer.innerHTML += `
        <button class="region-btn" onclick="filterFood('${key}')">${region.emoji} ${region.name} <span class="region-count">${count}</span></button>
      `;
    }
  });

  // List
  listContainer.innerHTML = '';
  Object.entries(REGIONS).forEach(([key, region]) => {
    const items = FOOD_DATA.filter(f => f.region === key);
    if (items.length === 0) return;

    // Separate regular and local-rec items
    const regularItems = items.filter(f => f.badge !== 'badge-local-rec');
    const localRecItems = items.filter(f => f.badge === 'badge-local-rec');

    let html = `
      <div class="region-section" data-region="${key}">
        <div class="region-section-title"><span class="region-emoji">${region.emoji}</span> ${region.name}</div>
        <div class="list-grid">
    `;

    regularItems.forEach(item => {
      var mapLink = item.mapUrl
        ? '<a class="map-link" href="' + item.mapUrl + '" target="_blank" rel="noopener">' + MAP_SVG + '구글지도</a>'
        : '';
      var scheduleTag = item.inSchedule
        ? '<div class="in-schedule">📌 ' + item.inSchedule + ' 일정 포함</div>'
        : '';
      html += `
        <div class="list-card">
          <div class="list-card-header"><div><h3>${item.name}</h3>${item.subName ? '<div class="cn-name">' + item.subName + '</div>' : ''}</div><span class="badge-type ${item.badge}">${getBadgeLabel(item.badge)}</span></div>
          <div class="list-desc">${item.desc}</div>
          <div class="reco">추천: ${item.reco}</div>
          <div class="address">${item.location}</div>
          <div class="list-meta"><span class="price">~€${item.price} <span class="krw">(₩${Math.round(item.price * EUR_TO_KRW).toLocaleString()})</span></span>${mapLink}</div>
          ${scheduleTag}
        </div>
      `;
    });

    html += '</div>';

    // Local rec section
    if (localRecItems.length > 0) {
      html += '<div class="region-local-header">🟢 #현지인맛집 — ' + region.name + ' 로컬 픽</div>';
      html += '<div class="list-grid">';
      localRecItems.forEach(item => {
        var mapLink = item.mapUrl
          ? '<a class="map-link" href="' + item.mapUrl + '" target="_blank" rel="noopener">' + MAP_SVG + '구글지도</a>'
          : '';
        var scheduleTag = item.inSchedule
          ? '<div class="in-schedule">📌 ' + item.inSchedule + ' 일정 포함</div>'
          : '';
        html += `
          <div class="list-card">
            <div class="list-card-header"><div><h3>${item.name}</h3>${item.subName ? '<div class="cn-name">' + item.subName + '</div>' : ''}</div><span class="badge-type ${item.badge}">#현지인맛집</span></div>
            <div class="list-desc">${item.desc}</div>
            <div class="reco">추천: ${item.reco}</div>
            <div class="address">${item.location}</div>
            <div class="list-meta"><span class="price">~€${item.price} <span class="krw">(₩${Math.round(item.price * EUR_TO_KRW).toLocaleString()})</span></span>${mapLink}</div>
            ${scheduleTag}
          </div>
        `;
      });
      html += '</div>';
    }

    html += '</div>';
    listContainer.innerHTML += html;
  });
}"""

assert OLD_RENDER_FOOD in html, "renderFoodPanel not found!"
html = html.replace(OLD_RENDER_FOOD, NEW_RENDER_FOOD)

# ============================================================
# 5. REPLACE renderCafePanel with Taichung-style cards
# ============================================================
OLD_RENDER_CAFE = """// ===== CAFE PANEL =====
function renderCafePanel() {
  const filterContainer = document.getElementById('cafe-filters');
  const listContainer = document.getElementById('cafe-list');

  // Add CRUD bar before filters
  let crudBar = document.getElementById('cafe-crud-bar');
  if (!crudBar) {
    crudBar = document.createElement('div');
    crudBar.id = 'cafe-crud-bar';
    crudBar.className = 'crud-bar';
    crudBar.innerHTML = '<button class="btn-add" onclick="openModal(\\'cafe\\')">+ ☕ 카페 추가</button>';
    filterContainer.parentNode.insertBefore(crudBar, filterContainer);
  }

  // Filters
  filterContainer.innerHTML = `
    <button class="region-btn active" onclick="filterCafe('all')">전체 <span class="region-count">${CAFE_DATA.length}</span></button>
  `;

  Object.entries(REGIONS).forEach(([key, region]) => {
    const count = CAFE_DATA.filter(f => f.region === key).length;
    if (count > 0) {
      filterContainer.innerHTML += `
        <button class="region-btn" onclick="filterCafe('${key}')">${region.emoji} ${region.name} <span class="region-count">${count}</span></button>
      `;
    }
  });

  // List
  listContainer.innerHTML = '';
  Object.entries(REGIONS).forEach(([key, region]) => {
    const items = CAFE_DATA.filter(f => f.region === key);
    if (items.length === 0) return;

    let html = `
      <div class="region-section" data-region="${key}">
        <div class="region-section-title"><span class="region-emoji">${region.emoji}</span> ${region.name}</div>
        <div class="list-grid">
    `;

    items.forEach(item => {
      html += `
        <div class="list-card">
          <div class="list-card-header">
            <div><h3>${item.name}</h3></div>
            <span class="badge-type ${item.badge}">${getBadgeLabel(item.badge)}</span>
          </div>
          <div class="list-desc">${item.desc}</div>
          <div class="reco">추천: ${item.reco}</div>
          <div class="address">${item.location}</div>
          <div class="list-meta">
            <span class="price">~€${item.price} <span class="krw">(₩${Math.round(item.price * EUR_TO_KRW)})</span></span>
            <a class="map-link" href="#" onclick="return false;">구글지도</a>
          </div>
        </div>
      `;
    });

    html += '</div></div>';
    listContainer.innerHTML += html;
  });
}"""

NEW_RENDER_CAFE = """// ===== CAFE PANEL =====
function renderCafePanel() {
  var MAP_SVG = '<svg class="map-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>';
  const filterContainer = document.getElementById('cafe-filters');
  const listContainer = document.getElementById('cafe-list');

  // Add CRUD bar before filters
  let crudBar = document.getElementById('cafe-crud-bar');
  if (!crudBar) {
    crudBar = document.createElement('div');
    crudBar.id = 'cafe-crud-bar';
    crudBar.className = 'crud-bar';
    crudBar.innerHTML = '<button class="btn-add" onclick="openModal(\\'cafe\\')">+ ☕ 카페 추가</button>';
    filterContainer.parentNode.insertBefore(crudBar, filterContainer);
  }

  // Filters
  filterContainer.innerHTML = `
    <button class="region-btn active" onclick="filterCafe('all')">전체 <span class="region-count">${CAFE_DATA.length}</span></button>
  `;

  Object.entries(REGIONS).forEach(([key, region]) => {
    const count = CAFE_DATA.filter(f => f.region === key).length;
    if (count > 0) {
      filterContainer.innerHTML += `
        <button class="region-btn" onclick="filterCafe('${key}')">${region.emoji} ${region.name} <span class="region-count">${count}</span></button>
      `;
    }
  });

  // List
  listContainer.innerHTML = '';
  Object.entries(REGIONS).forEach(([key, region]) => {
    const items = CAFE_DATA.filter(f => f.region === key);
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
        ? '<div class="in-schedule">📌 ' + item.inSchedule + ' 일정 포함</div>'
        : '';
      html += `
        <div class="list-card">
          <div class="list-card-header"><div><h3>${item.name}</h3>${item.subName ? '<div class="cn-name">' + item.subName + '</div>' : ''}</div><span class="badge-type ${item.badge}">${getBadgeLabel(item.badge)}</span></div>
          <div class="list-desc">${item.desc}</div>
          <div class="reco-cafe">추천: ${item.reco}</div>
          <div class="address">${item.location}</div>
          <div class="list-meta"><span class="price">~€${item.price} <span class="krw">(₩${Math.round(item.price * EUR_TO_KRW).toLocaleString()})</span></span>${mapLink}</div>
          ${scheduleTag}
        </div>
      `;
    });

    html += '</div></div>';
    listContainer.innerHTML += html;
  });
}"""

assert OLD_RENDER_CAFE in html, "renderCafePanel not found!"
html = html.replace(OLD_RENDER_CAFE, NEW_RENDER_CAFE)

# ============================================================
# 6. ADD ⋮ button to hotel cards in addMoreButtons function
# ============================================================
OLD_ADD_MORE = """  // Food/Cafe cards
  document.querySelectorAll('.list-card').forEach(function(card) {
    if (card.querySelector('.btn-more')) return;
    var wrap = document.createElement('div');
    wrap.style.cssText = 'position:absolute;top:0;right:0;z-index:2;';
    var btn = document.createElement('button');
    btn.className = 'btn-more';
    btn.innerHTML = '⋮';
    var dd = document.createElement('div');
    dd.className = 'card-dropdown';
    var delBtn = document.createElement('button');
    delBtn.className = 'card-dropdown-item danger';
    delBtn.textContent = '🗑 삭제하기';
    delBtn.onclick = function(e) {
      e.stopPropagation();
      dd.classList.remove('show');
      showConfirm(function() { card.remove(); });
    };
    dd.appendChild(delBtn);
    btn.onclick = function(e) {
      e.stopPropagation();
      document.querySelectorAll('.card-dropdown.show').forEach(function(d) { if(d !== dd) d.classList.remove('show'); });
      dd.classList.toggle('show');
    };
    wrap.appendChild(btn);
    wrap.appendChild(dd);
    card.appendChild(wrap);
  });
}"""

NEW_ADD_MORE = """  // Food/Cafe cards
  document.querySelectorAll('.list-card').forEach(function(card) {
    if (card.querySelector('.btn-more')) return;
    var wrap = document.createElement('div');
    wrap.style.cssText = 'position:absolute;top:0;right:0;z-index:2;';
    var btn = document.createElement('button');
    btn.className = 'btn-more';
    btn.innerHTML = '⋮';
    var dd = document.createElement('div');
    dd.className = 'card-dropdown';
    var delBtn = document.createElement('button');
    delBtn.className = 'card-dropdown-item danger';
    delBtn.textContent = '🗑 삭제하기';
    delBtn.onclick = function(e) {
      e.stopPropagation();
      dd.classList.remove('show');
      showConfirm(function() { card.remove(); });
    };
    dd.appendChild(delBtn);
    btn.onclick = function(e) {
      e.stopPropagation();
      document.querySelectorAll('.card-dropdown.show').forEach(function(d) { if(d !== dd) d.classList.remove('show'); });
      dd.classList.toggle('show');
    };
    wrap.appendChild(btn);
    wrap.appendChild(dd);
    card.appendChild(wrap);
  });

  // Hotel cards
  document.querySelectorAll('.hotel-card').forEach(function(card, idx) {
    if (card.querySelector('.btn-more')) return;
    var wrap = document.createElement('div');
    wrap.style.cssText = 'position:absolute;top:12px;right:12px;z-index:2;';
    var btn = document.createElement('button');
    btn.className = 'btn-more';
    btn.innerHTML = '⋮';
    btn.title = '더보기';
    var dd = document.createElement('div');
    dd.className = 'card-dropdown';

    // Edit button
    var editBtn = document.createElement('button');
    editBtn.className = 'card-dropdown-item';
    editBtn.textContent = '✏️ 수정하기';
    editBtn.onclick = function(e) {
      e.stopPropagation();
      dd.classList.remove('show');
      openHotelEditModal(idx);
    };
    dd.appendChild(editBtn);

    // Delete button
    var delBtn = document.createElement('button');
    delBtn.className = 'card-dropdown-item danger';
    delBtn.textContent = '🗑 삭제하기';
    delBtn.onclick = function(e) {
      e.stopPropagation();
      dd.classList.remove('show');
      showConfirm(function() {
        HOTEL_DATA.splice(idx, 1);
        if (hotelIndex >= HOTEL_DATA.length) hotelIndex = Math.max(0, HOTEL_DATA.length - 1);
        renderHotelPanel();
        addMoreButtons();
        saveToStorage();
      });
    };
    dd.appendChild(delBtn);

    btn.onclick = function(e) {
      e.stopPropagation();
      document.querySelectorAll('.card-dropdown.show').forEach(function(d) { if(d !== dd) d.classList.remove('show'); });
      dd.classList.toggle('show');
    };
    wrap.appendChild(btn);
    wrap.appendChild(dd);
    card.appendChild(wrap);
  });
}"""

assert OLD_ADD_MORE in html, "addMoreButtons food/cafe section not found!"
html = html.replace(OLD_ADD_MORE, NEW_ADD_MORE)

# ============================================================
# 7. ADD Hotel Edit Modal HTML + JS functions
# ============================================================
# Find the closing </script> to insert hotel modal functions before it
# We'll add openHotelEditModal function before the closing of the main script

OLD_DELETE_ALL = """function deleteAllData() {
  if (confirm('모든 데이터를 삭제하시겠습니까?')) {
    expenses = [];
    localStorage.removeItem(STORAGE_KEY);
    updateExpenseUI();
    alert('모든 데이터가 삭제되었습니다.');
  }
}"""

NEW_DELETE_ALL = """function deleteAllData() {
  if (confirm('모든 데이터를 삭제하시겠습니까?')) {
    expenses = [];
    localStorage.removeItem(STORAGE_KEY);
    updateExpenseUI();
    alert('모든 데이터가 삭제되었습니다.');
  }
}

// ===== HOTEL EDIT MODAL =====
function openHotelEditModal(idx) {
  var hotel = HOTEL_DATA[idx];
  if (!hotel) return;
  var overlay = document.getElementById('modal-hotel-edit');
  if (!overlay) {
    // Create hotel edit modal dynamically
    overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.id = 'modal-hotel-edit';
    overlay.innerHTML = `
      <div class="modal">
        <div class="modal-header"><h3>🏨 숙소 수정</h3><button class="modal-close" onclick="closeModal('hotel-edit')">✕</button></div>
        <div class="modal-body">
          <label>숙소명</label><input type="text" id="hotelEditName" class="modal-input">
          <label>부제 (서브네임)</label><input type="text" id="hotelEditSubName" class="modal-input">
          <label>숙소 유형</label><input type="text" id="hotelEditType" class="modal-input" placeholder="호텔 / Airbnb / 게스트하우스">
          <label>지역</label>
          <select id="hotelEditRegion" class="modal-input"></select>
          <label>체크인</label><input type="date" id="hotelEditCheckIn" class="modal-input">
          <label>체크아웃</label><input type="date" id="hotelEditCheckOut" class="modal-input">
          <label>가격 (EUR)</label><input type="number" id="hotelEditPriceEUR" class="modal-input" placeholder="EUR 기준 (없으면 빈칸)">
          <label>가격 (KRW)</label><input type="number" id="hotelEditPriceKRW" class="modal-input" placeholder="KRW 기준 (없으면 빈칸)">
          <label>예약 사이트</label><input type="text" id="hotelEditBookingSite" class="modal-input" placeholder="Booking.com / Airbnb">
          <label>예약 URL</label><input type="text" id="hotelEditBookingUrl" class="modal-input">
          <label>지도 URL</label><input type="text" id="hotelEditMapUrl" class="modal-input">
          <button class="modal-submit" onclick="submitHotelEdit()">수정 완료</button>
        </div>
      </div>
    `;
    document.body.appendChild(overlay);
    // Populate region select
    var sel = document.getElementById('hotelEditRegion');
    Object.entries(REGIONS).forEach(function(entry) {
      var opt = document.createElement('option');
      opt.value = entry[0];
      opt.textContent = entry[1].emoji + ' ' + entry[1].name;
      sel.appendChild(opt);
    });
  }
  // Fill form
  document.getElementById('hotelEditName').value = hotel.name || '';
  document.getElementById('hotelEditSubName').value = hotel.subName || '';
  document.getElementById('hotelEditType').value = hotel.type || '';
  document.getElementById('hotelEditRegion').value = hotel.region || '';
  document.getElementById('hotelEditCheckIn').value = hotel.checkIn || '';
  document.getElementById('hotelEditCheckOut').value = hotel.checkOut || '';
  document.getElementById('hotelEditPriceEUR').value = hotel.priceEUR || '';
  document.getElementById('hotelEditPriceKRW').value = hotel.priceKRW || '';
  document.getElementById('hotelEditBookingSite').value = hotel.bookingSite || '';
  document.getElementById('hotelEditBookingUrl').value = hotel.bookingUrl || '';
  document.getElementById('hotelEditMapUrl').value = hotel.mapUrl || '';
  overlay.dataset.editIdx = idx;
  overlay.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function submitHotelEdit() {
  var overlay = document.getElementById('modal-hotel-edit');
  var idx = parseInt(overlay.dataset.editIdx);
  var hotel = HOTEL_DATA[idx];
  if (!hotel) return;

  hotel.name = document.getElementById('hotelEditName').value;
  hotel.subName = document.getElementById('hotelEditSubName').value;
  hotel.type = document.getElementById('hotelEditType').value;
  hotel.region = document.getElementById('hotelEditRegion').value;
  hotel.checkIn = document.getElementById('hotelEditCheckIn').value;
  hotel.checkOut = document.getElementById('hotelEditCheckOut').value;

  var priceEUR = parseFloat(document.getElementById('hotelEditPriceEUR').value);
  var priceKRW = parseInt(document.getElementById('hotelEditPriceKRW').value);

  if (priceEUR > 0) {
    hotel.priceEUR = priceEUR;
    delete hotel.priceKRW;
  } else if (priceKRW > 0) {
    hotel.priceKRW = priceKRW;
    delete hotel.priceEUR;
  }

  // Calculate nights
  var ci = new Date(hotel.checkIn);
  var co = new Date(hotel.checkOut);
  hotel.nights = Math.round((co - ci) / (1000 * 60 * 60 * 24));

  hotel.bookingSite = document.getElementById('hotelEditBookingSite').value;
  hotel.bookingUrl = document.getElementById('hotelEditBookingUrl').value;
  hotel.mapUrl = document.getElementById('hotelEditMapUrl').value;

  renderHotelPanel();
  addMoreButtons();
  saveToStorage();
  closeModal('hotel-edit');
}"""

assert OLD_DELETE_ALL in html, "deleteAllData not found!"
html = html.replace(OLD_DELETE_ALL, NEW_DELETE_ALL)

# ============================================================
# 8. Update version number in header
# ============================================================
html = html.replace('v3.3', 'v3.4')

# ============================================================
# 9. Update list-card padding to match Taichung (20px)
# ============================================================
html = html.replace(
    """.list-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px;
      transition: all 0.3s;
      position: relative;
    }""",
    """.list-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
      transition: box-shadow 0.2s;
      position: relative;
    }"""
)

# Update hover style to match Taichung
html = html.replace(
    """.list-card:hover {
      border-color: var(--accent);
      background: var(--surface-hover);
    }""",
    """.list-card:hover { box-shadow: 0 0 0 1px var(--border), 0 8px 16px rgba(0,0,0,0.08); }"""
)

# Update h3 style
html = html.replace(
    """.list-card-header h3 {
      font-size: 16px;
      margin-bottom: 4px;
    }""",
    """.list-card h3 { font-size: 16px; font-weight: 600; letter-spacing: -0.02em; margin-bottom: 2px; }"""
)

# Update cn-name
html = html.replace(
    """.cn-name {
      font-size: 12px;
      color: var(--text-secondary);
    }""",
    """.list-card .cn-name { font-size: 13px; color: var(--text-secondary); }"""
)

# Update list-card-header margin
html = html.replace(
    """.list-card-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 12px;
      margin-bottom: 12px;
    }""",
    """.list-card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px; }"""
)

# ============================================================
# WRITE OUTPUT
# ============================================================
with open(DST, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ v3.4 generated: {DST}")
print(f"   File size: {len(html):,} chars")
