# 대시보드 에디토리얼 개편 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `index.html`을 에디토리얼 매거진 디자인 + 왼쪽 메뉴로 개편하고, 지식카드와 자동 스크랩을 하나의 목록·하나의 카테고리 체계로 보여준다.

**Architecture:** 순수 로직(카테고리 매핑, 카드 병합, 필터, 생성 커버 계산)은 `js/archive-core.js`로 빼서 Node 내장 테스트로 검증한다. `index.html`은 이 파일을 불러와 화면만 그린다. 카테고리 목록은 `categories.json`, 자동 스크랩은 `scraps.json`에서 읽는다. 이 계획만 끝나도 사이트는 정상 동작한다(스크랩 0건).

**Tech Stack:** 정적 HTML/CSS/바닐라 JS, Node 24 내장 테스트(`node --test`), GitHub Pages(`main` 브랜치 루트, 공개).

**설계서:** `docs/superpowers/specs/2026-11-22-link-scrap-cards-design.md` 4.7, 4.8, 4.9
**기준 시안:** https://claude.ai/artifact/Wis23SZk9oHuBuVRKpB2cE 의 "확정안 · 리스트 뷰", "확정안 · 카드 뷰"

**현재 구조 메모 (`index.html`, 2932줄):**
- 1~596줄 CSS, 598~789줄 본문 마크업, 790~2930줄 스크립트
- `KNOWLEDGE_DB` 배열 794줄부터(카드 106장). 항목 필드: `id, title, file, date, source, sourceUrl, tags, difficulty, summary, related, color, category`, 일부는 `series`
- 카테고리 설정 `_CATS` 2469줄, 카드 필터 `filterCards` 2557줄, 카드 렌더 `renderCards` 2579줄(안에 `_CI`, `_ICONS` 매핑), 초기화 2925줄
- 저장 키: 읽음 `ka-read-status`, 테마 `viz-theme`
- 현재 카테고리 값: 투자·주식 30, 기술·산업 26, 경제·거시 17, 시사·컬처 15, 투자·금융 12, 부동산 6

---

## File Structure

| 파일 | 역할 |
|---|---|
| `categories.json` (신규) | 통합 카테고리 목록과 생성 커버 색. 대시보드·요약기·단축어가 함께 읽음 |
| `scraps.json` (신규) | 자동 스크랩 카드 목록. 이 계획에서는 빈 배열 |
| `js/archive-core.js` (신규) | 순수 함수: 병합, 필터, 개수 집계, 생성 커버 |
| `tests/archive-core.test.js` (신규) | 위 함수의 테스트 |
| `tools/migrate_categories.py` (신규) | `index.html`의 옛 카테고리 값을 새 값으로 바꾸는 일회성 스크립트 |
| `index.html` (수정) | 스타일·마크업·렌더 함수 개편 |
| `tools/make_icon.py`, `icons/`, `manifest.webmanifest` (신규) | 아이폰 홈 화면 아이콘 |

---

### Task 1: 통합 카테고리 파일과 기존 카드 이전

**Files:**
- Create: `categories.json`, `scraps.json`, `tools/migrate_categories.py`
- Modify: `index.html` (`KNOWLEDGE_DB`의 `category` 값만)

- [ ] **Step 1: `categories.json` 작성**

```json
[
  { "name": "경제·투자", "color": "#1f3a2e" },
  { "name": "기술·산업", "color": "#1d2f5c" },
  { "name": "부동산", "color": "#5b3a1e" },
  { "name": "시사·컬처", "color": "#5c1f2a" },
  { "name": "패션", "color": "#6b2f55" },
  { "name": "테크", "color": "#111111" },
  { "name": "etc", "color": "#55524a" }
]
```

모든 색은 흰 글자와 대비 4.5:1 이상이다. 새 카테고리를 색 없이 추가하면 `#333333`을 쓴다(Task 2).

- [ ] **Step 2: `scraps.json` 작성**

```json
[]
```

- [ ] **Step 3: 이전 스크립트 작성 `tools/migrate_categories.py`**

```python
"""index.html의 KNOWLEDGE_DB category 값을 통합 카테고리로 바꾼다. 여러 번 실행해도 결과가 같다."""
import re
import sys
from collections import Counter
from pathlib import Path

MAPPING = {"투자·주식": "경제·투자", "경제·거시": "경제·투자", "투자·금융": "경제·투자"}
EXPECTED = {"경제·투자": 59, "기술·산업": 26, "부동산": 6, "시사·컬처": 15}
PATTERN = re.compile(r'(category:\s*")([^"]+)(")')


def migrate(text: str) -> str:
    return PATTERN.sub(lambda m: m.group(1) + MAPPING.get(m.group(2), m.group(2)) + m.group(3), text)


if __name__ == "__main__":
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
    out = migrate(path.read_text(encoding="utf-8"))
    counts = Counter(m.group(2) for m in PATTERN.finditer(out))
    print(dict(counts))
    if dict(counts) != EXPECTED:
        sys.exit("카테고리 개수가 예상과 다릅니다. index.html에 카드가 추가됐는지 확인하고 EXPECTED를 고치세요.")
    path.write_text(out, encoding="utf-8")
```

- [ ] **Step 4: 실행하고 개수 확인**

