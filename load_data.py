import sqlite3
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
DB_PATH = "olist.db"

files = {
    
    
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}

conn = sqlite3.connect(DB_PATH)
for table, filename in files.items():
    df = pd.read_csv(DATA_DIR / filename)
    df.to_sql(table, conn, if_exists="replace", index=False)
    print(f"Loaded {table}: {len(df)} rows")
conn.close()