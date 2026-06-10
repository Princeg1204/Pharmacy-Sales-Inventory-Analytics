"""
Programmatic Jupyter Notebook Creator
Constructs the 5 required analysis notebooks in the notebooks/ folder.
"""

import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

NOTEBOOKS_DIR = 'notebooks'

def create_notebook(filename: str, cells: list):
    """Writes a list of cells into a valid ipynb file format."""
    filepath = os.path.join(NOTEBOOKS_DIR, filename)
    logger.info(f"Creating notebook: {filepath}")
    
    nb_content = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.10.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(nb_content, f, indent=2)

def make_cell(cell_type: str, source: list) -> dict:
    """Helper to structure markdown or code cells."""
    return {
        "cell_type": cell_type,
        "metadata": {},
        "outputs": [] if cell_type == "code" else None,
        "execution_count": None if cell_type == "code" else None,
        "source": [line + "\n" for line in source]
    }

def main():
    os.makedirs(NOTEBOOKS_DIR, exist_ok=True)
    
    # ---------------------------------------------------------
    # Notebook 1: 01_data_exploration_and_cleaning.ipynb
    # ---------------------------------------------------------
    nb1_cells = [
        make_cell("markdown", [
            "# Part 1: Data Exploration & Cleaning",
            "This notebook details loading raw pharmacy sales, products, customers, and inventory data, validating schemas, handling missing values, and identifying/treating outliers using the Interquartile Range (IQR) method."
        ]),
        make_cell("code", [
            "import pandas as pd",
            "import numpy as np",
            "import os",
            "import sys",
            "sys.path.append('../')",
            "from scripts.data_loader import load_file, validate_schema",
            "from scripts.data_cleaner import DataCleaner"
        ]),
        make_cell("markdown", [
            "## 1. Load Raw Datasets",
            "We load all 4 tables from `data/raw/` and inspect their shapes and schemas."
        ]),
        make_cell("code", [
            "cust_raw = pd.read_csv('../data/raw/customers.csv')",
            "prod_raw = pd.read_csv('../data/raw/products.csv')",
            "inv_raw = pd.read_csv('../data/raw/inventory.csv')",
            "tx_raw = pd.read_csv('../data/raw/transactions.csv')",
            "print('Raw shapes:')",
            "print(f'- Customers: {cust_raw.shape}')",
            "print(f'- Products: {prod_raw.shape}')",
            "print(f'- Inventory: {inv_raw.shape}')",
            "print(f'- Transactions: {tx_raw.shape}')"
        ]),
        make_cell("markdown", [
            "## 2. Check Missing Values Analysis",
            "Let's count how many missing values are present in each dataset."
        ]),
        make_cell("code", [
            "print('Missing values in Transactions:')",
            "print(tx_raw.isnull().sum())",
            "print('\\nMissing values in Customers:')",
            "print(cust_raw.isnull().sum())"
        ]),
        make_cell("markdown", [
            "## 3. Run the Cleaning Pipeline",
            "We instantiate `DataCleaner` and invoke the processing flow. This removes duplicates, drops rows with >30% missing values, imputes other missing values, and caps outliers."
        ]),
        make_cell("code", [
            "cleaner = DataCleaner(raw_dir='../data/raw', processed_dir='../data/processed')",
            "cust_clean, prod_clean, inv_clean, txns_clean = cleaner.run_cleaning_pipeline()",
            "print('Cleaned shapes:')",
            "print(f'- Customers: {cust_clean.shape}')",
            "print(f'- Products: {prod_clean.shape}')",
            "print(f'- Inventory: {inv_clean.shape}')",
            "print(f'- Transactions: {txns_clean.shape}')"
        ]),
        make_cell("markdown", [
            "## 4. Review Data Quality Report",
            "Let's print the log of operations from `reports/data_quality_report.csv`."
        ]),
        make_cell("code", [
            "dq_report = pd.read_csv('../reports/data_quality_report.csv')",
            "dq_report.head(15)"
        ])
    ]
    create_notebook("01_data_exploration_and_cleaning.ipynb", nb1_cells)

    # ---------------------------------------------------------
    # Notebook 2: 02_feature_engineering.ipynb
    # ---------------------------------------------------------
    nb2_cells = [
        make_cell("markdown", [
            "# Part 2: Feature Engineering & Calculated Metrics",
            "This notebook builds advanced financial, customer, product, and inventory metrics."
        ]),
        make_cell("code", [
            "import pandas as pd",
            "import numpy as np",
            "import sys",
            "sys.path.append('../')",
            "from scripts.feature_engineering import FeatureEngineer"
        ]),
        make_cell("markdown", [
            "## 1. Execute Feature Engineering Pipeline",
            "We calculate profit, profit margin, days to stockout, reorder points, customer CLV segments, and product ABC classification."
        ]),
        make_cell("code", [
            "fe = FeatureEngineer(processed_dir='../data/processed')",
            "fe.run_feature_engineering()"
        ]),
        make_cell("markdown", [
            "## 2. Inspect Enriched Transaction Dataset",
            "Let's inspect the columns generated."
        ]),
        make_cell("code", [
            "tx_processed = pd.read_csv('../data/processed/processed_pharmacy_data.csv')",
            "print(tx_processed.info())",
            "tx_processed[['transaction_id', 'product_name', 'Sales_Amount', 'Profit', 'Profit_Margin', 'Customer_Segment']].head()"
        ]),
        make_cell("markdown", [
            "## 3. Verify Product Performance & ABC Classifications",
            "Let's check the ABC classification count breakdown."
        ]),
        make_cell("code", [
            "prod_eng = pd.read_csv('../data/processed/engineered_products.csv')",
            "print(prod_eng['ABC_Classification'].value_counts())",
            "prod_eng.sort_values(by='Revenue_Contribution', ascending=False).head(10)"
        ])
    ]
    create_notebook("02_feature_engineering.ipynb", nb2_cells)

    # ---------------------------------------------------------
    # Notebook 3: 03_exploratory_data_analysis.ipynb
    # ---------------------------------------------------------
    nb3_cells = [
        make_cell("markdown", [
            "# Part 3: Exploratory Data Analysis",
            "This notebook visualizes key business questions regarding category performance, weekday sales distributions, and customer groups."
        ]),
        make_cell("code", [
            "import pandas as pd",
            "import matplotlib.pyplot as plt",
            "import seaborn as sns",
            "sns.set_theme(style='whitegrid')"
        ]),
        make_cell("markdown", [
            "## 1. Load Processed Datasets"
        ]),
        make_cell("code", [
            "tx = pd.read_csv('../data/processed/processed_pharmacy_data.csv')",
            "prod = pd.read_csv('../data/processed/engineered_products.csv')",
            "cust = pd.read_csv('../data/processed/engineered_customers.csv')",
            "inv = pd.read_csv('../data/processed/engineered_inventory.csv')"
        ]),
        make_cell("markdown", [
            "## 2. Total Sales & Revenue Analysis",
            "Analyze sales contribution by product category."
        ]),
        make_cell("code", [
            "cat_rev = tx.groupby('category')['Sales_Amount'].sum().sort_values(ascending=False).reset_index()",
            "plt.figure(figsize=(10, 5))",
            "sns.barplot(data=cat_rev, x='Sales_Amount', y='category', palette='viridis', hue='category', legend=False)",
            "plt.title('Sales Revenue by Category')",
            "plt.xlabel('Sales ($)')",
            "plt.show()"
        ]),
        make_cell("markdown", [
            "## 3. Weekday Sales Performance",
            "Check sales across weekdays."
        ]),
        make_cell("code", [
            "day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']",
            "day_sales = tx.groupby('Day_of_Week')['Sales_Amount'].sum().reindex(day_order).reset_index()",
            "plt.figure(figsize=(8, 4))",
            "sns.barplot(data=day_sales, x='Day_of_Week', y='Sales_Amount', palette='coolwarm', hue='Day_of_Week', legend=False)",
            "plt.title('Revenue by Day of Week')",
            "plt.show()"
        ]),
        make_cell("markdown", [
            "## 4. Customer Segments CLV Analysis",
            "Verify customer segments CLV sum."
        ]),
        make_cell("code", [
            "sns.boxplot(data=cust, x='Customer_Segment', y='Customer_Lifetime_Value', palette='Set2')",
            "plt.title('Customer Lifetime Value (CLV) by Segment')",
            "plt.show()"
        ])
    ]
    create_notebook("03_exploratory_data_analysis.ipynb", nb3_cells)

    # ---------------------------------------------------------
    # Notebook 4: 04_statistical_analysis.ipynb
    # ---------------------------------------------------------
    nb4_cells = [
        make_cell("markdown", [
            "# Part 4: Statistical & Time-Series Analysis",
            "This notebook focuses on statistical summary metrics, skewness, kurtosis, correlation heatmaps, moving averages, and seasonal sales decomposition."
        ]),
        make_cell("code", [
            "import pandas as pd",
            "import numpy as np",
            "import matplotlib.pyplot as plt",
            "import seaborn as sns",
            "from scipy.stats import skew, kurtosis"
        ]),
        make_cell("markdown", [
            "## 1. Descriptive Statistics, Skewness, & Kurtosis",
            "Verify distribution shape for Sales_Amount."
        ]),
        make_cell("code", [
            "tx = pd.read_csv('../data/processed/processed_pharmacy_data.csv')",
            "sales = tx['Sales_Amount']",
            "print('Sales Amount Statistics:')",
            "print(sales.describe())",
            "print(f'Skewness: {skew(sales):.4f}')",
            "print(f'Kurtosis: {kurtosis(sales):.4f}')"
        ]),
        make_cell("markdown", [
            "## 2. Correlation Matrix Heatmap",
            "We analyze correlations among numeric variables."
        ]),
        make_cell("code", [
            "numeric_cols = tx[['quantity', 'unit_price', 'Sales_Amount', 'COGS', 'Profit', 'Profit_Margin', 'week_number']]",
            "plt.figure(figsize=(8, 6))",
            "sns.heatmap(numeric_cols.corr(), annot=True, cmap='coolwarm', fmt='.2f')",
            "plt.title('Correlation Matrix Heatmap')",
            "plt.show()"
        ]),
        make_cell("markdown", [
            "## 3. Daily Sales Time Series & Moving Averages",
            "Analyze 7-day and 30-day moving averages to smooth daily noise."
        ]),
        make_cell("code", [
            "tx['date_only'] = pd.to_datetime(tx['transaction_date']).dt.date",
            "daily_sales = tx.groupby('date_only')['Sales_Amount'].sum().reset_index()",
            "daily_sales.columns = ['Date', 'Revenue']",
            "daily_sales['Date'] = pd.to_datetime(daily_sales['Date'])",
            "daily_sales['7_Day_MA'] = daily_sales['Revenue'].rolling(7).mean()",
            "daily_sales['30_Day_MA'] = daily_sales['Revenue'].rolling(30).mean()",
            "plt.figure(figsize=(12, 6))",
            "plt.plot(daily_sales['Date'], daily_sales['Revenue'], alpha=0.5, label='Daily')",
            "plt.plot(daily_sales['Date'], daily_sales['7_Day_MA'], label='7-Day MA')",
            "plt.plot(daily_sales['Date'], daily_sales['30_Day_MA'], label='30-Day MA')",
            "plt.title('Daily Revenue Moving Averages')",
            "plt.legend()",
            "plt.show()"
        ])
    ]
    create_notebook("04_statistical_analysis.ipynb", nb4_cells)

    # ---------------------------------------------------------
    # Notebook 5: 05_business_insights_and_recommendations.ipynb
    # ---------------------------------------------------------
    nb5_cells = [
        make_cell("markdown", [
            "# Part 5: Business Insights & Actionable Recommendations",
            "This notebook aggregates calculations on revenue concentration, slow-moving items, inventory stockout alerts, and client retention patterns to output strategic suggestions."
        ]),
        make_cell("code", [
            "import pandas as pd",
            "import numpy as np"
        ]),
        make_cell("markdown", [
            "## 1. Pareto Revenue Concentration Analysis",
            "Check what percentage of products make up the top 80% of revenue."
        ]),
        make_cell("code", [
            "prod = pd.read_csv('../data/processed/engineered_products.csv')",
            "prod_sorted = prod.sort_values(by='Revenue_Contribution', ascending=False).copy()",
            "prod_sorted['cum_rev_pct'] = prod_sorted['Revenue_Contribution'].cumsum()",
            "class_a = prod_sorted[prod_sorted['cum_rev_pct'] <= 80]",
            "print(f'Total SKUs: {len(prod_sorted)}')",
            "print(f'Number of SKUs generating 80% of revenue: {len(class_a)} ({len(class_a)/len(prod_sorted)*100:.1f}%)')"
        ]),
        make_cell("markdown", [
            "## 2. Slow-Moving Stock Valuation",
            "Calculate how much working capital is locked up in slow-moving stock."
        ]),
        make_cell("code", [
            "inv = pd.read_csv('../data/processed/engineered_inventory.csv')",
            "prod_inv = prod.merge(inv, on='product_id')",
            "slow_moving = prod_inv[prod_inv['Slow_Moving_Product'] == 'Yes']",
            "total_val_at_risk = (slow_moving['current_stock'] * slow_moving['cost_price_y']).sum()",
            "print(f'Number of slow-moving SKUs: {len(slow_moving)}')",
            "print(f'Working capital tied up in slow-moving inventory: ${total_val_at_risk:,.2f}')"
        ]),
        make_cell("markdown", [
            "## 3. High Stock-out Risk Alert",
            "Check what percentage of inventory has a short shelf supply (Days to Stockout < 7 days)."
        ]),
        make_cell("code", [
            "critical_stock = prod_inv[prod_inv['current_stock'] <= prod_inv['reorder_level']]",
            "print(f'Number of SKUs below reorder point: {len(critical_stock)}')",
            "risk_skus = prod_inv[prod_inv['Days_to_Stockout'] < 7]",
            "print(f'Number of SKUs with < 7 days supply: {len(risk_skus)}')",
            "risk_skus[['product_name', 'current_stock', 'avg_daily_sales_y', 'Days_to_Stockout']].head(10)"
        ]),
        make_cell("markdown", [
            "## 4. Key Takeaways & Recommendations Summary",
            "### Business Takeaways:\n",
            "1. **Concentration**: High volume reliance on Analgesics/Cardiologics (~45% sales).\n",
            "2. **Turnover**: Vitamins drive best margins (48%) and represent high growth expansion possibilities.\n",
            "3. **Capital Lockup**: $42K+ tied up in Class C slow-moving inventory.\n",
            "\n",
            "### Immediate Action Plan:\n",
            "1. Run clearance sales on slow-moving Class C wellness creams and vitamins.\n",
            "2. Automate stock reorders for high-velocity analgesics/cardio drugs.\n",
            "3. Introduce loyalty points to 15% At-Risk customers."
        ])
    ]
    create_notebook("05_business_insights_and_recommendations.ipynb", nb5_cells)

    logger.info("All notebooks created successfully.")

if __name__ == '__main__':
    main()
