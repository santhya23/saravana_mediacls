# Test Runner Script
# File: run_tests.py
# This script runs all tests and generates comprehensive reports

import subprocess
import sys
import os
from datetime import datetime
import json

class TestRunner:
    """Automated test runner for Pharmacy System"""
    
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'tests': {}
        }
    
    def print_header(self, text):
        """Print formatted header"""
        print("\n" + "="*70)
        print(f"  {text}")
        print("="*70 + "\n")
    
    def run_unit_tests(self):
        """Run unit tests"""
        self.print_header("Running Unit Tests")
        
        try:
            result = subprocess.run(
                ['pytest', 'test_unit.py', '-v', '--html=reports/unit_test_report.html', '--self-contained-html'],
                capture_output=True,
                text=True
            )
            
            print(result.stdout)
            
            self.results['tests']['unit'] = {
                'status': 'passed' if result.returncode == 0 else 'failed',
                'return_code': result.returncode
            }
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ Error running unit tests: {e}")
            self.results['tests']['unit'] = {'status': 'error', 'error': str(e)}
            return False
    
    def run_selenium_tests(self):
        """Run Selenium automation tests"""
        self.print_header("Running Selenium UI Tests")
        
        print("⚠️  Make sure your Flask app is running on http://localhost:5000")
        print("Press Enter to continue or Ctrl+C to cancel...")
        try:
            input()
        except KeyboardInterrupt:
            print("\n❌ Selenium tests cancelled")
            return False
        
        try:
            result = subprocess.run(
                ['pytest', 'test_pharmacy_system.py', '-v', '--html=reports/selenium_test_report.html', '--self-contained-html'],
                capture_output=True,
                text=True
            )
            
            print(result.stdout)
            
            self.results['tests']['selenium'] = {
                'status': 'passed' if result.returncode == 0 else 'failed',
                'return_code': result.returncode
            }
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ Error running Selenium tests: {e}")
            self.results['tests']['selenium'] = {'status': 'error', 'error': str(e)}
            return False
    
    def check_code_quality(self):
        """Run code quality checks"""
        self.print_header("Running Code Quality Checks")
        
        # Check if pylint is installed
        try:
            subprocess.run(['pylint', '--version'], capture_output=True, check=True)
            has_pylint = True
        except:
            has_pylint = False
            print("⚠️  pylint not installed. Run: pip install pylint")
        
        if has_pylint:
            print("Running pylint...")
            result = subprocess.run(
                ['pylint', 'app.py', '--output-format=text'],
                capture_output=True,
                text=True
            )
            print(result.stdout[:1000])  # Print first 1000 chars
        
        print("✅ Code quality check completed")
    
    def check_dependencies(self):
        """Check if all dependencies are installed"""
        self.print_header("Checking Dependencies")
        
        required_packages = [
            'pytest',
            'selenium',
            'pytest-html',
            'flask',
            'flask-mysqldb'
        ]
        
        missing = []
        
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
                print(f"✅ {package}")
            except ImportError:
                print(f"❌ {package} - NOT INSTALLED")
                missing.append(package)
        
        if missing:
            print(f"\n⚠️  Missing packages: {', '.join(missing)}")
            print(f"Install with: pip install {' '.join(missing)}")
            return False
        
        print("\n✅ All dependencies installed")
        return True
    
    def generate_summary(self):
        """Generate test summary"""
        self.print_header("Test Summary")
        
        total_tests = len(self.results['tests'])
        passed_tests = sum(1 for t in self.results['tests'].values() if t['status'] == 'passed')
        failed_tests = sum(1 for t in self.results['tests'].values() if t['status'] == 'failed')
        
        print(f"Timestamp: {self.results['timestamp']}")
        print(f"Total Test Suites: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        
        print("\nDetailed Results:")
        for test_name, result in self.results['tests'].items():
            status_emoji = "✅" if result['status'] == 'passed' else "❌"
            print(f"  {status_emoji} {test_name.upper()}: {result['status'].upper()}")
        
        # Save results to file
        os.makedirs('reports', exist_ok=True)
        with open('reports/test_summary.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print("\n📊 Reports saved in 'reports/' directory")
        print("   - unit_test_report.html")
        print("   - selenium_test_report.html")
        print("   - test_summary.json")
    
    def run_all(self):
        """Run all tests"""
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║       🧪 Pharmacy Inventory Management System                   ║
║          Comprehensive Testing Suite                            ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
        """)
        
        # Check dependencies first
        if not self.check_dependencies():
            print("\n❌ Please install missing dependencies before running tests")
            return
        
        # Create reports directory
        os.makedirs('reports', exist_ok=True)
        
        # Run tests
        print("\n🚀 Starting test execution...\n")
        
        self.run_unit_tests()
        self.run_selenium_tests()
        self.check_code_quality()
        
        # Generate summary
        self.generate_summary()
        
        print("\n✅ Testing completed!")


# ============================================
# QUICK TEST COMMANDS
# ============================================

def print_quick_commands():
    """Print quick test commands"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                    Quick Test Commands                           ║
╚══════════════════════════════════════════════════════════════════╝

1. Run All Tests:
   python run_tests.py

2. Run Unit Tests Only:
   pytest test_unit.py -v

3. Run Selenium Tests Only:
   pytest test_pharmacy_system.py -v

4. Run Specific Test:
   pytest test_unit.py::TestMedicineOperations::test_medicine_validation -v

5. Run with HTML Report:
   pytest test_unit.py --html=report.html --self-contained-html

6. Run with Coverage:
   pytest --cov=app --cov-report=html

7. Run Tests in Parallel (faster):
   pytest -n auto

8. Run and Stop on First Failure:
   pytest -x

9. Run Only Failed Tests:
   pytest --lf

10. Run Tests Matching Pattern:
    pytest -k "medicine" -v

╔══════════════════════════════════════════════════════════════════╗
║                  Installation Commands                           ║
╚══════════════════════════════════════════════════════════════════╝

Install Testing Dependencies:
pip install pytest selenium pytest-html pytest-cov

Install ChromeDriver:
# For Windows:
1. Download from: https://chromedriver.chromium.org/
2. Add to PATH or place in project folder

# For Linux:
sudo apt-get install chromium-chromedriver

# For Mac:
brew install chromedriver

╔══════════════════════════════════════════════════════════════════╗
║                     Project Structure                            ║
╚══════════════════════════════════════════════════════════════════╝

pharmacy-system/
│
├── app.py                          # Your Flask application
├── test_pharmacy_system.py         # Selenium tests
├── test_unit.py                    # Unit tests
├── run_tests.py                    # This test runner
├── pytest.ini                      # Pytest configuration
│
├── reports/                        # Test reports directory
│   ├── unit_test_report.html
│   ├── selenium_test_report.html
│   └── test_summary.json
│
└── templates/                      # Your HTML templates
    └── ...

    """)


# ============================================
# CONFIGURATION FILE CONTENT
# ============================================

PYTEST_INI_CONTENT = """# pytest.ini - Pytest Configuration
[pytest]
# Test discovery patterns
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Output options
addopts = 
    -v
    --strict-markers
    --tb=short
    --disable-warnings

# Markers for organizing tests
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    unit: unit tests
    integration: integration tests
    selenium: selenium UI tests
    smoke: smoke tests for critical functionality
    
# Test paths
testpaths = .

# Logging
log_cli = true
log_cli_level = INFO
log_cli_format = %(asctime)s [%(levelname)8s] %(message)s
log_cli_date_format = %Y-%m-%d %H:%M:%S

# Coverage options (if pytest-cov installed)
# Run with: pytest --cov
[coverage:run]
omit = 
    */tests/*
    */venv/*
    */__pycache__/*
"""

# ============================================
# REQUIREMENTS FILE
# ============================================

REQUIREMENTS_TEST = """# requirements-test.txt
# Testing dependencies for Pharmacy Management System

pytest==7.4.3
pytest-html==4.1.1
pytest-cov==4.1.0
pytest-xdist==3.5.0
selenium==4.15.2
pylint==3.0.3
coverage==7.3.2
"""


def create_config_files():
    """Create configuration files"""
    print("Creating configuration files...")
    
    # Create pytest.ini
    with open('pytest.ini', 'w') as f:
        f.write(PYTEST_INI_CONTENT)
    print("✅ Created pytest.ini")
    
    # Create requirements-test.txt
    with open('requirements-test.txt', 'w') as f:
        f.write(REQUIREMENTS_TEST)
    print("✅ Created requirements-test.txt")
    
    # Create reports directory
    os.makedirs('reports', exist_ok=True)
    print("✅ Created reports directory")
    
    print("\n✅ Configuration files created successfully!")


# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == '--help':
            print_quick_commands()
        elif sys.argv[1] == '--setup':
            create_config_files()
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Use --help for available commands")
    else:
        runner = TestRunner()
        runner.run_all()