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
