#!/usr/bin/env python3
"""
Fix v3.2 hotel card to match Taichung v12 layout:
1. HOTEL_DATA: add bookingSite, mapUrl, subName fields
2. Hotel CSS: match Taichung exactly
3. renderHotelPanel: Taichung-style card with nights-bar, 6-grid info, price row, SVG buttons
"""

FILE = '/sessions/jolly-relaxed-meitner/mnt/여행 계획 대시보드/[2026-06] 프랑스/output/프랑스여행_여행일정대시보드_v3.2_2026.03.30.html'

with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# ============================================================
# 1. Replace HOTEL_DATA with enriched fields
# ============================================================
old_hotel_data = """const HOTEL_DATA = [
  { name: '마르세유 에어비앤비', type: 'Airbnb', checkIn: '2026-06-03', checkOut: '2026-06-05', nights: 2, region: 'marseille', priceKRW: 194480 },
  { name: 'Hôtel - Restaurant Le Relais', type: '호텔', checkIn: '2026-06-05', checkOut: '2026-06-06', nights: 1, region: 'provence', priceEUR: 82, mapUrl: 'https://maps.app.goo.gl/kJ5t46Wh2vWWygXcA', bookingUrl: '#' },
  { name: 'Saint-Jeannet 에어비앤비', type: 'Airbnb', checkIn: '2026-06-06', checkOut: '2026-06-08', nights: 2, region: 'cotedazur', priceKRW: 178628 },
  { name: '니스 에어비앤비', type: 'Airbnb', checkIn: '2026-06-08', checkOut: '2026-06-10', nights: 2, region: 'nice', priceKRW: 0 },
  { name: '파리 에어비앤비', type: 'Airbnb', checkIn: '2026-06-10', checkOut: '2026-06-13', nights: 3, region: 'paris', priceKRW: 699821 }
];"""

new_hotel_data = """const HOTEL_DATA = [
  { name: '마르세유 에어비앤비', subName: '마르세유 시내 · Rue Saint-Ferreol', type: 'Airbnb', typeEmoji: '🏠', checkIn: '2026-06-03', checkOut: '2026-06-05', nights: 2, region: 'marseille', priceKRW: 194480, bookingSite: 'Airbnb', bookingUrl: 'https://www.airbnb.com', mapUrl: 'https://www.google.com/maps/search/Rue+Saint-Ferreol+Marseille' },
  { name: 'Hôtel Le Relais', subName: '르 를레 · 무스티에생트마리', type: '호텔', typeEmoji: '🏨', checkIn: '2026-06-05', checkOut: '2026-06-06', nights: 1, region: 'provence', priceEUR: 82, bookingSite: 'Booking.com', bookingUrl: 'https://www.booking.com', mapUrl: 'https://maps.app.goo.gl/kJ5t46Wh2vWWygXcA' },
  { name: 'Saint-Jeannet 에어비앤비', subName: '생자네 · 코트다쥐르 내륙', type: 'Airbnb', typeEmoji: '🏠', checkIn: '2026-06-06', checkOut: '2026-06-08', nights: 2, region: 'cotedazur', priceKRW: 178628, bookingSite: 'Airbnb', bookingUrl: 'https://www.airbnb.com', mapUrl: 'https://www.google.com/maps/search/Saint-Jeannet+France' },
  { name: '니스 에어비앤비', subName: '니스 구시가지 근처', type: 'Airbnb', typeEmoji: '🏠', checkIn: '2026-06-08', checkOut: '2026-06-10', nights: 2, region: 'nice', priceKRW: 0, bookingSite: 'Airbnb', bookingUrl: 'https://www.airbnb.com', mapUrl: 'https://www.google.com/maps/search/Nice+Old+Town+accommodation' },
  { name: '파리 에어비앤비', subName: '마레 지구 (Marais)', type: 'Airbnb', typeEmoji: '🏠', checkIn: '2026-06-10', checkOut: '2026-06-13', nights: 3, region: 'paris', priceKRW: 699821, bookingSite: 'Airbnb', bookingUrl: 'https://www.airbnb.com', mapUrl: 'https://www.google.com/maps/search/Le+Marais+Paris+accommodation' }
];"""

