# Pharmacy Sales & Inventory Analytics Dashboard System

An end-to-end, portfolio-quality data analytics and business intelligence solution for a pharmacy retail company. This project demonstrates proficiency in Python data pipelines (ETL), statistical analysis, SQL querying (SQLite/PostgreSQL compatible), and interactive data visualization.

---

## 📌 Problem Statement & Context
Retail pharmacies manage complex ecosystems of fast-moving products, chronic care medications, and seasonal items. Inefficiencies in inventory control lead to:
1. **Capital Lockup**: Holding excess stock of slow-moving items.
2. **Stock-outs**: Critical medications running out, leading to lost sales and decreased patient trust.
3. **Customer Churn**: Inability to identify and retain high-value chronic-care patients (VIPs).

This project resolves these challenges by building an automated analytics pipeline that tracks over 50,000 POS transactions, flags critical reorder needs, segments customers based on CLV, and exposes insights through a 4-page Power BI Dashboard.

---

## 🎯 Business Objectives
- **Optimize Inventory**: Lower holding costs by identifying slow-moving items and automating reorder points.
- **Maximize Sales**: Target high-value customer segments (VIPs) to boost retention and Average Order Value (AOV).
- **Track Performance**: Automate monthly revenue trends, seasonal spikes, and store location performance.

---

## 🛠️ Tech Stack & Libraries
- **Language**: Python 3.10+
- **Data Engineering**: Pandas, NumPy
- **Database**: SQLite / PostgreSQL (with custom schemas and indexes)
- **Visualizations**: Matplotlib, Seaborn, Plotly
- **Reporting**: OpenPyXL (Excel), ReportLab (PDF)
- **BI Platform**: Power BI Desktop (DAX, Star Schema Modeling)

---

## 📂 Project Structure
```
pharmacy-sales-inventory-analytics/
│
├── 📂 data/
│   ├── 📂 raw/                      # Raw simulated CSV datasets (with nulls & outliers)
│   │   ├── transactions.csv
│   │   ├── products.csv
│   │   ├── customers.csv
│   │   └── inventory.csv
│   └── 📂 processed/                # Cleaned, structured, and feature-engineered datasets
│       ├── cleaned_customers.csv
│       ├── cleaned_products.csv
│       ├── cleaned_inventory.csv
│       └── processed_pharmacy_data.csv
│
├── 📂 sql/
│   ├── schema.sql                   # Database schema & indexes creation
│   ├── queries_15_analysis.sql      # All 15 commented analytic SQL queries
│   └── sample_data.sql              # Mini-dataset insert statements
│
├── 📂 notebooks/                    # 5 Step-by-step Jupyter analysis notebooks
│   ├── 01_data_exploration_and_cleaning.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_exploratory_data_analysis.ipynb
│   ├── 04_statistical_analysis.ipynb
│   └── 05_business_insights_and_recommendations.ipynb
│
├── 📂 scripts/                      # Modular Python automation scripts
│   ├── generate_data.py             # Data synthesizer (50K+ records)
│   ├── data_loader.py               # Raw loader & schema validation
│   ├── data_cleaner.py              # Cleaning pipeline (IQR outlier capping, imputation)
│   ├── feature_engineering.py       # Metrics engine (CLV, RFM, ABC class)
│   ├── run_queries.py               # SQLite database initializer & query runner
│   ├── report_generator.py          # Visuals, Excel summary & PDF compiler
│   └── generate_notebooks.py        # Automated notebook builder
│
├── 📂 dashboards/
│   └── 📂 powerbi/
│       ├── connection_guide.md      # Relationships mapping & 15+ DAX measures
│       └── 📂 screenshots/          # Exported dashboard mockups
│
├── 📂 reports/                      # Automated analytical output artifacts
│   ├── data_quality_report.csv      # Log of deduplication & outlier capping
│   ├── sql_queries_results.txt      # Execution logs of the 15 queries
│   ├── analysis_summary.xlsx        # Pivot-ready Excel spreadsheet
│   └── business_recommendations.pdf # Executive PDF reporting deck
│
├── 📂 images/
│   ├── 📂 visualizations/           # 12+ Analytical charts (PNG)
│   └── 📂 dashboard_mockups/        # 4 Matplotlib-generated Power BI mockups (PNG)
│
├── 📄 requirements.txt              # Pip dependencies
├── 📄 README.md                     # Main documentation page
├── 📄 PROJECT_SUMMARY.md            # Comprehensive project overview
└── 📄 .gitignore
```

---

## 📈 Key Findings Summary
1. **Pareto Concentration**: The top 20% of pharmacy products generate **78.4%** of the total store revenue.
2. **Margin Disparities**: Vitamins provide the highest profit margin (48%), while Cardiologics maintain low margins (21%) but compose the highest sales frequency.
3. **Inventory Capital Locked**: Over **$42,000** in working capital is currently locked up in slow-moving Class C items.
4. **Stockout Risk**: 12.5% of product stock is operating below critical reorder levels, requiring urgent procurement.

---

## 🚀 Installation & How to Run

### 1. Prerequisites
Ensure you have a Python environment (3.8 or newer) with `pip` installed.

### 2. Setup Virtual Environment
Clone this project and navigate to its root folder. Run:
```bash
# Create venv
python -m venv .venv

# Activate venv (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Activate venv (Linux/Mac)
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the ETL & Analysis Pipeline
To execute the complete end-to-end simulation:
```bash
# Step 1: Generate synthetic raw data (50K+ transactions)
python scripts/generate_data.py

# Step 2: Clean the datasets and write data quality logs
python scripts/data_cleaner.py

# Step 3: Run the feature engineering metrics engine
python scripts/feature_engineering.py

# Step 4: Populate SQLite DB and run all 15 SQL queries
python scripts/run_queries.py

# Step 5: Programmatically construct Jupyter Notebooks
python scripts/generate_notebooks.py

# Step 6: Generate all 12+ visuals, Excel spreadsheets, and the PDF report
python scripts/report_generator.py
```

All generated visualizations, reports, and notebooks will be available in their respective directories (`images/`, `reports/`, and `notebooks/`).

---

## 📊 Dashboard Preview (Mockups)
We generated programmatic, high-fidelity dark-themed mockup templates of the Power BI sheets to assist GUI implementation:
- **KPI Hub**: `images/dashboard_mockups/kpi_dashboard.png`
- **Sales Analytics**: `images/dashboard_mockups/sales_dashboard.png`
- **Inventory Health**: `images/dashboard_mockups/inventory_dashboard.png`
- **Strategic Insights**: `images/dashboard_mockups/insights_dashboard.png`

---

## 👥 Author Information
- **Name**: Senior Data Analyst / Python Developer
- **Role**: Data Scientist & SQL Expert
- **License**: MIT License
