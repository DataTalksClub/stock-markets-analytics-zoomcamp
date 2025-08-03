import numpy as np

import pandas as pd
import yfinance as yf

from tqdm import tqdm
from datetime import datetime, timedelta

import time
import os
import pandas_datareader as pdr

# https://companiesmarketcap.com/usa/largest-companies-in-the-usa-by-market-cap/

# 2025 Update: top-190 US stocks with >$50b market cap
US_STOCKS = [
    "AAPL", "MSFT", "NVDA", "GOOG", "AMZN", "META", "BRK-B", "LLY", "AVGO", "TSLA",
    "JPM", "WMT", "UNH", "V", "XOM", "MA", "PG", "JNJ", "COST", "ORCL", "HD", "ABBV",
    "BAC", "KO", "MRK", "NFLX", "CVX", "ADBE", "PEP", "CRM", "TMUS", "TMO", "AMD",
    "MCD", "CSCO", "WFC", "ABT", "PM", "DHR", "IBM", "TXN", "QCOM", "AXP", "VZ",
    "GE", "AMGN", "INTU", "NOW", "ISRG", "NEE", "CAT", "DIS", "RTX", "MS", "PFE",
    "SPGI", "UNP", "GS", "CMCSA", "AMAT", "UBER", "PGR", "T", "LOW", "SYK", "LMT",
    "HON", "TJX", "BLK", "ELV", "REGN", "BKNG", "COP", "VRTX", "NKE", "BSX", "PLD",
    "SCHW", "C", "PANW", "MMC", "ADP", "KKR", "UPS", "ADI", "AMT", "SBUX", "DE",
    "ANET", "BMY", "HCA", "CI", "KLAC", "FI", "LRCX", "BX", "GILD", "MU", "BA", "SO",
    "MDLZ", "ICE", "MO", "SHW", "DUK", "MCO", "CL", "INTC", "WM", "ZTS", "GD", "CTAS",
    "EQIX", "DELL", "NOC", "CME", "SCCO", "TDG", "SNYS", "APH", "WELL", "MCK", "PH",
    "PYPL", "ITW", "MSI", "PNC", "ABNB", "CMG", "USB", "CVS", "MMM", "FDX", "EOG",
    "ECL", "BDX", "CDNS", "TGT", "WDAY", "PLTR", "CSX", "ORLY", "CRWD", "MAR", "RSG",
    "AJG", "APO", "CARR", "EPD", "SPG", "APD", "AFL", "MRVL", "PSA", "DHI", "NEM",
    "FCX", "ROP", "SLB", "TFC", "FTNT", "EMR", "MPC", "NSC", "CEG", "PSX", "ADSK",
    "COF", "WMB", "ET", "IBKR", "GM", "MET", "O", "AEP", "OKE", "AZO", "HLT", "GEV",
    "SRE", "PCG", "DASH", "TRV", "CPRT", "OXY", "ROST", "KDP", "ALL", "BK", "DLR"
]

# https://companiesmarketcap.com/european-union/largest-companies-in-the-eu-by-market-cap/
EU_STOCKS = [] # 3-Sep-2024 : Remove EU stocks
# ['NVO','MC.PA', 'ASML', 'RMS.PA', 'OR.PA', 'SAP', 'ACN', 'TTE', 'SIE.DE','IDEXY','CDI.PA']
# https://companiesmarketcap.com/india/largest-companies-in-india-by-market-cap/
INDIA_STOCKS = [] # 3-Sep-2024 : Remove Indian stocks
# ['RELIANCE.NS','TCS.NS','HDB','BHARTIARTL.NS','IBN','SBIN.NS','LICI.NS','INFY','ITC.NS','HINDUNILVR.NS','LT.NS']



