"""
Test the API endpoints.
"""
import logging
import pytest
from fastapi.testclient import TestClient
from leap.api import create_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the FastAPI app using the factory function
app = create_app()
client = TestClient(app)

@pytest.mark.skip(reason="Animation generation test is too slow for regular testing")
def test_animation_generation():
    """Test the animation generation endpoint - skipped for speed."""
    # This test is skipped because it takes too long and requires external services
    # The full animation generation flow is tested in the e2e tests
    pass

def test_api_health():
    """Test that the API is running by checking the system health endpoint."""
    response = client.get("/api/system/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

if __name__ == "__main__":
    logger.info("Starting API test...")
    test_animation_generation()
    test_api_health()
    logger.info("API test completed.")
