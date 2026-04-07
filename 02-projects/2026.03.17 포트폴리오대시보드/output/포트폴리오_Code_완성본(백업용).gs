/**
 * ★ 주식 포트폴리오 대시보드 - Apps Script 웹앱
 *
 * ▶ 적용 방법:
 *   1. 스프레드시트 → 확장 프로그램 → Apps Script
 *   2. 이 파일 전체를 Code.gs에 붙여넣기
 *   3. Apps Script 편집기 좌측 "+" 클릭 → HTML → 파일명 "dashboard" 입력
 *      → 포트폴리오_자동대시보드.html 내용 전체를 붙여넣기
 *   4. 배포 → 웹 앱 → "나를 액세스하는 모든 사용자" → 새 배포 (또는 버전 업데이트)
 *   5. 발급된 웹앱 URL을 아이폰 Safari에서 열면 대시보드가 바로 표시됩니다.
 *      홈 화면에 추가(PWA)하면 앱처럼 사용 가능합니다.
 *   ※ getActiveSpreadsheet() 사용 — 스프레드시트에 연결된 스크립트이므로 ID 설정 불필요
 */

// ── 시트 이름 설정 ──────────────────────────────────────────────────────────
const SHEET_PORTFOLIO      = 'Portfolio';
const SHEET_DAILY_RETURN   = 'Daily Return';
const SHEET_MONTHLY_REVIEW = 'Monthly review';
const SHEET_WATCHLIST      = 'Watchlist';
const SHEET_TRANSACTIONS   = 'Transactions';
const SHEET_CASHFLOW       = 'Cashflow';
const SHEET_NEWS           = 'News';

// ── 티커 → 한글 검색어 딕셔너리 (뉴스 수집 대상 11개) ──────────────────────
// ※ 이 딕셔너리에 없는 티커는 뉴스 수집 대상에서 자동 제외됩니다.
// ※ OR 로 복수 검색어 지정 가능
const TICKER_KR_QUERY = {
  'NVDA' : '엔비디아',
  'AAPL' : '애플',
  'MSFT' : '마이크로소프트',
  'GOOGL': '알파벳 OR 구글',
  'O'    : '리얼티 인컴',
  'NVO'  : '노보 노디스크 OR 노보노디스크',
  'TSLA' : '테슬라',
  'PLTR' : '팔란티어',
  'CRWV' : '코어위브',
  'IONQ' : '아이온큐',
  'SMR'  : '뉴스케일파워 OR "뉴스케일 파워" OR 누스케일파워 OR "누스케일 파워" OR SMR',
  // ABBV·KO·ETSY·OKLO·URA : 제외
};

