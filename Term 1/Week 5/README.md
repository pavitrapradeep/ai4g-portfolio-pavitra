# Term 1 - Week 5: Machine Learning Basics

---

## 1. Homework & workshop assignments -> [`homework/`](homework/)

**What was the assignment?**

**What did I hand in?**
_List the files, or link to them. Notebook exports, screenshots, scripts._

**What did I find difficult, and how did I solve it?**

### Checklist
- [ ] My workshop / homework files are in `homework/`
- [ ] Everything runs without errors, or I explained what does not and why

---


## 2. Hackathon prototype -> [`hackathon/`](hackathon/)

> Your tool and your SDG for this hackathon are announced at the **start of Friday's class**.
> Write them down here once you know them.

**Project title:**

Corporate Bankruptcy Prediction Using Machine Learning


**My pair partner:**

Cameron

**Tool we had to use:**

scikit-learn

**SDG we had to address:**

SDG 8 — Decent Work and Economic Growth.

How is it related to our project?

Our project relates to SDG 8 because company financial distress and bankruptcy can have wider effects on employment, income security and economic security. When a company faces financial difficulties or bankruptcy, employees may face job or income insecurity, while investors, creditors and other businesses can also be affected. Our model uses financial indicators to identify companies that may be classified as bankrupt, helping a financial risk analyst identify companies that may require additional financial review. By supporting earlier identification of financial distress and more informed decision-making, the project can contribute to greater economic stability and security, while the model itself does not directly predict job loss or individual economic outcomes.

**What problem does it solve, and for whom?**

Our project addresses a specific financial-risk challenge: identifying companies that may be at risk of bankruptcy based on their financial indicators, particularly when financial distress may not be immediately obvious from a simple assessment. The project uses 95 financial indicators covering areas such as profitability, liquidity, leverage, cash flow and asset efficiency to classify companies as bankrupt or non-bankrupt. The model is intended to support early identification of potential financial distress, allowing a financial risk analyst to determine which companies require further assessment rather than relying only on a general accuracy-based prediction.

The project is designed for financial risk analysts at commercial banks who assess companies applying for business loans. These analysts already work with company financial information and are responsible for evaluating whether a company presents an acceptable level of financial risk before supporting a lending decision. The model provides them with an additional screening signal: companies predicted as potentially bankrupt can be prioritized for more detailed financial review. The model is therefore decision support, not an automatic loan-approval or rejection system.

The data were collected from the Taiwan Economic Journal for 1999–2009, and company bankruptcy was defined according to the business regulations of the Taiwan Stock Exchange.
https://archive.ics.uci.edu/dataset/572/taiwanese+bankruptcy+prediction

Problem:

Our project addresses the specific problem of identifying potential corporate bankruptcy risk during financial-risk assessment.

- The dataset contains 6,819 companies, including 220 companies classified as bankrupt (3.23%).
- Bankruptcy is therefore a relatively rare outcome, creating a strong class-imbalance problem.
- A model that predicts every company as non-bankrupt could achieve approximately 96.77% accuracy while detecting zero bankrupt companies, showing why identifying the minority bankruptcy class is important.
- Our models therefore prioritize recall for the bankruptcy class, because missing an actually bankrupt company can be more concerning for a risk analyst than incorrectly flagging a financially healthy company for additional review.
- The final model is intended to help analysts prioritize further financial-risk assessment, rather than replace professional judgement.

- 
Who is the user?


Primary user: Financial risk analysts at commercial banks assessing companies for business loans.

They are people who:
- evaluate the financial health and risk of companies;
- review financial indicators when assessing business-loan applications;
- need to identify companies that may require additional financial investigation;
- can use a bankruptcy-risk prediction as an initial screening signal before making or recommending a lending decision;
- are expected to combine the model's prediction with professional financial analysis rather than rely on the model alone.

- 
Who is it NOT for?

The model is not primarily intended for:

- individual employees;
- individual consumers;
- investors making personal investment decisions;
- companies outside the population represented by the dataset without additional validation;
- automated loan-approval systems;
- replacing professional financial-risk analysts.
  
The dataset represents Taiwanese companies, so the model's results should not automatically be assumed to generalize to companies in other countries, industries or economic environments.

**What did you build?**

We built a corporate bankruptcy-risk screening system designed for financial risk analysts at commercial banks who assess companies applying for business loans. The system takes 95 financial indicators for a company, covering areas such as profitability, liquidity, leverage, operating performance, asset efficiency and cash flow, and processes them through three tuned machine-learning classifiers: K-Nearest Neighbours (KNN), Logistic Regression and Random Forest. The models use a reproducible workflow with a stratified train-test split, preprocessing, 5-fold cross-validation and hyperparameter tuning, allowing us to fairly compare their ability to identify the minority bankruptcy class. The recommended Random Forest model returns a bankrupt/non-bankrupt prediction and the probability of each class, giving the analyst an additional risk signal to prioritize companies for deeper financial assessment before a lending decision. By helping identify potential corporate financial distress, the system can also support consideration of economic and income security for employees whose livelihoods depend on financially stable companies. The final lending decision remains with the analyst, making the system a financial-risk decision-support tool rather than an automated decision-maker.

**Link to the live thing (if any):**

Colab: https://colab.research.google.com/drive/1yyt95OR3dY6KDMTkGQRzEKFNa9b-B34D#scrollTo=401VNuI7Feni

