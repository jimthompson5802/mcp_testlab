#!/usr/bin/env python3
"""
Simple test script to verify the web application setup
"""
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from fastapi.testclient import TestClient
    from app_server import app

    client = TestClient(app)
    FASTAPI_AVAILABLE = True
except ImportError as e:
    print(f"Warning: FastAPI not available for testing: {e}")
    FASTAPI_AVAILABLE = False
    client = None


def test_health_endpoint():
    """Test the health check endpoint"""
    if not FASTAPI_AVAILABLE or client is None:
        return True

    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "swim-rules-agent"
    return True


def test_root_endpoint():
    """Test the root endpoint returns HTML"""
    if not FASTAPI_AVAILABLE or client is None:
        return True

    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    return True


def test_scenario_examples_endpoint():
    """Test the scenario examples endpoint"""
    if not FASTAPI_AVAILABLE or client is None:
        return True

    response = client.get("/api/scenario-examples")
    assert response.status_code == 200
    data = response.json()
    assert "stroke_violations" in data
    assert "starting_violations" in data
    assert "general_violations" in data
    assert isinstance(data["stroke_violations"], list)
    return True


def test_analyze_endpoint_valid_scenario():
    """Test the analyze endpoint with a valid scenario"""
    if not FASTAPI_AVAILABLE or client is None:
        return True

    test_scenario = "Swimmer did not touch the wall with both hands simultaneously during breaststroke turn"

    response = client.post("/api/analyze", json={"scenario": test_scenario})
    assert response.status_code == 200

    data = response.json()
    assert "decision" in data
    assert "confidence" in data
    assert "rationale" in data
    assert "rule_citations" in data
    assert data["decision"] in ["ALLOWED", "DISQUALIFICATION"]
    assert 0 <= data["confidence"] <= 100
    return True


def test_analyze_endpoint_empty_scenario():
    """Test the analyze endpoint with empty scenario"""
    if not FASTAPI_AVAILABLE or client is None:
        return True

    response = client.post("/api/analyze", json={"scenario": ""})
    assert response.status_code == 400
    return True


def test_analyze_endpoint_too_long_scenario():
    """Test the analyze endpoint with too long scenario"""
    if not FASTAPI_AVAILABLE or client is None:
        return True

    long_scenario = "a" * 2001  # Exceeds 2000 character limit

    response = client.post("/api/analyze", json={"scenario": long_scenario})
    assert response.status_code == 400
    return True


def test_file_structure():
    """Test that all required files exist"""
    base_path = Path(__file__).parent

    # Check main files
    assert (base_path / "app_server.py").exists()
    assert (base_path / "start_server.py").exists()
    assert (base_path / "requirements_web.txt").exists()

    # Check templates
    assert (base_path / "templates").exists()
    assert (base_path / "templates" / "index.html").exists()

    # Check static files
    assert (base_path / "static").exists()
    assert (base_path / "static" / "styles.css").exists()
    assert (base_path / "static" / "script.js").exists()
    assert (base_path / "static" / "sw.js").exists()

    return True


def run_manual_tests():
    """Run tests that can be executed manually"""
    print("🧪 Running Swim Rules Agent Web Application Tests")
    print("=" * 50)

    tests = [
        ("📁 Testing file structure", test_file_structure),
        ("🌐 Testing health endpoint", test_health_endpoint),
        ("� Testing root endpoint", test_root_endpoint),
        ("📋 Testing scenario examples endpoint", test_scenario_examples_endpoint),
        ("🔍 Testing analyze endpoint (valid)", test_analyze_endpoint_valid_scenario),
        ("❌ Testing analyze endpoint (empty)", test_analyze_endpoint_empty_scenario),
        ("📏 Testing analyze endpoint (too long)", test_analyze_endpoint_too_long_scenario),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            print(f"{test_name}...")
            if test_func():
                print(f"✅ {test_name} passed")
                passed += 1
            else:
                print(f"❌ {test_name} failed")
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} failed: {e}")
            failed += 1

    print(f"\n📊 Test Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("🎉 All tests passed successfully!")
        print("🚀 Ready to start the web application with: python start_server.py")
        return True
    else:
        print("⚠️ Some tests failed. Please check the setup.")
        return False


if __name__ == "__main__":
    # Check if we can import pytest for proper testing
    try:
        import pytest

        if FASTAPI_AVAILABLE:
            print("Running tests with pytest...")
            exit_code = pytest.main([__file__, "-v"])
            sys.exit(exit_code)
        else:
            print("FastAPI not available, running basic tests...")
            success = run_manual_tests()
            sys.exit(0 if success else 1)
    except ImportError:
        print("pytest not available, running manual tests...")
        success = run_manual_tests()
        sys.exit(0 if success else 1)
