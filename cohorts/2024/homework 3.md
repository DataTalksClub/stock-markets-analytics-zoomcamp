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

**NOTE**: new dummies will be used as features in the next tasks, please leave them in the dataset.

---
### Question 2 (2 points): Define new "hand" rules on macro and technical indicators variables

**What is the precision score for the best of the NEW variables (pred3 or pred4)**

Let's utilize the knowledge from the visualised tree (clf10) (Code Snippet 5: 1.4.4 Visualisation).
You're asked to define two new 'hand' rules (leading to 'positive' subtrees): 
- pred3_manual_gdp_fastd: (gdppot_us_yoy <= 0.027) & (fastd >= 0.251)
- pred4_manual_gdp_wti_oil: (gdppot_us_yoy >= 0.027) & (growth_wti_oil_30d <= 1.005)

Extend the Code Snippet 3 (Manual "hand rule" predictions): Calculate and add them to the dataframe.
You should notice that one of the predictions doesn't have any positive predictions on TEST dataset. 
Please debug that: check in the 'new_df' and the original dataset/data generation process that we didn't make any mistakes at the data transformations step; explain why this can happen even if there are no mistakes at the data transformation step.

As a result, write down the precision score for the remaining predictor (round to three decimal points). E.g. if you have 0.57897, your answer should be 0.579.

---
### Question 3 (1 point): Unique correct predictions from a 10-levels deep decision tree classifier (pred5_clf_10) 

**What is the total number of records in the TEST dataset when the new prediction pred5_clf_10 is better than all 'hand' rules (pred0..pred4)?**

NOTE: please include `random_state=42` to Decision Tree Classifier init function (line `clf = DecisionTreeClassifier(max_depth=max_depth, random_state=42)`) to ensure everyone gets the same results.

Suggested solution:
* Rewrite the '1.4.3 Inference for a decision tree' piece for the Decision Tree Classifier with max_depth=10 (clf_10), so that you fit the model on TRAIN+VALIDATION sets (unchanged from the lecture), but predict on the whole set X_all (to be able to define a new column 'pred5_clf_10' in the dataframe new_df). Here is the [link](https://stackoverflow.com/questions/40729162/merging-results-from-model-predict-with-original-pandas-dataframe) with explanation. It will solve the problem in 1.4.5 when predictions were made only for Test dataset and couldn't be easily joined with the full dataset. 

* Once you have it, define a new column 'only_pred5_is_correct' similar to 'hand' prediction rules with several conditions: is_positive_growth_5d_future AND is_correct_pred5 should be equal 1, while all other predictions is_correct_pred0..is_correct_pred4 should be equal to 0.

* Convert 'only_pred5_is_correct' column from bool to int, and find how many times it is equal to 1 in the TEST set. Write down this as an answer.

ADVANCED: define a function that can be applied to the whole row ([examples](https://sparkbyexamples.com/pandas/pandas-apply-function-to-every-row/)) and can find whether some prediction 'predX' (where X is one of the predictions) is uniquely correct. It should work even if there are 100 predictions available, so that you don't define manually the condition.  

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