// ── 라우터 ──────────────────────────────────────────────────────────────────
function doGet(e) {
  try {
    const action = (e.parameter && e.parameter.action) || 'page';
    const ss = SpreadsheetApp.getActiveSpreadsheet();

    // ── HTML 페이지 서빙 (action 없이 URL만 열었을 때) ───────────────────────
    // Apps Script 프로젝트에 dashboard.html 파일이 있어야 합니다.
    if (action === 'page') {
      return HtmlService.createHtmlOutputFromFile('dashboard')
        .setTitle('📈 내 포트폴리오')
        .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
    }

    // ── 데이터 쓰기 ─────────────────────────────────────────────
    // ※ HTML에서 URLSearchParams로 개별 파라미터를 전송하므로 각각 파싱
    if (action === 'addTransaction') {
      addTransactionRow(ss, {
        date   : e.parameter.date,
        ticker : e.parameter.ticker,
        sector : e.parameter.sector || '',
        type   : e.parameter.type,
        qty    : Number(e.parameter.qty),
        price  : Number(e.parameter.price),
        fee    : Number(e.parameter.fee)  || 0,
        fx     : Number(e.parameter.fx),
        memo   : e.parameter.memo || '',
      });
      return ok({ success: true });
    }
    if (action === 'addCashflow') {
      const cfType = e.parameter.cfType;
      const payload = { cfType, date: e.parameter.date };
      if (cfType === '배당금') {
        payload.ticker       = e.parameter.ticker || '';
        payload.divAmount    = Number(e.parameter.divAmount)   || 0;
        payload.divPerShare  = Number(e.parameter.divPerShare) || 0;
      } else if (cfType === '환전') {
        payload.exchangeAmount = Number(e.parameter.exchangeAmount) || 0;
        payload.exchangeRate   = Number(e.parameter.exchangeRate)   || 0;
      } else if (cfType === '투자금') {
        payload.person        = e.parameter.person || '';
        payload.investAmount  = Number(e.parameter.investAmount) || 0;
      }
      addCashflowRow(ss, payload);
      return ok({ success: true });
    }

    // ── 삭제 ─────────────────────────────────────────────────────
    if (action === 'deleteTransaction') {
      const rowNum = parseInt(e.parameter.rowNum);
      if (!rowNum || rowNum < 2) throw new Error('유효하지 않은 행 번호입니다.');
      ss.getSheetByName(SHEET_TRANSACTIONS).deleteRow(rowNum);
      return ok({ success: true });
    }
    if (action === 'deleteCashflow') {
      const rowNum = parseInt(e.parameter.rowNum);
      if (!rowNum || rowNum < 2) throw new Error('유효하지 않은 행 번호입니다.');
      ss.getSheetByName(SHEET_CASHFLOW).deleteRow(rowNum);
      return ok({ success: true });
    }

    // ── 탭 데이터 조회 ───────────────────────────────────────────
    if (action === 'getTransactions') {
      return ok({ transactions: getTransactions(ss) });
    }
    if (action === 'getCashflow') {
      const cf = getCashflow(ss);
      return ok({ cashflow: cf.rows, cfSummary: cf.summary });
    }

    // ── 뉴스 수집 (수동 트리거) ──────────────────────────────────
    if (action === 'fetchNews') {
      fetchAndStoreNews();
      return ok({ success: true, news: getNews(ss) });
    }

    // ── 포트폴리오 전체 데이터 (action=data) ─────────────────────
    if (action === 'data') return ok(getPortfolioData());

    // 알 수 없는 action → 에러
    return ok({ error: `알 수 없는 action: ${action}` });

  } catch (err) {
    Logger.log('doGet error: ' + err.message + '\n' + err.stack);
    return ok({ error: err.message });
  }
}

function ok(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

// ── 포트폴리오 전체 데이터 ──────────────────────────────────────────────────
function getPortfolioData() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  return {
    lastUpdated          : new Date().toISOString(),
    summary              : getSummary(ss),
    holdings             : getHoldings(ss),
    strategy             : getStrategy(ss),      // SECTOR1 산업별 (U35:Y48)
    sectorTheme          : getSectorTheme(ss),   // SECTOR2 테마별 (U52:Y59)
    monthlyHistory       : getMonthlyHistory(ss),
    monthlyReview        : getMonthlyReviewSummary(ss),
    monthlyReviewHistory : getMonthlyReviewHistory(ss),
    watchlist            : getWatchlist(ss),
    sectors              : getSectors(ss),
    news                 : getNews(ss),
  };
}

// ── 요약 KPI (Portfolio 시트 고정 셀) ────────────────────────────────────────
function getSummary(ss) {
  const ws = ss.getSheetByName(SHEET_PORTFOLIO);
  return {
    totalKrw     : ws.getRange('B6').getValue(),
    dailyPnlKrw  : ws.getRange('D6').getValue(),
    dailyReturn  : ws.getRange('E6').getValue(),
    dow          : ws.getRange('P6').getValue(),
    nasdaq       : ws.getRange('Q6').getValue(),
    sp500        : ws.getRange('R6').getValue(),
    exchangeRate : ws.getRange('S6').getValue(),
    investedUsd  : ws.getRange('C9').getValue(),
    investedKrw  : ws.getRange('E9').getValue(),
    totalUsd     : ws.getRange('C10').getValue(),
    pnlUsd       : ws.getRange('D12').getValue(),
    pnlKrw       : ws.getRange('E12').getValue(),
    returnRate   : ws.getRange('C12').getValue(),
    returnRateKrw: ws.getRange('E13').getValue(),
  };
}

// ── 섹터 목록 (Portfolio F17:F41, 중복 제거) ─────────────────────────────
function getSectors(ss) {
  const ws   = ss.getSheetByName(SHEET_PORTFOLIO);
  const data = ws.getRange('F17:F41').getValues();
  const set  = new Set();
  data.forEach(row => { if (row[0]) set.add(row[0]); });
  return [...set];
}

