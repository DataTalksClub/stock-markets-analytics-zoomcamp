# Automation Update Summaries

This file tracks notable updates to the `05-deployment-and-automation` pipeline over time, most recent first.

---

# 2026 Automation Update Summary

## Key Changes Made

### 1. yfinance Dependency Upgrade (requirements.txt)
- **Before**: `yfinance==0.2.40` (broken against Yahoo Finance's current API — every
  ticker returned `"possibly delisted; No price data found"`)
- **After**: `yfinance==1.7.0`
- **Verified**: `yf.Ticker("AAPL").history(...)` confirmed to return real data again;
  this matches the same `ticker_obj.history()` approach already used in the 2026
  Colab notebooks (01–05), so no code-logic change was needed, just the dependency bump.

### 2. Stock Universe Refresh (data_repo.py)
- **Before**: 190 US stocks hardcoded in 2025, several tickers had gone stale/renamed:
  - `SNYS` — plain typo, not a real ticker (404 from Yahoo Finance)
  - `MMC` — Marsh & McLennan renamed its ticker to `MRSH`
  - `FI` — incorrect; Fiserv's real ticker is `FISV`
  - `BK` — Bank of New York Mellon renamed its ticker to `BNY`
  - These 4 silently failed on every run (no data downloaded, no fallback worked either)
- **After**: Re-pulled the top-190 US companies by market cap (all >$50B) directly from
  the [companiesmarketcap.com CSV export](https://companiesmarketcap.com/eur/usa/largest-companies-in-the-usa-by-market-cap/?download=csv),
  excluding SpaceX (`SPCX`, privately held, not tradable via yfinance). Every ticker in
  the new list was individually validated against `yf.Ticker(...).history()`.
- **Result**: All 190 tickers now download successfully with zero skips/delisted errors
  (previously 4/190 silently failed every run).
- **New additions vs. old list**: `GEV`, `PLTR`, `SNOW`, `APP`, `HOOD`, `DDOG`, `VRT`,
  `CVNA`, `MNST`, `MRNA`, `LITE`, `RCL`, `TRGP`, `LNG`, `BE`, `CMI`, `WDC`, `SNDK`,
  `NET`, `GLW`, `VLO`, `PWR`, `MRSH`, `BNY`, `FISV`, `SNPS` (fixed names)
- **Dropped (fell below $50B threshold or superseded)**: `NKE`, `ZTS`, `PYPL`, `CMG`,
  `WDAY`, `BDX`, `TFC`, `ROP`, `ADSK`, `MET`, `O`, `OKE`, `AZO`, `SRE`, `PCG`, `CPRT`,
  `OXY`, `KDP`, `ALL`, `DHI`, `PSA`, `AFL`, `CARR`

### 3. Model Update (train.py)
- **Before**: `RandomForestClassifier(max_depth=17, n_estimators=200)`, no decision
  rule applied — only rank-based top/bottom selection
- **After**: `RandomForestClassifier(max_depth=13, n_estimators=100)` — the new best
  model identified in `cohorts/2026/homework4.md`, paired with a `rule=0.55` decision
  threshold (`pred10_rf_best_rule_55`)
- `make_inference()` now accepts a `rule_threshold` parameter (default `0.55`) and adds
  a `{pred_name}_rule_55` column (`1` if predicted probability ≥ 0.55 else `0`)

### 4. main.py Output Update
- Passes `rule_threshold=0.55` into `make_inference()`
- Displays the new `pred_rf_30d_best_rule_55` column alongside Close/Ticker/Date/rank
  in the top-3 and bottom-3 daily prediction printouts

## Files Modified
- requirements.txt: yfinance version bump
- data_repo.py: refreshed `US_STOCKS` list
- train.py: new RandomForest hyperparameters + rule-55 threshold column
- main.py: display updated prediction name/rule column

---
**Version**: 2026.1.0

---

# 2025 Automation Update Summary

## Key Changes Made

### 1. Stock Universe Update (data_repo.py)
- **Before**: ~53 stocks (US + EU + India)
- **After**: 190 US stocks only (>$50B market cap)
- **Change**: Removed EU_STOCKS and INDIA_STOCKS

### 2. Prediction Horizon Change
- **Before**: 5-day predictions
- **After**: 30-day predictions
- **Files**: data_repo.py, train.py, main.py

### 3. API Method Update (data_repo.py)
- **Before**: yf.download()
- **After**: ticker_obj.history()

### 4. Triple-Fallback Data System (March 2025)
- **Added**: Stooq and FRED fallbacks for blocked yfinance API
- **Fixed**: VIX, Oil, Bitcoin data now retrieved via FRED
- **Updated**: _fetch_index_with_fallback() method with 3-tier fallback
- **Result**: 100% data coverage

### 5. Transform Script Fixes
- **Fixed**: 'Adj Close' column compatibility with Stooq data
- **Fixed**: DataFrame index conflicts in technical indicator merges

## Files Modified
- data_repo.py: Stock lists, API methods, fallback system
- train.py: 30-day target variables
- main.py: Prediction naming and outputs
- transform.py: Stooq compatibility fixes

---
**Version**: 2025.2.0
