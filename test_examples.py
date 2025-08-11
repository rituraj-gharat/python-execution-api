#!/usr/bin/env python3
"""
Test examples for the Python Code Execution Service
"""

import requests
import json

# Test server URL (change this to your deployed URL)
BASE_URL = "http://localhost:8080"

def test_basic_execution():
    """Test basic script execution"""
    script = """
def main():
    return {"message": "Hello World", "numbers": [1, 2, 3, 4, 5]}
"""
    
    response = requests.post(f"{BASE_URL}/execute", 
                           json={"script": script})
    print("Basic Execution Test:")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

def test_data_science():
    """Test data science libraries"""
    script = """
import pandas as pd
import numpy as np

def main():
    # Create sample data
    data = {
        'name': ['Alice', 'Bob', 'Charlie', 'David'],
        'age': [25, 30, 35, 40],
        'salary': [50000, 60000, 70000, 80000]
    }
    df = pd.DataFrame(data)
    
    # Calculate statistics
    stats = {
        'mean_age': float(df['age'].mean()),
        'total_salary': float(df['salary'].sum()),
        'count': len(df),
        'numpy_sum': float(np.sum([1, 2, 3, 4, 5]))
    }
    
    return stats
"""
    
    response = requests.post(f"{BASE_URL}/execute", 
                           json={"script": script})
    print("Data Science Test:")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

def test_error_handling():
    """Test error handling"""
    script = """
def main():
    try:
        result = 10 / 0
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
"""
    
    response = requests.post(f"{BASE_URL}/execute", 
                           json={"script": script})
    print("Error Handling Test:")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

def test_invalid_script():
    """Test invalid script handling"""
    script = """
def main():
    return "This is not JSON"
"""
    
    response = requests.post(f"{BASE_URL}/execute", 
                           json={"script": script})
    print("Invalid Script Test:")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

def test_health_check():
    """Test health check endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check Test:")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

if __name__ == "__main__":
    print("Testing Python Code Execution Service")
    print("=" * 50)
    
    try:
        test_health_check()
        test_basic_execution()
        test_data_science()
        test_error_handling()
        test_invalid_script()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the service.")
        print("Make sure the service is running on localhost:8080")
    except Exception as e:
        print(f"Error: {e}") 