// ── 보유 종목 (Portfolio B15:S41) ────────────────────────────────────────────
// 범위 내 0-based 인덱스:
//   [0]=순번  [1]=TICKER  [2]=COMPANY  [3]=SECTOR1  [4]=SECTOR2  [5]=수량
//   [6]=보유기간  [7]=스킵  [8]=PRICE(USD)  [9]=평단가(USD)
//   [10]=현재가(KRW)  [11]=평단가(KRW)  [12]=CHANGE  [13]=일수익(USD)
//   [14]=평가금액(USD)  [15]=매수금액(USD)  [16]=수익(USD)  [17]=수익률
function getHoldings(ss) {
  const ws   = ss.getSheetByName(SHEET_PORTFOLIO);
  const data = ws.getRange('B15:S41').getValues();
  const holdings = [];
  for (const row of data) {
    const num = row[0];
    if (!num || typeof num !== 'number') continue;
    holdings.push({
      num        : num,
      ticker     : row[1]  || '',
      company    : row[2]  || '',
      sector1    : row[3]  || '',
      sector2    : row[4]  || '',
      qty        : row[5]  || 0,
      holdDays   : row[6]  || 0,
      price      : row[8]  || 0,
      avgPrice   : row[9]  || 0,
      currentKrw : row[10] || 0,
      avgKrw     : row[11] || 0,
      change     : row[12] || 0,
      dailyPnlUsd: row[13] || 0,
      valueUsd   : row[14] || 0,
      costUsd    : row[15] || 0,
      pnlUsd     : row[16] || 0,
      returnRate : row[17] || 0,
    });
  }
  return holdings;
}

// ── 산업별 비중 SECTOR1 (Portfolio U35:Y48) ───────────────────────────────────
// [0]=산업명  [1]=매수금액($)  [2]=평가금액($)  [3]=비율(%)  [4]=수익률
function getStrategy(ss) {
  const ws   = ss.getSheetByName(SHEET_PORTFOLIO);
  const data = ws.getRange('U35:Y48').getValues();
  const strategy = [];
  for (const row of data) {
    if (!row[0] || row[0] === 'SECTOR' || row[0] === '계') continue;
    strategy.push({ name: row[0], cost: row[1]||0, value: row[2]||0, ratio: row[3]||0, ret: row[4]||0 });
  }
  return strategy;
}

// ── 테마별 비중 SECTOR2 (Portfolio U52:Y59) ───────────────────────────────────
// [0]=테마명  [1]=매수금액($)  [2]=평가금액($)  [3]=비율(%)  [4]=수익률
function getSectorTheme(ss) {
  const ws   = ss.getSheetByName(SHEET_PORTFOLIO);
  const data = ws.getRange('U52:Y59').getValues();
  const theme = [];
  for (const row of data) {
    if (!row[0] || row[0] === 'SECTOR' || row[0] === '계') continue;
    theme.push({ name: row[0], cost: row[1]||0, value: row[2]||0, ratio: row[3]||0, ret: row[4]||0 });
  }
  return theme;
}

// ── 월별 자산 추이 (Daily Return 시트 A4:E2000) ───────────────────────────────
// 날짜별 총자산(원)에서 월별 마지막 값 추출
function getMonthlyHistory(ss) {
  const ws   = ss.getSheetByName(SHEET_DAILY_RETURN);
  if (!ws) return [];
  const data = ws.getRange('A4:E2000').getValues();
  const monthly = {};
  for (const row of data) {
    const date = row[0];
    if (!(date instanceof Date)) continue;
    const total = row[1];
    if (!total) continue;
    const ym = Utilities.formatDate(date, 'Asia/Seoul', 'yyyy-MM');
    monthly[ym] = { month: ym, total: Math.round(total) };
  }
  return Object.values(monthly).sort((a, b) => a.month.localeCompare(b.month));
}

