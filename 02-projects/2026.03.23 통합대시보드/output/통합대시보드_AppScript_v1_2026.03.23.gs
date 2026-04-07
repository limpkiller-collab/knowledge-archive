/**
 * ★ 통합 자산관리 대시보드 - Apps Script (서버)
 *
 * ▶ 적용 방법:
 *   1. 새 Google Apps Script 프로젝트 생성 (script.google.com)
 *   2. 이 파일 내용을 Code.gs에 붙여넣기
 *   3. Apps Script 편집기 좌측 "+" → HTML → 파일명 "dashboard" 입력
 *      → 통합대시보드_대시보드_v1 HTML 파일 내용 전체를 붙여넣기
 *   4. 아래 ASSET_DASHBOARD_URL, PORTFOLIO_DASHBOARD_URL을
 *      각각 기존 대시보드의 배포 URL로 변경
 *   5. 배포 → 웹 앱 → "나를 액세스하는 모든 사용자" → 새 배포
 *   6. 발급된 URL을 아이폰 Safari에서 열면 통합 대시보드가 표시됩니다.
 *
 * ▶ 주의사항:
 *   - 기존 두 대시보드의 AppScript도 embed 모드가 추가된 버전으로 업데이트 필요
 *     (자산관리 AppScript v4, 포트폴리오 AppScript v15)
 *   - 기존 두 대시보드의 HTML도 embed 모드가 추가된 버전으로 업데이트 필요
 *     (자산관리 HTML v22, 포트폴리오 HTML v35)
 */

// ── 기존 대시보드 배포 URL 설정 ──────────────────────────────────
// ※ 아래 URL을 각 대시보드의 실제 웹앱 배포 URL로 변경해주세요.
const ASSET_DASHBOARD_URL     = 'YOUR_ASSET_DASHBOARD_URL_HERE';
const PORTFOLIO_DASHBOARD_URL = 'YOUR_PORTFOLIO_DASHBOARD_URL_HERE';

// ── 웹앱 진입점 ──────────────────────────────────────────────────
function doGet() {
  const tmpl = HtmlService.createTemplateFromFile('dashboard');
  tmpl.assetUrl     = ASSET_DASHBOARD_URL;
  tmpl.portfolioUrl = PORTFOLIO_DASHBOARD_URL;

  return tmpl.evaluate()
    .setTitle('★ 통합 자산관리 대시보드')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}
