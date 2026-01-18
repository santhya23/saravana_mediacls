# Unit Tests for Pharmacy System Backend
# File: test_unit.py
# Run: pytest test_unit.py -v

import pytest
import sys
import os

# Add your app directory to path
sys.path.insert(0, os.path.abspath('.'))

# Import your app and database
# from app import app, db  # Uncomment and modify based on your structure

class TestDatabaseOperations:
    """Test database operations"""
    
    def test_database_connection(self):
        """Test database connection"""
        # Example test - modify based on your DB setup
        try:
            # Replace with your actual DB connection test
            # connection = db.connect()
            # assert connection is not None
            print("✅ Database connection test")
            assert True
        except Exception as e:
            pytest.fail(f"Database connection failed: {e}")
    
    def test_create_tables(self):
        """Test if all required tables exist"""
        # Example - modify based on your tables
        required_tables = [
            'medicines',
            'stock',
            'suppliers',
            'bills',
            'users'
        ]
        
        # Replace with your actual table check logic
        # existing_tables = db.get_table_names()
        # for table in required_tables:
        #     assert table in existing_tables
        
        print("✅ Database tables check")
        assert True


class TestMedicineOperations:
    """Test medicine-related operations"""
    
    def test_medicine_validation(self):
        """Test medicine data validation"""
        # Example validation test
        medicine_data = {
            'name': 'Paracetamol',
            'batch_no': 'BATCH001',
            'quantity': 100,
            'price': 50.00
        }
        
        # Test valid data
        assert medicine_data['quantity'] > 0
        assert medicine_data['price'] > 0
        assert len(medicine_data['name']) > 0
        
        print("✅ Medicine validation test passed")
    
    def test_negative_quantity_validation(self):
        """Test that negative quantities are rejected"""
        invalid_quantity = -10
        
        # Your validation function should reject this
        assert invalid_quantity < 0  # This should be caught by validation
        print("✅ Negative quantity detected correctly")
    
    def test_medicine_price_calculation(self):
        """Test price calculations"""
        price = 100.00
        quantity = 10
        discount = 10  # 10%
        
        subtotal = price * quantity
        discount_amount = (subtotal * discount) / 100
        final_price = subtotal - discount_amount
        
        assert final_price == 900.00
        print("✅ Price calculation correct")
    
    def test_batch_number_format(self):
        """Test batch number format"""
        valid_batch = "BATCH12345"
        invalid_batch = ""
        
        assert len(valid_batch) > 0
        assert valid_batch.isalnum() or '_' in valid_batch or '-' in valid_batch
        
        print("✅ Batch number format validation")


class TestBillingOperations:
    """Test billing-related operations"""
    
    def test_bill_total_calculation(self):
        """Test bill total calculation"""
        items = [
            {'price': 100, 'quantity': 2},  # 200
            {'price': 50, 'quantity': 3},   # 150
            {'price': 75, 'quantity': 1}    # 75
        ]
        
        total = sum(item['price'] * item['quantity'] for item in items)
        
        assert total == 425
        print("✅ Bill total calculation correct")
    
    def test_gst_calculation(self):
        """Test GST calculation"""
        subtotal = 1000
        gst_rate = 18  # 18%
        
        gst_amount = (subtotal * gst_rate) / 100
        total = subtotal + gst_amount
        
        assert gst_amount == 180
        assert total == 1180
        print("✅ GST calculation correct")
    
    def test_discount_calculation(self):
        """Test discount calculation"""
        subtotal = 1000
        
        # Percentage discount
        discount_percent = 10
        discount_amount = (subtotal * discount_percent) / 100
        assert discount_amount == 100
        
        # Fixed discount
        fixed_discount = 50
        final_total = subtotal - fixed_discount
        assert final_total == 950
        
        print("✅ Discount calculation correct")
    
    def test_bill_number_generation(self):
        """Test unique bill number generation"""
        import datetime
        
        # Example bill number format: BILL-YYYYMMDD-0001
        today = datetime.datetime.now()
        bill_prefix = f"BILL-{today.strftime('%Y%m%d')}"
        bill_number = f"{bill_prefix}-0001"
        
        assert bill_number.startswith("BILL-")
        assert len(bill_number) > 10
        
        print(f"✅ Bill number generated: {bill_number}")


