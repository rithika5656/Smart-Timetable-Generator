"""
Integration tests for the Flask application.
"""
from http import HTTPStatus

def test_health_check(client):
    """Test /health endpoint."""
    response = client.get("/health")
    assert response.status_code == HTTPStatus.OK
    assert response.json["status"] == "healthy"

def test_info(client):
    """Test /info endpoint."""
    response = client.get("/info")
    assert response.status_code == HTTPStatus.OK
    assert "version" in response.json

def test_generate_success(client, sample_data):
    """Test successful timetable generation."""
    payload = {
        "subjects": ",".join(sample_data["subjects"]),
        "teachers": ",".join(sample_data["teachers"]),
        "periods_per_day": 6
    }
    response = client.post("/generate", json=payload)
    assert response.status_code == HTTPStatus.OK
    assert "timetable" in response.json
    assert response.json["meta"]["status"] == "success"

def test_generate_validation_error(client):
    """Test validation failure."""
    payload = {"subjects": "", "teachers": ""}
    response = client.post("/generate", json=payload)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "error" in response.json

def test_validate_endpoint(client):
    """
    Test /validate endpoint.
    Ensures that valid input returns 'valid': True.
    """
    payload = {"subjects": "Math,History", "teachers": "A,B", "periods_per_day": 5}
    response = client.post("/validate", json=payload)
    assert response.status_code == 200
    assert response.json["valid"] is True
