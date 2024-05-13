## Module 3 Homework

In this homework, we're going to work with categorical variables, first ML models (Decision Trees), and hyperparameter tuning.

Please use the [Colab Module 3](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/03-modeling/Module_3_Colab_Time_Series_Modeling.ipynb) for all tasks to ensure you have the same dataframe used for the Modeling part, as covered during the lecture. 
We suggest copying and extending it (around "TODO" comments). 

---
### Question 1 (1 point): Dummies on Month and Week-of-Month

**Find the CORRELATION VALUE of the most correlated dummy <month-week_of_month> with the binary outcome variable (" is_positive_growth_5d_future")?**

You saw in the correlation analysis and modeling that September and October may be important seasonal months. In this task, we'll go futher and try to generate dummies for Month and Week-of-month (starting from 1). For example, the first week of October should be coded similar to this: 'October_w1'.
Once you've generated the new set of variables, find the most correlated (in absolute value) one with "is_positive_growth_5d_future" and round it to 3 digits after the comma.

Suggested path to a solution:
- [[Source](https://stackoverflow.com/questions/25249033/week-of-a-month-pandas)] Use this formula to get the week of month for the datetime variable d: `(d.day-1)//7+1` 
- Define a new string variable for all month-week_of_month combinations. Append it to the CATEGORICAL features set. You should have 5 variables treated as CATEGORICAL now: 'Month', 'Weekday', 'Ticker', 'ticker_type', 'month_wom'.
- Use [pandas.get_dummies()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.get_dummies.html) to generate dummies.
- Use [pandas.DataFrame.corr()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.corr.html) function (also used in [Code Snippet 1]) to get correlations with "is_positive_growth_5d_future", filter out only variables representing the new dummy set, and sort it by absolute values (you can define a new column "abs_corr" in the dataframe with correlations), and find the highest value (among new dummies set).

**NOTE**: these new dummies will be used as features in the next tasks, please leave it in the dataset.

---
### Question 2 (2 points): Define new "hand" rules on macro and technical indicators variables

**What is the precision score for the best of the NEW variables (pred3 or pred4)**

Let's utilize the knowledge from the visualised tree (clf10) (Code Snippet 5: 1.4.4 Visualisation).
You're asked to define two new 'hand' rules (leading to 'positive' subtrees): 
- pred3_manual_gdp_fastd: (gdppot_us_yoy <= 0.027) & (fastd >= 0.251)
- pred4_manual_gpd_wti_oil: (gdppot_us_yoy >= 0.027) & (growth_wti_oil_30d <= 1.005)

Define these two new variables and add them to the dataframe.
What is the precision score for them? Write down the best of two (round to the three decimal places
). E.g. if you have 0.5789, your answer should be 0.579.

(Additional: Are these two new 'hand' rules better than previously defined ones? If yes, then why do you think so?)

---
### Question 3 (1 point): Join predictions to the original dataframe

**What is the total number of records in the TEST dataset when the new prediction pred5_clf_10 is better than all 'hand' rules (pred0..pred4)?**

Here is the task:
* [Complete the code in 1.4.5] You need to integrate the predictions from the 10-level deep tree into the dataframe "new_df" and name it pred5_clf_10. You can recalculate the predictions for all train, validation, and test records, or have only test dataset records filled (and other predictions as NaN).
* Once you have it, find all records from the TEST dataset when pred5_clf_10 is the only correct prediction for the true growth (is_positive_growth_5d_future==1): i.e., all pred0, ..., pred4 should be equal to 0, pred5_clf_10 and is_positive_growth_5d_future equal to 1. 
* Write down the number of records (INTEGER) from the TEST dataset when pred5_clf_10 is better than all manual (pred0..pred4)

---
### Question 4: (2 points) Hyperparameter tuning for a Decision Tree

**What is the optimal tree depth (from 1 to 20) for a DecisionTreeClassifier?**

Modify the section 1.4 [Code Snippet 4]
* Re-define the train set X_train (using the condition split=='train'), create a validation set X_valid (using the condition split=='validation'), and leave the test set X_test unchanged.
* Apply the same data transformation rules (replace +-inf with NaN and then replace all NaNs with 0).
* Iterate in a loop for max_depth between 1 and 20: 
  * Train the DecisionTreeClassifier (clf) with max_depth=k on a train set.
  * Find the precision and accuracy scores on the validation set.
* Select the **best_max_depth** based on precision only and write it down as an answer.
* Define a new feature pred6_best_clf and join with the dataframe (using the method from Q3)

(Advanced: Read about [scikit-learn Decision Trees](https://scikit-learn.org/stable/modules/tree.html). Do you see the 'saturation' of precision/accuracy when max_depth is increasing, or there is a tendency of overfitting?)

---
### [EXPLORATORY] Question 5: What data is missing? 

Now that you have some insights from the correlation analysis and the Decision Trees regarding the most influential variables, suggest new indicators you would like to include in the dataset and explain why.

You can also propose something entirely different based on your intuition, but it should be relevant to the shared dataset of the largest Indian, EU, and US stocks. If you choose this approach, please specify the data source as well.

---
## Submitting the solutions

[NOT READY YET] Form for submitting: https://courses.datatalks.club/sma-zoomcamp-2024/homework/hw03

---
## Leaderboard

Leaderboard link: https://courses.datatalks.club/sma-zoomcamp-2024/leaderboard

---