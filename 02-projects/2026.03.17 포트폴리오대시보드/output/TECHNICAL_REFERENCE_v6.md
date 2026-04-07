# Technical Reference - Portfolio Dashboard v6

## File Structure

**Location**: `/sessions/nice-youthful-babbage/mnt/Claude/02-projects/2026.03.17 포트폴리오대시보드/output/`

**Files**:
- `포트폴리오대시보드_HTML_v5_2026.03.19.html` - Main dashboard file (130 KB, ~1,760 lines)
- `CHANGES_SUMMARY_v6_2026.03.19.md` - Feature implementation details
- `TECHNICAL_REFERENCE_v6.md` - This file

---

## Global Variables

```javascript
const CHARTS = {};                    // Chart.js instances
let CURRENT_FX = 1200;               // Current exchange rate ₩/$
let ALL_HOLDINGS = [];               // Array of holding objects
let ALL_WATCHLIST = [];              // Array of watchlist items
let ALL_SECTORS = [];                // Array of sector data
let ALL_MONTHLY_HISTORY = [];        // Monthly review history
let benchmarkVisible = false;        // Benchmark chart toggle state
let ptrStartY = 0;                   // Pull-to-refresh start Y position
let ptrActive = false;               // Pull-to-refresh active flag
```

---

## New Functions

### Theme Management

#### `initTheme()`
- Loads saved theme preference from localStorage
- Called on page load via DOMContentLoaded
- Sets theme to 'dark' by default if not saved

#### `setTheme(theme)`
- Parameters: `theme` ('dark' or 'light')
- Sets data-theme attribute on document root
- Updates button icons (🌙 / ☀️)
- Saves preference to localStorage

#### `toggleTheme()`
- Toggles between current theme and opposite
- Reads from localStorage to determine current state
- Calls `setTheme()` with new value

---

### Skeleton Loading

#### `showSkeletons()`
- Replaces all content with skeleton placeholders
- Called from `loadData()` before fetch
- Affected elements:
  - All KPI value displays
  - Chart canvases
  - Strategy/Sector detail sections
- Skeletons animate with shimmer effect (1.5s loop)

---

### Goal Asset Tracker

#### `renderGoalTracker(totalKrw, monthlyHistory)`
- Parameters:
  - `totalKrw` (number) - Current total asset in KRW
  - `monthlyHistory` (array) - Monthly review history for growth calculation
- Renders:
  - Progress bar with percentage
  - Three stat cards (current, target, remaining)
  - ETA text based on monthly growth
- Calculations:
  - Monthly growth = current month valuation - previous month valuation
  - Months needed = remaining / monthly growth
  - Achievement date = today + months needed

#### `editGoal()`
- Shows prompt dialog for new goal amount
- Stores in localStorage: key='portfolio_goal_krw'
- Validates positive number
- Re-renders goal tracker on save
- Shows success toast message

---

### Break-Even Analysis

#### `renderBreakevenChart(holdings)`
- Parameters: `holdings` (array) - All holding objects
- Filters: Only includes holdings where `returnRate < 0`
- Sorting: By return rate (worst first)
- Chart type: Horizontal bar chart (indexAxis: 'y')
- Data: `-returnRate * 100` = percentage to break-even
- Empty state: Shows message if no losers exist

---

### Benchmark Comparison

#### `toggleBenchmark()`
- Toggles `benchmarkVisible` flag
- Calls `renderCumRetChart()` to update chart
- When visible: Shows legend and benchmark datasets
- When hidden: Shows only portfolio line

#### Modified `renderCumRetChart(mrh)`
- Parameters: `mrh` (array) - Monthly review history
- Base dataset: Portfolio cumulative returns (always shown)
- Additional datasets (if `benchmarkVisible`):
  - S&P 500: 10% annual = 0.797% monthly compounding
  - NASDAQ: 12% annual = 0.949% monthly compounding
