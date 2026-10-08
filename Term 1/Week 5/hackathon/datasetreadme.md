# Dataset Card — Taiwanese Bankruptcy Prediction

## 1. Dataset Overview

- **Dataset name:** Taiwanese Bankruptcy Prediction
- **Source:** UCI Machine Learning Repository
- **UCI dataset:** Taiwanese Bankruptcy Prediction
- **DOI:** 10.24432/C5004D
- **Dataset link:** https://archive.ics.uci.edu/dataset/572/taiwanese+bankruptcy+prediction
- **Classification type:** Binary classification
- **Total observations:** 6,819 companies
- **Predictor features:** 95
- **Target variable:** `Bankrupt?`
- **Total columns:** 96
- **Missing values:** None according to the UCI documentation

The dataset is a real-world corporate-finance dataset used for binary classification. It contains financial indicators for Taiwanese companies and a target variable indicating whether a company was classified as bankrupt.

---

## 2. Who Collected the Data?

- **Original data source:** Taiwan Economic Journal (TEJ)
- **Coverage period:** 1999–2009
- **Geographic scope:** Taiwan
- **Bankruptcy definition:** Based on the business regulations of the Taiwan Stock Exchange
- **Donated to UCI:** 27 June 2020

The dataset was collected from the Taiwan Economic Journal and subsequently documented and published through the UCI Machine Learning Repository.

---

## 3. Population

The dataset represents **companies in Taiwan during the 1999–2009 period**.

Each observation represents one company and contains financial information used to classify its bankruptcy status.

### Population limitations

- It represents a specific historical population of Taiwanese companies.
- It should not automatically be assumed to represent:
  - Companies worldwide
  - Companies in other countries
  - Companies in different economic periods
  - Current financial conditions

---

## 4. Dataset Size

| Property | Value |
|---|---:|
| Companies / rows | 6,819 |
| Predictor features | 95 |
| Target variable | `Bankrupt?` |
| Total columns | 96 |
| Missing values | None |
| Classification | Binary |

---

## 5. Target Variable

The target variable is:

**`Bankrupt?`**

- `0` = Non-bankrupt
- `1` = Bankrupt

### Class distribution

| Class | Number of companies | Percentage |
|---|---:|---:|
| Non-bankrupt | 6,599 | 96.77% |
| Bankrupt | 220 | 3.23% |
| **Total** | **6,819** | **100%** |

The dataset therefore has a substantial **class-imbalance problem**, with bankrupt companies representing only a small proportion of the observations.

Because of this imbalance, accuracy alone is not an appropriate measure of model performance. In our project, **recall for the bankruptcy class** was selected as the primary cross-validation metric because failing to identify an actually bankrupt company is an important error for the intended financial-risk screening use case.

---

## 6. Features

The dataset contains **95 financial indicators** covering areas including:

- Profitability
- Liquidity
- Leverage and solvency
- Operating performance
- Asset efficiency
- Working capital
- Cash flow
- Revenue and income growth
- Financial ratios

### Examples of financial indicators

- Return on Assets (ROA)
- Current Ratio
- Acid Test
- Liability-to-Equity Ratio
- Working Capital to Total Assets
- Interest Coverage Ratio
- Net Income to Total Assets
- Total Asset Turnover
- Cash Flow to Total Assets
- Return on Total Asset Growth

The UCI documentation provides the complete list and descriptions of the 95 financial features.

---

## 7. Licence

- **Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0)
- The licence permits sharing and adaptation provided that appropriate credit is given.

### Dataset citation

> Taiwanese Bankruptcy Prediction [Dataset]. (2020). UCI Machine Learning Repository. https://doi.org/10.24432/C5004D

---

## 8. Known Limitations

### 8.1 Population limitation

The dataset represents Taiwanese companies, so the model should not automatically be applied to companies in other countries or economic environments.

### 8.2 Time-period limitation

The financial data cover **1999–2009**. Economic conditions, regulations, financial markets and business practices can change over time, so model performance may differ when applied to more recent companies.

### 8.3 Class imbalance

Only **3.23%** of observations are classified as bankrupt. A model could therefore achieve high overall accuracy while still failing to identify many bankrupt companies.

For this reason, our evaluation emphasizes:

- Recall
- Precision
- F1-score

rather than accuracy alone.

### 8.4 Limited scope of financial information

The model uses the financial indicators available in the dataset. Other factors that could influence bankruptcy risk may not be represented, including:

- Management decisions
- Market conditions
- Industry changes
- Macroeconomic conditions
- Qualitative business information

### 8.5 Intended use

The model should be used as a **financial-risk screening and decision-support tool**, not as:

- An automatic loan-approval system
- An automatic loan-rejection system
- A definitive statement that a company will become bankrupt

A qualified financial risk analyst should consider the prediction alongside additional financial and contextual information.

---

## 9. Why We Selected This Dataset

This dataset meets the requirements of the **AI for Good — Hackathon 5** assignment because it is:

- **Real and documented:** Collected from the Taiwan Economic Journal and documented by UCI.
- **A classification problem:** The target is the binary `Bankrupt?` variable.
- **Large enough:** Contains 6,819 rows and 95 predictor features.
- **Not a prohibited dataset:** It is not a built-in scikit-learn dataset.
- **Relevant to SDG 8:** Corporate financial distress can have consequences for employment, income and economic security.
- **Suitable for model comparison:** It provides a basis for comparing KNN, Logistic Regression and Random Forest as required by the project.

---

## 10. Data File

The project uses the original `data.csv` file associated with the UCI dataset.

- **File:** `data.csv`
- **Approximate size:** 10.9 MB
- **Assignment limit:** 25 MB

The dataset is therefore below the assignment's 25 MB threshold.

---

## 11. Source and Citation

**UCI Machine Learning Repository**

**Dataset:** Taiwanese Bankruptcy Prediction

- **DOI:** 10.24432/C5004D
- **Original data source:** Taiwan Economic Journal (TEJ), 1999–2009
- **Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0)
- **UCI:** https://archive.ics.uci.edu/dataset/572/taiwanese+bankruptcy+prediction
