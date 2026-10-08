Dataset Card — Taiwanese Bankruptcy Prediction

Dataset overview

Dataset name: Taiwanese Bankruptcy Prediction

Source: UCI Machine Learning Repository
UCI dataset: Taiwanese Bankruptcy Prediction
DOI: 10.24432/C5004D
link: https://archive.ics.uci.edu/dataset/572/taiwanese+bankruptcy+prediction

The dataset is a real-world corporate-finance dataset used for binary classification. It contains financial indicators for Taiwanese companies and a target variable indicating whether a company was classified as bankrupt.

Source: UCI Machine Learning Repository — Taiwanese Bankruptcy Prediction

Who collected the data?

The data were collected from the Taiwan Economic Journal (TEJ). The dataset covers the years 1999–2009. Company bankruptcy was defined according to the business regulations of the Taiwan Stock Exchange.

The dataset was donated to the UCI Machine Learning Repository on 27 June 2020.

Population

The dataset represents companies in Taiwan during the 1999–2009 period. Each observation represents a company and contains financial information used to classify its bankruptcy status.

The dataset therefore represents a specific historical population and should not automatically be assumed to represent companies worldwide, companies in other countries, or companies in different economic periods.

Dataset size

Rows / instances: 6,819 companies

Predictor features: 95

Target variable: Bankrupt?

Total columns: 96

Missing values: None according to the UCI documentation

Classification type: Binary classification

Target variable

The target column is:

Bankrupt?

0 = Non-bankrupt

1 = Bankrupt

The dataset contains:

6,599 non-bankrupt companies (96.77%)

220 bankrupt companies (3.23%)

This creates a substantial class-imbalance problem, because bankrupt companies represent only a small proportion of the observations.

Because of this imbalance, accuracy alone is not an appropriate measure of model performance. In our project, recall for the bankruptcy class was selected as the primary cross-validation metric because failing to identify an actually bankrupt company is an important error for the intended financial-risk screening use case.

Features

The dataset contains 95 financial indicators covering areas including:

Profitability

Liquidity

Leverage and solvency

Operating performance

Asset efficiency

Working capital

Cash flow

Revenue and income growth

Financial ratios

Examples include:

Return on Assets (ROA)

Current Ratio

Acid Test

Liability-to-Equity Ratio

Working Capital to Total Assets

Interest Coverage Ratio

Net Income to Total Assets

Total Asset Turnover

Cash Flow to Total Assets

Return on Total Asset Growth

The UCI documentation provides the full list and descriptions of the 95 features.

Licence

The UCI Machine Learning Repository lists this dataset under the Creative Commons Attribution 4.0 International (CC BY 4.0) licence.

The licence permits sharing and adaptation provided that appropriate credit is given.

Dataset citation:

Taiwanese Bankruptcy Prediction [Dataset]. (2020). UCI Machine Learning Repository. https://doi.org/10.24432/C5004D

Known limitations

1. Population limitation

The dataset represents Taiwanese companies, so the model should not automatically be applied to companies in other countries or economic environments.

2. Time-period limitation

The financial data cover 1999–2009. Economic conditions, regulations, financial markets and business practices can change over time, so model performance may differ on more recent companies.

3. Class imbalance

Only 3.23% of observations are bankrupt, meaning that a model can achieve high overall accuracy while still failing to identify many bankrupt companies. This is why our evaluation emphasizes bankruptcy recall, precision and F1 rather than accuracy alone.

4. Limited scope of financial information

The model uses the financial indicators available in the dataset. Other factors that could influence bankruptcy risk—such as management decisions, market conditions, industry changes, macroeconomic conditions or qualitative business information—are not necessarily represented.

5. Intended use

The model should be used as a financial-risk screening and decision-support tool, not as an automatic loan-approval/rejection system or a definitive statement that a company will become bankrupt. A qualified financial risk analyst should consider the prediction alongside additional financial and contextual information.

Why we selected this dataset

This dataset meets the requirements of the AI for Good — Hackathon 5 assignment because it is:

Real and documented: collected from the Taiwan Economic Journal and documented by UCI.

A classification problem: the target is the binary Bankrupt? variable.

Large enough: 6,819 rows and 95 usable predictor features.

Not a prohibited dataset: it is not a built-in scikit-learn dataset.

Relevant to SDG 8: 
corporate financial distress can have consequences for employment, income and economic security.

The dataset provides a suitable basis for comparing KNN, Logistic Regression and Random Forest as required by the project.

Data file

The project uses the original data.csv file associated with the UCI dataset. 
The UCI documentation lists the CSV file as approximately 10.9 MB, which is below the assignment's 25 MB threshold.

Source and citation

UCI Machine Learning Repository:
Taiwanese Bankruptcy Prediction

DOI: 10.24432/C5004D

Original data source: Taiwan Economic Journal (TEJ), 1999–2009.

Licence: Creative Commons Attribution 4.0 International (CC BY 4.0).

https://archive.ics.uci.edu/dataset/572/taiwanese+bankruptcy+prediction
