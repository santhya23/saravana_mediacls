import sqlite3

DB_PATH = 'database/pharmacy.db'

def add_po_id_column():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check existing columns
    cursor.execute("PRAGMA table_info(supplier_payments)")
    columns = [col[1] for col in cursor.fetchall()]

    if "po_id" not in columns:
        print("➕ Adding po_id column to supplier_payments...")
        cursor.execute("""
            ALTER TABLE supplier_payments
            ADD COLUMN po_id INTEGER
        """)
        conn.commit()
        print("✅ po_id column added successfully!")
    else:
        print("ℹ️ po_id column already exists")

    conn.close()

if __name__ == "__main__":
    add_po_id_column()
