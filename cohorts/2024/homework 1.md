## Module 1 Homework

In this homework, we're going to download finance data from various sources and make simple calculations/analysis.

### Question 1: [Macro] Average growth of GDP in 2023
**What is the average growth (in %) of GDP in 2023 (rounded to 1 digit after the point)**

Download the timeseries Real Gross Domestic Product (GDPC1) from FRED (https://fred.stlouisfed.org/series/GDPC1). 
Calculate year-over-year (YoY) growth rate (that is, divide current value to one 4 quarters ago). Find the average YoY growth in 2023 (average from 4 YoY numbers).
Round to 1 digit after the decimal point: e.g. if you get 5.66% growth => you should answer  5.7

### Question 2. [Macro] Inverse "Treasury Yield"
Download DGS2 and DGS10 interest rates series (https://fred.stlouisfed.org/series/DGS2,
 https://fred.stlouisfed.org/series/DGS10). Join them together to one dataframe on date (you might need to read about pandas.DataFrame.join()), calculate the difference dgs10-dgs2 daily.

Find the min value of (dgs10-dgs2) after since year 2000 (2000-01-01) and write it down as an answer, round to 1 digit after the decimal point.

(Additional: think about what does the "inverted yield curve" mean for the market and investors? do you see the same thing in your country/market of interest? Do you think it can be a good predictive feature for the models?)

### Question 3. tbd

### Question 4. tbd

### Question 5. tbd

### Question 6. tbd

### Question 7. tbd
