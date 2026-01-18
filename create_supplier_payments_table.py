import sqlite3
import os

DB_PATH = 'database/pharmacy.db'

def create_supplier_payments_table():
    print("🔧 Creating supplier_payments table...")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS supplier_payments (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier_id INTEGER NOT NULL,
            payment_date DATE,
            amount REAL DEFAULT 0,
            payment_mode TEXT,
            remarks TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
        )
    """)

    conn.commit()
    conn.close()

    print("✅ supplier_payments table created successfully!")

if __name__ == "__main__":
    create_supplier_payments_table()