// ── 이번달 수익 요약 KPI (Monthly review 시트 고정 셀) ─────────────────────────
function getMonthlyReviewSummary(ss) {
  const ws = ss.getSheetByName(SHEET_MONTHLY_REVIEW);
  return {
    monthlyInvest : ws.getRange('H4').getValue(),
    monthlyDiv    : ws.getRange('I4').getValue(),
    monthlyPnl    : ws.getRange('J4').getValue(),
    monthlyRet    : ws.getRange('K4').getValue(),
    monthlyChange : ws.getRange('G4').getValue(),
    avgMonthlyPnl : ws.getRange('J2').getValue(),
  };
}

// ── 월별 수익 전체 이력 (Monthly review A6:K100) ──────────────────────────────
// [0]=날짜  [2]=누적투자금  [3]=평가금액  [4]=누적수익금  [5]=누적수익률
// [6]=전월대비  [7]=월투자금  [8]=월배당금  [9]=순수익금  [10]=순수익률
function getMonthlyReviewHistory(ss) {
  const ws   = ss.getSheetByName(SHEET_MONTHLY_REVIEW);
  const data = ws.getRange('A6:K100').getValues();
  const history = [];
  for (const row of data) {
    if (!(row[0] instanceof Date)) continue;
    history.push({
      month         : Utilities.formatDate(row[0], 'Asia/Seoul', 'yyyy-MM'),
      invested      : row[2] || 0,
      valuation     : row[3] || 0,
      cumPnl        : row[4] || 0,
      cumRet        : row[5] || 0,
      monthlyChange : row[6] || 0,
      monthlyInvest : row[7] || 0,
      monthlyDiv    : row[8] || 0,
      monthlyPnl    : row[9] || 0,
      monthlyRet    : row[10] || 0,
    });
  }
  return history;
}

// ── 워치리스트 (Watchlist B6:O28) ───────────────────────────────────────────
// [0]=SECTOR  [1]=TICKER  [2]=전고점대비%  [3]=현재가
// [4]=-5%  [5]=-10%  [6]=-20%  [7]=-25%  [8]=-30%  [9]=-40%  [10]=-50%
// [11]=52D HIGH  [12]=52D LOW  [13]=P/E
function getWatchlist(ss) {
  const ws   = ss.getSheetByName(SHEET_WATCHLIST);
  const data = ws.getRange('B6:O28').getValues();
  const watchlist = [];
  for (const row of data) {
    if (!row[1]) continue;
    watchlist.push({
      sector    : row[0] || '',
      ticker    : row[1] || '',
      pctFrom52H: row[2] || 0,
      price     : row[3] || 0,
      t5        : row[4] || 0,
      t10       : row[5] || 0,
      t20       : row[6] || 0,
      t25       : row[7] || 0,
      t30       : row[8] || 0,
      t40       : row[9] || 0,
      t50       : row[10] || 0,
      high52    : row[11] || 0,
      low52     : row[12] || 0,
      pe        : row[13] || 0,
    });
  }
  return watchlist;
}

// ── 거래 내역 조회 (Transactions 시트, 행2~) ────────────────────────────────
function getTransactions(ss) {
  const ws      = ss.getSheetByName(SHEET_TRANSACTIONS);
  const lastRow = ws.getLastRow();
  if (lastRow < 2) return [];

  const numRows = lastRow - 1;
  const data    = ws.getRange(2, 1, numRows, 14).getValues();
  const txs     = [];

  for (let i = 0; i < data.length; i++) {
    const row    = data[i];
    const rowNum = i + 2;

    if (!row[0] && !row[1]) continue;

    let dateStr = '';
    if (row[0] instanceof Date) {
      dateStr = Utilities.formatDate(row[0], 'Asia/Seoul', 'yyyy-MM-dd');
    } else if (row[0]) {
      dateStr = String(row[0]);
    }
    if (!dateStr || !row[1]) continue;

    txs.push({
      rowNum   : rowNum,
      date     : dateStr,
      ticker   : String(row[1]  || ''),
      sector   : String(row[2]  || ''),
      company  : String(row[3]  || ''),
      type     : String(row[4]  || ''),
      qty      : Number(row[5]  || 0),
      price    : Number(row[6]  || 0),
      amount   : Number(row[7]  || 0),
      fee      : Number(row[8]  || 0),
      totalCost: Number(row[9]  || 0),
      fx       : Number(row[11] || 0),
      holdDays : Number(row[12] || 0),
    });
  }
  return txs.reverse();
}

