"""
Pharmacy Sales & Inventory Data Generator
Generates realistic, raw datasets with deliberate anomalies to test the ETL pipeline.
Includes:
- 5,000+ Customers (customers.csv)
- 150+ Products across 10 categories (products.csv)
- Inventory status (inventory.csv)
- 50,000+ Transactions over 15 months with seasonality & outliers (transactions.csv)
"""

import os
import random
import logging
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Constants
NUM_CUSTOMERS = 5200
NUM_PRODUCTS = 160
NUM_TRANSACTIONS = 53000
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2026, 3, 31)

# Categories and standard list of active substances
PRODUCT_CATEGORIES = {
    'Analgesics': ['Paracetamol', 'Ibuprofen', 'Aspirin', 'Tramadol', 'Naproxen', 'Diclofenac', 'Mefenamic Acid'],
    'Antibiotics': ['Amoxicillin', 'Azithromycin', 'Ciprofloxacin', 'Cephalexin', 'Doxycycline', 'Clarithromycin'],
    'Cardiologics': ['Atorvastatin', 'Amlodipine', 'Lisinopril', 'Metoprolol', 'Losartan', 'Ramipril', 'Clopidogrel'],
    'Antidiabetics': ['Metformin', 'Glimepiride', 'Sitagliptin', 'Gliclazide', 'Pioglitazone', 'Dapagliflozin'],
    'Gastrointestinals': ['Omeprazole', 'Pantoprazole', 'Ranitidine', 'Domperidone', 'Esomeprazole', 'Loperamide'],
    'Antihistamines': ['Cetirizine', 'Loratadine', 'Fexofenadine', 'Levocetirizine', 'Montelukast'],
    'Vitamins': ['Vitamin D3', 'Vitamin C', 'Multivitamin', 'Calcium Carbonate', 'B-Complex', 'Zinc Sulfate'],
    'Dermatologicals': ['Hydrocortisone Cream', 'Clotrimazole Cream', 'Ketoconazole Shampoo', 'Salicylic Acid Ointment'],
    'Respiratory': ['Salbutamol Inhaler', 'Fluticasone Spray', 'Levosalbutamol', 'Ambroxol Syrup', 'Dextromethorphan'],
    'Neurologicals': ['Gabapentin', 'Pregabalin', 'Sertraline', 'Escitalopram', 'Alprazolam', 'Clonazepam']
}

STORE_LOCATIONS = ['Downtown Pharmacy', 'Suburban Wellness Center', 'Metro Pharmacy Hub', 'Eastside Medical Pharmacy']
GENDERS = ['Male', 'Female', 'Other']

def generate_customers() -> pd.DataFrame:
    """Generates synthetic customer demographic data."""
    logger.info("Generating customer dataset...")
    first_names = ['John', 'Mary', 'Robert', 'Patricia', 'Michael', 'Linda', 'William', 'Elizabeth', 'David', 'Barbara',
                   'Richard', 'Susan', 'Joseph', 'Jessica', 'Thomas', 'Sarah', 'Charles', 'Karen', 'Christopher', 'Nancy',
                   'Amit', 'Priya', 'Raj', 'Anjali', 'Vikram', 'Neha', 'Sanjay', 'Deepa', 'Arjun', 'Kavita']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
                  'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
                  'Sharma', 'Patel', 'Verma', 'Gupta', 'Mehta', 'Singh', 'Reddy', 'Rao', 'Nair', 'Joshi']

    customers = []
    for i in range(1, NUM_CUSTOMERS + 1):
        cust_id = f"CUST{i:04d}"
        fname = random.choice(first_names)
        lname = random.choice(last_names)
        name = f"{fname} {lname}"
        email = f"{fname.lower()}.{lname.lower()}{random.randint(10, 99)}@pharmmail.com"
        gender = random.choice(GENDERS)
        
        # Age distribution: slightly older for pharmacy customer base
        age = int(np.clip(np.random.normal(52, 18), 18, 90))
        store = random.choice(STORE_LOCATIONS)
        
        # Registration date in the last 2 years
        days_ago = random.randint(0, 730)
        reg_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        customers.append({
            'customer_id': cust_id,
            'customer_name': name,
            'email': email,
            'gender': gender,
            'age': age,
            'store_location': store,
            'registration_date': reg_date
        })
    
    df = pd.DataFrame(customers)
    
    # Introduce some missing ages and genders (approx 1.5% nulls)
    df.loc[df.sample(frac=0.015).index, 'age'] = np.nan
    df.loc[df.sample(frac=0.015).index, 'gender'] = np.nan
    
    return df

