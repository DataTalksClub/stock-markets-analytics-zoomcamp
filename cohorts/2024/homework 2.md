## Module 2 Homework

In this homework, we're going to combine data from various sources to process it in Pandas and generate additional fields.

If not stated otherwise, please use the [Colab](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/02-dataframe-analysis/Module2_Colab_Working_with_the_data.ipynb) covered at the livestream to re-use the code snippets.

---
### Question 1: IPO Filings Web Scraping and Data Processing

**What's the total sum ($m) of 2023 filings that happenned of Fridays?**

Re-use the [Code Snippet 1] example to get the data from web for this endpoint: https://stockanalysis.com/ipos/filings/
Convert the 'Filing Date' to datetime(), 'Shares Offered' to float64 (if '-' is encountered, populate with NaNs).
Define a new field 'Avg_price' based on the "Price Range", which equals to NaN if no price is specified, to the price (if only one number is provided), or to the average of 2 prices (if a range is given).
You may be inspired by the function `extract_numbers()` in [Code Snippet 4], or you can write your own function to "parse" a string.
Define a column "Shares_offered_value", which equals to "Shares Offered" * "Avg_price" (when both columns are defined; otherwise, it's NaN)

Find the total sum in $m (closest INTEGER number) for all fillings during 2023, which happened on Fridays (`.dt.dayofweek()==4`). You should see 32 records in total, 24 of it is not null.

(additional: you can read about [S-1 IPO filing](https://www.dfinsolutions.com/knowledge-hub/thought-leadership/knowledge-resources/what-s-1-ipo-filing) to understand the context)

---
### Question 2:  IPOs "Fixed days hold" strategy


**Find the optimal number of days X (between 1 and 30), where 75% quantile growth is the highest?**


Reuse [Code Snippet 1] to retrieve the list of IPOs from 2023 and 2024 (from URLs: https://stockanalysis.com/ipos/2023/ and https://stockanalysis.com/ipos/2024/). Get all OHLCV daily prices for all stocks with an "IPO date" before March 1, 2024 ("< 2024-03-01") - 185 tickers. Sometimes you may need to adjust the symbol name (e.g., 'IBAC' on stockanalysis.com -> 'IBACU' on Yahoo Finance) to locate OHLCV prices for all stocks.

Let's assume you managed to buy a new stock (listed on IPO) on the first day at the [Adj Close] price]. Your strategy is to hold for exactly X full days (where X is between 1 and 30) and sell at the "Adj. Close" price in X days (e.g., if X=1, you sell on the next day).
Find X, when the 75% quantile growth (among 185 investments) is the highest. 

HINTs:
* You can generate 30 additional columns: growth_future_1d ... growth_future_30d, join that with the table of min_dates (first day when each stock has data on Yahoo Finance), and perform vector operations on the resulting dataset.
* You can use the `DataFrame.describe()` function to get mean, min, max, 25-50-75% quantiles.


Addtional: 
* You can also ensure that the mean and 50th percentile (median) investment returns are negative for most X values, implying a wager for a "lucky" investor who might be in the top 25%.
* What's your recommendation: Do you suggest pursuing this strategy for an optimal X?


---
### Question 3: Is Growth Concentrated in the Largest Stocks?

**Get the share of days when Large Stocks outperform (growth_7d - growth over 7 periods back) the Largest stocks?**


Reuse [Code Snippet 5] to obtain OHLCV stats for 33 stocks 
for 10 full years of data (2014-01-01 to 2023-12-31):

`US_STOCKS = ['MSFT', 'AAPL', 'GOOG', 'NVDA', 'AMZN', 'META', 'BRK-B', 'LLY', 'AVGO','V', 'JPM']`

`EU_STOCKS = ['NVO','MC.PA', 'ASML', 'RMS.PA', 'OR.PA', 'SAP', 'ACN', 'TTE', 'SIE.DE','IDEXY','CDI.PA']`

`INDIA_STOCKS = ['RELIANCE.NS','TCS.NS','HDB','BHARTIARTL.NS','IBN','SBIN.NS','LICI.NS','INFY','ITC.NS','HINDUNILVR.NS','LT.NS']`

`LARGEST_STOCKS = US_STOCKS + EU_STOCKS + INDIA_STOCKS`
<br/>

Now let's add the top 12-22 stocks (as of end-April 2024):
<br/>

`NEW_US = ['TSLA','WMT','XOM','UNH','MA','PG','JNJ','MRK','HD','COST','ORCL']`

`NEW_EU = ['PRX.AS','CDI.PA','AIR.PA','SU.PA','ETN','SNY','BUD','DTE.DE','ALV.DE','MDT','AI.PA','EL.PA']`

`NEW_INDIA = ['BAJFINANCE.NS','MARUTI.NS','HCLTECH.NS','TATAMOTORS.NS','SUNPHARMA.NS','ONGC.NS','ADANIENT.NS','ADANIENT.NS','NTPC.NS','KOTAKBANK.NS','TITAN.NS']`

`LARGE_STOCKS = NEW_EU + NEW_US + NEW_INDIA`

You should be able to obtain stats for 33 LARGEST STOCKS and 32 LARGE STOCKS.

Calculate  `growth_7d` for every stock and every day.
Get the average daily `growth_7d` for the LARGEST_STOCKS group vs. the LARGE_STOCKS group.

For example, for the first of data you should have:
| Date   |      ticker_category      |  growth_7d |
|----------|:-------------:|------:|
| 2014-01-01 |  LARGE | 1.011684 |
| 2014-01-01 |   LARGEST   |   1.011797 |

On that day, the LARGEST group was growing faster than LARGE one (new stocks).

Calculate the number of days when the LARGE GROUP (new smaller stocks) outperforms the LARGEST GROUP, divide it by the total number of trading days (which should be 2595 days), and convert it to a percentage (closest INTEGER value). For example, if you find that 1700 out of 2595 days meet this condition, it means that 1700/2595 = 0.655, or approximately 66% of days, the LARGE stocks were growing faster than the LARGEST ones. This suggests that you should consider extending your dataset with more stocks to seek higher growth.

---
## Submitting the solutions

Form for submitting: tbd_link
