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
### Question 2: Best CAGR for Random Forest Decision Rule

**What is the probability threshold for the best Random Forest decision rule?**


#### **The Idea**

The goal is to learn how to construct and interpret the `tpr_dataframe` for another model—**Random Forest**—and connect it with financial performance.

In this task, you'll define new predictors using custom probability thresholds ranging from **0.56 to 0.64**, thereby covering the full interval from **0.55 to 0.65** (two threshold-based predictors are already defined). The objective is to build a dataframe with these decision rules, following the expected pattern:

- **Higher thresholds → Higher precision**
- **Higher thresholds → Fewer total trades**

However, now you're optimizing not just for ML performance (like precision), but also for **financial results (CAGR)** and **time efficiency (average trades per day)**. These relationships aren’t always straightforward, so experimentation is key.



### Steps

1. **Comment out the scaler in preprocessing**

   The `StandardScaler` was originally used for Logistic Regression and never removed. Since Random Forest doesn't need feature scaling, the scaler biases its output.  
   ➤ *Comment it out to allow the Random Forest to perform optimally.*
   ```python
   # scaler = StandardScaler()
   # X_train_valid = scaler.fit_transform(X_train_valid)
   # X_valid = scaler.transform(X_valid)
   # X_test = scaler.transform(X_test)
   ```

2. **Reduce model depth to 14**

   To bring the Random Forest closer to a sub-optimal Decision Tree classifier, reduce its depth from 19 to 14.  
   ➤ *This helps avoid overfitting and encourages generalization.*
   ```python
   rf_best_max_depth = 14
   ```

3. **Construct the `tpr_fpr_dataframe` for the Random Forest classifier**

   - In your code:
     ```python
     # Comment out
     y_pred_test = clf_best.predict_proba(X_test)
     # Uncomment
     y_pred_test = rf_best.predict_proba(X_test)
     ```
   - The Random Forest model provides a smoother prediction probability distribution  
     *(see density plot using `sns.histplot(y_pred_test_class1)`)*.
   - The `df_scores` dataframe will now reflect Random Forest statistics.
   - Watch how **TP + FP (total trades)** decreases with higher thresholds.
   - Examine **precision and recall** at various thresholds:
     - Precision increases with higher thresholds.
     - Recall and total trades decrease.
   - ⚠️ *But beware: higher precision and fewer trades do not always result in better financial returns (CAGR).*

4. **Define new prediction columns for thresholds 0.56 to 0.64**

   Add predictors to cover the full threshold range:
   - Use names like (where xx and yy and parameters):  
     `new[predxx_rf_best_rule_yy] =  (y_pred_all_class1_array >= 0.yy).astype(int)`  

   - Continue after existing ones:  
     `new_df['pred10_rf_best_rule_55'] = (y_pred_all_class1_array >= 0.55).astype(int)`  
     `new_df['pred11_rf_best_rule_65'] = (y_pred_all_class1_array >= 0.65).astype(int)`

5. **Review the simulation results in `df_sim1_results`**

   - Identify the decision rule with:
     - **CAGR ≥ 1.1** (i.e., ~10% annual return)
     - **Avg. daily investments ≈ 5**
   - Extract the threshold value from the predictor name.
   - ✅ *It’s great to see that we can achieve strong returns with 3x less trading effort (e.g., 5 trades/day vs. 14–15).*


---
### Question 3: Predicting Strong Future Growth

**What is the CAGR for the best predictor of strong future growth (after redefining the target variable)?**

Your goal is to adjust how we define “strong future growth” and examine how it affects model performance.

1. Look at the distribution of `growth_future_30d` and `is_positive_growth_30d_future`. You’ll see that the median for  `growth_future_30d` is around 1.02 (2%), and the top 25% starts at about 1.08 (8%). The current version of `is_positive_growth_30d_future` has about 60% of records labeled as class 1 (when defined as 1 when `growth_future_30d`>1)

2. Redefine `is_positive_growth_30d_future` to equal 1, if `growth_future_30d >= 1.08`; otherwise, 0. This definition will be used for all future predictions. With this new version, only about 27% of records will be labeled as class 1..

3. Run the notebook again using this revised target. Threshold-based rules may not perform as well, so check which predictor now delivers the best financial result (CAGR)—it is likely to be  `pred5_clf_10`.

**Write down the CAGR for the best predictor. Were you able to improve it compared to the original best CAGR of 1.1556? Do you see more or fewer trades per day compared to before?**

---
### Question 4:  [EXPLORATORY] Describe Your Ideal Trading Strategy
**Briefly describe your ideal strategy**

So far, we’ve only used one simple rule: “Invest $100 in each positive prediction.” Now it’s your turn to design a better strategy.

Use what you’ve learned and be creative. You can use predictions from one model or combine predictions from several models or different thresholds from the same model.

For example, you might say: *“Take the 3 best predictions with a threshold above 0.7 and invest all my available money equally in them.”*

Think about how you would decide which predictions to use, how much to invest, how to reduce the number of trades, and how to manage risk.

Write a few clear sentences describing your strategy and how you would implement it.

---
## Submitting the solutions

Form for submitting: https://courses.datatalks.club/sma-zoomcamp-2025/homework/hw04

---
## Leaderboard

Leaderboard link: https://courses.datatalks.club/sma-zoomcamp-2025/leaderboard

---