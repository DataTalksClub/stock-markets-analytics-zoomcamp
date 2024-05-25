## Module 3 Homework

In this homework, we're going to work with categorical variables, first ML models (Decision Trees), and hyperparameter tuning.

Please use the [Colab Module 3](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/03-modeling/Module_3_Colab_Time_Series_Modeling.ipynb) for all tasks to ensure you have the same dataframe used for the Modeling part, as covered during the lecture. 
We suggest copying and extending it (around "TODO" comments).

**HINT**: If you want to avoid data truncation in GitHub's UI, try either of the following options:
* Open the notebook in [Colab, using the GitHub link to the notebook](https://colab.research.google.com/github/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/03-modeling/Module_3_Colab_Time_Series_Modeling.ipynb).
* Clone the repository to a local folder and open the notebook in Jupyter Notebook.
---
### Question 1 (1 point): Dummies on Month and Week-of-Month

**Find the ABSOLUTE CORRELATION VALUE of the most correlated dummy <month-week_of_month> with the binary outcome variable `is_positive_growth_5d_future`?**

You saw in the correlation analysis and modeling that September and October may be important seasonal months. In this task, we'll go futher and try to generate dummies for Month and Week-of-month (starting from 1). For example, the first week of October should be coded similar to this: 'October_w1'.
Once you've generated the new set of variables, find the most correlated (in absolute value) one with `is_positive_growth_5d_future` and round it to 3 digits after the comma.

Suggested path to a solution:
- [[Source](https://stackoverflow.com/questions/25249033/week-of-a-month-pandas)] Use this formula to get the week of month for the datetime variable d: `(d.day-1)//7+1` 
- Define a new string variable for all month-week_of_month combinations. Append it to the CATEGORICAL features set. You should have 5 variables treated as CATEGORICAL now: 'Month', 'Weekday', 'Ticker', 'ticker_type', 'month_wom'. In the end, you should get 115 dummy features, including 60 (=12*5) week_month_of_week dummies.
- Use [pandas.get_dummies()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.get_dummies.html) to generate dummies.
- Use [pandas.DataFrame.corr()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.corr.html) function (also used in [Code Snippet 1]) to get correlations with `is_positive_growth_5d_future`, filter out only variables representing the new dummy set, and sort it by absolute values (you can define a new column "abs_corr" in the dataframe with correlations), and find the highest value (among the new dummies features set).

**NOTE**: new dummies will be used as features in the next tasks, please leave them in the dataset.

---
### Question 2 (2 points): Define new "hand" rules on macro and technical indicators variables

**What is the precision score for the best of the NEW predictions (pred3 or pred4), rounded to 3 digits after the comma?**

Let's utilize the knowledge from the visualised tree (clf10) (Code Snippet 5: 1.4.4 Visualisation):

* You're asked to define two new 'hand' rules (leading to 'positive' subtrees): 
  - `pred3_manual_gdp_fastd`: (gdppot_us_yoy <= 0.027) & (fastd >= 0.251)
  - `pred4_manual_gdp_wti_oil`: (gdppot_us_yoy >= 0.027) & (growth_wti_oil_30d <= 1.005)

* Extend the Code Snippet 3 (Manual "hand rule" predictions): Calculate and add new rules (pred3 and pred4) to the dataframe.You should notice that one of the predictions doesn't have any positive predictions on TEST dataset (while it has many on TRAIN+VALIDATION). 

* Debug: check in the `new_df` and the original dataset/data generation process that we didn't make any mistakes during the data transformation step.

* Explain why this can happen even if there are no errors in the data features.

* As a result, write down the precision score for the remaining predictor (round to three decimal points). E.g. if you have 0.57897, your answer should be 0.579.

---
### Question 3 (1 point): Unique correct predictions from a 10-levels deep Decision Tree Classifier (pred5_clf_10) 

**What is the total number of records in the TEST dataset when the new prediction pred5_clf_10 is better than all 'hand' rules (pred0..pred4)?**

NOTE: please include `random_state=42` to Decision Tree Classifier init function (line `clf = DecisionTreeClassifier(max_depth=max_depth, random_state=42)`) to ensure everyone gets the same results.

Suggested solution:
* Step1: Rewrite the '1.4.3 Inference for a decision tree' piece for the Decision Tree Classifier with max_depth=10 (clf_10), so that you fit the model on TRAIN+VALIDATION sets (unchanged from the lecture), but predict on the whole set X_all (to be able to define a new column 'pred5_clf_10' in the dataframe new_df). Here is the [link](https://stackoverflow.com/questions/40729162/merging-results-from-model-predict-with-original-pandas-dataframe) with explanation. It will solve the problem in 1.4.5 when predictions were made only for Test dataset and couldn't be easily joined with the full dataset. 

* Step2: Once you have it, define a new column 'only_pred5_is_correct' similar to 'hand' prediction rules with several conditions: is_positive_growth_5d_future AND is_correct_pred5 should be equal 1, while all other predictions is_correct_pred0..is_correct_pred4 should be equal to 0.

* Step3: Convert 'only_pred5_is_correct' column from bool to int, and find how many times it is equal to 1 in the TEST set. Write down this as an answer.

ADVANCED: define a function that can be applied to the whole row of predictions ([a few examples of pandas-apply-row-functions](https://sparkbyexamples.com/pandas/pandas-apply-function-to-every-row/)) and can find whether some prediction 'predX' (where X is one of the predictions) is uniquely correct. It should work even if there are 100 predictions available, so that you don't define manually the condition for 'predX'.  

---
### Question 4: (2 points) Hyperparameter tuning for a Decision Tree

**What is the optimal tree depth (from 1 to 20) for a DecisionTreeClassifier?**

NOTE: please include `random_state=42` to Decision Tree Classifier init function (line `clf = DecisionTreeClassifier(max_depth=max_depth, random_state=42)`) to ensure consistency in results.

Follow these steps to find the optimal `max_depth`:
* Iterate through `max_depth` values from 1 to 20.
* Train the Decision Tree Classifier with the current `max_depth` parameter on TRAIN+VALIDATION set.
* Optionally, visualize how the 'head' of each fitted tree changes with more advanced (=deep) trees. You can use the [`sklearn.tree.plot_tree()`](https://scikit-learn.org/stable/modules/generated/sklearn.tree.plot_tree.html) function, or the compact way  with the `export_text()` functionality ([Stack Overflow example](https://stackoverflow.com/questions/20156951/how-do-i-find-which-attributes-my-tree-splits-on-when-using-scikit-learn)):
  ```
  from sklearn.tree import export_text
  tree_rules = export_text(model, feature_names=list(X_train), max_depth=3)
  print(tree_rules)
  ```
* Calculate the precision score (you can use the function [sklearn.metrics.precision_score()](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html)) on the TEST dataset for each of the fitted trees. You can also compare it with the precision score on a VALIDATION dataset, which is included to the training phase (to have more data to train on). You should see that the precision score on a VALIDATION set starts to grow with the complexity of a tree (overfit), which isn't seen on the precision score on TEST.
* Identify the optimal `max_depth`, where the  precision score is the highest on the TEST dataset. Record this value as  **best_max_depth** and submit as an answer.
* Make predictions on all records (TRAIN+VALIDATION+TEST) and add the new prediction `pred6_clf_best` to the dataframe `new_df`.

Additionally, compare the precision score of the tuned decision tree with previous predictions. You should observe an improvement (>0.58, or more than 58% precision), indicating that the tuned tree outperforms previous manual "hand" rules and Decision Tree predictions.

ADVANCED: Read more about different aspects of [scikit-learn Decision Trees](https://scikit-learn.org/stable/modules/tree.html). Draw a line of precision/accuracy vs. max_depth and note whether there's a saturation point of precision/accuracy as max_depth increases. In theory, there should be a trade-off between better fitting (=more complex trees) and generalization.

---
### [EXPLORATORY] Question 5: What data is missing? 

Now that you have some insights from the correlation analysis and the Decision Trees regarding the most influential variables, suggest new indicators you would like to include in the dataset and explain why.

You can also propose something entirely different based on your intuition, but it should be relevant to the shared dataset of the largest Indian, EU, and US stocks. If you choose this approach, please specify the data source as well.

---
## Submitting the solutions

Form for submitting: https://courses.datatalks.club/sma-zoomcamp-2024/homework/hw03

---
## Leaderboard

Leaderboard link: https://courses.datatalks.club/sma-zoomcamp-2024/leaderboard

---