import numpy as np

import pandas as pd
import yfinance as yf

from tqdm import tqdm
from datetime import datetime, timedelta

import time
import os
import pandas_datareader as pdr

# https://companiesmarketcap.com/usa/largest-companies-in-the-usa-by-market-cap/
US_STOCKS = ['MSFT', 'AAPL', 'GOOG', 'NVDA', 'AMZN', 'META', 'BRK-B', 'LLY', 'AVGO','V', 'JPM','TSLA',
             'WMT','XOM', 'UNH', 'MA','PG', 'ORCL', 'COST', 'JNJ', 'HD', 'MRK', 'BAC', 'ABBV', 'CVX',
             'NFLX', 'KO', 'AMD', 'ADBE', 'CRM', 'PEP', 'QCOM', 'TMO', 'TMUS', 'WFC', 'CSCO', 'AMAT', 'DHR',
             'MCD','DIS', 'ABT', 'TXN', 'GE', ' INTU', 'VZ', 'AMGN', 'AXP', 'CAT', 'IBM', 'PFE', 'PM', 'MS']
# https://companiesmarketcap.com/european-union/largest-companies-in-the-eu-by-market-cap/
EU_STOCKS = ['NVO','MC.PA', 'ASML', 'RMS.PA', 'OR.PA', 'SAP', 'ACN', 'TTE', 'SIE.DE','IDEXY','CDI.PA']
# https://companiesmarketcap.com/india/largest-companies-in-india-by-market-cap/
INDIA_STOCKS = ['RELIANCE.NS','TCS.NS','HDB','BHARTIARTL.NS','IBN','SBIN.NS','LICI.NS','INFY','ITC.NS','HINDUNILVR.NS','LT.NS']