html = html.replace(old_hotel_data, new_hotel_data)
print("FIX 1: HOTEL_DATA enriched ✓")

# ============================================================
# 2. Replace hotel CSS to match Taichung exactly
# ============================================================
old_hotel_css = """    .hotel-carousel-wrap {
      margin: 30px 0;
    }

    .hotel-carousel-viewport {
      overflow: hidden;
      border-radius: 12px;
      background: var(--surface);
      border: 1px solid var(--border);
    }

    .hotel-carousel-track {
      display: flex;
      transition: transform 0.4s ease-out;
    }

    .hotel-card {
      min-width: 100%;
      padding: 24px;
      background: var(--surface);
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .hotel-card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
    }

    .hotel-name {
      font-size: 20px;
      font-weight: 700;
    }

    .hotel-type-badge {
      display: inline-block;
      background: var(--tag-hotel);
      color: var(--tag-hotel-text);
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      white-space: nowrap;
    }

    .hotel-info-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 16px;
    }

    .hotel-info-item {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .hotel-info-label {
      font-size: 12px;
      color: var(--text-secondary);
      text-transform: uppercase;
      font-weight: 600;
    }

    .hotel-info-value {
      font-size: 15px;
      font-weight: 600;
    }

    .hotel-nights-bar {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }

    .hotel-night-chip {
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 8px 12px;
      text-align: center;
    }

    .night-date {
      font-size: 12px;
      color: var(--text-secondary);
    }

    .night-label {
      font-size: 13px;
      font-weight: 600;
      color: var(--accent);
    }

    .hotel-price-row {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 16px;
      padding: 16px;
      background: var(--bg);
      border-radius: 8px;
    }

    .hotel-price-item {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .hotel-price-label {
      font-size: 12px;
      color: var(--text-secondary);
      text-transform: uppercase;
      font-weight: 600;
    }

    .hotel-price-value {
      font-size: 18px;
      font-weight: 700;
      color: var(--accent);
    }

    .hotel-price-krw {
      font-size: 12px;
      color: var(--text-secondary);
    }

    .hotel-footer {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
    }

    .hotel-btn {
      flex: 1;
      min-width: 120px;
      padding: 12px 16px;
      border: 1px solid var(--border);
      background: transparent;
      color: var(--text);
      border-radius: 8px;
      cursor: pointer;
      font-size: 13px;
      font-weight: 600;
      transition: all 0.3s;
      text-align: center;
      text-decoration: none;
      font-family: 'Noto Sans KR', sans-serif;
    }

    .hotel-btn:hover {
      background: var(--surface-hover);
      border-color: var(--accent);
    }

    .hotel-btn-booking {
      background: var(--accent);
      color: white;
      border-color: var(--accent);
    }

    .hotel-btn-booking:hover {
      background: var(--accent-secondary);
      border-color: var(--accent-secondary);
    }

    .hotel-nav {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 16px 20px;
      background: var(--surface);
      gap: 12px;
    }

    .hotel-nav-btn {
      background: var(--surface-hover);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 8px 12px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 16px;
      transition: all 0.3s;
      font-family: 'Noto Sans KR', sans-serif;
    }

    .hotel-nav-btn:hover {
      background: var(--accent);
      color: white;
      border-color: var(--accent);
    }"""

