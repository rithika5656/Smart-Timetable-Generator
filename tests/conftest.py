"""
Pytest configuration and fixtures.
"""
import pytest
from app import app
from models import DayOfWeek, ClassSession

@pytest.fixture
def client():
    """Florence test client fixture."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def api_headers():
    return {"X-API-Key": "dev-api-key"}

@pytest.fixture
def sample_data():
    """Sample data for testing."""
    return {
        "subjects": ["Math", "Physics", "Chemistry"],
        "teachers": ["Mr. A", "Ms. B", "Dr. C"],
        "periods": 6
    }