// ── Cashflow 조회 (Cashflow 시트, 행2~) ─────────────────────────────────────
function getCashflow(ss) {
  const ws      = ss.getSheetByName(SHEET_CASHFLOW);
  const lastRow = ws.getLastRow();

  // ★ 배치 읽기: 2개 셀을 1회 호출로 통합
  const summaryVals = ws.getRange('L10:M11').getValues();
  const avgFxRate   = Number(summaryVals[0][0] || 0);
  const fxGainLoss  = Number(summaryVals[1][1] || 0);

  if (lastRow < 2) {
    return { rows: [], summary: { exTotalUsd: 0, avgFxRate, fxGainLoss } };
  }

  const numRows = lastRow - 1;
  const data    = ws.getRange(2, 1, numRows, 9).getValues();
  const flows   = [];
  let   exTotalUsd = 0;

  for (let i = 0; i < data.length; i++) {
    const row    = data[i];
    const rowNum = i + 2;

    if (!row[0]) continue;

    let dateStr = '';
    if (row[0] instanceof Date) {
      dateStr = Utilities.formatDate(row[0], 'Asia/Seoul', 'yyyy-MM-dd');
    } else if (row[0]) {
      dateStr = String(row[0]);
    }
    if (!dateStr) continue;

    if (String(row[6]).trim() === '환전') {
      exTotalUsd += Number(row[3] || 0);
    }

    flows.push({
      rowNum   : rowNum,
      date     : dateStr,
      investKrw: Number(row[1] || 0),
      exKrw    : Number(row[2] || 0),
      exUsd    : Number(row[3] || 0),
      divAmt   : Number(row[5] || 0),
      memo     : String(row[6] || ''),
      fxRate   : Number(row[7] || 0),
      category : String(row[8] || ''),
    });
  }

  return {
    rows   : flows.reverse(),
    summary: { exTotalUsd, avgFxRate, fxGainLoss },
  };
}

// ── 거래 내역 추가 (Transactions 시트) ──────────────────────────────────────
function addTransactionRow(ss, d) {
  const ws      = ss.getSheetByName(SHEET_TRANSACTIONS);
  const lastRow = ws.getLastRow() + 1;

  ws.getRange(lastRow, 1).setValue(new Date(d.date));
  ws.getRange(lastRow, 2).setValue(d.ticker);
  ws.getRange(lastRow, 3).setValue(d.sector || '');
  ws.getRange(lastRow, 4).setFormula(`=GOOGLEFINANCE("${d.ticker}","name")`);
  ws.getRange(lastRow, 5).setValue(d.type);
  ws.getRange(lastRow, 6).setValue(d.qty);
  ws.getRange(lastRow, 7).setValue(d.price);

  // ① 거래금액 (H) = 수량(F) × PRICE(G) — USD
  ws.getRange(lastRow, 8).setFormula(`=F${lastRow}*G${lastRow}`);
  ws.getRange(lastRow, 8).setNumberFormat('"$"#,##0.00');

  // ② 수수료 (I) — USD 표기
  ws.getRange(lastRow, 9).setValue(d.fee || 0);
  ws.getRange(lastRow, 9).setNumberFormat('"$"#,##0.00');

  // ③ 정산금액 (J) = 거래금액 + 수수료, USD 표기
  ws.getRange(lastRow, 10).setValue(d.qty * d.price + (d.fee || 0));
  ws.getRange(lastRow, 10).setNumberFormat('"$"#,##0.00');

  // ④ 원화환산 (K) = 정산금액(J) × 환율(L)
  ws.getRange(lastRow, 11).setFormula(`=J${lastRow}*L${lastRow}`);
  ws.getRange(lastRow, 12).setValue(d.fx);
  ws.getRange(lastRow, 13).setFormula(`=DAYS(TODAY(),A${lastRow})`);

  // ⑤ 주당금액 (N) — 정수 단위
  ws.getRange(lastRow, 14).setFormula(`=ROUND($K${lastRow}/$F${lastRow},0)`);
}

