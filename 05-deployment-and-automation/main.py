from scripts.data_repo import DataRepository
from scripts.transform import TransformData
from scripts.train import TrainModel

import pandas as pd
import warnings
import os

from datetime import datetime  # Import the datetime module

# 2025 Update: Rewritten automation to use 2025 colab data
# - Updated to 190 US stocks (removed EU and India stocks)
# - Changed from 5-day to 30-day future growth predictions
# - Updated API calls to use ticker object method for better reliability
# - Enhanced data processing and error handling

def main():

  # SLOWER workflow settings: full update (the latest data, retrain the model, make inference (few mins)
  FETCH_REPO = True
  TRANSFORM_DATA = True
  TRAIN_MODEL = True
  

  # FAST workflow settings (everything comes local_repo/ directory)
  # FETCH_REPO = False  # Use existing local data due to yfinance rate limits
  # TRANSFORM_DATA = False
  # TRAIN_MODEL = False

  # =========================================
  # Step1: Get data
  # =========================================
  print('Step 1: Getting data from APIs or Load from disk')
  repo = DataRepository()

  # Check if we have local data files
  data_dir = 'local_data/'
  ticker_file = os.path.join(data_dir, 'tickers_df.parquet')
  
  if FETCH_REPO:
    try:
      # Fetch All 3 datasets for all dates from APIs
      print("Attempting to fetch fresh data from APIs...")
      repo.fetch()
      # save data to a local dir
      repo.persist(data_dir=data_dir)
      print("Successfully fetched and saved fresh data!")
    except Exception as e:
      print(f"Failed to fetch fresh data: {e}")
      if os.path.exists(ticker_file):
        print("Falling back to existing local data...")
        repo.load(data_dir=data_dir)
      else:
        print("No local data available. Cannot proceed without data.")
        print("Please try again later when API rate limits are reset.")
        return
  else:
    # OR Load from disk
    if os.path.exists(ticker_file):
      print("Loading existing data from local files...")
      repo.load(data_dir=data_dir)
    else:
      print("No local data found and FETCH_REPO is False.")
      print("Please set FETCH_REPO=True to download data or ensure local data exists.")
      return

  # =========================================
  # Step2: Transform data into one dataframe
  # =========================================
  print('Step 2: Making data transformations (combining into one dataset)')

  transformed =  TransformData(repo = repo)

  if TRANSFORM_DATA:
    transformed.transform()
    transformed.persist(data_dir='local_data/')
  else:
    transformed.load(data_dir='local_data/')

  # =========================================
  # Step3: Train/ Load Model
  # =========================================
  print('Step 3: Training the model or loading from disk')

  # Suppress all warnings (not recommended in production unless necessary)
  warnings.filterwarnings("ignore")

  trained = TrainModel(transformed=transformed)

  if TRAIN_MODEL:
    trained.prepare_dataframe() # prepare dataframes
    trained.train_random_forest() # train the model
    trained.persist(data_dir='local_data/') # save the model to disk
  else:
    trained.prepare_dataframe() # prepare dataframes (incl. for inference)
    trained.load(data_dir='local_data/')

  # =========================================
  # Step4: Make Inference
  # =========================================
  print('Step 4: Making inference')

  prediction_name='pred_rf_30d_best'
  trained.make_inference(pred_name=prediction_name)
  COLUMNS = ['Close','Ticker','Date',prediction_name, prediction_name+'_rank']
  
  print('Results of the 30-day prediction estimation (last 10 days):')
  # Set display options to prevent truncation
  pd.set_option('display.max_rows', None)
  pd.set_option('display.max_columns', None)
  pd.set_option('display.max_colwidth', None)
  
  print('Top 3 predictions every day (30-day future growth):')
  print(trained.df_full[trained.df_full[f'{prediction_name}_rank']<=3].sort_values(by=["Date",f'{prediction_name}_rank']).tail(10)[COLUMNS])


  print('Bottom 3 predictions every day (30-day future growth):')
  max_date = trained.df_full.Date.max()
  count_predictions = trained.df_full[trained.df_full.Date==max_date].Ticker.nunique()
  print(trained.df_full[trained.df_full[f'{prediction_name}_rank']>=count_predictions-2].sort_values(by=["Date",f'{prediction_name}_rank']).tail(10)[COLUMNS])


  current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")
  print(f"Current date and time: {current_datetime}")

if __name__ == "__main__":
  main()
