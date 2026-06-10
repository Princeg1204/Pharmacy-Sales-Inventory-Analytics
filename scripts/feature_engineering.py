"""
Pharmacy Sales & Inventory Feature Engineering
Calculates sales & revenue, inventory, product performance, customer, and time-based metrics.
Outputs enriched tables:
- processed_pharmacy_data.csv (enriched transaction lines)
- engineered_products.csv
- engineered_customers.csv
- engineered_inventory.csv
"""

import os
import logging
import pandas as pd
import numpy as np
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FeatureEngineer:
    def __init__(self, processed_dir: str = 'data/processed'):
        self.processed_dir = processed_dir
        
    def load_cleaned_data(self) -> tuple:
        """Loads cleaned CSV files from data/processed/."""
        logger.info("Loading cleaned datasets for feature engineering...")
        cust = pd.read_csv(os.path.join(self.processed_dir, 'cleaned_customers.csv'))
        prod = pd.read_csv(os.path.join(self.processed_dir, 'cleaned_products.csv'))
        inv = pd.read_csv(os.path.join(self.processed_dir, 'cleaned_inventory.csv'))
        txns = pd.read_csv(os.path.join(self.processed_dir, 'cleaned_transactions.csv'))
        
        # Ensure correct date parsing
        txns['transaction_date'] = pd.to_datetime(txns['transaction_date'])
        cust['registration_date'] = pd.to_datetime(cust['registration_date'])
        
        return cust, prod, inv, txns

    def engineer_time_features(self, txns: pd.DataFrame) -> pd.DataFrame:
        """Extracts time-based features from transaction date."""
        logger.info("Engineering time-based features...")
        txns['Day_of_Week'] = txns['transaction_date'].dt.day_name()
        txns['Month'] = txns['transaction_date'].dt.month_name()
        txns['Quarter'] = txns['transaction_date'].dt.quarter.apply(lambda q: f"Q{q}")
        txns['Week_Number'] = txns['transaction_date'].dt.isocalendar().week
        # is_holiday is already present from generation, but we ensure proper formatting
        txns['is_holiday'] = txns['is_holiday'].fillna("No")
        return txns

    def run_feature_engineering(self):
        """Runs the entire feature engineering pipeline."""
        logger.info("=== STARTING FEATURE ENGINEERING ===")
        
        cust, prod, inv, txns = self.load_cleaned_data()
        
        # 1. SALES & REVENUE METRICS
        logger.info("Calculating transactional sales and revenue metrics...")
        # Merge transactions with product prices to get cost_price
        txns_merged = txns.merge(prod[['product_id', 'product_name', 'category', 'cost_price']], on='product_id', how='left')
        
        # Calculate Sales Amount, Cost of Goods Sold (COGS), Profit, and Margin
        txns_merged['Sales_Amount'] = txns_merged['quantity'] * txns_merged['unit_price']
        txns_merged['COGS'] = txns_merged['quantity'] * txns_merged['cost_price']
        txns_merged['Profit'] = txns_merged['Sales_Amount'] - txns_merged['COGS']
        txns_merged['Profit_Margin'] = np.where(
            txns_merged['Sales_Amount'] > 0, 
            (txns_merged['Profit'] / txns_merged['Sales_Amount']) * 100, 
            0.0
        )
        
        # Add Time-based features
        txns_merged = self.engineer_time_features(txns_merged)
        
        # 2. CUSTOMER METRICS & SEGMENTATION
        logger.info("Calculating customer metrics and segments...")
        cust_clv = txns_merged.groupby('customer_id')['Profit'].sum().reset_index()
        cust_clv.rename(columns={'Profit': 'Customer_Lifetime_Value'}, inplace=True)
        
        cust_orders = txns_merged.groupby('customer_id')['transaction_id'].nunique().reset_index()
        cust_orders.rename(columns={'transaction_id': 'Total_Orders'}, inplace=True)
        
        cust_rev = txns_merged.groupby('customer_id')['Sales_Amount'].sum().reset_index()
        cust_rev.rename(columns={'Sales_Amount': 'Total_Revenue'}, inplace=True)
        
        cust_last_date = txns_merged.groupby('customer_id')['transaction_date'].max().reset_index()
        cust_last_date.rename(columns={'transaction_date': 'Last_Purchase_Date'}, inplace=True)
        
        # Merge customer features
        cust_features = cust.merge(cust_clv, on='customer_id', how='left')
        cust_features = cust_features.merge(cust_orders, on='customer_id', how='left')
        cust_features = cust_features.merge(cust_rev, on='customer_id', how='left')
        cust_features = cust_features.merge(cust_last_date, on='customer_id', how='left')
        
        # Impute missing values for inactive customers (fill with 0)
        cust_features['Customer_Lifetime_Value'] = cust_features['Customer_Lifetime_Value'].fillna(0.0)
        cust_features['Total_Orders'] = cust_features['Total_Orders'].fillna(0).astype(int)
        cust_features['Total_Revenue'] = cust_features['Total_Revenue'].fillna(0.0)
        cust_features['Average_Order_Value'] = np.where(
            cust_features['Total_Orders'] > 0, 
            cust_features['Total_Revenue'] / cust_features['Total_Orders'], 
            0.0
        )
        
        # RFM Customer Segments:
        # VIP (CLV > 90th percentile)
        # Regular (between 10th and 90th percentile)
        # At-Risk (< 10th percentile)
        clv_10 = cust_features['Customer_Lifetime_Value'].quantile(0.10)
        clv_90 = cust_features['Customer_Lifetime_Value'].quantile(0.90)
        
        def segment_customer(clv):
            if clv > clv_90:
                return 'VIP'
            elif clv < clv_10:
                return 'At-Risk'
            else:
                return 'Regular'
                
        cust_features['Customer_Segment'] = cust_features['Customer_Lifetime_Value'].apply(segment_customer)
        cust_features['Customer_Segment'] = cust_features['Customer_Segment'].astype('category')
        
        # Calculate Repeat Purchase Rate
        total_cust_with_orders = (cust_features['Total_Orders'] > 0).sum()
        repeat_cust = (cust_features['Total_Orders'] > 1).sum()
        repeat_purchase_rate = (repeat_cust / total_cust_with_orders * 100) if total_cust_with_orders > 0 else 0.0
        logger.info(f"Repeat Purchase Rate calculated: {repeat_purchase_rate:.2f}%")
        
        # Map Customer Segment back to transactions for unified table
        txns_merged = txns_merged.merge(cust_features[['customer_id', 'Customer_Segment']], on='customer_id', how='left')
        
        # 3. PRODUCT PERFORMANCE & INVENTORY TURNOVER METRICS
        logger.info("Calculating product performance metrics...")
        
        # Total Sales frequency and revenue by product
        prod_metrics = txns_merged.groupby('product_id').agg(
            Product_Revenue=('Sales_Amount', 'sum'),
            Product_COGS=('COGS', 'sum'),
            Sales_Frequency=('transaction_id', 'count')
        ).reset_index()
        
        # Add active time period for Product Demand Score
        total_period_days = (txns_merged['transaction_date'].max() - txns_merged['transaction_date'].min()).days
        if total_period_days == 0:
            total_period_days = 1
            
        prod_metrics['Product_Demand_Score'] = (prod_metrics['Sales_Frequency'] / total_period_days) * 100
        
        # Total overall revenue for revenue contribution
        total_revenue = prod_metrics['Product_Revenue'].sum()
        prod_metrics['Revenue_Contribution'] = (prod_metrics['Product_Revenue'] / total_revenue) * 100
        
        # ABC Classification (A: top 20% revenue contribution, B: middle 30%, C: bottom 50%)
        # Let's sort descending by revenue and compute cumulative revenue percentage
        prod_metrics = prod_metrics.sort_values(by='Product_Revenue', ascending=False).reset_index(drop=True)
        prod_metrics['Cumulative_Revenue_Pct'] = prod_metrics['Product_Revenue'].cumsum() / total_revenue * 100
        
        # Classification according to typical business rules:
        # A: Top 20% of products by count (often contributes ~80% of sales)
        # B: Next 30% of products by count (often contributes ~15% of sales)
        # C: Remaining 50% of products (often contributes ~5% of sales)
        # Alternatively, Class A = up to 80% cum. revenue, B = 80-95%, C = 95-100%.
        # Prompt: ABC_Classification = "A" (top 20% revenue), "B" (middle 30%), "C" (bottom 50%)
        # We will implement it based on product count percentile:
        num_prods = len(prod_metrics)
        def get_abc_class(index):
            pct = (index + 1) / num_prods * 100
            if pct <= 20:
                return 'A'
            elif pct <= 50:
                return 'B'
            else:
                return 'C'
        
        prod_metrics['ABC_Classification'] = [get_abc_class(idx) for idx in prod_metrics.index]
        
        # Join product cost and current stock to calculate Inventory Turnover
        # Inventory Turnover = Annual_COGS / Average_Inventory_Value
        # Average inventory value = current stock * cost price (as a proxy, since average inventory is stable in our generator)
        prod_inventory = inv.merge(prod_metrics, on='product_id', how='left')
        prod_inventory['Inventory_Value'] = prod_inventory['current_stock'] * prod_inventory['cost_price']
        
        # Annualized COGS (scale COGS to 12 months since our period is 15 months)
        scale_to_annual = 365.0 / total_period_days
        prod_inventory['Annual_COGS'] = prod_inventory['Product_COGS'].fillna(0.0) * scale_to_annual
        
        # Inventory Turnover Ratio
        # Avoid division by zero
        prod_inventory['Inventory_Turnover'] = np.where(
            prod_inventory['Inventory_Value'] > 0,
            prod_inventory['Annual_COGS'] / prod_inventory['Inventory_Value'],
            prod_inventory['Annual_COGS'] / 1.0 # fallback if no stock value
        )
        
        # Label Fast & Slow moving products based on Inventory Turnover percentiles
        turnover_25 = prod_inventory['Inventory_Turnover'].quantile(0.25)
        turnover_75 = prod_inventory['Inventory_Turnover'].quantile(0.75)
        
        prod_inventory['Fast_Moving_Product'] = np.where(prod_inventory['Inventory_Turnover'] > turnover_75, 'Yes', 'No')
        prod_inventory['Slow_Moving_Product'] = np.where(prod_inventory['Inventory_Turnover'] < turnover_25, 'Yes', 'No')
        
        # Merge product performance and movement status back into products table
        prod_features = prod.merge(prod_inventory[['product_id', 'Inventory_Turnover', 'Fast_Moving_Product', 'Slow_Moving_Product', 'Product_Demand_Score', 'Revenue_Contribution', 'ABC_Classification']], on='product_id', how='left')
        
        # 4. INVENTORY STATUS & ALERTS
        logger.info("Calculating inventory health and reorder metrics...")
        
        # Days to Stockout = Current_Stock / Average_Daily_Sales
        # Avoid division by zero
        inv['Days_to_Stockout'] = np.where(
            inv['avg_daily_sales'] > 0,
            inv['current_stock'] / inv['avg_daily_sales'],
            999.0
        )
        
        # Reorder Point = (Average_Daily_Demand * Lead_Time_Days) + Safety_Stock
        inv['Reorder_Point'] = (inv['avg_daily_sales'] * inv['lead_time_days']) + inv['safety_stock']
        
        # Stock Status: "Critical" (<10 units), "Low" (10-50), "Optimal" (>50)
        def get_stock_status(stock):
            if stock < 10:
                return 'Critical'
            elif stock <= 50:
                return 'Low'
            else:
                return 'Optimal'
                
        inv['Stock_Status'] = inv['current_stock'].apply(get_stock_status)
        inv['Stock_Status'] = inv['Stock_Status'].astype('category')
        
        # 5. OUTPUTS
        logger.info("Saving all engineered datasets...")
        # Save processed unified transactions table
        txns_merged.to_csv(os.path.join(self.processed_dir, 'processed_pharmacy_data.csv'), index=False)
        logger.info(f"Saved processed_pharmacy_data.csv with shape {txns_merged.shape}")
        
        # Save engineered customer metadata
        cust_features.to_csv(os.path.join(self.processed_dir, 'engineered_customers.csv'), index=False)
        logger.info(f"Saved engineered_customers.csv with shape {cust_features.shape}")
        
        # Save engineered product metadata
        prod_features.to_csv(os.path.join(self.processed_dir, 'engineered_products.csv'), index=False)
        logger.info(f"Saved engineered_products.csv with shape {prod_features.shape}")
        
        # Save engineered inventory metadata
        inv.to_csv(os.path.join(self.processed_dir, 'engineered_inventory.csv'), index=False)
        logger.info(f"Saved engineered_inventory.csv with shape {inv.shape}")
        
        logger.info("=== FEATURE ENGINEERING COMPLETE ===")

if __name__ == '__main__':
    fe = FeatureEngineer()
    fe.run_feature_engineering()
