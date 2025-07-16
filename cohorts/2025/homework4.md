## Module 4 Homework (2025 Cohort)

In this homework, you are required to understand how the system works as a whole, adjust the code accordingly, and interpret the results correctly. The task involves modifying a few lines of code and run the whole notebook to check the results.

Please use the new workbook [[2025]_Module_04_Colab_Trading_Simulations.ipynb](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/04-trading-strategy-and-simulation/%5B2025%5D_Module_04_Colab_Trading_Simulations.ipynb) for all tasks. This workbook contains a clean version of the code, with hyperparameter tuning commented out and the best models hard-coded. It should take a few minutes to run on Google Colab. Before solving the problems, make sure you can run the workbook *"as is"*.

**IMPORTANT**: Every time you start a new problem, **make a fresh copy** of the notebook and start from scratch. Do **not** apply edits from previous tasks to the same notebook instance.

**HINT**: To avoid data truncation in GitHub’s UI, try one of the following:
* Open the notebook in [Colab using the GitHub link](https://colab.research.google.com/github/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/04-trading-strategy-and-simulation/%5B2025%5D_Module_04_Colab_Trading_Simulations.ipynb).
* Clone the repository locally and open the notebook in Jupyter Notebook.


---
### Question 1: Less Features is More 

**Find the CAGR for the pred9_clf_second_best_rule_92	using the new setup (with fewer dummy variables).**


**The idea**: Reducing the number of features can help models perform better. As seen in the lecture, some models (e.g., Logistic Regression, Deep Neural Networks) may underperform due to too many features—especially the numerous dummy variables from exercises and individual stock tickers.

1) **Redefine the "CATEGORICAL" set.** 
Remove `ticker` and `month_wom` from the `CATEGORICAL` list *just* before you generate dummies ising the `pd.get_dummies()` function. To check yourself: `df_with_dummies[NUMERICAL+DUMMIES].info()` in the original setup should give 301 features. In the new setup, `df_with_dummies[NUMERICAL+DUMMIES].info()` should show 208 features (about 31% fewer).

2) **Run the entire notebook.** 
At the end of the notebook (after the bubble chart), check the CAGR for `pred9_clf_second_best_rule_92` (the best predictor so far). Expected result: The new CAGR should be *slightly higher* than the original one, which was 1.155577.
 
---
### Question 2:  Best CAGR for Random Forest tuning

**tbd question**

tbd

---
### Question 3: Predicting Strong Future Growth
**tbd question**

tbd

---
### Question 4:  [EXPLORATORY] Describe Your Ideal Strategy
**tbd question**

tbd

---
## Submitting the solutions

Form for submitting: https://courses.datatalks.club/sma-zoomcamp-2025/homework/hw04

---
## Leaderboard

Leaderboard link: https://courses.datatalks.club/sma-zoomcamp-2025/leaderboard

---