Run: `python3 tools/migrate_categories.py`
Expected: `{'기술·산업': 26, '시사·컬처': 15, '부동산': 6, '경제·투자': 59}` (순서는 달라도 됨), 종료 코드 0

그 사이 `main`에 카드가 추가됐다면 개수가 달라 실패한다. 그때는 실제 개수를 확인해 `EXPECTED`를 고친 뒤 다시 실행한다.

- [ ] **Step 5: 옛 값이 남지 않았는지 확인**

Run: `grep -c 'category: "투자·주식"\|category: "경제·거시"\|category: "투자·금융"' index.html`
Expected: `0`

- [ ] **Step 6: Commit**

```bash
git add categories.json scraps.json tools/migrate_categories.py index.html
git commit -m "feat: 통합 카테고리 도입 및 기존 카드 106장 이전"
```

---

### Task 2: 순수 로직 모듈 `js/archive-core.js`

브라우저에서는 `window.ArchiveCore`, Node에서는 `require`로 쓰는 UMD 형태로 만든다.

**Files:**
- Create: `js/archive-core.js`, `tests/archive-core.test.js`

- [ ] **Step 1: 실패하는 테스트 작성 `tests/archive-core.test.js`**

```js
const test = require('node:test');
const assert = require('node:assert/strict');
const core = require('../js/archive-core.js');

const manual = [
  { id: 'a', title: '국채 금리', date: '2026-04-22', source: '뉴스레터', tags: ['금리', '채권'], summary: '요약', category: '경제·투자' },
  { id: 'b', title: 'K배터리', date: '2026-01-05', source: '', tags: [], summary: '', category: '기술·산업', series: '배터리' }
];
const scraps = [
  { id: 's1', title: '코트 스타일링', date: '2026-11-20', source: '인스타그램', sourceType: 'instagram_post', tags: ['코트'], summary: '', category: '패션', cover: 'covers/s1.jpg' }
];

test('mergeCards: 직접 정리 카드에 sourceType manual을 붙이고 최신순으로 합친다', () => {
  const all = core.mergeCards(manual, scraps);
  assert.deepEqual(all.map((c) => c.id), ['s1', 'a', 'b']);
  assert.equal(all[1].sourceType, 'manual');
  assert.equal(all[0].sourceType, 'instagram_post');
});

test('mergeCards: scraps가 배열이 아니면 직접 정리 카드만 돌려준다', () => {
  assert.equal(core.mergeCards(manual, null).length, 2);
});

test('filterCards: 카테고리·형식·검색·읽음을 함께 적용한다', () => {
  const all = core.mergeCards(manual, scraps);
  const base = { category: 'all', type: 'all', tag: 'all', series: 'all', read: 'all', query: '' };
  assert.equal(core.filterCards(all, base, {}).length, 3);
  assert.deepEqual(core.filterCards(all, { ...base, category: '패션' }, {}).map((c) => c.id), ['s1']);
  assert.deepEqual(core.filterCards(all, { ...base, type: 'manual' }, {}).map((c) => c.id), ['a', 'b']);
  assert.deepEqual(core.filterCards(all, { ...base, query: '채권' }, {}).map((c) => c.id), ['a']);
  assert.deepEqual(core.filterCards(all, { ...base, read: 'unread' }, { a: true }).map((c) => c.id), ['s1', 'b']);
  assert.deepEqual(core.filterCards(all, { ...base, series: '배터리' }, {}).map((c) => c.id), ['b']);
});

test('countByCategory: 목록에 있는 카테고리는 0건이어도 포함한다', () => {
  const all = core.mergeCards(manual, scraps);
  assert.deepEqual(core.countByCategory(all, ['경제·투자', '테크']), { '경제·투자': 1, '테크': 0, '기술·산업': 1, '패션': 1 });
});

test('coverFor: 이미지가 있으면 이미지, 없으면 글자형 생성 커버', () => {
  const cats = [{ name: '경제·투자', color: '#1f3a2e' }];
  assert.deepEqual(core.coverFor(scraps[0], cats), { kind: 'image', src: 'covers/s1.jpg' });
  assert.deepEqual(core.coverFor(manual[0], cats), { kind: 'generated', word: '금리', color: '#1f3a2e' });
  assert.deepEqual(core.coverFor(manual[1], cats), { kind: 'generated', word: 'K배터리', color: '#333333' });
  assert.equal(core.coverFor({ title: '아주 긴 제목이 들어간 카드입니다', tags: [], category: 'x', coverWord: '커피' }, cats).word, '커피');
});

test('typeLabel: 형식 이름', () => {
  assert.equal(core.typeLabel('manual'), '직접 정리');
  assert.equal(core.typeLabel('youtube'), '유튜브');
  assert.equal(core.typeLabel('unknown'), '기사');
});
```

- [ ] **Step 2: 실패 확인**

Run: `node --test tests/*.test.js`
Expected: FAIL — `Cannot find module '../js/archive-core.js'`

- [ ] **Step 3: 구현 `js/archive-core.js`**

