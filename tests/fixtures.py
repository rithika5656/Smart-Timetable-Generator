"""
Shared test fixtures.
"""
import pytest

@pytest.fixture
def sample_subjects():
    return ["Math", "Physics", "Chemistry"]

@pytest.fixture
def sample_teachers():
    return ["Mr. A", "Ms. B", "Dr. C"]

@pytest.fixture
def api_headers():
    return {"X-API-Key": "dev-api-key"}
