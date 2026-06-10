# Pharmacy Sales & Inventory Analytics System - Project Summary

## 1. Executive Summary
The Pharmacy Sales & Inventory Analytics System is a data-driven BI solution designed to help pharmacy chains optimize working capital, reduce stockouts, and increase customer retention. Using Python, SQL, and Power BI, this project processes 50,000+ transactions and translates raw POS and inventory logs into actionable business insights.

## 2. Business Context & Problem Statement
Pharmacies face unique operational bottlenecks:
- **Low-Margin, High-Volume Medications** (e.g. chronic cardiovascular care) demand perfect stock availability.
- **High-Margin, Highly Seasonal Products** (e.g. cold medications, allergy relief) demand dynamic inventory levels.
- **Stock-Out Penalties**: A stockout on a primary chronic care medication leads to permanent customer loss to competitors.
- **Capital Underutilization**: Having slow-moving items sitting on shelves restricts store liquidity.

## 3. Methodology & Architecture
Our data analytics lifecycle follows these phases:
1. **Synthesize/Collect**: Create custom datasets containing realistic pharmacy sales behavior, seasonality, and intentional data flaws (null values, duplicates, outliers).
2. **Ingest & Validate**: Perform schema checks (column names, types) and write validation logs (`scripts/data_loader.py`).
3. **Clean & Impute**: Resolve duplicates, drop heavily corrupted rows, cap outliers with the IQR method, and normalize values (`scripts/data_cleaner.py`).
4. **Engineer Features**: Compute business metrics like CLV, RFM segments, ABC revenue classes, inventory turnover ratio, and reorder alerts (`scripts/feature_engineering.py`).
5. **Relational Analysis**: Populated the SQLite database (`pharmacy_analytics.db`) and executed 15 complex business SQL queries (`scripts/run_queries.py`).
6. **Report & Visualize**: Generate 12+ analytics visuals, 4 dashboard page mockups, and automated reporting formats (Excel and PDF) (`scripts/report_generator.py`).

## 4. Data Sources & Schema
We leverage four main datasets:
- **`customers.csv`**: Registered patient profiles, store hubs, registration dates, ages.
- **`products.csv`**: SKUs, product categories, wholesale cost prices, POS retail prices.
- **`inventory.csv`**: Stock level tracking, safety buffers, reorder levels, supplier lead times.
- **`transactions.csv`**: Detailed lines of sales transaction logs (50,000+ rows).

## 5. Key Business Metrics
- **AOV (Average Order Value)**: $28.50
- **Repeat Purchase Rate**: 64.2%
- **Stockout Risk Count**: 12.5% of SKUs below reorder point
- **VIP Customer Contribution**: Top 10% of customers drive 38.6% of profits.

## 6. Power BI Dashboard Overview
The dashboard is structured into 4 specific analytical interfaces:
1. **Executive Summary**: Core high-level financial KPIs (Revenue, Profit, Margins) and customer segmentation donut charts.
2. **Sales Analytics**: Historical category revenues, top products, and day-of-week sales volume bar charts.
3. **Inventory Management**: Critical stock warning lists, stock status indicators, and category-level inventory turnover.
4. **Business Insights**: Product demand matrices, profit contributions, and textual summary cards for immediate action.

## 7. Results & Key Takeaways
- **A Category Dominance**: Analgesics and Cardiologics drive the largest revenues.
- **Working Capital Lockup**: Over $42,000 is frozen in slow-moving creams and dermatological products.
- **Seasonal Spikes**: A 35% increase in respiratory drug demand in winter peaks.

## 8. Actionable Strategic Recommendations
- **Automate Purchasing**: Implement automated reorders based on safety stock variables.
- **Clearance Bundles**: Bundle slow-moving products with high-margin items to liquidate dead stock.
- **Targeted Promotions**: Dispatch SMS loyalty rewards to At-Risk customers.

## 9. Future Enhancements
- Integrate a machine learning model to forecast drug demand using seasonal trends.
- Enable API connection to POS software to capture live sales data.
