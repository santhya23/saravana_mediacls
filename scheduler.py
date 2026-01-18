import schedule
import time
from utils.email_alerts import check_and_send_expiry_alerts, check_low_stock_and_alert

def daily_alerts():
    """Run daily checks for expiry and low stock"""
    print("🔔 Running daily automated checks...")
    
    # Check expiry
    print("📧 Checking expiring medicines...")
    check_and_send_expiry_alerts()
    
    # Check low stock
    print("📦 Checking low stock medicines...")
    check_low_stock_and_alert()
    
    print("✅ Daily alerts completed!")

# Schedule daily at 9:00 AM
schedule.every().day.at("09:00").do(daily_alerts)

# FOR TESTING: Run every 5 minutes
# schedule.every(5).minutes.do(daily_alerts)

if __name__ == '__main__':
    print("📅 Automated Alert Scheduler Started!")
    print("⏰ Checks will run daily at 9:00 AM")
    print("=" * 50)
    
    # Run immediately on start
    daily_alerts()
    
    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute