# Data Dictionary

This document details the structures, data types, and attributes of the tables in our analytics environment.

---

## 1. Customers Table (`customers.csv` / `customers`)
Registered pharmacy customers.

| Column Name | Data Type | Key / Constraint | Description | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `customer_id` | TEXT (VARCHAR) | PRIMARY KEY | Unique customer identifier | `CUST0001` |
| `customer_name` | TEXT (VARCHAR) | NOT NULL | Customer full name | `Alice Smith` |
| `email` | TEXT (VARCHAR) | - | Customer contact email | `alice.smith@pharmmail.com` |
| `gender` | TEXT (VARCHAR) | - | Customer gender | `Female` |
| `age` | INTEGER | - | Customer age in years | `34` |
| `store_location` | TEXT (VARCHAR) | - | Preferred shopping store location | `Downtown Pharmacy` |
| `registration_date` | DATE | - | Date the profile was registered | `2025-01-15` |

---

## 2. Products Table (`products.csv` / `products`)
Pharmacy product catalog items.

| Column Name | Data Type | Key / Constraint | Description | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `product_id` | TEXT (VARCHAR) | PRIMARY KEY | Unique product identifier | `PROD001` |
| `product_name` | TEXT (VARCHAR) | NOT NULL | Commercial product name | `Paracetamol 500mg (Tablets)` |
| `category` | TEXT (VARCHAR) | NOT NULL | Pharmaceutical category | `Analgesics` |
| `cost_price` | DECIMAL (REAL) | NOT NULL | Wholesale cost price | `1.50` |
| `retail_price` | DECIMAL (REAL) | NOT NULL | POS retail selling price | `2.50` |

---

## 3. Inventory Table (`inventory.csv` / `inventory`)
Current stock metrics.

| Column Name | Data Type | Key / Constraint | Description | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `product_id` | TEXT (VARCHAR) | FOREIGN KEY | References `products(product_id)` | `PROD001` |
| `current_stock` | INTEGER | NOT NULL | On-hand quantity in stock | `250` |
| `reorder_level` | INTEGER | NOT NULL | Stock count triggering purchase | `80` |
| `safety_stock` | INTEGER | NOT NULL | Safety buffer stock quantity | `20` |
| `lead_time_days` | INTEGER | NOT NULL | Supplier delivery wait time in days | `5` |
| `avg_daily_sales` | DECIMAL (REAL) | NOT NULL | Average daily units sold | `12.50` |
| `cost_price` | DECIMAL (REAL) | NOT NULL | wholesale cost price | `1.50` |

---

## 4. Transactions Table (`transactions.csv` / `transactions`)
POS Transaction detailed records.

| Column Name | Data Type | Key / Constraint | Description | Sample Value |
| :--- | :--- | :--- | :--- | :--- |
| `transaction_id` | TEXT (VARCHAR) | PRIMARY KEY | Unique transaction line ID | `TXN00001` |
| `transaction_date`| TIMESTAMP | - | Date & time of the transaction | `2025-01-20 10:15:00` |
| `customer_id` | TEXT (VARCHAR) | FOREIGN KEY | References `customers(customer_id)` | `CUST0001` |
| `product_id` | TEXT (VARCHAR) | FOREIGN KEY | References `products(product_id)` | `PROD001` |
| `quantity` | INTEGER | NOT NULL | Number of units purchased | `2` |
| `unit_price` | DECIMAL (REAL) | NOT NULL | Selling price per unit (after POS discount) | `2.50` |
| `store_location` | TEXT (VARCHAR) | NOT NULL | Store location of purchase | `Downtown Pharmacy` |
| `is_holiday` | TEXT (VARCHAR) | NOT NULL | Holiday period indicator (`Yes` / `No`) | `No` |
| `product_name` | TEXT (VARCHAR) | NOT NULL | Denormalized product name | `Paracetamol 500mg (Tablets)` |
| `category` | TEXT (VARCHAR) | NOT NULL | Denormalized category | `Analgesics` |
| `cost_price` | DECIMAL (REAL) | NOT NULL | Denormalized wholesale unit price | `1.50` |
| `sales_amount` | DECIMAL (REAL) | NOT NULL | Engineered: Total price (`qty * unit_price`) | `5.00` |
| `cogs` | DECIMAL (REAL) | NOT NULL | Engineered: Cost of goods sold (`qty * cost_price`)| `3.00` |
| `profit` | DECIMAL (REAL) | NOT NULL | Engineered: Net profit (`sales_amount - cogs`) | `2.00` |
| `profit_margin` | DECIMAL (REAL) | NOT NULL | Engineered: Margin percentage | `40.00` |
| `day_of_week` | TEXT (VARCHAR) | NOT NULL | Engineered: Weekday name | `Monday` |
| `month` | TEXT (VARCHAR) | NOT NULL | Engineered: Month name | `January` |
| `quarter` | TEXT (VARCHAR) | NOT NULL | Engineered: Quarter designation | `Q1` |
| `week_number` | INTEGER | NOT NULL | Engineered: Iso week number | `4` |
| `customer_segment`| TEXT (VARCHAR) | NOT NULL | Engineered: RFM customer category (`VIP`/`Regular`/`At-Risk`) | `Regular` |
