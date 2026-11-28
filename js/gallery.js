// 카드 화면의 이미지 갤러리. 좌우로 넘겨 보고, 내 사진을 추가하거나 지운다.
// 추가한 이미지는 GitHub 리포의 covers/<카드>/u-*.jpg 로 올라가고 목록은 card-images.json 에 적힌다.
(function () {
  var REPO = 'limpkiller-collab/knowledge-archive';
  var API = 'https://api.github.com/repos/' + REPO;
  var BRANCH = 'main';
  var MANIFEST = 'card-images.json';
  var MAX_SIDE = 1600;
  var MAX_FILES = 10;
  var ROOT = '../';

  var key = (location.pathname.split('/').pop() || '').replace(/\.html$/, '');
  if (!/^[A-Za-z0-9_-]+$/.test(key) || !window.ArchiveCore) return;

  var items = [];   // { path, added, src }
  var index = 0;
  var busy = false;
  var el = {};

  var CSS = ''
    + '.kg{margin:0 0 24px;color:inherit;font-family:inherit}'
    + '.kg.kg-append{max-width:720px;margin:48px auto 0;padding:0 24px 96px;box-sizing:border-box}'
    + '.kg-head{font-size:13px;font-weight:700;letter-spacing:.04em;margin:0 0 10px;opacity:.75}'
    + '.kg-frame{position:relative;background:#111;aspect-ratio:1/1;max-height:min(80vh,720px);overflow:hidden}'
    + '.kg-track{display:flex;width:100%;height:100%;overflow-x:auto;overflow-y:hidden;scroll-snap-type:x mandatory;'
    + '-webkit-overflow-scrolling:touch;scrollbar-width:none;overscroll-behavior-x:contain}'
    + '.kg-track::-webkit-scrollbar{display:none}'
    + '.kg-track:focus-visible{outline:3px solid #ff8a80;outline-offset:-3px}'
    + '.kg-slide{flex:0 0 100%;height:100%;scroll-snap-align:center;scroll-snap-stop:always;display:flex;align-items:center;justify-content:center}'
    + '.kg-slide img{width:100%;height:100%;object-fit:contain;display:block;margin:0}'
    + '.kg-nav{position:absolute;top:50%;transform:translateY(-50%);width:44px;height:44px;border:0;border-radius:50%;'
    + 'background:rgba(255,255,255,.92);color:#111;font-size:22px;line-height:1;cursor:pointer;display:none;align-items:center;justify-content:center;padding:0;'
    // 평소에는 옅게 두어 사진 속 글을 가리지 않고, 마우스를 올리거나 초점이 가면 또렷해진다.
    + 'opacity:.28;box-shadow:0 0 0 1px rgba(0,0,0,.3);transition:opacity .15s}'
    + '.kg-nav:hover,.kg-nav:focus-visible{opacity:1}'
    + '.kg-prev{left:10px}.kg-next{right:10px}'
    + '@media (hover:hover){.kg-nav{display:flex}}'
    + '.kg-nav[hidden]{display:none}'
    + '.kg-count{position:absolute;top:10px;right:10px;background:rgba(17,17,17,.78);color:#fff;font-size:12px;font-weight:700;'
    + 'padding:4px 9px;border-radius:999px;letter-spacing:0}'
    + '.kg-dots{display:flex;justify-content:center;gap:6px;padding:10px 0 0;flex-wrap:wrap}'
    + '.kg-dot{width:6px;height:6px;border-radius:50%;background:currentColor;opacity:.25}'
    + '.kg-dot[aria-current="true"]{opacity:1}'
    + '.kg-tools{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-top:12px}'
    + '.kg-btn{min-height:44px;padding:0 16px;border:1px solid currentColor;background:transparent;color:inherit;'
    + 'font:inherit;font-size:14px;font-weight:700;cursor:pointer;border-radius:0}'
    + '.kg-btn:disabled{opacity:.45;cursor:default}'
    + '.kg-status{font-size:13px;line-height:1.5;opacity:.8;flex:1 1 200px}'
    + '.kg-hint{font-size:12px;line-height:1.5;opacity:.6;margin:8px 0 0}';

  function h(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text) n.textContent = text;
    return n;
  }

  function mount() {
    var style = h('style');
    style.textContent = CSS;
    document.head.appendChild(style);

    var root = h('section', 'kg');
    root.setAttribute('aria-label', '이미지');
    var slot = document.getElementById('ka-gallery');
    var oldCover = document.querySelector('main > img.cover');
    if (slot) { slot.innerHTML = ''; slot.appendChild(root); }
    else if (oldCover) { oldCover.parentNode.replaceChild(root, oldCover); }
    else {
      root.className = 'kg kg-append';
      el.head = h('p', 'kg-head', '추가한 이미지');
      root.appendChild(el.head);
      (document.querySelector('main') || document.body).appendChild(root);
    }

    el.frame = h('div', 'kg-frame');
    el.track = h('div', 'kg-track');
    el.track.tabIndex = 0;
    el.track.setAttribute('role', 'group');
    el.track.setAttribute('aria-label', '이미지 넘겨 보기');
    el.prev = h('button', 'kg-nav kg-prev', '‹');
    el.prev.type = 'button';
    el.prev.setAttribute('aria-label', '이전 이미지');
    el.next = h('button', 'kg-nav kg-next', '›');
    el.next.type = 'button';
    el.next.setAttribute('aria-label', '다음 이미지');
    el.count = h('span', 'kg-count');
    el.frame.appendChild(el.track); el.frame.appendChild(el.prev); el.frame.appendChild(el.next); el.frame.appendChild(el.count);
    el.dots = h('div', 'kg-dots');
    el.dots.setAttribute('aria-hidden', 'true');

    var tools = h('div', 'kg-tools');
    el.add = h('button', 'kg-btn', '이미지 추가');
    el.add.type = 'button';
    el.del = h('button', 'kg-btn', '이 이미지 삭제');
    el.del.type = 'button';
    el.status = h('span', 'kg-status');
    el.status.setAttribute('role', 'status');
    tools.appendChild(el.add); tools.appendChild(el.del); tools.appendChild(el.status);
    el.file = h('input');
    el.file.type = 'file'; el.file.accept = 'image/*'; el.file.multiple = true; el.file.hidden = true;

    root.appendChild(el.frame); root.appendChild(el.dots); root.appendChild(tools);
    root.appendChild(h('p', 'kg-hint', '추가한 이미지는 공개 사이트에 올라갑니다. 주소를 아는 사람은 누구나 볼 수 있습니다.'));
    root.appendChild(el.file);

    el.prev.addEventListener('click', function () { go(locate() - 1); });
    el.next.addEventListener('click', function () { go(locate() + 1); });
    el.track.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { e.preventDefault(); go(locate() - 1); }
      if (e.key === 'ArrowRight') { e.preventDefault(); go(locate() + 1); }
    });
    el.track.addEventListener('scroll', locate, { passive: true });
    el.add.addEventListener('click', function () { if (!busy) el.file.click(); });
    el.file.addEventListener('change', function () {
      var files = Array.prototype.slice.call(el.file.files || []);
      el.file.value = '';
      if (files.length) addFiles(files);
    });
    el.del.addEventListener('click', removeCurrent);
  }

  // 지금 화면에 보이는 장을 스크롤 위치에서 다시 계산한다.
  function locate() {
    var w = el.track.clientWidth || 1;
    var i = Math.max(0, Math.min(items.length - 1, Math.round(el.track.scrollLeft / w)));
    if (i !== index) { index = i; sync(); }
    return index;
  }

  function go(i) {
    if (i < 0 || i >= items.length) return;
    el.track.scrollTo({ left: i * el.track.clientWidth, behavior: 'smooth' });
  }

  function render(keepIndex) {
    index = Math.max(0, Math.min(items.length - 1, keepIndex || 0));
    el.track.innerHTML = '';
    items.forEach(function (it, i) {
      var slide = h('div', 'kg-slide');
      var img = h('img');
      img.alt = (it.added ? '추가한 이미지 ' : '이미지 ') + (i + 1) + ' / ' + items.length;
      if (i > 1) img.loading = 'lazy';
      img.src = it.src;
      if (i === 0) img.addEventListener('load', function () {
        // 틀의 비율은 첫 장을 따른다. 너무 길거나 납작하지 않게 4:5 ~ 1.91:1 사이로 잡는다.
        var r = img.naturalWidth / (img.naturalHeight || 1);
        el.frame.style.aspectRatio = String(Math.max(0.8, Math.min(1.91, r || 1)));
      });
      slide.appendChild(img);
      el.track.appendChild(slide);
    });
    el.dots.innerHTML = '';
    if (items.length > 1) items.forEach(function () { el.dots.appendChild(h('span', 'kg-dot')); });
    var has = items.length > 0;
    el.frame.hidden = !has;
    el.dots.hidden = items.length < 2;
    if (el.head) el.head.hidden = !has;
    var target = index;
    el.track.scrollLeft = target * el.track.clientWidth;  // 스크롤 이벤트가 index를 바꾸기 전에 자리를 잡는다
    index = target;
    sync();
  }

  function sync() {
    var many = items.length > 1;
    el.count.hidden = !many;
    el.count.textContent = (index + 1) + ' / ' + items.length;
    el.prev.hidden = !many || index === 0;
    el.next.hidden = !many || index === items.length - 1;
    Array.prototype.forEach.call(el.dots.children, function (d, i) {
      d.setAttribute('aria-current', String(i === index));
    });
    var cur = items[index];
    el.del.hidden = !(cur && cur.added);
    el.del.disabled = busy;
    el.add.disabled = busy;
  }

  function say(msg) { el.status.textContent = msg || ''; }

  // ---------- GitHub ----------
  function getToken(forceAsk) {
    var token = null;
    try { token = localStorage.getItem('ka-gh-token'); } catch (e) {}
    if (token && !forceAsk) return token;
    token = window.prompt('이미지를 올리려면 GitHub 토큰이 필요합니다.\n단축어에 넣은 것과 같은 토큰을 붙여넣으세요. 이 기기의 브라우저에만 저장됩니다.');
    token = token ? token.trim() : '';
    if (!token) return null;
    try { localStorage.setItem('ka-gh-token', token); } catch (e) {}
    return token;
  }

  function api(token, path, method, body, raw) {
    return fetch(API + path, {
      method: method || 'GET',
      headers: { 'Authorization': 'Bearer ' + token, 'Accept': raw ? 'application/vnd.github.raw+json' : 'application/vnd.github+json' },
      body: body ? JSON.stringify(body) : undefined
    }).then(function (r) {
      if (!r.ok) { var err = new Error('GitHub ' + r.status); err.status = r.status; throw err; }
      return raw ? r.text() : r.json();
    });
  }

  // 이미지 추가·삭제와 목록 수정을 커밋 하나로 올린다. 그 사이 다른 커밋이 들어오면 처음부터 다시 한다.
  function commit(token, addBlobs, removePaths, message, attempt) {
    var head;
    return api(token, '/git/ref/heads/' + BRANCH).then(function (ref) {
      head = ref.object.sha;
      return Promise.all([
        api(token, '/git/commits/' + head),
        api(token, '/contents/' + MANIFEST + '?ref=' + head, 'GET', null, true)
          .then(function (t) { return JSON.parse(t); })
          .catch(function (e) { if (e.status === 404) return {}; throw e; })
      ]);
    }).then(function (res) {
      var manifest = ArchiveCore.editManifest(res[1], key, addBlobs.map(function (b) { return b.path; }), removePaths);
      var tree = addBlobs.map(function (b) { return { path: b.path, mode: '100644', type: 'blob', sha: b.sha }; })
        .concat(removePaths.map(function (p) { return { path: p, mode: '100644', type: 'blob', sha: null }; }))
        .concat([{ path: MANIFEST, mode: '100644', type: 'blob', content: JSON.stringify(manifest, null, 2) + '\n' }]);
      return api(token, '/git/trees', 'POST', { base_tree: res[0].tree.sha, tree: tree });
    }).then(function (tree) {
      return api(token, '/git/commits', 'POST', { message: message, tree: tree.sha, parents: [head] });
    }).then(function (c) {
      return api(token, '/git/refs/heads/' + BRANCH, 'PATCH', { sha: c.sha });
    }).catch(function (e) {
      if (e.status === 422 && (attempt || 0) < 3) return commit(token, addBlobs, removePaths, message, (attempt || 0) + 1);
      throw e;
    });
  }

  function explain(e) {
    if (e && (e.status === 401 || e.status === 403 || e.status === 404)) {
      try { localStorage.removeItem('ka-gh-token'); } catch (x) {}
      return '토큰이 맞지 않거나 권한이 없습니다. 다시 시도하면 토큰을 새로 묻습니다.';
    }
    if (e && e.status) return '올리지 못했습니다 (오류 ' + e.status + ').';
    return '올리지 못했습니다. 연결을 확인해 주세요.';
  }

  // 사진을 긴 변 1600px 이하의 JPEG으로 줄인다.
  function shrink(file) {
    return new Promise(function (resolve, reject) {
      var url = URL.createObjectURL(file);
      var img = new Image();
      img.onload = function () {
        var scale = Math.min(1, MAX_SIDE / Math.max(img.naturalWidth, img.naturalHeight));
        var canvas = document.createElement('canvas');
        canvas.width = Math.max(1, Math.round(img.naturalWidth * scale));
        canvas.height = Math.max(1, Math.round(img.naturalHeight * scale));
        var ctx = canvas.getContext('2d');
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        URL.revokeObjectURL(url);
        var dataUrl = canvas.toDataURL('image/jpeg', 0.85);
        resolve({ base64: dataUrl.split(',')[1], preview: dataUrl });
      };
      img.onerror = function () { URL.revokeObjectURL(url); reject(new Error('읽을 수 없는 이미지')); };
      img.src = url;
    });
  }

  function addFiles(files) {
    files = files.filter(function (f) { return /^image\//.test(f.type) || !f.type; });
    if (!files.length) return;
    if (files.length > MAX_FILES) { say('한 번에 ' + MAX_FILES + '장까지 올릴 수 있습니다.'); return; }
    var agreed = false;
    try { agreed = localStorage.getItem('ka-img-public-ok') === '1'; } catch (e) {}
    if (!agreed) {
      if (!window.confirm('추가한 이미지는 공개 사이트에 올라가 주소를 아는 누구나 볼 수 있습니다.\n계속할까요?')) return;
      try { localStorage.setItem('ka-img-public-ok', '1'); } catch (e) {}
    }
    var token = getToken(false);
    if (!token) return;
    busy = true; sync();
    say('이미지 준비 중…');
    var stamp = Date.now().toString(36);
    var shrunk;
    Promise.all(files.map(shrink)).then(function (list) {
      shrunk = list;
      say('올리는 중… (' + list.length + '장)');
      // 한 장씩 차례로 올린다.
      return list.reduce(function (chain, it, i) {
        return chain.then(function (blobs) {
          return api(token, '/git/blobs', 'POST', { content: it.base64, encoding: 'base64' }).then(function (b) {
            return blobs.concat([{ path: 'covers/' + key + '/u-' + stamp + '-' + (i + 1) + '.jpg', sha: b.sha }]);
          });
        });
      }, Promise.resolve([]));
    }).then(function (blobs) {
      return commit(token, blobs, [], 'images: ' + key + ' 이미지 ' + blobs.length + '장 추가').then(function () { return blobs; });
    }).then(function (blobs) {
      var first = items.length;
      blobs.forEach(function (b, i) { items.push({ path: b.path, added: true, src: shrunk[i].preview }); });
      busy = false;
      render(first);
      say(blobs.length + '장을 추가했습니다. 다른 기기에는 1분쯤 뒤에 보입니다.');
    }).catch(function (e) {
      busy = false; sync();
      say(e && e.status === undefined && e.message === '읽을 수 없는 이미지' ? '읽을 수 없는 이미지가 있어 올리지 않았습니다.' : explain(e));
    });
  }

  function removeCurrent() {
    var cur = items[locate()];
    if (busy || !cur || !cur.added) return;
    if (!window.confirm('이 이미지를 삭제할까요?')) return;
    var token = getToken(false);
    if (!token) return;
    busy = true; sync();
    say('삭제하는 중…');
    commit(token, [], [cur.path], 'images: ' + key + ' 이미지 1장 삭제').then(function () {
      items.splice(index, 1);
      busy = false;
      render(Math.min(index, items.length - 1));
      say('삭제했습니다.');
    }).catch(function (e) {
      busy = false; sync();
      say(explain(e).replace('올리지', '삭제하지'));
    });
  }

  // ---------- 시작 ----------
  function loadJson(path, fallback) {
    return fetch(ROOT + path, { cache: 'no-cache' })
      .then(function (r) { return r.ok ? r.json() : fallback; })
      .catch(function () { return fallback; });
  }

  function start() {
    var cover = document.querySelector('#ka-gallery img.cover, main > img.cover');
    var first = cover && cover.getAttribute('src');
    if (first) items = [{ path: first.replace(/^\.\.\//, ''), added: false, src: first }];
    mount();
    render(0);
    Promise.all([loadJson('scraps.json', []), loadJson(MANIFEST, {})]).then(function (res) {
      var scrap = (Array.isArray(res[0]) ? res[0] : []).filter(function (s) { return s.id === key; })[0] || {};
      var added = (res[1] && Array.isArray(res[1][key])) ? res[1][key] : [];
      items = ArchiveCore.galleryFor(scrap, added).map(function (g) {
        return { path: g.path, added: g.added, src: ROOT + g.path };
      });
      render(0);
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
