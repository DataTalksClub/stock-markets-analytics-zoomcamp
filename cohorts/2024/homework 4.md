## Module 4 Homework


In this homework, you are required to understand how the system works as a whole, adjust the code accordingly, and interpret the results correctly. The task involves modifying a few lines of code, with hints provided in the form of comments labeled "TODO: HQ4 Q..".

Please use the new workbook [Module_04_HA_Workbook](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/04-trading-strategy-and-simulation/Module_04_HA_Workbook.ipynb) for all tasks. This workbook contains a clean version of the code, with hyperparameter tuning commented out and the best models hard-coded. It should take a few minutes to run on Google Colab. Before solving the problems, ensure you can run the workbook "as is".

**IMPORTANT**: Copy the workbook every time you start solving a new problem and start from scratch. Do not apply previous tasks edits to the Colab. 

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

---

### Question 2 (2 points): Less Features is More

**The idea**: Reduce the features list to help models perform better. You may have noticed in the lecture that some of the models (Logistic Regression, Deep Neural Network) are not trained well, likely due to too many features in the dataset. We know there were too many dummies (including ones from the exercise and individual stock dummies). In this task, you are asked to remove most of the dummies from the feature set.

1) **Define "DUMMIES_SHORT" set.** This set should include all dummies from the extended set (DUMMIES) but exclude all dummies starting from 'month_' (month_week_of_month dummies) and from 'Ticker' (individual ticker dummies). Make sure you leave dummies starting from 'Month_' (capital 'M'). To check yourself: `df_with_dummies[NUMERICAL+DUMMIES].info()` should give 299 features, while the new one `df_with_dummies[NUMERICAL+DUMMIES_SHORT].info()` should give only 206 features (32% less!).

2) **Define the correct features_list.** Use DUMMIES_SHORT when you generate train, validation, and test dataframes and true values.

3) **Run the workbook till the end.** Check the CAGR for pred5_clf_10 and write it down as an answer. It should be slightly higher than the original workbook CAGR for pred5_clf_10 (1.1308).
 
(Advanced): You should see that simulations on many model-based predictions (names `.._rf_best_..`, `.._clf_best_..`) deliver worse results, likely because the feature set is very different now and you need to re-run the hyperparameters tuning again for Decision Tree and Random Forest classifiers. You may even see that Logistic Regression and Neural Network start to train. You can find the new best models rf_best and clf_best, and apply the decision rules strategies to improve the results even more.

---

### Question 3 (2 points): Predicting Strong Future Growth


**The idea**: There are many "neutral" growth days (with very small positive or negative growth), which may be extremely hard to predict. Let's aim to predict strong positive growth and potentially remove some headache for the models.

1) **Define a new column for the strong growth.** Define a new field `is_strong_positive_growth_5d_future` in the original dataset `df_full`. It should equal to 1 only if the future growth is higher than 2% (`growth_future_5d` is higher than 1.02)

2) **Generate correct true value datasets.** Change the value of a variable `to_predict` to the new feature  `is_strong_positive_growth_5d_future`. Ensure that all vectors with true values (y_train, y_valid, y_test, y_all, y_train_valid) are based on the new feature to predict. 

3) **Run the workbook till the end.** Find the best CAGR for the model-based predictions.
You should see that the best performing simulation (for model-based predictions) should be for the prediction `pred6_clf_best`, although it should be lower than the one in the Workbook (1.1311).

Write down the new CAGR as a result. 

(Advanced): You should see that the trick with predicting strong growth didn't work, as it didn't improve the CAGR. What are the potential reasons for this? Are we missing some steps?


---

### Question 4 (1 point): [EXPLORATORY] Describe Your Ideal Strategy

We've seen many strategies to produce predictions and have made significant improvements, but we've only explored one trading strategy: 'Invest $100 in each positive prediction'. Think about your best strategy for trading on these predictions and describe it.

Consider how you would combine the predictions, better utilize your capital, achieve efficiency (fewer trades), and possibly make other optimizations (e.g., stop loss, timing of entry/selling, portfolio optimization, short trades for market-neutral strategies). Please write down the specific details of what you would use and how you would implement your strategy.

---

## Submitting the solutions

Form for submitting: https://courses.datatalks.club/sma-zoomcamp-2024/homework/hw04

---
## Leaderboard

Leaderboard link: https://courses.datatalks.club/sma-zoomcamp-2024/leaderboard

---