"""
Tests for API v1.
"""
import json
import pytest
from tests.fixtures import api_headers

def test_api_health(client):
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['data']['status'] == 'healthy'

def test_api_generate_unauthorized(client):
    response = client.post('/api/v1/generate', json={})
    assert response.status_code == 401

def test_api_generate_success(client, api_headers):
    payload = {
        "subjects": ["Math", "Physics"],
        "teachers": ["Mr. A", "Ms. B"],
        "periods": 4
    }
    response = client.post('/api/v1/generate', headers=api_headers, json=payload)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['data']['meta']['api_version'] == 'v1'
