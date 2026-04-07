// ★ 자산관리 대시보드 - Google Apps Script (서버 로직)
const SPREADSHEET_ID = '17fqFEr64RYlHbb-ZezI-7x7FSNETu6xAxQoJCEoGMqU';

// ──────────────────────────────────────────────
// 웹앱 진입점
// ──────────────────────────────────────────────
function doGet(e) {
  const monthly     = getMonthlyData();
  const planActual  = getPlanActualData();
  const budget      = getBudgetData();
  const budgetChart = buildBudgetChart(budget);

  const now = new Date();
  const updatedStr = now.getFullYear() + '년 ' + (now.getMonth()+1) + '월 ' +
                     now.getDate() + '일 ' + now.getHours() + ':' +
                     String(now.getMinutes()).padStart(2, '0');

  const tmpl = HtmlService.createTemplateFromFile('dashboard');
  tmpl.monthlyJSON    = JSON.stringify(monthly);
  tmpl.planActualJSON = JSON.stringify(planActual);
  tmpl.budgetJSON     = JSON.stringify(budgetChart);
  tmpl.updatedStr     = updatedStr;

  // ── 임베드 모드 지원 (통합 대시보드 iframe용) ──
  const param = (e && e.parameter) || {};
  tmpl.embedMode = param.embed === '1';
  tmpl.navTarget = param.nav || '';

  return tmpl.evaluate()
    .setTitle('★ 자산관리 대시보드 (부부합산)')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

// ──────────────────────────────────────────────
// 예산 차트용 월별 합계 (cat 기반)
// ──────────────────────────────────────────────
function buildBudgetChart(budget) {
  const chart = {
    수입:  [0,0,0,0,0,0,0,0,0,0,0,0],
    저축성: [0,0,0,0,0,0,0,0,0,0,0,0],
    지출:  [0,0,0,0,0,0,0,0,0,0,0,0]
  };
  if (!budget) return chart;

  for (const [cat, items] of Object.entries(budget)) {
    let chartKey;
    if      (cat.includes('수입'))  chartKey = '수입';
    else if (cat.includes('저축'))  chartKey = '저축성';
    else if (cat.includes('지출'))  chartKey = '지출';
    else continue;

    for (const monthArr of Object.values(items)) {
      monthArr.forEach((v, i) => { chart[chartKey][i] += (v || 0); });
    }
  }
  return chart;
}

// ──────────────────────────────────────────────
// 유틸리티
// ──────────────────────────────────────────────
function parseNum(v) {
  if (v === null || v === undefined || v === '' || v === '-') return null;
  if (typeof v === 'number') return v;
  const n = parseFloat(String(v).replace(/[₩,\s]/g, ''));
  return isNaN(n) ? null : n;
}

function formatYYYYMM(v) {
  if (v instanceof Date) {
    return v.getFullYear() + '-' + String(v.getMonth() + 1).padStart(2, '0');
  }
  return String(v).trim();
}

function todayYYYYMM() {
  const now = new Date();
  return now.getFullYear() + '-' + String(now.getMonth() + 1).padStart(2, '0');
}

// ──────────────────────────────────────────────
// 연도 헤더 셀 → "XXXX년" 문자열 추출
// (텍스트/숫자/날짜 오브젝트 모두 대응)
// ──────────────────────────────────────────────
function extractYearLabel(raw) {
  if (raw === null || raw === undefined || raw === '') return null;
  if (raw instanceof Date) {
    const y = raw.getFullYear();
    if (y >= 2000 && y <= 2099) return y + '년';
    return null;
  }
  const s = String(raw).trim();
  if (s.match(/^20\d\d년$/)) return s;
  if (s.match(/^20\d\d$/) && parseInt(s) >= 2020 && parseInt(s) <= 2099) return s + '년';
  return null;
}

// ──────────────────────────────────────────────
// 총자산(실제) — 대시보드 차트용 (미래 제외)
// ──────────────────────────────────────────────
function getMonthlyData() {
  const ss    = SpreadsheetApp.openById(SPREADSHEET_ID);
  const sheet = ss.getSheetByName('총자산(실제)');
  if (!sheet) return [];
  const rows  = sheet.getDataRange().getValues();
  const today = todayYYYYMM();
  const result = [];
  for (const r of rows) {
    const dateVal = formatYYYYMM(r[1]);
    if (!dateVal.match(/^20\d\d-\d\d?$/)) continue;
    if (dateVal > today) continue;
    const 현금성 = parseNum(r[12]);
    const 주식   = parseNum(r[11]);
    if (현금성 === null || 주식 === null) continue;
    result.push({
      date:     dateVal,
      상은계:   parseNum(r[5]),
      아영계:   parseNum(r[9]),
      합산현금: parseNum(r[10]),
      주식:     주식,
      현금성:   현금성,
      주담대:   parseNum(r[13]),
      총계:     parseNum(r[14]),
      MoM합계:  parseNum(r[18]),
    });
  }
  return result;
}

// ──────────────────────────────────────────────
// 총자산SIM — 계획/실제 (미래 계획 포함)
// ──────────────────────────────────────────────
function getPlanActualData() {
  const ss    = SpreadsheetApp.openById(SPREADSHEET_ID);
  const sheet = ss.getSheetByName('총자산SIM');
  if (!sheet) return [];
  const rows     = sheet.getDataRange().getValues();
  const result   = [];
  const todayStr = todayYYYYMM();

  for (const r of rows) {
    const dateVal = formatYYYYMM(r[1]);
    if (!dateVal.match(/^20\d\d-\d\d$/)) continue;
    const plan     = parseNum(r[2]);
    const actual   = parseNum(r[3]);
    const isFuture = dateVal > todayStr;
    if (!isFuture && (actual === null || actual === 0)) continue;
    if (isFuture  && (plan   === null || plan   === 0)) continue;
    const achRaw = r[5];
    const achievement = (!isFuture && achRaw !== null && achRaw !== '' && !isNaN(parseFloat(achRaw)))
      ? parseFloat(achRaw) * 100 : null;
    result.push({
      date:        dateVal,
      plan:        plan,
      actual:      !isFuture ? actual : null,
      achievement: achievement,
      momWon:      !isFuture ? parseNum(r[6]) : null,
    });
  }
  return result;
}

// ──────────────────────────────────────────────
// 예산 — 대시보드 차트용 (상은+아영 현재연도 합산)
// ──────────────────────────────────────────────
function getBudgetData() {
  const seResult = getBudgetPersonData('상은', null);
  const ayResult = getBudgetPersonData('아영', null);
  const budget   = {};

  function mergeItems(data) {
    if (!data || !data.items) return;
    for (const [item, d] of Object.entries(data.items)) {
      const cat = d.cat;
      if (!cat) continue;
      if (!budget[cat]) budget[cat] = {};
      if (!budget[cat][item]) budget[cat][item] = Array(12).fill(0);
      d.months.forEach((v, i) => { budget[cat][item][i] += (v || 0); });
    }
  }

  if (seResult.success) mergeItems(seResult.data);
  if (ayResult.success) mergeItems(ayResult.data);
  return budget;
}

// ──────────────────────────────────────────────
// 예산 다년도 시계열 — 대시보드 기간선택용
// ──────────────────────────────────────────────
function getBudgetTimeSeries() {
  try {
    const seSample = getBudgetPersonData('상은', null);
    const years    = seSample.success ? seSample.data.years : [];
    const sorted   = years.slice().sort();
    const series   = { labels:[], 수입:[], 저축성:[], 지출:[] };

    for (const year of sorted) {
      const se      = getBudgetPersonData('상은', year);
      const ay      = getBudgetPersonData('아영', year);
      const seItems = se.success ? se.data.items : {};
      const ayItems = ay.success ? ay.data.items : {};
      const yNum    = String(year).replace('년','');

      for (let m = 0; m < 12; m++) {
        series.labels.push(yNum + '-' + String(m+1).padStart(2,'0'));
        let income=0, save=0, expense=0;

        function agg(items) {
          for (const d of Object.values(items)) {
            const v   = d.months[m] || 0;
            const cat = d.cat || '';
            if      (cat.includes('수입'))  income  += v;
            else if (cat.includes('저축'))  save    += v;
            else                            expense += v;
          }
        }
        agg(seItems); agg(ayItems);
        series.수입.push(income);
        series.저축성.push(save);
        series.지출.push(expense);
      }
    }
    return { success:true, data:series };
  } catch(e) { return { error:e.toString() }; }
}

// ══════════════════════════════════════════════
// 총자산(실제) CRUD
// 컬럼 (Sheets 1-based):
//  A=1(비어있음), B=2(날짜), C=3(상은입출금), D=4(상은예적금), E=5(상은마통)
//  F=6(상은계,수식), G=7(아영입출금), H=8(아영예적금), I=9(아영벤츠)
//  J=10(아영계,수식), K=11(합산현금,수식), L=12(주식), M=13(현금성자산계,수식)
//  N=14(주담대), O=15(총자산계,수식), P=16~, Q=17~, ..., AE=31
// ══════════════════════════════════════════════
function getAssetFullData() {
  try {
    const ss    = SpreadsheetApp.openById(SPREADSHEET_ID);
    const sheet = ss.getSheetByName('총자산(실제)');
    if (!sheet) return { error:'시트를 찾을 수 없습니다' };
    const rows  = sheet.getDataRange().getValues();
    const today = todayYYYYMM();
    const result = [];
    for (let i = 0; i < rows.length; i++) {
      const r       = rows[i];
      const dateVal = formatYYYYMM(r[1]);
      if (!dateVal.match(/^20\d\d-\d\d?$/)) continue;
      if (dateVal > today) continue;
      result.push({
        rowIndex:    i + 1,
        date:        dateVal,
        상은_입출금: parseNum(r[2]) || 0,
        상은_예적금: parseNum(r[3]) || 0,
        상은_마통:   parseNum(r[4]) || 0,
        상은_계:     parseNum(r[5]) || 0,
        아영_입출금: parseNum(r[6]) || 0,
        아영_예적금: parseNum(r[7]) || 0,
        아영_벤츠:   parseNum(r[8]) || 0,
        아영_계:     parseNum(r[9]) || 0,
        합산:        parseNum(r[10]) || 0,
        주식:        parseNum(r[11]) || 0,
        현금성:      parseNum(r[12]) || 0,
        주담대:      parseNum(r[13]) || 0,
        총계:        parseNum(r[14]) || 0,
      });
    }
    return { success:true, data:result };
  } catch(e) { return { error:e.toString() }; }
}

function addAssetRow(data) {
  try {
    const ss    = SpreadsheetApp.openById(SPREADSHEET_ID);
    const sheet = ss.getSheetByName('총자산(실제)');
    const rows  = sheet.getDataRange().getValues();
    let lastDataRow = 1;
    for (let i = 0; i < rows.length; i++) {
      if (formatYYYYMM(rows[i][1]).match(/^20\d\d-\d\d?$/)) lastDataRow = i + 1;
    }
    sheet.insertRowAfter(lastDataRow);
    const nr = lastDataRow + 1;

    // 입력값 (마통/주담대는 양수로 받아 음수 저장)
    sheet.getRange(nr,  2).setValue(data.date);
    sheet.getRange(nr,  3).setValue( Number(data.상은_입출금) || 0);
    sheet.getRange(nr,  4).setValue( Number(data.상은_예적금) || 0);
    sheet.getRange(nr,  5).setValue(-Math.abs(Number(data.상은_마통) || 0));
    sheet.getRange(nr,  7).setValue( Number(data.아영_입출금) || 0);
    sheet.getRange(nr,  8).setValue( Number(data.아영_예적금) || 0);
    sheet.getRange(nr,  9).setValue( Number(data.아영_벤츠)   || 0);
    sheet.getRange(nr, 12).setValue( Number(data.주식)        || 0);
    sheet.getRange(nr, 14).setValue(-Math.abs(Number(data.주담대) || 0));

    // 수식 직접 설정
    sheet.getRange(nr,  6).setFormula('=SUM(C' + nr + ':E' + nr + ')');  // F: 상은계
    sheet.getRange(nr, 10).setFormula('=SUM(G' + nr + ':I' + nr + ')');  // J: 아영계
    sheet.getRange(nr, 11).setFormula('=SUM(F' + nr + ':J' + nr + ')');  // K: 합산현금
    sheet.getRange(nr, 13).setFormula('=SUM(K' + nr + ':L' + nr + ')');  // M: 현금성자산계
    sheet.getRange(nr, 15).setFormula('=SUM(M' + nr + ':N' + nr + ')');  // O: 총자산계

    // P(16)~AE(31): 이전 행 수식 복사
    for (var col = 16; col <= 31; col++) {
      var src = sheet.getRange(lastDataRow, col);
      if (src.getFormula()) src.copyTo(sheet.getRange(nr, col));
    }

    return { success:true, rowIndex:nr };
  } catch(e) { return { error:e.toString() }; }
}

function updateAssetRow(rowIndex, data) {
  try {
    const ss    = SpreadsheetApp.openById(SPREADSHEET_ID);
    const sheet = ss.getSheetByName('총자산(실제)');
    sheet.getRange(rowIndex,  2).setValue(data.date);
    sheet.getRange(rowIndex,  3).setValue( Number(data.상은_입출금) || 0);
    sheet.getRange(rowIndex,  4).setValue( Number(data.상은_예적금) || 0);
    sheet.getRange(rowIndex,  5).setValue(-Math.abs(Number(data.상은_마통) || 0));
    sheet.getRange(rowIndex,  7).setValue( Number(data.아영_입출금) || 0);
    sheet.getRange(rowIndex,  8).setValue( Number(data.아영_예적금) || 0);
    sheet.getRange(rowIndex,  9).setValue( Number(data.아영_벤츠)   || 0);
    sheet.getRange(rowIndex, 12).setValue( Number(data.주식)        || 0);
    sheet.getRange(rowIndex, 14).setValue(-Math.abs(Number(data.주담대) || 0));
    return { success:true };
  } catch(e) { return { error:e.toString() }; }
}

// 삭제 대신 입력값 전체 0으로 초기화
function deleteAssetRow(rowIndex) {
  try {
    const sheet = SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName('총자산(실제)');
    sheet.getRange(rowIndex, 2).setValue('');
    [3,4,5,7,8,9,12,14].forEach(function(col) {
      sheet.getRange(rowIndex, col).setValue(0);
    });
    return { success:true };
  } catch(e) { return { error:e.toString() }; }
}

// ══════════════════════════════════════════════
// 가계부 — 읽기
// 시트 구조 (0-based index):
//  r[0]=연도헤더(A열), r[1]=구분(B열), r[2]=세부항목(C열)
//  r[3]=계획금액(D열), r[4]=실제평균(E열), r[5]=1월, ..., r[16]=12월, r[17]=계
// ══════════════════════════════════════════════
function getBudgetPersonData(person, yearParam) {
  try {
    const ss        = SpreadsheetApp.openById(SPREADSHEET_ID);
    const sheetName = '예산(' + person + ')';
    const sheet     = ss.getSheetByName(sheetName);
    if (!sheet) return { error:'시트 없음: ' + sheetName };
    const rows = sheet.getDataRange().getValues();

    // ── 연도 섹션 파악 (넓은 범위 탐색, Date 오브젝트 포함)
    const yearSections = [];
    for (let i = 0; i < rows.length; i++) {
      const row = rows[i];
      let foundYear = null;
      for (let j = 0; j < Math.min(row.length, 6); j++) {
        const yl = extractYearLabel(row[j]);
        if (yl) { foundYear = yl; break; }
      }
      if (foundYear) {
        if (yearSections.length > 0) yearSections[yearSections.length-1].endRow = i;
        yearSections.push({ year: foundYear, startRow: i, endRow: rows.length });
      }
    }

    if (yearSections.length === 0) {
      return { error:'연도 데이터 없음 (' + sheetName + ') — 시트에 "XXXX년" 형식의 연도 헤더가 있어야 합니다.' };
    }

    // years를 숫자 배열로 통일
    const allYears = yearSections.map(s => parseInt(s.year));
    const sortedSections = yearSections.slice().sort((a,b) => parseInt(b.year) - parseInt(a.year));
    let targetSection = sortedSections[0]; // 기본: 최신 연도
    if (yearParam !== null && yearParam !== undefined) {
      // 숫자(2021)든 문자열("2021", "2021년")이든 모두 매칭
      const yp = parseInt(String(yearParam).replace(/[^0-9]/g, ''));
      const found = yearSections.find(s => parseInt(s.year) === yp);
      if (found) targetSection = found;
    }

    const result = {
      year:  parseInt(targetSection.year),  // 숫자로 반환
      years: allYears.slice().sort((a,b) => a - b),  // 오름차순 숫자 배열
      items: {}
    };

    let currentCat = '';
    for (let i = targetSection.startRow + 1; i < targetSection.endRow; i++) {
      const r      = rows[i];
      const catRaw = String(r[1]).trim();   // B열: 구분
      const item   = String(r[2]).trim();   // C열: 세부항목

      // 카테고리 갱신 (연도 헤더·'구분' 제외, 비어있지 않은 경우)
      if (catRaw && catRaw !== '구분' && !extractYearLabel(r[1])) {
        currentCat = catRaw;
      }

      // 헤더 행 / 합계 행 스킵
      if (!item || item === '세부항목' || item === '구분') continue;
      if (item.includes('합계') || item.includes(' 계') || item.includes('여유자금')) continue;

      result.items[item] = {
        rowIndex:  i + 1,
        plan:      parseNum(r[3]) || 0,      // D열: 계획금액
        actualAvg: parseNum(r[4]) || 0,      // E열: 실제금액(평균)
        months:    Array.from({length:12}, (_,m) => parseNum(r[5+m]) || 0),  // F~Q열: 1~12월
        cat:       currentCat,
      };
    }
    return { success:true, data:result };
  } catch(e) { return { error:e.toString() }; }
}

// ──────────────────────────────────────────────
// 가계부 — 단건 저장 (계획금액 + 월별 금액 일괄)
// ──────────────────────────────────────────────
function saveBudgetRow(person, rowIndex, planValue, monthValues) {
  try {
    const sheet = SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName('예산(' + person + ')');
    if (!sheet) return { error:'시트 없음: 예산(' + person + ')' };
    if (planValue !== null && planValue !== undefined) {
      // D열(4번째)=계획금액, F열(6번째)=1월부터
      sheet.getRange(rowIndex, 4).setValue(Number(planValue) || 0);
    }
    if (monthValues && Array.isArray(monthValues)) {
      monthValues.forEach((v, m) => {
        sheet.getRange(rowIndex, 6 + m).setValue(Number(v) || 0);
      });
    }
    return { success:true };
  } catch(e) { return { error:e.toString() }; }
}

// (하위호환) 단일 컬럼 업데이트
function updateBudgetPlan(person, rowIndex, value) {
  return saveBudgetRow(person, rowIndex, value, null);
}
function updateBudgetMonth(person, rowIndex, month, value) {
  try {
    SpreadsheetApp.openById(SPREADSHEET_ID)
      .getSheetByName('예산(' + person + ')').getRange(rowIndex, 6 + month).setValue(Number(value) || 0);
    return { success:true };
  } catch(e) { return { error:e.toString() }; }
}

// ──────────────────────────────────────────────
// 진단용 (Apps Script 에디터에서 직접 실행)
// ──────────────────────────────────────────────
function testData() {
  Logger.log('=== testData ===');
  const monthly = getMonthlyData();
  Logger.log('monthly: ' + monthly.length + '건 / 최신: ' + JSON.stringify(monthly.slice(-1)));

  const pa = getPlanActualData();
  Logger.log('planActual: ' + pa.length + '건');

  const se = getBudgetPersonData('상은', null);
  Logger.log('budget 상은 성공: ' + se.success + ' / 오류: ' + se.error);
  if (se.success) {
    Logger.log('  연도: ' + se.data.year + ' / 항목수: ' + Object.keys(se.data.items).length);
    Logger.log('  첫 항목: ' + JSON.stringify(Object.entries(se.data.items).slice(0,2)));
  }

  const ay = getBudgetPersonData('아영', null);
  Logger.log('budget 아영 성공: ' + ay.success + ' / 오류: ' + ay.error);

  const bd = getBudgetData();
  Logger.log('budget 합산 카테고리: ' + Object.keys(bd).join(', '));

  const chart = buildBudgetChart(bd);
  Logger.log('chart 수입: ' + JSON.stringify(chart.수입));
  Logger.log('chart 저축성: ' + JSON.stringify(chart.저축성));
  Logger.log('chart 지출: ' + JSON.stringify(chart.지출));
}
