import sqlite3

DB_PATH = 'database/pharmacy.db'

def update_supplier_schema():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("🔄 Updating database schema for advanced supplier management...")
    
    try:
        # Check if purchase_orders table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='purchase_orders'")
        if not cursor.fetchone():
            print("📦 Creating purchase_orders table...")
            cursor.execute('''
                CREATE TABLE purchase_orders (
                    po_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    supplier_id INTEGER NOT NULL,
                    po_number TEXT UNIQUE NOT NULL,
                    po_date DATE NOT NULL,
                    expected_delivery DATE,
                    total_amount REAL NOT NULL,
                    status TEXT DEFAULT 'Pending',
                    invoice_path TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
                )
            ''')
            print("✅ purchase_orders table created!")
        
        # Purchase Order Items
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='purchase_order_items'")
        if not cursor.fetchone():
            print("📦 Creating purchase_order_items table...")
            cursor.execute('''
                CREATE TABLE purchase_order_items (
                    po_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    po_id INTEGER NOT NULL,
                    medicine_name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    batch_number TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL,
                    expiry_date DATE NOT NULL,
                    received_quantity INTEGER DEFAULT 0,
                    FOREIGN KEY (po_id) REFERENCES purchase_orders(po_id)
                )
            ''')
            print("✅ purchase_order_items table created!")
        
        # Purchase Returns
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='purchase_returns'")
        if not cursor.fetchone():
            print("📦 Creating purchase_returns table...")
            cursor.execute('''
                CREATE TABLE purchase_returns (
                    return_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    supplier_id INTEGER NOT NULL,
                    medicine_id INTEGER NOT NULL,
                    return_date DATE NOT NULL,
                    quantity INTEGER NOT NULL,
                    reason TEXT NOT NULL,
                    status TEXT DEFAULT 'Pending',
                    credit_amount REAL NOT NULL,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id),
                    FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id)
                )
            ''')
            print("✅ purchase_returns table created!")
        
        # Supplier Payments
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='supplier_payments'")
        if not cursor.fetchone():
            print("📦 Creating supplier_payments table...")
            cursor.execute('''
                CREATE TABLE supplier_payments (
                    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    supplier_id INTEGER NOT NULL,
                    po_id INTEGER,
                    payment_date DATE NOT NULL,
                    amount REAL NOT NULL,
                    payment_mode TEXT NOT NULL,
                    reference_number TEXT,
                    receipt_path TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id),
                    FOREIGN KEY (po_id) REFERENCES purchase_orders(po_id)
                )
            ''')
            print("✅ supplier_payments table created!")
        
        # Supplier Performance
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='supplier_performance'")
        if not cursor.fetchone():
            print("📦 Creating supplier_performance table...")
            cursor.execute('''
                CREATE TABLE supplier_performance (
                    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    supplier_id INTEGER NOT NULL,
                    po_id INTEGER NOT NULL,
                    delivery_time_days INTEGER,
                    quality_score INTEGER,
                    quantity_accuracy INTEGER,
                    recorded_date DATE NOT NULL,
                    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id),
                    FOREIGN KEY (po_id) REFERENCES purchase_orders(po_id)
                )
            ''')
            print("✅ supplier_performance table created!")
        
        # Update suppliers table with new columns if they don't exist
        cursor.execute("PRAGMA table_info(suppliers)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'gstin' not in columns:
            print("📦 Adding new columns to suppliers table...")
            cursor.execute('ALTER TABLE suppliers ADD COLUMN gstin TEXT')
            cursor.execute('ALTER TABLE suppliers ADD COLUMN contact_person TEXT')
            cursor.execute('ALTER TABLE suppliers ADD COLUMN payment_terms TEXT DEFAULT "30 Days"')
            cursor.execute('ALTER TABLE suppliers ADD COLUMN preferred_payment_mode TEXT DEFAULT "Bank Transfer"')
            cursor.execute('ALTER TABLE suppliers ADD COLUMN rating INTEGER DEFAULT 3')
            print("✅ Suppliers table updated!")
        
        conn.commit()
        print("\n🎉 Database schema updated successfully!")
        print("✅ All tables ready:")
        print("   - purchase_orders")
        print("   - purchase_order_items")
        print("   - purchase_returns")
        print("   - supplier_payments")
        print("   - supplier_performance")
        print("   - suppliers (updated with new columns)")
        
    except Exception as e:
        print(f"❌ Error updating schema: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    update_supplier_schema()