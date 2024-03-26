# Stock Market Analytics Zoomcamp

<p align="center">
  <a href="https://docs.google.com/forms/d/e/1FAIpQLSc5H6Jc-HJg9B7irveRASJCAS4BTnJcvM2QX2ykIGZ0UNgCPQ/viewform"><img src="https://user-images.githubusercontent.com/875246/185755203-17945fd1-6b64-46f2-8377-1011dcb1a444.png" height="50" /></a>
</p>


<b>TODO List before the course starts: </b>
- Subscribe to [PythonInvest](https://pythoninvest.com/) to receive analytics and future courses announcements. 
- Register in [DataTalks.Club's Slack](https://datatalks.club/slack.html)
- Join the [`#course-stocks-analytics-zoomcamp`](https://datatalks-club.slack.com/archives/C06L1RTF10F) channel
- Join the [course Telegram channel with announcements](https://t.me/stockanalyticszoomcamp)
- The videos are published on [PythonInvest's YouTube channel](https://www.youtube.com/@pythoninvest2480) 
- [Frequently asked technical questions](https://docs.google.com/document/d/1ABQD6ns4vZHKu2dHGqqJ85LCOF7LzxqfvWBVXb_-M9E/edit?usp=sharing)



<b>(Short) Syllabus (published on [PythonInvest's website](https://pythoninvest.com/course)) </b>

* [Module 1: Introduction and Data Sources](#Module-1-Introduction-and-Data-Sources)
* [Module 2: Working with the Data (in Pandas)](#Module-2-Working-with-the-Data-(in-Pandas))
* [Module 3: Analytical Modeling](#Module-3-Analytical-Modeling)
* [Module 4: Trading Strategy and Simulation](#Module-4-Trading-Strategy-and-Simulation)
* [Module 5: Deployment and Automation](#Module-5-Deployment-and-Automation)
* [Project](#project)


## Taking the course

### 2024 Cohort

* **Start**: 15 April 2024 (Monday) at 17:00 GMT
* **Registration link**: https://docs.google.com/forms/d/e/1FAIpQLSc5H6Jc-HJg9B7irveRASJCAS4BTnJcvM2QX2ykIGZ0UNgCPQ/viewform
* [Cohort folder](cohorts/2024/) with homeworks and deadlines
* Launch stream with course overview: to be added after March 25th


### Self-paced mode

All the materials of the course are freely available, so that you
can take the course at your own pace

* Follow the suggested syllabus (see below) week by week
* You don't need to fill in the registration form. Just start watching the videos and join Slack
* Check [FAQ](https://docs.google.com/document/d/1ABQD6ns4vZHKu2dHGqqJ85LCOF7LzxqfvWBVXb_-M9E/edit?usp=sharing) if you have problems
* If you can't find a solution to your problem in FAQ, ask for help in Slack


## (Detailed) Syllabus

### [Module 1: Introduction and Data Sources](01-data-sources/)

* Understanding Data-Driven Decisions and Initiating Data Extraction
  * Explore the philosophy behind making decisions based on data.
  * Delve into the landscape of potential personal investments.
  * Address questions about where to focus attention and considerations of risk and reward.
* Practical Setup: Colab and Initial Data Download
  * Guide you through setting up Colab for practical data analysis.
  * Download your initial financial data using Finance APIs.
* Essential Principles for API Selection
  * Considerations for selecting the right API for your data needs.
  * When it becomes necessary to consider payment options in the API selection process.
* Homework

[More details](01-data-sources/)


### [Module 2: Working with the Data (in Pandas)](02-dataframe-analysis/)

* The Core Libraries for Data Analysis in Python
  * Explore the core libraries: Numpy, Pandas, and Matplotlib (including Seaborn and Plotly Express).
* Understanding Data Types and Manipulation
  * Delve into various data types: numeric, string, and date categories.
  * Master the art of generating dummy variables for comprehensive analysis.
* Enhancing Datasets with Feature Generation Techniques
  * Derive additional features such as hour/day of the week, growth over different periods.
  * Incorporate technical indicators using the TaLib library.
  * Understand predictive elements, including future growth over a week, a month, or a year.
* Effective Data Cleaning Strategies
  * Learn strategies for cleaning and preparing data for analysis.
  * Acquire skills in joining multiple datasets for a holistic view.
* Thorough Descriptive Analysis
  * Conduct a comprehensive descriptive analysis of the dataset.
  * Explore correlations within the data to uncover meaningful insights.
* Homework

[More details](02-dataframe-analysis/)

### [Module 3: Analytical Modeling](03-modeling/)

* Framing Hypotheses and Unraveling Time-Series Predictions
* Heuristics and hand rules for practical predictions.
* Predicting time-series data: trends, seasonality, and remainder decomposition.
* Regression techniques for understanding data relationships.
* Binary classification to determine growth direction.
* [Optional] Example of neural networks in analytical modelling.
* Homework

[More details](03-modeling/)


### [Module 4: Trading Strategy and Simulation](04-trading-strategy-and-simulation/)

Moving Beyond Prediction into the realm of Trading Strategy and Simulation:

* [Optional] Explore screenshots of trading apps, guiding you on how to start—from downloading an app to placing a trade.
* Uncover key features of trading strategies, including considerations like trading fees, risk management, combining predictions, and timing of market entry.
* Delve into various strategy examples:
  * Single stock investment for a long-term approach.
  * Diversified portfolio optimisation for long investments in multiple stocks.
  * Market-neutral strategies, involving both long and short positions based on predictions.
  * Mean reversion strategy, driven by events.
  * Vertical stocks covering and pairs trading.
  * Exploration of "Penny" stocks and dividend strategies.
  * [Maybe - Advanced] Basic options strategy.
* Simulate the financial results based on predictions and the chosen strategy.
* Homework

[More details](04-trading-strategy-and-simulation/)


### [Module 5: Deployment and Automation](05-deployment-and-automation/)
Streamlining Processes from Prediction to Action:

* Transition from Colab notebooks to Python files for improved deployment and execution.
* Establish persistent storage mechanisms, including files and potentially a simple SQLite database with an introduction to SQL.
* Explore automation techniques such as scheduling cron jobs for a series of .py files and consider data workflow solutions like Apache Airflow.
* Learn to generate predictions and execute trades systematically.
* [Maybe - Advanced] Implement automated email notifications containing predictions, trade details, and updates on profit/loss for the designated period.
* Homework

[More details](05-deployment-and-automation/)


### [Project](project)

Putting everything we learned to practice

* Week 1 and 2: working on your project
* Week 3: reviewing your peers

More details: will be shared in the coming weeks


## Asking for help in Slack

The best way to get support is to use [DataTalks.Club's Slack](https://datatalks.club/slack.html). Join the [`#course-stocks-analytics-zoomcamp`](https://datatalks-club.slack.com/archives/C06L1RTF10F) channel.

To make discussions in Slack more organized:

* Follow [these recommendations](asking-questions.md) when asking for help
* Read the [DataTalks.Club community guidelines](https://datatalks.club/slack/guidelines.html)

