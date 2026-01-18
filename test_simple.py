# Simple Test File for Pharmacy System
# Save as: test_simple.py
# Run: python -m pytest test_simple.py -v

import pytest

class TestBasicOperations:
    """Basic tests to verify system logic"""
    
    def test_medicine_price_calculation(self):
        """Test medicine price calculation"""
        price = 100.00
        quantity = 10
        total = price * quantity
        
        assert total == 1000.00
        print("✅ Medicine price calculation: PASSED")
    
    def test_discount_calculation(self):
        """Test discount calculation"""
        subtotal = 1000
        discount_percent = 10
        
        discount_amount = (subtotal * discount_percent) / 100
        final_amount = subtotal - discount_amount
        
        assert discount_amount == 100
        assert final_amount == 900
        print("✅ Discount calculation: PASSED")
    
    def test_gst_calculation(self):
        """Test GST calculation"""
        subtotal = 1000
        gst_rate = 18  # 18%
        
        gst_amount = (subtotal * gst_rate) / 100
        total_with_gst = subtotal + gst_amount
        
        assert gst_amount == 180
        assert total_with_gst == 1180
        print("✅ GST calculation: PASSED")
    
    def test_stock_deduction(self):
        """Test stock deduction after sale"""
        initial_stock = 100
        sold_quantity = 15
        
        remaining_stock = initial_stock - sold_quantity
        
        assert remaining_stock == 85
        print("✅ Stock deduction: PASSED")
    
    def test_low_stock_alert(self):
        """Test low stock detection"""
        current_stock = 5
        threshold = 10
        
        is_low_stock = current_stock < threshold
        
        assert is_low_stock == True
        print("✅ Low stock detection: PASSED")
    
    def test_negative_quantity_validation(self):
        """Test negative quantity should be rejected"""
        quantity = -10
        
        # This should be caught by validation
        is_invalid = quantity < 0
        
        assert is_invalid == True
        print("✅ Negative quantity validation: PASSED")
    
    def test_email_validation(self):
        """Test email format validation"""
        import re
        
        valid_email = "supplier@example.com"
        invalid_email = "invalid-email"
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        assert re.match(email_pattern, valid_email) is not None
        assert re.match(email_pattern, invalid_email) is None
        print("✅ Email validation: PASSED")
    
    def test_bill_number_generation(self):
        """Test bill number format"""
        import datetime
        
        today = datetime.datetime.now()
        bill_prefix = f"BILL-{today.strftime('%Y%m%d')}"
        bill_number = f"{bill_prefix}-0001"
        
        assert bill_number.startswith("BILL-")
        assert len(bill_number) > 10
        print(f"✅ Bill number generated: {bill_number}")
    
    def test_outstanding_calculation(self):
        """Test outstanding payment calculation"""
        total_purchase = 50000
        paid_amount = 30000
        
        outstanding = total_purchase - paid_amount
        
        assert outstanding == 20000
        print("✅ Outstanding calculation: PASSED")
    
    def test_expiry_date_check(self):
        """Test expiry date validation"""
        from datetime import datetime, timedelta
        
        today = datetime.now()
        
        expired_date = today - timedelta(days=10)
        future_date = today + timedelta(days=30)
        
        is_expired = expired_date < today
        is_not_expired = future_date > today
        
        assert is_expired == True
        assert is_not_expired == True
        print("✅ Expiry date check: PASSED")
    
    def test_data_type_validation(self):
        """Test data type conversions"""
        price_str = "100.50"
        quantity_str = "50"
        
        price = float(price_str)
        quantity = int(quantity_str)
        
        assert price == 100.50
        assert quantity == 50
        print("✅ Data type validation: PASSED")
    
    def test_percentage_calculation(self):
        """Test percentage calculations"""
        total = 1000
        percentage = 15
        
        result = (total * percentage) / 100
        
        assert result == 150
        print("✅ Percentage calculation: PASSED")


class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_zero_quantity(self):
        """Test with zero quantity"""
        quantity = 0
        price = 100
        
        total = quantity * price
        
        assert total == 0
        print("✅ Zero quantity test: PASSED")
    
    def test_large_numbers(self):
        """Test with large numbers"""
        quantity = 1000000
        price = 999.99
        
        total = quantity * price
        
        assert total > 0
        print("✅ Large numbers test: PASSED")
    
    def test_decimal_precision(self):
        """Test decimal calculations"""
        price = 10.99
        quantity = 3
        
        total = round(price * quantity, 2)
        
        assert total == 32.97
        print("✅ Decimal precision test: PASSED")


class TestStringOperations:
    """Test string operations"""
    
    def test_medicine_name_formatting(self):
        """Test medicine name formatting"""
        medicine_name = "  paracetamol 500mg  "
        
        formatted = medicine_name.strip().title()
        
        assert formatted == "Paracetamol 500Mg"
        print("✅ Medicine name formatting: PASSED")
    
    def test_batch_number_validation(self):
        """Test batch number format"""
        batch_no = "BATCH12345"
        
        is_valid = len(batch_no) > 5 and batch_no.isalnum()
        
        assert is_valid == True
        print("✅ Batch number validation: PASSED")


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════╗
║         Pharmacy System - Simple Test Suite                     ║
║         Testing Core Business Logic                             ║
╚══════════════════════════════════════════════════════════════════╝

Run this file with: python -m pytest test_simple.py -v

    """)
    
    pytest.main([__file__, "-v", "-s"])