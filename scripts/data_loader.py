"""
Pharmacy Sales & Inventory Data Loader
Loads and validates raw datasets against defined schemas.
Generates schema validation reports.
"""

import os
import logging
from datetime import datetime
import pandas as pd
from typing import Dict, List, Tuple, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Expected schemas for raw tables
EXPECTED_SCHEMAS = {
    'customers': {
        'required_cols': ['customer_id', 'customer_name', 'email', 'gender', 'age', 'store_location', 'registration_date'],
        'types': {
            'customer_id': 'object',
            'customer_name': 'object',
            'email': 'object',
            'gender': 'object',
            'age': 'float64',
            'store_location': 'object',
            'registration_date': 'object'
        }
    },
    'products': {
        'required_cols': ['product_id', 'product_name', 'category', 'cost_price', 'retail_price'],
        'types': {
            'product_id': 'object',
            'product_name': 'object',
            'category': 'object',
            'cost_price': 'float64',
            'retail_price': 'float64'
        }
    },
    'inventory': {
        'required_cols': ['product_id', 'current_stock', 'reorder_level', 'safety_stock', 'lead_time_days', 'avg_daily_sales'],
        'types': {
            'product_id': 'object',
            'current_stock': 'int64',
            'reorder_level': 'int64',
            'safety_stock': 'int64',
            'lead_time_days': 'int64',
            'avg_daily_sales': 'float64'
        }
    },
    'transactions': {
        'required_cols': ['transaction_id', 'transaction_date', 'customer_id', 'product_id', 'quantity', 'unit_price', 'store_location', 'is_holiday'],
        'types': {
            'transaction_id': 'object',
            'transaction_date': 'object',
            'customer_id': 'object',
            'product_id': 'object',
            'quantity': 'float64',
            'unit_price': 'float64',
            'store_location': 'object',
            'is_holiday': 'object'
        }
    }
}

def load_file(file_path: str) -> Optional[pd.DataFrame]:
    """Loads CSV or JSON files into a Pandas DataFrame."""
    logger.info(f"Attempting to load file: {file_path}")
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return None
        
    _, ext = os.path.splitext(file_path)
    try:
        if ext.lower() == '.csv':
            df = pd.read_csv(file_path)
            logger.info(f"Successfully loaded CSV with {len(df)} rows.")
            return df
        elif ext.lower() == '.json':
            df = pd.read_json(file_path)
            logger.info(f"Successfully loaded JSON with {len(df)} rows.")
            return df
        else:
            logger.error(f"Unsupported file format: {ext}")
            return None
    except Exception as e:
        logger.error(f"Error loading file {file_path}: {str(e)}")
        return None

def validate_schema(df: pd.DataFrame, table_name: str) -> Tuple[bool, List[str]]:
    """Validates if the dataframe matches expected schema columns and types."""
    logger.info(f"Validating schema for table: {table_name}")
    if table_name not in EXPECTED_SCHEMAS:
        return False, [f"Table '{table_name}' is not defined in expected schemas."]
        
    errors = []
    schema = EXPECTED_SCHEMAS[table_name]
    required_cols = schema['required_cols']
    expected_types = schema['types']
    
    # Check column names
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        errors.append(f"Missing required columns: {missing_cols}")
        
    # Check data types (only for columns that exist)
    for col in df.columns:
        if col in expected_types:
            actual_type = str(df[col].dtype)
            expected_type = expected_types[col]
            # Perform soft matching for datatypes
            if expected_type == 'int64' and not ('int' in actual_type or 'float' in actual_type):
                errors.append(f"Column '{col}' type mismatch. Expected numerical type, got '{actual_type}'")
            elif expected_type == 'float64' and not ('float' in actual_type or 'int' in actual_type):
                errors.append(f"Column '{col}' type mismatch. Expected numerical type, got '{actual_type}'")
            elif expected_type == 'object' and not (actual_type == 'object' or actual_type.startswith('str') or actual_type == 'category'):
                errors.append(f"Column '{col}' type mismatch. Expected object/string type, got '{actual_type}'")

    is_valid = len(errors) == 0
    if is_valid:
        logger.info(f"Schema for {table_name} is VALID.")
    else:
        logger.warning(f"Schema for {table_name} is INVALID with {len(errors)} errors.")
        
    return is_valid, errors

def generate_validation_report(validation_results: Dict[str, Tuple[bool, List[str]]], report_path: str) -> None:
    """Generates a text report summarizing the schema validation outcomes."""
    logger.info(f"Writing schema validation report to {report_path}")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w') as f:
        f.write("==================================================\n")
        f.write("         SCHEMA VALIDATION REPORT\n")
        f.write(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("==================================================\n\n")
        
        all_passed = True
        for table, (passed, errors) in validation_results.items():
            status = "PASSED" if passed else "FAILED"
            f.write(f"Table: {table} -> Status: {status}\n")
            if not passed:
                all_passed = False
                f.write("Errors:\n")
                for err in errors:
                    f.write(f"  - {err}\n")
            f.write("-" * 50 + "\n")
            
        f.write("\nSummary:\n")
        if all_passed:
            f.write("All tables validated successfully. Pipeline ready for cleaning.\n")
        else:
            f.write("Schema issues found. Check error messages above before running ETL pipeline.\n")

if __name__ == '__main__':
    # Test loading files if executed directly
    raw_dir = 'data/raw'
    val_results = {}
    for table in EXPECTED_SCHEMAS.keys():
        path = os.path.join(raw_dir, f"{table}.csv")
        df = load_file(path)
        if df is not None:
            passed, errors = validate_schema(df, table)
            val_results[table] = (passed, errors)
        else:
            val_results[table] = (False, [f"File {path} could not be loaded."])
            
    generate_validation_report(val_results, 'reports/schema_validation_report.txt')