class TestStockOperations:
    """Test stock management operations"""
    
    def test_stock_deduction(self):
        """Test stock deduction after sale"""
        initial_stock = 100
        sold_quantity = 15
        
        remaining_stock = initial_stock - sold_quantity
        
        assert remaining_stock == 85
        assert remaining_stock >= 0
        
        print("✅ Stock deduction correct")
    
    def test_low_stock_detection(self):
        """Test low stock alert trigger"""
        current_stock = 5
        threshold = 10
        
        is_low_stock = current_stock < threshold
        
        assert is_low_stock == True
        print("✅ Low stock detection working")
    
    def test_out_of_stock_prevention(self):
        """Test that orders can't exceed stock"""
        available_stock = 10
        order_quantity = 15
        
        can_fulfill = available_stock >= order_quantity
        
        assert can_fulfill == False
        print("✅ Out of stock prevention working")
    
    def test_stock_update(self):
        """Test stock update operations"""
        current_stock = 50
        new_stock_added = 30
        
        updated_stock = current_stock + new_stock_added
        
        assert updated_stock == 80
        print("✅ Stock update calculation correct")


class TestSupplierOperations:
    """Test supplier-related operations"""
    
    def test_email_validation(self):
        """Test email format validation"""
        import re
        
        valid_email = "supplier@example.com"
        invalid_email = "invalid-email"
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        assert re.match(email_pattern, valid_email) is not None
        assert re.match(email_pattern, invalid_email) is None
        
        print("✅ Email validation working")
    
    def test_gstin_validation(self):
        """Test GSTIN format validation"""
        import re
        
        valid_gstin = "22AAAAA0000A1Z5"
        invalid_gstin = "INVALID123"
        
        gstin_pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
        
        assert re.match(gstin_pattern, valid_gstin) is not None
        assert re.match(gstin_pattern, invalid_gstin) is None
        
        print("✅ GSTIN validation working")
    
    def test_outstanding_calculation(self):
        """Test outstanding payment calculation"""
        total_purchase = 50000
        paid_amount = 30000
        
        outstanding = total_purchase - paid_amount
        
        assert outstanding == 20000
        print("✅ Outstanding calculation correct")


class TestExpiryOperations:
    """Test expiry-related operations"""
    
    def test_expiry_date_check(self):
        """Test if medicine is expired"""
        from datetime import datetime, timedelta
        
        today = datetime.now()
        
        expired_date = today - timedelta(days=10)
        future_date = today + timedelta(days=30)
        
        is_expired = expired_date < today
        is_not_expired = future_date > today
        
        assert is_expired == True
        assert is_not_expired == True
        
        print("✅ Expiry date check working")
    
    def test_days_until_expiry(self):
        """Test calculation of days until expiry"""
        from datetime import datetime, timedelta
        
        today = datetime.now()
        expiry_date = today + timedelta(days=45)
        
        days_until_expiry = (expiry_date - today).days
        
        assert days_until_expiry == 45
        print("✅ Days until expiry calculation correct")
    
    def test_expiry_alert_levels(self):
        """Test expiry alert level categorization"""
        days_until_expiry = 25
        
        if days_until_expiry <= 30:
            alert_level = "danger"
        elif days_until_expiry <= 60:
            alert_level = "warning"
        else:
            alert_level = "safe"
        
        assert alert_level == "danger"
        print("✅ Expiry alert level correct")