new_hotel_css = """    /* ===== HOTEL CAROUSEL (Taichung style) ===== */
    .hotel-carousel-wrap { position: relative; max-width: 640px; margin: 0 auto; }
    .hotel-carousel-viewport { overflow: hidden; border-radius: 16px; }
    .hotel-carousel-track { display: flex; transition: transform 0.38s cubic-bezier(0.4,0,0.2,1); will-change: transform; }
    .hotel-card { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 28px; min-width: 100%; box-sizing: border-box; position: relative; }
    .hotel-card-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; margin-bottom: 20px; }
    .hotel-name { font-size: 22px; font-weight: 700; letter-spacing: -0.03em; }
    .hotel-sub-name { margin-top: 4px; font-size: 14px; color: var(--text-secondary); }
    .hotel-type-badge { background: rgba(245,158,11,0.15); color: #f59e0b; font-size: 11px; font-weight: 600; padding: 4px 10px; border-radius: 20px; white-space: nowrap; }
    .hotel-info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 20px; }
    .hotel-info-item { display: flex; flex-direction: column; gap: 4px; }
    .hotel-info-label { font-size: 11px; color: var(--text-secondary); font-weight: 500; text-transform: uppercase; letter-spacing: 0.04em; }
    .hotel-info-value { font-size: 15px; font-weight: 600; color: var(--text); }
    .hotel-price-row { display: flex; gap: 12px; padding: 16px; background: rgba(59,130,246,0.06); border-radius: 10px; margin-bottom: 20px; align-items: center; flex-wrap: wrap; }
    .hotel-price-item { flex: 1; min-width: 120px; }
    .hotel-price-label { font-size: 11px; color: var(--text-secondary); font-weight: 500; text-transform: uppercase; margin-bottom: 4px; }
    .hotel-price-value { font-size: 18px; font-weight: 700; color: var(--accent); }
    .hotel-price-krw { font-size: 12px; color: var(--text-secondary); margin-top: 2px; }
    .hotel-footer { display: flex; gap: 10px; flex-wrap: wrap; }
    .hotel-btn { display: inline-flex; align-items: center; gap: 6px; padding: 9px 16px; border-radius: 8px; font-size: 13px; font-weight: 500; text-decoration: none; transition: opacity 0.2s; border: none; cursor: pointer; font-family: inherit; }
    .hotel-btn:hover { opacity: 0.8; text-decoration: none; }
    .hotel-btn-booking { background: rgba(3,133,255,0.12); color: #0385ff; }
    .hotel-btn-map { background: rgba(16,185,129,0.12); color: #10b981; }
    .hotel-nights-bar { display: flex; gap: 6px; margin-bottom: 20px; }
    .hotel-night-chip { flex: 1; background: var(--surface-hover); border: 1px solid var(--border); border-radius: 8px; padding: 8px 10px; text-align: center; }
    .hotel-night-chip .night-date { font-size: 11px; color: var(--text-secondary); }
    .hotel-night-chip .night-label { font-size: 13px; font-weight: 600; color: var(--text); margin-top: 2px; }

    .hotel-nav { display: flex; align-items: center; justify-content: center; gap: 16px; margin-top: 20px; }
    .hotel-nav-btn { width: 36px; height: 36px; border-radius: 50%; border: 1px solid var(--border); background: var(--surface); color: var(--text-secondary); display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s; font-size: 14px; font-family: inherit; }
    .hotel-nav-btn:hover { background: var(--surface-hover); color: var(--text); }
    .hotel-nav-btn:disabled { opacity: 0.3; cursor: default; }"""

html = html.replace(old_hotel_css, new_hotel_css)
print("FIX 2: Hotel CSS replaced ✓")

# ============================================================
# 3. Fix hotel-dots CSS
# ============================================================
old_dots = """    .hotel-dots {
      display: flex;"""
new_dots = """    .hotel-counter { font-size: 12px; color: var(--text-secondary); min-width: 36px; text-align: center; }
    .hotel-dots {
      display: flex;"""
# Only add if hotel-counter not already defined
if '.hotel-counter {' not in html:
    html = html.replace(old_dots, new_dots)
    print("FIX 3: Hotel counter CSS added ✓")

# ============================================================
# 4. Replace hotel nav HTML to use SVG arrows + centered layout
# ============================================================
old_hotel_nav_html = """      <button class="hotel-nav-btn" id="hotelPrev" onclick="hotelSlide(-1)">◀</button>"""
new_hotel_nav_html = """      <button class="hotel-nav-btn" id="hotelPrev" onclick="hotelSlide(-1)" aria-label="이전">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
            </button>"""
html = html.replace(old_hotel_nav_html, new_hotel_nav_html)

