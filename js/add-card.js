// 대시보드에서 링크나 사진·PDF 파일을 직접 보내 카드를 만든다.
// 링크는 단축어와 같은 요청(scrap-link)을 보내고, 파일은 비공개 저장소(받은 파일함)에 올린 뒤 scrap-file을 요청한다.
(function () {
  var API = 'https://api.github.com/repos/';
  var REPO = 'limpkiller-collab/knowledge-archive';
  var INBOX = 'limpkiller-collab/knowledge-archive-inbox';
  var TOKEN_KEY = 'ka-gh-token';
  var MAX_FILES = 12;
  var MAX_FILE_BYTES = 25 * 1024 * 1024;
  var NEW = '__new__';
  var d, fab, toastEl, toastTimer, busy = false;

  var css = ''
    + '.ac-fab{position:fixed;right:20px;bottom:calc(20px + env(safe-area-inset-bottom,0px));z-index:40;width:56px;height:56px;'
    + 'display:flex;align-items:center;justify-content:center;border:1px solid var(--rule);background:var(--text);color:var(--bg);cursor:pointer}'
    + '.ac-fab:hover{background:var(--accent);border-color:var(--accent)}'
    + '.ac-dialog{width:min(92vw,480px);max-height:90vh;overflow:auto;box-sizing:border-box;margin:auto;padding:24px;border:1px solid var(--rule);border-radius:0;'
    + 'background:var(--bg);color:var(--text);font:inherit}'
    + '.ac-dialog::backdrop{background:rgba(0,0,0,.5)}'
    + '.ac-dialog h2{font-size:20px;font-weight:900;margin:0 0 4px}'
    + '.ac-dialog label{display:block;font-size:13px;font-weight:700;margin:16px 0 6px}'
    + '.ac-dialog input,.ac-dialog select,.ac-dialog textarea{width:100%;box-sizing:border-box;min-height:44px;padding:8px 10px;'
    + 'border:1px solid var(--rule);border-radius:0;background:var(--bg);color:var(--text);font:inherit;font-size:16px}'
    + '.ac-dialog textarea{min-height:72px;resize:vertical}'
    + '.ac-dialog input[type=file]{padding:9px 10px;font-size:14px}'
    + '.ac-hint{font-size:12px;line-height:1.5;color:var(--text-sec);margin-top:6px}'
    + '.ac-or{font-size:12px;font-weight:700;color:var(--text-sec);margin:16px 0 -8px}'
    + '.ac-status{font-size:13px;font-weight:700;line-height:1.5;margin-top:16px;min-height:20px}'
    + '.ac-status.error{color:var(--accent)}'
    + '.ac-actions{display:flex;justify-content:flex-end;gap:8px;margin-top:12px}'
    + '.ac-actions button{min-height:44px;padding:0 18px;border:1px solid var(--rule);background:transparent;color:inherit;'
    + 'font:inherit;font-size:14px;font-weight:700;cursor:pointer}'
    + '.ac-actions .ac-primary{background:var(--text);color:var(--bg)}'
    + '.ac-actions button:disabled{opacity:.5;cursor:default}'
    + '.ac-toast{position:fixed;left:50%;bottom:calc(24px + env(safe-area-inset-bottom,0px));transform:translateX(-50%);z-index:60;'
    + 'width:max-content;max-width:calc(100vw - 32px);box-sizing:border-box;padding:12px 16px;background:var(--text);color:var(--bg);'
    + 'font-size:14px;font-weight:700;line-height:1.5}'
    + '.ac-toast[hidden]{display:none}';

  function $(sel) { return d.querySelector(sel); }

  function status(msg, isError) {
    var el = $('.ac-status');
    el.textContent = msg || '';
    el.className = 'ac-status' + (isError ? ' error' : '');
  }

  function toast(msg) {
    toastEl.textContent = msg;
    toastEl.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.hidden = true; }, 6000);
  }

  function getToken() {
    var token = null;
    try { token = localStorage.getItem(TOKEN_KEY); } catch (e) {}
    if (token) return token;
    token = window.prompt('카드를 만들려면 GitHub 토큰이 필요합니다.\n단축어에 넣은 것과 같은 토큰을 붙여넣으세요. 이 기기의 브라우저에만 저장됩니다.');
    token = token ? token.trim() : '';
    if (!token) return null;
    try { localStorage.setItem(TOKEN_KEY, token); } catch (e) {}
    return token;
  }
  function forgetToken() { try { localStorage.removeItem(TOKEN_KEY); } catch (e) {} }

  function call(token, path, method, body) {
    return fetch(API + path, {
      method: method,
      headers: { 'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json' },
      body: JSON.stringify(body)
    });
  }

  // 붙여넣은 글에서 주소만 골라낸다. 공유한 글에는 제목이 함께 붙어 오는 일이 많다.
  function pickUrl(text) {
    var m = /https?:\/\/[^\s<>"']+/i.exec(text || '');
    if (!m) return '';
    try { return new URL(m[0]).href; } catch (e) { return ''; }
  }

  function batchName(now) {
    function p(n) { return (n < 10 ? '0' : '') + n; }
    return 'web-' + now.getFullYear() + p(now.getMonth() + 1) + p(now.getDate()) + '-'
      + p(now.getHours()) + p(now.getMinutes()) + p(now.getSeconds());
  }

  function toBase64(file) {
    return new Promise(function (resolve, reject) {
      var r = new FileReader();
      r.onload = function () { resolve(String(r.result).split(',')[1] || ''); };
      r.onerror = function () { reject(new Error('read')); };
      r.readAsDataURL(file);
    });
  }

  function fail(msg) { var e = new Error(msg); e.shown = true; return e; }

  function dispatch(token, type, payload) {
    return call(token, REPO + '/dispatches', 'POST', { event_type: type, client_payload: payload }).then(function (r) {
      if (r.status === 204) return;
      if (r.status === 401 || r.status === 403 || r.status === 404) {
        forgetToken();
        throw fail('토큰이 맞지 않습니다. 다시 보내면 토큰을 새로 묻습니다.');
      }
      throw fail('요청에 실패했습니다 (오류 ' + r.status + ').');
    });
  }

  // 파일을 받은 파일함에 차례로 올린다. 한꺼번에 올리면 저장소에서 서로 부딪친다.
  function upload(token, batch, files) {
    var chain = Promise.resolve();
    files.forEach(function (file, i) {
      chain = chain.then(function () {
        status('파일 올리는 중 (' + (i + 1) + '/' + files.length + ')…');
        return toBase64(file);
      }).then(function (content) {
        return call(token, INBOX + '/contents/inbox/' + batch + '/' + (i + 1), 'PUT',
          { message: 'inbox: ' + batch + ' ' + (i + 1), content: content });
      }).then(function (r) {
        if (r.status === 201 || r.status === 200) return;
        if (r.status === 401) {
          forgetToken();
          throw fail('토큰이 맞지 않습니다. 다시 보내면 토큰을 새로 묻습니다.');
        }
        if (r.status === 403 || r.status === 404) {
          throw fail('이 토큰으로는 받은 파일함(knowledge-archive-inbox)에 올릴 수 없습니다. 토큰에 그 저장소의 Contents 쓰기 권한이 있는지 확인해 주세요.');
        }
        throw fail('파일을 올리지 못했습니다 (오류 ' + r.status + ').');
      });
    });
    return chain;
  }

  function submit(e) {
    e.preventDefault();
    if (busy) return;
    var raw = $('#ac-url').value.trim();
    var files = Array.prototype.slice.call($('#ac-files').files || []);
    var url = pickUrl(raw);
    if (!raw && !files.length) return status('링크를 붙여넣거나 파일을 골라 주세요.', true);
    if (raw && files.length) return status('링크와 파일은 따로 보내 주세요. 한 번에 하나만 카드로 만듭니다.', true);
    if (raw && !url) return status('링크 주소를 찾지 못했습니다. http로 시작하는 주소를 넣어 주세요.', true);
    if (files.length > MAX_FILES) return status('파일은 한 번에 ' + MAX_FILES + '개까지 보낼 수 있습니다.', true);
    if (files.some(function (f) { return f.size > MAX_FILE_BYTES; })) return status('파일 하나는 25MB까지 보낼 수 있습니다.', true);

    var category = $('#ac-category').value;
    if (category === NEW) category = $('#ac-new-category').value.replace(/\s+/g, ' ').trim().slice(0, 20);
    var note = $('#ac-note').value.trim();
    var token = getToken();
    if (!token) return;

    busy = true;
    $('.ac-primary').disabled = true;
    var work;
    if (files.length) {
      var batch = batchName(new Date());
      work = upload(token, batch, files).then(function () {
        status('카드 정리를 요청하는 중…');
        return dispatch(token, 'scrap-file', { batch: batch, category: category, note: note });
      });
    } else {
      status('카드 정리를 요청하는 중…');
      work = dispatch(token, 'scrap-link', { url: url, category: category, note: note });
    }
    work.then(function () {
      $('form').reset();
      $('#ac-new-category').hidden = true;
      status('');
      d.close();
      toast('보냈습니다. 1~2분 뒤 카드가 만들어지고 알림이 옵니다.');
    }).catch(function (err) {
      status(err && err.shown ? err.message : '보내지 못했습니다. 연결을 확인해 주세요.', true);
    }).then(function () {
      busy = false;
      $('.ac-primary').disabled = false;
    });
  }

  function fillCategories() {
    var sel = $('#ac-category');
    fetch('categories.json', { cache: 'no-store' })
      .then(function (r) { return r.ok ? r.json() : []; })
      .catch(function () { return []; })
      .then(function (list) {
        sel.innerHTML = '';
        var names = (Array.isArray(list) ? list : []).map(function (c) { return c.name; });
        [['', '자동 분류']].concat(names.map(function (n) { return [n, n]; }), [[NEW, '새 분류 직접 입력…']]).forEach(function (o) {
          var opt = document.createElement('option');
          opt.value = o[0]; opt.textContent = o[1];
          sel.appendChild(opt);
        });
      });
  }

  function open() {
    status('');
    fillCategories();
    d.showModal();
  }

  function mount() {
    var style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);

    fab = document.createElement('button');
    fab.type = 'button';
    fab.className = 'ac-fab';
    fab.setAttribute('aria-label', '카드 추가');
    fab.innerHTML = '<svg aria-hidden="true" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="square"><path d="M12 5v14M5 12h14"></path></svg>';
    fab.addEventListener('click', open);
    document.body.appendChild(fab);

    toastEl = document.createElement('div');
    toastEl.className = 'ac-toast';
    toastEl.setAttribute('role', 'status');
    toastEl.hidden = true;
    document.body.appendChild(toastEl);

    d = document.createElement('dialog');
    d.className = 'ac-dialog';
    d.innerHTML = '<form><h2>카드 추가</h2>'
      + '<p class="ac-hint">링크나 파일을 보내면 내용을 읽어 카드로 정리합니다.</p>'
      + '<label for="ac-url">링크</label><input id="ac-url" type="text" inputmode="url" autocomplete="off" autocapitalize="off" placeholder="https://">'
      + '<p class="ac-or">또는</p>'
      + '<label for="ac-files">사진·PDF 파일</label><input id="ac-files" type="file" multiple accept="image/*,application/pdf,.heic,.heif">'
      + '<p class="ac-hint">보낸 사진은 카드에 실려 공개됩니다. PDF 원본은 공개되지 않고 요약만 올라갑니다.</p>'
      + '<label for="ac-category">분류</label><select id="ac-category"><option value="">자동 분류</option></select>'
      + '<input id="ac-new-category" type="text" maxlength="20" placeholder="새 분류 이름" aria-label="새 분류 이름" hidden style="margin-top:8px">'
      + '<label for="ac-note">메모 (선택)</label><textarea id="ac-note" maxlength="500"></textarea>'
      + '<p class="ac-hint">메모는 노션에만 저장되고 사이트에는 올라가지 않습니다.</p>'
      + '<p class="ac-status" role="status" aria-live="polite"></p>'
      + '<div class="ac-actions"><button type="button" data-close>닫기</button><button type="submit" class="ac-primary">보내기</button></div></form>';
    document.body.appendChild(d);
    d.querySelector('form').addEventListener('submit', submit);
    d.querySelector('[data-close]').addEventListener('click', function () { d.close(); });
    d.addEventListener('click', function (e) { if (e.target === d && !busy) d.close(); });
    $('#ac-category').addEventListener('change', function (e) {
      var isNew = e.target.value === NEW;
      $('#ac-new-category').hidden = !isNew;
      if (isNew) $('#ac-new-category').focus();
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
  else mount();
})();