The notebook contains the complete working prototype, including dataset loading, preprocessing, 5-fold cross-validation, hyperparameter tuning, model comparison, evaluation, confusion matrix, and a new-company prediction with probability. It can be run from start to finish to reproduce the results.

GitHub repo : https://github.com/pavitrapradeep/ai4g-portfolio-pavitra/tree/main/Term%201/Week%205/hackathon


**How do I run it?**



1. Open the Google Colab notebook using the provided link.
2. Run all cells from **Runtime → Run all**.
3. The notebook automatically clones the GitHub repository and loads the `data.csv` dataset.
4. No manual dataset upload or additional installation is required.
5. The notebook then preprocesses the data, tunes KNN, Logistic Regression, and Random Forest using 5-fold cross-validation, evaluates the models on the test set, performs error analysis, and demonstrates a final prediction.

**Who did what?**

Both of us contributed equally to the overall project, with the work being completed collaboratively rather than divided into completely separate roles. We started by discussing the project requirements, selecting the Taiwanese Bankruptcy Prediction dataset, and deciding how it could be connected to SDG 8 and the specific problem of identifying companies at risk of bankruptcy. We then worked on understanding the dataset, exploring the features and target variable, checking the class imbalance, and preparing the data for modelling.
The coding work was also shared between us. We worked on implementing the preprocessing pipeline, train-test split, baseline model, and the three classification models: KNN, Logistic Regression, and Random Forest. We contributed to selecting suitable hyperparameters, running cross-validation, comparing the models using recall and other evaluation metrics, and interpreting the results. We also worked together on analysing the confusion matrix, false positives and false negatives, identifying the strengths and limitations of the models, and deciding which model should be recommended.

Alongside the technical work, we jointly prepared the project documentation, including the problem definition, dataset description, model comparison, ethical considerations, SDG 8 connection, README, and final explanations. We also reviewed the notebook to make sure the workflow was reproducible and that the final prediction demonstration and outputs were clear. Overall, the project was developed through shared discussion, coding, analysis, tuning, and documentation, with both of us contributing throughout the main stages of the work.


**Ethical reflection - what are the risks of your tool? Who could it harm?**

There are several risks specific to our model and the data we used. Our model predicts whether a company is classified as bankrupt based on its financial information, so an incorrect prediction could affect how a company is treated during a business-loan assessment. The dataset contains 6,819 Taiwanese companies from 1999–2009 and focuses on financial indicators such as profitability, liquidity, leverage and cash flow. It does not contain information about individual employees, age, gender, ethnicity or migrant status, so we could not check whether the model makes different types of mistakes for those groups. The data is also from one country and a specific time period, so the model may not perform in the same way for companies in other countries or under current economic conditions. For our model, a false negative is the more serious error because it means a company that is actually classified as bankrupt is predicted as non-bankrupt and may not receive additional financial review. A false positive means a company that is not bankrupt is flagged as potentially risky, which could lead to unnecessary additional review and use of the analyst’s time. Because missing a bankrupt company is more concerning, we used recall as the main metric when tuning and comparing the models instead of relying on accuracy, which would be misleading because the dataset is highly imbalanced. We also compared the models using 5-fold cross-validation and selected Random Forest because it achieved the highest recall while still giving a reasonable F1 score on the test set. Finally, the model should only be used as a supporting risk signal for a financial analyst and not as an automatic decision to approve or reject a loan. The dataset is available through the UCI Machine Learning Repository under the CC BY 4.0 licence, but its historical and geographical limitations should be considered before using the model in a real-world setting.

### Checklist
- [ ] Prototype code (or export / workflow file) is in `hackathon/`
- [ ] This week's slides are in `hackathon/`
- [ ] The prototype actually runs, and I wrote down how to run it
- [ ] Ethical reflection written above

---

## 3. Presentation -> [`presentation/`](presentation/)

*Only fill this in for the week your group was selected to present. You need at least **one** of these across the whole term.*

- [ ] My group presented in this week
- [ ] Slides are in `presentation/`
- [ ] Proof of the live demo is in `presentation/` (recording, screenshots, or link)

**How did it go? What would I do differently next time?**

---

## 4. Reflection

**What is the most important thing I learned this week?**

The most important thing I learned this week is that building a machine-learning model is not just about getting the highest accuracy. We learned how important it is to choose the right evaluation metric based on the problem. In our dataset, bankruptcy was the minority class, so accuracy could be misleading because a model could predict most companies as non-bankrupt and still get a high accuracy. Using recall helped us focus more on identifying companies that were actually classified as bankrupt. I also learned how different models can perform very differently even when they use the same data, and how cross-validation, hyperparameter tuning and error analysis help us make a more informed choice instead of simply choosing the model with the highest score.

**Where does this connect to "AI for Good"?**

This connects to AI for Good because our model shows how AI can be used to support better financial-risk decisions while also considering the people affected by those decisions. Identifying companies at risk of bankruptcy can help financial analysts notice potential financial problems earlier, which can indirectly support economic stability and the security of employees whose income depends on those companies. At the same time, we learned that AI should not make these decisions automatically because false predictions can negatively affect companies. This is why we use our model as a supporting tool for a financial analyst rather than allowing it to make the final lending decision.
