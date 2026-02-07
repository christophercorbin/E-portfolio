"""Integration tests for deployed backend API.

These tests verify the actual deployed API endpoints are working correctly.
They should be run after deployment to validate the live system.
"""

import os
import sys
import requests
import pytest
from datetime import datetime


# Test configuration
API_URL = os.environ.get("API_URL", "")
TIMEOUT = 30  # seconds


@pytest.fixture
def valid_contact_data():
    """Fixture for valid contact form data."""
    return {
        "name": f"Integration Test User {datetime.utcnow().isoformat()}",
        "email": "integration-test@example.com",
        "message": "This is an automated integration test message. Please ignore.",
    }


class TestDeployedAPI:
    """Integration tests for deployed API endpoints."""

    def test_api_url_configured(self):
        """Test that API_URL environment variable is set."""
        assert API_URL, "API_URL environment variable must be set for integration tests"
        assert API_URL.startswith("https://"), f"API_URL must be HTTPS, got: {API_URL}"
        print(f"✅ Testing API at: {API_URL}")

    def test_api_health_check(self):
        """Test basic API connectivity."""
        if not API_URL:
            pytest.skip("API_URL not configured")

        try:
            # Make a simple request to check if API is reachable
            response = requests.options(API_URL, timeout=TIMEOUT)
            assert response.status_code in [200, 204], f"API health check failed: {response.status_code}"
            print("✅ API is reachable")
        except requests.exceptions.RequestException as e:
            pytest.fail(f"API health check failed: {str(e)}")

    def test_cors_headers_present(self):
        """Test that CORS headers are properly configured."""
        if not API_URL:
            pytest.skip("API_URL not configured")

        response = requests.options(API_URL, headers={"Origin": "https://example.com"}, timeout=TIMEOUT)

        assert "access-control-allow-origin" in [
            h.lower() for h in response.headers
        ], "CORS Access-Control-Allow-Origin header missing"
        assert "access-control-allow-methods" in [
            h.lower() for h in response.headers
        ], "CORS Access-Control-Allow-Methods header missing"

        print("✅ CORS headers properly configured")

    def test_post_contact_form_success(self, valid_contact_data):
        """Test successful contact form submission."""
        if not API_URL:
            pytest.skip("API_URL not configured")

        response = requests.post(
            API_URL, json=valid_contact_data, headers={"Content-Type": "application/json"}, timeout=TIMEOUT
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"

        data = response.json()
        assert "message" in data, "Response should contain 'message' field"
        assert "submissionId" in data, "Response should contain 'submissionId' field"
        assert len(data["submissionId"]) > 0, "submissionId should not be empty"

        print(f"✅ Contact form submission successful: {data['submissionId']}")

    def test_post_missing_name(self):
        """Test API validation for missing name."""
        if not API_URL:
            pytest.skip("API_URL not configured")

        data = {"email": "test@example.com", "message": "Test message without name"}

        response = requests.post(API_URL, json=data, headers={"Content-Type": "application/json"}, timeout=TIMEOUT)

        assert response.status_code == 400, f"Should reject missing name, got {response.status_code}"

        error_data = response.json()
        assert "error" in error_data, "Error response should contain 'error' field"
        assert "name" in error_data["error"].lower(), "Error should mention 'name'"

        print("✅ Validation correctly rejects missing name")

    def test_post_invalid_email(self):
        """Test API validation for invalid email format."""
        if not API_URL:
            pytest.skip("API_URL not configured")

        data = {"name": "Test User", "email": "invalid-email", "message": "Test message with invalid email"}

        response = requests.post(API_URL, json=data, headers={"Content-Type": "application/json"}, timeout=TIMEOUT)

        assert response.status_code == 400, f"Should reject invalid email, got {response.status_code}"

        error_data = response.json()
        assert "error" in error_data, "Error response should contain 'error' field"
        assert "email" in error_data["error"].lower(), "Error should mention 'email'"

        print("✅ Validation correctly rejects invalid email")

    def test_post_message_too_short(self):
        """Test API validation for message that's too short."""
        if not API_URL:
            pytest.skip("API_URL not configured")

        data = {"name": "Test User", "email": "test@example.com", "message": "Short"}  # Less than 10 characters

        response = requests.post(API_URL, json=data, headers={"Content-Type": "application/json"}, timeout=TIMEOUT)

        assert response.status_code == 400, f"Should reject short message, got {response.status_code}"

        error_data = response.json()
        assert "error" in error_data, "Error response should contain 'error' field"
        assert (
            "message" in error_data["error"].lower() or "character" in error_data["error"].lower()
        ), "Error should mention message length"

        print("✅ Validation correctly rejects short message")

    def test_post_spam_detection(self):
        """Test API spam detection."""
        if not API_URL:
            pytest.skip("API_URL not configured")

        data = {
            "name": "Spam User",
            "email": "spam@example.com",
            "message": "Buy viagra now! Amazing casino deals and bitcoin opportunities!",
        }

        response = requests.post(API_URL, json=data, headers={"Content-Type": "application/json"}, timeout=TIMEOUT)

        assert response.status_code == 400, f"Should reject spam message, got {response.status_code}"

        error_data = response.json()
        assert "error" in error_data, "Error response should contain 'error' field"
        assert "spam" in error_data["error"].lower(), "Error should mention 'spam'"

        print("✅ Spam detection working correctly")

    def test_response_time_acceptable(self, valid_contact_data):
        """Test that API response time is acceptable (< 5 seconds)."""
        if not API_URL:
            pytest.skip("API_URL not configured")

        import time

        start_time = time.time()

        # Make request (response not used, but request must complete for timing)
        requests.post(
            API_URL, json=valid_contact_data, headers={"Content-Type": "application/json"}, timeout=TIMEOUT
        )

        response_time = time.time() - start_time

        assert response_time < 5.0, f"API response too slow: {response_time:.2f}s (should be < 5s)"

        print(f"✅ API response time acceptable: {response_time:.2f}s")

    def test_concurrent_requests(self, valid_contact_data):
        """Test API can handle concurrent requests."""
        if not API_URL:
            pytest.skip("API_URL not configured")

        import concurrent.futures

        def make_request(index):
            data = valid_contact_data.copy()
            data["name"] = f"{data['name']} - Request {index}"
            response = requests.post(API_URL, json=data, headers={"Content-Type": "application/json"}, timeout=TIMEOUT)
            return response.status_code == 200

        # Make 5 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(make_request, range(5)))

        success_count = sum(results)
        assert success_count >= 4, f"Only {success_count}/5 concurrent requests succeeded"

        print(f"✅ Handled {success_count}/5 concurrent requests successfully")


class TestAPIMetrics:
    """Tests for API performance metrics."""

    def test_api_availability(self):
        """Test API uptime/availability."""
        if not API_URL:
            pytest.skip("API_URL not configured")

        # Make multiple requests to check consistency
        success_count = 0
        total_requests = 3
        error_count = 0

        for i in range(total_requests):
            try:
                response = requests.options(API_URL, timeout=TIMEOUT)
                if response.status_code in [200, 204]:
                    success_count += 1
            except requests.RequestException as exc:
                error_count += 1
                print(f"⚠️ API availability check attempt {i + 1} failed with exception: {exc}")

        availability = (success_count / total_requests) * 100
        assert availability >= 66.0, f"API availability too low: {availability:.1f}% (should be > 66%)"

        print(f"✅ API availability: {availability:.1f}% (errors: {error_count})")


def print_test_summary():
    """Print a summary of integration test results."""
    print("\n" + "=" * 60)
    print("Integration Test Summary")
    print("=" * 60)
    print(f"API URL: {API_URL if API_URL else 'NOT CONFIGURED'}")
    print(f"Timestamp: {datetime.utcnow().isoformat()}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    print_test_summary()
    sys.exit(pytest.main([__file__, "-v", "-s"]))