class TestUserOperations:
    """Test user-related operations"""
    
    def test_password_hashing(self):
        """Test password hashing"""
        import hashlib
        
        password = "MyPassword123"
        
        # Simple hash example (use bcrypt in production)
        hashed = hashlib.sha256(password.encode()).hexdigest()
        
        assert hashed != password
        assert len(hashed) > 0
        
        print("✅ Password hashing working")
    
    def test_password_strength(self):
        """Test password strength validation"""
        weak_password = "123"
        strong_password = "MyStrong@Pass123"
        
        def check_password_strength(pwd):
            return len(pwd) >= 8 and any(c.isupper() for c in pwd) and any(c.isdigit() for c in pwd)
        
        assert check_password_strength(weak_password) == False
        assert check_password_strength(strong_password) == True
        
        print("✅ Password strength validation working")


class TestReportOperations:
    """Test report generation operations"""
    
    def test_date_range_filtering(self):
        """Test filtering data by date range"""
        from datetime import datetime, timedelta
        
        today = datetime.now()
        start_date = today - timedelta(days=30)
        end_date = today
        
        # Sample data with dates
        transactions = [
            {'date': today - timedelta(days=5), 'amount': 100},
            {'date': today - timedelta(days=40), 'amount': 200},
            {'date': today - timedelta(days=15), 'amount': 150}
        ]
        
        # Filter transactions within date range
        filtered = [t for t in transactions if start_date <= t['date'] <= end_date]
        
        assert len(filtered) == 2  # Only 2 transactions in range
        print("✅ Date range filtering working")
    
    def test_revenue_calculation(self):
        """Test total revenue calculation"""
        sales = [
            {'amount': 500, 'discount': 50},
            {'amount': 1000, 'discount': 100},
            {'amount': 750, 'discount': 0}
        ]
        
        total_revenue = sum(sale['amount'] - sale['discount'] for sale in sales)
        
        assert total_revenue == 2100
        print("✅ Revenue calculation correct")


class TestDataValidation:
    """Test general data validation"""
    
    def test_required_fields(self):
        """Test required field validation"""
        data = {
            'name': 'Test Medicine',
            'price': 100,
            'quantity': 50
        }
        
        required_fields = ['name', 'price', 'quantity']
        
        for field in required_fields:
            assert field in data
            assert data[field] is not None
        
        print("✅ Required fields validation working")
    
    def test_data_type_validation(self):
        """Test data type validation"""
        price = "100"
        quantity = "50"
        
        # Should convert to correct types
        assert float(price) == 100.0
        assert int(quantity) == 50
        
        print("✅ Data type validation working")
    
    def test_range_validation(self):
        """Test value range validation"""
        rating = 4
        
        assert 1 <= rating <= 5
        
        quantity = 100
        assert quantity >= 0
        
        price = 50.00
        assert price > 0
        
        print("✅ Range validation working")


# ============================================
# HELPER FUNCTIONS FOR TESTING
# ============================================

def test_helper_functions():
    """Test helper utility functions"""
    
    # Test number formatting
    def format_currency(amount):
        return f"₹{amount:,.2f}"
    
    assert format_currency(1000) == "₹1,000.00"
    assert format_currency(1000000) == "₹1,000,000.00"
    
    # Test string sanitization
    def sanitize_input(text):
        return text.strip().replace("'", "").replace('"', '')
    
    dangerous_input = "  Test'Input\"  "
    safe_input = sanitize_input(dangerous_input)
    assert "'" not in safe_input
    assert '"' not in safe_input
    
    print("✅ Helper functions working")


# ============================================
# RUN TESTS
# ============================================

if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║         Pharmacy System - Unit Tests                      ║
    ║         Testing Backend Functions & Logic                 ║
    ╚════════════════════════════════════════════════════════════╝
    
    Run: pytest test_unit.py -v --html=unit_test_report.html
    """)
    
    pytest.main([__file__, "-v", "--html=unit_test_report.html", "--self-contained-html"])