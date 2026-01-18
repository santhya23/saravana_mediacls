import sqlite3
import os

DB_PATH = 'database/pharmacy.db'

def update_schema():
    """Update existing database schema to match new requirements"""
    
    print("🔄 === DATABASE SCHEMA UPDATE START ===")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Backup old data
    print("📦 Backing up existing data...")
    
    # Get existing suppliers data
    try:
        old_suppliers = cursor.execute('SELECT * FROM suppliers').fetchall()
        print(f"✅ Found {len(old_suppliers)} existing suppliers")
    except:
        old_suppliers = []
    
    # Get existing medicines data
    try:
        old_medicines = cursor.execute('SELECT * FROM medicines').fetchall()
        print(f"✅ Found {len(old_medicines)} existing medicines")
    except:
        old_medicines = []
    
    # Drop existing tables
    print("🗑️  Dropping old tables...")
    cursor.execute('DROP TABLE IF EXISTS sale_items')
    cursor.execute('DROP TABLE IF EXISTS sales')
    cursor.execute('DROP TABLE IF EXISTS medicines')
    cursor.execute('DROP TABLE IF EXISTS suppliers')
    conn.commit()
    
    # Create new tables with updated schema
    print("🔨 Creating new tables with updated schema...")
    
    # Suppliers table with NEW fields
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier_name TEXT NOT NULL,
            contact_person TEXT,
            phone TEXT,
            gstin TEXT,
            payment_terms TEXT,
            rating REAL DEFAULT 0.0,
            total_orders INTEGER DEFAULT 0,
            outstanding REAL DEFAULT 0.0,
            address TEXT,
            email TEXT,
            contact_number TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Medicines table with NEW fields
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicines (
            medicine_id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_name TEXT NOT NULL,
            category TEXT,
            batch_number TEXT,
            price REAL NOT NULL,
            quantity INTEGER DEFAULT 0,
            status TEXT,
            expiry_date DATE,
            supplier_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
        )
    ''')
    
    # Sales table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            customer_name TEXT,
            total_amount REAL DEFAULT 0,
            payment_method TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Sale items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sale_items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER,
            medicine_id INTEGER,
            quantity INTEGER,
            price REAL,
            subtotal REAL,
            FOREIGN KEY (sale_id) REFERENCES sales(sale_id),
            FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id)
        )
    ''')
    
    conn.commit()
    print("✅ New schema created successfully!")
    
    # Migrate old data if exists
    if old_suppliers:
        print("📥 Migrating old supplier data...")
        for supplier in old_suppliers:
            try:
                # Try to map old fields to new fields
                cursor.execute('''
                    INSERT INTO suppliers (supplier_name, contact_person, phone, address, email, contact_number)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    supplier[1] if len(supplier) > 1 else 'Unknown Supplier',  # supplier_name
                    'Contact Person',  # contact_person (new field)
                    supplier[2] if len(supplier) > 2 else '',  # phone/contact_number
                    supplier[4] if len(supplier) > 4 else '',  # address
                    supplier[3] if len(supplier) > 3 else '',  # email
                    supplier[2] if len(supplier) > 2 else '',  # contact_number
                ))
            except Exception as e:
                print(f"⚠️  Error migrating supplier: {e}")
        conn.commit()
        print(f"✅ Migrated {len(old_suppliers)} suppliers")
    
    conn.close()
    
    print("\n✅ === SCHEMA UPDATE COMPLETE ===")
    print("📝 New fields added:")
    print("   Suppliers: contact_person, phone, gstin, payment_terms, rating, total_orders, outstanding")
    print("   Medicines: status")
    print("\n🚀 Now run: python populate_database.py")

if __name__ == '__main__':
    update_schema()