```js
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.ArchiveCore = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  var TYPE_LABELS = {
    manual: '직접 정리', article: '기사', instagram_post: '인스타그램',
    instagram_reel: '릴스', youtube: '유튜브'
  };
  var DEFAULT_COLOR = '#333333';

  function mergeCards(manual, scraps) {
    var a = (manual || []).map(function (c) { return Object.assign({ sourceType: 'manual' }, c); });
    var b = Array.isArray(scraps) ? scraps : [];
    return a.concat(b).sort(function (x, y) { return x.date < y.date ? 1 : x.date > y.date ? -1 : 0; });
  }

  function filterCards(cards, f, readStatus) {
    var q = (f.query || '').toLowerCase();
    return cards.filter(function (k) {
      var tags = k.tags || [];
      if (f.category !== 'all' && k.category !== f.category) return false;
      if (f.type !== 'all' && k.sourceType !== f.type) return false;
      if (f.tag !== 'all' && tags.indexOf(f.tag) === -1) return false;
      if (f.series !== 'all' && k.series !== f.series) return false;
      var isRead = !!readStatus[k.id];
      if (f.read === 'read' && !isRead) return false;
      if (f.read === 'unread' && isRead) return false;
      if (!q) return true;
      return [k.title, k.summary, tags.join(' '), k.source].some(function (v) {
        return (v || '').toLowerCase().indexOf(q) !== -1;
      });
    });
  }

  function countByCategory(cards, names) {
    var counts = {};
    (names || []).forEach(function (n) { counts[n] = 0; });
    cards.forEach(function (k) { counts[k.category] = (counts[k.category] || 0) + 1; });
    return counts;
  }

  function coverFor(card, categories) {
    if (card.cover) return { kind: 'image', src: card.cover };
    var cat = (categories || []).filter(function (c) { return c.name === card.category; })[0];
    var word = card.coverWord || (card.tags && card.tags[0]) || card.title.split(/\s*[—:·]\s*/)[0];
    return { kind: 'generated', word: word, color: (cat && cat.color) || DEFAULT_COLOR };
  }

  function typeLabel(t) { return TYPE_LABELS[t] || '기사'; }

  return {
    mergeCards: mergeCards, filterCards: filterCards, countByCategory: countByCategory,
    coverFor: coverFor, typeLabel: typeLabel, TYPE_LABELS: TYPE_LABELS
  };
});
```

- [ ] **Step 4: 통과 확인**

Run: `node --test tests/*.test.js`
Expected: `pass 6`, `fail 0`

- [ ] **Step 5: Commit**

```bash
git add js/archive-core.js tests/archive-core.test.js
git commit -m "feat: 카드 병합·필터·생성 커버 순수 로직 추가"
```

---

### Task 3: `index.html`이 통합 데이터를 쓰도록 배선

디자인을 바꾸기 전에 데이터 흐름부터 바꾼다. 이 Task가 끝나면 화면 모양은 그대로이고 카테고리만 통합된 상태다.

**Files:**
- Modify: `index.html` (스크립트 영역)

- [ ] **Step 1: 스크립트 불러오기**

790줄의 `<script>` 바로 앞에 추가한다.

```html
  <script src="js/archive-core.js"></script>
```

- [ ] **Step 2: 상태 변수 추가**

`var readStatus = {};` 아래에 추가한다.

```js
    var activeType = 'all';
    var CATEGORIES = [];
    var ALL_CARDS  = ArchiveCore.mergeCards(KNOWLEDGE_DB, []);
```

- [ ] **Step 3: `filterCards`를 통합 로직으로 교체**

2557줄의 `function filterCards() { ... }` 전체를 아래로 바꾼다.

```js
    function filterCards() {
      return ArchiveCore.filterCards(ALL_CARDS, {
        category: activeCategory, type: activeType, tag: activeTag,
        series: activeSeries, read: activeReadFilter, query: searchQuery
      }, readStatus);
    }
```

- [ ] **Step 4: `KNOWLEDGE_DB`를 직접 도는 나머지 코드를 `ALL_CARDS`로 변경**

Run: `grep -n "KNOWLEDGE_DB" index.html`

선언(794줄)과 Step 2의 `mergeCards` 호출을 뺀 모든 사용처(`renderCatFilters`, `renderTagFilters`, `renderSeriesFilters`, `renderStats`, `openSwipeView` 등)를 `ALL_CARDS`로 바꾼다. 각 사용처에서 `k.tags`, `k.source`를 쓰는 곳은 스크랩에도 같은 필드가 있으므로 그대로 둔다.

- [ ] **Step 5: `_CATS`를 `categories.json` 기반으로 교체**

2469줄의 `var _CATS = [ ... ];`를 아래로 바꾼다.

```js
    function catList() {
      return [{ id: 'all', label: '전체' }].concat(CATEGORIES.map(function (c) {
        return { id: c.name, label: c.name };
      }));
    }
```

`renderSidebarNav` 안의 `_CATS.forEach`를 `catList().forEach`로 바꾸고, 아이콘 `<span class="material-symbols-outlined nav-icon ...">` 줄은 지운다. `renderCards` 안의 `_CI`, `_ICONS` 매핑과 그것을 쓰는 `catCls`, `catIcon`도 지우고 `catBadge`는 아래로 바꾼다.

```js
          var catBadge = '<span class="cat-badge">' + k.category + ' · ' + ArchiveCore.typeLabel(k.sourceType) + '</span>';
```

- [ ] **Step 6: 초기화에서 두 JSON을 불러오기**

2925줄의 `// ============ INIT ============` 블록을 아래로 바꾼다.

