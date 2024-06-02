## Module 4 Homework


In this homework, you are required to understand how the system works as a whole, adjust the code accordingly, and interpret the results correctly. The task involves modifying a few lines of code, with hints provided in the form of comments labeled "TODO: HQ4 Q..".

Please use the new workbook [Module_04_HA_Workbook](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/04-trading-strategy-and-simulation/Module_04_HA_Workbook.ipynb) for all tasks. This workbook contains a clean version of the code, with hyperparameter tuning commented out and the best models hard-coded. It should take a few minutes to run on Google Colab.

Before solving the problems, ensure you can run the workbook "as is".


**HINT**: If you want to avoid potential data truncation in GitHub's UI, try either of the following options:
* Open the notebook in [Colab, using the GitHub link to the notebook](https://colab.research.google.com/github/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/04-trading-strategy-and-simulation/Module_04_HA_Workbook.ipynb).
* Clone the repository to a local folder and open the notebook in Jupyter Notebook.

---
### Question 1 (2 points): Find the new global best CAGR with Random Forest tuning

**The idea**: You may have noticed that the Random Forest predictions provide close to maximum CAGR results ("1.1291" for pred9_rf_best_rule_55, "1.0923" for pred10_rf_best_rule_60) with less effort (average trades per day).

In this task, you are asked to define new predictors with custom threshold rules from 0.51 to 0.54 and from 0.56 to 0.59 to cover the full interval from 0.51 to 0.60. You should be able to observe one peak of financial performance and understand why we don't need to extend the interval with more predictions on other thresholds.


1) **Before defining new predictors:** modify the code to generate the dataframe `df_scores` for Random Forest classifier `rf_best` and not a Decision Tree (`clf_best`). Look at for precision/recall rates for different threshold values. You'll see that the precision rate goes up with a higher threshold, but recall (and total number of deals) goes down. However, don't be misled by this, as the financial simulation may show a different view (even with higher precision and fewer trades, you may obtain worse results).

2) Define new Random Forest predictions (with names `predxx_rf_best_rule_yy`) based on the missing thresholds to cover the full interval 0.51..0.60

3) Review the last dataframe with the simulation results (`df_sim1_results`).
Find the best simulation results. Do you see that one of the new predictors could deliver the new best CAGR?
Write down the new best CAGR value as an answer.