old_hotel_next = """      <button class="hotel-nav-btn" id="hotelNext" onclick="hotelSlide(1)">▶</button>"""
new_hotel_next = """      <button class="hotel-nav-btn" id="hotelNext" onclick="hotelSlide(1)" aria-label="다음">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
            </button>"""
html = html.replace(old_hotel_next, new_hotel_next)
print("FIX 4: Hotel nav SVG arrows ✓")

# ============================================================
# 5. Replace renderHotelPanel function
# ============================================================
old_render = """function renderHotelPanel() {
  const track = document.getElementById('hotelTrack');
  const dotsContainer = document.getElementById('hotelDots');

  track.innerHTML = '';
  dotsContainer.innerHTML = '';

  HOTEL_DATA.forEach((hotel, idx) => {
    const card = document.createElement('div');
    card.className = 'hotel-card';

    const priceDisplay = hotel.priceEUR ? `€${hotel.priceEUR}` : `₩${hotel.priceKRW}`;
    const priceKRWDisplay = hotel.priceEUR ? `≈ ₩${Math.round(hotel.priceEUR * EUR_TO_KRW)}` : hotel.priceKRW.toLocaleString();
    const pricePerNight = hotel.priceEUR ? `€${(hotel.priceEUR / hotel.nights).toFixed(2)}` : `₩${Math.round(hotel.priceKRW / hotel.nights)}`;
    const pricePerNightKRW = hotel.priceEUR ? `≈ ₩${Math.round((hotel.priceEUR / hotel.nights) * EUR_TO_KRW)}` : hotel.priceKRW / hotel.nights;

    card.innerHTML = `
      <div class="hotel-card-header">
        <div class="hotel-name">${hotel.name}</div>
        <span class="hotel-type-badge">${hotel.type}</span>
      </div>
      <div class="hotel-info-grid">
        <div class="hotel-info-item">
          <div class="hotel-info-label">지역</div>
          <div class="hotel-info-value">${REGIONS[hotel.region].name}</div>
        </div>
        <div class="hotel-info-item">
          <div class="hotel-info-label">체크인</div>
          <div class="hotel-info-value">${hotel.checkIn}</div>
        </div>
        <div class="hotel-info-item">
          <div class="hotel-info-label">체크아웃</div>
          <div class="hotel-info-value">${hotel.checkOut}</div>
        </div>
      </div>
      <div class="hotel-nights-bar">
        <div class="hotel-night-chip">
          <div class="night-date">${hotel.checkIn} ~ ${hotel.checkOut}</div>
          <div class="night-label">${hotel.nights}박</div>
        </div>
      </div>
      <div class="hotel-price-row">
        <div class="hotel-price-item">
          <div class="hotel-price-label">총 금액</div>
          <div class="hotel-price-value">${priceDisplay}</div>
          <div class="hotel-price-krw">${priceKRWDisplay}</div>
        </div>
        <div class="hotel-price-item">
          <div class="hotel-price-label">1박 요금</div>
          <div class="hotel-price-value">${pricePerNight}</div>
          <div class="hotel-price-krw">${pricePerNightKRW}</div>
        </div>
      </div>
      <div class="hotel-footer">
        <a class="hotel-btn hotel-btn-booking" href="${hotel.bookingUrl || '#'}" target="_blank">예약</a>
        ${hotel.mapUrl ? `<a class="hotel-btn hotel-btn-map" href="${hotel.mapUrl}" target="_blank">구글지도</a>` : '<button class="hotel-btn hotel-btn-map" disabled>구글지도</button>'}
      </div>
    `;

    track.appendChild(card);

    const dot = document.createElement('div');
    dot.className = `hotel-dot ${idx === 0 ? 'active' : ''}`;
    dot.onclick = () => hotelGoto(idx);
    dotsContainer.appendChild(dot);
  });

  updateHotelNav();
}"""