```js
    // ============ INIT ============
    function renderAll() {
      renderTagFilters();
      renderCatFilters();
      renderStats();
      renderCards();
    }
    function loadJson(path, fallback) {
      return fetch(path, { cache: 'no-cache' })
        .then(function (r) { return r.ok ? r.json() : fallback; })
        .catch(function () { return fallback; });
    }
    loadReadStatus();
    renderAll();
    Promise.all([loadJson('categories.json', []), loadJson('scraps.json', [])]).then(function (res) {
      CATEGORIES = res[0];
      ALL_CARDS  = ArchiveCore.mergeCards(KNOWLEDGE_DB, res[1]);
      renderAll();
    });
```

먼저 한 번 그린 뒤 JSON이 오면 다시 그리므로, 두 파일을 읽지 못해도 기존 카드는 보인다(설계서 4.5).

- [ ] **Step 7: 브라우저에서 확인**

`.claude/launch.json`에 정적 서버를 등록한다(없으면 새로 만든다).

```json
{
  "version": "0.0.1",
  "configurations": [
    { "name": "archive", "runtimeExecutable": "python3", "runtimeArgs": ["-m", "http.server", "8765"], "port": 8765 }
  ]
}
```

`preview_start`로 `archive`를 띄우고 다음을 확인한다.
- 콘솔 오류 0건
- 왼쪽 카테고리에 경제·투자 59, 기술·산업 26, 부동산 6, 시사·컬처 15, 패션 0, 테크 0, etc 0
- 경제·투자를 누르면 59장만 보임
- 검색, 읽음 표시, 랜덤 보기가 이전처럼 동작

- [ ] **Step 8: Commit**

```bash
git add index.html .claude/launch.json
git commit -m "refactor: 대시보드가 통합 카테고리와 scraps.json을 읽도록 변경"
```

---

### Task 4: 에디토리얼 스타일과 왼쪽 메뉴

**Files:**
- Modify: `index.html` (CSS 1~596줄, 본문 마크업 598~789줄, `renderSidebarNav`, `renderStats`)

- [ ] **Step 1: 디자인 토큰 교체**

`:root { ... }`와 `html.theme-light { ... }` 두 블록(12~50줄)을 아래로 바꾼다. 기본을 라이트로 두고 다크는 `html.theme-dark`로 옮긴다. 변수 이름은 유지해서 나머지 CSS가 그대로 동작하게 한다.

```css
    :root {
      --bg: #ffffff; --surface-low: #ffffff; --surface-mid: #f6f6f6; --surface-high: #ffffff;
      --surface-highest: #eeeeee; --surface-bright: #ffffff;
      --primary: #b3261e; --primary-fixed: #b3261e; --on-primary-fixed: #ffffff;
      --secondary: #111111; --tertiary: #b3261e;
      --on-surface: #111111; --on-surface-v: #555555; --outline-v: #dddddd;
      --border: #dddddd; --rule: #111111;
      --text: #111111; --text-sec: #555555; --accent: #b3261e;
    }
    html.theme-dark {
      --bg: #111111; --surface-low: #111111; --surface-mid: #1b1b1b; --surface-high: #111111;
      --surface-highest: #262626; --surface-bright: #1b1b1b;
      --primary: #ff8a80; --primary-fixed: #ff8a80; --on-primary-fixed: #111111;
      --secondary: #f5f5f5; --tertiary: #ff8a80;
      --on-surface: #f5f5f5; --on-surface-v: #b8b8b8; --outline-v: #3a3a3a;
      --border: #3a3a3a; --rule: #f5f5f5;
      --text: #f5f5f5; --text-sec: #b8b8b8; --accent: #ff8a80;
    }
```

`<html ... class="theme-dark">`(2줄)의 `class`를 지우고, `applyTheme`(2741줄)이 `theme-light` 대신 `theme-dark` 클래스를 켜고 끄도록 고친다. 저장된 값이 없으면 라이트가 기본이다.

```js
    var currentTheme = 'light';
    function applyTheme(t) {
      currentTheme = t;
      document.getElementById('htmlRoot').classList.toggle('theme-dark', t === 'dark');
      document.getElementById('themeIcon').textContent = t === 'dark' ? 'light_mode' : 'dark_mode';
      localStorage.setItem('viz-theme', t);
    }
```

- [ ] **Step 2: 글꼴과 기본 규칙**

`body` 규칙의 `font-family`를 `'Noto Sans KR', -apple-system, sans-serif`로, `letter-spacing`을 `-0.02em`으로 바꾼다. 글꼴 링크(8줄)에서 `Inter`는 빼고 `Noto Sans KR`의 400·500·700·900만 남긴다. Material Symbols는 검색·테마·랜덤 아이콘에 계속 쓰므로 남긴다.

- [ ] **Step 3: 에디토리얼 공통 규칙 추가**

`</style>` 바로 앞에 추가한다. 뒤에 오는 규칙이 앞의 것을 덮어쓰므로, 기존 `.topbar`, `.sidebar`, `.hero-*`, `.ka-card`, `.filter-chip` 규칙에서 둥근 모서리·그림자·블러·그라데이션이 남아 보이면 해당 선언을 지운다.

