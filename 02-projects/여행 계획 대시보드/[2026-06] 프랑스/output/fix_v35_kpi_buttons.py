#!/usr/bin/env python3
"""v3.5 -> v3.6: KPI cards match Taichung layout, CRUD buttons smaller, expense button consistent"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, '프랑스여행_여행일정대시보드_v3.5_2026.03.30.html')
DST = os.path.join(BASE, '프랑스여행_여행일정대시보드_v3.6_2026.03.30.html')

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

changes = 0

def do(text, old, new, label=""):
    global changes
    if old not in text:
        print(f"  SKIP: {label}")
        return text
    changes += 1
    print(f"  OK: {label}")
    return text.replace(old, new, 1)

# ==== 1. KPI CSS: match Taichung sizing ====
html = do(html,
    """.kpi-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      animation: fadeInUp 0.6s ease-out forwards;
      opacity: 0;
    }""",
    """.kpi-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
      transition: box-shadow 0.2s;
      animation: fadeInUp 0.6s ease-out forwards;
      opacity: 0;
    }
    .kpi-card:hover { box-shadow: 0 0 0 1px var(--border), 0 8px 16px rgba(0,0,0,0.08); }""",
    'kpi-card CSS')

html = do(html,
    """.kpi-icon {
      font-size: 32px;
      margin-bottom: 8px;
    }""",
    """.kpi-icon {
      font-size: 20px;
      margin-bottom: 8px;
      display: block;
    }""",
    'kpi-icon')

html = do(html,
    """.kpi-label {
      font-size: 13px;
      color: var(--text-secondary);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      font-weight: 600;
    }""",
    """.kpi-label {
      font-size: 12px;
      color: var(--text-secondary);
      font-weight: 500;
      letter-spacing: 0.02em;
      text-transform: uppercase;
    }""",
    'kpi-label')

html = do(html,
    """.kpi-value {
      font-size: 28px;
      font-weight: 700;
      color: var(--text);
    }""",
    """.kpi-value {
      font-size: 24px;
      font-weight: 700;
      letter-spacing: -0.02em;
      display: block;
      margin-top: 4px;
    }""",
    'kpi-value')

html = do(html,
    """.kpi-sub {
      font-size: 13px;
      color: var(--text-secondary);
    }""",
    """.kpi-sub {
      font-size: 12px;
      color: var(--text-secondary);
      margin-top: 2px;
    }""",
    'kpi-sub')

# ==== 2. KPI HTML: SVG stroke colors to match Taichung (day1~day4) ====
# First KPI icon: currentColor -> var(--day1) (blue, calendar)
html = do(html,
    'class="kpi-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4"',
    'class="kpi-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--day1)" stroke-width="2"><rect x="3" y="4"',
    'kpi icon 1 color')

# Second KPI icon: accent-secondary -> var(--day2) (purple, plane)
html = do(html,
    'class="kpi-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--accent-secondary)" stroke-width="2"><path d="M22 2L2 10l7 3 3 7z"',
    'class="kpi-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--day2)" stroke-width="2"><path d="M22 2L2 10l7 3 3 7z"',
    'kpi icon 2 color')

# Third KPI icon: positive -> var(--day3) (green, house)
html = do(html,
    'class="kpi-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--positive)" stroke-width="2"><path d="M3 9l9-7 9 7v11',
    'class="kpi-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--day3)" stroke-width="2"><path d="M3 9l9-7 9 7v11',
    'kpi icon 3 color')

# Fourth KPI icon: warning -> var(--day4) (yellow, dollar)
html = do(html,
    'class="kpi-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--warning)" stroke-width="2"><line x1="12" y1="1"',
    'class="kpi-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--day4)" stroke-width="2"><line x1="12" y1="1"',
    'kpi icon 4 color')

# ==== 3. CRUD buttons: match Taichung's compact style ====
# Replace .crud-bar .btn-add to match Taichung's .btn-add
html = do(html,
    """.crud-bar .btn-add {
      display: inline-flex; align-items: center; gap: 6px;
      padding: 8px 16px; border-radius: 20px; border: none;
      background: #3b82f6; color: #fff; font-size: 13px; font-weight: 600;
      cursor: pointer; font-family: inherit; transition: all 0.2s;
    }
    .crud-bar .btn-add:hover { opacity: 0.85; transform: translateY(-1px); }""",
    """.crud-bar .btn-add {
      display: inline-flex; align-items: center; gap: 3px;
      padding: 4px 10px; border-radius: 6px; border: none;
      background: var(--accent); color: #fff; font-size: 11px; font-weight: 500;
      cursor: pointer; font-family: inherit; transition: opacity 0.2s;
    }
    .crud-bar .btn-add:hover { opacity: 0.85; }""",
    'crud-bar btn-add compact')

# Also add SVG + icon to the schedule/expense buttons in HTML
html = do(html,
    '<button class="btn-add" onclick="openModal(\'expense\')">+ \ud83d\udcb8 \uc0ac\uc6a9\uacbd\ube44</button>\n    <button class="btn-add" onclick="openModal(\'schedule\')">+ \ud83d\udcc5 \uc77c\uc815 \ucd94\uac00</button>',
    '<button class="btn-add" onclick="openModal(\'expense\')"><svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg> \ud83d\udcb8 \uc0ac\uc6a9\uacbd\ube44</button>\n    <button class="btn-add" onclick="openModal(\'schedule\')"><svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg> \ud83d\udcc5 \uc77c\uc815 \ucd94\uac00</button>',
    'crud-bar buttons SVG icons')

# ==== 4. Expense panel: replace inline button with crud-bar style ====
html = do(html,
    """<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
    <h2>\ud83d\udcb8 \uc0ac\uc6a9\uacbd\ube44</h2>
    <button class="btn-add" onclick="openModal('expense')" style="margin:0;">+ \ud83d\udcb8 \uc0ac\uc6a9\uacbd\ube44 \ucd94\uac00</button>
  </div>
  <p style="color:var(--text-secondary); margin-bottom:16px;">\uc5ec\ud589\uc5d0\uc11c \uc0ac\uc6a9\ud55c \uc2e4\uc81c \uacbd\ube44\ub97c \ucd94\uc801\ud558\uc138\uc694</p>""",
    """<div class="crud-bar" style="margin-bottom:0;">
    <button class="btn-add" onclick="openModal('expense')"><svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg> \ud83d\udcb8 \uc0ac\uc6a9\uacbd\ube44 \ucd94\uac00</button>
  </div>
  <h2>\ud83d\udcb8 \uc0ac\uc6a9\uacbd\ube44</h2>
  <p style="color:var(--text-secondary); margin-bottom:16px;">\uc5ec\ud589\uc5d0\uc11c \uc0ac\uc6a9\ud55c \uc2e4\uc81c \uacbd\ube44\ub97c \ucd94\uc801\ud558\uc138\uc694</p>""",
    'expense panel crud-bar button')

# ==== 5. Also update JS-generated food/cafe crud buttons to use SVG ====
html = do(html,
    """crudBar.innerHTML = '<button class="btn-add" onclick="openModal(\\'food\\')">+ \ud83c\udf5c \ub9db\uc9d1 \ucd94\uac00</button>';""",
    """crudBar.innerHTML = '<button class="btn-add" onclick="openModal(\\'food\\')"><svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg> \ud83c\udf5c \ub9db\uc9d1 \ucd94\uac00</button>';""",
    'food crud SVG icon')

html = do(html,
    """crudBar.innerHTML = '<button class="btn-add" onclick="openModal(\\'cafe\\')">+ \u2615 \uce74\ud398 \ucd94\uac00</button>';""",
    """crudBar.innerHTML = '<button class="btn-add" onclick="openModal(\\'cafe\\')"><svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg> \u2615 \uce74\ud398 \ucd94\uac00</button>';""",
    'cafe crud SVG icon')

# ==== 6. Version update ====
html = do(html,
    '\ud504\ub791\uc2a4 \uc5ec\ud589 \ub300\uc2dc\ubcf4\ub4dc v3.5',
    '\ud504\ub791\uc2a4 \uc5ec\ud589 \ub300\uc2dc\ubcf4\ub4dc v3.6',
    'footer version')

html = do(html,
    '<!-- Version History (\ucd5c\uc2e0\uc21c) -->\n<!-- v3.5',
    '<!-- Version History (\ucd5c\uc2e0\uc21c) -->\n<!-- v3.6 (2026.03.30) : KPI \uce74\ub4dc \ud0c0\uc774\uc911 \ub808\uc774\uc544\uc6c3 \uc801\uc6a9, CRUD \ubc84\ud2bc \ucf4c\ud329\ud2b8\ud654, \uc0ac\uc6a9\uacbd\ube44 \ubc84\ud2bc \ud1b5\uc77c -->\n<!-- v3.5',
    'version history')

# ==== WRITE ====
with open(DST, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n=== v3.6 generated: {os.path.basename(DST)} ===")
print(f"    File size: {len(html):,} chars")
print(f"    Changes applied: {changes}")