def generate_products() -> pd.DataFrame:
    """Generates synthetic product inventory details with pricing."""
    logger.info("Generating product dataset...")
    products = []
    prod_idx = 1
    
    for category, drug_list in PRODUCT_CATEGORIES.items():
        for drug in drug_list:
            # Let's generate multiple strengths/forms for each substance
            forms = ['Tablets', 'Capsules', 'Syrup' if category in ['Respiratory', 'Vitamins', 'Analgesics'] else 'Cream' if category == 'Dermatologicals' else 'Tablets']
            strengths = ['10mg', '20mg', '100mg', '500mg'] if category != 'Dermatologicals' else ['1%', '2%', '0.05%']
            
            # Filter form/strength combination
            selected_forms = random.sample(forms, min(len(forms), random.randint(1, 2)))
            for f in selected_forms:
                s = random.choice(strengths)
                prod_id = f"PROD{prod_idx:03d}"
                prod_name = f"{drug} {s} ({f})"
                
                # Pricing model based on category
                if category == 'Vitamins':
                    cost = round(random.uniform(2.0, 15.0), 2)
                    margin = random.uniform(0.35, 0.60) # Higher margin
                elif category in ['Cardiologics', 'Antidiabetics']:
                    cost = round(random.uniform(5.0, 45.0), 2)
                    margin = random.uniform(0.15, 0.30) # High volume, lower margin
                elif category == 'Antibiotics':
                    cost = round(random.uniform(10.0, 60.0), 2)
                    margin = random.uniform(0.25, 0.40)
                else:
                    cost = round(random.uniform(3.0, 25.0), 2)
                    margin = random.uniform(0.20, 0.45)
                
                retail = round(cost * (1.0 + margin), 2)
                
                products.append({
                    'product_id': prod_id,
                    'product_name': prod_name,
                    'category': category,
                    'cost_price': cost,
                    'retail_price': retail
                })
                prod_idx += 1
                if prod_idx > NUM_PRODUCTS:
                    break
        if prod_idx > NUM_PRODUCTS:
            break
            
    # If we need more products to reach target count
    while len(products) < NUM_PRODUCTS:
        category = random.choice(list(PRODUCT_CATEGORIES.keys()))
        drug = random.choice(PRODUCT_CATEGORIES[category])
        prod_id = f"PROD{prod_idx:03d}"
        prod_name = f"{drug} {random.choice(['10mg', '500mg'])} (Tablets)"
        cost = round(random.uniform(5.0, 30.0), 2)
        retail = round(cost * random.uniform(1.2, 1.5), 2)
        products.append({
            'product_id': prod_id,
            'product_name': prod_name,
            'category': category,
            'cost_price': cost,
            'retail_price': retail
        })
        prod_idx += 1
        
    return pd.DataFrame(products)

def generate_inventory(products_df: pd.DataFrame) -> pd.DataFrame:
    """Generates synthetic stock levels matching products."""
    logger.info("Generating inventory dataset...")
    inventory = []
    for _, row in products_df.iterrows():
        p_id = row['product_id']
        category = row['category']
        
        # High turnover categories like Analgesics have higher daily sales
        if category in ['Analgesics', 'Antihistamines', 'Vitamins']:
            avg_daily = round(random.uniform(4.0, 15.0), 2)
        else:
            avg_daily = round(random.uniform(0.5, 4.0), 2)
            
        lead_time = random.randint(3, 10)
        safety_stock = int(avg_daily * random.uniform(2, 5))
        reorder_level = max(15, int((avg_daily * lead_time) + safety_stock))
        
        # Stock status: let some products be critical, some low, most optimal
        status_roll = random.random()
        if status_roll < 0.05: # 5% out of stock/critical
            current_stock = random.randint(0, 9)
        elif status_roll < 0.15: # 10% low stock
            current_stock = random.randint(10, reorder_level)
        else: # optimal stock
            current_stock = random.randint(reorder_level + 1, int(avg_daily * 45))
            
        inventory.append({
            'product_id': p_id,
            'current_stock': current_stock,
            'reorder_level': reorder_level,
            'safety_stock': safety_stock,
            'lead_time_days': lead_time,
            'avg_daily_sales': avg_daily,
            'cost_price': row['cost_price'] # Include for SQL queries joins
        })
        
    return pd.DataFrame(inventory)

