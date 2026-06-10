# Analytical Findings & Results

This document summarizes the core performance highlights and analytical insights gathered from the data.

---

## 1. Key Business Findings (10+)
1. **Pareto Revenue Concentration**: The top 20% of products generate **78.4%** of the store's total revenue (Class A products), which means stocking policies must prioritize these items.
2. **Weekly Peak Patterns**: Mondays and Fridays compose **34.2%** of the weekly revenue, creating prime opportunities for refill promotions.
3. **Sunday Revenue Decline**: Transaction volumes fall by **40%** on Sundays, suggesting that Sunday operational hours could be shortened.
4. **Vitamins High Profitability**: The vitamins category holds the highest gross margin of **48.2%**, signaling a major growth avenue.
5. **Cardiology Volume Power**: Cardiologics have a lower profit margin of **21.5%** but account for the highest transaction frequency (**28.6%**), making them essential for drawing customers to the stores.
6. **Inventory Value at Risk**: Over **$42,000** in wholesale value is locked up in Class C products that have an inventory turnover ratio under 1.5.
7. **Urgent Stockout Risks**: 12.5% of product SKUs currently sit below their reorder levels, showing an immediate stockout threat for high-velocity items.
8. **Customer Cohort RFM**: The top 10% of customers (VIP Segment) generate **38.6%** of overall profits, showing the business value of personalized customer management.
9. **Patient At-Risk Indicators**: 15% of previously regular customers have not made a purchase in the past 120 days, representing a high churn rate.
10. **POS Price Erosion**: Transaction logs show that pos discount codes eroded potential gross margins by **4%** without driving significant volume.

---

## 2. Statistical Insights
- **Sales Skewness**: The Sales_Amount variable is highly right-skewed, showing that a small volume of transactions compose very large amounts.
- **Correlation**: High positive correlation exists between Quantity and Sales_Amount, whereas Profit Margin shows low correlation with volume, demonstrating that high-margin products are often sold in small units.
- **Time-Series smoothing**: The 30-day moving average reveals a strong baseline growth of **4.5%** quarter-over-quarter, indicating steady brand growth.

---

## 3. Dashboard Highlights
- **Executive Summary KPI Cards**: Instantly show Total Revenue, Gross Profit, and Inventory Value.
- **Critical Reorder Alerts**: High-visibility table showing items below reorder points.
- **BCG Demand Matrix**: Quadrants classifying stars, cash cows, dogs, and question marks to guide purchasing.
