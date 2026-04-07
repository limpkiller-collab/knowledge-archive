#!/usr/bin/env python3
"""v3.4 -> v3.5: Budget comma + Taichung, Expense button, Blue->White text"""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, '\ud504\ub791\uc2a4\uc5ec\ud589_\uc5ec\ud589\uc77c\uc815\ub300\uc2dc\ubcf4\ub4dc_v3.4_2026.03.30.html')
DST = os.path.join(BASE, '\ud504\ub791\uc2a4\uc5ec\ud589_\uc5ec\ud589\uc77c\uc815\ub300\uc2dc\ubcf4\ub4dc_v3.5_2026.03.30.html')

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

changes = 0

def do_replace(text, old, new, label=""):
    global changes
    if old not in text:
        print(f"  SKIP: {label}")
        return text
    changes += 1
    print(f"  OK: {label}")
    return text.replace(old, new, 1)

# ==== 1. --accent: blue -> white/dark ====
html = do_replace(html, '--accent: #3b82f6;', '--accent: #f0f0f0;', 'dark accent')
html = do_replace(html, '--accent-secondary: #8b5cf6;', '--accent-secondary: #d4d4d4;', 'dark accent-secondary')
html = do_replace(html, '--accent: #2563eb;', '--accent: #1a1a1a;', 'light accent')
html = do_replace(html, '--accent-secondary: #7c3aed;', '--accent-secondary: #404040;', 'light accent-secondary')

# ==== 2. Fix interactive elements to keep blue ====
# main-tab active
html = do_replace(html,
    'color: var(--accent);\n      border-bottom-color: var(--accent);\n      background: transparent;',
    'color: #3b82f6;\n      border-bottom-color: #3b82f6;\n      background: transparent;',
    'main-tab active')

# region-btn active
html = do_replace(html,
    '.region-btn.active {\n      background: var(--accent);',
    '.region-btn.active {\n      background: #3b82f6;',
    'region-btn active')

# in-schedule
html = do_replace(html,
    'color: var(--accent); font-weight: 500; margin-top: 6px;',
    'color: #3b82f6; font-weight: 500; margin-top: 6px;',
    'in-schedule')

# map-link
html = do_replace(html,
    '.map-link { font-size: 12px; color: var(--accent);',
    '.map-link { font-size: 12px; color: #3b82f6;',
    'map-link')

# progress-bar gradient
html = do_replace(html,
    'background: linear-gradient(90deg, var(--accent), var(--accent-secondary));',
    'background: linear-gradient(90deg, #3b82f6, #8b5cf6);',
    'progress bar gradient')

# ==== 3. Financial amounts -> gold ====
# summary-value
html = do_replace(html,
    '.summary-value {\n      font-size: 24px;\n      font-weight: 700;\n      color: var(--accent);',
    '.summary-value {\n      font-size: 24px;\n      font-weight: 700;\n      color: var(--warning, #f59e0b);',
    'summary-value')

# hotel-price-value
html = do_replace(html,
    '.hotel-price-value { font-size: 18px; font-weight: 700; color: var(--accent); }',
    '.hotel-price-value { font-size: 18px; font-weight: 700; color: var(--warning, #f59e0b); }',
    'hotel-price-value')

# budget-total was using accent color
html = do_replace(html,
    '.budget-total {\n      display: flex;\n      justify-content: space-between;\n      align-items: center;\n      padding: 12px 0;\n      border-top: 1px solid var(--border);\n      margin-top: 8px;\n      font-weight: 700;\n      color: var(--accent);',
    '.budget-total {\n      display: flex;\n      justify-content: space-between;\n      align-items: center;\n      padding: 12px 0 0;\n      margin-top: 8px;\n      border-top: 2px solid var(--border);\n      font-size: 14px;\n      font-weight: 600;',
    'budget-total')

# budget-row .amount
html = do_replace(html,
    '.budget-row .amount {\n      font-weight: 600;\n      color: var(--accent);',
    '.budget-row .amount {\n      font-weight: 600;\n      font-variant-numeric: tabular-nums;\n      text-align: right;',
    'budget-row amount')