class DataRepository:
  ticker_df: pd.DataFrame
  indexes_df: pd.DataFrame
  macro_df: pd.DataFrame

  min_date: str
  ALL_TICKERS: list[str] = US_STOCKS + EU_STOCKS + INDIA_STOCKS  # All 190 US stocks

  def __init__(self):
    self.ticker_df = None
    self.indexes_df = None
    self.macro_df = None

  def _get_growth_df(self, df:pd.DataFrame, prefix:str)->pd.DataFrame:
    '''Help function to produce a df with growth columns'''
    for i in [1,3,7,30,90,365]:
      df['growth_'+prefix+'_'+str(i)+'d'] = df['Close'] / df['Close'].shift(i)
      GROWTH_KEYS = [k for k in df.keys() if k.startswith('growth')]
    return df[GROWTH_KEYS]
  
  def _fetch_index_with_fallback(self, yf_symbol, stooq_symbol, name, min_date, fred_symbol=None):
    '''Fetch index data with yfinance first, Stooq second, FRED third fallback for REAL data'''
    data = None
    
    # First try: yfinance
    try:
      ticker_obj = yf.Ticker(yf_symbol)
      data = ticker_obj.history(start=min_date, interval="1d")
      
      if not data.empty:
        print(f"yfinance SUCCESS: Got {len(data)} rows for {name}")
        data.index = pd.to_datetime(data.index)
      else:
        print(f"yfinance returned no data for {name}")
        
    except Exception as e:
      print(f"yfinance error for {name}: {e}")
    
    # Second fallback: If yfinance failed or returned no data, try Stooq for REAL data
    if data is None or data.empty:
      try:
        print(f"Trying Stooq fallback for {name}...")
        data = pdr.get_data_stooq(stooq_symbol, start=min_date)
        
        # Stooq returns data in reverse chronological order, so reverse it
        data = data.sort_index()
        data.index = pd.to_datetime(data.index)
        
        if not data.empty:
          print(f"Stooq SUCCESS: Got {len(data)} rows of REAL data for {name}")
        else:
          print(f"Stooq also returned no data for {name}")
          
      except Exception as e:
        print(f"Stooq fallback error for {name}: {e}")
    
    # Third fallback: If both yfinance and Stooq failed, try FRED for REAL data
    if (data is None or data.empty) and fred_symbol:
      try:
        print(f"Trying FRED fallback for {name}...")
        fred_data = pdr.get_data_fred(fred_symbol, start=min_date)
        
        if not fred_data.empty:
          # Convert FRED data to OHLCV format (FRED only has Close prices)
          data = pd.DataFrame(index=fred_data.index)
          data['Close'] = fred_data.iloc[:, 0]  # FRED data is single column
          data['Open'] = data['Close']  # Use Close as Open for FRED data
          data['High'] = data['Close']  # Use Close as High for FRED data  
          data['Low'] = data['Close']   # Use Close as Low for FRED data
          data['Volume'] = 0            # FRED doesn't have volume data
          data.index = pd.to_datetime(data.index)
          
          print(f"FRED SUCCESS: Got {len(data)} rows of REAL data for {name}")
        else:
          print(f"FRED also returned no data for {name}")
          
      except Exception as e:
        print(f"FRED fallback error for {name}: {e}")
    
    # If still no data, create empty DataFrame with proper structure
    if data is None or data.empty:
      print(f"No data available for {name} from any source, creating empty DataFrame")
      data = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume'])
      data.index = pd.DatetimeIndex([])
    
    # Sleep to avoid overloading APIs
    time.sleep(1)
    return data
    
  def fetch(self, min_date = None):
    '''Fetch all data from APIs'''

    print('Fetching Tickers info from YFinance')
    self.fetch_tickers(min_date=min_date)
    print('Fetching Indexes info from YFinance')
    self.fetch_indexes(min_date=min_date)
    print('Fetching Macro info from FRED (Pandas_datareader)')
    self.fetch_macro(min_date=min_date)
  
  def fetch_tickers(self, min_date=None):
    '''Fetch Tickers data from yfinance API with Stooq fallback for REAL data'''
    if min_date is None:
      # Use a more recent start date to avoid too much historical data
      min_date = "2022-01-01"
    
    # Convert to datetime if it's a string
    if isinstance(min_date, str):
      min_date = pd.to_datetime(min_date)   

    print(f'Going download data for this tickers: {self.ALL_TICKERS}')
    tq = tqdm(self.ALL_TICKERS)
    
    for i,ticker in enumerate(tq):
      tq.set_description(ticker)
      historyPrices = None

      # First try: Use the 2025 colab approach with yfinance
      try:
        ticker_obj = yf.Ticker(ticker)
        historyPrices = ticker_obj.history(start=min_date, interval="1d")
        
        if not historyPrices.empty:
          print(f"yfinance SUCCESS: Got {len(historyPrices)} rows for {ticker}")
        else:
          print(f"yfinance returned no data for {ticker}")
          
      except Exception as e:
        print(f"yfinance error for {ticker}: {e}")
      
      # Fallback: If yfinance failed or returned no data, try Stooq for REAL data
      if historyPrices is None or historyPrices.empty:
        try:
          print(f"Trying Stooq fallback for {ticker}...")
          # For US stocks, we need to add .US suffix for Stooq
          stooq_ticker = f"{ticker}.US"
          historyPrices = pdr.get_data_stooq(stooq_ticker, start=min_date)
          
          # Stooq returns data in reverse chronological order, so reverse it
          historyPrices = historyPrices.sort_index()
          
          if not historyPrices.empty:
            print(f"Stooq SUCCESS: Got {len(historyPrices)} rows of REAL data for {ticker}")
          else:
            print(f"Stooq also returned no data for {ticker}")
            
        except Exception as e:
          print(f"Stooq fallback error for {ticker}: {e}")
      
      # Skip if no data from either source
      if historyPrices is None or historyPrices.empty:
        print(f"No data available for {ticker} from any source, skipping...")
        time.sleep(1)
        continue

      # Ensure index is datetime
      historyPrices.index = pd.to_datetime(historyPrices.index)

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
          historyPrices['growth_'+str(i)+'d'] = historyPrices['Close'] / historyPrices['Close'].shift(i)
      historyPrices['growth_future_30d'] = historyPrices['Close'].shift(-30) / historyPrices['Close']

      # Technical indicators
      # SimpleMovingAverage 10 days and 20 days
      historyPrices['SMA10']= historyPrices['Close'].rolling(10).mean()
      historyPrices['SMA20']= historyPrices['Close'].rolling(20).mean()
      historyPrices['growing_moving_average'] = np.where(historyPrices['SMA10'] > historyPrices['SMA20'], 1, 0)
      historyPrices['high_minus_low_relative'] = (historyPrices['High'] - historyPrices['Low']) / historyPrices['Close']

      # 30d rolling volatility : https://ycharts.com/glossary/terms/rolling_vol_30
      # Calculate daily returns first, then rolling std of returns
      historyPrices['daily_returns'] = historyPrices['Close'].pct_change()
      historyPrices['volatility'] = historyPrices['daily_returns'].rolling(30).std() * np.sqrt(252)

      # what we want to predict (2025 update: changed from 5d to 30d)
      historyPrices['is_positive_growth_30d_future'] = np.where(historyPrices['growth_future_30d'] > 1, 1, 0)

      # sleep 1 sec between downloads - not to overload the API server
      time.sleep(1)

      if self.ticker_df is None:
        self.ticker_df = historyPrices
      else:
        self.ticker_df = pd.concat([self.ticker_df, historyPrices], ignore_index=True)
      
  def fetch_indexes(self, min_date=None):
    '''Fetch Indexes data from yfinance API with Stooq fallback for REAL data'''

    if min_date is None:
      # Use a recent start date for better data availability
      min_date = "2020-01-01"
    
    min_date = pd.to_datetime(min_date)   
    
    # Define index mappings: (yfinance_symbol, stooq_symbol, name)
    index_mappings = [
        ("^GDAXI", "^DAX", "DAX"),
        ("^GSPC", "^SPX", "S&P500"),
        ("^DJI", "^DJI", "Dow Jones"),
        ("EPI", "EPI", "India ETF"),
        ("^VIX", "^VIX", "VIX"),
        ("GC=F", "GC.F", "Gold"),
        ("CL=F", "CL.F", "WTI Oil"),
        ("BZ=F", "BZ.F", "Brent Oil"),
        ("BTC-USD", "BTC.USD", "Bitcoin")
    ]
    
    # Fetch each index with fallback (including FRED symbols for missing data)
    dax_daily = self._fetch_index_with_fallback("^GDAXI", "^DAX", "DAX", min_date)
    snp500_daily = self._fetch_index_with_fallback("^GSPC", "^SPX", "S&P500", min_date)
    dji_daily = self._fetch_index_with_fallback("^DJI", "^DJI", "Dow Jones", min_date)
    epi_etf_daily = self._fetch_index_with_fallback("EPI", "EPI", "India ETF", min_date)
    vix = self._fetch_index_with_fallback("^VIX", "^VIX", "VIX", min_date, fred_symbol="VIXCLS")
    gold = self._fetch_index_with_fallback("GC=F", "GC.F", "Gold", min_date)  # No FRED gold data available
    crude_oil = self._fetch_index_with_fallback("CL=F", "CL.F", "WTI Oil", min_date, fred_symbol="DCOILWTICO")
    brent_oil = self._fetch_index_with_fallback("BZ=F", "BZ.F", "Brent Oil", min_date, fred_symbol="DCOILBRENTEU")
    btc_usd = self._fetch_index_with_fallback("BTC-USD", "BTC.USD", "Bitcoin", min_date, fred_symbol="CBBTCUSD")
    
    # Prepare to merge
    dax_daily_to_merge = self._get_growth_df(dax_daily, 'dax')
    snp500_daily_to_merge = self._get_growth_df(snp500_daily, 'snp500')
    dji_daily_to_merge = self._get_growth_df(dji_daily, 'dji')
    epi_etf_daily_to_merge = self._get_growth_df(epi_etf_daily, 'epi')
    vix_to_merge = vix.rename(columns={'Close':'vix_adj_close'})[['vix_adj_close']]
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

    # Only save if dataframes exist and are not empty
    if self.ticker_df is not None and not self.ticker_df.empty:
      file_name = 'tickers_df.parquet'
      if os.path.exists(os.path.join(data_dir, file_name)):
        os.remove(os.path.join(data_dir, file_name))
      self.ticker_df.to_parquet(os.path.join(data_dir,file_name), compression='brotli')
      print(f"Saved {len(self.ticker_df)} ticker records")
    else:
      print("No ticker data to save")
  
    if self.indexes_df is not None and not self.indexes_df.empty:
      file_name = 'indexes_df.parquet'
      if os.path.exists(os.path.join(data_dir, file_name)):
        os.remove(os.path.join(data_dir, file_name))
      self.indexes_df.to_parquet(os.path.join(data_dir,file_name), compression='brotli')
      print(f"Saved {len(self.indexes_df)} index records")
    else:
      print("No index data to save")
  
    if self.macro_df is not None and not self.macro_df.empty:
      file_name = 'macro_df.parquet'
      if os.path.exists(os.path.join(data_dir, file_name)):
        os.remove(os.path.join(data_dir, file_name))
      self.macro_df.to_parquet(os.path.join(data_dir,file_name), compression='brotli')
      print(f"Saved {len(self.macro_df)} macro records")
    else:
      print("No macro data to save")

  def load(self, data_dir:str):
    """Load files from the local directory"""
    self.ticker_df = pd.read_parquet(os.path.join(data_dir,'tickers_df.parquet'))
    self.macro_df = pd.read_parquet(os.path.join(data_dir,'macro_df.parquet'))
    self.indexes_df = pd.read_parquet(os.path.join(data_dir,'indexes_df.parquet'))
