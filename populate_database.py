import sqlite3
from datetime import datetime, timedelta
import random
import os

DB_PATH = 'database/pharmacy.db'


def create_tables():
    """Create database tables with updated schema"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA foreign_keys = ON')
    cursor = conn.cursor()
    
    # Suppliers table with updated fields
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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Medicines table with updated fields
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
    conn.close()


def populate_database():
    """Populate pharmacy DB with Tamil Nadu suppliers and medicines"""

    os.makedirs('database', exist_ok=True)
    create_tables()

    conn = sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA foreign_keys = ON')
    cursor = conn.cursor()

    print("🔄 === DATABASE POPULATION START ===")

    # Clear existing data
    print("🗑️  Clearing existing data...")
    cursor.execute('DELETE FROM sale_items')
    cursor.execute('DELETE FROM sales')
    cursor.execute('DELETE FROM medicines')
    cursor.execute('DELETE FROM suppliers')
    conn.commit()

    # 1. SUPPLIERS - Tamil Nadu based real companies
    print("📦 Adding Tamil Nadu suppliers...")
    suppliers = [
        ('Tamil Nadu Medicals Agencies', 'Murugan K', '9445123456', '33AABCT1234F1Z5', 'Net 30', 4.5, 245, 45000, 'RS Puram, Coimbatore'),
        ('Kaveri Pharmaceuticals Pvt Ltd', 'Lakshmi R', '8756102367', '33AABCK5678G1Z8', 'Net 45', 4.8, 312, 22000, 'Gandhipuram, Coimbatore'),
        ('Sri Venkateswara Medicals', 'Rajesh Kumar', '9654120758', '33AABCS9012H1Z1', 'Cash on Delivery', 4.2, 189, 38500, 'Peelamedu, Coimbatore'),
        ('Meenakshi Pharma Distributors', 'Priya S', '9786102354', '33AABCM3456I1Z4', 'Net 30', 4.6, 276, 15000, 'Saibaba Colony, Coimbatore'),
        ('Apollo Health & Lifestyle', 'Senthil Nathan', '9785694100', '33AABCA7890J1Z7', 'Net 60', 4.9, 428, 8000, 'Avinashi Road, Coimbatore'),
        ('Sunshine Pharmaceuticals', 'Anitha M', '985910245', '33AABCS2345K1Z0', 'Net 30', 4.3, 198, 52000, 'Townhall, Coimbatore'),
        ('Chennai Drug House', 'Karthik V', '9478510232', '33AABCC6789L1Z3', 'Net 45', 4.7, 356, 12000, 'Ukkadam, Coimbatore'),
        ('Madurai Medical Agencies', 'Vasanthi P', '9965410123', '33AABCM1234M1Z6', 'Cash on Delivery', 4.1, 167, 67000, 'Sungam, Coimbatore'),
        ('Coimbatore Pharma Traders', 'Sivakumar R', '7456901234', '33AABCC5678N1Z9', 'Net 30', 4.4, 234, 29000, 'Karamadai Road, Coimbatore'),
        ('Erode Drug Distributors', 'Deepa K', '8596147258', '33AABCE9012O1Z2', 'Net 45', 4.5, 289, 18000, 'Mettupalayam Road, Coimbatore'),
        ('Salem Medical Suppliers', 'Ganesh B', '6365471256', '33AABCS3456P1Z5', 'Net 60', 4.6, 312, 25000, 'Saravanampatti, Coimbatore'),
        ('Tiruppur Health Care', 'Malini S', '948596467', '33AABCT7890Q1Z8', 'Cash on Delivery', 4.0, 145, 72000, 'Singanallur, Coimbatore'),
    ]
    cursor.executemany(
        '''
        INSERT INTO suppliers (
            supplier_name,
            contact_person,
            phone,
            gstin,
            payment_terms,
            rating,
            total_orders,
            outstanding,
            address
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        suppliers
    )



    conn.commit()

    supplier_ids = [row[0] for row in cursor.execute(
        'SELECT supplier_id FROM suppliers'
    ).fetchall()]
    print(f"✅ {len(supplier_ids)} suppliers added")

    # 2. MEDICINES - Real medicines with Tamil Nadu context
    print("💊 Adding medicines...")

    medicines = [
        # Analgesics & Antipyretics
        ('Dolo 650mg', 'Analgesic', 'DLO650-2024-001', 2.50, 500, 'In Stock', '2027-03-15', supplier_ids[0]),
        ('Crocin Advance', 'Analgesic', 'CRC-2024-102', 3.00, 450, 'In Stock', '2027-02-20', supplier_ids[1]),
        ('Combiflam Tablet', 'Analgesic', 'CMB-2024-203', 5.50, 380, 'In Stock', '2027-04-10', supplier_ids[2]),
        ('Ibugesic Plus', 'Analgesic', 'IBG-2024-304', 6.00, 320, 'In Stock', '2027-01-25', supplier_ids[3]),
        ('Zerodol SP', 'Analgesic', 'ZRD-2024-405', 8.50, 280, 'In Stock', '2026-12-30', supplier_ids[4]),
        ('Brufen 400mg', 'Analgesic', 'BRF-2024-506', 4.50, 290, 'In Stock', '2027-05-18', supplier_ids[5]),
        ('Flexon Tablet', 'Analgesic', 'FLX-2024-607', 3.50, 410, 'In Stock', '2027-03-22', supplier_ids[6]),
        
        # Antibiotics
        ('Azithral 500', 'Antibiotic', 'AZT-2024-708', 18.00, 250, 'In Stock', '2026-11-15', supplier_ids[0]),
        ('Augmentin 625', 'Antibiotic', 'AUG-2024-809', 22.50, 220, 'In Stock', '2026-10-20', supplier_ids[1]),
        ('Amoxyclav 625', 'Antibiotic', 'AMX-2024-910', 16.00, 200, 'In Stock', '2026-09-25', supplier_ids[2]),
        ('Ciprofloxacin 500mg', 'Antibiotic', 'CPR-2024-011', 12.00, 180, 'In Stock', '2027-01-10', supplier_ids[3]),
        ('Cefixime 200mg', 'Antibiotic', 'CFX-2024-112', 15.50, 160, 'In Stock', '2026-12-05', supplier_ids[4]),
        ('Levofloxacin 500mg', 'Antibiotic', 'LVF-2024-213', 19.00, 145, 'In Stock', '2027-02-14', supplier_ids[5]),
        ('Clavam 625', 'Antibiotic', 'CLV-2024-314', 21.00, 170, 'In Stock', '2026-11-28', supplier_ids[6]),
        
        # Antacids & Digestive
        ('Pan 40', 'Antacid', 'PAN-2024-415', 6.50, 420, 'In Stock', '2027-04-20', supplier_ids[7]),
        ('Omez 20mg', 'Antacid', 'OMZ-2024-516', 5.50, 480, 'In Stock', '2027-05-12', supplier_ids[8]),
        ('Gelusil Syrup', 'Antacid', 'GLS-2024-617', 45.00, 150, 'In Stock', '2027-03-08', supplier_ids[9]),
        ('Digene Tablet', 'Antacid', 'DGN-2024-718', 2.00, 550, 'In Stock', '2027-06-15', supplier_ids[10]),
        ('Rantac 150mg', 'Antacid', 'RNT-2024-819', 4.00, 380, 'In Stock', '2027-02-28', supplier_ids[11]),
        ('Rablet 20mg', 'Antacid', 'RBL-2024-920', 7.00, 340, 'In Stock', '2027-01-18', supplier_ids[0]),
        
        # Anti-diabetic
        ('Glycomet GP1', 'Antidiabetic', 'GLC-2024-021', 9.50, 300, 'In Stock', '2027-03-30', supplier_ids[1]),
        ('Janumet 50/500', 'Antidiabetic', 'JNM-2024-122', 28.00, 180, 'In Stock', '2026-12-22', supplier_ids[2]),
        ('Amaryl M 1mg', 'Antidiabetic', 'AMR-2024-223', 12.00, 220, 'In Stock', '2027-01-15', supplier_ids[3]),
        ('Gluconorm G1', 'Antidiabetic', 'GLN-2024-324', 11.50, 260, 'In Stock', '2027-04-05', supplier_ids[4]),
        ('Pioz 15mg', 'Antidiabetic', 'PIZ-2024-425', 15.00, 190, 'In Stock', '2026-11-10', supplier_ids[5]),
        
        # Cardiovascular
        ('Telma 40mg', 'Cardiovascular', 'TLM-2024-526', 8.50, 280, 'In Stock', '2027-02-18', supplier_ids[6]),
        ('Amlodipine 5mg', 'Cardiovascular', 'AML-2024-627', 3.50, 420, 'In Stock', '2027-05-20', supplier_ids[7]),
        ('Atorva 10mg', 'Cardiovascular', 'ATV-2024-728', 12.00, 310, 'In Stock', '2027-03-25', supplier_ids[8]),
        ('Ecosprin 75mg', 'Cardiovascular', 'ECS-2024-829', 2.50, 480, 'In Stock', '2027-06-10', supplier_ids[9]),
        ('Metoprolol 25mg', 'Cardiovascular', 'MTP-2024-930', 4.50, 350, 'In Stock', '2027-01-28', supplier_ids[10]),
        
        # Respiratory
        ('Ascoril LS Syrup', 'Respiratory', 'ASC-2024-031', 85.00, 120, 'In Stock', '2027-02-15', supplier_ids[11]),
        ('Levolin Inhaler', 'Respiratory', 'LVL-2024-132', 145.00, 80, 'In Stock', '2027-04-22', supplier_ids[0]),
        ('Deriphyllin Tablet', 'Respiratory', 'DRP-2024-233', 6.50, 240, 'In Stock', '2026-12-18', supplier_ids[1]),
        ('Montair LC', 'Respiratory', 'MTR-2024-334', 11.00, 290, 'In Stock', '2027-03-12', supplier_ids[2]),
        ('Chericof Syrup', 'Respiratory', 'CHR-2024-435', 65.00, 110, 'In Stock', '2027-01-20', supplier_ids[3]),
        
        # Vitamins & Supplements
        ('Becosules Capsules', 'Vitamin', 'BCS-2024-536', 3.50, 450, 'In Stock', '2027-05-28', supplier_ids[4]),
        ('Neurobion Forte', 'Vitamin', 'NRB-2024-637', 4.00, 420, 'In Stock', '2027-06-15', supplier_ids[5]),
        ('Shelcal 500', 'Vitamin', 'SHL-2024-738', 6.50, 380, 'In Stock', '2027-04-18', supplier_ids[6]),
        ('Evion 400', 'Vitamin', 'EVN-2024-839', 5.00, 340, 'In Stock', '2027-02-25', supplier_ids[7]),
        ('Zincovit Tablet', 'Vitamin', 'ZNC-2024-940', 4.50, 410, 'In Stock', '2027-03-30', supplier_ids[8]),
        
        # Antifungal & Antiparasitic
        ('Candid Cream', 'Antifungal', 'CND-2024-041', 42.00, 150, 'In Stock', '2027-01-12', supplier_ids[9]),
        ('Fluconazole 150mg', 'Antifungal', 'FLC-2024-142', 18.00, 180, 'In Stock', '2026-12-08', supplier_ids[10]),
        ('Zentel 400mg', 'Antiparasitic', 'ZNT-2024-243', 9.00, 220, 'In Stock', '2027-02-20', supplier_ids[11]),
        ('Metrogyl 400', 'Antiparasitic', 'MTG-2024-344', 5.50, 310, 'In Stock', '2027-04-15', supplier_ids[0]),
        
        # Eye & Ear Drops
        ('Tears Naturale', 'Eye Drop', 'TRS-2024-445', 85.00, 90, 'In Stock', '2027-03-05', supplier_ids[1]),
        ('Moxiflox Eye Drop', 'Eye Drop', 'MXF-2024-546', 42.00, 110, 'In Stock', '2027-01-18', supplier_ids[2]),
        ('Otiflox Ear Drop', 'Ear Drop', 'OTF-2024-647', 38.00, 95, 'In Stock', '2026-11-22', supplier_ids[3]),
        
        # Dermatology
        ('Betnovate N Cream', 'Dermatology', 'BTV-2024-748', 52.00, 140, 'In Stock', '2027-02-10', supplier_ids[4]),
        ('Lacto Calamine Lotion', 'Dermatology', 'LCT-2024-849', 95.00, 120, 'In Stock', '2027-04-28', supplier_ids[5]),
        ('Soframycin Cream', 'Dermatology', 'SFR-2024-950', 28.00, 160, 'In Stock', '2027-03-15', supplier_ids[6]),
        
        # Gastro
        ('Pudin Hara', 'Gastro', 'PDH-2024-051', 35.00, 180, 'In Stock', '2027-05-10', supplier_ids[7]),
        ('Aristozyme Syrup', 'Gastro', 'ARS-2024-152', 72.00, 95, 'In Stock', '2027-02-22', supplier_ids[8]),
        ('Cyclopam Tablet', 'Gastro', 'CYC-2024-253', 7.50, 280, 'In Stock', '2027-01-08', supplier_ids[9]),
        
        # Gynecology
        ('Meftal Spas', 'Gynecology', 'MFS-2024-354', 8.00, 240, 'In Stock', '2027-03-18', supplier_ids[10]),
        ('Duphaston 10mg', 'Gynecology', 'DPH-2024-455', 22.00, 150, 'In Stock', '2026-12-25', supplier_ids[11]),
        ('Folvite 5mg', 'Gynecology', 'FLV-2024-556', 3.00, 380, 'In Stock', '2027-04-12', supplier_ids[0]),
        
        # Antihypertensive
        ('Losar 50mg', 'Antihypertensive', 'LSR-2024-657', 9.50, 290, 'In Stock', '2027-02-08', supplier_ids[1]),
        ('Amlong 5mg', 'Antihypertensive', 'AML-2024-758', 4.50, 340, 'In Stock', '2027-05-15', supplier_ids[2]),
        ('Dilzem 30mg', 'Antihypertensive', 'DLZ-2024-859', 6.00, 270, 'In Stock', '2027-01-22', supplier_ids[3]),
        
        # Antiallergic
        ('Cetrizine 10mg', 'Antiallergic', 'CTZ-2024-960', 2.00, 520, 'In Stock', '2027-06-18', supplier_ids[4]),
        ('Allegra 120mg', 'Antiallergic', 'ALG-2024-061', 9.00, 280, 'In Stock', '2027-03-28', supplier_ids[5]),
        ('Avil 25mg', 'Antiallergic', 'AVL-2024-162', 3.50, 380, 'In Stock', '2027-04-20', supplier_ids[6]),
        
        # Antispasmodic
        ('Buscopan 10mg', 'Antispasmodic', 'BSC-2024-263', 8.50, 220, 'In Stock', '2027-02-12', supplier_ids[7]),
        ('Spasmoproxyvon', 'Antispasmodic', 'SPX-2024-364', 5.00, 260, 'In Stock', '2027-01-15', supplier_ids[8]),
        
        # Emergency & Injections
        ('Adrenaline Injection', 'Emergency', 'ADR-2024-465', 45.00, 8, 'Low Stock', '2026-10-15', supplier_ids[9]),
        ('Dexamethasone Inj', 'Emergency', 'DXM-2024-566', 28.00, 15, 'Low Stock', '2026-11-20', supplier_ids[10]),
        ('Human Mixtard 30/70', 'Insulin', 'HMI-2024-667', 320.00, 12, 'Low Stock', '2026-09-28', supplier_ids[11]),
        ('Actrapid Insulin', 'Insulin', 'ACT-2024-768', 280.00, 9, 'Low Stock', '2026-08-15', supplier_ids[0]),
        
        # Low Stock Items
        ('Rabies Vaccine', 'Vaccine', 'RBV-2024-869', 350.00, 4, 'Low Stock', '2026-07-10', supplier_ids[1]),
        ('Tetanus Toxoid', 'Vaccine', 'TTX-2024-970', 65.00, 6, 'Low Stock', '2026-06-22', supplier_ids[2]),
        ('Fortwin Injection', 'Analgesic', 'FTW-2024-071', 52.00, 7, 'Low Stock', '2026-08-05', supplier_ids[3]),
        
        # Out of Stock
        ('Covishield Vaccine', 'Vaccine', 'CVS-2024-172', 250.00, 0, 'Out of Stock', '2026-05-18', supplier_ids[4]),
        ('N95 Mask Box', 'Safety', 'N95-2024-273', 450.00, 0, 'Out of Stock', '2027-01-10', supplier_ids[5]),
        
        # Near Expiry
        ('Sinarest Tablet', 'Cold & Flu', 'SNR-2024-374', 4.50, 180, 'Near Expiry', '2026-02-15', supplier_ids[6]),
        ('Vicks Vaporub', 'Cold & Flu', 'VCK-2024-475', 85.00, 95, 'Near Expiry', '2026-02-20', supplier_ids[7]),
        ('Coldact Tablet', 'Cold & Flu', 'CLD-2024-576', 6.00, 140, 'Near Expiry', '2026-02-10', supplier_ids[8]),
        
        # Additional Common Medicines
        ('D Cold Total', 'Cold & Flu', 'DCT-2024-677', 7.50, 220, 'In Stock', '2027-03-22', supplier_ids[9]),
        ('Allegra M Tablet', 'Antiallergic', 'ALM-2024-778', 11.00, 190, 'In Stock', '2027-04-15', supplier_ids[10]),
        ('Norflox TZ', 'Antibiotic', 'NFX-2024-879', 14.00, 210, 'In Stock', '2026-12-12', supplier_ids[11]),
        ('Sporlac Sachet', 'Probiotic', 'SPL-2024-980', 18.00, 150, 'In Stock', '2027-05-08', supplier_ids[0]),
        ('ORS Orange Flavor', 'Rehydration', 'ORS-2024-081', 12.00, 280, 'In Stock', '2027-06-20', supplier_ids[1]),
        ('Electral Powder', 'Rehydration', 'ELC-2024-182', 11.00, 310, 'In Stock', '2027-05-25', supplier_ids[2]),
        ('Avomine Tablet', 'Antiemetic', 'AVM-2024-283', 5.50, 240, 'In Stock', '2027-03-10', supplier_ids[3]),
        ('Ondem MD 4', 'Antiemetic', 'OND-2024-384', 9.00, 200, 'In Stock', '2027-02-28', supplier_ids[4]),
        ('Mucaine Gel', 'Antacid', 'MCN-2024-485', 92.00, 85, 'In Stock', '2027-01-18', supplier_ids[5]),
        ('Liv 52 DS', 'Hepatoprotective', 'LIV-2024-586', 145.00, 110, 'In Stock', '2027-04-25', supplier_ids[6]),
        ('Unienzyme Tablet', 'Digestive', 'UNZ-2024-687', 6.00, 260, 'In Stock', '2027-03-15', supplier_ids[7]),
        ('Chymoral Forte', 'Enzyme', 'CHM-2024-788', 12.50, 180, 'In Stock', '2027-02-20', supplier_ids[8]),
        ('Volini Gel', 'Pain Relief', 'VLN-2024-889', 125.00, 95, 'In Stock', '2027-05-12', supplier_ids[9]),
        ('Moov Cream', 'Pain Relief', 'MOV-2024-990', 98.00, 105, 'In Stock', '2027-04-08', supplier_ids[10]),
        ('Burnol Cream', 'Burn Relief', 'BRN-2024-091', 45.00, 130, 'In Stock', '2027-03-18', supplier_ids[11]),
    ]

    cursor.executemany(
        '''
        INSERT INTO medicines
        (medicine_name, category, batch_number, price, quantity, status, expiry_date, supplier_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        medicines
    )
    conn.commit()

    medicine_ids = [row[0] for row in cursor.execute(
        'SELECT medicine_id FROM medicines WHERE quantity > 0'
    ).fetchall()]
    print(f"✅ {len(medicines)} medicines added")

    # 3. SALES – last 30 days with South Indian names
    print("💰 Adding sales for last 30 days...")

    customers = [
        'Walk-in Customer',
        'Murugan S',
        'Lakshmi Priya',
        'Karthik Raja',
        'Anitha Devi',
        'Rajesh Kumar',
        'Priya Shankar',
        'Senthil Nathan',
        'Deepa Krishnan',
        'Sivakumar M',
        'Malini Subramanian',
        'Ganesh Babu',
        'Vasanthi P',
        'Arun Prakash',
        'Kavitha R'
    ]
    payments = ['Cash', 'UPI', 'Card', 'PhonePe', 'GPay']

    days_back = 30
    sales_per_day = random.randint(4, 8)  # 4-8 sales per day

    for d in range(days_back):
        sale_day = datetime.now() - timedelta(days=d)
        daily_sales = random.randint(4, 8)
        
        for _ in range(daily_sales):
            customer = random.choice(customers)
            payment = random.choice(payments)
            total_amount = 0.0

            cursor.execute(
                '''
                INSERT INTO sales (sale_date, customer_name, total_amount, payment_method)
                VALUES (?, ?, ?, ?)
                ''',
                (sale_day, customer, 0, payment)
            )
            sale_id = cursor.lastrowid

            # each sale: 1–4 different medicines
            item_count = random.randint(1, 4)
            used_meds = random.sample(medicine_ids, min(item_count, len(medicine_ids)))

            for med_id in used_meds:
                qty = random.randint(1, 5)
                price = cursor.execute(
                    'SELECT price FROM medicines WHERE medicine_id = ?',
                    (med_id,)
                ).fetchone()[0]
                subtotal = round(price * qty, 2)
                total_amount += subtotal

                cursor.execute(
                    '''
                    INSERT INTO sale_items
                    (sale_id, medicine_id, quantity, price, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                    ''',
                    (sale_id, med_id, qty, price, subtotal)
                )

                # reduce stock but do not go negative
                cursor.execute(
                    '''
                    UPDATE medicines
                    SET quantity = MAX(quantity - ?, 0)
                    WHERE medicine_id = ?
                    ''',
                    (qty, med_id)
                )

            cursor.execute(
                'UPDATE sales SET total_amount = ? WHERE sale_id = ?',
                (round(total_amount, 2), sale_id)
            )

    # Update status based on quantity after sales
    cursor.execute('''
        UPDATE medicines 
        SET status = CASE 
            WHEN quantity = 0 THEN 'Out of Stock'
            WHEN quantity < 10 THEN 'Low Stock'
            WHEN DATE(expiry_date) < DATE('now', '+30 days') THEN 'Near Expiry'
            ELSE 'In Stock'
        END
    ''')

    conn.commit()
    conn.close()

    # Final summary
    conn = sqlite3.connect(DB_PATH)
    print("\n📊 === FINAL DATABASE SUMMARY ===")
    print(f"✅ Suppliers: {conn.execute('SELECT COUNT(*) FROM suppliers').fetchone()[0]}")
    print(f"✅ Medicines: {conn.execute('SELECT COUNT(*) FROM medicines').fetchone()[0]}")
    print(f"✅ Sales Records: {conn.execute('SELECT COUNT(*) FROM sales').fetchone()[0]}")

    print("\n🚀 === READY! Run: python app.py ===")


if __name__ == '__main__':
    populate_database()
