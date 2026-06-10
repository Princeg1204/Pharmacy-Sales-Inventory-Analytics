"""
Pharmacy Sales & Inventory Data Cleaner
Implements the cleaning pipeline for the pharmacy retail datasets:
- Deduplication
- Drops highly corrupted rows (>30% missing values)
- Imputes missing values (median for numeric, mode/Unknown for categorical, ffill for dates)
- Capping outliers using the IQR method (5th/95th percentiles)
- Text field standardization (strip, lowercase)
- Data type conversions
- Outputs a comprehensive Data Quality Report
"""

import os
import logging
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataCleaner:
    def __init__(self, raw_dir: str = 'data/raw', processed_dir: str = 'data/processed'):
        self.raw_dir = raw_dir
        self.processed_dir = processed_dir
        os.makedirs(self.processed_dir, exist_ok=True)
        self.quality_metrics = []

    def log_quality_metric(self, table: str, operation: str, before_val: Any, after_val: Any, details: str = ""):
        """Logs modifications for the Data Quality Report."""
        self.quality_metrics.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'table': table,
            'operation': operation,
            'metric_before': before_val,
            'metric_after': after_val,
            'details': details
        })

    def clean_customers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cleans the customer dataset."""
        logger.info("Cleaning customers dataset...")
        table_name = "customers"
        initial_len = len(df)
        
        # 1. Remove duplicates
        df = df.drop_duplicates().copy()
        self.log_quality_metric(table_name, "Deduplication", initial_len, len(df), f"Removed {initial_len - len(df)} duplicate rows.")
        
        # 2. Check for rows with >30% missing values
        # Since customers has 7 columns, 30% is 2.1 cols. Drop rows with >=3 missing values.
        missing_count = df.isnull().sum(axis=1)
        corrupt_rows = (missing_count / df.shape[1]) > 0.3
        num_dropped = corrupt_rows.sum()
        df = df[~corrupt_rows].copy()
        self.log_quality_metric(table_name, "Drop Corrupt Rows (>30% missing)", initial_len - (initial_len - len(df)), len(df), f"Dropped {num_dropped} rows.")

        # 3. Handle missing values
        # Age (numeric) -> Median
        age_null_before = df['age'].isnull().sum()
        age_median = df['age'].median()
        df['age'] = df['age'].fillna(age_median)
        self.log_quality_metric(table_name, "Impute Missing Age", age_null_before, 0, f"Imputed with median age: {age_median:.1f}")
        
        # Gender (categorical) -> Mode or "Unknown"
        gender_null_before = df['gender'].isnull().sum()
        gender_mode = df['gender'].mode()[0] if not df['gender'].mode().empty else "Unknown"
        df['gender'] = df['gender'].fillna("Unknown")
        self.log_quality_metric(table_name, "Impute Missing Gender", gender_null_before, 0, "Imputed with 'Unknown'")

        # 4. Convert types
        df['customer_id'] = df['customer_id'].astype(str)
        df['customer_name'] = df['customer_name'].astype(str).str.strip()
        df['email'] = df['email'].astype(str).str.strip().str.lower()
        df['gender'] = df['gender'].astype('category')
        df['age'] = df['age'].astype(int)
        df['store_location'] = df['store_location'].astype(str).str.strip()
        df['registration_date'] = pd.to_datetime(df['registration_date'], errors='coerce')
        
        # Clean registration dates missing (if any) using forward fill
        reg_date_nulls = df['registration_date'].isnull().sum()
        if reg_date_nulls > 0:
            df['registration_date'] = df['registration_date'].ffill()
            self.log_quality_metric(table_name, "Impute Registration Date", reg_date_nulls, df['registration_date'].isnull().sum(), "Forward filled dates")

        logger.info(f"Finished cleaning customers. Rows: {len(df)}")
        return df

    def clean_products(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cleans the products dataset."""
        logger.info("Cleaning products dataset...")
        table_name = "products"
        initial_len = len(df)
        
        # 1. Deduplicate
        df = df.drop_duplicates().copy()
        self.log_quality_metric(table_name, "Deduplication", initial_len, len(df), "Removed duplicates")
        
        # 2. Text standardization
        df['product_id'] = df['product_id'].astype(str)
        df['product_name'] = df['product_name'].astype(str).str.strip()
        df['category'] = df['category'].astype('category')
        
        # 3. Numeric verification
        df['cost_price'] = pd.to_numeric(df['cost_price'], errors='coerce').astype(float)
        df['retail_price'] = pd.to_numeric(df['retail_price'], errors='coerce').astype(float)
        
        logger.info(f"Finished cleaning products. Rows: {len(df)}")
        return df

    def clean_inventory(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cleans the inventory dataset."""
        logger.info("Cleaning inventory dataset...")
        table_name = "inventory"
        initial_len = len(df)
        
        df = df.drop_duplicates().copy()
        self.log_quality_metric(table_name, "Deduplication", initial_len, len(df), "Removed duplicates")
        
        # Convert numeric types
        int_cols = ['current_stock', 'reorder_level', 'safety_stock', 'lead_time_days']
        for col in int_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
            
        df['avg_daily_sales'] = pd.to_numeric(df['avg_daily_sales'], errors='coerce').fillna(0.0).astype(float)
        df['product_id'] = df['product_id'].astype(str)
        
        logger.info(f"Finished cleaning inventory. Rows: {len(df)}")
        return df

    def handle_outliers_iqr(self, df: pd.DataFrame, col: str, table_name: str) -> Tuple[pd.DataFrame, int]:
        """Identifies and caps outliers at the 5th and 95th percentiles using the IQR method."""
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        outliers = (df[col] < lower_bound) | (df[col] > upper_bound)
        num_outliers = outliers.sum()
        
        p05 = df[col].quantile(0.05)
        p95 = df[col].quantile(0.95)
        
        logger.info(f"Outlier detection in {table_name}.{col}: IQR [{lower_bound:.2f}, {upper_bound:.2f}]. Outliers: {num_outliers}. Capping to [P05: {p05:.2f}, P95: {p95:.2f}]")
        
        # Cap values
        df[col] = np.where(df[col] < lower_bound, p05, df[col])
        df[col] = np.where(df[col] > upper_bound, p95, df[col])
        
        self.log_quality_metric(
            table_name, 
            f"Outlier Treatment ({col})", 
            int(num_outliers), 
            0, 
            f"Capped at 5th ({p05:.2f}) and 95th ({p95:.2f}) percentiles."
        )
        
        return df, int(num_outliers)

    def clean_transactions(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cleans the transactions dataset."""
        logger.info("Cleaning transactions dataset...")
        table_name = "transactions"
        initial_len = len(df)
        
        # 1. Remove duplicate rows
        df = df.drop_duplicates().copy()
        self.log_quality_metric(table_name, "Deduplication", initial_len, len(df), f"Removed {initial_len - len(df)} duplicate rows.")
        
        # 2. Check for rows with >30% missing values
        # transactions has 8 columns. 30% is 2.4. Drop rows with >= 3 missing values.
        missing_count = df.isnull().sum(axis=1)
        corrupt_rows = (missing_count / df.shape[1]) > 0.3
        num_dropped = corrupt_rows.sum()
        df = df[~corrupt_rows].copy()
        self.log_quality_metric(table_name, "Drop Corrupt Rows (>30% missing)", initial_len - (initial_len - len(df)), len(df), f"Dropped {num_dropped} rows.")

        # 3. Convert date column & handle missing dates with forward fill
        date_nulls_before = df['transaction_date'].isnull().sum()
        df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
        # Sort by transaction_date to forward fill chronologically
        df = df.sort_values('transaction_date').reset_index(drop=True)
        df['transaction_date'] = df['transaction_date'].ffill()
        # If any still null (e.g. first row), bfill
        df['transaction_date'] = df['transaction_date'].bfill()
        self.log_quality_metric(table_name, "Impute Missing Date (Forward Fill)", date_nulls_before, df['transaction_date'].isnull().sum(), "Forward filled transaction dates")

        # 4. Handle missing values for Numeric columns
        # Quantity -> Median
        qty_nulls_before = df['quantity'].isnull().sum()
        qty_median = df['quantity'].median()
        df['quantity'] = df['quantity'].fillna(qty_median)
        self.log_quality_metric(table_name, "Impute Missing Quantity", qty_nulls_before, 0, f"Imputed with median: {qty_median}")
        
        # Unit Price -> Median
        price_nulls_before = df['unit_price'].isnull().sum()
        price_median = df['unit_price'].median()
        df['unit_price'] = df['unit_price'].fillna(price_median)
        self.log_quality_metric(table_name, "Impute Missing Unit Price", price_nulls_before, 0, f"Imputed with median: {price_median}")

        # 5. Outlier Detection and Treatment using IQR
        df, _ = self.handle_outliers_iqr(df, 'quantity', table_name)
        df, _ = self.handle_outliers_iqr(df, 'unit_price', table_name)

        # 6. Normalization & Text Standardization
        # Normalize unit price to 0-1 range and save as a new column
        min_p = df['unit_price'].min()
        max_p = df['unit_price'].max()
        df['normalized_unit_price'] = (df['unit_price'] - min_p) / (max_p - min_p) if max_p != min_p else 0.0
        self.log_quality_metric(table_name, "Normalize Unit Price", f"[{min_p:.2f}, {max_p:.2f}]", "[0.0, 1.0]", "Min-Max normalization")

        # Standardize text columns
        df['transaction_id'] = df['transaction_id'].astype(str)
        df['customer_id'] = df['customer_id'].astype(str)
        df['product_id'] = df['product_id'].astype(str)
        df['store_location'] = df['store_location'].astype(str).str.strip()
        df['is_holiday'] = df['is_holiday'].astype(str).str.strip().str.capitalize()
        
        # Enforce positive values
        df['quantity'] = df['quantity'].abs().astype(int)
        df['unit_price'] = df['unit_price'].abs()
        
        logger.info(f"Finished cleaning transactions. Rows: {len(df)}")
        return df

    def save_quality_report(self) -> None:
        """Saves the log of quality changes to reports/data_quality_report.csv."""
        logger.info("Saving Data Quality Report...")
        df_report = pd.DataFrame(self.quality_metrics)
        df_report.to_csv('reports/data_quality_report.csv', index=False)
        logger.info("Data Quality Report saved successfully.")

    def run_cleaning_pipeline(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Runs the entire end-to-end cleaning pipeline."""
        logger.info("=== STARTING CLEANING PIPELINE ===")
        
        cust = pd.read_csv(os.path.join(self.raw_dir, 'customers.csv'))
        prod = pd.read_csv(os.path.join(self.raw_dir, 'products.csv'))
        inv = pd.read_csv(os.path.join(self.raw_dir, 'inventory.csv'))
        txns = pd.read_csv(os.path.join(self.raw_dir, 'transactions.csv'))
        
        # Clean individual files
        cust_clean = self.clean_customers(cust)
        prod_clean = self.clean_products(prod)
        inv_clean = self.clean_inventory(inv)
        txns_clean = self.clean_transactions(txns)
        
        # Save individual cleaned datasets
        cust_clean.to_csv(os.path.join(self.processed_dir, 'cleaned_customers.csv'), index=False)
        prod_clean.to_csv(os.path.join(self.processed_dir, 'cleaned_products.csv'), index=False)
        inv_clean.to_csv(os.path.join(self.processed_dir, 'cleaned_inventory.csv'), index=False)
        txns_clean.to_csv(os.path.join(self.processed_dir, 'cleaned_transactions.csv'), index=False)
        
        # Save quality report
        self.save_quality_report()
        
        logger.info("=== CLEANING PIPELINE COMPLETE ===")
        return cust_clean, prod_clean, inv_clean, txns_clean

if __name__ == '__main__':
    cleaner = DataCleaner()
    cleaner.run_cleaning_pipeline()
