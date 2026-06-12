# Pharmacy Database Management & Analytics System

An end-to-end database management and analytics solution for a pharmacy retail company.
Built using PostgreSQL-compatible SQL schema design, Python ETL pipelines, and Power BI
reporting — covering 50,000+ POS transactions across sales, inventory, and customer data.

---

## Author

- **Name**: Gajera Prince
- **GitHub**: [github.com/Princeg1204](https://github.com/Princeg1204)
- **LinkedIn**: [linkedin.com/in/princegajera](https://www.linkedin.com/in/princegajera/)

---

## Problem Statement

Retail pharmacies struggle with three core database management challenges:

1. **Inventory Drift** — No real-time visibility into stock levels; manual tracking leads to
   over-stocking slow-moving items and stock-outs on critical medications.
2. **Revenue Leakage** — Inability to query and segment transaction data to identify
   high-value customers or profit-draining product categories.
3. **Report Delays** — Business decisions are delayed because analytics reports are manually
   prepared rather than generated directly from the database.

This project resolves these challenges by designing a normalized relational database,
writing 15 analytical SQL queries, and building an automated Python pipeline
to load, clean, and query structured pharmacy data.

---

## Tech Stack

| Layer | Tools Used |
|---|---|
| Database | SQLite (local) / PostgreSQL-compatible schema |
| Schema & Queries | SQL — DDL (CREATE, INDEX), DML (INSERT), DQL (SELECT, JOIN, GROUP BY, subqueries, views) |
| ETL Pipeline | Python 3.10+, Pandas, NumPy |
| Reporting | OpenPyXL (Excel), ReportLab (PDF) |
| BI Dashboard | Power BI Desktop (DAX measures, Star Schema) |
| Version Control | Git, GitHub |

---

## Database Design

The schema (`sql/schema.sql`) defines 4 normalized relational tables with
primary keys, foreign keys, and performance indexes:

| Table | Description |
|---|---|
| `transactions` | 50,000+ POS sales records with product, customer, date, quantity, revenue |
| `products` | Product master with category, unit cost, selling price, ABC classification |
| `customers` | Customer profiles with CLV score, RFM segment, location |
| `inventory` | Real-time stock levels, reorder thresholds, supplier info |

**Indexes created** for performance optimization on high-frequency query columns:
- `idx_transactions_date` — speeds up date-range queries
- `idx_transactions_product_id` — optimizes product-level joins
- `idx_inventory_stock_level` — accelerates low-stock alert queries

---

## SQL Analysis — 15 Queries

All queries are in `sql/queries_15_analysis.sql`. Key queries include:

| # | Query | Technique Used |
|---|---|---|
| 1 | Total revenue by product category | GROUP BY, SUM |
| 2 | Top 10 revenue-generating products | ORDER BY, LIMIT |
| 3 | Month-over-month revenue trend | DATE functions, GROUP BY |
| 4 | Low-stock products below reorder point | WHERE, JOIN |
| 5 | Customer purchase frequency ranking | COUNT, GROUP BY, ORDER BY |
| 6 | Profit margin per category | Computed column, AVG |
| 7 | VIP customer identification (top 20% by CLV) | Subquery, percentile filter |
| 8 | Dead stock — items not sold in 90 days | LEFT JOIN, IS NULL, date filter |
| 9 | Revenue contribution by store location | GROUP BY, percentage calculation |
| 10 | Category-wise average order value | AVG, JOIN across 2 tables |
| 11 | Stock turnover ratio per product | Division operation, JOIN |
| 12 | Daily transaction volume trend | DATE GROUP BY |
| 13 | Products with highest stockout risk | JOIN + threshold filter |
| 14 | Customer retention — repeat buyers | COUNT > 1 subquery |
| 15 | Executive KPI summary view | Multi-table aggregation |

---

## Key Database Findings

- **Pareto Rule holds**: Top 20% of products generate 78.4% of total revenue
- **$42,000+ capital locked** in slow-moving Class C inventory items
- **12.5% of products** are below critical reorder levels — flagged by SQL query
- **Vitamins** show highest profit margin (48%); Cardiologics highest sales volume

---

## Project Structure