# ==== 4. Budget CSS Taichung tweaks ====
html = do_replace(html,
    '.budget-card {\n      background: var(--surface);\n      border: 1px solid var(--border);\n      border-radius: 12px;\n      padding: 20px;\n      display: flex;\n      flex-direction: column;\n      gap: 12px;\n    }',
    '.budget-card {\n      background: var(--surface);\n      border: 1px solid var(--border);\n      border-radius: 12px;\n      padding: 20px;\n      transition: box-shadow 0.2s;\n    }\n\n    .budget-card:hover { box-shadow: 0 0 0 1px var(--border), 0 8px 16px rgba(0,0,0,0.08); }',
    'budget-card')

html = do_replace(html,
    '.budget-card h3 {\n      font-size: 16px;\n      font-weight: 700;\n      margin-bottom: 12px;\n      padding-bottom: 12px;\n      border-bottom: 1px solid var(--border);',
    '.budget-card h3 {\n      font-size: 15px;\n      font-weight: 600;\n      margin-bottom: 14px;\n      display: flex;\n      align-items: center;\n      gap: 8px;',
    'budget-card h3')

html = do_replace(html,
    '.budget-row {\n      display: flex;\n      justify-content: space-between;\n      align-items: center;\n      padding: 8px 0;\n      font-size: 14px;',
    '.budget-row {\n      display: flex;\n      justify-content: space-between;\n      align-items: center;\n      padding: 8px 0;\n      border-bottom: 1px solid var(--border);\n      font-size: 13px;',
    'budget-row')

# ==== 5. Replace renderBudgetPanel function ====
budget_start = html.index('// ===== BUDGET PANEL =====\nfunction renderBudgetPanel()')
budget_end = html.index('\n// ===== EXPENSE PANEL =====')

NEW_BUDGET = r"""// ===== BUDGET PANEL =====
function fmtNum(n) { return n.toLocaleString(); }
function fmtEUR(n) { return '\u20ac' + n.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}); }

function renderBudgetPanel() {
  const grid = document.getElementById('budgetGrid');
  grid.innerHTML = '';

  const categories = [
    { icon: '\u2708\ufe0f', name: '\ud56d\uacf5\uad8c', key: 'flight' },
    { icon: '\ud83d\ude82', name: '\uad50\ud1b5\ube44', key: 'transport' },
    { icon: '\ud83c\udf7d\ufe0f', name: '\uc2dd\ube44', key: 'meal' },
    { icon: '\ud83c\udfa1', name: '\uad00\uad11/\uccb4\ud5d8', key: 'activity' },
    { icon: '\ud83c\udfe8', name: '\uc219\uc18c', key: 'hotel' }
  ];

  categories.forEach(cat => {
    const items = BUDGET_DATA[cat.key] || [];
    let catTotalEUR = 0;
    let catTotalKRW = 0;

    let h = '<div class="budget-card"><h3>' + cat.icon + ' ' + cat.name + '</h3>';

    items.forEach(item => {
      const krw = item.currency === 'EUR' ? Math.round(item.amount * EUR_TO_KRW) : item.amount;
      let amountStr = '';
      if (item.currency === 'EUR') {
        amountStr = fmtEUR(item.amount) + '<span class="krw">\u20a9' + fmtNum(krw) + '</span>';
        catTotalEUR += item.amount;
      } else {
        amountStr = '\u20a9' + fmtNum(item.amount);
      }
      catTotalKRW += krw;
      h += '<div class="budget-row"><span class="label">' + item.label + '</span><span class="amount">' + amountStr + '</span></div>';
    });

    let subStr = '';
    if (catTotalEUR > 0) {
      subStr = fmtEUR(catTotalEUR) + '<br><span class="krw">\u20a9' + fmtNum(catTotalKRW) + '</span>';
    } else {
      subStr = '\u20a9' + fmtNum(catTotalKRW);
    }
    h += '<div class="budget-total"><span>' + cat.name + ' \uc18c\uacc4</span><span>' + subStr + '</span></div></div>';
    grid.innerHTML += h;
  });

  // Total summary card
  var allKRW = 0;
  ['transport','meal','activity','hotel','flight'].forEach(function(key) {
    (BUDGET_DATA[key] || []).forEach(function(item) {
      allKRW += item.currency === 'EUR' ? Math.round(item.amount * EUR_TO_KRW) : item.amount;
    });
  });

  var totalCard = document.createElement('div');
  totalCard.className = 'budget-card';
  totalCard.style.borderColor = 'var(--warning)';
  totalCard.style.borderWidth = '2px';

  var sh = '<h3>\ud83d\udcb0 \ucd1d \uc608\uc0c1 \uacbd\ube44</h3>';

  [
    {name: '\uad50\ud1b5\ube44', key: 'transport'},
    {name: '\uc2dd\ube44', key: 'meal'},
    {name: '\uad00\uad11/\uccb4\ud5d8', key: 'activity'},
    {name: '\uc219\uc18c', key: 'hotel'},
    {name: '\ud56d\uacf5\uad8c', key: 'flight'}
  ].forEach(function(cs) {
    var items = BUDGET_DATA[cs.key] || [];
    var eurSum = 0, krwSum = 0;
    items.forEach(function(item) {
      if (item.currency === 'EUR') {
        eurSum += item.amount;
        krwSum += Math.round(item.amount * EUR_TO_KRW);
      } else {
        krwSum += item.amount;
      }
    });
    var amtStr = '';
    if (eurSum > 0 && krwSum > Math.round(eurSum * EUR_TO_KRW)) {
      amtStr = fmtEUR(eurSum) + ' + \u20a9' + fmtNum(krwSum - Math.round(eurSum * EUR_TO_KRW)) + '<span class="krw">\u20a9' + fmtNum(krwSum) + '</span>';
    } else if (eurSum > 0) {
      amtStr = fmtEUR(eurSum) + '<span class="krw">\u20a9' + fmtNum(krwSum) + '</span>';
    } else {
      amtStr = '\u20a9' + fmtNum(krwSum);
    }
    sh += '<div class="budget-row"><span class="label">' + cs.name + '</span><span class="amount">' + amtStr + '</span></div>';
  });

  sh += '<div class="budget-total"><span>\ucd1d \ud569\uacc4</span><span style="font-size:16px;">\u20a9' + fmtNum(allKRW) + '</span></div>';

  totalCard.innerHTML = sh;
  grid.appendChild(totalCard);
}
"""