def generate_transactions(cust_df: pd.DataFrame, prod_df: pd.DataFrame) -> pd.DataFrame:
    """Generates 50K+ transactions over 15 months with seasonal patterns and noise."""
    logger.info("Generating transaction dataset...")
    
    customers_list = cust_df['customer_id'].tolist()
    products_list = prod_df['product_id'].tolist()
    product_map = prod_df.set_index('product_id').to_dict('index')
    
    transactions = []
    
    # Pre-build daily probabilities to model seasonality
    # Flu season: Nov, Dec, Jan, Feb
    # Allergy season: Mar, Apr, May
    # Monday and Friday are peak sales days
    
    current_date = START_DATE
    delta_days = (END_DATE - START_DATE).days
    
    logger.info(f"Simulating sales from {START_DATE.date()} to {END_DATE.date()} ({delta_days} days)")
    
    # Generate transactions day by day to model trends
    dates_list = []
    day_txn_counts = []
    
    for day in range(delta_days + 1):
        date_val = START_DATE + timedelta(days=day)
        month = date_val.month
        weekday = date_val.weekday() # 0 = Monday, 6 = Sunday
        
        # Base transaction count per day
        base_txn = 100
        
        # Seasonality factors
        season_mult = 1.0
        if month in [11, 12, 1]:  # Winter peak
            season_mult = 1.35
        elif month in [4, 5]:  # Spring allergy
            season_mult = 1.2
        elif month in [7, 8]:  # Summer dip
            season_mult = 0.85
            
        # Weekly pattern
        weekday_mult = 1.0
        if weekday in [0, 4]:  # Monday, Friday
            weekday_mult = 1.25
        elif weekday == 6:  # Sunday
            weekday_mult = 0.6
            
        # Random daily variation
        random_mult = np.random.normal(1.0, 0.1)
        
        txn_count = int(base_txn * season_mult * weekday_mult * random_mult)
        day_txn_counts.append(txn_count)
        dates_list.append(date_val)
        
    # Scale counts to target approximately NUM_TRANSACTIONS
    total_simulated = sum(day_txn_counts)
    scale_factor = NUM_TRANSACTIONS / total_simulated
    day_txn_counts = [int(cnt * scale_factor) for cnt in day_txn_counts]
    
    txn_id_counter = 1
    
    # List of holidays (approximate dates in US/India)
    holidays = [
        '2025-01-01', '2025-05-26', '2025-07-04', '2025-09-01', '2025-11-27', '2025-12-25',
        '2026-01-01'
    ]
    
    for i, date_val in enumerate(dates_list):
        count = day_txn_counts[i]
        date_str = date_val.strftime('%Y-%m-%d %H:%M:%S')
        is_holiday = 'Yes' if date_val.strftime('%Y-%m-%d') in holidays else 'No'
        
        for _ in range(count):
            cust_id = random.choice(customers_list)
            prod_id = random.choice(products_list)
            prod_info = product_map[prod_id]
            category = prod_info['category']
            
            # Determine quantity
            # High-volume items like Analgesics / Vitamins might be bought in larger quantities
            if category in ['Analgesics', 'Vitamins']:
                qty = int(np.clip(np.random.negative_binomial(3, 0.6) + 1, 1, 10))
            else:
                qty = int(np.clip(np.random.negative_binomial(2, 0.7) + 1, 1, 4))
                
            unit_price = prod_info['retail_price']
            
            # Apply slight price variation/discount on some sales (e.g. 15% of transactions get 5-10% discount)
            if random.random() < 0.15:
                discount = random.choice([0.05, 0.10])
                unit_price = round(unit_price * (1.0 - discount), 2)
                
            store_loc = random.choice(STORE_LOCATIONS)
            
            transactions.append({
                'transaction_id': f"TXN{txn_id_counter:05d}",
                'transaction_date': date_str,
                'customer_id': cust_id,
                'product_id': prod_id,
                'quantity': qty,
                'unit_price': unit_price,
                'store_location': store_loc,
                'is_holiday': is_holiday
            })
            txn_id_counter += 1
            
    df = pd.DataFrame(transactions)
    
    logger.info(f"Generated {len(df)} initial transactions.")
    
    # Introduce duplicate rows (approx 200 duplicates)
    logger.info("Introducing duplicate rows...")
    duplicates = df.sample(n=200, replace=True).copy()
    # Modify transaction ID slightly or keep same to test dedup
    df = pd.concat([df, duplicates], ignore_index=True)
    
    # Introduce nulls in critical columns
    logger.info("Introducing missing values (nulls)...")
    
    # 1. Quantity missing (~1%)
    qty_nulls = df.sample(frac=0.01).index
    df.loc[qty_nulls, 'quantity'] = np.nan
    
    # 2. Unit Price missing (~1%)
    price_nulls = df.sample(frac=0.01).index
    df.loc[price_nulls, 'unit_price'] = np.nan
    
    # 3. Transaction Date missing (~0.5%)
    date_nulls = df.sample(frac=0.005).index
    df.loc[date_nulls, 'transaction_date'] = np.nan
    
    # 4. Create rows with > 30% missing values (e.g., missing ID, date, quantity and price)
    # Since we have 8 columns, 3 missing columns is > 30% (3/8 = 37.5%)
    logger.info("Introducing highly corrupted rows (>30% missing)...")
    corrupt_indices = df.sample(n=120).index
    df.loc[corrupt_indices, ['quantity', 'unit_price', 'customer_id']] = np.nan
    
    # Introduce outliers
    logger.info("Introducing outliers...")
    
    # 1. Large quantity outlier (pricing/bulk error)
    qty_outlier_idx = df.sample(n=150).index
    df.loc[qty_outlier_idx, 'quantity'] = df.loc[qty_outlier_idx, 'quantity'].apply(lambda x: random.randint(150, 400))
    
    # 2. Unit price outlier (pricing/data-entry decimal error)
    price_outlier_idx = df.sample(n=80).index
    df.loc[price_outlier_idx, 'unit_price'] = df.loc[price_outlier_idx, 'unit_price'].apply(lambda p: round(p * 10.0 if not np.isnan(p) else 150.0, 2))
    
    # Shuffle the dataset to mix things up
    df = df.sample(frac=1.0).reset_index(drop=True)
    
    return df

def main():
    """Generates all datasets and writes them to the data/raw/ directory."""
    os.makedirs('data/raw', exist_ok=True)
    
    logger.info("--- STARTING DATA GENERATION ---")
    
    cust_df = generate_customers()
    cust_df.to_csv('data/raw/customers.csv', index=False)
    logger.info(f"Saved customers.csv with shape {cust_df.shape}")
    
    prod_df = generate_products()
    prod_df.to_csv('data/raw/products.csv', index=False)
    logger.info(f"Saved products.csv with shape {prod_df.shape}")
    
    inv_df = generate_inventory(prod_df)
    inv_df.to_csv('data/raw/inventory.csv', index=False)
    logger.info(f"Saved inventory.csv with shape {inv_df.shape}")
    
    tx_df = generate_transactions(cust_df, prod_df)
    tx_df.to_csv('data/raw/transactions.csv', index=False)
    logger.info(f"Saved transactions.csv with shape {tx_df.shape}")
    
    logger.info("--- DATA GENERATION COMPLETE ---")

if __name__ == '__main__':
    main()