```css
    /* ===== EDITORIAL ===== */
    .topbar { display: none; }
    .sidebar {
      position: fixed; top: 0; left: 0; bottom: 0; width: 250px; padding: 32px 22px;
      background: var(--bg); border-right: 1px solid var(--rule); overflow-y: auto;
      display: flex; flex-direction: column; backdrop-filter: none;
    }
    .brand { font-size: 26px; font-weight: 900; line-height: 1.1; letter-spacing: -0.05em;
      padding-bottom: 18px; border-bottom: 4px solid var(--rule); }
    .sidebar-section-label { font-size: 11px; font-weight: 900; letter-spacing: 0.08em;
      color: var(--text-sec); padding: 20px 0 6px; }
    .sidebar-nav-item {
      display: flex; align-items: center; width: 100%; min-height: 44px; padding: 0;
      background: none; border: 0; border-bottom: 1px solid var(--border); border-radius: 0;
      font: inherit; font-size: 15px; font-weight: 500; color: var(--text); cursor: pointer; text-align: left;
    }
    .sidebar-nav-item.active { font-weight: 900; color: var(--accent); background: none; }
    .sidebar-nav-item .nav-count { margin-left: auto; font-size: 13px; color: var(--text-sec); }
    .main-content { margin-left: 250px; padding: 28px 40px 48px; }
    .content-inner { max-width: 1040px; }
    .masthead { display: flex; flex-wrap: wrap; align-items: center; gap: 16px;
      border-bottom: 1px solid var(--rule); padding-bottom: 12px; margin-bottom: 28px;
      font-size: 13px; color: var(--text-sec); }
    .masthead .topbar-search { margin-left: auto; border: 0; border-bottom: 1px solid var(--rule);
      border-radius: 0; background: none; height: 44px; }
    .lead-row { display: flex; flex-wrap: wrap; gap: 40px; margin-bottom: 28px; }
    .lead { flex: 999 1 420px; min-width: 0; display: flex; flex-direction: column; gap: 16px;
      color: var(--text); text-decoration: none; }
    .lead-kicker { font-size: 12px; font-weight: 700; letter-spacing: 0.06em; color: var(--accent); }
    .lead-title { font-size: 42px; font-weight: 900; line-height: 1.2; letter-spacing: -0.04em; margin: 0; }
    .lead-summary { font-size: 17px; line-height: 1.75; color: var(--text-sec); max-width: 600px; margin: 0; }
    .recent { flex: 1 1 300px; min-width: 0; }
    .recent h2, .section-head h2 { margin: 0; font-size: 14px; font-weight: 900; }
    .recent h2 { padding-bottom: 10px; border-bottom: 2px solid var(--rule); }
    .recent-item { display: flex; gap: 14px; padding: 14px 0; border-bottom: 1px solid var(--border);
      text-decoration: none; color: var(--text); min-height: 44px; }
    .recent-no { font-size: 22px; font-weight: 900; color: var(--text-sec); line-height: 1.2; width: 30px; }
    .item-meta { font-size: 11px; font-weight: 700; letter-spacing: 0.05em; color: var(--text-sec); }
    .section-head { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 16px;
      border-top: 4px solid var(--rule); padding-top: 10px; }
    .view-toggle { display: flex; border: 1px solid var(--rule); margin-left: auto; }
    .view-toggle button { min-height: 44px; padding: 0 16px; border: 0; background: var(--bg);
      color: var(--text); font: inherit; font-size: 13px; font-weight: 500; cursor: pointer; }
    .view-toggle button[aria-pressed="true"] { background: var(--rule); color: var(--bg); font-weight: 900; }
    .card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 0 32px; }
    .ka-card { display: flex; flex-direction: column; gap: 8px; padding: 18px 0; background: none;
      border: 0; border-bottom: 1px solid var(--border); border-radius: 0; box-shadow: none;
      text-decoration: none; color: var(--text); position: relative; }
    .ka-card:hover .card-title { color: var(--accent); }
    .ka-card.is-read .card-title { color: var(--text-sec); }
    .card-stripe { display: none; }
    .card-title { font-size: 19px; font-weight: 900; line-height: 1.4; letter-spacing: -0.03em; }
    .card-summary { font-size: 13px; line-height: 1.6; color: var(--text-sec); }
    .card-cover { display: none; }
    @media (max-width: 760px) {
      .sidebar { position: static; width: auto; border-right: 0; border-bottom: 1px solid var(--rule); padding: 20px; }
      .main-content { margin-left: 0; padding: 20px; }
      .lead-title { font-size: 30px; }
    }
```

- [ ] **Step 4: 본문 마크업 교체**

`<header class="topbar">`부터 모바일 검색바 `</div>`까지(602~628줄)를 지운다. 테마 버튼은 왼쪽 메뉴 아래로 옮긴다.

`<nav class="sidebar">` 블록(631~644줄)을 아래로 바꾼다.

```html
  <nav class="sidebar" role="navigation" aria-label="카테고리 메뉴">
    <div class="brand">지식<br>Archive</div>
    <div class="sidebar-section-label">카테고리</div>
    <div class="sidebar-nav" id="sidebarNav"></div>
    <div class="sidebar-section-label">형식</div>
    <div class="sidebar-nav" id="typeNav"></div>
    <div style="margin-top:auto;padding-top:24px;display:flex;gap:8px;">
      <button class="icon-btn" onclick="cycleTheme()" aria-label="테마 전환" id="themeBtn">
        <span class="material-symbols-outlined" style="font-size:20px" id="themeIcon">dark_mode</span>
      </button>
      <button class="icon-btn" onclick="openSwipeView()" aria-label="랜덤 보기">
        <span class="material-symbols-outlined" style="font-size:20px">shuffle</span>
      </button>
    </div>
  </nav>
```