- Formula: `(1 + annual/12)^month - 1`
- Colors: Portfolio (purple), S&P (cyan), NASDAQ (blue)

---

## Pull-to-Refresh Implementation

### Touch Event Handlers

**touchstart**:
- Records initial Y position if scrollY === 0
- Sets ptrActive flag to true

**touchmove**:
- Calculates delta from start position
- Updates PTR div height to show pull distance
- Changes text feedback based on threshold (60px)
- Only active if ptrActive && scrollY === 0

**touchend**:
- Checks if delta > 60px
- If yes: Calls `loadData()` and shows "새로고침 중…" text
- If no: Resets PTR container to height 0
- Sets ptrActive to false

### PTR HTML Element

```html
<div id="ptr" style="...">
  <span id="ptr-text">↓ 당겨서 새로고침</span>
</div>
```

---

## localStorage Keys

| Key | Default | Purpose |
|-----|---------|---------|
| `webapp_url` | none | Google Apps Script deployment URL |
| `portfolio_layout` | {} | Section visibility state |
| `portfolio_news_tickers` | null | Watchlist for news filtering |
| `portfolio_goal_krw` | 500000000 | User's goal asset amount |
| `portfolio_theme` | 'dark' | User's theme preference |

---

## CSS Variables (Theme System)

### Dark Mode (Default)
```css
:root {
  --bg: #0f1117;
  --surface: #1a1d27;
  --surface2: #222636;
  --border: #2e3250;
  --text: #e8ecf0;
  --muted: #8b92a9;
  --accent: #5b8dee;
  --green: #22c55e;
  --red: #ef4444;
  --yellow: #f59e0b;
  --purple: #a855f7;
  --cyan: #06b6d4;
  --orange: #f97316;
}
```

### Light Mode
```css
[data-theme="light"] {
  --bg: #f5f5f7;
  --surface: #ffffff;
  --surface2: #f0f0f5;
  --border: #d1d5db;
  --text: #1a1d27;
  --muted: #6b7280;
  --accent: #3b82f6;
  /* Other colors inherit from dark mode */
}
```

---

## New CSS Classes

### Skeleton Loading
- `.skeleton` - Base pulsing gradient
- `.skeleton-text` - 14px height for text
- `.skeleton-value` - 28px height for values
- `.skeleton-chart` - 200px height for charts
- `@keyframes shimmer` - 1.5s infinite animation

### Goal Tracker
- `.goal-tracker-content` - Container padding
- `.goal-progress-bar` - Progress bar container
- `.goal-progress-fill` - Animated progress fill
- `.goal-stats` - 3-column grid for stat cards
- `.goal-stat-item` - Individual stat item
- `.goal-stat-label` - Stat label styling
- `.goal-stat-value` - Stat value styling
- `.goal-edit-btn` - Edit button styling

### Theme Toggle
- `.theme-toggle` - Button styling (no background)
- `[data-theme="light"]` - Light mode selector

### Pull-to-Refresh
- `#ptr` (ID) - Container (inline styles only)

### Breakeven
- `.breakeven-container` - Chart container
- `.breakeven-no-data` - Empty state message

---

## HTML Sections Added

### Goal Tracker
```html
<div id="sec-goal-tracker" class="sec-wrap" data-span="4">
  <!-- Progress bar, stats, edit button -->
</div>
```
- Positioned after KPI cards
- Before sec-chart-asset

### Breakeven Analysis
```html
<div id="sec-breakeven" class="sec-wrap" data-span="4">
  <!-- Horizontal bar chart or empty state -->
</div>
```
- Positioned after sec-monthly-table
- Before closing sec-grid-container

### Pull-to-Refresh
```html
<div id="ptr">
  <span id="ptr-text">↓ 당겨서 새로고침</span>
</div>
```
- Positioned right after `<div id="dashboard">`

### Theme Toggle Button
```html
<button class="theme-toggle" id="themeToggleBtn" onclick="toggleTheme()">🌙</button>
```
- Added to header before refresh button