// ── Cashflow 추가 (Cashflow 시트) ────────────────────────────────────────────
function addCashflowRow(ss, d) {
  const ws      = ss.getSheetByName(SHEET_CASHFLOW);
  const lastRow = ws.getLastRow() + 1;

  ws.getRange(lastRow, 1).setValue(new Date(d.date));

  if (d.cfType === '배당금') {
    ws.getRange(lastRow, 6).setValue(d.divAmount);
    ws.getRange(lastRow, 7).setValue(`배당금입금 - ${d.ticker}(주당 ${d.divPerShare || '0'})`);
    ws.getRange(lastRow, 9).setValue('배당금');

  } else if (d.cfType === '환전') {
    ws.getRange(lastRow, 3).setValue(-(d.exchangeAmount * d.exchangeRate));
    ws.getRange(lastRow, 4).setValue(d.exchangeAmount);
    ws.getRange(lastRow, 7).setValue('환전');
    ws.getRange(lastRow, 8).setValue(d.exchangeRate);

  } else if (d.cfType === '투자금') {
    ws.getRange(lastRow, 2).setValue(d.investAmount);
    ws.getRange(lastRow, 3).setValue(d.investAmount);
    ws.getRange(lastRow, 9).setValue(d.person);
  }
}

// ══════════════════════════════════════════════════════════════════════════════
// 📰 뉴스 기능
// ══════════════════════════════════════════════════════════════════════════════

// ── 뉴스 수집 소스 (한국어 3개 언론사) ────────────────────────────────────────
const NEWS_RSS_SOURCES = [
  { name: '한국경제', url: 'https://www.hankyung.com/feed/all-news' },
  { name: '매일경제', url: 'https://www.mk.co.kr/rss/30000001' },
  { name: '연합뉴스', url: 'https://www.yna.co.kr/rss/economy.xml' },
];

// ── 국내 시장 기사 제외 키워드 (제목 기준) ────────────────────────────────────
const DOMESTIC_FILTER = ['코스닥', '코스피', 'KOSPI', 'KOSDAQ', '유가증권시장', '코스피200', '종합주가지수', '국내증시'];

// ── News 시트에서 기사 읽기 (6컬럼: ticker/date/title/summary/link/source) ───
function getNews(ss) {
  try {
    const ws = ss.getSheetByName(SHEET_NEWS);
    if (!ws || ws.getLastRow() < 2) return [];
    const data = ws.getRange(2, 1, ws.getLastRow() - 1, 6).getValues();
    return data.filter(r => r[0] && r[2]).map(r => ({
      ticker  : String(r[0]),
      date    : r[1] instanceof Date ? Utilities.formatDate(r[1], 'Asia/Seoul', 'yyyy-MM-dd') : String(r[1]),
      title   : String(r[2]),
      summary : String(r[3]),
      link    : String(r[4]),
      source  : String(r[5] || ''),
    }));
  } catch(e) { return []; }
}

// ── 3개 RSS 소스에서 24시간 내 기사 수집, 종목당 최대 3건 저장 ─────────────────
function fetchAndStoreNews() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  // 보유 종목 중 딕셔너리에 등록된 티커만 대상
  const heldTickers = new Set(getHoldings(ss).map(h => h.ticker).filter(Boolean));
  const targets = Object.keys(TICKER_KR_QUERY).filter(t => heldTickers.has(t));

  const cutoff = new Date();
  cutoff.setHours(cutoff.getHours() - 24);  // 24시간 컷오프

  // 티커별 수집 버킷 초기화
  const bucket = {};
  targets.forEach(t => { bucket[t] = []; });

  // ── 소스별 RSS 피드 수집 ────────────────────────────────────────────────────
  for (const src of NEWS_RSS_SOURCES) {
    try {
      const res = UrlFetchApp.fetch(src.url, { muteHttpExceptions: true, followRedirects: true });
      if (res.getResponseCode() !== 200) {
        Logger.log(`⚠️ ${src.name} 응답 오류: ${res.getResponseCode()}`);
        continue;
      }

      const items = parseRSSItems_(res.getContentText());
      Logger.log(`${src.name}: ${items.length}건 파싱`);

      for (const item of items) {
        // 24시간 필터
        const pubDate = item.pubDate ? new Date(item.pubDate) : null;
        if (!pubDate || pubDate < cutoff) continue;

        const titleText = (item.title || '').trim();
        const summText  = (item.summary || '').trim();
        const fullText  = titleText + ' ' + summText;

        // 국내 시장 기사 제외 (제목 기준)
        if (DOMESTIC_FILTER.some(kw => titleText.includes(kw))) continue;

        const dateStr = Utilities.formatDate(pubDate, 'Asia/Seoul', 'yyyy-MM-dd');

        // 각 티커 검색어와 매칭
        for (const ticker of targets) {
          if (bucket[ticker].length >= 3) continue;
          if (matchTickerQuery_(fullText, ticker)) {
            bucket[ticker].push([ticker, dateStr, titleText, summText.slice(0, 150), item.link || '', src.name]);
          }
        }
      }
    } catch(e) {
      Logger.log(`❌ ${src.name} 수집 실패: ${e.message}`);
    }
  }

  // ── News 시트에 저장 ────────────────────────────────────────────────────────
  const rows = targets.flatMap(t => bucket[t]);
  const ws = ss.getSheetByName(SHEET_NEWS) || ss.insertSheet(SHEET_NEWS);
  ws.clearContents();
  ws.getRange(1, 1, 1, 6).setValues([['Ticker','Date','Title','Summary','Link','Source']]);
  if (rows.length > 0) ws.getRange(2, 1, rows.length, 6).setValues(rows);

  const covered = targets.filter(t => bucket[t].length > 0).length;
  Logger.log(`✅ 뉴스 업데이트 완료: 총 ${rows.length}건 / ${covered}개 종목`);
}

