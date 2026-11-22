// 카드 화면 오른쪽 위의 ⋯ 메뉴: 편집(제목·분류·해시태그), 공유, 전체 화면 캡처, 삭제.
// 링크로 저장한 카드(scraps.json에 있는 카드)에서만 나타난다.
(function () {
  var DISPATCH_URL = 'https://api.github.com/repos/limpkiller-collab/knowledge-archive/dispatches';
  var CAPTURE_LIB = 'https://cdn.jsdelivr.net/npm/html-to-image@1.11.11/dist/html-to-image.js';
  var ROOT = '../';
  var key = (location.pathname.split('/').pop() || '').replace(/\.html$/, '');
  if (!/^[A-Za-z0-9_-]+$/.test(key)) return;

  var card = null;       // scraps.json 항목
  var categories = [];
  var el = {};

  var CSS = ''
    + '.km-btn{position:absolute;top:32px;right:24px;width:44px;height:44px;border:1px solid var(--border,#ddd);border-radius:50%;'
    + 'background:var(--bg,#fff);color:inherit;cursor:pointer;display:flex;align-items:center;justify-content:center;padding:0}'
    + '.km-btn:hover{border-color:currentColor}'
    + '.km-menu{position:absolute;top:82px;right:24px;z-index:20;min-width:200px;margin:0;padding:6px 0;'
    + 'background:var(--bg,#fff);color:inherit;border:1px solid var(--rule,#111);box-shadow:0 8px 24px rgba(0,0,0,.18)}'
    + '.km-menu[hidden]{display:none}'
    + '.km-menu button{display:block;width:100%;min-height:44px;padding:0 16px;border:0;background:transparent;color:inherit;'
    + 'font:inherit;font-size:15px;font-weight:700;text-align:left;cursor:pointer}'
    + '.km-menu button:hover,.km-menu button:focus-visible{background:var(--border,#ddd)}'
    + '.km-menu .km-danger{color:var(--accent,#b3261e)}'
    + '.km-dialog{width:min(92vw,480px);box-sizing:border-box;padding:24px;border:1px solid var(--rule,#111);border-radius:0;'
    + 'background:var(--bg,#fff);color:var(--text,#111);font-family:inherit}'
    + '.km-dialog::backdrop{background:rgba(0,0,0,.5)}'
    + '.km-dialog h2{font-size:20px;font-weight:900;margin:0 0 16px}'
    + '.km-dialog label{display:block;font-size:13px;font-weight:700;margin:14px 0 6px}'
    + '.km-dialog input,.km-dialog select{width:100%;box-sizing:border-box;min-height:44px;padding:8px 10px;border:1px solid var(--rule,#111);'
    + 'border-radius:0;background:var(--bg,#fff);color:inherit;font:inherit;font-size:16px}'
    + '.km-help{font-size:12px;color:var(--sec,#555);margin:6px 0 0;line-height:1.5}'
    + '.km-actions{display:flex;justify-content:flex-end;gap:8px;margin-top:20px;flex-wrap:wrap}'
    + '.km-actions button,.km-actions a{min-height:44px;padding:0 18px;border:1px solid var(--rule,#111);background:transparent;color:inherit;'
    + 'font:inherit;font-size:14px;font-weight:700;cursor:pointer;display:inline-flex;align-items:center;text-decoration:none;box-sizing:border-box}'
    + '.km-actions .km-primary{background:var(--text,#111);color:var(--bg,#fff)}'
    + '.km-actions button:disabled{opacity:.5;cursor:default}'
    + '.km-actions [hidden]{display:none}'
    + '.km-shot{display:block;max-width:100%;max-height:55vh;margin:0 auto;border:1px solid var(--border,#ddd)}'
    + '.km-toast{position:fixed;left:50%;bottom:24px;transform:translateX(-50%);z-index:50;max-width:88vw;padding:12px 18px;'
    + 'background:#111;color:#fff;font-size:14px;font-weight:700;line-height:1.5;border:1px solid #fff}'
    + '.km-toast[hidden]{display:none}';

  function h(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text) n.textContent = text;
    return n;
  }
  function decode(s) { var t = document.createElement('textarea'); t.innerHTML = s || ''; return t.value; }

  var toastTimer;
  function toast(msg, keep) {
    el.toast.textContent = msg;
    el.toast.hidden = false;
    clearTimeout(toastTimer);
    if (!keep) toastTimer = setTimeout(function () { el.toast.hidden = true; }, 5000);
  }

  function getToken() {
    var token = null;
    try { token = localStorage.getItem('ka-gh-token'); } catch (e) {}
    if (token) return token;
    token = window.prompt('이 작업에는 GitHub 토큰이 필요합니다.\n단축어에 넣은 것과 같은 토큰을 붙여넣으세요. 이 기기의 브라우저에만 저장됩니다.');
    token = token ? token.trim() : '';
    if (!token) return null;
    try { localStorage.setItem('ka-gh-token', token); } catch (e) {}
    return token;
  }

  // GitHub Actions에 작업을 요청한다. 성공하면 true.
  function dispatch(type, payload) {
    var token = getToken();
    if (!token) return Promise.resolve(false);
    return fetch(DISPATCH_URL, {
      method: 'POST',
      headers: { 'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json' },
      body: JSON.stringify({ event_type: type, client_payload: payload })
    }).then(function (r) {
      if (r.status === 204) return true;
      if (r.status === 401 || r.status === 403 || r.status === 404) {
        try { localStorage.removeItem('ka-gh-token'); } catch (e) {}
        toast('토큰이 맞지 않습니다. 다시 시도하면 토큰을 새로 묻습니다.');
      } else {
        toast('요청에 실패했습니다 (오류 ' + r.status + ').');
      }
      return false;
    }).catch(function () { toast('요청을 보내지 못했습니다. 연결을 확인해 주세요.'); return false; });
  }

  // ---------- 화면에 반영 ----------
  function showTags(tags) {
    var p = document.querySelector('main .tags');
    if (!p) {
      p = h('p', 'tags');
      var summary = document.querySelector('main .summary');
      if (!summary) return;
      summary.parentNode.insertBefore(p, summary.nextSibling);
      p.style.cssText = 'font-size:14px;font-weight:700;color:var(--accent);margin:-12px 0 24px;line-height:1.7';
    }
    p.textContent = tags.map(function (t) { return '#' + t; }).join(' ');
    p.hidden = !tags.length;
  }
  function applyToPage(title, category, tags) {
    var h1 = document.querySelector('main h1');
    if (h1) h1.textContent = title;
    document.title = title;
    var kicker = document.querySelector('main .kicker');
    if (kicker) {
      var parts = kicker.textContent.split(' · ');
      parts[0] = category;
      kicker.textContent = parts.join(' · ');
    }
    showTags(tags);
  }

  // ---------- 편집 ----------
  function openEdit() {
    var d = el.edit;
    d.querySelector('#km-title').value = card.title;
    var sel = d.querySelector('#km-category');
    sel.innerHTML = '';
    var names = categories.map(function (c) { return c.name; });
    if (names.indexOf(card.category) === -1) names.push(card.category);
    names.forEach(function (n) {
      var o = h('option', '', n); o.value = n; if (n === card.category) o.selected = true; sel.appendChild(o);
    });
    var other = h('option', '', '새 분류 직접 입력…'); other.value = '__new__'; sel.appendChild(other);
    d.querySelector('#km-newcat-wrap').hidden = true;
    d.querySelector('#km-newcat').value = '';
    d.querySelector('#km-tags').value = card.tags.map(function (t) { return '#' + t; }).join(' ');
    d.showModal();
  }
  function saveEdit(e) {
    e.preventDefault();
    var d = el.edit;
    var title = d.querySelector('#km-title').value.replace(/\s+/g, ' ').trim().slice(0, 120);
    var sel = d.querySelector('#km-category').value;
    var category = (sel === '__new__' ? d.querySelector('#km-newcat').value : sel).replace(/\s+/g, ' ').trim().slice(0, 20);
    var tags = [];
    d.querySelector('#km-tags').value.split(/[,\s]+/).forEach(function (t) {
      t = t.replace(/^#+/, '').slice(0, 30);
      if (t && tags.indexOf(t) === -1 && tags.length < 10) tags.push(t);
    });
    if (!title || !category) { toast('제목과 분류를 입력해 주세요.'); return; }
    var save = d.querySelector('.km-primary');
    save.disabled = true;
    dispatch('scrap-edit', { id: key, title: title, category: category, tags: tags }).then(function (ok) {
      save.disabled = false;
      if (!ok) return;
      card.title = title; card.category = category; card.tags = tags;
      applyToPage(title, category, tags);
      d.close();
      toast('수정을 요청했습니다. 사이트와 노션에는 1~2분 뒤 반영됩니다.');
    });
  }

  // ---------- 공유 ----------
  function share() {
    var data = { title: card.title, url: location.href.split('#')[0] };
    if (navigator.share) {
      navigator.share(data).catch(function () {});
      return;
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(data.url).then(function () { toast('카드 주소를 복사했습니다.'); },
        function () { window.prompt('카드 주소입니다. 복사해 주세요.', data.url); });
    } else {
      window.prompt('카드 주소입니다. 복사해 주세요.', data.url);
    }
  }

  // ---------- 전체 화면 캡처 ----------
  function loadCaptureLib() {
    if (window.htmlToImage) return Promise.resolve();
    return new Promise(function (resolve, reject) {
      var s = document.createElement('script');
      s.src = CAPTURE_LIB;
      s.onload = resolve;
      s.onerror = function () { reject(new Error('lib')); };
      document.head.appendChild(s);
    });
  }
  function capture() {
    toast('화면을 이미지로 만드는 중…', true);
    var main = document.querySelector('main');
    var skip = function (node) {
      var c = node.classList;
      return !(c && (c.contains('km-btn') || c.contains('km-menu') || c.contains('kg-tools') || c.contains('kg-hint')
        || c.contains('kg-nav') || c.contains('back')));
    };
    var opts = { pixelRatio: 2, backgroundColor: getComputedStyle(document.body).backgroundColor, filter: skip, cacheBust: true,
      skipFonts: true };  // 웹폰트 수백 개를 이미지에 넣느라 멈추지 않도록 기기 글꼴로 그린다
    loadCaptureLib().then(function () {
      // 사파리는 첫 번째 시도에서 이미지가 빠지는 일이 있어 한 번 더 그린다.
      return window.htmlToImage.toBlob(main, opts).then(function () { return window.htmlToImage.toBlob(main, opts); });
    }).then(function (blob) {
      if (!blob) throw new Error('empty');
      el.toast.hidden = true;
      var name = key + '.png';
      var url = URL.createObjectURL(blob);
      var d = el.shot;
      d.querySelector('img').src = url;
      var dl = d.querySelector('.km-download');
      dl.href = url; dl.download = name;
      var file = null;
      try { file = new File([blob], name, { type: 'image/png' }); } catch (e) {}
      var shareBtn = d.querySelector('.km-share-shot');
      var canShare = !!(file && navigator.canShare && navigator.canShare({ files: [file] }));
      shareBtn.hidden = !canShare;
      shareBtn.onclick = function () { navigator.share({ files: [file], title: card.title }).catch(function () {}); };
      d.showModal();
    }).catch(function () {
      toast('화면을 이미지로 만들지 못했습니다.');
    });
  }

  // ---------- 삭제 ----------
  function remove() {
    if (!window.confirm('이 카드를 삭제할까요?\n\n' + card.title + '\n\n사이트와 노션에서 함께 지워집니다.')) return;
    dispatch('scrap-delete', { id: key }).then(function (ok) {
      if (!ok) return;
      try {
        var ids = JSON.parse(localStorage.getItem('ka-deleted') || '[]');
        if (ids.indexOf(key) === -1) ids.push(key);
        localStorage.setItem('ka-deleted', JSON.stringify(ids));
      } catch (e) {}
      location.href = ROOT + 'index.html';
    });
  }

  // ---------- 화면 구성 ----------
  function dialog(html) {
    var d = h('dialog', 'km-dialog');
    d.innerHTML = html;
    document.body.appendChild(d);
    d.addEventListener('click', function (e) { if (e.target === d) d.close(); });
    Array.prototype.forEach.call(d.querySelectorAll('[data-close]'), function (b) {
      b.addEventListener('click', function () { d.close(); });
    });
    return d;
  }

  function mount() {
    var main = document.querySelector('main');
    if (!main) return;
    var style = h('style'); style.textContent = CSS; document.head.appendChild(style);
    if (getComputedStyle(main).position === 'static') main.style.position = 'relative';

    el.btn = h('button', 'km-btn');
    el.btn.type = 'button';
    el.btn.setAttribute('aria-label', '카드 메뉴');
    el.btn.setAttribute('aria-haspopup', 'menu');
    el.btn.setAttribute('aria-expanded', 'false');
    el.btn.innerHTML = '<svg aria-hidden="true" width="20" height="20" viewBox="0 0 20 20" fill="currentColor"><circle cx="4" cy="10" r="1.7"></circle><circle cx="10" cy="10" r="1.7"></circle><circle cx="16" cy="10" r="1.7"></circle></svg>';

    el.menu = h('div', 'km-menu');
    el.menu.setAttribute('role', 'menu');
    el.menu.hidden = true;
    [['편집', openEdit], ['공유', share], ['전체 화면 캡처', capture], ['삭제', remove, 'km-danger']].forEach(function (it) {
      var b = h('button', it[2] || '', it[0]);
      b.type = 'button'; b.setAttribute('role', 'menuitem');
      b.addEventListener('click', function () { closeMenu(); it[1](); });
      el.menu.appendChild(b);
    });
    main.appendChild(el.btn); main.appendChild(el.menu);

    el.toast = h('div', 'km-toast'); el.toast.setAttribute('role', 'status'); el.toast.hidden = true;
    document.body.appendChild(el.toast);

    el.edit = dialog('<form method="dialog"><h2>카드 편집</h2>'
      + '<label for="km-title">제목</label><input id="km-title" type="text" maxlength="120" required autocomplete="off">'
      + '<label for="km-category">분류</label><select id="km-category"></select>'
      + '<div id="km-newcat-wrap" hidden><label for="km-newcat">새 분류 이름</label><input id="km-newcat" type="text" maxlength="20" autocomplete="off"></div>'
      + '<label for="km-tags">해시태그</label><input id="km-tags" type="text" autocomplete="off" autocapitalize="off">'
      + '<p class="km-help">띄어쓰기나 쉼표로 구분합니다. 최대 10개.</p>'
      + '<div class="km-actions"><button type="button" data-close>취소</button><button type="submit" class="km-primary">저장</button></div></form>');
    el.edit.querySelector('form').addEventListener('submit', saveEdit);
    el.edit.querySelector('#km-category').addEventListener('change', function (e) {
      var isNew = e.target.value === '__new__';
      el.edit.querySelector('#km-newcat-wrap').hidden = !isNew;
      if (isNew) el.edit.querySelector('#km-newcat').focus();
    });

    el.shot = dialog('<h2>전체 화면 캡처</h2><img class="km-shot" alt="카드 전체 화면 이미지">'
      + '<p class="km-help">아이폰에서는 이미지를 길게 눌러 사진에 저장할 수도 있습니다.</p>'
      + '<div class="km-actions"><button type="button" data-close>닫기</button>'
      + '<button type="button" class="km-share-shot">공유</button><a class="km-download km-primary">저장</a></div>');

    el.btn.addEventListener('click', function () { el.menu.hidden ? openMenu() : closeMenu(); });
    document.addEventListener('click', function (e) {
      if (!el.menu.hidden && !el.menu.contains(e.target) && !el.btn.contains(e.target)) closeMenu();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !el.menu.hidden) { closeMenu(); el.btn.focus(); }
    });
  }
  function openMenu() {
    el.menu.hidden = false;
    el.btn.setAttribute('aria-expanded', 'true');
    el.menu.querySelector('button').focus();
  }
  function closeMenu() {
    el.menu.hidden = true;
    el.btn.setAttribute('aria-expanded', 'false');
  }

  function loadJson(path, fallback) {
    return fetch(ROOT + path, { cache: 'no-cache' })
      .then(function (r) { return r.ok ? r.json() : fallback; })
      .catch(function () { return fallback; });
  }

  function start() {
    Promise.all([loadJson('scraps.json', []), loadJson('categories.json', [])]).then(function (res) {
      var entry = (Array.isArray(res[0]) ? res[0] : []).filter(function (s) { return s.id === key; })[0];
      if (!entry) return;
      card = { title: decode(entry.title), category: decode(entry.category), tags: (entry.tags || []).map(decode) };
      categories = (Array.isArray(res[1]) ? res[1] : []).map(function (c) { return { name: c.name }; });
      mount();
      showTags(card.tags);
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
