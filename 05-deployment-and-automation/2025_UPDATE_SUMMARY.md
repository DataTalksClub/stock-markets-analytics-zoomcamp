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
