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

  // 카드 파일 이름(확장자 제외). 직접 추가한 이미지 목록(card-images.json)의 키로 쓴다.
  function cardKey(card) {
    return String((card && card.file) || '').split('/').pop().replace(/\.html$/, '');
  }

  // 카드에서 넘겨 볼 이미지 목록. 게시물 이미지(없으면 커버 한 장) 뒤에 직접 추가한 이미지가 붙는다.
  function galleryFor(card, added) {
    var base = card && card.images && card.images.length ? card.images : (card && card.cover ? [card.cover] : []);
    return base.map(function (p) { return { path: p, added: false }; })
      .concat((added || []).map(function (p) { return { path: p, added: true }; }));
  }

  // 직접 추가한 이미지 목록을 고친 새 객체를 돌려준다. 이미지가 하나도 남지 않은 카드는 키를 지운다.
  function editManifest(manifest, key, add, remove) {
    var out = {};
    Object.keys(manifest || {}).forEach(function (k) { out[k] = manifest[k].slice(); });
    var list = (out[key] || []).filter(function (p) { return (remove || []).indexOf(p) === -1; });
    (add || []).forEach(function (p) { if (list.indexOf(p) === -1) list.push(p); });
    if (list.length) out[key] = list; else delete out[key];
    return out;
  }

  return {
    mergeCards: mergeCards, filterCards: filterCards, countByCategory: countByCategory,
    coverFor: coverFor, typeLabel: typeLabel, TYPE_LABELS: TYPE_LABELS,
    cardKey: cardKey, galleryFor: galleryFor, editManifest: editManifest
  };
});
