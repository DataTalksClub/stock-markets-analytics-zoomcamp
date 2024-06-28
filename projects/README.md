## Course Project

### Objective

The goal of this project is to apply everything we have learned in this course to build an end-to-end machine learning project. The scoring is designed to foster experimentation and extend the knowledge received during the course. There is a minimum project score of 6 points for the points in bold in the Evaluation section. The maximum score is 36 points. To pass, you need to obtain the minimum score and present your individual results in the project.


## Problem statement

For the project, you are required to build an end-to-end algo-trading strategy.

For that, you will need:

* Select data sources (or APIs) to be used for the project.
* Generate a unified combined dataset (one table from all sources).
* Perform necessary data transformations, create new derived features (e.g., dummies), and prepare the dataset for ML.
* Train one or several ML models to predict future returns.
* Define a trading strategy based on predictions and simulate it.
* Automate the solution.

## Deliverables

Suggested set of things to include:
* README.md
* Notebooks (research outcomes in Colab or Jupiter Notebooks),
* .py files with scripts for each step
* data workflow and command list to run it automatically
* pipenv or requirements.txt
* (maybe) Dockerfile
* Other files required for your project

[!IMPORTANT]  Please don’t submit data files to GitHub. Instead, save them to a drive and provide the link, or make them available for full download from APIs.

## Peer reviewing

> [!IMPORTANT]  
> To evaluate the projects, we'll use peer reviewing. This is a great opportunity for you to learn from each other.
> * To get points for your project, you need to evaluate 3 projects of your peers
> * You get 3 extra points for each evaluation

## Evaluation Criteria

1) Problem Description (up to 4 points)
    * [ ] **(1 point) Problem is described in README briefly without much detail.**
    * [ ] (1 point) Problem is described in README with enough context and the end goal, so it is clear what the problem is and how the solution will be used.
    * [ ] (1 point) New problem definition (not just the current setup of a week-long strategy for the largest stocks): e.g., hourly or long-term trading for stocks, different stock exchanges (other countries), crypto, betting, etc.
    * [ ] (1 point) State-of-the-art clear description of each step, findings, and how to reproduce it. It is easy to understand the logic of each step, and important findings/difficulties are outlined.

2) Data Sources (up to 4 points)
    * [ ] **(1 point) Use the data sources and the features from the lectures.**
    * [ ] (1 point) 20+ new features with their description in the data sources section (+10% volume).
    * [ ] (1 point) New datasource is introduced - not YFinance, Fred (e.g., paid data, web scraping, alternative free data provider with unique features, etc.).
    * [ ] (1 point) Large dataset with >1 million of records.

3) Data Transformations + EDA (up to 3 points)
    * [ ] **(1 point) Data is combined into one data frame. Feature sets are defined (TO_PREDICT, NUMERIC, DUMMIES, etc.).**
    * [ ] (1 point) New relevant features are generated from transformations (at least 5. One dummy set is one feature): it can be binned variables from numeric features or manual transformations.
    * [ ] (1 point) Exploratory Data Analysis: describe variables you want to predict, run correlation analysis between features and TO_PREDICT, etc.

4) Modeling (up to 5 points)
    * [ ] **(1 point) One model from the lecture is used (DecisionTree, RandomForest).**
    * [ ] (1 point) More than one model from the lecture is used to generate predictions.
    * [ ] (1 point) Custom decision rules on target higher probability events.
    * [ ] (1 point) Hyperparameters tuning is used to tune models.
    * [ ] (1 point) New models are introduced: XGBoost, Regression, Deep Neural Networks and their variations (RNN, LSTM, GNN).

5) Trading Simulation (up to 8 points)
    * [ ] **(1 point) Vector simulations for at least 1 strategy (and approximate returns on capital).**
    * [ ] (1 point) Two or more strategies are covered (sim1_, sim2_, etc. fields are generated for each prediction).
    * [ ] (1 point) Exact simulations (iter.rows) with reinvestment of capital gains and efficient capital utilization.
    * [ ] (1 point) Profitability discussion vs. benchmark, CAGR, Sharpe ratio, max drawdown, rolling returns, etc.
    * [ ] (1 point) The best strategy has advanced features: risk management (e.g., stop loss), time of entry/sell, increased investment with higher probability, portfolio optimization.
    * [ ] (1 point) New strategy: introduce a new empirical strategy based on the predictions, e.g., long-short strategy, or use no more than 1-3-5 concurrent investments, or combine with market conditions (trade only when volatility is high or current price is close to 52 weeks low), etc.
    * [ ] (1 point) Exceptional profitability: choose a realistic benchmark (e.g., S&P500 index) and show that your best prediction/strategy delivers better performance (CAGR) on average than a benchmark.
    * [ ] (1 point) Deep exploratory analysis: how predictions/precision are different by tickers (or markets, or month of year, or other features, etc.). Debug wrong predictions. Give ideas on the data features/models/strategies improvement based on the insights.
  

6) Automation (up to 5 points)

    * [ ] **(1 point) All notebooks (used in workflow) are exported to scripts. There is one notebook that calls all functions from the .py files and shows how to execute the workflow (end-to-end data workflow: download, transform, predict, simulate, show the latest new trades).**
    * [ ] (1 point) Dependencies are managed (e.g., file with dependencies, pipfile + README explaining how to install dependencies and activate the environment).
    * [ ] (1 point) The full system can be re-run via Cron job and generate predictions for the last available data (e.g., last day data -> predictions for the future days).
    * [ ] (1 point) Two regimes for the system: run from a file on drive (easy to replicate, no data loading+transformations, but no update for the latest data), or download data from the sources.
    * [ ] (1 point) Incremental data loading/transformations with storage on drive/database/elsewhere (not on GitHub).

7) Bonus points (up to 7 points)
    * [ ] (1 point) The code is well designed and commented on in modules.
    * [ ] (1 point) Additional code to place bets through any Brokers API.
    * [ ] (1 point) Additional code for monitoring models, financial results, trades → e.g., a dashboard (describe how to make it live), or Telegram bot to send messages with trades, data updates, etc.
    * [ ] (1 point) Containerization.
    * [ ] (1 point) Cloud deployment.
    * [ ] (1-2 points) Subjective bonus points from a peer reviewer: why do you like the project, what was particularly well done in the project?

## Project Submission
* [2024, Project submission attempt 1]
Please submit your projects here before end of day 2024-07-14 (23:59:59 GMT+1)
https://courses.datatalks.club/sma-zoomcamp-2024/project/project1
* [2024, Project review attempt 1]
Please review 3 peers projects between 2024-07-15 (00:00:00 GMT+1) and 2024-07-21 (23:59:59 GMT+1) https://courses.datatalks.club/sma-zoomcamp-2024/project/project1/eval