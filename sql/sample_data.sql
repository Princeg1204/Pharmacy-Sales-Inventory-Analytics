-- ==============================================================================
-- PHARMACY SALES & INVENTORY - SAMPLE INSERT STATEMENTS
-- ==============================================================================

-- 1. Insert Sample Customers
INSERT INTO customers (customer_id, customer_name, email, gender, age, store_location, registration_date) VALUES
('CUST0001', 'Alice Smith', 'alice.smith@pharmmail.com', 'Female', 34, 'Downtown Pharmacy', '2025-01-15'),
('CUST0002', 'Bob Johnson', 'bob.johnson@pharmmail.com', 'Male', 52, 'Suburban Wellness Center', '2025-02-10'),
('CUST0003', 'Carol Davis', 'carol.davis@pharmmail.com', 'Female', 67, 'Metro Pharmacy Hub', '2025-03-05'),
('CUST0004', 'David Wilson', 'david.wilson@pharmmail.com', 'Male', 21, 'Eastside Medical Pharmacy', '2025-04-18');

-- 2. Insert Sample Products
INSERT INTO products (product_id, product_name, category, cost_price, retail_price) VALUES
('PROD001', 'Paracetamol 500mg (Tablets)', 'Analgesics', 1.50, 2.50),
('PROD002', 'Amoxicillin 250mg (Capsules)', 'Antibiotics', 5.00, 7.50),
('PROD003', 'Atorvastatin 20mg (Tablets)', 'Cardiologics', 12.00, 18.00),
('PROD004', 'Metformin 500mg (Tablets)', 'Antidiabetics', 2.00, 3.20);

-- 3. Insert Sample Inventory
INSERT INTO inventory (product_id, current_stock, reorder_level, safety_stock, lead_time_days, avg_daily_sales, cost_price) VALUES
('PROD001', 250, 80, 20, 5, 12.50, 1.50),
('PROD002', 45, 30, 10, 7, 3.20, 5.00),
('PROD003', 150, 40, 15, 6, 2.80, 12.00),
('PROD004', 8, 50, 15, 8, 4.50, 2.00);

-- 4. Insert Sample Transactions
INSERT INTO transactions (
    transaction_id, transaction_date, customer_id, product_id, quantity, unit_price, store_location, is_holiday,
    product_name, category, cost_price, sales_amount, cogs, profit, profit_margin, day_of_week, month, quarter, week_number, customer_segment
) VALUES
('TXN00001', '2025-01-20 10:15:00', 'CUST0001', 'PROD001', 2, 2.50, 'Downtown Pharmacy', 'No', 
 'Paracetamol 500mg (Tablets)', 'Analgesics', 1.50, 5.00, 3.00, 2.00, 40.00, 'Monday', 'January', 'Q1', 4, 'Regular'),
('TXN00002', '2025-02-15 14:30:00', 'CUST0002', 'PROD003', 1, 18.00, 'Suburban Wellness Center', 'No', 
 'Atorvastatin 20mg (Tablets)', 'Cardiologics', 12.00, 18.00, 12.00, 6.00, 33.33, 'Saturday', 'February', 'Q1', 7, 'Regular'),
('TXN00003', '2025-03-12 11:45:00', 'CUST0003', 'PROD002', 3, 7.50, 'Metro Pharmacy Hub', 'No', 
 'Amoxicillin 250mg (Capsules)', 'Antibiotics', 5.00, 22.50, 15.00, 7.50, 33.33, 'Wednesday', 'March', 'Q1', 11, 'Regular'),
('TXN00004', '2025-04-25 17:00:00', 'CUST0004', 'PROD004', 5, 3.20, 'Eastside Medical Pharmacy', 'No', 
 'Metformin 500mg (Tablets)', 'Antidiabetics', 2.00, 16.00, 10.00, 6.00, 37.50, 'Friday', 'April', 'Q2', 17, 'Regular');
