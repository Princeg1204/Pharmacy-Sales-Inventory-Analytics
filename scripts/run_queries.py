"""
SQL Query Executor & Database Population Script
Populates the SQLite database with cleaned pharmacy data.
Runs all 15 analysis queries, formats output, and saves results.
"""

import os
import sqlite3
import logging
import re
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_PATH = 'pharmacy_analytics.db'
SCHEMA_PATH = 'sql/schema.sql'
QUERIES_PATH = 'sql/queries_15_analysis.sql'
PROCESSED_DIR = 'data/processed'
OUTPUT_REPORT_PATH = 'reports/sql_queries_results.txt'

def populate_database(conn: sqlite3.Connection):
    """Loads cleaned CSV data and populates SQLite database tables."""
    logger.info("Populating database tables from processed CSVs...")
    
    # 1. Customers
    cust_df = pd.read_csv(os.path.join(PROCESSED_DIR, 'cleaned_customers.csv'))
    cust_df.to_sql('customers', conn, if_exists='append', index=False)
    logger.info(f"Loaded {len(cust_df)} rows into 'customers' table.")
    
    # 2. Products
    prod_df = pd.read_csv(os.path.join(PROCESSED_DIR, 'cleaned_products.csv'))
    prod_df.to_sql('products', conn, if_exists='append', index=False)
    logger.info(f"Loaded {len(prod_df)} rows into 'products' table.")
    
    # 3. Inventory
    inv_df = pd.read_csv(os.path.join(PROCESSED_DIR, 'cleaned_inventory.csv'))
    # Align columns to inventory table schema
    inv_df.to_sql('inventory', conn, if_exists='append', index=False)
    logger.info(f"Loaded {len(inv_df)} rows into 'inventory' table.")
    
    # 4. Transactions
    tx_df = pd.read_csv(os.path.join(PROCESSED_DIR, 'processed_pharmacy_data.csv'))
    tx_df.to_sql('transactions', conn, if_exists='append', index=False)
    logger.info(f"Loaded {len(tx_df)} rows into 'transactions' table.")

def setup_database():
    """Initializes SQLite database and creates tables using schema.sql."""
    logger.info(f"Initializing SQLite database at: {DB_PATH}")
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        logger.info("Removed existing database file.")
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Read and execute schema
    with open(SCHEMA_PATH, 'r') as f:
        schema_sql = f.read()
        
    cursor.executescript(schema_sql)
    conn.commit()
    logger.info("Database schema applied successfully.")
    
    # Populate tables
    populate_database(conn)
    conn.commit()
    conn.close()

def parse_sql_queries() -> list:
    """Parses queries_15_analysis.sql and extracts individual query strings and titles."""
    logger.info(f"Parsing query file: {QUERIES_PATH}")
    with open(QUERIES_PATH, 'r') as f:
        content = f.read()
        
    # Split content by QUERY indicators
    query_blocks = re.split(r'--\s*QUERY\s+(\d+):\s*([^\n]+)', content)
    
    queries = []
    # The first element is before QUERY 1, then blocks of (idx, title, query_sql)
    for i in range(1, len(query_blocks), 3):
        q_num = query_blocks[i].strip()
        q_title = query_blocks[i+1].strip()
        q_sql_full = query_blocks[i+2]
        
        # Clean SQL and comments
        q_sql = ""
        for line in q_sql_full.split('\n'):
            if not line.strip().startswith('--') and line.strip():
                q_sql += line + '\n'
                
        # Split multiple queries if any, select the first valid
        q_sql = q_sql.strip()
        if q_sql.endswith(';'):
            q_sql = q_sql[:-1]
            
        queries.append({
            'number': q_num,
            'title': q_title,
            'sql': q_sql
        })
        
    logger.info(f"Parsed {len(queries)} queries successfully.")
    return queries

def execute_and_log_queries():
    """Executes all 15 queries and logs outcomes to reports/sql_queries_results.txt."""
    queries = parse_sql_queries()
    
    conn = sqlite3.connect(DB_PATH)
    
    logger.info(f"Executing queries. Saving outputs to {OUTPUT_REPORT_PATH}...")
    os.makedirs(os.path.dirname(OUTPUT_REPORT_PATH), exist_ok=True)
    
    with open(OUTPUT_REPORT_PATH, 'w') as f:
        f.write("==============================================================================\n")
        f.write("               PHARMACY ANALYTICS - SQL QUERY EXECUTION LOG\n")
        f.write("==============================================================================\n\n")
        
        for q in queries:
            num = q['number']
            title = q['title']
            sql = q['sql']
            
            f.write(f"--- QUERY {num}: {title} ---\n")
            f.write(f"SQL QUERY:\n{sql};\n\n")
            
            try:
                # Load query result as DataFrame
                df = pd.read_sql_query(sql, conn)
                
                # Write formatted output
                f.write("RESULT SET:\n")
                if len(df) == 0:
                    f.write("No rows returned.\n")
                else:
                    f.write(df.to_string(index=False))
                    f.write("\n")
                f.write(f"Rows returned: {len(df)}\n")
            except Exception as e:
                logger.error(f"Error executing Query {num}: {str(e)}")
                f.write(f"ERROR: Failed to execute query. Details: {str(e)}\n")
                
            f.write("\n" + "=" * 80 + "\n\n")
            
    conn.close()
    logger.info("Query execution complete.")

def main():
    setup_database()
    execute_and_log_queries()

if __name__ == '__main__':
    main()