HERO 섹션(650~697줄 부근의 `<section class="hero-grid ...">` 전체)을 아래로 바꾼다.

```html
      <header class="masthead">
        <span>하나의 지식, 하나의 페이지 · 직접 정리한 카드와 보낸 링크가 한곳에 쌓입니다</span>
        <div class="topbar-search" role="search">
          <span class="material-symbols-outlined" style="font-size:17px" aria-hidden="true">search</span>
          <input type="text" id="searchInput" placeholder="제목·태그·키워드 검색" aria-label="지식 검색">
        </div>
      </header>
      <div class="lead-row">
        <a class="lead" id="leadCard" href="#"></a>
        <aside class="recent"><h2>최근 추가</h2><div id="recentList"></div></aside>
      </div>
```

필터 영역의 카테고리 칩 줄(`id="catFilters"`)과 그 위의 `<hr class="cat-divider">`는 왼쪽 메뉴와 중복되므로 지운다. 결과 표시 줄(`results-info`)을 아래로 바꾼다.

```html
      <div class="section-head">
        <h2>전체 카드</h2>
        <span id="resultsCount" class="item-meta">0장</span>
        <span class="active-filter-label" id="activeFilters"></span>
        <div class="view-toggle" role="group" aria-label="보기 방식">
          <button type="button" id="viewBtn-list" aria-pressed="true" onclick="setView('list')">리스트</button>
          <button type="button" id="viewBtn-card" aria-pressed="false" onclick="setView('card')">카드</button>
        </div>
      </div>
```

- [ ] **Step 5: 지운 요소를 쓰던 스크립트 정리**

모바일 검색 관련(`mobSearch`, `toggleMobileSearch`, `searchInputMobile`)과 HERO 통계 요소(`heroReadCount`, `heroTotal`, `heroProgress`, `heroLatestTitle`, `heroLatestDate`, `heroTotalBig`, `sidebarTotal`, `sidebarRead`, `sidebarProgress`)를 채우던 코드를 지운다. `renderCatFilters`는 개수 집계 후 `renderSidebarNav`만 호출하도록 줄인다.

```js
    function renderCatFilters() {
      var counts = ArchiveCore.countByCategory(ALL_CARDS, CATEGORIES.map(function (c) { return c.name; }));
      renderSidebarNav(counts, ALL_CARDS.length);
      renderTypeNav();
    }
```

`renderSidebarNav`가 만드는 버튼에서 아이콘을 뺐는지 확인하고(Task 3 Step 5), `resultsCount` 문구를 `filtered.length + '장'`으로 바꾼다.

- [ ] **Step 6: 형식 메뉴와 머리기사 렌더 추가**

`renderSidebarNav` 아래에 추가한다.

```js
    function filterType(t) { activeType = t; renderCatFilters(); renderCards(); }
    function renderTypeNav() {
      var nav = document.getElementById('typeNav');
      var types = ['all'].concat(Object.keys(ArchiveCore.TYPE_LABELS));
      nav.innerHTML = types.map(function (t) {
        var on = activeType === t;
        return '<button class="sidebar-nav-item' + (on ? ' active' : '') + '" onclick="filterType(\'' + t + '\')"'
          + ' aria-current="' + (on ? 'page' : 'false') + '">'
          + (t === 'all' ? '전체' : ArchiveCore.typeLabel(t)) + '</button>';
      }).join('');
    }
    function metaLine(k) {
      return k.category + ' · ' + ArchiveCore.typeLabel(k.sourceType) + ' · ' + k.date;
    }
    function renderLead() {
      var lead = ALL_CARDS[0];
      if (!lead) return;
      var el = document.getElementById('leadCard');
      el.href = lead.file;
      el.innerHTML = '<div class="lead-kicker">최신 · ' + metaLine(lead) + '</div>'
        + '<h1 class="lead-title">' + lead.title + '</h1>'
        + '<p class="lead-summary">' + lead.summary + '</p>';
      document.getElementById('recentList').innerHTML = ALL_CARDS.slice(1, 6).map(function (k, i) {
        return '<a class="recent-item" href="' + k.file + '"><span class="recent-no">' + (i + 1) + '</span>'
          + '<span style="display:flex;flex-direction:column;gap:4px"><span class="item-meta">' + metaLine(k) + '</span>'
          + '<span style="font-size:15px;font-weight:700;line-height:1.45">' + k.title + '</span></span></a>';
      }).join('');
    }
```

`renderStats` 본문을 `renderLead();` 한 줄로 바꾼다.

제목·요약은 지금도 `innerHTML`로 넣고 있고 값은 리포 안의 파일에서만 온다. 자동 스크랩의 값은 파이프라인이 저장할 때 HTML 이스케이프한다(파이프라인 계획 Task 7).

- [ ] **Step 7: 브라우저에서 시안과 비교**