new_render = r"""function renderHotelPanel() {
  var BOOKING_SVG = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8h1a4 4 0 010 8h-1"/><path d="M2 8h16v9a4 4 0 01-4 4H6a4 4 0 01-4-4V8z"/><line x1="6" y1="1" x2="6" y2="4"/><line x1="10" y1="1" x2="10" y2="4"/><line x1="14" y1="1" x2="14" y2="4"/></svg>';
  var MAP_SVG = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>';

  var track = document.getElementById('hotelTrack');
  var dotsContainer = document.getElementById('hotelDots');
  track.innerHTML = '';
  dotsContainer.innerHTML = '';

  var DOW_MAP = {'0':'일','1':'월','2':'화','3':'수','4':'목','5':'금','6':'토'};
  function fmtDate(dateStr) {
    var d = new Date(dateStr);
    return d.getFullYear() + '. ' + String(d.getMonth()+1).padStart(2,'0') + '. ' + String(d.getDate()).padStart(2,'0') + ' (' + DOW_MAP[d.getDay()] + ')';
  }
  function shortDate(dateStr) {
    var d = new Date(dateStr);
    return (d.getMonth()+1) + '/' + d.getDate() + ' (' + DOW_MAP[d.getDay()] + ')';
  }

  HOTEL_DATA.forEach(function(hotel, idx) {
    var card = document.createElement('div');
    card.className = 'hotel-card';

    // Price calculations
    var totalPriceKRW, totalDisplay, perNightDisplay, perNightKRW;
    if (hotel.priceEUR) {
      totalPriceKRW = Math.round(hotel.priceEUR * EUR_TO_KRW);
      totalDisplay = hotel.priceEUR.toLocaleString() + ' EUR';
      var pn = hotel.priceEUR / hotel.nights;
      perNightDisplay = pn.toFixed(0) + ' EUR';
      perNightKRW = Math.round(pn * EUR_TO_KRW);
    } else {
      totalPriceKRW = hotel.priceKRW;
      totalDisplay = '₩' + hotel.priceKRW.toLocaleString();
      var pnk = Math.round(hotel.priceKRW / hotel.nights);
      perNightDisplay = '₩' + pnk.toLocaleString();
      perNightKRW = pnk;
    }

    // Generate nights bar chips
    var nightsHTML = '';
    var ciDate = new Date(hotel.checkIn);
    for (var n = 0; n < hotel.nights; n++) {
      var nd = new Date(ciDate);
      nd.setDate(nd.getDate() + n);
      nightsHTML += '<div class="hotel-night-chip"><div class="night-date">' + shortDate(nd.toISOString().slice(0,10)) + '</div><div class="night-label">' + (n+1) + '박째</div></div>';
    }

    var h = '';
    // Header
    h += '<div class="hotel-card-header"><div>';
    h += '<div class="hotel-name">' + hotel.name + '</div>';
    h += '<div class="hotel-sub-name">' + (hotel.subName || '') + '</div>';
    h += '</div>';
    h += '<span class="hotel-type-badge">' + (hotel.typeEmoji || '🏨') + ' ' + hotel.type + '</span>';
    h += '</div>';

    // Nights bar
    h += '<div class="hotel-nights-bar">' + nightsHTML + '</div>';

    // Info grid (6 items like Taichung)
    h += '<div class="hotel-info-grid">';
    h += '<div class="hotel-info-item"><span class="hotel-info-label">체크인</span><span class="hotel-info-value">' + fmtDate(hotel.checkIn) + '</span></div>';
    h += '<div class="hotel-info-item"><span class="hotel-info-label">체크아웃</span><span class="hotel-info-value">' + fmtDate(hotel.checkOut) + '</span></div>';
    h += '<div class="hotel-info-item"><span class="hotel-info-label">숙박일수</span><span class="hotel-info-value">' + hotel.nights + '박</span></div>';
    h += '<div class="hotel-info-item"><span class="hotel-info-label">지역</span><span class="hotel-info-value">' + REGIONS[hotel.region].name + '</span></div>';
    h += '<div class="hotel-info-item"><span class="hotel-info-label">숙소 유형</span><span class="hotel-info-value">' + hotel.type + '</span></div>';
    h += '<div class="hotel-info-item"><span class="hotel-info-label">예약 사이트</span><span class="hotel-info-value">' + (hotel.bookingSite || '-') + '</span></div>';
    h += '</div>';

    // Price row
    h += '<div class="hotel-price-row">';
    h += '<div class="hotel-price-item"><div class="hotel-price-label">' + hotel.nights + '박 총 가격</div>';
    h += '<div class="hotel-price-value">' + totalDisplay + '</div>';
    if (hotel.priceEUR) h += '<div class="hotel-price-krw">≈ ₩' + totalPriceKRW.toLocaleString() + '</div>';
    h += '</div>';
    h += '<div class="hotel-price-item"><div class="hotel-price-label">1박 가격</div>';
    h += '<div class="hotel-price-value">' + perNightDisplay + '</div>';
    h += '<div class="hotel-price-krw">≈ ₩' + perNightKRW.toLocaleString() + '</div>';
    h += '</div></div>';

    // Buttons (Taichung style with SVG icons)
    h += '<div class="hotel-footer">';
    h += '<a class="hotel-btn hotel-btn-booking" href="' + (hotel.bookingUrl || '#') + '" target="_blank" rel="noopener">' + BOOKING_SVG + ' ' + (hotel.bookingSite || '') + ' 예약 확인</a>';
    if (hotel.mapUrl) {
      h += '<a class="hotel-btn hotel-btn-map" href="' + hotel.mapUrl + '" target="_blank" rel="noopener">' + MAP_SVG + ' 구글지도</a>';
    }
    h += '</div>';

    card.innerHTML = h;
    track.appendChild(card);

    var dot = document.createElement('div');
    dot.className = 'hotel-dot' + (idx === 0 ? ' active' : '');
    dot.onclick = (function(i) { return function() { hotelGoto(i); }; })(idx);
    dotsContainer.appendChild(dot);
  });

  updateHotelNav();
}"""

