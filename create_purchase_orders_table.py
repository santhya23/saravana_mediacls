import sqlite3
import os

DB_PATH = 'database/pharmacy.db'

def create_purchase_orders_table():
    print("🔧 Creating purchase_orders table...")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchase_orders (
            po_id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier_id INTEGER,
            order_date DATE,
            total_amount REAL DEFAULT 0,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
        )
    """)

    conn.commit()
    conn.close()

    print("✅ purchase_orders table created successfully!")

if __name__ == "__main__":
    create_purchase_orders_table()