`preview_start`로 띄우고 스크린샷을 찍어 "확정안 · 리스트 뷰" 시안과 비교한다. 확인 항목:
- 왼쪽 메뉴(브랜드, 카테고리 7개와 개수, 형식 5개), 머리기사가 "국채 금리 — 돈의 흐름이 바뀌는 신호를 읽는 법", 최근 추가 5건
- 형식에서 "직접 정리"를 누르면 106장, "유튜브"를 누르면 0장과 빈 상태 문구
- 테마 버튼으로 다크 전환 시 글자와 괘선이 모두 보임
- 폭 375px(`resize_window` mobile)에서 메뉴가 위로 쌓이고 가로 스크롤이 없음
- 콘솔 오류 0건

- [ ] **Step 8: Commit**

```bash
git add index.html
git commit -m "feat: 대시보드 에디토리얼 디자인과 왼쪽 메뉴 적용"
```

---

### Task 5: 카드 뷰와 커버 이미지

**Files:**
- Modify: `index.html` (CSS, `renderCards`)

- [ ] **Step 1: 카드 뷰 스타일 추가**

Task 4에서 넣은 `.card-cover { display: none; }` 줄을 아래로 바꾼다.

```css
    .card-cover { display: none; aspect-ratio: 16 / 9; padding: 16px; box-sizing: border-box;
      flex-direction: column; justify-content: space-between; color: #ffffff;
      background-size: cover; background-position: center; }
    .card-cover-label { font-size: 11px; font-weight: 700; letter-spacing: 0.06em; }
    .card-cover-word { font-size: 56px; font-weight: 900; line-height: 1.05; letter-spacing: -0.05em;
      overflow-wrap: anywhere; }
    .card-grid.view-card { grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 32px 28px; }
    .card-grid.view-card .ka-card { padding: 0 0 18px; border-bottom: 1px solid var(--rule); }
    .card-grid.view-card .card-cover { display: flex; }
```

- [ ] **Step 2: 뷰 상태와 전환 함수 추가**

`var activeType = 'all';` 아래에 추가한다.

```js
    var activeView = localStorage.getItem('ka-view') === 'card' ? 'card' : 'list';
    function setView(v) {
      activeView = v;
      try { localStorage.setItem('ka-view', v); } catch (e) {}
      renderCards();
    }
```

- [ ] **Step 3: `renderCards`에서 커버와 뷰 클래스 적용**

카드 HTML을 만드는 부분에서 `<div class="card-stripe" ...>` 줄을 커버로 바꾼다. `forEach` 안, `html +=` 앞에 추가한다.

```js
          var cv = ArchiveCore.coverFor(k, CATEGORIES);
          var coverHtml = cv.kind === 'image'
            ? '<div class="card-cover" role="img" aria-label="' + k.title + ' 커버" style="background-image:url(\'' + cv.src + '\')"></div>'
            : '<div class="card-cover" aria-hidden="true" style="background:' + cv.color + '">'
              + '<span class="card-cover-label">' + k.category + '</span>'
              + '<span class="card-cover-word">' + cv.word + '</span></div>';
```

`html +=` 문에서 `'<div class="card-stripe" style="background:' + k.color + '"></div>'`를 `coverHtml`로 바꾼다. 카테고리 배지 줄은 `'<span class="item-meta">' + metaLine(k) + '</span>'`로 바꾼다.

`grid.innerHTML = html;` 바로 뒤에 추가한다.

```js
        grid.classList.toggle('view-card', activeView === 'card');
        document.getElementById('viewBtn-list').setAttribute('aria-pressed', activeView === 'list');
        document.getElementById('viewBtn-card').setAttribute('aria-pressed', activeView === 'card');
```

- [ ] **Step 4: 이미지 커버 표시를 임시 데이터로 확인**

`scraps.json`을 임시로 아래 내용으로 바꾼다. 이미지 파일을 따로 만들지 않도록 `cover`에는 데이터 URL을 넣는다.

```json
[
  { "id": "scrap-test", "title": "커버 확인용 카드", "file": "cards/bonds-vs-stocks.html", "date": "2026-11-22",
    "source": "확인", "sourceUrl": "", "sourceType": "youtube", "tags": ["확인"], "summary": "이미지 커버 확인용",
    "category": "테크", "cover": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='9'%3E%3Crect width='16' height='9' fill='%23888'/%3E%3C/svg%3E" }
]
```

브라우저에서 확인한다.
- "카드"를 누르면 격자로 바뀌고 모든 카드에 커버가 보임
- 확인용 카드는 회색 이미지 커버, 나머지 106장은 카테고리 색 바탕에 첫 태그가 크게 표시됨
- 테크 1, 형식 "유튜브" 1로 집계됨. 머리기사가 확인용 카드로 바뀜
- 새로고침해도 카드 뷰가 유지됨. "리스트"를 누르면 글자 목록으로 돌아가고 커버가 사라짐
- 콘솔 오류 0건

- [ ] **Step 5: 임시 데이터 되돌리기**

`scraps.json`을 다시 `[]`로 바꾼다.

Run: `cat scraps.json`
Expected: `[]`

- [ ] **Step 6: 전체 테스트 재실행**

Run: `node --test tests/*.test.js`
Expected: `pass 6`, `fail 0`

- [ ] **Step 7: Commit**

```bash
git add index.html scraps.json
git commit -m "feat: 리스트/카드 뷰 전환과 커버 이미지 추가"
```

