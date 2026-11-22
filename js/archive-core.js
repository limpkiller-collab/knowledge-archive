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