html = html[:budget_start] + NEW_BUDGET + html[budget_end:]

# ==== 6. Expense panel - add button ====
html = do_replace(html,
    '<div class="main-panel" id="panel-expense">\n  <h2>\ud83d\udcb8 \uc0ac\uc6a9\uacbd\ube44</h2>\n  <p style="color:var(--text-secondary);">\uc5ec\ud589\uc5d0\uc11c \uc0ac\uc6a9\ud55c \uc2e4\uc81c \uacbd\ube44\ub97c \ucd94\uc801\ud558\uc138\uc694</p>',
    '<div class="main-panel" id="panel-expense">\n  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">\n    <h2>\ud83d\udcb8 \uc0ac\uc6a9\uacbd\ube44</h2>\n    <button class="btn-add" onclick="openModal(\'expense\')" style="margin:0;">+ \ud83d\udcb8 \uc0ac\uc6a9\uacbd\ube44 \ucd94\uac00</button>\n  </div>\n  <p style="color:var(--text-secondary); margin-bottom:16px;">\uc5ec\ud589\uc5d0\uc11c \uc0ac\uc6a9\ud55c \uc2e4\uc81c \uacbd\ube44\ub97c \ucd94\uc801\ud558\uc138\uc694</p>',
    'expense add button')

# ==== 7. Version update ====
html = do_replace(html,
    '\ud504\ub791\uc2a4 \uc5ec\ud589 \ub300\uc2dc\ubcf4\ub4dc v3.4',
    '\ud504\ub791\uc2a4 \uc5ec\ud589 \ub300\uc2dc\ubcf4\ub4dc v3.5',
    'footer version')

html = do_replace(html,
    '<!-- Version History (\ucd5c\uc2e0\uc21c) -->\n<!-- v3.4',
    '<!-- Version History (\ucd5c\uc2e0\uc21c) -->\n<!-- v3.5 (2026.03.30) : \uc608\uc0b0\ud0ed \ucc9c\ub2e8\uc704 \ucf64\ub9c8 + \ud0c0\uc774\uc911 \ub808\uc774\uc544\uc6c3, \uc0ac\uc6a9\uacbd\ube44 \ucd94\uac00\ubc84\ud2bc, \ud30c\ub780\u2192\ud770\uc0c9 \ud14d\uc2a4\ud2b8 -->\n<!-- v3.4',
    'version history')

# ==== WRITE ====
with open(DST, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n=== v3.5 generated: {os.path.basename(DST)} ===")
print(f"    File size: {len(html):,} chars")
print(f"    Changes applied: {changes}")
print(f"    Remaining var(--accent): {html.count('var(--accent)')}")