---

### Task 6: 아이폰 홈 화면 아이콘

확정 시안은 "5. 카드 네 장"이다. 검은 바탕(#111111)에 정사각형 네 장을 2×2로 놓고, 왼쪽 위 한 장만 붉은색(#e5483d), 나머지는 흰색이다. 모서리 둥글림은 iOS가 알아서 하므로 이미지는 꽉 찬 정사각형으로 만든다.

**Files:**
- Create: `tools/make_icon.py`, `icons/apple-touch-icon.png`, `icons/icon-512.png`, `manifest.webmanifest`
- Modify: `index.html` (`<head>`), `.gitignore`

- [ ] **Step 1: 아이콘 생성 스크립트 `tools/make_icon.py`**

외부 라이브러리 없이 PNG를 쓴다.

```python
"""홈 화면 아이콘을 만든다: 검은 바탕에 카드 네 장, 왼쪽 위만 붉은색."""
import struct
import zlib
from pathlib import Path

BG, RED, WHITE = (0x11, 0x11, 0x11), (0xE5, 0x48, 0x3D), (0xFF, 0xFF, 0xFF)


def pixels(size: int):
    pad, gap = round(size * 28 / 180), round(size * 12 / 180)
    cell = (size - 2 * pad - gap) // 2
    starts = (pad, pad + cell + gap)

    def color(x, y):
        for row, y0 in enumerate(starts):
            for col, x0 in enumerate(starts):
                if x0 <= x < x0 + cell and y0 <= y < y0 + cell:
                    return RED if (row, col) == (0, 0) else WHITE
        return BG

    return [[color(x, y) for x in range(size)] for y in range(size)]


def write_png(path: Path, size: int) -> None:
    raw = b"".join(b"\x00" + bytes(c for px in row for c in px) for row in pixels(size))

    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))

    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))
    path.parent.mkdir(exist_ok=True)
    path.write_bytes(png)


if __name__ == "__main__":
    write_png(Path("icons/apple-touch-icon.png"), 180)
    write_png(Path("icons/icon-512.png"), 512)
```

- [ ] **Step 2: 생성하고 눈으로 확인**

Run: `python3 tools/make_icon.py && file icons/*.png`
Expected: `icons/apple-touch-icon.png: PNG image data, 180 x 180, 8-bit/color RGB` 와 `icons/icon-512.png: PNG image data, 512 x 512, 8-bit/color RGB`

Read 도구로 `icons/apple-touch-icon.png`를 열어 왼쪽 위가 붉고 나머지 세 장이 흰색인지 확인한다.

- [ ] **Step 3: `.gitignore`에 예외 추가**

`.gitignore`가 `*.png`를 무시하므로 `*.png` 줄 바로 아래에 추가한다.

```
!icons/*.png
```

- [ ] **Step 4: `manifest.webmanifest` 작성**

```json
{
  "name": "지식 Archive",
  "short_name": "지식 Archive",
  "start_url": "./index.html",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#111111",
  "icons": [
    { "src": "icons/apple-touch-icon.png", "sizes": "180x180", "type": "image/png" },
    { "src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
```

- [ ] **Step 5: `index.html`의 `<head>`에 추가**

`<title>지식 Archive</title>` 바로 아래에 넣는다.

```html
  <link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
  <link rel="icon" type="image/png" href="icons/icon-512.png">
  <link rel="manifest" href="manifest.webmanifest">
  <meta name="apple-mobile-web-app-title" content="지식 Archive">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="theme-color" content="#111111">
```

- [ ] **Step 6: 브라우저에서 확인**

`preview_start`로 띄운 뒤 네트워크 요청에서 `icons/apple-touch-icon.png`와 `manifest.webmanifest`가 200으로 오는지, 탭 아이콘이 바뀌었는지 확인한다. 실제 홈 화면 추가는 배포 후 사용자가 아이폰 사파리의 "홈 화면에 추가"로 확인한다.

- [ ] **Step 7: Commit**

```bash
git add tools/make_icon.py icons manifest.webmanifest index.html .gitignore
git commit -m "feat: 아이폰 홈 화면 아이콘과 웹앱 매니페스트"
```

---

### Task 7: 리포 밖 정리와 배포 확인

- [ ] **Step 1: 지식카드 등록 스킬의 카테고리 이름 확인**

Run: `grep -rln "투자·주식\|경제·거시\|투자·금융" ~/.claude/skills ~/.claude/plugins 2>/dev/null`

나오는 파일이 있으면 사용자에게 목록을 보여주고, 옛 이름을 `경제·투자`로 바꿔도 되는지 확인받은 뒤 고친다. 이 리포 밖의 파일이므로 확인 없이 고치지 않는다. 나오는 파일이 없으면 이 단계는 끝이다.

- [ ] **Step 2: 기존 카드 페이지 링크 확인**

브라우저에서 리스트 뷰의 카드 3장을 눌러 `cards/*.html`이 정상으로 열리는지 확인한다. 카드 본문은 이 계획에서 고치지 않았다.

- [ ] **Step 3: 병합과 배포는 사용자 확인 후 진행**

`main`에 병합하면 공개 사이트(https://limpkiller-collab.github.io/knowledge-archive/)에 바로 반영된다. 병합 전에 사용자에게 확인받는다.
