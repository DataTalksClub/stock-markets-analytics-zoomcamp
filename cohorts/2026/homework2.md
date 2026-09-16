## Module 2 Homework (2026 Cohort)

In this homework, we're going to combine data from various sources to process it in Pandas and generate additional fields.

If not stated otherwise, please use the code snippets covered in the livestream to download and process the data.

---
### Question 1: [IPO] Withdrawn IPOs by Company Type

**What is the total withdrawn IPO value (in $ millions) for the company class with the highest total withdrawal value?**

From the Recently Filed IPO list ([iposcoop.com/ipos-recently-filed](https://www.iposcoop.com/ipos-recently-filed/)), collect and process the data to find out which company type saw the most withdrawn IPO value before Sep 11, 2026.

#### Steps:
1. **Data Loading:** Use `pandas.read_html()` with the URL above to load the IPO recently filed table. Filter the rows to keep only those where 'Expected To Trade' is 'Withdrawn'. You should identify 32 entries.
2. **Company Classification:** Create a new column called **Company Type**, categorizing company names based on patterns (order matters, assign the first matched value):
    - "Technologies" -> Technologies
    - "Acquisition Corp", "Acquisition Corporation", or "Corp" -> Acquisition Corp
    - "Inc" or "Incorporated" -> Inc.
    - "Group" -> Group
    - "Ltd" or "Limited" -> Limited
    - "Holdings" or "Holding" -> Holdings
    - Others -> Other

    **Note:** The order of the rules above is important — use the first matching rule. For example, "EUPEC International Group Ltd." will be classified as `Group` (not `Limited`), since the "Group" rule appears before the "Ltd"/"Limited" rule. Also, matches must be exact: "Xinxu Copper Industry Technology Ltd." will be classified as `Limited` (not `Technologies`), because "Technology" does not match the "Technologies" pattern.
3. **Price Parsing:** Define a new field **Avg_price** by parsing the 'Price Low' and 'Price High' fields. Create a function to extract numeric values (e.g., '$8.00' -> 8.0) and calculate the average between low and high. Handle '-' or missing values as `None`/`NaN`.
4. **Numeric Conversion:** Convert 'Shares (millions)' and 'Est \$ Vol (millions)' to numeric formats, cleaning currency symbols (\$) and commas where necessary.
5. **Value Calculation:** Create a new column **Shares_offered_value**:
    - If `Shares (millions) * Avg_price` is not null, use that value.
    - Otherwise, use the value from the `Est $ Vol (millions)` column.
6. **Aggregation:** Group by **Company Type** and calculate the sum of **Shares_offered_value**.

**Answer:** Which class had the highest total value of withdrawals, and what was that value?

---
### Question 2: [IPO] Median Sharpe Ratio for 2025 IPOs (First 8 Months)

**What is the median Sharpe ratio (as of 11 September 2026) for companies that went public before 1 September 2025?**

The goal is to replicate the large-scale `yfinance` OHLCV data download and perform basic financial calculations on IPO stocks.

#### Steps:
1.  **Data Loading:** Download the list of 231 IPOs in 2025 from `https://www.iposcoop.com/2025-pricings/`.
2.  **Filtering:** Filter the list to keep only those IPOs with an 'Offer Date' before **1 September 2025**. Also, exclude entries with a 0% return to ensure active tickers are processed. You should see 148 stocks.
3.  **Data Download:** Use `yfinance` to download daily stock data for the filtered tickers and save it to the `stocks_df` dataframe. Make sure you can correctly process the cases when stocks are not present in Yahoo Finance (probably delisted). At this stage you should see about 134 stocks.
4.  **Feature Engineering:**
    *   Define `growth_252d` as `Close / Close.shift(252)` to represent growth after approximately one year of trading.
    *   Calculate **annualized volatility** using the specific formula: `stocks_df['volatility'] = stocks_df['Close'].rolling(30).std() * np.sqrt(252)`.
5.  **Sharpe Ratio Calculation:** Calculate the Sharpe ratio assuming a risk-free rate of **5.0%** (0.05) - it is close to the current value of the US 10Y Treasury bond yield:
    *   `stocks_df['Sharpe'] = (stocks_df['growth_252d'] - 0.05) / stocks_df['volatility']`
6.  **Final Analysis:** Filter the resulting DataFrame to keep data only for the trading day **'2026-09-11'** and compute descriptive statistics (using the `describe()` function).

#### Expected Observations:
*   Compare the median vs. mean for `growth_252d` to see if high-growth outliers are biasing the average.
*   Identify the count of stocks that successfully reached the 252-day trading milestone.
*   Do you see examples of stocks with risk-adjusted returns (Sharpe ratio) more attractive than pure growth statistics?

**Answer:** What is the median Sharpe ratio for these stocks as of September 11, 2026?

---
### Question 3: [IPO] 'Fixed Months Holding Strategy'

**What is the optimal number of months (1 to 12) to hold a newly IPO'd stock in order to maximize the median growth value?**

#### Goal:
Investigate the performance of 2025 IPO stocks over fixed time horizons (1 to 12 months) to identify the holding period that yields the highest median return relative to the first day's closing price.

#### Steps:
1. **Data Source:** Use the existing `stocks_df` containing daily OHLCV data and calculated features for the 2025 IPOs filtered in Question 2.
2. **Feature Engineering:** Calculate 12 future growth columns representing fixed holding periods:
   - `future_growth_1_m`, `future_growth_2_m`, ..., `future_growth_12_m`.
   - Assume 1 month equals 21 trading days (e.g., 1 month = 21 days, 2 months = 42 days, ..., 12 months = 252 days).
3. **Identify Entry Points:** For each ticker, determine the first available trading day (`min_date`) and the corresponding closing price.
4. **Data Alignment:** Perform an inner join between the `min_date` records and the full growth dataset. This isolates the returns for each stock starting specifically from its IPO date.
5. **Median Analysis:** Compute descriptive statistics for these 12 columns. Specifically, identify the month where the **50th percentile (median)** value is highest.

#### Observations:
- Do you observe any trend of the median growth over time? What does it mean for an investor eager to base their strategy on the newly IPOed companies?
- Compare the median to the mean to understand how extreme outliers (high-growth stocks) affect the average versus the typical stock's performance.

**Answer:** Based on the analysis of the filtered tickers, what is the optimal holding period (in months) and its corresponding maximum median growth value?

---
### Question 4: [Strategy] Simple RSI-Based Trading Strategy

**What is the total profit (in $ thousands) you would have earned by investing $1000 every time a stock was oversold (RSI < 30)?**

#### Goal:
Apply a simple rule-based trading strategy using the Relative Strength Index (RSI) technical indicator to identify oversold signals and calculate cumulative profits over a 25-year period.

#### Steps:
1.  **Data Acquisition:** Use the provided brotli-compressed parquet file containing precomputed technical and macro indicators for a broad set of tickers.
    ```python
    import gdown
    import pandas as pd
    file_id = "1grCTCzMZKY5sJRtdbLVCXg8JXA8VPyg-"
    gdown.download(f"https://drive.google.com/uc?id={file_id}", "data.parquet", quiet=False)
    df = pd.read_parquet("data.parquet", engine="pyarrow")
    ```
2.  **Strategy Setup:** Define the RSI threshold for an "oversold" signal as **RSI < 30**.
3.  **Filtering:** Filter the dataset to isolate trades occurring between **2000-01-01** and **2025-06-01** where the RSI signal was triggered.
4.  **Profit Calculation:**
    - Assume an investment of **$1,000** for every signal.
    - Use the **30-day forward return** (`growth_future_30d`) to determine the outcome of each trade.
    - Calculate Net Income: `net_income = 1000 * (selected_df['growth_future_30d'] - 1).sum()`

#### Observations:
- Increasing the threshold from 25 (we used last year) to 30 significantly increases the number of trading opportunities (from ~1,568 to 5,206).
- With an average 30-day return of **1.26%** and a win rate of **55.13%**, the strategy shows consistent, albeit modest, capital growth over the long term.

**Answer:** Based on a few thousands of trades, what is the net income earned (in $ thousands)?

---
### Q5. [Exploratory, Optional] Predicting a Positive-Return IPO

Most of the strategies for investing in IPOs deliver **negative average and median returns** (and even the 75th percentile).

**Question:**
How would you change the strategy if you want to **increase profitability**?

> This is an open-ended brainstorming question — propose ideas for identifying IPOs with positive future returns or building a more effective trading strategy.

---
## Submitting the solutions

Form for submitting: https://courses.datatalks.club/sma-zoomcamp-2026/homework/hw02

---
## Leaderboard

Leaderboard link: https://courses.datatalks.club/sma-zoomcamp-2026/leaderboard

---


