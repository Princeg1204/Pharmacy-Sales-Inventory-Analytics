-- Database Schema for Pharmacy Sales & Inventory Analytics System
-- Compatible with SQLite and PostgreSQL

-- Drop tables if they exist
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

-- 1. Customers Table
CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    gender VARCHAR(20),
    age INTEGER,
    store_location VARCHAR(100),
    registration_date DATE
);

-- 2. Products Table
CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    cost_price DECIMAL(10, 2) NOT NULL,
    retail_price DECIMAL(10, 2) NOT NULL
);

-- 3. Inventory Table
CREATE TABLE inventory (
    product_id VARCHAR(50) PRIMARY KEY,
    current_stock INTEGER NOT NULL,
    reorder_level INTEGER NOT NULL,
    safety_stock INTEGER NOT NULL,
    lead_time_days INTEGER NOT NULL,
    avg_daily_sales DECIMAL(10, 2) NOT NULL,
    cost_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- 4. Transactions Table (Enriched/Processed for Analytics)
CREATE TABLE transactions (
    transaction_id VARCHAR(50),
    transaction_date TIMESTAMP,
    customer_id VARCHAR(50),
    product_id VARCHAR(50),
    quantity INTEGER,
    unit_price DECIMAL(10, 2),
    store_location VARCHAR(100),
    is_holiday VARCHAR(5),
    normalized_unit_price DECIMAL(10, 6),
    product_name VARCHAR(100),
    category VARCHAR(50),
    cost_price DECIMAL(10, 2),
    Sales_Amount DECIMAL(10, 2),
    COGS DECIMAL(10, 2),
    Profit DECIMAL(10, 2),
    Profit_Margin DECIMAL(10, 2),
    Day_of_Week VARCHAR(15),
    Month VARCHAR(15),
    Quarter VARCHAR(5),
    Week_Number INTEGER,
    Customer_Segment VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Create indexes for performance optimization
CREATE INDEX idx_transactions_product ON transactions(product_id);
CREATE INDEX idx_transactions_customer ON transactions(customer_id);
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
CREATE INDEX idx_transactions_category ON transactions(category);
CREATE INDEX idx_transactions_store ON transactions(store_location);