// ── 검색어 매칭 헬퍼 (OR 연산자 지원) ─────────────────────────────────────────
function matchTickerQuery_(text, ticker) {
  const terms = TICKER_KR_QUERY[ticker]
    .split(' OR ')
    .map(t => t.replace(/"/g, '').trim())
    .filter(Boolean);
  return terms.some(term => text.includes(term));
}

// ── RSS XML 파싱 ──────────────────────────────────────────────────────────────
function parseRSSItems_(xmlText) {
  const items  = [];
  const chunks = xmlText.match(/<item>([\s\S]*?)<\/item>/g) || [];
  for (const chunk of chunks) {
    const get = tag => {
      const cd = chunk.match(new RegExp(`<${tag}[^>]*><!\\[CDATA\\[([\\s\\S]*?)\\]\\]><\\/${tag}>`));
      if (cd) return cd[1];
      const pl = chunk.match(new RegExp(`<${tag}[^>]*>([\\s\\S]*?)<\\/${tag}>`));
      return pl ? pl[1] : '';
    };
    const rawTitle   = get('title').replace(/\s*-\s*[^-\n]+$/, '').trim();
    const rawSummary = get('description')
      .replace(/<[^>]+>/g, ' ').replace(/&[a-z]+;/gi, ' ').replace(/\s+/g, ' ').trim();
    items.push({
      title   : rawTitle,
      link    : get('link').trim(),
      pubDate : get('pubDate').trim(),
      summary : rawSummary.slice(0, 300),
    });
  }
  return items;
}

function setNewsTrigger() {
  ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === 'fetchAndStoreNews')
    .forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('fetchAndStoreNews').timeBased().everyDays(1).atHour(9).inTimezone('Asia/Seoul').create();
  Logger.log('✅ 뉴스 자동 업데이트 트리거 설정 완료 (매일 오전 9시)');
}

// ── 테스트 함수 ──────────────────────────────────────────────────────────────
function testGetData() {
  Logger.log(JSON.stringify(getPortfolioData(), null, 2));
}
function testGetTransactions() {
  Logger.log(JSON.stringify(getTransactions(SpreadsheetApp.getActiveSpreadsheet()), null, 2));
}
function testGetCashflow() {
  Logger.log(JSON.stringify(getCashflow(SpreadsheetApp.getActiveSpreadsheet()), null, 2));
}
function testAddTransaction() {
  addTransactionRow(SpreadsheetApp.getActiveSpreadsheet(), { date:'2026-03-14', ticker:'NVDA', sector:'Technology', type:'매수', qty:1, price:115.50, fee:0.01, fx:1450 });
  Logger.log('testAddTransaction 완료');
}
function testFetchNews() {
  fetchAndStoreNews();
  Logger.log(JSON.stringify(getNews(SpreadsheetApp.getActiveSpreadsheet()).slice(0,3), null, 2));
}