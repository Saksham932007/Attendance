#!/usr/bin/env python3
import requests
import json
import time
import os
from pprint import pprint

# Get the backend URL from the frontend .env file
def get_backend_url():
    with open('/app/frontend/.env', 'r') as f:
        for line in f:
            if line.startswith('REACT_APP_BACKEND_URL='):
                return line.strip().split('=')[1].strip('"\'')
    return None

BACKEND_URL = get_backend_url()
if not BACKEND_URL:
    raise ValueError("Could not find REACT_APP_BACKEND_URL in frontend/.env")

API_BASE_URL = f"{BACKEND_URL}/api"
print(f"Using API base URL: {API_BASE_URL}")

# Test results tracking
test_results = {
    "total_tests": 0,
    "passed_tests": 0,
    "failed_tests": 0,
    "tests": []
}

def run_test(test_name, test_func):
    """Run a test and track results"""
    print(f"\n{'=' * 80}")
    print(f"RUNNING TEST: {test_name}")
    print(f"{'-' * 80}")
    
    test_results["total_tests"] += 1
    start_time = time.time()
    
    try:
        result = test_func()
        duration = time.time() - start_time
        
        if result:
            test_results["passed_tests"] += 1
            status = "PASSED"
        else:
            test_results["failed_tests"] += 1
            status = "FAILED"
            
        test_results["tests"].append({
            "name": test_name,
            "status": status,
            "duration": f"{duration:.2f}s"
        })
        
        print(f"{'-' * 80}")
        print(f"TEST RESULT: {status} ({duration:.2f}s)")
        return result
    
    except Exception as e:
        duration = time.time() - start_time
        test_results["failed_tests"] += 1
        test_results["tests"].append({
            "name": test_name,
            "status": "ERROR",
            "duration": f"{duration:.2f}s",
            "error": str(e)
        })
        
        print(f"{'-' * 80}")
        print(f"TEST ERROR: {str(e)} ({duration:.2f}s)")
        return False

def test_health_endpoint():
    """Test the health check endpoint"""
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print("Response:")
    pprint(response.json())
    
    # Verify response
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert response.json()["status"] == "healthy", "Health status should be 'healthy'"
    assert response.json()["service"] == "AI Attendance Analyzer", "Service name mismatch"
    
    return True

def test_sample_data_generation():
    """Test the sample data generation endpoint"""
    response = requests.get(f"{API_BASE_URL}/sample-data")
    print(f"Status Code: {response.status_code}")
    print("Response:")
    pprint(response.json())
    
    # Verify response
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert "message" in response.json(), "Response should contain 'message'"
    assert "employees_count" in response.json(), "Response should contain 'employees_count'"
    assert "records_count" in response.json(), "Response should contain 'records_count'"
    assert response.json()["employees_count"] == 5, "Should generate 5 employees"
    assert response.json()["records_count"] > 100, "Should generate multiple attendance records"
    
    return True

def test_dashboard_stats():
    """Test the dashboard stats endpoint"""
    response = requests.get(f"{API_BASE_URL}/dashboard-stats")
    print(f"Status Code: {response.status_code}")
    print("Response:")
    pprint(response.json())
    
    # Verify response
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert "employees_count" in response.json(), "Response should contain 'employees_count'"
    assert "records_count" in response.json(), "Response should contain 'records_count'"
    assert "has_analysis" in response.json(), "Response should contain 'has_analysis'"
    assert response.json()["employees_count"] == 5, "Should have 5 employees"
    assert response.json()["records_count"] > 100, "Should have multiple attendance records"
    
    return True

def test_analyze_attendance():
    """Test the attendance analysis endpoint"""
    response = requests.post(f"{API_BASE_URL}/analyze-attendance")
    print(f"Status Code: {response.status_code}")
    print("Response (summary):")
    
    # Verify response
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    data = response.json()
    assert "message" in data, "Response should contain 'message'"
    assert "summary" in data, "Response should contain 'summary'"
    assert "detailed_results" in data, "Response should contain 'detailed_results'"
    
    # Print summary
    pprint(data["summary"])
    
    # Print first result as sample
    print("\nSample Analysis Result:")
    if data["detailed_results"]:
        pprint(data["detailed_results"][0])
    
    # Verify detailed results
    assert len(data["detailed_results"]) == 5, "Should have 5 employee results"
    
    # Verify AI insights are present
    for result in data["detailed_results"]:
        assert "ai_insights" in result, "Each result should have AI insights"
        assert len(result["ai_insights"]) > 50, "AI insights should be substantial"
        assert "attendance_percentage" in result, "Each result should have attendance percentage"
        assert "status" in result, "Each result should have status"
        
        # Verify 70% threshold rule implementation
        if result["attendance_percentage"] >= 70:
            assert result["status"] == "meets_threshold", "Attendance >= 70% should meet threshold"
        else:
            assert result["status"] == "below_threshold", "Attendance < 70% should be below threshold"
    
    return True

def test_attendance_report():
    """Test the attendance report endpoint"""
    response = requests.get(f"{API_BASE_URL}/attendance-report")
    print(f"Status Code: {response.status_code}")
    print("Response (summary):")
    
    # Verify response
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    data = response.json()
    assert "summary" in data, "Response should contain 'summary'"
    assert "results" in data, "Response should contain 'results'"
    
    # Print summary
    pprint(data["summary"])
    
    # Verify results
    assert len(data["results"]) == 5, "Should have 5 employee results"
    
    # Verify summary statistics
    summary = data["summary"]
    assert "total_employees" in summary, "Summary should contain 'total_employees'"
    assert "meeting_70_percent_threshold" in summary, "Summary should contain 'meeting_70_percent_threshold'"
    assert "below_threshold" in summary, "Summary should contain 'below_threshold'"
    assert "average_attendance_rate" in summary, "Summary should contain 'average_attendance_rate'"
    
    # Verify consistency
    assert summary["total_employees"] == len(data["results"]), "Total employees should match results count"
    assert summary["meeting_70_percent_threshold"] + summary["below_threshold"] == summary["total_employees"], "Meeting + below should equal total"
    
    # Print first result as sample
    print("\nSample Report Result:")
    if data["results"]:
        pprint(data["results"][0])
    
    return True

def run_all_tests():
    """Run all tests in sequence"""
    print("\n" + "=" * 80)
    print("STARTING BACKEND API TESTS")
    print("=" * 80)
    
    # Run tests in the correct sequence
    health_check = run_test("Health Check Endpoint", test_health_endpoint)
    
    if health_check:
        sample_data = run_test("Sample Data Generation", test_sample_data_generation)
        
        if sample_data:
            dashboard = run_test("Dashboard Statistics", test_dashboard_stats)
            analysis = run_test("AI Attendance Analysis", test_analyze_attendance)
            
            if analysis:
                report = run_test("Attendance Report", test_attendance_report)
    
    # Print summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {test_results['total_tests']}")
    print(f"Passed: {test_results['passed_tests']}")
    print(f"Failed: {test_results['failed_tests']}")
    print("-" * 80)
    
    for test in test_results["tests"]:
        status_display = "✅" if test["status"] == "PASSED" else "❌"
        print(f"{status_display} {test['name']} - {test['status']} ({test['duration']})")
        if test["status"] == "ERROR" and "error" in test:
            print(f"   Error: {test['error']}")
    
    print("=" * 80)
    
    return test_results["failed_tests"] == 0

if __name__ == "__main__":
    run_all_tests()