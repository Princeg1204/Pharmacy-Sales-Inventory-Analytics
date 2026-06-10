# Data Methodology & Processing Pipeline

This document explains the technical implementation of our end-to-end data processing pipeline, including data generation, cleaning rules, feature engineering formulas, and verification checks.

---

## 1. Data Synthesizer Design
We developed `scripts/generate_data.py` to compile a representative simulated pharmacy retail environment containing over 50,000 POS records over 15 months. The generator models realistic market dynamics:
- **Seasonality Peaks**: Spikes in respiratory drug demand in winter (colds and flu) and antihistamines in spring (seasonal allergies).
- **Weekly Patterns**: Higher transaction frequency on Mondays and Fridays (refill trends).
- **Outliers & Anomaly Noise**: Decimal place shift entry errors (multiplied prices) and large-quantity POS errors.
- **Nulls & Corruption**: A 1.5% random missing value rate in quantity, unit price, age, and gender fields, plus fully corrupted rows containing over 30% missing fields.

---

## 2. Ingestion & Validation
`scripts/data_loader.py` acts as our gateway handler:
1. **Format Handling**: Loads either standard flat CSV or structured JSON formats.
2. **Schema Verification**: Compares column names and basic structures against expectations.
3. **Validation Logs**: Outputs a text summary detailing schema validations.

---

## 3. Cleaning & Imputation Pipeline
`scripts/data_cleaner.py` handles the data normalization steps:
- **Deduplication**: Removes exact row duplicates.
- **Corrupted Row Removal**: Drops records that contain more than 30% missing columns (e.g. invalid records).
- **Numeric Imputation**: Fills missing values in transaction quantity and unit price using the column median to prevent average distortions.
- **Categorical Imputation**: Imputes missing customer gender fields as `"Unknown"` rather than dropping valuable transactions.
- **Date Alignment**: Applies forward fill (`ffill`) on transactional timestamp sequences.
- **Outlier Capping**: Detects values outside the Interquartile Range ($1.5 \times \text{IQR}$) bounds on transaction quantity and unit price, capping them at the 5th and 95th percentiles respectively.
- **Text Standardization**: Standardizes fields via strip operations and lowercase conversion to prevent mismatch in groupings.
- **Min-Max Price Normalization**: Computes normalized unit price in range `0-1` to facilitate comparison.

---

## 4. Engineered Feature Metrics
`scripts/feature_engineering.py` runs calculated aggregations:
- **Transaction Revenue & Profit**:
  $$\text{Sales\_Amount} = \text{quantity} \times \text{unit\_price}$$
  $$\text{COGS} = \text{quantity} \times \text{cost\_price}$$
  $$\text{Profit} = \text{Sales\_Amount} - \text{COGS}$$
  $$\text{Profit\_Margin} = \frac{\text{Profit}}{\text{Sales\_Amount}} \times 100$$
- **RFM Customer Segmentation**: Groups customers based on Lifetime Value (CLV, sum of transactional profits) into VIPs (CLV > 90th percentile), At-Risk (CLV < 10th percentile), and Regular patients.
- **Inventory Days to Stockout & Safety Levels**:
  $$\text{Days\_to\_Stockout} = \frac{\text{Current\_Stock}}{\text{Average\_Daily\_Sales}}$$
  $$\text{Reorder\_Point} = (\text{Average\_Daily\_Demand} \times \text{Lead\_Time\_Days}) + \text{Safety\_Stock}$$
- **ABC Classification**: Ranks products descending by total sales revenue. Labels the top 20% of products as Class A, middle 30% as Class B, and bottom 50% as Class C.
- **Inventory Turnover Ratio**:
  $$\text{Inventory\_Turnover} = \frac{\text{Annual\_COGS}}{\text{Current\_Stock} \times \text{Cost\_Price}}$$

---

## 5. Relational Verification
Using `scripts/run_queries.py`, a SQLite database is created, table constraints are checked, and all 15 key SQL queries are verified for output accuracy.