class DataRepository:
  ticker_df: pd.DataFrame
  indexes_df: pd.DataFrame
  macro_df: pd.DataFrame

  min_date: str
  ALL_TICKERS: list[str] = US_STOCKS  + EU_STOCKS + INDIA_STOCKS

  def __init__(self):
    self.ticker_df = None
    self.indexes_df = None
    self.macro_df = None

  def _get_growth_df(self, df:pd.DataFrame, prefix:str)->pd.DataFrame:
    '''Help function to produce a df with growth columns'''
    for i in [1,3,7,30,90,365]:
      df['growth_'+prefix+'_'+str(i)+'d'] = df['Adj Close'] / df['Adj Close'].shift(i)
      GROWTH_KEYS = [k for k in df.keys() if k.startswith('growth')]
    return df[GROWTH_KEYS]
    
  def fetch(self, min_date = None):
    '''Fetch all data from APIs'''

    print('Fetching Tickers info from YFinance')
    self.fetch_tickers(min_date=min_date)
    print('Fetching Indexes info from YFinance')
    self.fetch_indexes(min_date=min_date)
    print('Fetching Macro info from FRED (Pandas_datareader)')
    self.fetch_macro(min_date=min_date)
  
  def fetch_tickers(self, min_date=None):
    '''Fetch Tickers data from the Yfinance API'''
    if min_date is None:
      min_date = "1970-01-01"
    else:
      min_date = pd.to_datetime(min_date)   

    print(f'Going download data for this tickers: {self.ALL_TICKERS[0:3]}')
    tq = tqdm(self.ALL_TICKERS)
    for i,ticker in enumerate(tq):
      tq.set_description(ticker)

      # Download stock prices from YFinance
      historyPrices = yf.download(tickers = ticker,
                          # period = "max",
                          start=min_date,
                          interval = "1d")

      # generate features for historical prices, and what we want to predict

      if ticker in US_STOCKS:
        historyPrices['ticker_type'] = 'US'
      elif ticker in EU_STOCKS:
        historyPrices['ticker_type'] = 'EU'
      elif ticker in INDIA_STOCKS:
        historyPrices['ticker_type'] = 'INDIA'
      else:
        historyPrices['ticker_type'] = 'ERROR'

      historyPrices['Ticker'] = ticker
      historyPrices['Year']= historyPrices.index.year
      historyPrices['Month'] = historyPrices.index.month
      historyPrices['Weekday'] = historyPrices.index.weekday
      historyPrices['Date'] = historyPrices.index.date

      # historical returns
      for i in [1,3,7,30,90,365]:
          historyPrices['growth_'+str(i)+'d'] = historyPrices['Adj Close'] / historyPrices['Adj Close'].shift(i)
      historyPrices['growth_future_5d'] = historyPrices['Adj Close'].shift(-5) / historyPrices['Adj Close']

      # Technical indicators
      # SimpleMovingAverage 10 days and 20 days
      historyPrices['SMA10']= historyPrices['Close'].rolling(10).mean()
      historyPrices['SMA20']= historyPrices['Close'].rolling(20).mean()
      historyPrices['growing_moving_average'] = np.where(historyPrices['SMA10'] > historyPrices['SMA20'], 1, 0)
      historyPrices['high_minus_low_relative'] = (historyPrices.High - historyPrices.Low) / historyPrices['Adj Close']

      # 30d rolling volatility : https://ycharts.com/glossary/terms/rolling_vol_30
      historyPrices['volatility'] =   historyPrices['Adj Close'].rolling(30).std() * np.sqrt(252)

      # what we want to predict
      historyPrices['is_positive_growth_5d_future'] = np.where(historyPrices['growth_future_5d'] > 1, 1, 0)

      # sleep 1 sec between downloads - not to overload the API server
      time.sleep(1)

      if self.ticker_df is None:
        self.ticker_df = historyPrices
      else:
        self.ticker_df = pd.concat([self.ticker_df, historyPrices], ignore_index=True)
      
  def fetch_indexes(self, min_date=None):
    '''Fetch Indexes data from the Yfinance API'''

    if min_date is None:
      min_date = "1970-01-01"
    else:
      min_date = pd.to_datetime(min_date)   
    
    # https://finance.yahoo.com/quote/%5EGDAXI/
    # DAX PERFORMANCE-INDEX
    dax_daily = yf.download(tickers = "^GDAXI",
                        start = min_date,    
                        # period = "max",
                        interval = "1d")
    # sleep 1 sec between downloads - not to overload the API server
    time.sleep(1)
    
    # https://finance.yahoo.com/quote/%5EGSPC/
    # SNP - SNP Real Time Price. Currency in USD
    snp500_daily = yf.download(tickers = "^GSPC",
                     start = min_date,          
                    #  period = "max",
                     interval = "1d")
    # sleep 1 sec between downloads - not to overload the API server
    time.sleep(1)
    
    # https://finance.yahoo.com/quote/%5EDJI?.tsrc=fin-srch
    # Dow Jones Industrial Average
    dji_daily = yf.download(tickers = "^DJI",
                     start = min_date,       
                    #  period = "max",
                     interval = "1d")
    # sleep 1 sec between downloads - not to overload the API server
    time.sleep(1)
    
    # https://finance.yahoo.com/quote/EPI/history?p=EPI
    # WisdomTree India Earnings Fund (EPI) : NYSEArca - Nasdaq Real Time Price (USD)
    epi_etf_daily = yf.download(tickers = "EPI",
                     start = min_date,            
                    #  period = "max",
                     interval = "1d")
    # sleep 1 sec between downloads - not to overload the API server
    time.sleep(1)
    
    # VIX - Volatility Index
    # https://finance.yahoo.com/quote/%5EVIX/
    vix = yf.download(tickers = "^VIX",
                        start = min_date, 
                        # period = "max",
                        interval = "1d")
    # sleep 1 sec between downloads - not to overload the API server
    time.sleep(1)
    
    # GOLD
    # https://finance.yahoo.com/quote/GC%3DF
    gold = yf.download(tickers = "GC=F",
                     start = min_date,   
                    #  period = "max",
                     interval = "1d")
    # sleep 1 sec between downloads - not to overload the API server
    time.sleep(1)
    
    # WTI Crude Oil
    # https://uk.finance.yahoo.com/quote/CL=F/
    crude_oil = yf.download(tickers = "CL=F",
                     start = min_date,          
                    #  period = "max",
                     interval = "1d")
    # sleep 1 sec between downloads - not to overload the API server
    time.sleep(1)

    # Brent Oil
    # WEB: https://uk.finance.yahoo.com/quote/BZ=F/
    brent_oil = yf.download(tickers = "BZ=F",
                            start = min_date,
                            # period = "max",
                            interval = "1d")
    # sleep 1 sec between downloads - not to overload the API server
    time.sleep(1)


    # BTC_USD
    # WEB: https://finance.yahoo.com/quote/BTC-USD/
    btc_usd =  yf.download(tickers = "BTC-USD",
                           start = min_date,
                          #  period = "max",
                           interval = "1d")
    # sleep 1 sec between downloads - not to overload the API server
    time.sleep(1)
    
    # Prepare to merge
    dax_daily_to_merge = self._get_growth_df(dax_daily, 'dax')
    snp500_daily_to_merge = self._get_growth_df(snp500_daily, 'snp500')
    dji_daily_to_merge = self._get_growth_df(dji_daily, 'dji')
    epi_etf_daily_to_merge = self._get_growth_df(epi_etf_daily, 'epi')
    vix_to_merge = vix.rename(columns={'Adj Close':'vix_adj_close'})[['vix_adj_close']]
    gold_to_merge = self._get_growth_df(gold, 'gold')
    crude_oil_to_merge = self._get_growth_df(crude_oil,'wti_oil')
    brent_oil_to_merge = self._get_growth_df(brent_oil,'brent_oil')
    btc_usd_to_merge = self._get_growth_df(btc_usd,'btc_usd')

    # Merging
    m2 = pd.merge(snp500_daily_to_merge,
                               dax_daily_to_merge,
                               left_index=True,
                               right_index=True,
                               how='left',
                               validate='one_to_one')
    
    m3 = pd.merge(m2,
                  dji_daily_to_merge,
                  left_index=True,
                  right_index=True,
                  how='left',
                  validate='one_to_one')
    
    m4 = pd.merge(m3,
                  epi_etf_daily_to_merge,
                  left_index=True,
                  right_index=True,
                  how='left',
                  validate='one_to_one')
    
    m5 = pd.merge(m4,
                  vix_to_merge,
                  left_index=True,
                  right_index=True,
                  how='left',
                  validate='one_to_one')
    
    m6 = pd.merge(m5,
                  gold_to_merge,
                  left_index=True,
                  right_index=True,
                  how='left',
                  validate='one_to_one')
    
    m7 = pd.merge(m6,
                  crude_oil_to_merge,
                  left_index=True,
                  right_index=True,
                  how='left',
                  validate='one_to_one')    

    m8 = pd.merge(m7,
                  brent_oil_to_merge,
                  left_index=True,
                  right_index=True,
                  how='left',
                  validate='one_to_one')  

    m9 = pd.merge(m8,
                  btc_usd_to_merge,
                  left_index=True,
                  right_index=True,
                  how='left',
                  validate='one_to_one')  

    self.indexes_df = m9

  def fetch_macro(self, min_date=None):
    '''Fetch Macro data from FRED (using Pandas datareader)'''

    if min_date is None:
      min_date = "1970-01-01"
    else:
      min_date = pd.to_datetime(min_date)

    # Real Potential Gross Domestic Product (GDPPOT), Billions of Chained 2012 Dollars, QUARTERLY
    # https://fred.stlouisfed.org/series/GDPPOT
    gdppot = pdr.DataReader("GDPPOT", "fred", start=min_date)
    gdppot['gdppot_us_yoy'] = gdppot.GDPPOT/gdppot.GDPPOT.shift(4)-1
    gdppot['gdppot_us_qoq'] = gdppot.GDPPOT/gdppot.GDPPOT.shift(1)-1
    # sleep 1 sec between downloads - not to overload the API server
    time.sleep(1)

    # # "Core CPI index", MONTHLY
    # https://fred.stlouisfed.org/series/CPILFESL
    # The "Consumer Price Index for All Urban Consumers: All Items Less Food & Energy"
    # is an aggregate of prices paid by urban consumers for a typical basket of goods, excluding food and energy.
    # This measurement, known as "Core CPI," is widely used by economists because food and energy have very volatile prices.
    cpilfesl = pdr.DataReader("CPILFESL", "fred", start=min_date)
    cpilfesl['cpi_core_yoy'] = cpilfesl.CPILFESL/cpilfesl.CPILFESL.shift(12)-1
    cpilfesl['cpi_core_mom'] = cpilfesl.CPILFESL/cpilfesl.CPILFESL.shift(1)-1    
    time.sleep(1)

    # Fed rate https://fred.stlouisfed.org/series/FEDFUNDS
    fedfunds = pdr.DataReader("FEDFUNDS", "fred", start=min_date)
    time.sleep(1)


    # https://fred.stlouisfed.org/series/DGS1
    dgs1 = pdr.DataReader("DGS1", "fred", start=min_date)
    time.sleep(1)

    # https://fred.stlouisfed.org/series/DGS5
    dgs5 = pdr.DataReader("DGS5", "fred", start=min_date)
    time.sleep(1)

    # https://fred.stlouisfed.org/series/DGS10
    dgs10 = pdr.DataReader("DGS10", "fred", start=min_date)
    time.sleep(1)

    gdppot_to_merge = gdppot[['gdppot_us_yoy','gdppot_us_qoq']]
    cpilfesl_to_merge = cpilfesl[['cpi_core_yoy','cpi_core_mom']]


    # Merging - start from daily stats (dgs1)
    m2 = pd.merge(dgs1,
                  dgs5,
                  left_index=True,
                  right_index=True,
                  how='left',
                  validate='one_to_one')
    
    m2['Date'] = m2.index

    # gdppot_to_merge is Quarterly (but m2 index is daily)
    m2['Quarter'] = m2.Date.dt.to_period('Q').dt.to_timestamp()

    m3 = pd.merge(m2,
                  gdppot_to_merge,
                  left_on='Quarter',
                  right_index=True,
                  how='left',
                  validate='many_to_one')

    # gdppot_to_merge is Quarterly
    # m3.index = pd.to_datetime(m3.index) # Ensure the index is a DatetimeIndex
    m3['Month'] = m2.Date.dt.to_period('M').dt.to_timestamp()

    m4 = pd.merge(m3,
                  fedfunds,
                  left_on='Month',
                  right_index=True,
                  how='left',
                  validate='many_to_one')
    
    m5 = pd.merge(m4,
                  cpilfesl_to_merge,
                  left_on='Month',
                  right_index=True,
                  how='left',
                  validate='many_to_one')
       
    m6 = pd.merge(m5,
                  dgs10,
                  left_index=True,
                  right_index=True,
                  how='left',
                  validate='one_to_one')
    
    fields_to_fill = ['cpi_core_yoy',	'cpi_core_mom','FEDFUNDS','DGS1','DGS5','DGS10']
    # Fill missing values in selected fields with the last defined value
    for field in fields_to_fill:
      m6[field] = m6[field].ffill()

    self.macro_df =  m6   

  def persist(self, data_dir:str):
    '''Save dataframes to files in a local directory 'dir' '''
    os.makedirs(data_dir, exist_ok=True)

    file_name = 'tickers_df.parquet'
    if os.path.exists(file_name):
      os.remove(file_name)
    self.ticker_df.to_parquet(os.path.join(data_dir,file_name), compression='brotli')
  
    file_name = 'indexes_df.parquet'
    if os.path.exists(file_name):
      os.remove(file_name)
    self.indexes_df.to_parquet(os.path.join(data_dir,file_name), compression='brotli')
  
    file_name = 'macro_df.parquet'
    if os.path.exists(file_name):
      os.remove(file_name)
    self.macro_df.to_parquet(os.path.join(data_dir,file_name), compression='brotli')

  def load(self, data_dir:str):
    """Load files from the local directory"""
    self.ticker_df = pd.read_parquet(os.path.join(data_dir,'tickers_df.parquet'))
    self.macro_df = pd.read_parquet(os.path.join(data_dir,'macro_df.parquet'))
    self.indexes_df = pd.read_parquet(os.path.join(data_dir,'indexes_df.parquet'))