### Mobile Theme Tab
```html
<button class="mtab-item" id="mtab-theme" onclick="toggleTheme()">
  <span class="mtab-icon">🌙</span>테마
</button>
```
- Added to mobile tab bar before layout button

---

## Data Flow

### Data Loading Sequence
1. User opens dashboard or clicks refresh
2. `loadData()` called
3. `showSkeletons()` called to show placeholders
4. Fetch request to Apps Script
5. Data received and `renderDashboard(data)` called
6. Skeletons replaced by actual content
7. Charts initialized/updated
8. `renderGoalTracker()` and `renderBreakevenChart()` called
9. Layout loaded from localStorage

---

## Browser Compatibility

- **Mobile gesture**: Touch events (iOS Safari, Chrome Mobile)
- **Dark mode**: CSS custom properties, attribute selectors
- **Charts**: Chart.js 4.5.1
- **Storage**: localStorage API
- **Responsive**: CSS Grid, Flexbox, media queries

---

## Performance Notes

1. **Skeleton Loading**: Reduces CLS (Cumulative Layout Shift)
2. **Pull-to-Refresh**: Only active when scrollY === 0 (minimal overhead)
3. **Benchmark Calculation**: Done in-memory, no external API calls
4. **Theme Toggle**: CSS-only switching after initial setup
5. **localStorage**: Used for preferences (< 50KB total)

---

## Testing Checklist

- [ ] Skeleton loading appears before data loads
- [ ] Pull gesture triggers refresh when > 60px
- [ ] Goal tracker shows correct percentage
- [ ] Goal edit dialog accepts valid numbers
- [ ] Breakeven chart shows only losing positions
- [ ] Benchmark toggle works on cumulative return chart
- [ ] Dark/light theme toggles and persists
- [ ] Mobile tab bar theme button works
- [ ] Header theme button works
- [ ] All sections visible/hideable in layout panel
- [ ] No console errors on page load
- [ ] Responsive on mobile (375px) and desktop (1200px+)

---

## Known Limitations

1. **Benchmark Data**: Uses simulated historical averages, not real index data
2. **Goal ETA**: Linear projection; assumes consistent monthly growth
3. **Pull-to-Refresh**: Desktop browsers won't show visual feedback (but still works)
4. **Theme Preference**: Requires JavaScript enabled
5. **Skeleton Duration**: Fixed 1.5s animation regardless of actual load time

---

## Future Enhancement Opportunities

1. Real S&P 500 / NASDAQ index data integration
2. Configurable skeleton loading duration
3. Pull-to-refresh haptic feedback (on supported devices)
4. Advanced goal projection (exponential growth, seasonal adjustment)
5. Breakeven alert notifications
6. System theme preference detection (prefers-color-scheme)
7. Benchmark selection dropdown (different indices)
8. Goal achievement milestone notifications

---

## Support & Debugging

### Common Issues

**Skeleton not showing**:
- Check `showSkeletons()` is called in `loadData()`
- Verify CSS .skeleton classes are defined
- Check browser console for errors

**Pull-to-refresh not working**:
- Ensure touch event listeners attached to document
- Check scrollY === 0 on initial touch
- Verify `loadData()` is callable

**Theme not persisting**:
- Check localStorage.setItem() in `setTheme()`
- Verify data-theme attribute set on documentElement
- Check localStorage quota not exceeded

**Breakeven chart not showing**:
- Verify `breakevenChart` canvas ID correct
- Check `renderBreakevenChart()` called in `renderDashboard()`
- Verify holdings have returnRate property

---

## Code Statistics

- **Total Functions**: 200+ (including new ones)
- **CSS Classes**: 150+ (including new ones)
- **Event Handlers**: 15+ (including touch handlers)
- **localStorage Keys**: 5
- **Chart.js Instances**: 9
- **Global Variables**: 10+

