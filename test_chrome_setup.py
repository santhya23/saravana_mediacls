from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

try:
    # ChromeDriver setup
    driver = webdriver.Chrome()
    
    print("✅ ChromeDriver working!")
    print(f"✅ Chrome version: {driver.capabilities['browserVersion']}")
    
    # Open Google
    driver.get("https://www.google.com")
    print("✅ Browser opened successfully!")
    
    time.sleep(3)
    
    driver.quit()
    print("✅ Test completed successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Check if chromedriver.exe is in project folder")
    print("2. Check Chrome and ChromeDriver versions match")
    print("3. Run: pip install selenium")