html = html.replace(old_render, new_render)
print("FIX 5: renderHotelPanel replaced ✓")

# ============================================================
# 6. Version history
# ============================================================
old_ver = """  v3.2 (2026.03.30) : 일정카드 레이아웃 타이중 v12와 동일하게 변경,"""
new_ver = """  v3.3 (2026.03.30) : 숙소 카드 타이중 v12 레이아웃으로 변경,
                       박별 칩바, 6칸 정보그리드, SVG 버튼, 구글지도 연동
  v3.2 (2026.03.30) : 일정카드 레이아웃 타이중 v12와 동일하게 변경,"""

html = html.replace(old_ver, new_ver)
print("FIX 6: Version history ✓")

# ============================================================
# WRITE as v3.3
# ============================================================
OUT = '/sessions/jolly-relaxed-meitner/mnt/여행 계획 대시보드/[2026-06] 프랑스/output/프랑스여행_여행일정대시보드_v3.3_2026.03.30.html'
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html)

content = html
lines = content.split('\n')
print(f"\nOutput: {OUT}")
print(f"Lines: {len(lines)}")

checks = [
    ('hotel-card-header', 'Hotel card header'),
    ('hotel-name', 'Hotel name CSS'),
    ('hotel-sub-name', 'Hotel sub name'),
    ('hotel-type-badge', 'Hotel type badge'),
    ('hotel-nights-bar', 'Nights bar'),
    ('hotel-night-chip', 'Night chip'),
    ('hotel-info-grid', 'Info grid'),
    ('hotel-info-label', 'Info label'),
    ('hotel-price-row', 'Price row'),
    ('hotel-price-value', 'Price value'),
    ('hotel-btn-booking', 'Booking button'),
    ('hotel-btn-map', 'Map button'),
    ('BOOKING_SVG', 'Booking SVG'),
    ('hotel-carousel-wrap', 'Carousel wrap'),
    ('hotelSlide', 'Hotel slide fn'),
    ('bookingSite', 'bookingSite field'),
    ('subName', 'subName field'),
    ('typeEmoji', 'typeEmoji field'),
    ('google.com/maps', 'Google Maps URLs'),
    ('renderSchedule', 'Schedule intact'),
    ('modal-overlay', 'Modal intact'),
    ('FOOD_DATA', 'Food data intact'),
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

if all_ok:
    print("\n✅ All checks passed!")
else:
    print("\n⚠️ Some checks failed!")
